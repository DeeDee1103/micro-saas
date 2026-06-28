# Claude Code Build Prompt — "Logpost" (Log Parser + Alerting)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — run and verify each before continuing. Don't scaffold everything at once.

## 1. What we're building
A cheap, lightweight log-monitoring tool for small dev teams who can't justify Datadog/Splunk. Teams send us logs via a keyed HTTP endpoint; we auto-parse common formats, store them searchably, watch for error spikes/anomalies, and fire Slack/email alerts. Core value loop: **ingest → parse → detect → alert.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TypeScript) · Supabase (Postgres + Auth + RLS) · Inngest (windowed evaluation + cooldowns) · Resend (email alerts) · Stripe (our own billing, later) · Claude Sonnet `claude-sonnet-4-6` (optional: summarize an error cluster)
- Extra: Slack (incoming webhook or OAuth) for alert delivery
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** projects + per-project ingest API keys; HTTP ingest endpoint; parsers for nginx, Apache, and JSON app logs; searchable log storage; alert rules (error-rate threshold over a rolling window); Slack + email notifications with dedupe/cooldown; dashboard (error rate over time, recent alerts).
**Out (not yet):** SMS, our paid tiers, log drains/integrations, full-text search at scale, anomaly ML (Milestone 5), retention tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `projects` — `owner_id`, name
- `ingest_keys` — `project_id`, `key_hash`, `last_used_at`
- `log_events` — `project_id`, `ts`, `level`, `message`, `source`, `fields` (jsonb), `raw`
- `alert_rules` — `project_id`, `name`, `match` (level/pattern), `threshold`, `window_seconds`, `cooldown_seconds`, channel config
- `alerts` — `rule_id`, `fired_at`, `summary`, `status`
- `notification_targets` — `project_id`, type (`slack` | `email`), config

## 5. Core flows
1. **Ingest:** `POST /api/ingest` authenticated by project ingest key → parse/normalize (detect format) → insert `log_events`. Return 200 fast; batch inserts.
2. **Detect:** Inngest evaluates each `alert_rule` over its rolling window (e.g., error count > threshold) on a schedule; respects `cooldown_seconds` to avoid alert storms.
3. **Notify:** on fire, write `alerts` row and send to Slack/email; dedupe identical alerts within cooldown.
4. **Dashboard:** error rate chart, recent events with filters, alert history.

## 6. Guardrails
- Authenticate every ingest request by key; hash keys at rest; rate-limit per key.
- Dedupe + cooldown so one incident ≠ 50 alerts.
- Treat log contents as potentially sensitive (PII) — don't log them server-side beyond storage.
- RLS so a project's logs are private. Secrets in env only.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`. *Verify:* boots, migrations apply.
- **M1** Projects + ingest keys + `/api/ingest` + parsers (nginx/Apache/JSON). *Verify:* posting sample logs of each format stores normalized rows.
- **M2** Log storage browse/search UI. *Verify:* can filter by level/text/time.
- **M3** Alert rules + Inngest evaluation + Slack/email + cooldown. *Verify:* a burst of error logs fires exactly one alert; a second burst within cooldown does not.
- **M4** Dashboard (error-rate chart + alert history). *Verify:* metrics match seeded data.
- **M5** (Optional) baseline anomaly detection; Claude Sonnet summary of an error cluster.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, `SLACK_WEBHOOK_URL` (or `SLACK_CLIENT_ID`/`SLACK_CLIENT_SECRET`), `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `ANTHROPIC_API_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
Confirm a one-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding anything in §3-Out). Write real tests for **ingest parsing** and **alert dedupe/cooldown**. After each milestone, give exact verification steps. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript + server components + simplest thing that passes the check.

**Start with M0.**
