# Day 1 • Lesson 2: Steering Documents (250 Credits)

**Reveal Date:** Monday, September 21, 2026  
**Kiro Surface:** Kiro IDE / Kiro CLI / Kiro Web  
**Official Documentation:** [https://kiro.dev/docs/steering/](https://kiro.dev/docs/steering/)  
**Rubric Weight:** **250 Kiro Credits** (Required for the 1,000-Credit Completion Bonus)

---

## 1. Core Concepts Learned in Lesson 2

1. **What Are Steering Documents?**
   - Steering documents reside in `.kiro/steering/*.md` (workspace scope) or `~/.kiro/steering/*.md` (global scope).
   - They give Kiro persistent, structured project context so its generated code consistently follows your architecture, libraries, and security rules without repeating instructions in every prompt.

2. **YAML Frontmatter Inclusion Modes:**
   - `inclusion: always` — Loaded unconditionally into every Kiro session.
   - `inclusion: fileMatch` (with `fileMatchPattern: "**/*.py"`) — Loaded dynamically only when working on matching files.
   - `inclusion: manual` — Loaded on demand when referenced via `#steering-file-name` in chat.

3. **Kiro's 3-Part Best Practice Formula for Steering Files:**
   1. **Define the Standard/Convention** you want Kiro to enforce.
   2. **Explain the Engineering Intent/Context** behind the enforcement.
   3. **Provide a Code Comparison** (`❌ Non-Compliant` vs. `✅ Compliant`).

---

## 2. The 5 Production Steering Examples Included in This Folder

| # | File | Inclusion Mode | What It Steers |
| :- | :--- | :--- | :--- |
| **01** | [example-01-vbc-traceability-standard.md](./example-01-vbc-traceability-standard.md) | `inclusion: always` | Global `FR-X` $\to$ `COMP-X` $\to$ `ENT-X` $\to$ `TEST-X` VBC traceability |
| **02** | [example-02-jev-system1-decision-contracts.md](./example-02-jev-system1-decision-contracts.md) | `inclusion: fileMatch` (`**/*jev*.py`) | Typed Jev `Noul` $\in [0,1]$, `Score` $\in [0,100]$, `Choice` enum & offline fallback |
| **03** | [example-03-fastapi-security-oauth2-guardrails.md](./example-03-fastapi-security-oauth2-guardrails.md) | `inclusion: fileMatch` (`**/api/**/*.py`) | Mandatory `VBC-03` OAuth2 Bearer JWT, rate limiting & `401`/`403`/`429` responses |
| **04** | [example-04-postgres-ddl-entity-integrity.md](./example-04-postgres-ddl-entity-integrity.md) | `inclusion: fileMatch` (`**/*.sql`) | `VBC-04` UUID primary keys, `tenant_id` foreign keys, indexes & audit columns |
| **05** | [example-05-react-tailwind-telemetry-ui.md](./example-05-react-tailwind-telemetry-ui.md) | `inclusion: fileMatch` (`**/*.tsx`) | System-1 (`<200ms`) vs. System-2 (`~22s`) latency badges & VBC score gauges |
