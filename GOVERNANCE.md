# Governance

Lluis Eriksson is the current maintainer and final decision maker for theorem
scope, public API, releases, and scholarly claims.

Changes to a public theorem, dependency pin, license, claims boundary, or
release identity require explicit maintainer review. Routine documentation and
tooling fixes may be merged after all required checks pass.

The project follows a conservative release policy:

- theorem aliases remain stable within a major version;
- dependency updates are isolated and reviewed;
- release tags are created only after clean CI;
- archived versions are never rewritten;
- corrections that affect a mathematical statement receive a new version and a
  prominent changelog entry.
