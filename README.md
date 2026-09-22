# ArchitectOS Pulse 🎓⚡

**System-1 (Jev) & System-2 (ArchitectOS) Spec-to-Code Drift Guardrail & Autonomous Blueprint Engine for the Kiro University Challenge (Up to 5,250 Credits)**

---

## 🏗️ Repository Structure & Kiro University Challenge Mapping

This repository is initialized with the complete **Kiro + Jev + ArchitectOS Skill & Power Suite**, covering all **7 Required Lessons + 2 Bonus Lessons**:

```text
architectos-pulse/
├── .agents/
│   ├── plugins/architectos-jev-pulse/plugin.json        # Workspace Agent Plugin
│   └── skills/kiro-university-challenge/                # Complete Reusable Challenge Skill
│       ├── SKILL.md
│       ├── references/
│       ├── examples/kiro_templates/
│       └── scripts/
├── .kiro/
│   ├── specs/                                           # Lesson 1 (250 cr): EARS Spec-Driven Development
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── steering/                                        # Lesson 2 (250 cr): Steering Documents
│   │   └── architectos-vbc-standards.md
│   ├── hooks/                                           # Lesson 3 (250 cr): PostFileSave Jev Guardrail Hook
│   │   └── post-save-jev-guard.json
│   ├── agents/                                          # Lesson 7 (1,000 cr): Custom Agent Configuration
│   │   └── architect-pulse-agent.json
│   ├── mcp.json                                         # Lesson 6 (1,000 cr): Model Context Protocol Config
│   └── cloud-config.json                                # Bonus 1 (250 cr): Kiro Cloud Session Sync
├── architectos-jev-power/                               # Lesson 5 (500 cr) & Bonus 2 (250 cr): Custom Kiro Power
│   ├── plugin.json
│   ├── mcp.json
│   └── skills/vbc-jev-verifier/SKILL.md
├── tests/
│   └── property_tests/                                  # Lesson 4 (500 cr): Kiro IDE Property-Based Testing
│       └── test_vbc_jev_properties.py
└── scripts/
    └── jev_hook_verify.py                               # Sub-200ms Jev System-1 Drift & VBC Verifier
```

---

## ⚡ Quick Verification & Self-Grading Commands

```bash
# 1. Run the Lesson 4 Property-Based Test Suite (550+ fuzzing assertions)
python3 tests/property_tests/test_vbc_jev_properties.py -v

# 2. Run the Automated 5,250-Credit Challenge Self-Grader
python3 .agents/skills/kiro-university-challenge/scripts/grade_kiro_submission.py --repo .
```
