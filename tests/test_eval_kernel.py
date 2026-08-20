import json
from pathlib import Path
import pytest
from nora_evals.schema import FixtureManifest
from nora_evals.runner import EvalRunner
from nora_evals.scorers import (
    score_provenance,
    score_contradiction_recall,
    score_authorization_isolation,
    score_unsupported_claims
)

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "synthetic_sample_eval.json"

def test_scorers():
    # Provenance
    p, s, msg = score_provenance({"locators": ["loc-1"]}, "loc-1")
    assert p is True and s == 1.0

    # Contradiction
    p, s, msg = score_contradiction_recall({"retrieved_items": ["item-1", "contra-1"]}, "contra-1")
    assert p is True and s == 1.0

    # Authorization
    p, s, msg = score_authorization_isolation({"retrieved_items": ["allowed-1"]}, ["secret-1"])
    assert p is True and s == 1.0

    # Unsupported claim
    p, s, msg = score_unsupported_claims({"unsupported_claims_flagged": True}, True)
    assert p is True and s == 1.0

def test_eval_runner_end_to_end():
    assert FIXTURE_PATH.exists()
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    manifest = FixtureManifest.from_dict(data)
    
    runner = EvalRunner()
    bundle = runner.run_fixture(manifest)
    
    assert bundle.total_cases == 4
    assert bundle.passed_cases == 4
    assert bundle.overall_score == 1.0
    assert bundle.fixture_id == "synthetic-baseline-001"
