import json
from pathlib import Path
from nora_evals.schema import FixtureManifest
from nora_evals.runner import EvalRunner
from nora_evals.report import generate_markdown_report

CROSS_PROJECT_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "cross_project_baseline.json"

def test_cross_project_baseline_report():
    assert CROSS_PROJECT_FIXTURE.exists()
    data = json.loads(CROSS_PROJECT_FIXTURE.read_text(encoding="utf-8"))
    manifest = FixtureManifest.from_dict(data)
    
    runner = EvalRunner()
    bundle = runner.run_fixture(manifest)
    
    assert bundle.total_cases == 4
    assert bundle.passed_cases == 4
    
    report_md = generate_markdown_report(bundle)
    assert "# Evaluation Baseline Report" in report_md
    assert "cross-project-baseline-v1" in report_md
    assert "100.0%" in report_md
