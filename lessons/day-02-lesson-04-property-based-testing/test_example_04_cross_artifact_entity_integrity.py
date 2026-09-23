"""
Lesson 4 • Property-Based Testing Example 04:
VBC-04 & VBC-06 Cross-Artifact Relational DDL-to-API Referential Integrity Invariants.
"""
import random
import re
import string
import unittest
from typing import Set


def extract_ddl_tables(sql_text: str) -> Set[str]:
    return {
        m.lower()
        for m in re.findall(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)", sql_text, re.I)
    }


def verify_cross_artifact_entity_links(sql_text: str, api_referenced_entities: Set[str]) -> dict:
    defined_tables = extract_ddl_tables(sql_text)
    normalized_refs = {e.lower() for e in api_referenced_entities}
    missing_tables = sorted(list(normalized_refs - defined_tables))
    coverage = 100.0 if not normalized_refs else round(((len(normalized_refs) - len(missing_tables)) / len(normalized_refs)) * 100.0, 2)
    return {
        "defined_tables": defined_tables,
        "missing_tables": missing_tables,
        "entity_coverage_pct": coverage,
        "vbc_04_06_passed": len(missing_tables) == 0 and len(defined_tables) > 0,
    }


class TestExample04CrossArtifactEntityIntegrity(unittest.TestCase):
    """Property-based tests for DDL-to-API referential integrity (`VBC-04` & `VBC-06`)."""

    def _rand_table_name(self) -> str:
        return "tbl_" + "".join(random.choices(string.ascii_lowercase, k=6))

    def test_property_superset_ddl_always_achieves_100_percent_entity_coverage(self):
        r"""
        INVARIANT 1 (Superset Referential Completeness):
        FOR ALL non-empty sets of API-referenced entities $E_{API}$ and extra DDL tables $E_{extra}$,
        if `schema.sql` defines $E_{API} \cup E_{extra}$, `missing_tables` MUST be empty and coverage == 100.0%.
        """
        for _ in range(200):
            api_entities = {self._rand_table_name() for _ in range(random.randint(1, 8))}
            extra_tables = {self._rand_table_name() for _ in range(random.randint(0, 5))}
            all_tables = api_entities.union(extra_tables)
            sql = "\n".join(f"CREATE TABLE IF NOT EXISTS {t} (id UUID PRIMARY KEY);" for t in all_tables)

            res = verify_cross_artifact_entity_links(sql, api_entities)
            self.assertTrue(res["vbc_04_06_passed"])
            self.assertEqual(res["missing_tables"], [])
            self.assertEqual(res["entity_coverage_pct"], 100.0)

    def test_property_removing_any_referenced_table_strictly_drops_coverage(self):
        """
        INVARIANT 2 (Orphan Reference Detection):
        Removing k >= 1 tables referenced by the API from `schema.sql` MUST always force
        `vbc_04_06_passed == False` and `len(missing_tables) == k`.
        """
        for _ in range(200):
            api_entities = [self._rand_table_name() for _ in range(random.randint(2, 8))]
            unique_entities = list(set(api_entities))
            if len(unique_entities) < 2:
                continue
            k_remove = random.randint(1, len(unique_entities) - 1)
            kept = set(unique_entities[k_remove:])
            sql = "\n".join(f"CREATE TABLE {t} (id UUID PRIMARY KEY);" for t in kept)

            res = verify_cross_artifact_entity_links(sql, set(unique_entities))
            self.assertFalse(res["vbc_04_06_passed"])
            self.assertEqual(len(res["missing_tables"]), k_remove)
            self.assertLess(res["entity_coverage_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
