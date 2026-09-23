# Lesson 1 • Example 02: ArchitectOS System-2 8-Specialist Blueprint Pipeline

**Spec ID:** `SPEC-L1-EX02`  
**Component Target:** `COMP-COORDINATOR` (`backend/app/orchestrator/coordinator.py`)  
**Database Entity:** `ENT-BLUEPRINT-SESSION` (`blueprint_sessions`)

---

## 1. Requirements (`requirements.md` — EARS Notation)

### FR-201: Shared Structured Context Propagation
```text
WHEN a user submits a software product idea to start an ArchitectOS session
THE SYSTEM SHALL sequentially orchestrate all 8 specialist agents (`Coordination`, `Requirements`, `Architecture`, `Database`, `API`, `Testing`, `Risk`, `Communication`) while passing upstream structured artifacts (`FR-X`, `COMP-X`, `ENT-X`) into each downstream specialist prompt.
```

### FR-202: Targeted Self-Correction Loop Without Full Re-Execution
```text
IF the `Risk Engineering` stage detects a Verified Blueprint Coverage (VBC) below 85.0% or any critical security finding
THEN THE SYSTEM SHALL re-invoke only the affected upstream specialist discipline with targeted repair instructions rather than restarting the 8-agent pipeline from scratch.
```

### FR-203: Native `.kiro/specs/` Bundle Export
```text
WHEN an ArchitectOS blueprint session reaches `ready == True` (`VBC >= 94%`)
THE SYSTEM SHALL export a standardized `.kiro/specs/` archive containing `requirements.md`, `architecture.md`, `schema.sql`, `api.yaml`, `test-matrix.md`, and `risk-audit.md`.
```

### FR-204: Human Architect Gate Signoff
```text
WHILE a session is awaiting final production release signoff
THE SYSTEM SHALL hold final specification packaging at the `Human Architect Gate` until explicit approval (`approved == True`) is recorded with audit notes.
```

---

## 2. Technical Design (`design.md`)
- **State Machine:** `INIT` $\to$ `SPECIALIST_PIPELINE` $\to$ `VBC_VERIFY` $\to$ (`TARGETED_REPAIR` if `VBC < 85%`) $\to$ `HUMAN_GATE` $\to$ `KIRO_EXPORT`.

## 3. Implementation Tasks (`tasks.md`)
- [x] `TASK-201` (`FR-201`): Wire context injection across all 8 specialist prompts.
- [x] `TASK-202` (`FR-202`): Implement selective `architecture_retry` and `risk_retry` repair loops.
- [x] `TASK-203` (`FR-203`): Implement `format_kiro_specs()` and ZIP stream generator.
- [x] `TASK-204` (`FR-204`): Add `record_human_approval()` endpoint and trajectory log entry.
