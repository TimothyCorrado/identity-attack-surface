import os
import re
import pandas as pd

INFILE = os.path.join("output", "accounts_ranked.csv")
OUTFILE = os.path.join("output", "domain_aliases.csv")

DEST_DOMAIN = "corradosec.com"

# Preference order for primary category (drives prefix)
CATEGORY_PRIORITY = ["finance", "auth", "cloud", "career", "social", "promo"]

def clean_localpart(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s[:40] if s else "alias"

def pick_primary_category(categories: str) -> str:
    cats = {c.strip().lower() for c in str(categories).split(",") if c.strip()}
    for c in CATEGORY_PRIORITY:
        if c in cats:
            return c
    return "misc"

def base_from_domain(domain: str) -> str:
    # Use the registrable-ish base (e.g., accountonline.com -> accountonline)
    d = (domain or "").lower().strip()
    if d.startswith("www."):
        d = d[4:]
    base = d.split(".")[0] if "." in d else d
    return clean_localpart(base)

def make_alias(primary: str, base: str) -> str:
    # Example: finance-usbank@corradosec.com
    return f"{primary}-{base}@{DEST_DOMAIN}"

def main():
    if not os.path.exists(INFILE):
        raise FileNotFoundError(f"Missing {INFILE}. Run rank_exposures.py first.")

    df = pd.read_csv(INFILE, na_filter=False)

    required = {"domain", "max_risk", "categories"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}. Found: {list(df.columns)}")

    used = set()
    aliases = []

    for _, row in df.iterrows():
        domain = str(row["domain"]).strip().lower()
        categories = str(row["categories"])
        max_risk = int(row["max_risk"]) if str(row["max_risk"]).isdigit() else row["max_risk"]

        primary = pick_primary_category(categories)
        base = base_from_domain(domain)

        local_alias = make_alias(primary, base)

        # De-conflict if duplicates occur
        if local_alias in used:
            i = 2
            while True:
                candidate = f"{primary}-{base}-{i}@{DEST_DOMAIN}"
                if candidate not in used:
                    local_alias = candidate
                    break
                i += 1

        used.add(local_alias)
        bank_safe = f"{base}@{DEST_DOMAIN}"

        aliases.append({
            "domain": domain,
            "max_risk": max_risk,
            "categories": categories,
            "primary_category": primary,
            "recommended_alias": local_alias,
            "bank_safe_alias": bank_safe
        })

    out = pd.DataFrame(aliases)
    os.makedirs("output", exist_ok=True)
    out.to_csv(OUTFILE, index=False)

    print(f"Wrote: {OUTFILE}")
    print(out.head(15).to_string(index=False))

if __name__ == "__main__":
    main()