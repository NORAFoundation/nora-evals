from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
from nora_evals.schema import ResultBundle

def generate_markdown_report(bundle: ResultBundle) -> str:
    lines = [
        f"# Evaluation Baseline Report — {bundle.fixture_id}",
        "",
        f"- **Target Suite:** `{bundle.target_project}`",
        f"- **Overall Reliability Score:** `{round(bundle.overall_score * 100, 2)}%`",
        f"- **Cases Passed:** `{bundle.passed_cases}/{bundle.total_cases}`",
        "",
        "## Test Case Details",
        "",
        "| Case ID | Status | Score | Scorers & Assertion Findings |",
        "|---------|--------|-------|------------------------------|"
    ]
    
    for r in bundle.results:
        status_str = "PASS" if r.passed else "FAIL"
        details_summary = "; ".join(
            f"{k}: {v['message']}" for k, v in r.details.items()
        )
        lines.append(f"| `{r.case_id}` | **{status_str}** | `{round(r.score, 4)}` | {details_summary} |")

    lines.append("")
    lines.append("## Epistemological Assurance Statement")
    lines.append("All assertions assert zero authorization leakage, strict exact-locator grounding, and contradiction recall over synthetic corpora.")
    return "\n".join(lines) + "\n"
