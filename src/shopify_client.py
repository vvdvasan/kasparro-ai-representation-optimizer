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
    token = get_access_token()
    if token:
        print("=== PRODUCTS ===")
        products = fetch_products(token)
        print(f"Found {len(products)} products")

        print("\n=== PAGES ===")
        pages = fetch_pages(token)
        for page in pages:
            print(f"- {page['title']}")

        print("\n=== SHOP ===")
        shop = fetch_shop(token)
        print(f"Name: {shop.get('name')}")
        print(f"Email: {shop.get('email')}")
        print(f"Description: {shop.get('description')}")

        print("\n=== POLICIES ===")
        policies = fetch_policies(token)
        for policy in policies:
            print(f"- {policy['title']}")