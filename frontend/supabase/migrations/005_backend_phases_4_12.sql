-- Pakistan Justice Navigator — backend phases 4–12
-- * document processing status/provenance columns
-- * private storage bucket with per-user folder policies
-- * citizens may not insert 'system' messages
-- * chunk provenance columns + retrieval RPCs that return chunk_id

-- ---------------------------------------------------------------------------
-- Case documents: processing status tracking
-- ---------------------------------------------------------------------------
alter table public.case_documents add column if not exists size_bytes bigint;
alter table public.case_documents add column if not exists sha256 text;
alter table public.case_documents add column if not exists page_count integer;
alter table public.case_documents add column if not exists error text;
alter table public.case_documents add column if not exists updated_at timestamptz not null default now();

drop trigger if exists case_documents_set_updated_at on public.case_documents;
create trigger case_documents_set_updated_at
before update on public.case_documents
for each row execute function public.set_updated_at();

create index if not exists idx_cases_user_updated on public.cases(user_id, updated_at desc);
create index if not exists idx_case_messages_case_created on public.case_messages(case_id, created_at);

-- ---------------------------------------------------------------------------
-- Messages: authenticated users may only write citizen/assistant messages to their own cases
-- ---------------------------------------------------------------------------
drop policy if exists "users_insert_own_case_messages" on public.case_messages;
create policy "users_insert_own_case_messages"
on public.case_messages for insert
to authenticated
with check (
  role in ('citizen', 'assistant')
  and exists (
    select 1 from public.cases c
    where c.id = case_messages.case_id
      and c.user_id = auth.uid()
  )
);

-- Ownership can never be transferred by an update.
drop policy if exists "users_update_own_cases" on public.cases;
create policy "users_update_own_cases"
on public.cases for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

-- ---------------------------------------------------------------------------
-- Storage: private bucket, objects live under "<auth.uid()>/<case_id>/<document_id>.<ext>"
-- ---------------------------------------------------------------------------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('case-documents', 'case-documents', false, 10485760, array['application/pdf', 'image/png', 'image/jpeg'])
on conflict (id) do update set public = false,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "case_documents_owner_insert" on storage.objects;
create policy "case_documents_owner_insert"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'case-documents'
  and (storage.foldername(name))[1] = auth.uid()::text
  and exists (
    select 1 from public.cases c
    where c.id::text = (storage.foldername(name))[2]
      and c.user_id = auth.uid()
  )
);

drop policy if exists "case_documents_owner_select" on storage.objects;
create policy "case_documents_owner_select"
on storage.objects for select
to authenticated
using (
  bucket_id = 'case-documents'
  and (storage.foldername(name))[1] = auth.uid()::text
);
-- No update/delete policies: uploaded evidence is immutable for citizens (service role handles retention).

-- ---------------------------------------------------------------------------
-- Legal chunks: provenance columns used by the backend index
-- ---------------------------------------------------------------------------
alter table public.legal_chunks add column if not exists chunk_index integer;
alter table public.legal_chunks add column if not exists section_heading text;
alter table public.legal_chunks add column if not exists section_confidence text;
alter table public.legal_chunks add column if not exists file_sha256 text;
alter table public.legal_chunks add column if not exists fetched_at timestamptz;

-- Return types change (chunk_id, section_heading added) → drop and recreate.
drop function if exists public.search_legal_chunks_lexical(text, integer);
create function public.search_legal_chunks_lexical(
  query_text text,
  match_count integer default 8
)
returns table (
  chunk_id text, document_id text, title text, document_type text, jurisdiction text, authority text,
  court text, bench text, citation text, section_or_article text, section_heading text,
  source_name text, source_url text, source_tier smallint, page_start integer, page_end integer,
  file_sha256 text, snippet text, score double precision
)
language sql
stable
security invoker
set search_path = public, extensions
as $$
  select c.chunk_id, c.document_id, c.title, c.document_type, c.jurisdiction, c.authority, c.court, c.bench,
         c.citation, c.section_or_article, c.section_heading, c.source_name, c.source_url, c.source_tier,
         c.page_start, c.page_end, c.file_sha256, left(c.content, 1200) as snippet,
         ts_rank_cd(c.fts, websearch_to_tsquery('english', query_text))::double precision as score
  from public.legal_chunks c
  where c.fts @@ websearch_to_tsquery('english', query_text)
  order by score desc
  limit greatest(1, least(match_count, 20));
$$;

revoke all on function public.search_legal_chunks_lexical(text, integer) from public, anon, authenticated;
grant execute on function public.search_legal_chunks_lexical(text, integer) to service_role;

drop function if exists public.match_legal_chunks(extensions.vector, double precision, integer);
create function public.match_legal_chunks(
  query_embedding extensions.vector(384),
  match_threshold double precision default 0.3,
  match_count integer default 8
)
returns table (
  chunk_id text, document_id text, title text, document_type text, jurisdiction text, authority text,
  court text, bench text, citation text, section_or_article text, section_heading text,
  source_name text, source_url text, source_tier smallint, page_start integer, page_end integer,
  file_sha256 text, snippet text, score double precision
)
language sql
stable
security invoker
set search_path = public, extensions
as $$
  select c.chunk_id, c.document_id, c.title, c.document_type, c.jurisdiction, c.authority, c.court, c.bench,
         c.citation, c.section_or_article, c.section_heading, c.source_name, c.source_url, c.source_tier,
         c.page_start, c.page_end, c.file_sha256, left(c.content, 1200) as snippet,
         (1 - (c.embedding <=> query_embedding))::double precision as score
  from public.legal_chunks c
  where c.embedding is not null
    and (1 - (c.embedding <=> query_embedding)) >= match_threshold
  order by c.embedding <=> query_embedding
  limit greatest(1, least(match_count, 20));
$$;

revoke all on function public.match_legal_chunks(extensions.vector, double precision, integer) from public, anon, authenticated;
grant execute on function public.match_legal_chunks(extensions.vector, double precision, integer) to service_role;
