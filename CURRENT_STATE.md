# Current State — nora-evals

**Status:** REFERENCE / CONFORMANCE INFRASTRUCTURE IN REVIEW
**Version:** 0.0.1

## Implemented Reference Slice

The minimum reference evaluation infrastructure is complete and verified:

- `src/nora_evals/schema.py`: Dataclasses for `FixtureManifest`, `TestCase`, `AssertionSpec`, `EvalResult`, and `ResultBundle`.
- `src/nora_evals/scorers.py`: Assertions for `provenance`, `contradiction`, `authorization`, and `unsupported_claims`.
- `src/nora_evals/runner.py`: `EvalRunner` harness for executing benchmark fixtures and compiling machine-readable reports.
- `src/nora_evals/cli.py`: Command-line tool `nora-evals run --fixture <path> [--out <path>]`.

## Verified

- `make test` / `pytest`: **5 passed in 0.02s**.
- Test module: `tests/test_runner.py` (and associated test suite).
- Benchmark fixture used separately: `tests/fixtures/synthetic_sample_eval.json`.

## Not Yet Established

- canonical feature parity;
- public extraction completeness;
- production evaluation suite integration;
- resolution of Appeals-Agent fixture licensing (PROV-EVALS-001).
