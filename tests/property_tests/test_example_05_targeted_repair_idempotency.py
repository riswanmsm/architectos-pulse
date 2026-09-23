"""
Lesson 4 • Property-Based Testing Example 05:
Targeted Self-Correction Loop Convergence & Idempotency Invariants ($R(R(B)) == R(B)$).
"""
import random
import unittest
from typing import Dict


def targeted_specialist_repair(blueprint: Dict[str, str]) -> Dict[str, str]:
    """
    Deterministic model of ArchitectOS + Jev Targeted Self-Correction Loop:
    Inspects only deficient slices and injects canonical compliant clauses without mutating valid slices.
    """
    repaired = dict(blueprint)
    if "WHEN " not in repaired.get("requirements", "") or "THE SYSTEM SHALL" not in repaired.get("requirements", ""):
        repaired["requirements"] = (
            repaired.get("requirements", "").strip()
            + "\nWHEN a user submits a request THE SYSTEM SHALL validate and process FR-1 within 150ms."
        ).strip()

    if "OAuth2" not in repaired.get("architecture", "") or "Rate-limiting" not in repaired.get("architecture", ""):
        repaired["architecture"] = (
            repaired.get("architecture", "").strip()
            + "\nCOMP-1 API Gateway enforces OAuth2 Bearer JWT authentication and Rate-limiting (100 req/min)."
        ).strip()

    if "CREATE TABLE" not in repaired.get("database", "").upper():
        repaired["database"] = (
            repaired.get("database", "").strip()
            + "\nCREATE TABLE IF NOT EXISTS ent_1_records (id UUID PRIMARY KEY, tenant_id UUID NOT NULL);"
        ).strip()

    if "401" not in repaired.get("testing", "") or "429" not in repaired.get("testing", ""):
        repaired["testing"] = (
            repaired.get("testing", "").strip()
            + "\nTEST-1 verifies FR-1 negative assertions for 401 Unauthorized and 429 Too Many Requests."
        ).strip()

    return repaired


def score_blueprint(bp: Dict[str, str]) -> float:
    checks = [
        "WHEN " in bp.get("requirements", "") and "THE SYSTEM SHALL" in bp.get("requirements", ""),
        "OAuth2" in bp.get("architecture", "") and "Rate-limiting" in bp.get("architecture", ""),
        "CREATE TABLE" in bp.get("database", "").upper(),
        "401" in bp.get("testing", "") and "429" in bp.get("testing", ""),
    ]
    return (sum(1 for c in checks if c) / len(checks)) * 100.0


class TestExample05TargetedRepairIdempotency(unittest.TestCase):
    """Property-based tests for ArchitectOS + Jev self-correction loop idempotency and monotonicity."""

    def test_property_repair_is_strictly_idempotent_and_converges_to_100_vbc(self):
        """
        INVARIANT 1 (Idempotency & Convergence):
        FOR ALL arbitrary/incomplete initial blueprints B,
        1. score(repair(B)) >= score(B) (Monotonic improvement)
        2. score(repair(B)) == 100.0% (Single-pass convergence)
        3. repair(repair(B)) == repair(B) (Strict functional idempotency)
        """
        sample_fragments = ["", "Draft spec", "WHEN x THE SYSTEM SHALL y", "OAuth2 Rate-limiting", "CREATE TABLE t (id INT);"]
        for _ in range(200):
            initial = {
                "requirements": random.choice(sample_fragments),
                "architecture": random.choice(sample_fragments),
                "database": random.choice(sample_fragments),
                "testing": random.choice(sample_fragments),
            }
            initial_score = score_blueprint(initial)
            repaired_once = targeted_specialist_repair(initial)
            repaired_twice = targeted_specialist_repair(repaired_once)

            self.assertGreaterEqual(score_blueprint(repaired_once), initial_score)
            self.assertEqual(score_blueprint(repaired_once), 100.0)
            self.assertEqual(repaired_once, repaired_twice, "Targeted repair must be strictly idempotent: R(R(B)) == R(B)")


if __name__ == "__main__":
    unittest.main()
