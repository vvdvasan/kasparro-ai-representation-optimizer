import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_fix_advice(issue):
    prompt = f"""You are an AI commerce expert helping a Shopify merchant improve how AI agents perceive their store.

Issue detected: {issue['check']}
Affected: {issue['product']}
Severity: {issue['severity']}
Basic fix: {issue['fix']}

Give a specific, actionable 2-3 sentence recommendation that explains:
1. Why this hurts their AI representation
2. Exactly what to write or add to fix it

Be direct and specific. No fluff."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

def generate_fix_content(issue):
    check = issue['check']
    product = issue['product']

    if "Missing Product Description" in check:
        prompt = f"""You are a Shopify product copywriter. Write a product description for '{product}'.
Write 2-3 sentences covering what it is, key features, and who it's for.
Return ONLY the description text. No labels, no quotes, no extra text."""

    elif "Missing Product Tags" in check:
        prompt = f"""You are a Shopify SEO expert. Generate 5-7 relevant tags for a product called '{product}'.
Return ONLY a comma-separated list of tags. No labels, no extra text.
Example format: tag1, tag2, tag3"""

    elif "Missing Product Category" in check:
        prompt = f"""You are a Shopify product expert. Suggest the most appropriate product_type category for '{product}'.
Return ONLY the category name, 1-3 words maximum. No labels, no extra text.
Example: Motorcycle Gear"""

    else:
        return None

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def get_executive_summary(results, shop_name):
    prompt = f"""You are an AI commerce expert. A Shopify store called '{shop_name}' just ran an AI readiness audit.

Results:
- AI Readiness Score: {results['score']}/100
- Critical Issues: {len(results['critical'])}
- High Issues: {len(results['high'])}
- Medium Issues: {len(results['medium'])}
- Products with empty descriptions: {results['product_stats']['empty_descriptions']} out of {results['product_stats']['total_products']}

Write a 3-sentence executive summary that:
1. States how ready this store is for AI agents
2. Identifies the biggest problem
3. States the most important first action

Be direct and specific."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content