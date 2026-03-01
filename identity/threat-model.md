# Identity Threat Model

## Threats Considered

### Credential Stuffing

Attacker uses leaked credentials across services.

Mitigation:

- Unique passwords
- Alias isolation

---

### SIM Swap Attack

Attacker transfers victim phone number.

Mitigation:

- Hardware key authentication
- Removal of SMS MFA

---

### Phishing

Attacker captures credentials via fake login page.

Mitigation:

- FIDO2 hardware keys
- Passkey authentication

---

### Email Account Takeover

Attacker gains access to primary email.

Mitigation:

- Hardware key protection
- Tier-0 root identity isolation

---

### Domain Takeover

Attacker gains control of domain registrar.

Mitigation:

- Root identity isolation
- Hardware key protection

---

## Residual Risk

Risk reduced to physical device compromise scenarios.