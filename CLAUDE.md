# CLAUDE.md — Micro-SaaS Project

This repo is a micro-SaaS exploration. The goal is one small, integration-heavy B2B product reaching **$10k MRR**. Research, ranking, build specs, validation plan, and landing pages all live here.

## Active build: "Recover" (dunning / failed-payment recovery)
The chosen product is a **dunning tool** — recovers failed subscription payments for membership/SaaS businesses via automated retries + branded reminder sequences. It won the shortlist on the combination of fast time-to-revenue and a real engineering moat (Stripe/webhook reliability).

**To build it, follow `build-prompts/01-dunning-build-prompt.md` exactly.** It is milestone-gated (M0→M6); build and verify one milestone at a time. M0 generates the project-specific CLAUDE.md inside the actual app repo.

> When you start the real app, scaffold it in its own directory (e.g. `apps/recover/`) and let M0 create that app's own CLAUDE.md. This top-level file is portfolio context.

## Owner context
- Solo founder, strong backend/integration engineer. Windows dev (WSL2 available).
- Edge = boring integration/infra glue where engineering is the moat, not marketing.

## Stack (standard across all ideas here)
Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (background jobs) · Resend (email) · Stripe (billing + integration target) · Claude Sonnet `claude-sonnet-4-6` (AI features). Vercel-ready.

## Repo map
- `build-prompts/` — a ready-to-run Claude Code spec per idea. `01-dunning` is active; `02–15` are the ranked backlog.
- `landing-pages/` — one deployable smoke-test page per idea (`01-recover` is the flagship). `_generate_landing_pages.py` regenerates all from one config — edit copy/palette/pricing there, not in the HTML.
- `validation/validation-plan.md` — the one-week parallel build+sell playbook: who to talk to, the questions, the landing-page funnel, and the go/no-go scorecard.
- `DECISION.md` — the shortlist ranking + revenue math + why dunning.

## How to work in this repo
- Building was never the bottleneck — demand is. Run validation (`validation/`) in parallel with the build.
- For the active build, obey the milestone gates in `build-prompts/01-dunning-build-prompt.md`; don't scaffold everything at once.
- Keep MVP scope tight; ask before adding anything outside a prompt's "out of scope" list.
- Landing pages: set `FORM_ENDPOINT` + add an analytics script before driving traffic. Events fired: `Early access`, `Pricing click`, `Nav pricing`.

## Next actions
1. Scaffold the Recover app (M0 of the dunning build prompt).
2. Deploy `landing-pages/01-recover-landing.html`; wire the form + analytics.
3. Run the dunning card in `validation/validation-plan.md` — 10 buyer conversations + smoke test this week.
4. Decision gate: 2+ pre-sale commitments + ~10 signups → push to M3–M4.
