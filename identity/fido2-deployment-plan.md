# FIDO2 Hardware Key Deployment Plan

## Objective

Deploy phishing-resistant hardware authentication using YubiKey 5C NFC.

---

## Hardware

Quantity: 2

Model: YubiKey 5C NFC

Configuration:

- Primary key (daily use)
- Backup key (offline storage)

---

## Target Accounts

Tier 0:

- Cloudflare
- Domain registrar

Tier 1:

- Microsoft
- Google
- Password manager

Tier 2:

- Financial accounts
- Brokerage accounts

---

## Deployment Sequence

For each account:

1. Add hardware key
2. Add backup hardware key
3. Test login
4. Save recovery codes
5. Remove SMS authentication

---

## Security Impact

Eliminates:

- Phishing login risk
- SIM swap takeover
- Credential-only compromise

---

## Status

Keys ordered.

Pending enrollment.