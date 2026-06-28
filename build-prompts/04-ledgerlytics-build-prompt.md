# Claude Code Build Prompt — "Ledgerlytics" (Subscription-Finance Report Builder)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A reporting tool for finance teams at subscription businesses. They connect their billing provider (Stripe first), and we sync the data, let them build custom reports with a simple builder, render dashboards, and email scheduled PDF/CSV reports the native tool can't produce. Core value: **connect → sync → build → schedule/export.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (periodic sync + scheduled report delivery) · Resend (report emails) · Stripe (data source **and** our billing) · Claude Sonnet (optional: "explain this change" narrative)
- Extra: a PDF generator (e.g., `@react-pdf/renderer` or Puppeteer)
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** Stripe connect (read-only); sync subscriptions/invoices/customers; computed metrics (MRR, churn, new vs churned, ARPU); a report builder (pick metrics + dimensions + filters + a chart type); dashboards; scheduled email reports; CSV + PDF export.
**Out (not yet):** Chargebee/Recurly (M4), our paid tiers, real-time data, multi-user roles, write-back to Stripe.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `connections` — `owner_id`, provider, encrypted credential ref, `last_synced_at`
- `subscriptions`, `invoices`, `customers` — synced snapshots (provider IDs + key fields)
- `metric_snapshots` — period, metric, value (cached computed metrics)
- `report_definitions` — `owner_id`, name, `spec` (jsonb: metrics, dimensions, filters, viz)
- `scheduled_reports` — `report_id`, cadence, recipients, format
- `report_runs` — `report_id`, generated_at, output ref

## 5. Core flows
1. **Connect + sync:** Stripe read-only connect → Inngest periodic sync of subscriptions/invoices/customers → compute and cache metrics.
2. **Build:** user composes a `report_definition` (metrics/dimensions/filters/viz) → dashboard renders it.
3. **Schedule/export:** scheduled job generates PDF/CSV → emails recipients via Resend; on-demand export too.

## 6. Guardrails
- Request **read-only** scopes; never mutate the provider.
- Idempotent, paginated sync for large datasets.
- Encrypt credentials; secrets in env; RLS per tenant.
- Compute metrics deterministically; document the MRR/churn definitions in `CLAUDE.md`.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Stripe connect + sync subscriptions/invoices/customers + MRR/churn calc. *Verify:* metrics match a test Stripe account.
- **M2** Report builder UI (metrics/dimensions/filters) + dashboard render. *Verify:* a custom report renders correctly.
- **M3** Scheduled reports + PDF/CSV export + Resend delivery. *Verify:* a scheduled report emails a correct PDF.
- **M4** Add Chargebee/Recurly connector behind the same interface.
- **M5** (Optional) Claude Sonnet narrative explaining month-over-month changes.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_CONNECT_CLIENT_ID`, `CREDENTIAL_ENCRYPTION_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `ANTHROPIC_API_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **metric calculations** and **scheduled-report generation**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
