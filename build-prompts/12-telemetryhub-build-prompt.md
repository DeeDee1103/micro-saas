# Claude Code Build Prompt — "TelemetryHub" (IoT Analytics Dashboard)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
The reporting layer IoT platforms lack: ingest device telemetry (manufacturing/logistics), compute KPIs/aggregations, render dashboards, fire threshold alerts, and schedule exports. The real work is **reliable high-volume data plumbing**. Core value: **ingest telemetry → aggregate → dashboard/alert/export.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (aggregation jobs + scheduled exports) · Resend (alerts/exports) · Stripe (our billing, later)
- Extra: HTTP ingest now; MQTT ingest at M5. Use Postgres for time-series MVP (batch inserts; add downsampling/retention later).
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** register devices + ingest keys; HTTP telemetry ingest (batched); time-series storage; KPI/aggregation engine; dashboards (charts); threshold alert rules + notifications; scheduled CSV exports.
**Out (not yet):** MQTT (M5), real-time streaming UI, anomaly ML, multi-tenant org roles, our paid tiers.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `devices` — `owner_id`, name, type, metadata
- `ingest_keys` — `owner_id`, `key_hash`, scope
- `telemetry` — `device_id`, ts, metric, value, `fields` (jsonb) — indexed for time-range queries
- `kpi_definitions` — `owner_id`, name, aggregation spec (metric, window, function)
- `dashboards` — `owner_id`, layout/spec (jsonb)
- `alert_rules` / `alerts` — threshold rules + fired alerts
- `scheduled_exports` — cadence, scope, recipients

## 5. Core flows
1. **Ingest:** `POST /api/telemetry` keyed by ingest key → validate → **batch insert** telemetry. Return 200 fast.
2. **Aggregate (Inngest):** roll up KPIs over windows (avg/min/max/sum/percentiles) for fast dashboard reads.
3. **Dashboard:** charts over time ranges per device/metric/KPI.
4. **Alert + export:** threshold rules notify on breach (dedupe/cooldown); scheduled jobs email CSV exports.

## 6. Guardrails
- Authenticate + rate-limit ingest by key; hash keys at rest.
- Handle volume: batch writes, index for time-range queries, plan retention/downsampling (M5).
- Alert dedupe/cooldown. RLS per tenant; secrets in env.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Devices + ingest keys + batched HTTP ingest + telemetry store. *Verify:* a burst of telemetry stores efficiently and is queryable by time range.
- **M2** KPI/aggregation engine + dashboard charts. *Verify:* aggregates match hand-computed values.
- **M3** Threshold alert rules + notifications. *Verify:* breaching a threshold fires one alert (respecting cooldown).
- **M4** Scheduled CSV exports via Resend.
- **M5** MQTT ingest + retention/downsampling.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **batched ingest under load** and **aggregation correctness**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
