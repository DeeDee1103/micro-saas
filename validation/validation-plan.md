# One-Week Parallel Build + Validation Plan

The goal: in seven days, build the first slice (M0–M2) of one idea **while** putting the problem in front of real buyers — so by Sunday you have both working code and a real read on demand. The calls shape the build; the build converts the leads.

---

## Part A — The shared playbook (same for every idea)

### The one rule: don't pitch, investigate
You're not selling yet. You're finding out whether the pain is real and whether people already spend time or money on it. The fastest way to fool yourself is to ask "would you use a tool that…" — people say yes to be nice. Ask about their **past and present behavior** instead.

### The parallel week
- **Mon** — Pick the idea. Write a one-sentence problem statement. Start the **M0 build** (scaffold + CLAUDE.md + schema). Stand up the **smoke-test landing page**. List your 10 target people and where they hang out. Send the first 10 outreach messages.
- **Tue** — Build **M1**. Post the *problem* (not the product) in 2 niche communities. Launch ~$50 of targeted ads at the landing page. Book calls as replies come in.
- **Wed** — Build **M2**. Run 2–3 discovery calls. Watch signups.
- **Thu** — Continue build. Run 2–3 more calls. **Rewrite the landing headline using the exact words you heard on calls.**
- **Fri** — Run remaining calls. Make the **pre-sale ask** to the warmest 2–3 people (you now have M0–M2 to show them).
- **Sat** — Tally signups, call insights, and pre-sale commitments against the scorecard below.
- **Sun** — Decide: double down, re-niche, or drop. Either way you've lost a week, not a quarter.

### The 7 universal discovery questions (ask everyone)
1. Walk me through the last time you dealt with [problem]. What did you actually do?
2. How do you handle [X] today — what tools, spreadsheets, or people are involved?
3. What's the most frustrating part, and how often does it happen?
4. What does it cost you — hours per week, dollars, or both?
5. Have you looked for a tool to fix this? What did you try, and why did you stop?
6. *(If they use a tool)* What does it not do that you wish it did, and what do you pay for it?
7. Who else deals with this that I should talk to? *(referrals)*

Then, only at the end: **"What would have to be true for you to switch?"** and **"What's fixing this worth to you?"** — never "would you pay $X?"

