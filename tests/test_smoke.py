def test_scaffold_smoke():
    assert True

def test_aml_rubric_scorer():
    from nora_evals.scorers import evaluate_assertion
    
    actual = {"model_output": "The First Bank receivership was successfully established in Martin County during 2024."}
    rubrics = ["Must mention First Bank", "Must mention receivership"]
    
    passed, score, msg = evaluate_assertion("aml_rubric", actual, rubrics)
    assert passed is True
    assert score == 1.0
    assert "Local Fallback Pass" in msg

def test_aml_rubric_scorer_fail():
    from nora_evals.scorers import evaluate_assertion
    
    actual = {"model_output": "Standard foreclosure completed."}
    rubrics = ["Must mention First Bank", "Must mention receivership"]
    
    passed, score, msg = evaluate_assertion("aml_rubric", actual, rubrics)
    assert passed is False
    assert score == 0.0
    assert "Local Fallback Fail" in msg

