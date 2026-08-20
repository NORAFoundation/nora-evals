# Evaluation Baseline Report — cross-project-baseline-v1

- **Target Suite:** `nora-foundation-suite`
- **Overall Reliability Score:** `100.0%`
- **Cases Passed:** `4/4`

## Test Case Details

| Case ID | Status | Score | Scorers & Assertion Findings |
|---------|--------|-------|------------------------------|
| `EVID-PROV-01` | **PASS** | `1.0` | provenance: Matched locators: {'order://us/wi/ramsey/501#L1-L10'} |
| `RETR-CONTRA-01` | **PASS** | `1.0` | contradiction: Recalled contradictions: {'EVIDENCE-DOC-2-CONTRADICTION'} |
| `AUTH-ISOLATE-01` | **PASS** | `1.0` | authorization: Zero unauthorized candidate leakage |
| `REASON-UNSUP-01` | **PASS** | `1.0` | unsupported_claims: Unsupported claims flagged: True (expected: True) |

## Epistemological Assurance Statement
All assertions assert zero authorization leakage, strict exact-locator grounding, and contradiction recall over synthetic corpora.
