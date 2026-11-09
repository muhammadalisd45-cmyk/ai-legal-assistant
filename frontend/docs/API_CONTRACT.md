# Member 1 ↔ Member 2 / Member 4 API Contract

The citizen frontend stays usable even while the team services are being integrated. Every fallback is explicit so the UI never silently upgrades metadata into legal evidence.

## 1. Triage — Member 2

Frontend route: `POST /api/triage`

The Next.js route forwards configured services to `BACKEND_API_URL/api/v1/triage`. If no backend is configured, it uses deterministic demo triage and labels the response as demo mode. If a configured backend fails or returns an invalid response, it returns a safe `502` response and does not substitute demo output.
### Request
```json
{
  "description": "Mere chacha inherited property par qabza kiye hue hain...",
  "language": "roman-ur"
}
```

Allowed languages: `en`, `roman-ur`, `ur`.

### Response
```json
{
  "mode": "backend",
  "category": "Property / inheritance",
  "summary": "Short citizen-friendly summary",
  "urgency": "medium",
  "facts": ["Citizen-provided fact only"],
  "legalIssues": ["Ownership or inheritance basis", "Possession"],
  "missingInformation": ["Who is shown as owner in the latest record?"],
  "suggestedDocuments": ["Registry / ownership document", "Legal notice"],
  "followUpQuestions": [
    {"id": "q1", "prompt": "Who is shown as owner in the latest document you have?", "type": "text"}
  ],
  "sourceIds": ["PK-009", "PK-010"],
  "guardrail": "Preliminary informational triage — not a final legal opinion."
}
```

The proxy maps `description` to backend `message`, and `en` / `roman-ur` / `ur` to `english` / `roman_urdu` / `urdu`. The backend returns `mode: "live"` or `mode: "deterministic_fallback"`; the latter becomes `mode: "backend-fallback"` with a visible notice in the citizen flow.

## 2. Legal search — Member 4

Frontend route: `POST /api/legal-search`

When `LEGAL_RAG_API_URL` is configured, Next.js forwards to `LEGAL_RAG_API_URL/v1/search`. If the service is unavailable, Next.js falls back to title/metadata discovery and returns a warning.

### Request
```json
{
  "query": "inherited property possession",
  "limit": 6
}
```

### Response — ingested source text
```json
{
  "query": "inherited property possession",
  "mode": "local-ingested-chunks",
  "results": [
    {
      "document_id": "PK-009",
      "title": "Transfer of Property Act, 1882",
      "jurisdiction": "Federal",
      "authority": "Parliament of Pakistan",
      "court": "",
      "bench": "",
      "section_or_article": "Section ...",
      "source_url": "official URL",
      "page_start": 12,
      "page_end": 12,
      "score": 8.2,
      "evidence_level": "chunk",
      "snippet": "source-grounded excerpt"
    }
  ]
}
```

### Response — safe metadata fallback
```json
{
  "query": "inherited property possession",
  "mode": "metadata-only",
  "warning": "No ingested chunk index is available yet. Results identify source documents only and do not assert exact legal provisions.",
  "results": [
    {
      "document_id": "PK-009",
      "title": "Transfer of Property Act, 1882",
      "source_url": "official URL",
      "bench": "",
      "evidence_level": "metadata",
      "section_or_article": "",
      "snippet": "Metadata match only — ingest the official document before claiming an exact provision."
    }
  ]
}
```

Member 1 must never manufacture `section_or_article`, citation, bench, case number or quote. Those values must come from verified source metadata/chunks.

## 3. Member 4 health

`GET /health`

```json
{
  "ok": true,
  "index_file_present": true,
  "index_ready": false,
  "local_chunk_count": 0,
  "supabase_configured": false
}
```

`index_ready=false` is intentional until at least one real official source chunk exists.

## 4. Document intelligence — Member 3 handoff

Recommended endpoint: `POST /v1/cases/{case_id}/documents`

```json
{
  "document_id": "uuid",
  "document_type": "Legal Notice",
  "status": "analyzed",
  "parties": [],
  "important_dates": [],
  "deadlines": [],
  "extracted_facts": [],
  "source_file_name": "notice.pdf"
}
```

The citizen UI already has selected/uploaded/processing/analyzed/failed document states and should only show `analyzed` after the service confirms it.

## 3. Unified backend (phases 4–12)

`backend/` now serves triage, search, answers and cases from one FastAPI app; point both
`BACKEND_API_URL` and `LEGAL_RAG_API_URL` at it. Existing response fields above are unchanged; new fields are additive:

* Triage adds `detected_language`, `response_language`, `urgency_indicators[]`, `urgency_note`, `fallback_reason`, `request_id`. `urgency` can also be `critical` or `unknown`.
* Search results add `chunk_id`, `section_heading`, `page_start`/`page_end`, `page_reference`, `is_legal_provision`,
  `relevance {term_coverage, semantic_similarity, strong_match}` and `provenance {page_url, file_sha256, fetched_at}`.
  The response adds `detected_language`, `evidence_summary`, `low_confidence`, `fallback_reason`.
  The `mode` is one of `local-hybrid`, `local-lexical`, `supabase-hybrid` or `metadata-only`.
* `POST /api/v1/answer` returns citation-backed answers (`mode`: `live` | `extractive_fallback` | `no_evidence`).
* `/api/v1/cases…` provides authenticated case, message and document persistence (see `backend/README.md`).

Live check: `BACKEND_API_URL=http://127.0.0.1:8000 [NEXT_APP_URL=http://127.0.0.1:3000] npm run test:integration`.
