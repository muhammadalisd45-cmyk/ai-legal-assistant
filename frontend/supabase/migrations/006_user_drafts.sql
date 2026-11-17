-- Pakistan Justice Navigator — document drafts saved to the signed-in account
-- Before this, drafts lived only in browser localStorage and were lost when browser data was cleared.

create table if not exists public.user_drafts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  draft_id text not null check (char_length(draft_id) between 1 and 64),
  template_id text not null default '' check (char_length(template_id) <= 64),
  title text not null default '' check (char_length(title) <= 200),
  body text not null default '' check (char_length(body) <= 100000),
  reviewed boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, draft_id)
);

create index if not exists idx_user_drafts_user_updated on public.user_drafts(user_id, updated_at desc);

drop trigger if exists user_drafts_set_updated_at on public.user_drafts;
create trigger user_drafts_set_updated_at
before update on public.user_drafts
for each row execute function public.set_updated_at();

alter table public.user_drafts enable row level security;

drop policy if exists "users_select_own_drafts" on public.user_drafts;
create policy "users_select_own_drafts"
on public.user_drafts for select
to authenticated
using (auth.uid() = user_id);

drop policy if exists "users_insert_own_drafts" on public.user_drafts;
create policy "users_insert_own_drafts"
on public.user_drafts for insert
to authenticated
with check (auth.uid() = user_id);

drop policy if exists "users_update_own_drafts" on public.user_drafts;
create policy "users_update_own_drafts"
on public.user_drafts for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

drop policy if exists "users_delete_own_drafts" on public.user_drafts;
create policy "users_delete_own_drafts"
on public.user_drafts for delete
to authenticated
using (auth.uid() = user_id);

revoke all on public.user_drafts from anon;
grant select, insert, update, delete on public.user_drafts to authenticated;
