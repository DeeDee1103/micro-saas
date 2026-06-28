# Claude Code Build Prompt — "ClaimSnap" (Short-Term-Rental Damage-Claim Portal)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A tool for short-term-rental hosts (Airbnb/VRBO) to document property damage with photos and produce a structured, submittable insurance claim fast. The core differentiator is **photo-to-report automation**: AI analyzes the photos, drafts an itemized damage report, the host reviews/edits, and we generate a branded PDF claim. Core value: **capture photos → AI drafts report → human approves → submit.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS + Storage for photos) · Inngest (async AI processing) · Resend (send claim / notify) · Stripe (our billing, later) · Claude Sonnet `claude-sonnet-4-6` **with vision** (analyze photos + draft report)
- Extra: PDF generator
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** properties; claims with incident details; multi-photo upload; AI photo analysis → itemized damage draft (with confidence); host review/edit; branded PDF generation; submit/email to insurer; claim status tracking.
**Out (not yet):** direct insurer API filing, payments, multi-user teams, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `properties` — `owner_id`, name, address
- `claims` — `owner_id`, `property_id`, incident_date, booking_ref, status (`draft`|`review`|`submitted`)
- `claim_photos` — `claim_id`, storage ref, `ai_description`, `ai_tags` (jsonb), confidence
- `claim_items` — `claim_id`, description, est_cost, source (`ai`|`host`)
- `claim_reports` — `claim_id`, version, pdf ref, generated_at

## 5. Core flows
1. **Create claim + upload photos** → stored privately in Supabase Storage.
2. **AI analysis (Inngest + Claude Sonnet vision):** describe damage per photo, propose itemized `claim_items` with confidence; never invent items not visible.
3. **Human review:** host edits/adds/removes items (AI output is a draft, not final).
4. **Generate + submit:** branded PDF from approved items; email to insurer via Resend; track status.

## 6. Guardrails
- Photos are sensitive — Storage RLS, signed URLs, no public exposure.
- AI is **draft-only**; host must approve before generation. Flag low-confidence items.
- Secrets in env; RLS per tenant.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + Storage + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Property + claim CRUD + private photo upload. *Verify:* photos store privately and render via signed URLs.
- **M2** AI photo analysis → itemized draft + confidence + review UI. *Verify:* uploaded photos yield sensible itemized items; host can edit.
- **M3** Branded PDF generation + email submission. *Verify:* approved claim produces a correct PDF and sends.
- **M4** Dashboard + claim status tracking.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `CLAIM_PHOTOS_BUCKET`, `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **photo privacy (no public access)** and the **AI-draft → human-approval gate**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
