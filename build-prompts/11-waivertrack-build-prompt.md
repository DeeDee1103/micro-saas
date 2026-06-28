# Claude Code Build Prompt — "WaiverTrack" (Lien-Waiver / Bid-Security Tracker)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A tracker for construction general contractors to manage lien waivers and bid securities: request signed waivers from subs/vendors, track signed vs outstanding, automate renewal/expiry reminders, and see everything on one dashboard. Boring, sticky, recurring. Core value: **request → track status → remind on expiry → never miss a deadline.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS + Storage for documents) · Inngest (reminder/expiry scheduling) · Resend (reminders + requests) · Stripe (our billing, later)
- Extra (M4): an e-signature API (DocuSign / Dropbox Sign)
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** projects; parties (subs/vendors); waivers (type, amount, status, uploaded signed doc); bid securities (amount, expiry, status); request links; automated renewal/expiry reminders; central dashboard of all active items.
**Out (not yet):** e-signature integration (M4), payment-on-signature, accounting integration, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `projects` — `owner_id`, name, client
- `parties` — `project_id`, name, role (`sub`|`vendor`), contact email
- `waivers` — `project_id`, `party_id`, type (conditional/unconditional, progress/final), amount, status (`requested`|`signed`|`overdue`), signed_doc ref
- `bid_securities` — `project_id`, amount, issuer, expiry_date, status
- `reminders` — entity ref, scheduled_at, sent_at, status

## 5. Core flows
1. **Set up:** create project → add parties → create waiver/bid-security records.
2. **Request:** send a waiver request (link/email) → upload signed doc → status flips to signed.
3. **Remind (Inngest):** schedule reminders for outstanding waivers and upcoming bid-security expiries; send via Resend; escalate as deadlines approach.
4. **Dashboard:** all active items, statuses, and an expiry timeline.

## 6. Guardrails
- Document Storage with RLS + signed URLs; full audit trail of status changes.
- Reminder reliability is the product — make scheduling idempotent (no duplicate sends). Secrets in env; RLS per tenant.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + Storage + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Projects + parties + waiver/bid-security CRUD + signed-doc upload. *Verify:* records persist; docs upload privately.
- **M2** Request flow + status tracking + reminders (Inngest/Resend). *Verify:* an outstanding waiver triggers a reminder; uploading the signed doc stops further reminders.
- **M3** Dashboard + expiry alerts (bid-security countdown). *Verify:* an item nearing expiry surfaces and alerts.
- **M4** E-signature integration (request → sign → auto-capture signed doc).

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DOCS_BUCKET`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **reminder scheduling idempotency** and **status-transition correctness**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