### The landing-page smoke test (same skeleton, idea-specific copy)
A single page that tests intent without a product behind it:
- **Headline:** the outcome or pain in their words (you'll refine it after calls)
- **Subhead:** how it works, one line
- **3 bullets:** the core value
- **Primary CTA:** "Get early access" → email capture (the fake door)
- **Optional second CTA:** "See pricing" → reveal 3 tiers → a click here is a *buying-intent* signal worth more than an email
- **Track:** visitors → email signups → pricing clicks
- **Stack:** Carrd/Framer/Tally + Plausible for speed, or just ship a Next.js page (you'll have one anyway). Drive traffic via the 2 community posts + $50 ads.

### Outreach templates
**Cold DM / email (Mom-Test framed):**
> Hey [name] — I'm researching how [role, e.g. membership-site operators] handle [problem, e.g. failed subscription payments]. Not selling anything; I'm trying to understand the workflow before I build. Could I steal 15 minutes this week to hear how you deal with it today? Happy to share what I learn from others doing the same.

**Community post (problem, not product):**
> For those of you running [context] — how are you currently handling [problem]? I keep seeing people duct-tape this with [spreadsheets/manual work] and I'm curious whether that's universal or just me. What's your setup?

**Pre-sale ask (Friday, to warm leads):**
> This is exactly the problem I'm building for. I've got an early version working. Want to be design partner #1? It's $[X]/mo, first month free in exchange for feedback. I'll set you up personally.

### Go / no-go scorecard (Saturday)
**Green (build on):** 10+ email signups in 48h from one niche post · 3+ people described the pain *unprompted* and named what they pay/spend today · 2+ pre-sale "yes, set me up" commitments · landing CTA conversion >5–10% of visitors.
**Yellow (re-niche):** interest but vague; people like it but don't currently spend time/money on it; <5 signups → try a narrower audience and rerun.
**Red (drop):** "cool idea" with zero current spend, no unprompted pain, <2 signups, no pre-sale interest.

---

## Part B — Per-idea cards

> Each card: **Who** (the 10) + where to find them · **Sharpest questions** (add to the 7 universal) · **Landing angle** (headline + CTA).

### 1. Dunning / failed-payment recovery
- **Who:** operators of membership sites, course creators, subscription-box and small-SaaS founders, agencies on retainers, Patreon/Memberstack/Outseta users. **Where:** r/SaaS, r/Entrepreneur, r/membershipsites, Indie Hackers, MicroConf Connect, r/stripe, #buildinpublic on X.
- **Ask:** How much MRR do you lose to failed cards monthly? When a payment fails, do you do anything, or just let Stripe retry? Tried Churnkey / Baremetrics Recover / Stripe Smart Retries — why or why not? What % do you actually recover?
- **Landing:** "Recover the revenue your failed cards are quietly costing you." → CTA: "See what you're losing — get early access."

### 2. Log parser + alerting
- **Who:** solo devs and small-startup CTOs running prod apps, SREs/DevOps at <50-person companies. **Where:** Hacker News, r/devops, r/sre, r/selfhosted, r/webdev, Lobsters, dev Discords.
- **Ask:** How do you know *right now* if your app is throwing errors in prod? Do you pay for Datadog/Splunk/Better Stack — what's it cost? What stopped you adopting one? Last incident — how did you find out?
- **Landing:** "Error alerts for your app — without the Datadog bill." → CTA: "Get early access — send a test log."

### 3. Legacy↔modern integration middleware
- **Who:** ops/IT at SMBs in your chosen vertical running a legacy system + a modern tool, fractional ops consultants, MSPs. **Where:** the vertical's subreddit, r/sysadmin, r/msp, industry Slack/FB groups, **Upwork** (search the recurring "sync data between X and Y" gigs).
- **Ask:** Which two systems don't talk to each other? How do you move data between them today — CSV, manual entry, someone's job? Hours/week? Tried Zapier or an integrator — why didn't it stick?
- **Landing:** "Stop re-keying data between [System A] and [System B]." → CTA: "Book a 15-min fit call."

### 4. Subscription-finance report builder
- **Who:** finance managers, controllers, fractional CFOs, RevOps at subscription businesses (10–200 employees). **Where:** r/SaaS, r/FPandA, r/bookkeeping, fractional-CFO communities, LinkedIn finance groups.
- **Ask:** How do you build the monthly board/revenue report today, and how long does it take? What can't Stripe/Chargebee's native reports do? You export to Excel — for what exactly? What does leadership always ask for that you rebuild by hand?
- **Landing:** "The subscription reports Stripe won't build for you." → CTA: "Get early access."

### 5. Performance caching / prefetch layer
- **Who:** CTOs/eng leads at vertical-SaaS vendors with a slow app (find them via their own G2/Capterra "it's slow" reviews), plus their ops teams. *Sell to vendors — fewer, more technical buyers.* **Where:** Hacker News, vertical-SaaS founder communities, LinkedIn, direct outreach.
- **Ask:** Where's your app slowest, and what have you tried? Is performance driving complaints or churn? Who owns perf internally? What would near-instant reads be worth to you?
- **Landing:** "Make your slow API feel instant — a drop-in caching layer." → CTA: "Request a latency audit." *(consultative, not self-serve)*

### 6. Courier / logistics reporting
- **Who:** ops managers and owners at courier / last-mile / delivery firms still living in spreadsheets. **Where:** r/logistics, r/couriers, r/smallbusiness, logistics FB groups, LinkedIn logistics.
- **Ask:** How do you report on delivery and driver performance today? Hours/week in spreadsheets? Which metrics matter most (on-time %, per-driver)? What can't your current TMS show you?
- **Landing:** "Driver and delivery KPIs without the spreadsheet grind." → CTA: "Get early access — upload a sample CSV."

### 7. Legal-software health monitoring + backup
- **Who:** office managers and IT at small law firms, solo/small-firm attorneys, MSPs serving law firms. **Where:** r/Lawyertalk, r/legaltech, r/msp, legal office-manager groups.
- **Ask:** Has your case-management software ever gone down or lost data — what happened? Do you back it up, and how? Who notices when it's down? What would monitoring + guaranteed backup be worth?
- **Landing:** "Know the moment your legal software breaks — and never lose data again." → CTA: "Get early access."

### 8. STR damage-claim portal
- **Who:** Airbnb/VRBO hosts (especially multi-property), STR property managers, co-hosts. **Where:** r/AirBnB, r/airbnb_hosts, r/vrbo, STR Facebook groups, Hostaway/Hospitable communities.
- **Ask:** Last time a guest damaged something — walk me through filing the claim. How long did it take, and did you get reimbursed? What was most painful — photos, paperwork, the insurer? How many claims a year?
- **Landing:** "File a damage claim in minutes — snap photos, we draft the report." → CTA: "Get early access."

### 9. HOA ordinance compliance scanner
- **Who:** HOA board members, community-association managers (CAMs), property managers. **Where:** r/HOA, r/PropertyManagement, Community Associations Institute (CAI) groups, HOA-manager FB groups.
- **Ask:** How do you keep up with changing city ordinances? Ever been fined or blindsided by a rule? How do you check compliance now, and who's responsible? What does a violation/fine cost?
- **Landing:** "Catch ordinance violations before the fine arrives." → CTA: "Get early access — pick your city." *(pilot one city)*

### 10. Multi-channel inventory sync
- **Who:** multi-channel e-commerce sellers (Shopify + Etsy + Woo), small brands, makers. **Where:** r/ecommerce, r/shopify, r/Etsy, r/FulfillmentByAmazon, maker/seller FB groups.
- **Ask:** How do you keep stock in sync across channels today? Ever oversold — how often? What do you do manually to prevent it? Tried Sellbrite or similar — why or why not?
- **Landing:** "Never oversell again — real-time stock sync across Shopify, Etsy & more." → CTA: "Get early access — connect your store."

### 11. Lien-waiver / bid-security tracker
- **Who:** GC office managers, construction project admins, small general contractors, subcontractor coordinators. **Where:** r/Construction, r/Contractor, construction FB groups, LinkedIn construction.
- **Ask:** How do you track lien waivers and bid securities now — spreadsheet? Ever missed one or had a payment held up? Who chases signatures? Hours a month on it?
- **Landing:** "Never lose track of a lien waiver again." → CTA: "Get early access."

### 12. IoT analytics dashboard
- **Who:** ops/plant managers and IoT product owners at manufacturing/logistics firms running device fleets. **Where:** r/IOT, r/manufacturing, r/PLC, industrial-IoT LinkedIn groups.
- **Ask:** What device data do you collect, and how do you report on it? Can your platform show the KPIs you actually need? Do you export to Excel — for what? What's invisible today that you wish you could see?
- **Landing:** "Turn device data into the dashboards your IoT platform won't build." → CTA: "Request access."

### 13. SaaS spend-audit tool
- **Who:** small-business owners, office managers, ops leads, fractional CFOs/bookkeepers. **Where:** r/smallbusiness, r/Entrepreneur, r/bookkeeping, ops FB groups.
- **Ask:** Can you list every SaaS subscription you pay for right now? Ever found one you'd forgotten? How do you track them, and who watches the spend?
- **Landing:** "Find the subscriptions you forgot you're paying for." → CTA: "Get early access — see your savings."

### 14. AP / invoice automation
- **Who:** AP clerks, controllers, bookkeepers, office managers at mid-market firms with high invoice volume. **Where:** r/Accounting, r/bookkeeping, r/Controller, finance LinkedIn groups, Upwork (data-entry gigs).
- **Ask:** How many invoices a month, and how are they processed — manual entry? Hours on it? Error rate? Tried Bill.com or Ramp — why or why not (too pricey/complex)?
- **Landing:** "Stop hand-keying invoices — extract, match, approve." → CTA: "Get early access — try it on one invoice."

### 15. AI claim-narrative drafter (insurance)
- **Who:** insurance brokers/agents, claims handlers at small agencies. **Where:** r/Insurance, r/InsuranceAgent, insurance-agent FB groups, LinkedIn insurance.
- **Ask:** How long does writing a claim narrative take, and what's your process? Do you reuse templates? What's the most repetitive part? How many a week?
- **Landing:** "Draft claim narratives in minutes, not hours." → CTA: "Get early access."

---

## Part C — If you're starting with dunning (recommended)
Run card #1 this week against the shared playbook. Concretely: Monday, scaffold M0 of the dunning build and put up the "Recover the revenue your failed cards are quietly costing you" page; reach out to 10 membership/SaaS operators; by Friday, show the warmest 2–3 your working detect-and-remind loop and make the design-partner pre-sale ask. Two pre-sale yeses + 10 signups = green light to push to M3–M4.
