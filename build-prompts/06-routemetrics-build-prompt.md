# Claude Code Build Prompt — "RouteMetrics" (Courier / Logistics Reporting)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A reporting tool that replaces spreadsheets for courier / last-mile operations. Ops managers import delivery data (CSV/Excel first, since most still use spreadsheets), and we compute KPIs, render dashboards, generate driver scorecards, and email scheduled reports. Core value: **import → compute KPIs → dashboard → scheduled reports.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (scheduled report delivery) · Resend (report emails) · Stripe (our billing, later) · Claude Sonnet (optional: "why did on-time rate drop" narrative)
- Extra: a CSV/XLSX parser (e.g., `papaparse` / `xlsx`) and a PDF generator
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** CSV/Excel import with column mapping + validation; normalized deliveries + drivers; KPI engine (on-time rate, avg delivery time, deliveries/driver, exceptions); dashboards; driver scorecards; scheduled PDF/email reports.
**Out (not yet):** live ERP/CRM API connectors (M4), route optimization, real-time tracking, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `data_sources` — `owner_id`, name, type (`csv` for now)
- `deliveries` — `owner_id`, date, `driver_id`, route, status, promised_window, delivered_at, `on_time` (bool)
- `drivers` — `owner_id`, name, external ref
- `kpi_definitions` — `owner_id`, name, formula spec
- `scheduled_reports` — `owner_id`, cadence, recipients, scope

## 5. Core flows
1. **Import:** upload CSV/XLSX → map columns → validate → normalize into `deliveries`/`drivers`.
2. **Compute:** KPI engine derives on-time rate, avg delivery time, per-driver scorecards, exception counts.
3. **Report:** dashboards render KPIs; Inngest generates scheduled PDF reports and emails them via Resend.

## 6. Guardrails
- Validate imports (bad rows reported, not silently dropped); handle large files (stream/batch).
- RLS per tenant; secrets in env.
- Document KPI formulas in `CLAUDE.md` so they're auditable.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** CSV/XLSX import + column mapping + validation + normalization. *Verify:* a sample file produces correct `deliveries`/`drivers`.
- **M2** KPI engine + dashboard + driver scorecards. *Verify:* on-time rate and per-driver stats match hand-calculated figures.
- **M3** Scheduled reports + PDF + Resend. *Verify:* a scheduled report emails a correct PDF.
- **M4** Optional live connector (ERP/CRM API) behind the same import interface.
- **M5** (Optional) Claude Sonnet insight narrative on KPI changes.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `ANTHROPIC_API_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **import validation** and **KPI calculations**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
