# Claude Code Build Prompt — "SpendLens" (SaaS Spend-Audit Tool)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A tool that connects a small business's accounting or bank/card feed, detects recurring SaaS charges, and flags waste — unused, duplicate, or price-increased subscriptions — with a savings dashboard and a monthly email. It *saves* money, so the ROI sells itself. Core value: **connect → detect recurring charges → flag waste → quantify savings.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (periodic sync + monthly report) · Resend (savings email) · Stripe (our billing, later)
- Extra: QuickBooks/Xero API (start with one) **or** Plaid for bank/card transactions
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** connect one data source (QuickBooks or Plaid); sync transactions; recurring-charge detection (group by vendor + cadence); flags (duplicate vendor, price increase, dormant/unused); savings dashboard; monthly email summary.
**Out (not yet):** auto-cancellation, multi-source merge (M5), alternative-vendor suggestions, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `connections` — `owner_id`, provider, encrypted credential ref, `last_synced_at`
- `transactions` — `owner_id`, date, amount, vendor_raw, vendor_normalized, source
- `detected_subscriptions` — `owner_id`, vendor, cadence, typical_amount, first_seen, last_seen, status
- `flags` — `subscription_id`, kind (`duplicate`|`price_increase`|`dormant`), detail, est_monthly_savings
- `savings_recommendations` — `owner_id`, summary, total_potential

## 5. Core flows
1. **Connect + sync (Inngest):** read-only connect → sync transactions (idempotent, paginated).
2. **Detect:** normalize vendors, group recurring charges by vendor + cadence into `detected_subscriptions`.
3. **Flag:** detect duplicates (same category, multiple vendors), price increases (amount drift), dormancy (no recent usage signal) → compute estimated savings.
4. **Report:** savings dashboard + monthly Resend email.

## 6. Guardrails
- **Read-only** financial scopes; this is sensitive financial data — encrypt credentials, minimize what's stored, RLS per tenant.
- Idempotent sync. Secrets in env. Be conservative with flags (false "cancel this" advice erodes trust).

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Connect (QuickBooks or Plaid) + transaction sync. *Verify:* transactions import idempotently.
- **M2** Recurring-charge detection engine. *Verify:* known recurring vendors are grouped with correct cadence/amount.
- **M3** Flags (duplicate/price-increase/dormant) + savings dashboard. *Verify:* seeded patterns produce the right flags + savings totals.
- **M4** Monthly email report via Resend.
- **M5** Add a second data source behind the same interface.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `CREDENTIAL_ENCRYPTION_KEY`, `QUICKBOOKS_CLIENT_ID`/`QUICKBOOKS_CLIENT_SECRET` (or `PLAID_CLIENT_ID`/`PLAID_SECRET`), `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **recurring-charge detection** and **flag accuracy** (precision over recall — avoid false positives). Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
