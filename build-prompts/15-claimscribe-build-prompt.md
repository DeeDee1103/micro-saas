# Claude Code Build Prompt — "ClaimScribe" (AI Claim-Narrative Drafter for Insurance Brokers)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A tool for insurance brokers that turns structured claim facts into a properly formatted claim narrative. The broker enters the facts, picks a claim type, and AI drafts the narrative in the right tone/format; the broker edits, regenerates, and exports. Core value: **enter facts → AI drafts (grounded on inputs) → human edits → export.** The differentiator is verticalized, template-driven drafting — not a generic chatbot.

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (async generation if needed) · Resend (notifications) · Stripe (our billing, later) · Claude Sonnet `claude-sonnet-4-6` (drafting)
- Extra: export to PDF/Word
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** claim intake form (structured facts) by claim type; a template library (structure + tone per claim type); AI draft generation grounded strictly on the entered facts; edit/regenerate with version history; export to PDF/Word.
**Out (not yet):** AMS/CRM integration (M5), multi-user review chains, e-signature, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `claims` — `owner_id`, claim_type, `facts` (jsonb), status (`draft`|`final`)
- `templates` — claim_type, structure spec, tone guidance
- `narrative_drafts` — `claim_id`, version, content, generated_at, `source` (`ai`|`edited`)
- `exports` — `claim_id`, format, file ref, created_at

## 5. Core flows
1. **Intake:** broker selects a claim type → fills a structured facts form.
2. **Draft (Claude Sonnet):** generate the narrative using the type's template + tone, grounded **only** on entered facts — no invented details.
3. **Edit/regenerate:** broker edits; can regenerate; every version is saved.
4. **Export:** produce a PDF/Word doc of the approved narrative.

## 6. Guardrails
- AI output is a **draft**; the broker approves before export. The prompt must forbid fabricating facts not present in the inputs — if a needed fact is missing, the draft should flag a placeholder, not invent it.
- Version every change. RLS per tenant; secrets in env.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Claim intake form + claim types. *Verify:* facts persist per claim type.
- **M2** AI draft generation grounded on inputs + template. *Verify:* drafts reflect only entered facts; missing facts become flagged placeholders, not fabrications.
- **M3** Edit/regenerate + version history + export to PDF/Word. *Verify:* edits version correctly and export matches.
- **M4** Template library management per claim type.
- **M5** (Optional) AMS/CRM integration to pull claim data in.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write a real test for the **no-fabrication rule** (a fact absent from inputs must not appear in the draft). Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components.

**Start with M0.**
