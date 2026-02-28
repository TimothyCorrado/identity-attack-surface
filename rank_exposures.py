import os
import re
import pandas as pd

INPUT = os.path.join("output", "exposures.csv")
OUT_RANKED = os.path.join("output", "accounts_ranked.csv")
OUT_ALIASES = os.path.join("output", "aliases_suggested.csv")

EMAIL_RE = re.compile(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})", re.I)

# Keywords -> category + score weight
RULES = [
    ("finance", 50, ["paypal", "bank", "card", "billing", "invoice", "payment", "stripe"]),
    ("auth",    45, ["password reset", "security alert", "verify", "verification", "signin", "sign in", "2-step", "2fa", "mfa", "login", "suspicious"]),
    ("cloud",   35, ["azure", "aws", "gcp", "google cloud", "okta", "entra", "microsoft"]),
    ("career",  15, ["recruit", "careers", "job", "application", "interview", "hiring"]),
    ("social",  10, ["linkedin", "facebook", "instagram", "x.com", "twitter"]),
    ("promo",    5, ["welcome", "promotion", "promotions", "unsubscribe", "sale", "deal"]),
]

def extract_email(s: str) -> str | None:
    if not isinstance(s, str):
        return None
    m = EMAIL_RE.search(s)
    return m.group(1).lower() if m else None

def registrable_domain(domain: str) -> str:
    """
    Heuristic 'registrable' domain (good enough without extra deps).
    Handles common 2-level TLDs like .co.uk, .com.au, etc.
    """
    parts = domain.split(".")
    if len(parts) <= 2:
        return domain
    two_level = {"co", "com", "net", "org", "gov", "edu"}
    if parts[-2] in two_level and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])

def slug_from_domain(dom: str) -> str:
    base = registrable_domain(dom)
    left = base.split(".")[0]
    left = re.sub(r"[^a-z0-9]+", "", left.lower())
    return left[:24] if left else "alias"

def score_row(subject: str, sender: str) -> tuple[int, str]:
    text = f"{subject or ''} {sender or ''}".lower()
    score = 0
    cats = []
    for cat, pts, keys in RULES:
        if any(k in text for k in keys):
            score += pts
            cats.append(cat)
    # small bump if it's from a noreply (often account-related)
    if "no-reply" in text or "noreply" in text:
        score += 5
    return score, ",".join(sorted(set(cats)))

def main():
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Missing {INPUT}")

    df = pd.read_csv(INPUT)
    # Expect columns like: subject,sender
    if "sender" not in df.columns or "subject" not in df.columns:
        raise ValueError(f"Expected columns subject,sender. Found: {list(df.columns)}")

    df["email"] = df["sender"].apply(extract_email)
    df = df[df["email"].notna()].copy()

    df["domain_full"] = df["email"].str.split("@", n=1).str[1]
    df["domain"] = df["domain_full"].apply(registrable_domain)

    scores = df.apply(lambda r: score_row(str(r["subject"]), str(r["sender"])), axis=1)
    df["risk_score"] = [s[0] for s in scores]
    df["categories"] = [s[1] for s in scores]

    grouped = (
        df.groupby("domain", as_index=False)
          .agg(
              count=("domain", "size"),
              max_risk=("risk_score", "max"),
              categories=("categories", lambda x: ",".join(
                sorted({c for c in ",".join([str(v) for v in x]).split(",") if c})
                )),
              example_sender=("sender", "first"),
              example_subject=("subject", "first"),
          )
    )

    grouped = grouped.sort_values(["max_risk", "count"], ascending=[False, False]).reset_index(drop=True)

    # Suggested aliases (you’ll replace @yourdomain.com later)
    grouped["suggested_alias_localpart"] = grouped["domain"].apply(slug_from_domain)
    grouped["suggested_alias_example"] = grouped["suggested_alias_localpart"] + "@YOURDOMAIN.com"

    os.makedirs("output", exist_ok=True)
    grouped.to_csv(OUT_RANKED, index=False)

    aliases = grouped[["domain", "suggested_alias_example", "max_risk", "count", "categories"]].copy()
    aliases.to_csv(OUT_ALIASES, index=False)

    print(f"Wrote: {OUT_RANKED}")
    print(f"Wrote: {OUT_ALIASES}")
    print(f"Top 10 domains:\n{grouped.head(10)[['domain','max_risk','count','categories']].to_string(index=False)}")

if __name__ == "__main__":
    main()