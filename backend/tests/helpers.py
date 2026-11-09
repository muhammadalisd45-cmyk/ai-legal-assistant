"""Test utilities: tiny valid PDFs, mock LLM transports, fixture corpus."""
from __future__ import annotations

import json

import httpx


def make_pdf(pages: list[str], javascript: bool = False) -> bytes:
    """Build a small, valid, text-bearing PDF (Helvetica, one text block per page)."""
    objects: list[bytes] = []

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    pages_id_placeholder = len(objects) + 1 + 2 * len(pages)  # computed below
    content_ids = []
    for text in pages:
        lines = text.split("\n")
        ops = ["BT", "/F1 11 Tf", "14 TL", "50 780 Td"]
        for line in lines:
            safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"({safe}) Tj T*")
        ops.append("ET")
        stream = "\n".join(ops).encode("latin-1", "replace")
        content_ids.append(add(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"))
    for cid in content_ids:
        page_ids.append(add(
            b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>"
            % (pages_id_placeholder, font, cid)))
    kids = b" ".join(b"%d 0 R" % pid for pid in page_ids)
    pages_id = add(b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, len(page_ids)))
    assert pages_id == pages_id_placeholder
    extra = b" /OpenAction << /S /JavaScript /JS (app.alert\\(1\\)) >>" if javascript else b""
    catalog = add(b"<< /Type /Catalog /Pages %d 0 R%s >>" % (pages_id, extra))

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, catalog, xref)
    return bytes(out)


def chat_completion(payload: dict) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": json.dumps(payload, ensure_ascii=False)}}]}


class ScriptedLLM(httpx.AsyncBaseTransport):
    """Replays a list of responses (dict → 200 JSON completion, int → HTTP status, Exception → raised)."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests: list[dict] = []

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(json.loads(request.content or b"{}"))
        item = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
        if isinstance(item, Exception):
            raise item
        if isinstance(item, int):
            return httpx.Response(item, json={"error": "scripted"})
        if isinstance(item, str):
            return httpx.Response(200, json={"choices": [{"message": {"content": item}}]})
        return httpx.Response(200, json=chat_completion(item))


FIXTURE_CHUNKS = [
    {
        "chunk_id": "PK-003-section-497-p0167-c00", "document_id": "PK-003", "title": "Code of Criminal Procedure, 1898",
        "document_type": "Federal Act", "jurisdiction": "Federal", "court": "", "bench": "", "authority": "Parliament of Pakistan",
        "citation": "", "section_or_article": "Section 497", "section_heading": "When bail may be taken in case of non-bailable offence",
        "section_confidence": "high", "page_start": 167, "page_end": 168, "source_name": "Pakistan Code",
        "source_url": "https://pakistancode.gov.pk/pdffiles/crpc.pdf", "source_tier": 1,
        "content": "497. When bail may be taken in case of non-bailable offence. (1) When any person accused of non-bailable "
                   "offence is arrested or detained without warrant by an officer in charge of a police station, he may be "
                   "released on bail, but he shall not be so released if there appear reasonable grounds for believing that "
                   "he has been guilty of an offence punishable with death or imprisonment for life.",
        "file_sha256": "abc", "fetched_at": "2026-11-08T00:00:00+00:00",
    },
    {
        "chunk_id": "PK-003-section-154-p0079-c00", "document_id": "PK-003", "title": "Code of Criminal Procedure, 1898",
        "document_type": "Federal Act", "jurisdiction": "Federal", "court": "", "bench": "", "authority": "Parliament of Pakistan",
        "citation": "", "section_or_article": "Section 154", "section_heading": "Information in cognizable cases",
        "section_confidence": "high", "page_start": 79, "page_end": 79, "source_name": "Pakistan Code",
        "source_url": "https://pakistancode.gov.pk/pdffiles/crpc.pdf", "source_tier": 1,
        "content": "154. Information in cognizable cases. Every information relating to the commission of a cognizable offence "
                   "if given orally to an officer in charge of a police station, shall be reduced to writing by him or under "
                   "his direction, and be read over to the informant.",
        "file_sha256": "abc", "fetched_at": "2026-11-08T00:00:00+00:00",
    },
    {
        "chunk_id": "PK-007-section-9-p0004-c00", "document_id": "PK-007", "title": "Specific Relief Act, 1877",
        "document_type": "Federal Act", "jurisdiction": "Federal", "court": "", "bench": "", "authority": "Parliament of Pakistan",
        "citation": "", "section_or_article": "Section 9", "section_heading": "Suit by person dispossessed of immovable property",
        "section_confidence": "high", "page_start": 4, "page_end": 4, "source_name": "Pakistan Code",
        "source_url": "https://pakistancode.gov.pk/pdffiles/sra.pdf", "source_tier": 1,
        "content": "9. Suit by person dispossessed of immovable property. If any person is dispossessed without his consent of "
                   "immovable property otherwise than in due course of law, he or any person claiming through him may, by "
                   "suit, recover possession thereof, notwithstanding any other title that may be set up in such suit.",
        "file_sha256": "def", "fetched_at": "2026-11-08T00:00:00+00:00",
    },
    {
        "chunk_id": "PK-001-article-10a-p0023-c00", "document_id": "PK-001",
        "title": "Constitution of the Islamic Republic of Pakistan, 1973", "document_type": "Constitution",
        "jurisdiction": "Federal", "court": "", "bench": "", "authority": "Parliament of Pakistan", "citation": "",
        "section_or_article": "Article 10A", "section_heading": "Right to fair trial", "section_confidence": "high",
        "page_start": 23, "page_end": 23, "source_name": "Pakistan Code",
        "source_url": "https://pakistancode.gov.pk/pdffiles/constitution.pdf", "source_tier": 1,
        "content": "10A. Right to fair trial. For the determination of his civil rights and obligations or in any criminal "
                   "charge against him a person shall be entitled to a fair trial and due process.",
        "file_sha256": "ghi", "fetched_at": "2026-11-08T00:00:00+00:00",
    },
]
for _chunk in FIXTURE_CHUNKS:
    import hashlib as _hashlib

    _chunk["content_hash"] = _hashlib.sha256(_chunk["content"].encode("utf-8")).hexdigest()
