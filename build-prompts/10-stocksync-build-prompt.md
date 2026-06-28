# Claude Code Build Prompt — "StockSync" (Multi-Channel Inventory Sync)

> Paste into Claude Code. Build **incrementally, one milestone at a time** — verify each before continuing.

## 1. What we're building
Real-time inventory sync across e-commerce channels (Shopify first, then Etsy, then WooCommerce) so merchants never oversell, plus restock alerts based on sales velocity. The hard, defensible part is **conflict-free, loop-safe sync** across channels with different rate limits. Core value: **a sale on any channel updates a canonical quantity that's pushed to all others — instantly and without sync loops.**

## 2. Tech stack (don't substitute without asking)
- Next.js 14 (App Router, TS) · Supabase (Postgres + Auth + RLS) · Inngest (sync orchestration + retries) · Resend (restock alerts) · Stripe (our billing, later)
- Extra: Shopify Admin API + webhooks, Etsy API, WooCommerce REST
- Dev on Windows (WSL2 available); Vercel-ready

## 3. MVP scope
**In:** connect channels; import products; map the same product across channels to a canonical SKU; ingest sale/inventory webhooks; push quantity updates to other channels (idempotent, loop-safe); restock alerts on velocity; dashboard.
**Out (not yet):** POS integrations, multi-warehouse, bundles/kits, our paid tiers. (WooCommerce + reconciliation arrive at M5.)

## 4. Data model (Supabase, tenant-scoped + RLS)
- `stores` — `owner_id`, platform, encrypted credentials, status
- `products` — `owner_id`, canonical SKU, title
- `channel_listings` — `product_id`, `store_id`, platform product/variant id, last_known_qty
- `inventory_levels` — `product_id`, canonical_qty, updated_at, `update_source`
- `sync_events` — `product_id`, source store, delta, applied_at, status
- `low_stock_rules` / `alerts` — thresholds + fired alerts
- `processed_webhooks` — idempotency by platform event id

## 5. Core flows
1. **Connect + import:** OAuth each store → import products → operator maps them to canonical SKUs.
2. **Ingest:** platform webhook (sale/inventory change) → verify + dedupe → compute new canonical qty.
3. **Propagate:** push the new qty to all *other* channel listings, marking writes as system-originated so the resulting webhooks **don't re-trigger** another sync (loop prevention).
4. **Alerts:** when velocity/threshold rules trip, email a restock alert.

## 6. Guardrails
- **Loop prevention is the #1 risk:** tag our own writes and ignore the echo webhooks they generate.
- Idempotency on every inbound webhook; per-platform rate-limit handling/backoff.
- Reconciliation job to catch drift (M5). Encrypt credentials; RLS per tenant; secrets in env.

## 7. Milestones (ship + verify each)
- **M0** Scaffold + `CLAUDE.md` + migrations + RLS + `.env.example`.
- **M1** Shopify connect + product import + webhook ingest (verified + idempotent). *Verify:* a Shopify sale records a `sync_event` exactly once.
- **M2** Canonical SKU mapping + quantity model. *Verify:* listings map to one SKU with a single canonical qty.
- **M3** Sync engine: push updates cross-channel, loop-safe + add Etsy. *Verify:* a Shopify sale decrements the Etsy listing and does **not** cause a feedback loop.
- **M4** Restock alerts + dashboard. *Verify:* crossing a threshold emails one alert.
- **M5** WooCommerce connector + reconciliation job.

## 8. Env vars (`.env.example`)
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, `ETSY_API_KEY`, `CREDENTIAL_ENCRYPTION_KEY`, `RESEND_API_KEY`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `APP_URL`

## 9. How I want you (Claude Code) to work
One-paragraph plan per milestone before coding. Stay in MVP scope (ask before adding §3-Out). Write real tests for **webhook idempotency** and **sync-loop prevention** (a system write must not cascade). Verification steps after each milestone. Maintain `CLAUDE.md`. Ask before destructive actions. TypeScript.

**Start with M0.**
