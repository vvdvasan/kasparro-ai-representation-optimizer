import requests
import os
from dotenv import load_dotenv

load_dotenv()

STORE_URL = os.getenv("SHOPIFY_STORE_URL")
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

BASE = f"https://{STORE_URL}/admin/api/2026-04"

def get_access_token():
    return ACCESS_TOKEN

def fetch_products(token=None):
    response = requests.get(f"{BASE}/products.json?limit=250", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["products"]
    print(f"❌ fetch_products failed: {response.status_code}")
    return []

def fetch_pages(token=None):
    response = requests.get(f"{BASE}/pages.json", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["pages"]
    print(f"❌ fetch_pages failed: {response.status_code}")
    return []

def fetch_shop(token=None):
    response = requests.get(f"{BASE}/shop.json", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["shop"]
    print(f"❌ fetch_shop failed: {response.status_code}")
    return {}

def fetch_policies(token=None):
    response = requests.get(f"{BASE}/policies.json", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["policies"]
    print(f"❌ fetch_policies failed: {response.status_code}")
    return []

def update_product(product_id, data):
    response = requests.put(
        f"{BASE}/products/{product_id}.json",
        headers=HEADERS,
        json={"product": data}
    )
    if response.status_code == 200:
        return response.json()["product"]
    print(f"❌ update_product failed: {response.status_code} {response.text[:200]}")
    return None

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from audit_engine import run_audit

    products = fetch_products()
    pages = fetch_pages()
    shop = fetch_shop()
    policies = fetch_policies()

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