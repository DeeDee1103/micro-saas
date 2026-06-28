# DECISION.md — Shortlist ranking & why dunning

Scores are 1–5, **higher is better** (Build ease, Open field, Speed to revenue, Moat-fit). Composite weights Speed and Moat ×1.5 (max 25). Revenue is illustrative at benchmark-midpoint pricing, before churn/refunds/CAC. "→$10k" = customers needed for $10k MRR. `*` = estimated price.

| # | Idea | Build | Field | Speed | Moat | /25 | Price/mo | MRR@100 | →$10k |
|---|------|:---:|:---:|:---:|:---:|:---:|---:|---:|---:|
| 1 | Dunning / payment recovery | 4 | 2 | 5 | 5 | **21.0** | $75 | $7,500 | ~134 |
| 2 | Log parser + alerting (Tracepoint) | 4 | 3 | 4 | 5 | **20.5** | $29* | $2,900 | ~345 |
| 3 | Legacy integration middleware (Bridgeline) | 2 | 4 | 3 | 5 | **18.0** | $149* | $14,900 | ~67 |
| 4 | Finance report builder (Ledgerlytics) | 3 | 3 | 4 | 4 | **18.0** | $149 | $14,900 | ~67 |
| 5 | Performance caching layer (Swiftcache) | 2 | 5 | 2 | 5 | **17.5** | $299* | $29,900 | ~34 |
| 6 | Courier reporting (RouteMetrics) | 3 | 4 | 3 | 4 | **17.5** | $249 | $24,900 | ~40 |
| 7 | Legal-software monitoring (Caseguard) | 3 | 4 | 3 | 4 | **17.5** | $149* | $14,900 | ~67 |
| 8 | STR damage-claim portal (ClaimSnap) | 3 | 4 | 3 | 4 | **17.5** | $49* | $4,900 | ~204 |
| 9 | HOA ordinance scanner (OrdinanceWatch) | 3 | 4 | 3 | 4 | **17.5** | $99* | $9,900 | ~101 |
| 10 | Multi-channel inventory sync (StockSync) | 3 | 2 | 4 | 4 | **17.0** | $249 | $24,900 | ~40 |
| 11 | Lien-waiver tracker (WaiverTrack) | 4 | 4 | 3 | 3 | **17.0** | $99 | $9,900 | ~101 |
| 12 | IoT analytics (TelemetryHub) | 2 | 4 | 3 | 4 | **16.5** | $299 | $29,900 | ~34 |
| 13 | SaaS spend-audit (SpendLens) | 4 | 2 | 4 | 3 | **16.5** | $50 | $5,000 | ~200 |
| 14 | AP / invoice automation (InboxAP) | 2 | 2 | 3 | 5 | **16.0** | $199* | $19,900 | ~51 |
| 15 | AI claim-narrative drafter (ClaimScribe) | 3 | 4 | 3 | 3 | **16.0** | $149 | $14,900 | ~67 |

## Why dunning won
- **Fastest to revenue + strongest moat** in one idea — rare. Most high-moat ideas (caching, middleware, invoices) are slow to sell; most fast-revenue ideas (spend-audit) sit in crowded fields.
- 100% backend/Stripe/webhook work — the owner's wheelhouse; ties to prior webhook-reliability interest.
- ROI conversation is frictionless ("you're losing ~$X/mo to failed cards").
- Independently surfaced twice in a separate 50-idea list — a third-party demand vote.

## Key tension to remember
Rank ≠ revenue-difficulty. The top-ranked ideas (dunning ~134 logos, log parser ~345) need the **most** customers because their edge is speed/moat, not price. The quieter high-ACV plays (caching, IoT, courier, inventory) hit $10k with **34–40 logos** — an easier sales grind. Lever that collapses logo counts: **per-seat / per-location pricing**.

## Runner-up to watch
**Log parser (Tracepoint)** — owner is the target user, so fastest validation + cheap dev-channel distribution. Good parallel test alongside dunning.
