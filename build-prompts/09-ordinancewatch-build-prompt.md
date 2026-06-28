# Claude Code Build Prompt — "OrdinanceWatch" (HOA Compliance Scanner)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A tool that reads local city ordinances + HOA rules and flags potential violations for properties/HOAs **before** they get fined. The defensible asset is a maintained, structured ordinance dataset per jurisdiction plus an AI-assisted matching engine. Core value: **maintain ordinance corpus → scan property against rules → flag findings with citations → alert.**

> Start with ONE pilot jurisdiction. The ongoing dataset maintenance is the moat — design for it.

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (scheduled re-scans + ordinance-update checks) · Resend (alerts) · Stripe (our billing, later) · Claude Sonnet (parse ordinance text → structured rules; assist matching)
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** ingest + structure ordinances for one pilot city; property/HOA profiles; a scan engine that matches property attributes against structured rules (AI-assisted); findings with severity + **source citation**; alerts + dashboard; re-scan on ordinance updates.
**Out (not yet):** multi-jurisdiction at launch (M4), automated municipal-site crawling, legal-grade guarantees, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `jurisdictions` — name, region
- `ordinances` — `jurisdiction_id`, title, source_url, effective_date, raw_text, `rules` (jsonb: structured conditions)
- `properties` — `owner_id`, `jurisdiction_id`, attributes (jsonb)
- `scans` — `property_id`, ran_at, status
- `findings` — `scan_id`, `ordinance_id`, severity, explanation, **citation** (ordinance ref)
- `alerts` — `owner_id`, finding_id, status

## 5. Core flows
1. **Maintain corpus:** ingest ordinance text → Claude Sonnet structures it into machine-checkable `rules` (human reviews before activating).
2. **Scan:** match a property's attributes against active rules (AI assists ambiguous cases) → produce `findings` with severity + ordinance citation.
3. **Alert + dashboard:** notify on new/elevated findings; dashboard lists issues with source links.
4. **Update detection (Inngest):** periodically flag when a tracked ordinance changes → re-scan affected properties.

## 6. Guardrails
- Output is **advisory, not legal advice** — always cite the source ordinance; surface a clear disclaimer.
- Structured rules are human-approved before going live (AI structuring is a draft).
- Keep dataset current; record `effective_date` + source. RLS per tenant; secrets in env.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Ordinance ingestion + AI structuring + human-approval UI (one pilot city). *Verify:* a real ordinance becomes a reviewable structured rule.
- **M2** Property profiles + scan engine + findings with citations. *Verify:* a property that violates a rule produces a cited finding; a compliant one doesn't.
- **M3** Alerts + dashboard with source citations + disclaimer.
- **M4** Multi-jurisdiction support + ordinance-update detection/re-scan.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for the **scan/matching engine** (true positives and true negatives) and the **citation requirement** (no finding without a source). Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
