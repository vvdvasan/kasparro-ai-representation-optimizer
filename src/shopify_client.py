import requests
import os
from dotenv import load_dotenv

load_dotenv()

STORE_URL = os.getenv("SHOPIFY_STORE_URL")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")

def get_access_token():
    url = f"https://{STORE_URL}/admin/oauth/access_token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Token failed: {response.status_code}")
        return None

def fetch_products(token):
    url = f"https://{STORE_URL}/admin/api/2026-04/products.json?limit=250"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["products"]
    return []

def fetch_pages(token):
    url = f"https://{STORE_URL}/admin/api/2026-04/pages.json"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["pages"]
    return []

def fetch_shop(token):
    url = f"https://{STORE_URL}/admin/api/2026-04/shop.json"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["shop"]
    return {}

def fetch_policies(token):
    url = f"https://{STORE_URL}/admin/api/2026-04/policies.json"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["policies"]
    return []

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from audit_engine import run_audit

    token = get_access_token()
    if token:
        products = fetch_products(token)
        pages = fetch_pages(token)
        shop = fetch_shop(token)
        policies = fetch_policies(token)

        results = run_audit(products, shop, policies, pages)

        print(f"\n🏪 STORE: {shop.get('name')}")
        print(f"🎯 AI READINESS SCORE: {results['score']}/100")
        print(f"📊 TOTAL ISSUES: {results['total_issues']}")
        print(f"🔴 CRITICAL: {len(results['critical'])}")
        print(f"🟠 HIGH: {len(results['high'])}")
        print(f"🟡 MEDIUM: {len(results['medium'])}")

        print("\n🔴 CRITICAL ISSUES:")
        for issue in results['critical']:
            print(f"  [{issue['product']}] {issue['check']}")
            print(f"  → Fix: {issue['fix']}\n")

        print("🟠 HIGH ISSUES:")
        for issue in results['high']:
            print(f"  [{issue['product']}] {issue['check']}")
            print(f"  → Fix: {issue['fix']}\n")

        print("🟡 MEDIUM ISSUES:")
        for issue in results['medium']:
            print(f"  [{issue['product']}] {issue['check']}")
            print(f"  → Fix: {issue['fix']}\n")