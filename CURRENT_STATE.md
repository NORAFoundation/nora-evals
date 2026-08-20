# Current State — nora-evals

**Status:** IMPLEMENTED (Minimum Vertical Slice Verified)  
**Version:** 0.0.1  

## Implemented Components

- `src/nora_evals/schema.py`: Dataclasses for `FixtureManifest`, `TestCase`, `AssertionSpec`, `EvalResult`, and `ResultBundle`.
- `src/nora_evals/scorers.py`: Assertions for `provenance`, `contradiction`, `authorization`, and `unsupported_claims`.
- `src/nora_evals/runner.py`: `EvalRunner` harness for executing benchmark fixtures and compiling machine-readable reports.
- `src/nora_evals/cli.py`: Command-line tool `nora-evals run --fixture <path> [--out <path>]`.

## Verification Evidence

- End-to-end synthetic benchmark executed via `tests/fixtures/synthetic_sample_eval.json`.
- `make test` / `pytest`: **3 passed in 0.02s**.
