# Alias Architecture

## Objective

Prevent identity correlation and reduce breach blast radius using domain-based alias isolation.

Each service receives a unique email identity.

---

## Tier Model

| Tier | Alias Pattern | Purpose |
|---|---|---|
| Tier 0 | root@corradosec.com | Domain / infrastructure |
| Tier 1 | auth-service@corradosec.com | Identity providers |
| Tier 2 | service@corradosec.com | Financial accounts |
| Tier 3 | auth-platform@corradosec.com | SaaS / social |
| Tier 4 | random@corradosec.com | Low trust services |

---

## Security Benefits

Prevents:

- Cross-service correlation
- Credential stuffing amplification
- Targeted phishing precision

Enables:

- Breach attribution
- Attack surface monitoring
- Identity isolation

---

## Example

Compromise of:

finance-robinhood@corradosec.com

Does NOT expose:

auth-microsoft@corradosec.com

Isolation preserved.

---

## Implementation

Cloudflare catch-all routing deployed.

Aliases generated and assigned per service.