# Technical Document — AuraScan
## AI Representation Optimizer for Shopify Merchants
### Team: StoreSignal | Track 5 — Kasparro Agentic Commerce Hackathon

---

## 1. System Architecture

AuraScan is a four-component pipeline built in Python, 
where each component has a single responsibility and 
communicates with the next through well-defined interfaces.

'''
Shopify Admin API
↓
shopify_client.py   — data retrieval layer
↓
audit_engine.py     — analysis and scoring layer
↓
groq_advisor.py     — AI advice generation layer
↓
app.py              — Streamlit presentation layer
↑
Shopify Admin API   — write-back layer (Apply Fix)
'''
Data flows in one direction during an audit. On a fix, 
the write-back path returns from app.py through 
shopify_client.py to Shopify. No component holds state 
between sessions — all state is managed by Streamlit's 
session_state.

---

## 2. Component Breakdown

**shopify_client.py — Data Retrieval Layer**

This component handles all communication with the 
Shopify Admin API. It uses a static Admin API access 
token (shpat_) loaded from environment variables via 
python-dotenv. Four read functions fetch products, 
pages, shop metadata, and policies respectively. One 
write function — update_product() — executes the 
agentic fix by sending a PUT request to the products 
endpoint with AI-generated content.

The token is loaded at module level into a shared 
HEADERS dictionary, which is reused across all requests. 
API version is pinned to 2026-04 to prevent unexpected 
breaking changes from Shopify's rolling releases.

**audit_engine.py — Analysis and Scoring Layer**

This component performs all diagnostic logic. It 
receives raw Python dictionaries from shopify_client.py 
and applies 14 deterministic checks across four 
categories. No LLM is involved at this stage — every 
check is a straightforward conditional on the presence 
or quality of a data field. This is an intentional 
design decision: audit logic must be consistent, 
explainable, and reproducible. LLM involvement at the 
audit stage would introduce non-determinism into the 
scoring, which would undermine merchant trust.

The scoring model is reward-based with weighted partial 
credit. Products contribute up to 60 points based on 
field completeness (description weighted at 4, category 
at 3, tags at 2, vendor at 1). Store identity contributes 
up to 15 points, policies up to 15 points, and pages up 
to 10 points. The final score is capped between 0 and 100.

**groq_advisor.py — AI Advice Generation Layer**

This component handles all LLM interactions via the 
Groq API using Llama 3.3 70B. It exposes three functions. 
get_executive_summary() generates a store-level diagnosis 
on dashboard load. get_fix_advice() generates contextual, 
per-issue recommendations when the merchant requests them. 
generate_fix_content() produces ready-to-apply content — 
a product description, tag list, or category name — that 
is passed to shopify_client.py for write-back.

Each function uses a tightly scoped prompt that constrains 
the model to return only what is needed. 
generate_fix_content() prompts explicitly instruct the 
model to return plain text with no labels, no formatting, 
and no preamble — ensuring the output can be written 
directly to Shopify fields without post-processing.

**app.py — Presentation and Orchestration Layer**

This component renders the Streamlit dashboard and 
coordinates the full pipeline. Store data is fetched and 
cached with a 10-second TTL using @st.cache_data, enabling 
near-real-time score updates after fixes are applied. The 
executive summary is cached separately with a 300-second 
TTL to prevent unnecessary Groq calls on every data 
refresh. Per-issue advice and generated fix content are 
stored in Streamlit's session_state to persist across 
rerenders without repeat API calls.

The Apply Fix flow is as follows: the merchant clicks 
"Get AI Advice," which calls get_fix_advice() and 
generate_fix_content() simultaneously. The suggested 
content is displayed for review. The merchant clicks 
"Apply Fix to Shopify," which calls update_product() 
with the appropriate field mapped from the issue type. 
On success, the cache is cleared and the dashboard reruns, 
reflecting the updated score within 10 seconds.

---

## 3. The AI vs Deterministic Boundary

This is the most important architectural decision in 
the system. The boundary between deterministic code and 
LLM involvement is explicit and intentional.

Deterministic (audit_engine.py): all 14 checks, all 
severity classifications, all score calculations. These 
never involve an LLM. The audit result for a given store 
will always be identical regardless of when it is run.

