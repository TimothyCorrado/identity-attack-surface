# Identity Security Architecture

## Overview

This directory documents the identity hardening component of the CorradoSec Cloud Identity Attack Surface Scanner project.

The objective is to reduce account takeover risk through:

- Domain-based alias compartmentalization
- Hardware-backed authentication (FIDO2)
- Offline recovery readiness
- Elimination of SMS-based MFA

This implements Zero Trust identity principles at the individual level.

---

## Architecture Summary

Security stack:

Alias Isolation → Password Manager → Hardware Security Key (FIDO2) → Account Access

Each layer reduces attack surface and prevents credential reuse attacks.

---

## Current Status

| Control | Status |
|---|---|
| Custom domain alias routing | Complete |
| Catch-all email isolation | Complete |
| Tier-0 root identity isolation | Complete |
| Password entropy hardening | Complete |
| Offline recovery storage | Complete |
| Hardware key deployment | Pending |

---

## Directory Contents

| File | Purpose |
|---|---|
| alias-architecture.md | Alias compartment model |
| threat-model.md | Threat analysis |
| fido2-deployment-plan.md | Hardware key rollout |
| recovery-model.md | Disaster recovery design |

---

## Security Objective

Prevent unauthorized access even if:

- Password is leaked
- Phone number is compromised
- Email address is exposed

---

## Next Phase

Hardware security key enrollment and passkey deployment.