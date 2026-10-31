# CODEOWNERS pattern (Aomi org)

GitHub reads **CODEOWNERS only from each application repository** (or from a `.github` default for new repos). This org repo does **not** replace per-repo ownership files.

## Recommended layout

1. Copy [`CODEOWNERS.template`](../CODEOWNERS.template) to `.github/CODEOWNERS` (or repo-root `CODEOWNERS`) when bootstrapping a repo.
2. Replace the catch-all `@aomihq` line with path-specific teams or people as the repo grows.
3. Keep production-control paths owned by the human prod delegate documented in your runbook. The org is on **GitHub Team** today; **rulesets** are planned. Until rulesets land, CODEOWNERS is advisory for review routing (poteto enforces merge gates in CI).

## Example (per repo)

```gitattributes
# Default owner for review routing
* @aomihq

# Tighter paths (illustrative)
/deploy/prod/ @tiennguyentt
/.github/workflows/prod-*.yml @tiennguyentt
```

## References

- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
