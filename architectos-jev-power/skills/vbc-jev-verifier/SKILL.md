---
name: kiro-university-challenge
description: >-
  Complete end-to-end engineering, scaffolding, grading, and submission runbook
  for the Kiro University Challenge (Sept 21 - Oct 5, 2026; up to 5,250 credits).
  Use this skill whenever designing, building, verifying, or grading a Kiro
  project, configuring .kiro/ artifacts (Specs/EARS, Steering, Hooks, Property-Based
  Testing, Powers, MCP, Custom Agents), or integrating Jev (System 1 guardrail/router)
  with ArchitectOS (System 2 multi-agent blueprint verifier).
---

# Kiro University Challenge + Jev & ArchitectOS Master Skill

This skill provides the complete architecture, templates, automated grader, and scaffolding tools to earn the maximum **5,250 Kiro credits** in the **Kiro University Challenge** by combining:
- **Kiro Agentic IDE/CLI/Web** (`.kiro/` Spec-Driven Development ecosystem)
- **Jev (System 1 Typed Decision Engine)** (`Choice`, `Score`, `Noul` in `<200ms`)
- **ArchitectOS (System 2 Multi-Agent Blueprint Engine)** (8-specialist committee + `VBC-01..08` deterministic verifier)

---

## 1. Quick-Start Commands & Helper Scripts

Run these scripts directly to scaffold a compliant challenge project or audit your repository's score out of **5,250 credits**:

1. **Scaffold a Full 5,250-Credit Kiro + Jev + ArchitectOS Project:**
   ```bash
   python3 /Users/riswansaheed/Development/competitions/.agents/skills/kiro-university-challenge/scripts/scaffold_kiro_challenge.py --target /Users/riswansaheed/Development/competitions/architectos-pulse
   ```
2. **Run the Automated 5,250-Credit Self-Grader & Compliance Auditor:**
   ```bash
   python3 /Users/riswansaheed/Development/competitions/.agents/skills/kiro-university-challenge/scripts/grade_kiro_submission.py --repo /Users/riswansaheed/Development/competitions/architectos-pulse
   ```

---

## 2. The 5,250-Credit Grading Rubric & Required Artifacts

Every submission is scored once on the **Final Exam build** (opens **Fri Sept 25, 2026**, due **Mon Oct 5, 2026 at 23:59 PT**). Your repository **MUST** include the `.kiro/` directory containing evidence for all 7 required lessons + 2 bonuses:

| Lesson | Topic | Credits | Required File / Evidence in Repository | Template Reference |
| :--- | :--- | :---: | :--- | :--- |
| **Lesson 1** | **Spec-Driven Development** | **250** | `.kiro/specs/requirements.md` (with **EARS** `WHEN ... THE SYSTEM SHALL ...`), `design.md`, `tasks.md` | [requirements.md](./examples/kiro_templates/specs/requirements.md) |
| **Lesson 2** | **Steering Documents** | **250** | `.kiro/steering/*.md` with YAML frontmatter (`inclusion: always`) + context + code examples | [architectos-vbc-standards.md](./examples/kiro_templates/steering/architectos-vbc-standards.md) |
| **Lesson 3** | **Hooks** | **250** | `.kiro/hooks/*.json` with `version: "v1"`, `trigger` (`PostFileSave`), `matcher`, and `action` | [post-save-jev-guard.json](./examples/kiro_templates/hooks/post-save-jev-guard.json) |
| **Lesson 4** | **Property-Based Testing (IDE)** | **500** | `tests/property_tests/test_*.py` running invariant checks (e.g. `hypothesis` / fuzzing properties) | [test_vbc_jev_properties.py](./examples/kiro_templates/tests/test_vbc_jev_properties.py) |
| **Lesson 5** | **Powers** | **500** | Installed/active Kiro Power with `plugin.json`, `skills/<name>/SKILL.md`, and `mcp.json` | [plugin.json](./examples/kiro_templates/power/plugin.json) |
| **Lesson 6** | **Model Context Protocol (MCP)** | **1,000** | `.kiro/mcp.json` (or workspace `mcp.json`) registering `mcpServers` (`architectos-jev`) | [mcp.json](./examples/kiro_templates/mcp.json) |
| **Lesson 7** | **Custom Agents** | **1,000** | `.kiro/agents/*.json` defining `name`, `tools`, `resources`, `permissions.rules`, `prompt`, `model` | [architect-pulse-agent.json](./examples/kiro_templates/agents/architect-pulse-agent.json) |
| **Completion** | **All 7 Lessons Combined** | **1,000** | Automatic bonus when Lessons 1–7 are all verified in the final repo | — |
| **Bonus 1** | **Kiro Web & Cloud Sessions** | **250** | *(Paid tier)* Sync local `.kiro` to Kiro Cloud Configuration & run a Cloud Session | [Syllabus Guide](./references/syllabus_and_grading_rubric.md) |
| **Bonus 2** | **Package a Kiro Power** | **250** | *(All tiers)* Custom power directory at repo root (`architectos-jev-power/plugin.json`) | [plugin.json](./examples/kiro_templates/power/plugin.json) |
| **TOTAL** | **Maximum Possible Award** | **5,250** | **Full Compliance + All 7 Core + 2 Bonuses** | — |

---

## 3. Non-Negotiable Disqualification Safeguards

Before submitting, always verify these 6 strict rules from the official Terms & Conditions:
1. **First Git Commit Date:** The repository's very first commit **MUST be on or after Monday, September 21, 2026 (09:00 PT)**. Never reuse an older Git repo history—always `git init` a fresh repository for the challenge!
2. **Code Freeze During Judging:** Zero GitHub commits are permitted after **October 5, 2026 at 23:59 PT** until judging finishes (**October 19, 2026** or award email receipt).
3. **GitHub Account Age:** Your GitHub account must be at least **3 months old** and publicly match your social identity.
4. **Demo Video Length:** Strictly **30 seconds to 3 minutes (3:00 max)**. Judges stop watching at 3:00. Show both the working app and the `.kiro/` setup.
5. **Social Post Requirements:** Public post on **X** (tag `@kirodotdev`) or **LinkedIn** (tag `@kiro`) with **both** `#KiroUniversity` and `#BuildWithKiro`, a 2–3 sentence description, your public GitHub URL, and demo video link.
6. **Submission Write-Up:** Submit via `https://kiro.dev/2026/university` with a structured write-up detailing how each of the 7 lessons + 2 bonuses was used (use the ready-made template in [syllabus_and_grading_rubric.md](./references/syllabus_and_grading_rubric.md)).

---

## 4. Progressive Disclosure Reference Guides

Read these detailed reference files when executing specific phases of the project:
- **[Syllabus, Daily Lessons & Submission Write-Up Template](./references/syllabus_and_grading_rubric.md)**: Complete day-by-day rules, verification criteria, and copy-paste submission form write-up.
- **[Jev (System 1) + ArchitectOS (System 2) + Kiro Architecture](./references/jev_architectos_architecture.md)**: How to wire Jev (`Choice`, `Score`, `Noul`) into ArchitectOS's `BlueprintVerifier` (`VBC-01..08`), Kiro `PostFileSave` Hooks, and MCP tools.
- **[Winning Projects Playbook (Past AWS & Kiro Winners)](./references/winning_projects_playbook.md)**: Key architectural patterns from *CirKit*, *ChanseyCare*, *InteractionKit*, *Upload Drive-In*, *Denarii*, *KiroSpecGuard*, and *Splice*.
