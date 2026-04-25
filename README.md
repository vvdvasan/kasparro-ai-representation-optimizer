# AuraScan — AI Representation Optimizer for Shopify

**Team StoreSignal | Track 5 — Kasparro Agentic Commerce Hackathon**

---

## What This Is

AuraScan is a merchant-facing diagnostic tool that helps 
Shopify store owners understand how AI agents perceive 
their store — and what to fix to improve that perception.

When a customer asks ChatGPT or Google AI Mode to recommend 
a product, those agents read store data directly. If that 
data is incomplete, vague, or missing, the merchant gets 
skipped. Most merchants have no visibility into this problem.

AuraScan makes it visible — and fixable.

---

## What It Does

AuraScan connects to a Shopify store via Admin API, runs 
14 diagnostic checks across product data, store identity, 
policies, and pages, and generates an AI Readiness Score 
out of 100. For each issue found, it provides a severity 
rating, a specific fix recommendation, and an AI-generated 
fix that the merchant can review and push directly to 
Shopify in one click.

**Score journey on our demo store (RiderzPlanet):**
0/100 (intentionally broken) → 51/100 (baseline with 
mixed data) → 74/100 (after fixing critical issues) → 
100/100 (fully optimised)

---

## The 14 Audit Checks

Products (6): Description, Category, Tags, Vendor, SKU, 
Weight — Store (2): Store Name, Store Description — 
Policies (4): Refund, Privacy, Shipping, Terms of Service 
— Pages (2): About Us, FAQ

---

## Tech Stack

Python 3.11 · Streamlit · Groq API (Llama 3.3 70B) · 
Shopify Admin API 2026-04 · python-dotenv

---

## Project Structure

kasparro-ai-representation-optimizer/
├── app.py                  — Streamlit dashboard
├── src/
│   ├── shopify_client.py   — Shopify API layer
│   ├── audit_engine.py     — 14-check audit + scoring
│   └── groq_advisor.py     — Groq AI advice + fix generation
├── docs/
│   ├── PRODUCT_DOCUMENT.md
│   └── TECHNICAL_DOCUMENT.md
├── requirements.txt
└── .env.example

---

## Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/vvdvasan/kasparro-ai-representation-optimizer.git
cd kasparro-ai-representation-optimizer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**

Copy `.env.example` to `.env` and fill in your credentials:

SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_your_token_here
GROQ_API_KEY=gsk_your_key_here

To get your Shopify Admin API token: Shopify Admin → 
Settings → Apps and sales channels → Develop apps → 
your app → API credentials → Admin API access token.

To get your Groq API key: console.groq.com → API Keys → 
Create API Key.

**4. Run the dashboard**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Submission Details

**Team:** StoreSignal
**Members:** Danavasan V (23BAU012) · Dhatchanamoorthy K 
(23BAD027) — Kumaraguru College of Technology, Coimbatore
**Track:** 5 — AI Representation Optimizer
**Demo video:** [link to be added]
