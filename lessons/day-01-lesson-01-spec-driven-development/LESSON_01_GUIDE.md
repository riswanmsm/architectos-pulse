# Day 1 • Lesson 1: Spec-Driven Development (250 Credits)

**Reveal Date:** Monday, September 21, 2026  
**Kiro Surface:** Kiro IDE / Kiro CLI / Kiro Web  
**Official Documentation:** [https://kiro.dev/docs/specs/](https://kiro.dev/docs/specs/)  
**Rubric Weight:** **250 Kiro Credits** (Required for the 1,000-Credit Completion Bonus)

---

## 1. Core Concepts Learned in Lesson 1

1. **Why Spec-Driven Development (SDD)?**
   - Unstructured "vibe coding" causes architectural drift, missing edge-case validation, and broken database/API contracts.
   - Kiro's Feature Specs guide development through a deterministic 3-stage pipeline inside `.kiro/specs/`:
     1. **`requirements.md`**: Structured user stories and testable acceptance criteria using **EARS (Easy Approach to Requirements Syntax)**.
     2. **`design.md`**: Technical architecture, component boundaries (`COMP-X`), data models (`ENT-X`), and sequence flows.
     3. **`tasks.md`**: Ordered, checkable implementation sub-tasks mapped back to specific `FR-X` requirements.

2. **The EARS Syntax Standard:**
   - **Ubiquitous:** `THE SYSTEM SHALL <response>`
   - **Event-Driven:** `WHEN <trigger event> THE SYSTEM SHALL <deterministic response>`
   - **State-Driven:** `WHILE <in specific state> THE SYSTEM SHALL <deterministic response>`
   - **Unwanted Behavior / Guardrail:** `IF <error/invalid condition> THEN THE SYSTEM SHALL <mitigation/rejection response>`

---

## 2. The 5 Production Examples Included in This Folder

| # | File | Feature Area | EARS Requirements Covered |
| :- | :--- | :--- | :--- |
| **01** | [example-01-jev-system1-drift-gate.md](./example-01-jev-system1-drift-gate.md) | Jev System-1 (`Noul`, `Score`, `Choice`) Real-Time Spec Drift Guardrail | `FR-101` to `FR-104` |
| **02** | [example-02-architectos-8-specialist-pipeline.md](./example-02-architectos-8-specialist-pipeline.md) | ArchitectOS System-2 8-Specialist Blueprint Synthesis & Self-Correction | `FR-201` to `FR-204` |
| **03** | [example-03-deterministic-vbc-verifier.md](./example-03-deterministic-vbc-verifier.md) | Deterministic Cross-Artifact Verifier (`VBC-01` through `VBC-08`) | `FR-301` to `FR-304` |
| **04** | [example-04-oauth2-jwt-tenant-isolation.md](./example-04-oauth2-jwt-tenant-isolation.md) | Multi-Tenant OAuth2 JWT Security & API Gateway Rate Limiting | `FR-401` to `FR-404` |
| **05** | [example-05-mcp-jsonrpc-protocol-bridge.md](./example-05-mcp-jsonrpc-protocol-bridge.md) | Model Context Protocol (MCP) JSON-RPC 2.0 Tool & Elicitation Server | `FR-501` to `FR-504` |
