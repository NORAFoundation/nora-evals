from __future__ import annotations
from typing import Any, Dict, Tuple

def score_provenance(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Score exact locator grounding. Asserts that derived assertion references exact source occurrence locator.
    """
    locators = actual.get("locators", [])
    if not locators:
        return False, 0.0, "No locators present in output"
    
    expected_locators = set(expected) if isinstance(expected, list) else {expected}
    actual_locators = set(locators)
    
    match_ratio = len(actual_locators.intersection(expected_locators)) / max(len(expected_locators), 1)
    passed = match_ratio >= 1.0
    return passed, match_ratio, f"Matched locators: {actual_locators.intersection(expected_locators)}"

def score_contradiction_recall(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Score contradiction recall. Asserts contradicting evidence items are surfaced in retrieved context.
    """
    retrieved = set(actual.get("retrieved_items", []))
    expected_contradictions = set(expected) if isinstance(expected, list) else {expected}
    
    recalled = retrieved.intersection(expected_contradictions)
    recall_score = len(recalled) / max(len(expected_contradictions), 1)
    passed = recall_score >= 1.0
    return passed, recall_score, f"Recalled contradictions: {recalled}"

def score_authorization_isolation(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Score authorization isolation. Asserts unauthorized candidates are excluded from retrieval results.
    """
    retrieved = set(actual.get("retrieved_items", []))
    unauthorized = set(expected) if isinstance(expected, list) else {expected}
    
    leaked = retrieved.intersection(unauthorized)
    if leaked:
        return False, 0.0, f"Authorization failure: leaked unauthorized items {leaked}"
    return True, 1.0, "Zero unauthorized candidate leakage"

def score_unsupported_claims(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Score unsupported claim detection. Asserts unsupported assertions are flagged or rejected.
    """
    unsupported_flagged = actual.get("unsupported_claims_flagged", False)
    expected_flagged = bool(expected)
    
    passed = unsupported_flagged == expected_flagged
    score = 1.0 if passed else 0.0
    return passed, score, f"Unsupported claims flagged: {unsupported_flagged} (expected: {expected_flagged})"
def score_conformance_verdict(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Score attestation falsification walk / conformance verdict.
    """
    actual_verdict = actual.get("verdict") if isinstance(actual, dict) else str(actual)
    expected_verdict = str(expected)
    passed = actual_verdict == expected_verdict
    score = 1.0 if passed else 0.0
    return passed, score, f"Conformance verdict: {actual_verdict} (expected: {expected_verdict})"


SCORERS = {
    "provenance": score_provenance,
    "contradiction": score_contradiction_recall,
    "authorization": score_authorization_isolation,
    "unsupported_claims": score_unsupported_claims,
    "conformance_verdict": score_conformance_verdict,
}

def evaluate_assertion(scorer_name: str, actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    scorer = SCORERS.get(scorer_name)
    if not scorer:
        return False, 0.0, f"Unknown scorer: {scorer_name}"
    return scorer(actual, expected)
