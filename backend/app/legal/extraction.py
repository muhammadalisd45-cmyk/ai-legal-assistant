"""PDF text extraction and cleaning that preserves page numbers and section boundaries."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader

_PAGE_HEADER = re.compile(r"^\s*Page\s+\d+\s+of\s+\d+\s*$", re.IGNORECASE | re.MULTILINE)
_BARE_PAGE_NO = re.compile(r"^\s*[-–]?\s*\d{1,4}\s*[-–]?\s*$", re.MULTILINE)
_SOFT_HYPHEN_BREAK = re.compile(r"(\w)[�­-]\s*\n\s*([a-z])")
_APOSTROPHE = re.compile(r"(\w)�(s|t|ll|re|ve|d|m)\b")
_DASH_AFTER_HEADING = re.compile(r"\.\s*(?:�|_{2,}|—|--)\s*")
_SECTION_LINE = re.compile(
    r"^\s*(?P<mk>\d{1,2}\[)?(?P<num>\d{1,4}(?: ?[A-Z]{1,2})?)(?P<sep>[.,])\s+(?:—\s*)?(?P<title>[A-Z\[][^\n]{2,220}?)"
    r"(?:\.\s*(?:—|_{1,2}|--)|\.(?=\s+[A-Z(\d\[])|:\s|\.\s*$|—|\n)",
    re.MULTILINE,
)
_NUMBERED_LINE = re.compile(r"^\s*(?:\d{1,2}\[)?\d{1,4}(?: ?[A-Z]{1,2})?\.\s+\S")
_SCHEDULE = re.compile(r"^\s*(?:THE\s+)?(?P<name>(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+)?"
                       r"SCHEDULE(?P<roman>\s+[IVX]{1,4})?\s*$", re.MULTILINE)
_ORDER = re.compile(r"^\s*ORDER\s+(?P<roman>[IVXLC]{1,7}(?:-?[A-Z])?)\s*$", re.MULTILINE)


@dataclass
class Page:
    number: int  # 1-based, as printed by PDF viewers (#page=N)
    text: str
    is_contents: bool = False


def clean_page_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\r", "\n")
    text = _PAGE_HEADER.sub("", text)
    text = _BARE_PAGE_NO.sub("", text)
    text = _SOFT_HYPHEN_BREAK.sub(r"\1\2", text)
    text = _APOSTROPHE.sub(r"\1'\2", text)
    text = _DASH_AFTER_HEADING.sub(". — ", text)
    text = text.replace("�", '"').replace("­", "-").replace(";", ";")
    text = re.sub(r"[ \t ]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _page_stats(text: str) -> tuple[int, int, float, float]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return 0, 0, 0.0, 0.0
    numbered = sum(1 for line in lines if _NUMBERED_LINE.match(line))
    avg_len = sum(len(line) for line in lines) / len(lines)
    prose_ratio = sum(1 for line in lines if len(line) >= 70) / len(lines)
    return len(lines), numbered, avg_len, prose_ratio


def looks_like_contents(text: str, previous_was_contents: bool = False) -> bool:
    count, numbered, avg_len, prose_ratio = _page_stats(text)
    if count < 6:
        return False
    has_contents_heading = bool(re.search(r"^\s*CONTENTS\s*$", text, re.MULTILINE))
    # TOC pages are dominated by short numbered heading lines without prose.
    if numbered / count >= 0.45 and avg_len < 75:
        return True
    # Weaker signal only for pages continuing a TOC run (schedule tables elsewhere also have short lines).
    if previous_was_contents and numbered >= 3 and prose_ratio < 0.3:
        return True
    return has_contents_heading and numbered / count >= 0.3


def extract_pages(path: Path, max_pages: int | None = None) -> list[Page]:
    reader = PdfReader(str(path))
    pages: list[Page] = []
    for index, page in enumerate(reader.pages, start=1):
        if max_pages and index > max_pages:
            break
        raw = page.extract_text() or ""
        cleaned = clean_page_text(raw)
        if cleaned:
            previous = bool(pages) and pages[-1].is_contents and pages[-1].number == index - 1
            pages.append(Page(number=index, text=cleaned, is_contents=looks_like_contents(cleaned, previous)))
    return pages


@dataclass
class SectionUnit:
    label: str        # "Section 3", "Article 10A", "First Schedule, Article 120", "Preamble"
    number: str
    heading: str
    text: str
    page_start: int
    page_end: int
    segments: list[tuple[int, str]] = field(default_factory=list)  # (page number, text on that page)


def _split_num(num: str) -> tuple[int, str]:
    compact = num.replace(" ", "")
    match = re.match(r"(\d+)([A-Z]*)$", compact)
    if not match:
        return 0, ""
    return int(match.group(1)), match.group(2)


def _key(value: int, suffix: str) -> tuple[int, str]:
    return value, suffix


def resolve_number(raw: str, last: tuple[int, str], gap: int = 60) -> str | None:
    """Pick the reading of a heading number that continues the sequence.

    PDF extraction fuses footnote superscripts onto headings ("28." = footnote 2 + section 8), so every
    candidate is also read with one or two leading digits removed. The reading closest to the expected
    next number wins; implausible jumps and backwards numbers (list items, cross-references) are rejected.
    """
    value, suffix = _split_num(raw)
    if value == 0 and not suffix:
        return None
    digits = str(value)
    readings = [(value, suffix)]
    for cut in (1, 2):
        if len(digits) > cut and digits[cut] != "0":
            readings.append((int(digits[cut:]), suffix))
    last_value, last_suffix = last

    def ok(reading: tuple[int, str]) -> bool:
        return _key(*reading) > _key(last_value, last_suffix)

    near = [r for r in readings if ok(r) and r[0] - last_value <= 3]
    if near:
        best = min(near, key=lambda r: (r[0] - last_value, len(r[1])))
        return f"{best[0]}{best[1]}"
    if ok(readings[0]) and readings[0][0] - last_value <= gap:
        return f"{value}{suffix}"
    return None


@dataclass
class _Event:
    page_index: int
    position: int
    kind: str          # "schedule" | "order" | "section"
    match: re.Match
    number: str | None = None
    label: str = ""


def _accept_jump(raw: str, last: tuple[int, str], following: list[_Event]) -> str | None:
    """Accept a larger forward jump (e.g. repealed ranges 266–336) when the next two headings continue it."""
    value, suffix = _split_num(raw)
    if (value, suffix) <= last:
        return None
    probe = (value, suffix)
    confirmations = 0
    for event in following[:6]:
        if event.kind != "section":
            break
        nxt = resolve_number(event.match.group("num"), probe, gap=5)
        if nxt is not None:
            confirmations += 1
            probe = _split_num(nxt)
            if confirmations >= 2:
                return f"{value}{suffix}"
    return None


def split_sections(pages: list[Page], unit_name: str = "Section") -> list[SectionUnit]:
    """Split body pages into provision units, starting a new unit at each accepted heading.

    Numbering restarts inside SCHEDULEs ("First Schedule, Article N") and CPC ORDERs ("Order XXXIX, Rule N");
    text after such a heading is never attributed to the preceding section.
    """
    body = [page for page in pages if not page.is_contents]
    events: list[_Event] = []
    for index, page in enumerate(body):
        found = [_Event(index, m.start(), "schedule", m) for m in _SCHEDULE.finditer(page.text)]
        found += [_Event(index, m.start(), "order", m) for m in _ORDER.finditer(page.text)]
        for m in _SECTION_LINE.finditer(page.text):
            if m.group("sep") == "," and not m.group("mk"):
                continue  # "1908, the ..." — a comma heading only occurs after an amendment marker "1[185, ..."
            found.append(_Event(index, m.start(), "section", m))
        events.extend(sorted(found, key=lambda e: e.position))

    # Pass 1: decide which events open a new unit.
    accepted: list[_Event] = []
    last: tuple[int, str] = (0, "")
    context: str | None = None
    for i, event in enumerate(events):
        if event.kind == "schedule":
            name = (event.match.group("name") or "").strip().title()
            roman = (event.match.group("roman") or "").strip()
            context = f"{name} Schedule".strip() if name else f"Schedule {roman}".strip()
            last = (0, "")
            event.label = context
            accepted.append(event)
            continue
        if event.kind == "order":
            context = f"Order {event.match.group('roman')}"
            last = (0, "")
            event.label = context
            accepted.append(event)
            continue
        raw = event.match.group("num")
        number = resolve_number(raw, last) or _accept_jump(raw, last, events[i + 1:])
        if number is None:
            continue
        event.number = number
        if context is None:
            event.label = f"{unit_name} {number}"
        elif context.startswith("Order"):
            event.label = f"{context}, Rule {number}"
        else:
            event.label = f"{context}, Article {number}"
        last = _split_num(number)
        accepted.append(event)

    # Pass 2: slice the page texts at accepted boundaries.
    units: list[SectionUnit] = []
    boundaries = [(e.page_index, e.position, e) for e in accepted]
    current = SectionUnit("Preamble", "", "", "", body[0].number if body else 1, body[0].number if body else 1)

    def append_text(unit: SectionUnit, text: str, page_number: int) -> None:
        if text.strip():
            if not unit.text:
                unit.page_start = page_number
            unit.text += ("\n" if unit.text else "") + text.strip()
            unit.page_end = page_number
            unit.segments.append((page_number, text.strip()))

    b = 0
    for index, page in enumerate(body):
        cursor = 0
        while b < len(boundaries) and boundaries[b][0] == index:
            _, position, event = boundaries[b]
            append_text(current, page.text[cursor:position], page.number)
            if current.text.strip():
                units.append(current)
            heading = event.match.group("title").strip().rstrip(".,;:") if event.kind == "section" else event.label
            current = SectionUnit(event.label, event.number or "", heading, "", page.number, page.number)
            cursor = position
            b += 1
        append_text(current, page.text[cursor:], page.number)
    if current.text.strip():
        units.append(current)
    for unit in units:
        unit.text = re.sub(r"\n{2,}", "\n\n", unit.text).strip()
    return units
