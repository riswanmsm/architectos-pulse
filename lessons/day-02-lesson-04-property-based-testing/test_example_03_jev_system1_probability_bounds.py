"""
Lesson 4 • Property-Based Testing Example 03:
Jev System-1 Decision Engine Mathematical Bounds (`Noul`, `Score`, `Choice`).
"""
import math
import random
import string
import unittest


ALLOWED_SPECIALISTS = (
    "none",
    "requirements_engineering",
    "architecture_engineering",
    "data_engineering",
    "integration_engineering",
    "quality_engineering",
    "risk_engineering",
)


def jev_system1_evaluate(raw_logit: float, raw_rubric_points: float, failure_domain: str) -> dict:
    """
    Computes Jev System-1 typed outputs from arbitrary raw model/heuristic signals:
    1. Noul: Sigmoid probability clamped strictly in [0.0, 1.0]
    2. Score: Normalized rubric percentage clamped strictly in [0.0, 100.0]
    3. Choice: Deterministic mapping into ALLOWED_SPECIALISTS
    """
    # Safe sigmoid avoiding overflow
    clamped_logit = max(-60.0, min(60.0, float(raw_logit)))
    noul_prob = round(1.0 / (1.0 + math.exp(-clamped_logit)), 6)
    score = round(min(100.0, max(0.0, float(raw_rubric_points))), 2)

    domain_map = {
        "req": "requirements_engineering",
        "arch": "architecture_engineering",
        "db": "data_engineering",
        "api": "integration_engineering",
        "test": "quality_engineering",
        "sec": "risk_engineering",
    }
    if noul_prob >= 0.85 and score >= 85.0:
        choice = "none"
    else:
        choice = domain_map.get(failure_domain, "risk_engineering")

    return {
        "noul": noul_prob,
        "score": score,
        "choice": choice,
    }


class TestExample03JevSystem1ProbabilityBounds(unittest.TestCase):
    """Property-based tests for Jev System-1 (`Noul`, `Score`, `Choice`) invariants."""

    def test_property_extreme_logits_and_scores_preserve_strict_bounds(self):
        """
        INVARIANT 1 (Probability & Rubric Measure Bounds):
        FOR ALL real numbers raw_logit in [-1e9, +1e9] and raw_rubric_points in [-1e6, +1e6],
        0.0 <= noul <= 1.0, 0.0 <= score <= 100.0, and choice in ALLOWED_SPECIALISTS.
        """
        for _ in range(250):
            logit = random.uniform(-1e6, 1e6)
            points = random.uniform(-5000.0, 5000.0)
            domain = "".join(random.choices(string.ascii_lowercase, k=3))

            out = jev_system1_evaluate(logit, points, domain)
            self.assertGreaterEqual(out["noul"], 0.0)
            self.assertLessEqual(out["noul"], 1.0)
            self.assertGreaterEqual(out["score"], 0.0)
            self.assertLessEqual(out["score"], 100.0)
            self.assertIn(out["choice"], ALLOWED_SPECIALISTS)

    def test_property_monotonic_sigmoid_ordering(self):
        """
        INVARIANT 2 (Sigmoid Order Preservation):
        FOR ALL logit_a < logit_b, Jev `noul(logit_a)` <= Jev `noul(logit_b)`.
        """
        for _ in range(200):
            a = random.uniform(-50.0, 50.0)
            b = a + random.uniform(0.001, 25.0)
            out_a = jev_system1_evaluate(a, 90.0, "sec")
            out_b = jev_system1_evaluate(b, 90.0, "sec")
            self.assertLessEqual(out_a["noul"], out_b["noul"])


if __name__ == "__main__":
    unittest.main()
