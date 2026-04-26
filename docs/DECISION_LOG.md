# Decision Log — AuraScan
## Team StoreSignal | Track 5 — Kasparro Agentic Commerce Hackathon

---

## Decision 001: Track Selection
**Date:** 2026-04-07
**Decision:** Chose Track 5 (AI Representation Optimizer) over Tracks 1–4.
**Reasoning:** Track 1 was familiar ground — a similar e-commerce 
assistant had been built during a prior internship. Track 5 addresses 
the deeper, less visible problem: not helping buyers find products, but 
ensuring merchants can be found by AI agents in the first place. The 
supply-side problem is higher-order, more underserved, and more directly 
aligned with what Kasparro builds commercially.
**Alternative considered:** Track 1 — rejected for insufficient 
differentiation.
**Tradeoff:** More product-intensive with fewer flashy demos. Depth 
over polish.

---

## Decision 002: Tool Name
**Date:** 2026-04-07
**Decision:** Named the tool AuraScan. Named the team StoreSignal.
**Reasoning:** AuraScan communicates the core idea precisely — scanning 
the invisible layer of a store that AI agents perceive but merchants 
cannot see. StoreSignal was retained as the registered team name.
**Alternative considered:** StoreSignal as both team and tool name — 
rejected for lacking diagnostic connotation.
**Tradeoff:** None significant.

---

## Decision 003: Audit Scope — 14 Checks
**Date:** 2026-04-08
**Decision:** Scoped the audit to 14 deterministic checks across four 
categories: products (6), store identity (2), policies (4), pages (2).
**Reasoning:** These checks cover the fields Shopify's Agentic Plan 
exposes directly to AI agents and are fully supported by the Admin API. 
Broader checks — image quality, review sentiment, metafields, domain 
configuration — require computer vision, third-party data, or additional 
API passes that fall outside the timeline.
**Alternative considered:** 30+ check audit — rejected. Shallow coverage 
across many dimensions is less defensible than reliable coverage across 
fewer.
**Tradeoff:** Narrower scope in exchange for higher reliability and full 
explainability on every check.
**Known removal:** SEO meta description was scoped then removed. The 
Shopify Admin API does not expose metafields_global_description_tag on 
standard product endpoints without a separate metafield pass. Removed 
to avoid false positives.

---

## Decision 004: Scoring Model — Reward-Based over Penalty-Based
**Date:** 2026-04-10
**Decision:** Replaced penalty-based scoring with reward-based weighted 
partial credit.
**Reasoning:** Penalty-based scoring treated a product with 3 of 6 fields 
filled identically to one with 0 — both scored zero. This obscured 
progress and made the tool feel punitive. Reward-based scoring makes 
improvement visible immediately: when a merchant fixes one issue, the 
score moves. That feedback loop is the core product experience.
**Weights:** Description (4), category (3), tags (2), vendor (1) per 
product. Products contribute 60 points total; store identity 15; 
policies 15; pages 10.
**Alternative considered:** Pass/fail checklist — rejected for failing 
to prioritise what to fix first.
**Tradeoff:** Slightly more complex to explain; significantly more 
motivating in practice.

---

## Decision 005: Authentication — Direct Token over OAuth
**Date:** 2026-04-18
**Decision:** Replaced OAuth client_credentials flow with a direct Admin 
API access token (shpat_).
**Reasoning:** The OAuth approach returned "app_not_installed" — that 
flow is designed for public apps installed by multiple merchants via the 
App Store, not single-store private integrations. The direct token is 
simpler, more reliable, and architecturally appropriate for this use case.
**Alternative considered:** Persisting with OAuth — rejected after 
confirming it is inappropriate for single-store private access.
**Tradeoff:** Single-store limitation in exchange for zero authentication 
friction. OAuth remains the correct upgrade path for multi-merchant 
production use.

---

