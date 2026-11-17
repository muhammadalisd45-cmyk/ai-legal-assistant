# Source sync pipeline: official law sources → inventory → corpus

The corpus must not go stale. This pipeline reads the **official** listing pages of Pakistan's law websites
on a schedule, keeps a complete inventory of every law they publish with its **direct PDF link**, detects what
changed, and (optionally) brings new and amended laws into the searchable corpus.

```
official_sources.csv ──► sync_sources.py ──► law_inventory.csv/.json  +  changes/<date>.json, changes.csv
 (registry: real            │  crawl listings        (every law, direct PDF link,
  listing URLs,             │  diff vs inventory      first/last seen, site "last updated")
  adapters, policy)         │  resolve PDF links
                            ▼
                     --ingest: plan ─► member4_manifest.csv (+ derived files) ─► acquire (download + validate)
                                       ─► quarantine failures ─► incremental index (embed only new text)
```

## Files (all under `frontend/data/sources/`)

| File | What it is | Edited by |
|---|---|---|
| `official_sources.csv` | Registry of every official source found in the research: listing URL, new-items feed, PDF URL pattern, adapter, collection status, robots/terms summary, refresh cadence, `enabled`, `auto_ingest` | People (review changes) |
| `law_inventory.csv` / `.json` | One row per law listed by an enabled source | Pipeline |
| `changes/YYYY-MM-DD.json`, `changes.csv` | What changed in each run (cumulative CSV log) | Pipeline |
| `sync_state.json` | Baseline date per source and the last 50 runs' stats | Pipeline |
| `last_run_summary.md` | Human-readable summary of the last run (also used as the PR body) | Pipeline |

### `official_sources.csv` columns

| Column | Meaning |
|---|---|
| `source_id` | Stable id, used as the prefix of every `law_key` |
| `listing_url` | The page(s) the adapter actually fetches (`{A-Z}`, `{offset}`, `{YYYY}` mark iteration) |
| `new_items_url` | The site's own "latest" / "recently updated" page, for humans checking a run |
| `document_url_pattern` | Shape of the direct PDF links found on that source |
| `adapter` | Python reader in `app/legal/official_codes.py` (`none` = not automated yet) |
| `collection_status` | `open`, `open_courtesy_request`, `needs_permission`, `blocked`, `unavailable` — from the research. **Only `open` sources can sync.** |
| `robots_txt`, `terms` | What the site says about automated access and reuse (quoted in the research notes) |
| `source_tier` | 1 = official primary; 2 = official secondary compilation (e.g. Sindh Judicial Academy) |
| `enabled`, `auto_ingest` | Crawl this source? Add its new principal laws to the corpus automatically? |
| `evidence` | Research note backing the row |

### `law_inventory.csv` columns

| Column | Meaning |
|---|---|
| `law_key` | `source_id:` + the site's own id (Pakistan Code token, Punjab article code, KP law id, Balochistan docid, Sindh file name) |
| `title`, `year`, `jurisdiction` | As listed; year from the title, else from the promulgation date |
| `instrument_type` | Act, Ordinance, Order, Code, Constitution, Rules, Regulations, Notification, Policy, Other |
| `is_amendment`, `site_marked_repealed` | From the title / listing line |
| `act_number`, `promulgation_date`, `category`, `site_status`, `source_last_updated` | Parsed from the listing's metadata line (e.g. Punjab's "Last Updated On", Pakistan Code's "Under Review") |
| `detail_url` | The law's page on the official site |
| `pdf_url` | **Direct official PDF** (what `acquire_corpus.py` downloads); `urdu_pdf_url` where the site has one (Sindh) |
| `pdf_checked_at` | When the PDF link was last read from the detail page |
| `first_seen`, `last_seen`, `last_changed`, `removed` | Lifecycle of the row across runs |
| `listing_hash` | Fingerprint of title + metadata **excluding view counters**, used to detect edits |
| `manifest_id` | The corpus document this law is (if it is in the corpus) |

### Change types

| Change | Meaning |
|---|---|
| `new` | Listed for the first time after the source's baseline |
| `listing_changed` | Title or metadata line changed (e.g. Punjab "Last Updated On" moved) |
| `pdf_changed` | The direct PDF link changed (new consolidated version) |
| `removed` / `reappeared` | Dropped from / returned to the listing (never recorded on a partial crawl) |

## Ingest policy (`--ingest`)

Conservative on purpose — the corpus is legal evidence:

* **Add** a law only if it is `new`, its source has `auto_ingest=true`, it is a principal instrument
  (Act / Ordinance / Order / Code / Constitution), not an amendment, not marked repealed, has a direct PDF on
  an allow-listed official host (`app/legal/manifest.py: OFFICIAL_HOSTS`), and is not already in the corpus.
* **Update** a corpus document when the official PDF behind it changed; it is re-downloaded (`force`).
* **Amendments** are linked to the principal law they amend (reported in the summary). Consolidated sources
  (Pakistan Code, KP Code) then update the principal's PDF, which the next point catches: every law already
  in the corpus has its PDF link re-checked on **every** run.
* After download, a PDF that is scanned (needs OCR) or whose first pages do not contain the title is
  **quarantined** to `metadata_only`, so it is never used as evidence.
