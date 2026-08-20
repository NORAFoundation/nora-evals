from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time

@dataclass
class AssertionSpec:
    scorer: str  # provenance, contradiction, authorization, unsupported_claims
    expected: Any
    weight: float = 1.0

@dataclass
class TestCase:
    id: str
    category: str
    prompt: str
    context: Dict[str, Any]
    expected_output: Any
    assertions: List[AssertionSpec] = field(default_factory=list)

@dataclass
class FixtureManifest:
    id: str
    name: str
    version: str
    target_project: str
    description: str
    cases: List[TestCase] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FixtureManifest:
        cases = []
        for c in data.get("cases", []):
            assertions = [
                AssertionSpec(
                    scorer=a["scorer"],
                    expected=a["expected"],
                    weight=a.get("weight", 1.0)
                ) for a in c.get("assertions", [])
            ]
            cases.append(TestCase(
                id=c["id"],
                category=c.get("category", "general"),
                prompt=c.get("prompt", ""),
                context=c.get("context", {}),
                expected_output=c.get("expected_output"),
                assertions=assertions
            ))
        return cls(
            id=data["id"],
            name=data["name"],
            version=data.get("version", "1.0.0"),
            target_project=data.get("target_project", "generic"),
            description=data.get("description", ""),
            cases=cases
        )

@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResultBundle:
    fixture_id: str
    target_project: str
    timestamp: float
    total_cases: int
    passed_cases: int
    overall_score: float
    results: List[EvalResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "target_project": self.target_project,
            "timestamp": self.timestamp,
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "overall_score": round(self.overall_score, 4),
            "results": [
                {
                    "case_id": r.case_id,
                    "passed": r.passed,
                    "score": round(r.score, 4),
                    "details": r.details
                } for r in self.results
            ]
        }
