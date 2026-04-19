import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from shopify_client import get_access_token, fetch_products, fetch_pages, fetch_shop, fetch_policies
from audit_engine import run_audit
from groq_advisor import get_fix_advice, get_executive_summary

st.set_page_config(
    page_title="AI Representation Optimizer",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 AI Representation Optimizer")
st.caption("Track 5 — Kasparro Agentic Commerce Hackathon")

@st.cache_data(ttl=300)
def load_store_data():
    token = get_access_token()
    if not token:
        return None, None, None, None, None
    products = fetch_products(token)
    pages = fetch_pages(token)
    shop = fetch_shop(token)
    policies = fetch_policies(token)
    return products, pages, shop, policies, token

with st.spinner("Connecting to Shopify store..."):
    products, pages, shop, policies, token = load_store_data()

if not token:
    st.error("Failed to connect to Shopify store. Check your .env credentials.")
    st.stop()

results = run_audit(products, shop, policies, pages)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("AI Readiness Score", f"{results['score']}/100")
with col2:
    st.metric("🔴 Critical", len(results['critical']))
with col3:
    st.metric("🟠 High", len(results['high']))
with col4:
    st.metric("🟡 Medium", len(results['medium']))

st.divider()

with st.spinner("Generating executive summary..."):
    summary = get_executive_summary(results, shop.get('name'))
st.info(f"**AI Summary:** {summary}")

st.divider()

tab1, tab2, tab3 = st.tabs(["🔴 Critical Issues", "🟠 High Issues", "🟡 Medium Issues"])

with tab1:
    if results['critical']:
        for issue in results['critical']:
            with st.expander(f"[{issue['product']}] {issue['check']}"):
                st.write(f"**Basic Fix:** {issue['fix']}")
                if st.button(f"Get AI Advice", key=f"crit_{issue['check']}_{issue['product']}"):
                    with st.spinner("Getting AI advice..."):
                        advice = get_fix_advice(issue)
                    st.success(advice)
    else:
        st.success("No critical issues!")

with tab2:
    if results['high']:
        for issue in results['high']:
            with st.expander(f"[{issue['product']}] {issue['check']}"):
                st.write(f"**Basic Fix:** {issue['fix']}")
                if st.button(f"Get AI Advice", key=f"high_{issue['check']}_{issue['product']}"):
                    with st.spinner("Getting AI advice..."):
                        advice = get_fix_advice(issue)
                    st.success(advice)
    else:
        st.success("No high issues!")

with tab3:
    if results['medium']:
        for issue in results['medium']:
            with st.expander(f"[{issue['product']}] {issue['check']}"):
                st.write(f"**Basic Fix:** {issue['fix']}")
                if st.button(f"Get AI Advice", key=f"med_{issue['check']}_{issue['product']}"):
                    with st.spinner("Getting AI advice..."):
                        advice = get_fix_advice(issue)
                    st.success(advice)
    else:
        st.success("No medium issues!")

st.divider()
st.caption(f"Store: {shop.get('name')} | Total Issues: {results['total_issues']} | Powered by Groq + Shopify Admin API")