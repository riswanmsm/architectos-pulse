# Kiro University Challenge: Full Syllabus, Grading Rubric & Submission Templates

## 1. Official Timeline & Eligibility
- **Challenge Window:** Monday, September 21, 2026 (09:00 PT) – Monday, October 5, 2026 (23:59 PT).
- **Daily Lessons Drop:** Sept 21 – Sept 24, 2026.
- **Final Exam Opens:** Friday, September 25, 2026.
- **Submission Deadline:** Monday, October 5, 2026 at 23:59 PT (PDT).
- **Judging Window (Code Freeze):** October 6 – October 19, 2026 (10 business days). **Do NOT push commits to your repo during this window.**
- **Credit Redemption & Expiry:** Redeem awards by **November 30, 2026**; credits remain active until **March 31, 2027**.

---

## 2. Day-by-Day Lesson Breakdown & Technical Requirements

### Day 1 — Monday, Sept 21, 2026
#### Lesson 1: Spec-Driven Development (250 Credits)
- **What Judges Check:** Presence of `.kiro/specs/` containing structured feature specifications (`requirements.md`, `design.md`, `tasks.md`).
- **Best Practice (EARS Syntax):** Write requirements using **EARS (Easy Approach to Requirements Syntax)**:
  ```text
  WHEN <trigger/precondition>
  THE SYSTEM SHALL <expected deterministic system response>
  ```
- **ArchitectOS + Jev Integration:** ArchitectOS generates the `.kiro/specs/` bundle (`requirements.md`, `architecture.md`, `schema.sql`, `api.yaml`, `test-matrix.md`, `risk-audit.md`) with formal `FR-X`, `NFR-X`, `COMP-X`, and `ENT-X` identifiers.

#### Lesson 2: Steering Documents (250 Credits)
- **What Judges Check:** Markdown files inside `.kiro/steering/` that provide persistent architectural context, coding conventions, and code comparisons.
- **Best Practice:**
  1. Include YAML frontmatter (`inclusion: always` or `inclusion: fileMatch` with `fileMatchPattern`).
  2. State the **Standard/Convention** to enforce.
  3. Explain the **Engineering Intent/Context** behind the rule.
  4. Provide a concrete **Good vs. Bad Code Comparison**.

---

### Day 2 — Tuesday, Sept 22, 2026
#### Lesson 3: Hooks (250 Credits)
- **What Judges Check:** JSON hook configurations stored in `.kiro/hooks/*.json` that automatically trigger commands or agent actions on session events.
- **Required JSON Structure:**
  ```json
  {
    "version": "v1",
    "hooks": [
      {
        "name": "Jev System-1 Spec Drift & VBC Guard",
        "trigger": "PostFileSave",
        "matcher": "\\.(py|ts|tsx|sql|yaml)$",
        "action": {
          "type": "command",
          "command": "python3 scripts/jev_hook_verify.py"
        }
      }
    ]
  }
  ```

#### Lesson 4: Property-Based Testing (PBT) — *Kiro IDE Exclusive* (500 Credits)
- **What Judges Check:** Property-based tests generated/executed via the Kiro IDE that test general logical invariants across hundreds of generated inputs rather than hardcoded example assertions.
- **Best Practice:** Extract invariants directly from your `.kiro/specs/requirements.md` EARS rules (e.g., using `hypothesis` in Python or `fast-check` in TypeScript) and store them in `tests/property_tests/`.

---

### Day 3 — Wednesday, Sept 23, 2026
#### Lesson 5: Powers (500 Credits)
- **What Judges Check:** Usage of Kiro Powers—packaged bundles (`plugin.json` + `skills/` + `mcp.json`) that dynamically load specialized tools, domain workflows, and skills when matching keywords are mentioned.

#### Lesson 6: Model Context Protocol (MCP) (1,000 Credits)
- **What Judges Check:** Registration and active use of MCP servers in `.kiro/mcp.json` (or workspace `mcp.json`) extending Kiro with domain-specific tools, external APIs, or verifiers.

---

### Day 4 — Thursday, Sept 24, 2026
#### Lesson 7: Custom Agents (1,000 Credits)
- **What Judges Check:** Custom agent configuration files (`.kiro/agents/*.json`) specifying tailored `tools`, `excludedTools`, `includeMcpJson`, `resources` (`file://...`, `skill://...`), `permissions.rules`, `prompt`, `model`, and `welcomeMessage`.

#### Bonus Lesson 1: Kiro Web, Cloud Sessions & Cloud Configuration (250 Credits — *Paid Plans*)
- **What Judges Check:** Uploading local `.kiro` configuration to Kiro Cloud Configuration and running a cloud session (e.g., autonomous refactor, test expansion, or spec execution) in Kiro Web / Cloud Sandbox.

