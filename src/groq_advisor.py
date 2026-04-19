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