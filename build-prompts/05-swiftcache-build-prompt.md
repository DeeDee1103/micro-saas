# Claude Code Build Prompt — "Swiftcache" (Performance Caching / Prefetch Layer)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
A drop-in read-through caching + prefetch layer that sits in front of a slow upstream API and makes reads feel instant. A "control plane" (dashboard + config) plus a "data plane" (a reverse proxy backed by Redis). Buyers are vertical-SaaS vendors (or their ops teams) whose product is slow under load. Core value: **proxy → cache → prefetch → invalidate, with hit-rate/latency visibility.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) for the control plane + proxy route handlers · Supabase (Postgres + Auth + RLS) for config/metrics · Upstash Redis for the cache store · Inngest (scheduled prefetch refresh) · Resend (alerts) · Stripe (our billing, later)
- Dev on Windows (WSL2 available); Vercel-ready (edge-friendly proxy)

## 3. MVP scope
**In:** register an upstream service (base URL + auth passthrough); per-path cache rules (TTL + vary keys); a read-through proxy endpoint; scheduled prefetch refresh; a manual invalidation API; metrics dashboard (request count, hit rate, p50/p95 latency).
**Out (not yet):** write-path handling, multi-region edge tuning, our paid tiers, automatic rule learning.

## 4. Data model (Supabase, tenant-scoped + RLS)
- `services` — `owner_id`, name, `upstream_base_url`, auth-passthrough config
- `cache_rules` — `service_id`, `path_pattern`, `ttl_seconds`, `vary_on` (jsonb: headers/query/user), `prefetch_schedule` (nullable)
- `request_metrics` — `service_id`, ts, path, `cache_status` (`hit`|`miss`), `latency_ms`
- (Cache entries themselves live in Upstash, keyed by service + path + vary key.)

## 5. Core flows
1. **Proxy:** client calls `/proxy/{serviceId}/{...path}` → resolve matching `cache_rule` → build cache key (path + vary keys) → on **hit** return cached instantly; on **miss** fetch upstream (passing through auth), store with TTL, return. Record a `request_metrics` row.
2. **Prefetch (Inngest):** for rules with a schedule, refresh cache entries proactively so users never hit a cold miss.
3. **Invalidate:** `POST /api/services/{id}/invalidate` clears keys by path/pattern (call from the customer's app on data change).
4. **Dashboard:** hit rate, p50/p95 latency, requests over time per service.

## 6. Guardrails
- **Cache-key correctness is critical:** never serve one user's data to another — `vary_on` must include auth/user where responses are user-specific. Default to NOT caching unless a rule explicitly allows it.
- Stale-while-revalidate where safe; respect upstream cache headers.
- Auth passthrough: never log credentials. Secrets in env. RLS per tenant on config/metrics.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + Upstash wired + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Read-through proxy with per-path TTL + auth passthrough. *Verify:* first call misses, second call hits and is faster.
- **M2** Metrics capture + dashboard (hit rate, p50/p95). *Verify:* numbers reflect real calls.
- **M3** Scheduled prefetch (Inngest) + invalidation endpoint. *Verify:* prefetched path is warm on first user call; invalidation forces a miss.
- **M4** Multi-service config UI + `vary_on` rules. *Verify:* user-specific responses aren't cross-served.
- **M5** Stale-while-revalidate + upstream-header respect.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **cache-key vary correctness** (no cross-user leakage) and **hit/miss accounting**. Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
