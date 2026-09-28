# Research OS Repository Governance

## G-001 — Human-authored repository history

**Status:** binding cross-lab invariant  
**Scope:** EPISTEME and every Research OS lab/repository unless the human owner explicitly revokes this rule.

GitHub Actions may be used as a compute, test, CI, validation, benchmark, packaging, and artifact runner. It must not become a repository author or contributor.

Accordingly:

1. Workflows must use the minimum permissions required and should default to `contents: read`.
2. `github-actions[bot]` must not create commits, push commits or tags, merge pull requests, or otherwise write Git history.
3. Scientific receipts produced by Actions remain workflow artifacts unless a human-authored repository update later incorporates them.
4. A workflow must not use a bot-authored writeback merely to trigger the next scientific stage. Stage activation is performed by a human-authored commit or another explicitly human-controlled path.
5. New and modified workflows must be checked for repository-write permissions and bot commit/push steps before activation.
6. If an existing lab contains a bot-authored write path, retire that path prospectively rather than rewriting historical Git provenance unless the owner separately requests history surgery.

This rule concerns repository provenance, not computation: GitHub-hosted runners remain permitted and encouraged when they improve reproducibility.
