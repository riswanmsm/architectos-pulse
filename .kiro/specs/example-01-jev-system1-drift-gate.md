# Lesson 1 • Example 01: Jev System-1 Real-Time Spec Drift Gate

**Spec ID:** `SPEC-L1-EX01`  
**Component Target:** `COMP-JEV-GUARD` (`scripts/jev_hook_verify.py`, `backend/app/orchestrator/jev_engine.py`)  
**Database Entity:** `ENT-DRIFT-TELEMETRY` (`jev_guardrail_events`)

---

## 1. Requirements (`requirements.md` — EARS Notation)

### FR-101: Sub-200ms Binary Spec Drift Evaluation (`jev.noul`)
```text
WHEN a developer or Kiro agent saves a source file matching `\.(py|ts|tsx|sql|yaml)$`
THE SYSTEM SHALL execute `jev.noul(spec_context, code_diff)` and emit a typed compliance probability $P(\text{compliant}) \in [0.0, 1.0]$ within 200ms.
```

### FR-102: Multi-Criteria Semantic VBC Rubric Scoring (`jev.score`)
```text
WHEN `jev.noul` completes evaluation of a modified artifact
THE SYSTEM SHALL compute a weighted rubric score $S \in [0.0, 100.0]$ across Requirements Alignment (`VBC-01`), Auth Security (`VBC-03`), and Entity Integrity (`VBC-04`).
```

### FR-103: Unwanted Drift Interception & Specialist Routing (`jev.choice`)
```text
IF the Jev compliance probability $P(\text{compliant}) < 0.85$ OR the VBC rubric score $S < 85.0$
THEN THE SYSTEM SHALL invoke `jev.choice` to select the exact remediation specialist from `["requirements_engineering", "architecture_engineering", "data_engineering", "integration_engineering", "quality_engineering", "risk_engineering"]`.
```

### FR-104: Offline Deterministic Resilience
```text
WHILE the environment lacks an active `JEV_API_KEY` or external network connectivity
THE SYSTEM SHALL transparently execute the local deterministic AST + mathematical rubric engine with $<15\text{ms}$ latency and zero runtime exceptions.
```

---

## 2. Technical Design (`design.md`)
- **Input Contract:** `{ "spec_path": ".kiro/specs/requirements.md", "modified_file": "str", "diff_content": "str" }`
- **Output Contract:** `{ "noul_prob": 0.98, "vbc_score": 96.4, "routed_choice": "none", "latency_ms": 14.2 }`

## 3. Implementation Tasks (`tasks.md`)
- [x] `TASK-101` (`FR-101`): Implement `JevSystemOneEngine.noul()` with probability clamping in $[0.0, 1.0]$.
- [x] `TASK-102` (`FR-102`): Implement `JevSystemOneEngine.score()` mapped to `VBC-01..07` weights.
- [x] `TASK-103` (`FR-103`): Implement `JevSystemOneEngine.choice()` deterministic specialist router.
- [x] `TASK-104` (`FR-104`): Verify offline fallback via Property-Based Test `test_example_03_jev_system1_probability_bounds.py`.
