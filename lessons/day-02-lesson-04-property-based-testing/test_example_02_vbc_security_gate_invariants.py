"""
Lesson 4 • Property-Based Testing Example 02:
VBC-03 Security Gate Invariants (OAuth2 Bearer JWT & Rate-Limiting Enforcement).
"""
import random
import string
import unittest


def verify_vbc03_security_gate(arch_spec: str, api_spec: str, base_vbc_score: float) -> dict:
    """
    Implements VBC-03: Evaluates whether architecture and API contracts enforce OAuth2/JWT
    and rate-limiting, and caps readiness score if any vulnerability or missing auth exists.
    """
    combined = f"{arch_spec} {api_spec}".lower()
    has_auth = any(k in combined for k in ["oauth2", "jwt", "bearer"])
    has_rate_limit = any(k in combined for k in ["rate-limiting", "rate_limit", "throttling", "429"])
    has_insecure_marker = any(k in combined for k in ["insecure", "placeholder auth", "no rate-limiting", "unauthenticated admin"])

    passed = has_auth and has_rate_limit and not has_insecure_marker
    clamped_base = min(100.0, max(0.0, float(base_vbc_score)))
    if not passed:
        return {
            "vbc_03_passed": False,
            "ready": False,
            "readiness_score": min(int(clamped_base), 78),
            "routed_specialist": "risk_engineering",
        }
    return {
        "vbc_03_passed": True,
        "ready": clamped_base >= 85.0,
        "readiness_score": max(int(clamped_base), 94) if clamped_base >= 85.0 else int(clamped_base),
        "routed_specialist": "none",
    }


class TestExample02VbcSecurityGateProperties(unittest.TestCase):
    """Property-based tests for VBC-03 authentication & rate-limiting release gate invariants."""

    def _fuzzed_text(self, forbidden_words: list) -> str:
        raw = "".join(random.choices(string.ascii_lowercase + " ", k=80))
        for w in forbidden_words:
            raw = raw.replace(w, "")
        return raw

    def test_property_missing_auth_or_rate_limit_always_blocks_release(self):
        """
        INVARIANT 1 (Zero-Trust Security Gate):
        FOR ALL base VBC scores in [0, 100] (even 100.0%), if OAuth2/JWT or rate-limiting is absent,
        `ready` MUST be False, `readiness_score` MUST be <= 78, and `routed_specialist` MUST be `risk_engineering`.
        """
        for _ in range(200):
            fuzzed_arch = self._fuzzed_text(["oauth2", "jwt", "bearer", "rate-limiting", "throttling", "429"])
            fuzzed_api = self._fuzzed_text(["oauth2", "jwt", "bearer", "rate-limiting", "throttling", "429"])
            random_score = random.uniform(0.0, 100.0)

            res = verify_vbc03_security_gate(fuzzed_arch, fuzzed_api, random_score)
            self.assertFalse(res["vbc_03_passed"])
            self.assertFalse(res["ready"])
            self.assertLessEqual(res["readiness_score"], 78)
            self.assertEqual(res["routed_specialist"], "risk_engineering")

    def test_property_explicit_vulnerability_poisoning_always_blocks_release(self):
        """
        INVARIANT 2 (Vulnerability Poisoning Rejection):
        Even when OAuth2 JWT and 429 rate-limiting keywords are present, injecting 'placeholder auth'
        or 'insecure' into any part of the spec MUST immediately fail VBC-03.
        """
        for _ in range(200):
            valid_prefix = "API Gateway with OAuth2 Bearer JWT and 429 rate-limiting "
            poison = random.choice(["placeholder auth", "insecure", "no rate-limiting", "unauthenticated admin"])
            res = verify_vbc03_security_gate(valid_prefix + poison, "security: BearerAuth", 99.0)
            self.assertFalse(res["vbc_03_passed"])
            self.assertFalse(res["ready"])
            self.assertLessEqual(res["readiness_score"], 78)


if __name__ == "__main__":
    unittest.main()
