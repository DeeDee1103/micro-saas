# Claude Code Build Prompt — "Caseguard" (Legal-Software Health Monitoring + Backup)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
An external monitoring + backup tool for a legal practice-management app that small firms depend on (the category is notorious for crashes and data loss). We run uptime/latency checks, alert on failures/anomalies, and take scheduled backups of the firm's data to their own storage with integrity verification. Core value: **monitor → alert → back up → verify.** No legal expertise required — this is infrastructure.

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (scheduled checks + backups) · Resend (alerts) · Stripe (our billing, later)
- Extra: object storage for backups (Supabase Storage or S3-compatible); generic API connector to the target legal app
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** register a monitored target (URL + optional API credentials); scheduled uptime/latency checks; failure + anomaly alerts (Slack/email); scheduled data backups via the target's API/export; backup integrity verification; status + history dashboard.
**Out (not yet):** automated restore-into-app (M5 manual restore export only), multi-app support, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `monitors` — `owner_id`, name, target URL, type (`uptime`|`api`), credential ref, check interval
- `checks` — `monitor_id`, ts, `ok` (bool), `latency_ms`, detail
- `backups` — `monitor_id`, ts, storage ref, size, `integrity_ok`, status
- `alerts` — `monitor_id`, fired_at, kind, status
- `notification_targets` — `owner_id`, type (`slack`|`email`), config

## 5. Core flows
1. **Health checks (Inngest):** on schedule, hit the target; record `checks`; alert on failure or latency anomaly (with dedupe/cooldown).
2. **Backups (Inngest):** on schedule, pull data via the target's API/export → store → verify integrity (checksum/row counts) → record; alert on backup failure.
3. **Dashboard:** current status, uptime history, latency trend, backup log + downloadable backups.

## 6. Guardrails
- Encrypt stored credentials; secrets in env.
- Verify backup integrity — a backup that can't be validated must alert, not silently "succeed."
- Alert dedupe/cooldown. RLS per tenant so one firm's data/credentials are isolated.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + storage wired + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Uptime/latency monitors + checks + Slack/email alerts (dedupe/cooldown). *Verify:* a down target fires one alert; recovery clears it.
- **M2** Scheduled backups + storage + integrity verification. *Verify:* a backup runs, stores, and reports integrity; a corrupted backup alerts.
- **M3** Dashboard (status, uptime/latency history, backup log). *Verify:* matches recorded data.
- **M4** Anomaly detection on latency/check patterns.
- **M5** Manual restore export (download a backup in a usable format).

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `CREDENTIAL_ENCRYPTION_KEY`, `BACKUP_STORAGE_BUCKET`, `RESEND_API_KEY`, `SLACK_WEBHOOK_URL`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **alert dedupe/cooldown** and **backup integrity verification**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
