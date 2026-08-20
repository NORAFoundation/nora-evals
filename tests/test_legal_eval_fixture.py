import json
from pathlib import Path
from nora_evals.schema import FixtureManifest
from nora_evals.runner import EvalRunner

LEGAL_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "synthetic_legal_eval.json"

def test_synthetic_legal_eval_fixture():
    assert LEGAL_FIXTURE_PATH.exists()
    data = json.loads(LEGAL_FIXTURE_PATH.read_text(encoding="utf-8"))
    manifest = FixtureManifest.from_dict(data)
    
    runner = EvalRunner()
    bundle = runner.run_fixture(manifest)
    
    assert bundle.total_cases == 2
    assert bundle.passed_cases == 2
    assert bundle.overall_score == 1.0
