# Day 2 • Lesson 3: Hooks (250 Credits)

**Reveal Date:** Tuesday, September 22, 2026  
**Kiro Surface:** Kiro IDE / Kiro CLI / Kiro Web  
**Official Documentation:** [https://kiro.dev/docs/hooks/](https://kiro.dev/docs/hooks/)  
**Rubric Weight:** **250 Kiro Credits** (Required for the 1,000-Credit Completion Bonus)

---

## 1. Core Concepts Learned in Lesson 3

1. **What Are Kiro Hooks?**
   - Hooks are automated event listeners stored as JSON files in `.kiro/hooks/*.json`.
   - Whenever a session lifecycle event occurs (such as the agent saving a file, calling an MCP tool, or completing a turn), Kiro matches the event against your hook rules and executes either a **shell command** (`type: "command"`) or an **autonomous agent prompt** (`type: "prompt"`).

2. **Anatomy of a `.kiro/hooks/*.json` File:**
   - `version`: `"v1"`
   - `hooks`: Array of hook objects containing:
     - `name`: Human-readable description of the guardrail/automation.
     - `trigger`: Event trigger (`PostFileSave`, `PreToolUse`, `PostToolUse`, `OnSessionStart`, `PreCommit`).
     - `matcher`: Regular expression filtering which file paths or tool names activate the hook.
     - `action`: `{ "type": "command", "command": "..." }` or `{ "type": "prompt", "prompt": "..." }`.

---

## 2. The 5 Production Hook Examples Included in This Folder

| # | File | Trigger | Matcher | Automated Action |
| :- | :--- | :--- | :--- | :--- |
| **01** | [example-01-post-save-jev-drift-guard.json](./example-01-post-save-jev-drift-guard.json) | `PostFileSave` | `\.(py\|ts\|tsx\|sql\|yaml)$` | Runs sub-200ms Jev System-1 (`Noul` + `Score`) spec drift check |
| **02** | [example-02-post-save-ears-spec-validator.json](./example-02-post-save-ears-spec-validator.json) | `PostFileSave` | `\.kiro/specs/.*\.md$` | Verifies every `FR-X` requirement uses formal EARS (`WHEN ... THE SYSTEM SHALL ...`) |
| **03** | [example-03-post-save-openapi-security-audit.json](./example-03-post-save-openapi-security-audit.json) | `PostFileSave` | `(api\.yaml\|routes.*\.py)$` | Runs `VBC-03` security audit checking OAuth2 JWT & 429 rate-limiting |
| **04** | [example-04-post-save-property-test-runner.json](./example-04-post-save-property-test-runner.json) | `PostFileSave` | `(verifier\|jev).*\.py$` | Executes the Kiro IDE Property-Based Testing suite (`tests/property_tests/`) |
| **05** | [example-05-pre-commit-kiro-rubric-grader.json](./example-05-pre-commit-kiro-rubric-grader.json) | `PostFileSave` | `(\.kiro/.*\|plugin\.json)$` | Runs the 5,250-credit `grade_kiro_submission.py` self-grader |
