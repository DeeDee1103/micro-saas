# Claude Code Build Prompt — "Bridgeline" (Legacy↔Modern Integration Middleware)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
Middleware that syncs data between a legacy system and a modern API for **one specific vertical's A↔B pair**. It does field mapping, scheduled/triggered syncs, idempotent upserts, conflict handling, retries, and gives full run visibility. The connectors must be **pluggable** so new source/destination pairs can be added without rewrites. Core value: **extract → transform → load, reliably, with a dead-letter safety net.**

> Pick ONE concrete pair to start. Default: a legacy **CSV-over-SFTP export** as source, a modern **REST/OAuth API** (e.g., a CRM) as destination. Don't try to be a general iPaaS.

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (scheduling, retries, dead-letter) · Resend (failure notifications) · Stripe (our billing, later) · Claude Sonnet (optional: suggest field mappings)
- Extra: `ssh2-sftp-client` (or similar) for SFTP; generic REST client for destination
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** define a connection (source + destination + credentials); a field-mapping engine with simple transforms; scheduled or webhook-triggered sync runs; idempotent upserts keyed on external IDs; per-record results; conflict + error surfacing; manual replay of failed records; run-history dashboard.
**Out (not yet):** more than one source and one destination connector (add a 2nd at M5), visual mapping drag-drop, real-time streaming, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `connections` — `owner_id`, name, `source_type`, `source_config` (jsonb), `dest_type`, `dest_config` (jsonb), encrypted credential refs, schedule
- `mappings` — `connection_id`, `field_map` (jsonb: src→dest + transform), version
- `sync_runs` — `connection_id`, `started_at`, `finished_at`, `status`, counts
- `sync_records` — `run_id`, `external_id`, `status` (`ok`|`conflict`|`error`|`skipped`), `error`, payload snapshot
- `dead_letters` — `connection_id`, `external_id`, payload, `last_error`, `retries`
- `processed_keys` — idempotency (`connection_id` + `external_id` + content hash)

## 5. Core flows
1. **Configure:** create connection (source/dest configs + credentials) and a mapping.
2. **Run (Inngest):** scheduled or triggered → extract from source → transform via mapping → load to destination with idempotent upsert → write per-record result.
3. **Resilience:** retries with backoff; records exceeding retries go to `dead_letters`; conflicts flagged for review; failures notify via Resend.
4. **Dashboard:** run history, per-record drill-down, conflicts, and one-click replay of dead-lettered records.

## 6. Guardrails
- **Idempotent upserts** keyed on external IDs + content hash — never duplicate or lose records.
- Retries/backoff; dead-letter rather than silent drop.
- Encrypt stored credentials; secrets in env.
- Full audit trail; RLS so each tenant's connections/data are isolated.
- Pluggable connector interface (`extract()`, `load()`) so adding a pair is additive.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example` + connector interface defined.
- **M1** One source (CSV/SFTP) + one destination (REST/OAuth) connector + credential storage. *Verify:* can pull a sample file and authenticate to the destination.
- **M2** Mapping engine + transforms. *Verify:* source fields map and transform into destination shape.
- **M3** Sync run engine (Inngest) + idempotency + retries + dead-letter. *Verify:* re-running a sync creates zero duplicates; a forced failure lands in `dead_letters` and can be replayed.
- **M4** Dashboard (run history, conflicts, errors, manual replay). *Verify:* matches run data.
- **M5** Add a second connector; (optional) Claude Sonnet field-mapping suggestions.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `CREDENTIAL_ENCRYPTION_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `ANTHROPIC_API_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding anything in §3-Out). Write real tests for **idempotency** and **dead-letter + replay**. Give verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + simplest passing implementation.

**Start with M0**, and define the pluggable connector interface as part of it.
