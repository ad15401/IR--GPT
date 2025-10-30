# MFA Fatigue / Account Takeover (IR Playbook)

**Trigger:** Multiple unexpected MFA prompts; user approves one; new VPN login from unusual IP.

**Containment (reversible first):**
1) Out-of-band verify with user (phone call).
2) Revoke active sessions / tokens for the account.
3) Force password reset; rotate recovery factors.
4) Enforce phishing-resistant MFA (number matching / FIDO2).
5) Temporary IP block while confirming scope.

**Analysis Checklist (Detection & Analysis):**
- Review auth logs (time, IP, device, geo, user agent).
- Check OAuth consent grants; revoke suspicious tokens.
- Hunt for the IP across 24–72h in SIEM.
- Look for mailbox rules / inbox forwarding.

**Eradication & Recovery:**
- Reset long-lived tokens, app passwords.
- Remove malicious rules; re-enroll MFA.
- Monitor for re-auth attempts.

**Documentation:**
- Record timestamps, actions, approvals, and evidence.
- Map steps to NIST SP 800-61 phases.

**References:** NIST SP 800-61; NIST CSF (Detect, Respond, Recover).
