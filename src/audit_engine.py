def audit_products(products):
    issues = []
    total = len(products)
    empty_desc = 0
    empty_category = 0
    empty_tags = 0
    empty_vendor = 0

    for product in products:
        name = product.get("title", "Unknown")

        if not product.get("body_html"):
            empty_desc += 1
            issues.append({
                "check": "Missing Product Description",
                "product": name,
                "severity": "CRITICAL",
                "fix": f"Add a detailed description for '{name}' with specifications, use case, and key features."
            })

        if not product.get("product_type"):
            empty_category += 1
            issues.append({
                "check": "Missing Product Category",
                "product": name,
                "severity": "HIGH",
                "fix": f"Set a product category for '{name}' so AI agents can classify it correctly."
            })

        if not product.get("tags"):
            empty_tags += 1
            issues.append({
                "check": "Missing Product Tags",
                "product": name,
                "severity": "MEDIUM",
                "fix": f"Add relevant tags to '{name}' to improve AI discoverability."
            })

        if not product.get("vendor"):
            empty_vendor += 1
            issues.append({
                "check": "Missing Vendor",
                "product": name,
                "severity": "MEDIUM",
                "fix": f"Add vendor information for '{name}'."
            })

    return issues, {
        "total_products": total,
        "empty_descriptions": empty_desc,
        "empty_categories": empty_category,
        "empty_tags": empty_tags,
        "empty_vendors": empty_vendor
    }


def audit_store(shop):
    issues = []

    if not shop.get("name"):
        issues.append({
            "check": "Missing Store Name",
            "product": "Store",
            "severity": "CRITICAL",
            "fix": "Add your store name."
        })

    return issues


def audit_policies(policies):
    issues = []
    found = [p["title"].lower() for p in policies]

    required = ["refund policy", "privacy policy", "shipping policy", "terms of service"]
    for policy in required:
        if policy not in found:
            issues.append({
                "check": f"Missing Policy: {policy.title()}",
                "product": "Policies",
                "severity": "HIGH",
                "fix": f"Add a '{policy.title()}' page. AI agents use policies to build trust with buyers."
            })

    return issues


def audit_pages(pages):
    issues = []
    found = [p["title"].lower() for p in pages]

    if "about us" not in found and "about" not in found:
        issues.append({
            "check": "Missing About Us Page",
            "product": "Pages",
            "severity": "HIGH",
            "fix": "Add an 'About Us' page. AI agents use this to understand store identity."
        })

    if "faq" not in found and "frequently asked questions" not in found:
        issues.append({
            "check": "Missing FAQ Page",
            "product": "Pages",
            "severity": "HIGH",
            "fix": "Add a FAQ page. AI agents pull from FAQs to answer buyer questions."
        })

    return issues


def run_audit(products, shop, policies, pages):
    all_issues = []
    product_issues, product_stats = audit_products(products)
    all_issues.extend(product_issues)
    all_issues.extend(audit_store(shop))
    all_issues.extend(audit_policies(policies))
    all_issues.extend(audit_pages(pages))

    critical = [i for i in all_issues if i["severity"] == "CRITICAL"]
    high = [i for i in all_issues if i["severity"] == "HIGH"]
    medium = [i for i in all_issues if i["severity"] == "MEDIUM"]

    total_products = product_stats["total_products"]

    # Product completeness score (0-60 points) — weighted partial credit
    def product_completeness(p):
        score = 0
        if p.get("body_html"): score += 4      # most important
        if p.get("product_type"): score += 3   # second
        if p.get("tags"): score += 2           # third
        if p.get("vendor"): score += 1         # least
        return score

    max_per_product = 10  # 4+3+2+1
    total_possible = total_products * max_per_product
    earned = sum(product_completeness(p) for p in products)
    product_score = round((earned / total_possible) * 60) if total_possible else 0

    # Store info score (0-15 points)
    store_score = 15

    # Policies score (0-15 points)
    found_policies = [p["title"].lower() for p in policies]
    required = ["refund policy", "privacy policy", "shipping policy", "terms of service"]
    policy_score = round((sum(1 for p in required if p in found_policies) / len(required)) * 15)

    # Pages score (0-10 points)
    found_pages = [p["title"].lower() for p in pages]
    has_about = "about us" in found_pages or "about" in found_pages
    has_faq = "faq" in found_pages or "frequently asked questions" in found_pages
    page_score = (5 if has_about else 0) + (5 if has_faq else 0)

    score = product_score + store_score + policy_score + page_score
    score = max(0, min(100, score))

    return {
        "score": score,
        "total_issues": len(all_issues),
        "critical": critical,
        "high": high,
        "medium": medium,
        "product_stats": product_stats
    }