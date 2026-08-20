# Rights / Provenance Review Register — nora-evals

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

Formal external rights/provenance review is outstanding for every entry below.
This register is the durable record of each unresolved item. It is **not** a
resolution of any legal/rights question; no item below may be treated as cleared
until a named reviewer records a decision.

| ID | Source repo / commit / lineage | Source path(s) | Why review required | License / rights question | Evidence already collected | Required reviewer / decision | Remediation if rejected | Publication impact |
|----|-------------------------------|----------------|---------------------|---------------------------|---------------------------|------------------------------|-------------------------|--------------------|
| PROV-EVALS-001 | `NORAFoundation/Appeals-Agent` @ `e150a953` (Apache-2.0) | `eval/wargame_spec.md` → `tests/fixtures/synthetic_legal_eval.json` | Fixture generalized from domain-specific spec; no `rights_basis` / `relicensing_status` / `authorization_reference` recorded (unlike other targets). | Is the generalization sufficiently derivative-free of the original spec's domain content? Is the source's Apache-2.0 notice preserved for the fixture? | SOURCE_PROVENANCE.yaml entry; secret/privacy/license scan pass (agent-level); **note: no governance commit recording "pending formal rights review" exists in this repo** (evidence file flags HEAD lacks the governance commit present in other targets). | Named human reviewer; add the missing governance/rights-record commit after review. | Remove/replace fixture content; add governance commit; re-run gates. | Blocks publication of nora-evals (hard blocker per G5). |

**Rights review pending items (inherited from evidence file):**
- `nora-evals` is the only target whose HEAD **lacks** the "pending formal rights review"
  governance commit; formal rights review pending and unrecorded for this repo.

**Status line (required closeout language):**
Technical publication preparation complete. Formal rights/provenance review remains
outstanding. Repository remains private. No visibility authorization has been granted.