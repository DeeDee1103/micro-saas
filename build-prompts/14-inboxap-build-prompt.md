# Claude Code Build Prompt — "InboxAP" (AP / Invoice Automation)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
An accounts-payable tool that extracts structured data from incoming invoices (PDF/email/image), matches them to purchase orders, routes for approval, and exports to accounting. The moat is a **reliable document-extraction pipeline** with human-in-the-loop on low-confidence fields. Core value: **invoice in → AI extract (with confidence) → human verify → match + approve → sync.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS + Storage for documents) · Inngest (async extraction + sync) · Resend (approval routing emails) · Stripe (our billing, later) · Claude Sonnet `claude-sonnet-4-6` **with document/vision** (extraction)
- Extra (M4): QuickBooks/Xero export
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** invoice intake (upload + a forwarding email address); AI extraction → vendor, amount, dates, line items, with **per-field confidence**; a review UI that surfaces low-confidence fields; PO matching; approval workflow; export to accounting.
**Out (not yet):** auto-payment (never auto-pay), OCR for handwriting, multi-entity, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `invoices` — `owner_id`, source (`upload`|`email`), doc ref, vendor, amount, currency, invoice_date, due_date, status (`extracted`|`review`|`matched`|`approved`|`exported`)
- `extractions` — `invoice_id`, raw, `structured` (jsonb), `confidence` (jsonb per field)
- `line_items` — `invoice_id`, description, qty, unit_price, total
- `purchase_orders` — `owner_id`, po_number, vendor, amount, lines
- `matches` — `invoice_id`, `po_id`, match_status
- `approvals` — `invoice_id`, approver, decision, decided_at
- `sync_log` — `invoice_id`, target, status

## 5. Core flows
1. **Intake:** upload or email-forward → store doc privately → enqueue extraction.
2. **Extract (Inngest + Claude Sonnet):** parse fields + line items with confidence; ground strictly in the document (no invented values).
3. **Review:** UI highlights low-confidence fields for human correction before proceeding.
4. **Match + approve:** match to a PO; route for approval via Resend.
5. **Export:** push approved invoices to accounting; log result.

## 6. Guardrails
- **Human-in-the-loop** on low-confidence fields; never auto-approve or auto-pay.
- Documents are sensitive — Storage RLS, signed URLs, audit trail.
- Extraction must be grounded in the document; flag uncertainty rather than guess. Secrets in env; RLS per tenant.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + Storage + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Invoice upload + email-forward intake. *Verify:* invoices arrive and store privately.
- **M2** AI extraction → fields + line items + confidence + review UI. *Verify:* sample invoices extract correctly; low-confidence fields are flagged for review.
- **M3** PO matching + approval workflow. *Verify:* an invoice matches a PO and routes for approval.
- **M4** Accounting export/sync + dashboard.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `INVOICES_BUCKET`, `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **extraction confidence handling** (low-confidence → review, not auto-advance) and **document privacy**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
