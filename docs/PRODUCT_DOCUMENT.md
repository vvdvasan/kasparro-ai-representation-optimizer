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

## 2. Who This Is For

**Primary user: Shopify store owners like Ravi.**

Ravi runs an online store on Shopify. He has decent products 
and spends ₹15,000/month on Instagram ads. Traffic comes in 
but sales remain low. He can't figure out why.

What Ravi knows: Social media ads create visibility. If he 
posts enough, customers will find him.

What Ravi doesn't know: AI agents like ChatGPT and Google AI 
Mode are now the first filter before a customer even clicks 
an ad or visits a store. These agents read his store data 
directly. If that data is weak, AI skips him — regardless 
of how much he spends on ads.

What Ravi needs: A diagnostic tool that shows him exactly 
why AI agents are skipping his store, what's broken in his 
data, how severe each problem is, and what to fix first — 
with specific, actionable recommendations.

That is who we built this for.

## 3. What We Built

We built a merchant-facing diagnostic tool called StoreSignal 
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
   based on issues found, deducting points by severity
4. **Advise** — uses Groq (Llama 3.3 70B) to generate an 
   executive summary of the store's AI readiness and 
   on-demand specific fix advice for each issue

The output is a Streamlit dashboard showing the score, 
all issues ranked by severity, and actionable 
recommendations — giving merchants a clear picture of 
why AI agents are skipping them and exactly what to fix.

## 4. Core User Journey



## 5. Key Product Decisions
## 6. What We Chose NOT to Build
## 7. Tradeoffs We Encountered