
# Product Document — AI Representation Optimizer

## 1. The Problem

Shopping is shifting. Customers increasingly ask AI agents 
like ChatGPT and Google AI Mode for product recommendations 
before visiting any store. These AI agents read store data 
directly — product descriptions, policies, FAQs, store 
identity — and decide which stores to recommend.

When a merchant's store data is weak, incomplete, or 
ambiguous, the AI cannot confidently understand or represent 
their products. The result: the merchant gets skipped or 
misrepresented in AI recommendations.

This creates a compounding problem:
- No AI recommendation → no customer visit
- No customer visit → no sale
- No sale → no reviews
- No reviews → AI has even less signal to trust the store
- Competitor with better data gets recommended instead
- Gap widens permanently over time

The merchant experiences declining sales, weakening brand 
value, and rising customer acquisition costs — without ever 
understanding why. They have no tool to diagnose the root 
cause or know what to fix.

That is the problem we solve.

AuraScan not only diagnoses these gaps but closes the 
loop — merchants can apply AI-generated fixes directly 
to their Shopify store from the dashboard, without 
touching Shopify admin manually.

## 2. Who This Is For

**Primary user: Shopify store owners like Ravi.**

Ravi runs an online store selling motorcycle gear. He spends 
₹15,000/month on Instagram ads and gets traffic — but sales 
remain low and he can't figure out why.

What Ravi doesn't know: AI agents like ChatGPT and Google AI 
Mode now filter stores before a customer ever clicks an ad. 
These agents read store data directly. If that data is weak, 
Ravi gets skipped — regardless of his ad spend.

He needs a tool that shows him exactly what's broken, how 
severe each problem is, and what to fix first.

That is who we built this for.

## 3. What We Built

We built a merchant-facing diagnostic tool called AuraScan 
that connects to a Shopify store via Admin API, audits it 
across 14 checks, and generates an AI Readiness Score out 
of 100 with a ranked action plan.

The tool works in four stages:
1. **Connect** — authenticates with the merchant's Shopify 
   store and pulls product data, pages, policies, and store 
   identity via Admin API
2. **Audit** — runs 14 diagnostic checks across product 
   quality, store identity, policy coverage, and page 
   completeness — classifying each issue as Critical, High, 
   or Medium severity
3. **Score** — calculates an AI Readiness Score (0-100) 
   using reward-based weighted scoring across four 
   categories:products, store identity, policies, and pages
4. **Advise & Fix** — uses Groq (Llama 3.3 70B) to 
   generate an executive summary, on-demand per-issue 
   fix advice, and AI-generated fix content that merchants can review 
   and push directly to Shopify in one click

The output is a Streamlit dashboard showing the score, 
all issues ranked by severity, and actionable 
recommendations — giving merchants a clear picture of 
why AI agents are skipping them and exactly what to fix.

## 4. Core User Journey

Ravi opens AuraScan and the first thing he sees is a number — 51/100. He doesn't need to read anything else to know 
something is wrong.

Below the score, a Groq-generated summary tells him exactly why in plain English — 
3 of his products have no description, his store has no refund policy and AI agents 
are skipping him because of it.

He clicks into Critical Issues. Each problem is named — not vague.
"[Riding Jacket] Missing Product Description." He clicks it, reads the AI advice, 
clicks Apply Fix. Groq generates a description. He reviews it, confirms it. It 
pushes live to his Shopify store instantly.

His score jumps to 74.

He works through the list. Every fix is one click. Every 
recommendation is specific to his product. By the end, his 
store scores 100/100 — fully readable, fully trustworthy, 
ready to be recommended by AI agents.

He didn't touch Shopify admin once.

## 5. Key Product Decisions

**Decision 1: Why Track 5 over other tracks**
Track 1 (AI Shopping Agent) was familiar territory — we had 
built something similar for our Infosys project. We chose 
Track 5 because it addresses a deeper, less visible problem. 
Every merchant on Shopify faces it, but none can see it. 
It's not about building another shopping assistant — it's 
about diagnosing the invisible layer that determines whether 
AI agents recommend you or skip you. That's why we named it 
AuraScan — it scans what merchants can't see themselves.

**Decision 2: Reward-based scoring over penalty-based**
We initially built penalty-based scoring — start at 100, 
deduct points for each issue. We switched to reward-based 
with partial credit because it better reflects reality. A 
product with 3 out of 5 fields filled deserves a higher 
score than a product with 0 fields filled. Penalty-based 
scoring treated both the same — zero. Reward-based scoring 
makes improvement visible and motivating. When a merchant 
fixes one issue, they see their score jump immediately. 
That feedback loop is the core of our product experience.

