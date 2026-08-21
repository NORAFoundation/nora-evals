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


def score_aml_rubric(actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    """
    Evaluates memory system answers against the AML (Agent Memory Leaderboard) rubric.
    Performs online API judging if credentials are set, else falls back to local rules.
    """
    import os
    import json
    import urllib.request
    import urllib.error

    predicted = str(actual.get("model_output", actual.get("answer", ""))).strip()
    
    # Normalize rubrics input
    rubrics = []
    if isinstance(expected, list):
        rubrics = [str(r) for r in expected]
    elif isinstance(expected, dict):
        rubrics = [str(r) for r in expected.get("rubrics", [])]
    else:
        rubrics = [str(expected)]

    if not predicted:
        return False, 0.0, "AML Rubric Fail: Output is empty"
    if not rubrics:
        return False, 0.0, "AML Rubric Fail: No rubrics provided"

    # Try online judge API first
    api_key = os.environ.get("JUDGE_API_KEY")
    api_base = os.environ.get("JUDGE_API_BASE", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("JUDGE_MODEL", "gpt-4o-mini")

    if api_key:
        rubrics_text = "\n".join(f"{i}. {r}" for i, r in enumerate(rubrics, start=1))
        prompt = (
            "Starting now, you are a rigorous instruction-following grading teacher. "
            "Your task is to grade the student answer based on the rubrics. "
            "This is a strict, all-or-nothing grading system. Overall Score is binary (0 or 1).\n\n"
            f"【Rubrics】:\n{rubrics_text}\n\n"
            f"【Student Response】:\n{predicted}\n\n"
            "Please strictly output ONLY the following JSON format:\n"
            "{\n  \"Grading Rationale\": \"xxx\",\n"
            "  \"List of Requirement Satisfaction Status\": [\"yes\", \"no\"],\n"
            "  \"Overall Score\": 1\n"
            "}"
        )
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "response_format": {"type": "json_object"}
        }
        try:
            req = urllib.request.Request(
                f"{api_base}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                content = res_data["choices"][0]["message"]["content"]
                result = json.loads(content)
                score = float(result.get("Overall Score", 0))
                rationale = result.get("Grading Rationale", "Judge evaluated successfully.")
                return score == 1.0, score, f"AML Online Judge: {rationale}"
        except Exception as err:
            # Fall back to offline evaluation if API call fails
            pass

    # Offline/Local Fallback Rubric Grading
    failed_rubrics = []
    meta_words = {"must", "should", "mention", "contain", "include", "please", "state", "list", "describe", "refer", "require"}
    
    for rubric in rubrics:
        # Extract clean words, removing punctuation, and filter out metadata noise
        words = [w.strip(".,;:?!()\"'").lower() for w in rubric.split()]
        r_words = [w for w in words if len(w) >= 3 and w not in meta_words]
        
        if not r_words:
            # Fall back to matching the whole raw rubric string (lowercased) if no words survive filters
            r_words = [rubric.lower()]
            
        matched_words = [w for w in r_words if w in predicted.lower()]
        
        # If less than 50% of critical terms match, flag the rubric as failed
        if len(r_words) > 0 and (len(matched_words) / len(r_words)) < 0.5:
            failed_rubrics.append(rubric)

    if failed_rubrics:
        return False, 0.0, f"AML Local Fallback Fail. Failed requirements: {failed_rubrics}"
    
    return True, 1.0, "AML Local Fallback Pass. All semantic rubrics satisfied."


SCORERS = {
    "provenance": score_provenance,
    "contradiction": score_contradiction_recall,
    "authorization": score_authorization_isolation,
    "unsupported_claims": score_unsupported_claims,
    "conformance_verdict": score_conformance_verdict,
    "aml_rubric": score_aml_rubric,
}

def evaluate_assertion(scorer_name: str, actual: Dict[str, Any], expected: Any) -> Tuple[bool, float, str]:
    scorer = SCORERS.get(scorer_name)
    if not scorer:
        return False, 0.0, f"Unknown scorer: {scorer_name}"
    return scorer(actual, expected)