* `--backfill <source_id> [--backfill-limit N] [--backfill-match text]` adds existing back-catalogue laws
  under the same rules (opt-in, in batches).

## Safety guards

* The **first crawl of a source is a baseline**: its back catalogue is recorded but not reported as `new`.
* **Stable keys.** A law's key comes from the site's own id where its URLs are stable. Punjab Code gives every
  law a *new URL on every visit*, so its key is title + Act No. + promulgation date (`UNSTABLE_URL_SITES`);
  a law the site lists twice keeps both rows (`~2` suffix).
* **Anomaly guard.** More than max(25, 5 % of the source) `new`, `removed` or `pdf_changed` in one run means the
  site changed shape, not the law: the run is recorded and flagged, and **nothing from that source is
  ingested** (`stats.anomaly`, shown in the summary).
* **Per-run cap.** At most 25 laws are added per run (`--max-add`); the rest are deferred and reported.
* **Link-only rows are upgraded, not duplicated.** If a law already in the manifest as `metadata_only` gains an
  official PDF, that row is upgraded in place.
* A crawl that lists fewer than 80 % of the previous count is treated as **partial** (site trouble):
  nothing is marked removed.
* One failing source never stops the others; the run exits with code 2 so the scheduler can flag it.
* Requests are sequential per site with a delay (default 0.5 s), identified by a project User-Agent; sources
  whose research status is `blocked` / `needs_permission` cannot be enabled for sync.
* Re-indexing reuses the stored embedding of every chunk whose exact text is unchanged (same model), so a
  weekly run embeds only new or amended provisions (`build_index.py --full` forces a full rebuild).

## Running it

```bash
cd backend
python scripts/sync_sources.py                       # inventory + change log only
python scripts/sync_sources.py --ingest              # + corpus updates, download, validate, re-index
python scripts/sync_sources.py --sources punjab_code --resolve all
python scripts/sync_sources.py --ingest --backfill punjab_code --backfill-limit 25
```

## Scheduling

* **GitHub Actions**: `.github/workflows/legal-sources-sync.yml` runs every Monday 06:30 PKT (and on demand),
  caches PDFs/embeddings between runs, and opens/updates a pull request `automation/legal-sources-sync` with
  the summary as its description — a person reviews new laws before they reach `main`.
* **Windows (local)**: `backend/scripts/run_source_sync.ps1 [-Ingest]`; the file header has the `schtasks`
  command to register it weekly. Logs go to `backend/logs/` (git-ignored).

## Going live: Supabase (how a new law reaches a user)

The deployed app never fetches government sites while a user is waiting. It searches the index in Supabase,
so a law is "live" once it is in Supabase:

```
Mon 06:30 PKT  legal-sources-sync.yml   crawl → new/changed laws → download + validate → index → pull request
(review)       a person merges the PR   (the PR body lists every added / re-downloaded / quarantined law)
on merge       publish-legal-corpus.yml push_to_supabase.py: upsert changed chunks, DELETE superseded chunks,
                                        drop documents no longer in the manifest → live for every user
```

Latency: at most a week (schedule) + review time; run "Legal sources sync" manually for an urgent law.

`push_to_supabase.py` is incremental: it reads chunk ids/hashes/titles/source URLs from Supabase, upserts only
chunks that differ, **deletes chunks of superseded versions** (otherwise users could be shown amended-away
text), and reuses vectors whose embedded text is unchanged — embedding only changed chunks. `--dry-run`
prints the plan; `--full` re-uploads everything (needed after changing the embedding model). Each document's
`metadata.source_last_checked` records when the official site last listed it, for an "as of" date in answers.

**Required configuration**

| Where | Setting |
|---|---|
| GitHub → Settings → Environments → `production` | secrets `SUPABASE_URL`, `SUPABASE_SECRET_KEY` (service role); optional required reviewers |
| Backend host | `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, `RETRIEVAL_BACKEND=auto` (or `supabase`). **Without the secret key the backend silently uses the index baked into its image, which goes stale.** |
| Frontend host | `BACKEND_API_URL` and `LEGAL_RAG_API_URL` pointing at the backend (otherwise the frontend falls back to its bundled metadata list) |
| Supabase | migrations `001`–`005` applied |

First publish: run `python scripts/push_to_supabase.py` once from a machine that has the local embeddings
(`legal_chunk_embeddings.npy`), so ~9,800 vectors are reused rather than recomputed in CI. Later publishes are
small. The frontend's source-library page reads a bundled JSON copy of the directory, so that list (not search)
updates on the frontend's next deploy.

## Adding a source

1. Add a row to `official_sources.csv` (cite the research note; set `collection_status` honestly).
2. Write an adapter in `app/legal/official_codes.py` returning `Listing(site, jurisdiction, title, detail_url,
   pdf_url?, meta?)`, register it in `SITES` (and its PDF pattern in `_PDF_PATTERNS` if PDFs sit on detail pages).
3. Add the PDF host to `OFFICIAL_HOSTS` only if it is an official government/court host.
4. Run once without `--ingest` (baseline), check `law_inventory.csv`, then enable `auto_ingest` if wanted.

Judgment sources are registered but not enabled: their adapters, OCR, headnote stripping and anonymisation
(see the research report, Part F) come first, and several need written permission.
