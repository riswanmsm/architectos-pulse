# Winning Projects Playbook: Lessons from Recent Kiro & AWS Challenge Winners

## 1. Benchmark Winners Analyzed (2025–2026)

| Project | Challenge & Award | Core Value Proposition | Key Kiro / AWS Pattern |
| :--- | :--- | :--- | :--- |
| **CirKit** | 🏆 *Best Industrial* (KiroHacks / Featured July 2026 Blog) | Converts natural language & PDF schematics into wired breadboards with animated current flow (`VCC` $\to$ `GND`) & safety checks. | Shared `schema.json` contract in `.kiro/specs/`; per-module `.kiro/steering/` files; **Post-response build hooks** yielding 0 broken builds across 55 commits. |
| **ChanseyCare** | 🏆 *1st Place Grand Prize* (KiroHacks / Featured July 2026 Blog) | Voice-activated remote wellness triage bridging home robotics state to live clinician dashboards. | Used Kiro specs to map deterministic JSON state transitions (`help` $\to$ `Needs Help` $\to$ `In Session` $\to$ `Escalated`). |
| **InteractionKit** | 🏆 *Grand Prize Winner* ($100k Kiroween Challenge) | Python SDK wrapping MediaPipe computer vision into plug-and-play hand/head gesture controls. | Built as a meta-tool *for* Kiro developers—using `.kiro/specs` and `.kiro/hooks` to auto-generate gesture handlers. |
| **Upload Drive-In** | 🏆 *1st Place Overall* (Code with Kiro Hackathon) | Self-hosted fault-tolerant enterprise large-file ingestion server. | Solved a universal engineering pain point with clean spec-to-test traceability. |
| **Denarii** | 🥈 *2nd Place Overall* (Code with Kiro Hackathon) | AI financial advisor using a **Weighted Decision Matrix** + **Multi-Criteria Decision Analysis (MCDA)**. | Combined LLM reasoning with explicit mathematical decision scoring (just like **Jev `Score` + `VBC`**). |
| **KiroSpecGuard** | 🏅 *Category Winner* (Code with Kiro Hackathon) | "Security seatbelt for Kiro" catching vulnerabilities on save and generating audit reports. | Directly mirrors **ArchitectOS Pulse**'s pre-flight risk audit (`VBC-03`) and `PostFileSave` hooks. |
| **Splice** | 🏅 *Category Winner* (Kiroween Challenge) | Turns OpenAPI specs into live mock servers and production SDKs in seconds. | Tight loop between `.kiro/specs/api.yaml` and runnable code. |

---

## 2. The 5 Rules to Guarantee a Top Score in Kiro University

1. **Make the `.kiro/` Folder the Star of the Repo & Video:**
   - Reviewers specifically inspect your `.kiro/` folder first. In your 2.5-minute demo video, spend the **first 60 seconds** showing the working app, and the **next 90 seconds** walking through `.kiro/specs/`, `.kiro/steering/`, `.kiro/hooks/`, `.kiro/agents/`, `.kiro/mcp.json`, your **Property-Based Tests running in Kiro IDE**, and your packaged `plugin.json` Kiro Power.
2. **Use Formal EARS Syntax in `.kiro/specs/requirements.md`:**
   - Lesson 1 explicitly highlights EARS (`WHEN ... THE SYSTEM SHALL ...`). Every requirement `FR-1`..`FR-8` in your spec should use exact `WHEN / THE SYSTEM SHALL` clauses so reviewers give instant full marks for Lesson 1.
3. **Demonstrate Real Automation in `.kiro/hooks/`:**
   - Don't just put a dummy `echo` command in `.kiro/hooks/`. Have your `PostFileSave` hook invoke the **Jev + ArchitectOS Drift Verifier** script (`python3 scripts/jev_hook_verify.py`) that writes a live status badge or audit log.
4. **Write Genuine Property-Based Tests (Lesson 4 — 500 Credits):**
   - Use Python's `hypothesis` library (plus standard `unittest` compatibility) to test at least **4 universal invariants** (e.g., VBC score monotonicity, security gate rejection of unauthenticated routes, Jev `Noul` probability bounds $\in [0, 1]$, and EARS parser idempotency).
5. **Bundle Your Project as an Installable Kiro Power (Bonus 2 — 250 Credits):**
   - Include `architectos-jev-power/plugin.json` with `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"` so your project qualifies for both Lesson 5 (500 credits) and Bonus Lesson 2 (250 credits).
