# Security policy

## Supported version

Security and reproducibility fixes are accepted for the latest tagged release.

## Reporting

Do not publish a vulnerability involving release integrity, CI permissions, or
dependency substitution before the maintainer has had a reasonable opportunity
to investigate. Use GitHub's private vulnerability reporting feature when it is
enabled; otherwise contact the repository owner through the private contact
method listed on the owner's GitHub profile.

## Scope

Relevant reports include:

- compromised or mutable dependency pins;
- workflow permission escalation;
- release archives that do not match their manifests;
- scripts executing untrusted repository content with elevated permissions;
- provenance claims that can be bypassed by path or metadata drift.

Mathematical errors should be reported through the public issue tracker unless
there is a separate reason for confidentiality.
