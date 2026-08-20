#!/usr/bin/env python3
"""nora-evals demo: fixture -> runner -> scorers -> machine-readable report.

Run:  python examples/demo.py
"""
from __future__ import annotations

import json
from pathlib import Path

from nora_evals.runner import EvalRunner
from nora_evals.schema import FixtureManifest

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "tests" / "fixtures" / "synthetic_sample_eval.json"
)


def main() -> None:
    print("nora-evals — benchmark harness demo")
    print("=" * 48)

    # 1. Load fixture.
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    manifest = FixtureManifest.from_dict(data)
    print(f"  \u2713 Runner initialized (fixture: {manifest.id})")
    print(f"  \u2713 Fixtures loaded ({manifest.target_project}, {len(manifest.cases)} cases)")

    # 2. Execute.
    runner = EvalRunner()
    bundle = runner.run_fixture(manifest)

    # 3. Report.
    for result in bundle.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  \u2713 {result.case_id}: {status} (score {result.score:.2f})")
    print(f"  \u2713 Scorers executed: {len(bundle.results)} cases, "
          f"{bundle.passed_cases} passed, overall {bundle.overall_score:.2f}")

    out_dir = Path("./output")
    out_dir.mkdir(exist_ok=True)
    report = out_dir / "eval_report_demo.json"
    report.write_text(
        json.dumps({
            "fixture_id": bundle.fixture_id,
            "target_project": bundle.target_project,
            "total_cases": bundle.total_cases,
            "passed_cases": bundle.passed_cases,
            "overall_score": bundle.overall_score,
        }, indent=2),
        encoding="utf-8",
    )
    print(f"  \u2713 Report generated ({report})")

    print("=" * 48)
    if bundle.passed_cases != bundle.total_cases:
        raise SystemExit("Demo failed: not all cases passed.")
    print("Demo PASS — benchmark harness executed cleanly.")


if __name__ == "__main__":
    main()