AI-assisted (groq_advisor.py): executive summaries, 
per-issue advice, and fix content generation. These 
involve Llama 3.3 70B and may produce slightly different 
outputs on repeated calls. They are advisory and creative 
— not diagnostic.

This boundary exists because merchants need to trust the 
audit score. A score that changes every time the page 
loads — because an LLM decided the description was "good 
enough" this time — would be meaningless. The score is 
deterministic. The advice is generative.

---

## 4. Failure Handling

Each component handles failures gracefully rather than 
crashing the dashboard.

In shopify_client.py, all fetch functions return empty 
lists or dictionaries on API failure, with the error 
logged to the terminal. The dashboard will render with 
zero issues detected rather than throwing an exception. 
update_product() returns None on failure and the dashboard 
displays an explicit error message to the merchant.

In audit_engine.py, product fields that return None or 
empty strings are treated as missing. The 
product_completeness function uses .get() with defaults 
throughout, so malformed product data does not raise 
KeyError exceptions.

In groq_advisor.py, if the Groq API is unavailable or 
returns a rate limit error, the exception will surface 
to the Streamlit UI as a visible error. This is acceptable 
for a hackathon scope — a production version would 
implement retry logic with exponential backoff.

In app.py, if the token is invalid or missing, the 
dashboard halts with st.stop() and displays a clear 
credential error. The Apply Fix flow includes a product 
ID lookup that surfaces an explicit error if the product 
cannot be found rather than failing silently.

---

## 5. Known Limitations and Future Improvements

**Single-store architecture.** AuraScan uses a hardcoded 
Admin API token and audits one store at a time. 
Multi-merchant support would require OAuth 2.0 
implementation, a token storage layer, and per-merchant 
data isolation. The architecture supports this extension 
— only shopify_client.py would need to change.

**Auto-fix covers three issue types only.** The agentic 
Apply Fix writes descriptions, tags, and categories. 
Issues flagged for policies and pages cannot be auto-fixed 
because they require human-authored legal and editorial 
content. A warning is displayed for these issue types.

**SEO meta description check removed.** The Shopify Admin 
API does not expose metafields_global_description_tag on 
standard product endpoints without additional metafield 
queries. This check was scoped and removed to avoid false 
positives. It is identified as a future improvement 
requiring a separate metafield fetch pass.

**Groq rate limits.** The free tier of the Groq API allows 
approximately 30 requests per minute. For a store with 
many issues, rapid sequential advice requests could trigger 
rate limiting. A production version would implement request 
queuing.

**Session-scoped fix history.** The Fixed tab tracks 
applied fixes within the current browser session only. 
Fix history is not persisted to a database. Refreshing 
the browser clears the fixed issues log.

**What we would build with more time:**
1. Live OAuth flow for any merchant to connect their 
   store in one click
2. Auto-fix extended to policies and pages with 
   human-in-the-loop approval workflows
3. Groq retry logic with exponential backoff for 
   production reliability
4. Persistent fix history stored in a database rather 
   than session-scoped memory
5. Pagination for stores with more than 250 products
6. Competitor benchmarking via Kasparro data partnerships
7. Variant-level sales velocity tracking using 
   read_orders scope

---

## 6. Tech Stack Summary

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.11.9 |
| Dashboard | Streamlit | 1.51.0 |
| LLM Provider | Groq API | 0.36.0 |
| LLM Model | Llama 3.3 70B | — |
| Store API | Shopify Admin API | 2026-04 |
| HTTP Client | requests | 2.32.5 |
| Env Management | python-dotenv | 1.2.1 |

---

## 7. Security Notes

The Admin API token (shpat_) is stored in a .env file 
that is excluded from version control via .gitignore. 
It is never hardcoded in source files and never logged 
to the terminal or dashboard. The token is loaded once 
at module initialisation in shopify_client.py and 
referenced only through the shared HEADERS dictionary.

The Groq API key follows the same pattern — stored in 
.env, loaded via os.getenv(), never exposed in output.

Write operations via update_product() are scoped to 
product fields only (body_html, tags, product_type) and 
require explicit merchant confirmation before execution. 
No bulk operations are performed without per-item approval.
