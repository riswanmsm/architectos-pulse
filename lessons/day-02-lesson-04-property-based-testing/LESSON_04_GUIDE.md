# Day 2 • Lesson 4: Property-Based Testing (Kiro IDE Exclusive — 500 Credits)

**Reveal Date:** Tuesday, September 22, 2026  
**Kiro Surface:** **Kiro IDE Exclusive**  
**Official Documentation:** [https://kiro.dev/docs/specs/correctness/](https://kiro.dev/docs/specs/correctness/)  
**Rubric Weight:** **500 Kiro Credits** (Double the value of Lessons 1–3!)

---

## 1. Core Concepts Learned in Lesson 4

1. **Why Property-Based Testing (PBT) Over Example Tests?**
   - Traditional unit tests only check 2–3 hardcoded inputs (`assert add(2, 3) == 5`). AI coding agents can accidentally pass example tests while failing edge cases.
   - **Property-Based Testing (PBT)** defines **universal invariants** derived directly from your `.kiro/specs/requirements.md` EARS rules and tests them against **hundreds of randomly generated/fuzzed inputs**.
   - In the **Kiro IDE**, PBTs are extracted during the **Design phase** (`design.md`) and executed to mathematically verify correctness.

2. **The 4 Types of Invariants Kiro Extracts from Specs:**
   - **Round-Trip / Isomorphism Invariants:** `parse(format(x)) == x`
   - **Boundary & Clamping Invariants:** `0.0 <= Jev.noul(x) <= 1.0` and `0.0 <= Jev.score(x) <= 100.0`
   - **Security Rejection Invariants (`VBC-03`):** Removing JWT/rate-limiting from *any* valid blueprint must *always* force `ready == False` and `readiness_score <= 78`.
   - **Idempotency & Monotonicity Invariants:** Applying targeted specialist repair twice equals applying it once ($R(R(x)) == R(x)$), and never decreases Verified Blueprint Coverage ($\text{VBC}(R(x)) \ge \text{VBC}(x)$).

---

## 2. The 5 Executable Property-Based Test Modules Included in This Folder

| # | File | Universal Invariant Verified | Fuzzing Iterations |
| :- | :--- | :--- | :---: |
| **01** | [test_example_01_ears_parser_invariants.py](./test_example_01_ears_parser_invariants.py) | EARS (`WHEN ... THE SYSTEM SHALL ...`) extraction set-uniqueness, permutation invariance & round-trip formatting | 200 runs |
| **02** | [test_example_02_vbc_security_gate_invariants.py](./test_example_02_vbc_security_gate_invariants.py) | `VBC-03` Security Gate: Any unauthenticated or unthrottled API/architecture strictly forces `ready == False` & `readiness_score <= 78` | 200 runs |
| **03** | [test_example_03_jev_system1_probability_bounds.py](./test_example_03_jev_system1_probability_bounds.py) | Jev System-1 (`Noul`, `Score`, `Choice`) probability bounds $\in [0,1]$, rubric score bounds $\in [0,100]$ & deterministic specialist routing | 250 runs |
| **04** | [test_example_04_cross_artifact_entity_integrity.py](./test_example_04_cross_artifact_entity_integrity.py) | `VBC-04` & `VBC-06` SQL DDL (`CREATE TABLE` / `ENT-X`) to OpenAPI entity referential integrity & monotonic score improvement | 200 runs |
| **05** | [test_example_05_targeted_repair_idempotency.py](./test_example_05_targeted_repair_idempotency.py) | ArchitectOS + Jev Targeted Self-Correction Loop convergence ($\text{VBC}(R(B)) \ge 94\%$) and idempotency ($R(R(B)) == R(B)$) | 200 runs |