**Decision 3: Agentic Apply Fix with merchant approval**
We could have built fully automatic fixes — detect issue, 
generate fix, push to Shopify, done. We didn't. Auto-pushing 
AI-generated content without merchant review risks putting 
wrong data live on a real store. We chose a one-click 
approve pattern — Groq generates the fix, merchant reviews 
it, merchant confirms, then it pushes. This gives merchants 
control while removing the friction of manual editing.

**Decision 4: Lazy loading for Groq advice**
Generating AI advice for all issues on page load would 
take 20+ seconds and burn rate limits on content the 
merchant never reads. Advice is fetched on demand — 
only when the merchant explicitly requests it.

**Decision 5: Four separated files, one job each**
shopify_client.py only talks to Shopify. audit_engine.py 
only analyses data. groq_advisor.py only talks to Groq. 
app.py only handles the UI. Each file has one 
responsibility. If Shopify changes their API tomorrow, 
only one file changes. This is not over-engineering — 
it's the minimum structure needed to keep the codebase 
maintainable under deadline pressure.

## 6. What We Chose NOT to Build and Why

**Competitor comparison**
Requires access to other merchants' stores. Competitors 
will never install our app and grant access. Technically 
impossible without consent. Noted as future scope if 
Kasparro builds a data partnership layer.

**Image quality analysis**
Shopify API returns image URLs, not images. Analysing 
quality requires computer vision — a separate ML pipeline 
outside our scope and stack.

**Price analysis**
Requires competitor pricing data from outside Shopify. 
Same access problem as competitor comparison.

**Domain name alignment**
Belongs to SEO layer, not AI agent layer. AI agents read 
store content, not domain names. Not relevant to our 
problem statement.

**Fully automatic fixes without approval**
Auto-pushing AI content to a live store without merchant 
review risks publishing wrong data. We chose approve-then-
push over fully autonomous fixing.

**Future scope (post-hackathon):**
- Inventory & Variant Intelligence — track variant-level 
  sales velocity, stock alerts, demand-based notifications 
  using read_orders and read_inventory scopes
- Competitor Benchmarking via data partnerships — compare 
  product descriptions, keywords, pricing, tags against 
  market competitors
- Market-Driven Description Optimization — rewrite 
  descriptions using trending search terms and category 
  keywords
- Dynamic Pricing Intelligence — flag overpriced or 
  underpriced products relative to market benchmarks
- Demand-Based Promotions — surface high-demand products 
  with discount recommendations to maximize AI promotion
- Sales data and inventory intelligence via read_orders 
  and read_inventory scopes — variant-level velocity 
  tracking, stock alerts, demand-based promotions

## 7. Tradeoffs We Encountered

**Tradeoff 1: Speed vs completeness of audit**
We audit 14 checks. A more thorough audit would include 
metafield completeness, image quality, review sentiment, 
and variant stock levels. We chose focused depth over broad coverage — the checks 
we built directly impact AI agent readiness and are 
fully supported by the Shopify Admin API.

**Tradeoff 2: 10-second cache vs real-time accuracy**
We cache store data for 10 seconds to avoid hammering 
the Shopify API on every Streamlit rerender. This means 
score updates appear within 10 seconds of a fix being 
applied — not instantly. We accepted this small delay 
to keep the dashboard stable and API-friendly.

**Tradeoff 3: Groq speed vs model accuracy**
Llama 3.3 70B on Groq is fast and free. A more capable 
model might generate better fix advice. We chose speed 
and accessibility over maximum accuracy — for a 
merchant-facing tool, fast and good enough beats slow 
and perfect.

**Tradeoff 4: Single store vs multi-store**
AuraScan currently audits one store at a time using a 
hardcoded Admin API token. A production version would 
use OAuth to let any merchant connect their store. We 
chose single-store simplicity to ship a working product 
within the deadline. The OAuth architecture is 
understood and documented for future implementation.

**Tradeoff 5: Auto-fix scope**
The agentic Apply Fix currently works for three issue 
types — descriptions, tags, and categories. High and 
Medium issues like missing policies and pages require 
manual action in Shopify admin. We chose to build 
auto-fix only where AI-generated content is 
unambiguous and safe to push. Policy pages require 
human-written legal content — auto-generating them 
would be irresponsible.