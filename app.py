import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from shopify_client import get_access_token, fetch_products, fetch_pages, fetch_shop, fetch_policies, update_product
from audit_engine import run_audit
from groq_advisor import get_fix_advice, get_executive_summary, generate_fix_content

st.set_page_config(
    page_title="AuraScan",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 AuraScan")
st.caption("Track 5 — Kasparro Agentic Commerce Hackathon")

if "fixed_issues" not in st.session_state:
    st.session_state["fixed_issues"] = []

@st.cache_data(ttl=10)
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

def get_product_id_by_name(products, name):
    for p in products:
        if p['title'] == name:
            return p['id']
    return None

def render_issue(issue, key_prefix, products):
    with st.expander(f"[{issue['product']}] {issue['check']}"):
        st.write(f"**Basic Fix:** {issue['fix']}")

        advice_key = f"{key_prefix}_advice_{issue['check']}_{issue['product']}"
        fix_key = f"{key_prefix}_fix_{issue['check']}_{issue['product']}"
        applied_key = f"{key_prefix}_applied_{issue['check']}_{issue['product']}"

        if st.session_state.get(applied_key):
            st.success(f"✅ Fix already applied to {issue['product']}")
            return

        if st.button("Get AI Advice", key=f"{key_prefix}_btn_{issue['check']}_{issue['product']}"):
            with st.spinner("Getting AI advice..."):
                advice = get_fix_advice(issue)
                fix_content = generate_fix_content(issue)
            st.session_state[advice_key] = advice
            st.session_state[fix_key] = fix_content

        if st.session_state.get(advice_key):
            st.success(st.session_state[advice_key])

            if st.session_state.get(fix_key):
                st.markdown("**🤖 Suggested Fix:**")
                st.markdown(f"> {st.session_state[fix_key]}")

                if st.button(f"⚡ Apply Fix to Shopify", key=f"{key_prefix}_apply_{issue['check']}_{issue['product']}"):
                    product_id = get_product_id_by_name(products, issue['product'])
                    if not product_id:
                        st.error(f"Could not find product ID for {issue['product']}")
                        return

                    fix_content = st.session_state[fix_key]
                    update_data = {}

                    if "Missing Product Description" in issue['check']:
                        update_data["body_html"] = fix_content
                    elif "Missing Product Tags" in issue['check']:
                        update_data["tags"] = fix_content
                    elif "Missing Product Category" in issue['check']:
                        update_data["product_type"] = fix_content

                    if update_data:
                        with st.spinner(f"Applying fix to {issue['product']}..."):
                            result = update_product(product_id, update_data)
                        if result:
                            st.success(f"✅ Fix applied to {issue['product']} in Shopify!")
                            st.session_state[applied_key] = True
                            st.session_state["fixed_issues"].append({
                                "product": issue['product'],
                                "check": issue['check'],
                                "severity": issue['severity'],
                                "time": datetime.now().strftime("%I:%M %p")
                            })
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("Failed to apply fix. Check your API token permissions.")

tab1, tab2, tab3, tab4 = st.tabs(["🔴 Critical Issues", "🟠 High Issues", "🟡 Medium Issues", f"✅ Fixed ({len(st.session_state['fixed_issues'])})"])

with tab1:
    if results['critical']:
        for issue in results['critical']:
            render_issue(issue, "crit", products)
    else:
        st.success("No critical issues!")

with tab2:
    if results['high']:
        for issue in results['high']:
            render_issue(issue, "high", products)
    else:
        st.success("No high issues!")

with tab3:
    if results['medium']:
        for issue in results['medium']:
            render_issue(issue, "med", products)
    else:
        st.success("No medium issues!")

with tab4:
    if st.session_state["fixed_issues"]:
        for fixed in st.session_state["fixed_issues"]:
            st.success(f"✅ [{fixed['product']}] {fixed['check']} — Fixed at {fixed['time']}")
    else:
        st.info("No fixes applied yet in this session.")

st.divider()
st.caption(f"Store: {shop.get('name')} | Total Issues: {results['total_issues']} | Powered by Groq + Shopify Admin API")