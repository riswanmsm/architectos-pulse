# Lesson 1 • Example 03: Deterministic Cross-Artifact Verifier (VBC-01 to VBC-08)

**Spec ID:** `SPEC-L1-EX03`  
**Component Target:** `COMP-VERIFIER` (`backend/app/orchestrator/verifier.py`)  
**Database Entity:** `ENT-VERIFICATION-AUDIT` (`vbc_verification_reports`)

---

## 1. Requirements (`requirements.md` — EARS Notation)

### FR-301: Requirement-to-Architecture & API Traceability (`VBC-01`)
```text
WHEN `BlueprintVerifier.verify_artifacts()` inspects `requirements.md`, `architecture.md`, and `api.yaml`
THE SYSTEM SHALL extract every `FR-[1-9][0-9]*` identifier and verify that each `FR-X` is explicitly mapped in either a `COMP-X` component or an OpenAPI route definition.
```

### FR-302: Requirement-to-Negative-Test Traceability (`VBC-02` & `VBC-07`)
```text
WHEN `BlueprintVerifier.verify_artifacts()` evaluates `test-matrix.md`
THE SYSTEM SHALL verify that every `FR-X` has a linked `TEST-X` case AND that negative/conflict assertions (`401`, `403`, `429`, `conflict`) are explicitly declared.
```

### FR-303: Relational Entity & DDL Integrity (`VBC-04`)
```text
WHEN `BlueprintVerifier.verify_artifacts()` parses `schema.sql`
THE SYSTEM SHALL extract all `CREATE TABLE` and `ENT-X` definitions and fail verification if zero relational entities are defined.
```

### FR-304: Measurable Non-Functional Targets (`VBC-05`)
```text
IF `requirements.md` and `test-matrix.md` omit quantitative SLA metrics (`ms`, `% uptime`, `users`, `p95`)
THEN THE SYSTEM SHALL mark rule `VBC-05` as `passed: False` and append a repair recommendation to quantify NFR latency/availability targets.
```

---

## 2. Technical Design (`design.md`)
- **Rule Matrix:** `VBC-01` (Implementation Coverage), `VBC-02` (Test Coverage), `VBC-03` (Auth & Rate Limiting), `VBC-04` (Entity Integrity), `VBC-05` (Measurable NFRs), `VBC-07` (Negative Testing).

## 3. Implementation Tasks (`tasks.md`)
- [x] `TASK-301` (`FR-301`): Build regex + AST token extractors for `FR-X` and `COMP-X`.
- [x] `TASK-302` (`FR-302`): Validate `TEST-X` and negative HTTP status assertions.
- [x] `TASK-303` (`FR-303`): Parse SQL `CREATE TABLE` statements and entity identifiers.
- [x] `TASK-304` (`FR-304`): Compute aggregate `vbc_score` and cap `readiness_score <= 78` on critical findings.
