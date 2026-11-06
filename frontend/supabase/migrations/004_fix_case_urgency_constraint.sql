-- Align case urgency values with the frontend and FastAPI contract.

alter table public.cases
  drop constraint if exists cases_urgency_check;

alter table public.cases
  add constraint cases_urgency_check
  check (
    urgency is null
    or urgency in ('low', 'medium', 'high', 'critical', 'unknown')
  );
