"""nora-evals package."""

from .report import generate_markdown_report
from .runner import EvalRunner
from .scorers import (
    SCORERS,
    evaluate_assertion,
    score_authorization_isolation,
    score_conformance_verdict,
    score_contradiction_recall,
    score_provenance,
    score_unsupported_claims,
)

__all__ = [
    "EvalRunner",
    "SCORERS",
    "evaluate_assertion",
    "generate_markdown_report",
    "score_authorization_isolation",
    "score_conformance_verdict",
    "score_contradiction_recall",
    "score_provenance",
    "score_unsupported_claims",
]
__version__ = "0.0.1"
