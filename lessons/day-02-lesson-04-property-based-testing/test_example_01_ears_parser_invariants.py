"""
Lesson 4 • Property-Based Testing Example 01:
EARS Requirement Parser & Formatter Invariants (Set Uniqueness, Permutation Invariance, Round-Trip).
"""
import random
import re
import string
import unittest
from typing import List, Dict


def format_ears_requirement(fr_id: int, trigger: str, response: str) -> str:
    """Formats a structured requirement into canonical EARS notation."""
    clean_trigger = " ".join(trigger.split()).strip() or "a valid request arrives"
    clean_response = " ".join(response.split()).strip() or "process the request deterministically"
    return f"### FR-{fr_id}\nWHEN {clean_trigger}\nTHE SYSTEM SHALL {clean_response}\n"


def parse_ears_requirements(markdown_text: str) -> List[Dict[str, str]]:
    """Extracts FR-X IDs and EARS WHEN / THE SYSTEM SHALL clauses."""
    pattern = re.compile(
        r"###\s+(FR-[1-9][0-9]*)\s*\nWHEN\s+(.+?)\s*\nTHE SYSTEM SHALL\s+(.+?)(?:\n|$)",
        re.IGNORECASE,
    )
    results = []
    seen = set()
    for match in pattern.finditer(markdown_text):
        fr_code = match.group(1).upper()
        if fr_code not in seen:
            seen.add(fr_code)
            results.append({
                "id": fr_code,
                "when": match.group(2).strip(),
                "shall": match.group(3).strip(),
            })
    return sorted(results, key=lambda x: int(x["id"].split("-")[1]))


class TestExample01EarsParserProperties(unittest.TestCase):
    """Property-based tests for Lesson 1 & Lesson 4 EARS specification parsing."""

    def _rand_clause(self) -> str:
        words = [
            "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
            for _ in range(random.randint(3, 7))
        ]
        return " ".join(words)

    def test_property_round_trip_serialization(self):
        """
        INVARIANT 1 (Round-Trip Property):
        FOR ALL valid (fr_id, trigger, response) tuples,
        formatting to EARS markdown and parsing back MUST preserve exact IDs and normalized clauses.
        """
        for i in range(1, 201):
            trig = self._rand_clause()
            resp = self._rand_clause()
            md = format_ears_requirement(i, trig, resp)
            parsed = parse_ears_requirements(md)
            self.assertEqual(len(parsed), 1)
            self.assertEqual(parsed[0]["id"], f"FR-{i}")
            self.assertEqual(parsed[0]["when"], trig)
            self.assertEqual(parsed[0]["shall"], resp)

    def test_property_permutation_and_duplication_invariance(self):
        """
        INVARIANT 2 (Permutation & Idempotent Deduplication Property):
        Shuffling the order of EARS blocks or duplicating blocks in a spec document
        MUST yield the exact same canonical sorted list of unique FR-X requirements.
        """
        for _ in range(100):
            ids = random.sample(range(1, 50), k=random.randint(4, 12))
            blocks = [format_ears_requirement(idx, self._rand_clause(), self._rand_clause()) for idx in ids]
            shuffled = list(blocks)
            random.shuffle(shuffled)
            duplicated = shuffled + random.sample(blocks, k=len(blocks) // 2)

            res_original = parse_ears_requirements("\n".join(blocks))
            res_permuted = parse_ears_requirements("\n".join(duplicated))
            self.assertEqual(res_original, res_permuted)


if __name__ == "__main__":
    unittest.main()