#### Bonus Lesson 2: Package a Kiro Power (250 Credits — *Open to All Tiers*)
- **What Judges Check:** Creating and bundling your own custom Kiro Power with a valid `plugin.json` manifest following `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"`, packaged skills (`SKILL.md`), and `mcp.json`.

---

## 3. Ready-to-Use Submission Write-Up Template (Copy & Paste for Final Entry Form)

When submitting at `https://kiro.dev/2026/university`, paste and customize this structured breakdown so the reviewer can immediately verify all **5,250 credits**:

```markdown
### Project Overview (2-3 Sentences)
**ArchitectOS Pulse** combines **ArchitectOS** (an 8-specialist "System 2" architecture committee) with **Jev** (a sub-200ms "System 1" typed decision and guardrail engine) inside **Kiro** to eliminate spec-to-code drift in Spec-Driven Development. It automatically transforms product ideas into verified `.kiro/specs/`, guards every file save via Jev (`Choice`, `Score`, `Noul`) hooks, and self-repairs security or schema mismatches via MCP.

### How Each Kiro University Lesson Was Incorporated

1. **Lesson 1 — Spec-Driven Development (250 Credits):**
   - Located in `.kiro/specs/requirements.md`, `.kiro/specs/design.md`, `.kiro/specs/tasks.md`, `.kiro/specs/schema.sql`, and `.kiro/specs/api.yaml`.
   - Uses formal **EARS notation** (`WHEN ... THE SYSTEM SHALL ...`) mapped deterministically to architecture components (`COMP-X`) and database entities (`ENT-X`).

2. **Lesson 2 — Steering Documents (250 Credits):**
   - Located in `.kiro/steering/architectos-vbc-standards.md` and `.kiro/steering/jev-system1-guardrails.md`.
   - Uses YAML frontmatter (`inclusion: always`) with explicit conventions, architectural rationale, and side-by-side compliant vs. non-compliant code examples enforcing `VBC-01` through `VBC-08`.

3. **Lesson 3 — Hooks (250 Credits):**
   - Located in `.kiro/hooks/post-save-jev-guard.json`.
   - Automatically triggers on `PostFileSave` for `.py`, `.ts`, `.sql`, and `.yaml` files, invoking the System-1 Jev Guardrail verifier (`scripts/jev_hook_verify.py`) to detect spec drift in `<200ms`.

4. **Lesson 4 — Property-Based Testing in Kiro IDE (500 Credits):**
   - Located in `tests/property_tests/test_vbc_jev_properties.py`.
   - Designed and executed in **Kiro IDE** to test mathematical and structural invariants across hundreds of generated blueprints and API specs (e.g., verifying that unauthenticated routes always force `ready == False` and `readiness_score <= 78`, and Jev `Noul`/`Score` outputs remain bounded in $[0, 1]$ and $[0, 100]$).

5. **Lesson 5 — Powers (500 Credits):**
   - Activated Kiro Powers dynamically using domain keywords (`"vbc"`, `"blueprint"`, `"jev"`, `"drift"`, `"security"`, `"openapi"`) to inject specialized verification workflows and reference checklists on demand.

6. **Lesson 6 — Model Context Protocol (MCP) (1,000 Credits):**
   - Configured in `.kiro/mcp.json` and implemented in `backend/app/mcp/server.py`.
   - Exposes 5 specialized MCP tools (`architectos_generate_blueprint`, `architectos_verify_spec`, `architectos_audit_risk`, `jev_verify_code_drift`, and `jev_route_specialist`) via JSON-RPC 2.0.

7. **Lesson 7 — Custom Agents (1,000 Credits):**
   - Configured in `.kiro/agents/architect-pulse-agent.json`.
   - Defines a purpose-built Principal Architect & Security Auditor agent pre-loaded with `PRODUCT_VISION.md`, `.kiro/specs/`, MCP server access, and fine-grained `shell` permissions (`pytest`, `python3`, `git`).

8. **Bonus Lesson 1 — Kiro Web & Cloud Sessions (250 Credits):**
   - Synced local `.kiro/` steering, hooks, specs, and custom agents via Kiro Cloud Configuration to execute autonomous multi-file verification and test generation in Kiro Cloud Sessions.

9. **Bonus Lesson 2 — Packaged Custom Kiro Power (250 Credits):**
   - Packaged as a standalone, shareable Kiro Power in `architectos-jev-power/` with an `agent-plugins.org` v1.0.0 compliant `plugin.json` manifest, `skills/vbc-jev-verifier/SKILL.md`, and `mcp.json`.
```
