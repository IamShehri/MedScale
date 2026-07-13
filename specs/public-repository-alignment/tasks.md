# Public Repository Alignment — Tasks

| ID | Task | Owner | Deps | Status | Evidence |
|---|---|---|---|---|---|
| ALIGN-01 | Capture divergence audit output and classify all uncommitted files by risk and phase | owner | — | done | git status, diff, branch, log |
| ALIGN-02 | Enumerate public/experimental/internal exports for all M17–M18 subpackages | owner | ALIGN-01 | done | __init__.py + contracts.py scans |
| ALIGN-03 | Document README status and roadmap drift relative to current code | owner | ALIGN-01 | done | README.md / ROADMAP.md |
| ALIGN-04 | Document version metadata mismatches: __about__, CITATION, CHANGELOG, RELEASES, pyproject classifiers | owner | ALIGN-01 | done | version scan |
| ALIGN-05 | Document doc/ADR index gaps and proposed ADR numbering hygiene | owner | ALIGN-03 | done | docs/adr listing + docs/README.md |
| ALIGN-06 | Propose public API stability classification with rationale | owner | ALIGN-02 | done | classification matrix |
| ALIGN-07 | Draft public repository alignment PR sequence from dependency evidence | owner | ALIGN-04, ALIGN-06 | done | plan + final report |
| ALIGN-08 | Run ruff / mypy / pytest / build and capture exact counts | owner | — | done | terminal verification |
| ALIGN-09 | Install built wheel in clean env and run `medscale --version` + core smoke command | owner | ALIGN-08 | pending | smoke output |
| ALIGN-10 | Prepare final GO/NO-GO recommendation for publishing | owner | ALIGN-09 | pending | final report |
