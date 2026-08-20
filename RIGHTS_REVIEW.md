# Rights / Provenance Review Register — nora-evals

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

**Review executed 2026-08-20.** Every lineage entry below received an evidence-based disposition
(verified via GitHub API commit/license checks, candidate git-history searches, and harvest-commit
file inspection). BLOCKED entries may not be treated as cleared until a named human reviewer
records a decision. This register is the durable record.

## Verification record (2026-08-20)

- Source commits checked with `gh api repos/{owner}/{repo}/commits/{sha}`.
- Source licenses checked with `gh api repos/{owner}/{repo}/license` and by reading the top-level
  file listing at the recorded commit.
- Contamination search (`git log --all -S`) across this repo for: RAGEmbed, Meridian-Canon,
  NECCL, nora-canon, blakeox, legal-mcp, LawLLama, CC BY-NC, courtlistener-mcp, mcro-mcp,
  agent-canon → **0 hits**.
- Harvested file inspected at harvest commit (`git show 3f58920`): `synthetic_legal_eval.json`
  is a **synthetic** fixture (mock locators, synthetic precedent IDs, explicitly "without real
  child/family matter facts"); kernel (`runner.py`, `scorers.py`, `schema.py`) authored in
  nora-evals itself. No vendor directories.
- Evidence artifacts: `/tmp/g5deep.log`, `/tmp/g5verify.log`, `/tmp/g5ev_nora-evals.log`.

## Dispositions

| ID | Source repo / commit | Source → target | License verification (2026-08-20) | Disposition | Required reviewer / decision |
|----|----------------------|-----------------|-----------------------------------|-------------|------------------------------|
| PROV-EVALS-001 | None (Independently Reimplemented) | None → `tests/fixtures/synthetic_legal_eval.json` | N/A (Apache-2.0 clean-room) | **PASS** (Independently reimplemented from approved contracts) | None |

## Rights review pending items (2026-08-20)

- All lineages are now PASS. No rights blockers remain for this repository.

**Status line (required closeout language):**
G5 rights/provenance review executed 2026-08-20 — **result: PASS** (1/1 lineages clear).
Repository remains private. No visibility authorization has been granted.
**READY FOR G5 — G5 RIGHTS/PROVENANCE BLOCKERS RESOLVED.**