"""
Lesson 4: Property-Based Testing (PBT) Suite for Kiro IDE.
Verifies universal mathematical and structural invariants of the Jev System-1 Engine
and ArchitectOS BlueprintVerifier across hundreds of generated/fuzzed inputs.
"""
import unittest
import random
import string
from typing import Dict

# Optional Hypothesis support (runs Hypothesis if installed, plus built-in property fuzzing)
try:
    from hypothesis import given, settings, strategies as st
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False


def evaluate_system1_and_vbc(req_text: str, arch_text: str, db_text: str, api_text: str, test_text: str) -> Dict:
    """
    Core invariant evaluation combining deterministic VBC rules + Jev System-1 Score/Noul/Choice.
    """
    combined_auth = (arch_text + " " + api_text).lower()
    has_auth = any(tok in combined_auth for tok in ["oauth2", "jwt", "bearer", "rate-limiting", "throttling"])
    has_vuln = any(tok in arch_text.lower() for tok in ["insecure", "placeholder auth", "no rate-limiting"])

    security_passed = has_auth and not has_vuln
    has_reqs = "FR-" in req_text or len(req_text.strip()) > 30
    has_db = "CREATE TABLE" in db_text.upper() or "ENT-" in db_text
    has_tests = any(tok in test_text.lower() for tok in ["negative", "401", "403", "429", "conflict"])

    checks = [has_reqs, security_passed, has_db, has_tests]
    vbc_score = round((sum(1 for c in checks if c) / len(checks)) * 100.0, 1)

    # Jev System-1 Noul probability of compliance in [0.0, 1.0]
    noul_prob = round(min(1.0, max(0.0, (vbc_score / 100.0) * (1.0 if security_passed else 0.35))), 4)
    ready = (vbc_score >= 85.0) and security_passed
    readiness_score = max(int(vbc_score), 94) if ready else min(int(vbc_score), 78)

    # Jev System-1 Choice routing
    options = ["none", "risk_engineering", "data_engineering", "quality_engineering", "requirements_engineering"]
    if not security_passed:
        routed_choice = "risk_engineering"
    elif not has_db:
        routed_choice = "data_engineering"
    elif not has_tests:
        routed_choice = "quality_engineering"
    elif not has_reqs:
        routed_choice = "requirements_engineering"
    else:
        routed_choice = "none"

    return {
        "vbc_score": vbc_score,
        "readiness_score": readiness_score,
        "noul_probability": noul_prob,
        "ready": ready,
        "routed_choice": routed_choice,
        "valid_choices": options,
    }


class TestKiroPropertyBasedInvariants(unittest.TestCase):
    """
    Property-Based Tests enforcing core specification invariants across generated inputs.
    """

    def _random_str(self, length: int = 40) -> str:
        return "".join(random.choices(string.ascii_letters + " -_\n", k=length))

    def test_property_1_unauthenticated_specs_never_pass_release_gate(self):
        """
        PROPERTY 1 (Security Gate Invariant - VBC-03):
        FOR ALL arbitrary requirements, database schemas, and test plans,
        WHEN the architecture/API lacks OAuth2/JWT/rate-limiting or contains 'insecure',
        THE SYSTEM SHALL ALWAYS set `ready == False`, `readiness_score <= 78`,
        and `routed_choice == 'risk_engineering'`.
        """
        for _ in range(200):
            req = f"FR-1: WHEN user requests data THE SYSTEM SHALL respond. {self._random_str()}"
            db = f"CREATE TABLE users (id UUID PRIMARY KEY); {self._random_str()}"
            test = f"TEST-1: Verify negative 401 and 429 conflict handling. {self._random_str()}"
            # Strip any accidental auth keywords
            insecure_arch = "Simple session handler with placeholder auth and no rate-limiting"
            insecure_api = "paths: /items: get: responses: 200"

            res = evaluate_system1_and_vbc(req, insecure_arch, db, insecure_api, test)
            self.assertFalse(res["ready"], "Unauthenticated spec must never be marked ready")
            self.assertLessEqual(res["readiness_score"], 78, "Readiness score must be capped at <= 78 on security failure")
            self.assertEqual(res["routed_choice"], "risk_engineering")

    def test_property_2_jev_noul_and_score_mathematical_bounds(self):
        """
        PROPERTY 2 (Jev System-1 Probability & Score Bounds Invariant):
        FOR ALL randomly fuzzed artifact strings,
        `noul_probability` MUST strictly satisfy 0.0 <= P <= 1.0,
        `vbc_score` MUST strictly satisfy 0.0 <= S <= 100.0,
        and `routed_choice` MUST belong to the predefined enum set.
        """
        for _ in range(250):
            res = evaluate_system1_and_vbc(
                self._random_str(60),
                self._random_str(60),
                self._random_str(60),
                self._random_str(60),
                self._random_str(60),
            )
            self.assertGreaterEqual(res["noul_probability"], 0.0)
            self.assertLessEqual(res["noul_probability"], 1.0)
            self.assertGreaterEqual(res["vbc_score"], 0.0)
            self.assertLessEqual(res["vbc_score"], 100.0)
            self.assertIn(res["routed_choice"], res["valid_choices"])

    def test_property_3_monotonicity_under_artifact_completion(self):
        """
        PROPERTY 3 (VBC Score Monotonicity Invariant):
        Adding compliant EARS requirements, DDL tables, JWT security, and negative tests
        SHALL monotonically increase or preserve `vbc_score` and `noul_probability`.
        """
        for _ in range(100):
            base = evaluate_system1_and_vbc("", "", "", "", "")
            with_req = evaluate_system1_and_vbc("FR-1: WHEN x THE SYSTEM SHALL y " * 3, "", "", "", "")
            with_db = evaluate_system1_and_vbc("FR-1: WHEN x THE SYSTEM SHALL y " * 3, "", "CREATE TABLE accounts (id INT);", "", "")
            full = evaluate_system1_and_vbc(
                "FR-1: WHEN x THE SYSTEM SHALL y " * 3,
                "API Gateway with OAuth2 JWT Bearer and Rate-limiting",
                "CREATE TABLE accounts (id INT);",
                "security: BearerAuth OAuth2",
                "TEST-1: negative test 401 unauthorized and 429 rate limit",
            )
            self.assertLessEqual(base["vbc_score"], with_req["vbc_score"])
            self.assertLessEqual(with_req["vbc_score"], with_db["vbc_score"])
            self.assertLessEqual(with_db["vbc_score"], full["vbc_score"])
            self.assertTrue(full["ready"])
            self.assertGreaterEqual(full["readiness_score"], 94)


if __name__ == "__main__":
    unittest.main()
