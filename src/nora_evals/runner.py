from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from nora_evals.schema import FixtureManifest, EvalResult, ResultBundle
from nora_evals.scorers import evaluate_assertion

class EvalRunner:
    """
    Executes benchmark fixtures against candidate adapters or synthetic targets.
    """
    def __init__(self, system_adapter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        self.system_adapter = system_adapter or self._default_mock_adapter

    @staticmethod
    def _default_mock_adapter(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default adapter for self-contained synthetic fixture testing.
        Passes back mock context assertions.
        """
        context = input_data.get("context", {})
        return {
            "locators": context.get("mock_locators", []),
            "retrieved_items": context.get("mock_retrieved_items", []),
            "unsupported_claims_flagged": context.get("mock_unsupported_flagged", False)
        }

    def run_fixture(self, manifest: FixtureManifest) -> ResultBundle:
        results = []
        total_score = 0.0
        passed_count = 0

        for case in manifest.cases:
            actual_output = self.system_adapter({"prompt": case.prompt, "context": case.context})
            
            case_passed = True
            case_scores = []
            case_details = {}

            for assertion in case.assertions:
                p, s, msg = evaluate_assertion(assertion.scorer, actual_output, assertion.expected)
                case_scores.append(s * assertion.weight)
                case_details[assertion.scorer] = {"passed": p, "score": s, "message": msg}
                if not p:
                    case_passed = False

            avg_score = sum(case_scores) / max(len(case_scores), 1) if case_scores else 1.0
            if case_passed:
                passed_count += 1
            total_score += avg_score

            results.append(EvalResult(
                case_id=case.id,
                passed=case_passed,
                score=avg_score,
                details=case_details
            ))

        overall_score = total_score / max(len(manifest.cases), 1)

        return ResultBundle(
            fixture_id=manifest.id,
            target_project=manifest.target_project,
            timestamp=time.time(),
            total_cases=len(manifest.cases),
            passed_cases=passed_count,
            overall_score=overall_score,
            results=results
        )