## Decision 006: AI vs Deterministic Boundary
**Date:** 2026-04-18
**Decision:** All 14 audit checks and score calculations are 
deterministic. Groq is used exclusively for advice generation and fix 
content — never for scoring.
**Reasoning:** LLM-based scoring is non-deterministic. The same store 
could score differently on repeated runs. Merchants cannot trust a 
diagnostic score that varies randomly. The audit must be reproducible 
and explainable. LLM involvement is appropriate only where creative 
variation is acceptable — advice and content, not measurement.
**Alternative considered:** Using Groq to evaluate description quality 
— rejected for introducing non-determinism into the scoring layer.
**Tradeoff:** The deterministic boundary reduces nuance (a 60-character 
description passes the same as a 600-character one) but makes every 
score fully trustworthy and auditable.

---

## Decision 007: Agentic Fix — Approve Before Push
**Date:** 2026-04-18
**Decision:** The Apply Fix pipeline requires explicit merchant approval 
before any write to Shopify.
**Reasoning:** Auto-pushing AI-generated content to a live store risks 
publishing wrong or off-brand product data without the merchant's 
knowledge. A store is a business — content changes must go through the 
owner. The approve-then-push pattern gives merchants full control while 
removing the friction of manual editing in Shopify admin.
**Alternative considered:** Fully automatic fixes — rejected for removing 
merchant agency over their own store data.
**Tradeoff:** One additional confirmation step in exchange for a 
meaningful reduction in risk of incorrect data being published.

---

## Decision 008: Auto-Fix Scope — Three Issue Types Only
**Date:** 2026-04-18
**Decision:** Auto-fix is available only for product descriptions, tags, 
and categories. All other issue types surface advice only.
**Reasoning:** Descriptions, tags, and categories are content fields 
where AI generation is unambiguous, reviewable in seconds, and safe to 
push. Policy pages, About Us, and FAQ require human-authored legal and 
editorial content. Auto-generating a return policy would be irresponsible 
and potentially harmful to the merchant's legal standing.
**Alternative considered:** Auto-fix for all 14 issue types — rejected 
because several involve content that cannot responsibly be AI-generated 
without significant human oversight.
**Tradeoff:** Narrower auto-fix scope in exchange for responsible, 
defensible output on every fix applied.

---

## Decision 009: Lazy Loading for Groq Advice
**Date:** 2026-04-18
**Decision:** Groq advice is generated on demand when the merchant 
explicitly requests it — not pre-generated on dashboard load.
**Reasoning:** A store with 26 issues would require 26 sequential Groq 
calls on every load, adding 20+ seconds of latency and consuming rate 
limits on content the merchant may never read. On-demand loading keeps 
the dashboard fast and API usage efficient.
**Alternative considered:** Pre-generating all advice on load — rejected 
for latency, rate limit consumption, and wasted generation.
**Tradeoff:** The merchant clicks to see advice rather than seeing it 
immediately. The speed and efficiency gain justifies this.

---

## Decision 010: Dual-Layer Caching Strategy
**Date:** 2026-04-18
**Decision:** Store data is cached at a 10-second TTL. The executive 
summary is cached separately at 300 seconds.
**Reasoning:** A single cache forces a choice between real-time score 
updates (short TTL) and avoiding unnecessary Groq regeneration (long 
TTL). Separating the two caches resolves this — store data refreshes 
frequently for near-real-time score feedback after fixes, while the 
summary regenerates only when meaningfully needed.
**Alternative considered:** Single unified cache — rejected for forcing 
an unnecessary tradeoff.
**Tradeoff:** Marginally more complex cache management in exchange for 
both real-time responsiveness and API efficiency.

---

## Decision 011: Single Store vs Multi-Store
**Date:** 2026-04-07
**Decision:** Built for single-store operation using a hardcoded Admin 
API token. OAuth-based multi-merchant support was deferred.
**Reasoning:** Multi-merchant support requires OAuth 2.0, a token storage 
layer, and per-merchant data isolation — a significant scope addition 
consuming 3–4 days of a 14-day timeline without meaningfully improving 
the submission. All Shopify communication is isolated in 
shopify_client.py. Multi-merchant support requires changes to that file 
alone — the architecture is ready; the scope was not.
**Alternative considered:** OAuth multi-merchant from the start — 
rejected as outside the timeline.
**Tradeoff:** Single-store limitation now. Clear, documented upgrade path 
for production.