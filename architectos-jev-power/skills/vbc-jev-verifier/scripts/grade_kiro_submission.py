#!/usr/bin/env python3
"""
Automated Self-Grader & Compliance Auditor for the Kiro University Challenge (Up to 5,250 Credits).
Inspects a repository for all 7 Required Lessons + 2 Bonus Lessons + Git commit date compliance.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def check_git_compliance(repo_path: Path) -> dict:
    """Verifies that git is initialized and the first commit is on or after 2026-09-21."""
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        return {
            "passed": False,
            "message": "No .git repository initialized yet (run `git init` and commit on/after Sept 21, 2026).",
        }
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo_path), "log", "--reverse", "--format=%cI"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if not out:
            return {"passed": True, "message": "Git initialized (no commits yet; first commit will be compliant)."}
        first_commit_iso = out.splitlines()[0]
        first_dt = datetime.fromisoformat(first_commit_iso)
        cutoff = datetime(2026, 9, 21, 0, 0, 0, tzinfo=timezone.utc)
        is_valid = first_dt.astimezone(timezone.utc) >= cutoff
        return {
            "passed": is_valid,
            "message": f"First commit timestamp: {first_commit_iso} ({'COMPLIANT >= 2026-09-21' if is_valid else 'DISQUALIFICATION RISK: Commit before 2026-09-21!'})",
        }
    except Exception as e:
        return {"passed": False, "message": f"Git check warning: {e}"}


def grade_repository(repo: Path) -> dict:
    results = []
    earned_core = 0
    core_lessons_passed = 0

    # Lesson 1: Spec-Driven Development (250 credits)
    specs_dir = repo / ".kiro" / "specs"
    spec_files = list(specs_dir.glob("*.md")) + list(specs_dir.glob("*.sql")) + list(specs_dir.glob("*.yaml")) if specs_dir.exists() else []
    has_ears = False
    for sf in spec_files:
        txt = sf.read_text(encoding="utf-8", errors="ignore")
        if "WHEN " in txt and "THE SYSTEM SHALL" in txt:
            has_ears = True
            break
    l1_pass = len(spec_files) >= 1 and has_ears
    l1_credits = 250 if l1_pass else 0
    earned_core += l1_credits
    if l1_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 1",
        "title": "Spec-Driven Development (EARS syntax in .kiro/specs/)",
        "max_credits": 250,
        "earned": l1_credits,
        "passed": l1_pass,
        "evidence": f"Found {len(spec_files)} spec file(s), EARS syntax={'Yes' if has_ears else 'No'}",
    })

    # Lesson 2: Steering Documents (250 credits)
    steering_dir = repo / ".kiro" / "steering"
    steering_files = list(steering_dir.glob("*.md")) if steering_dir.exists() else []
    has_frontmatter = False
    for stf in steering_files:
        txt = stf.read_text(encoding="utf-8", errors="ignore")
        if txt.startswith("---") and "inclusion:" in txt:
            has_frontmatter = True
            break
    l2_pass = len(steering_files) >= 1 and has_frontmatter
    l2_credits = 250 if l2_pass else 0
    earned_core += l2_credits
    if l2_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 2",
        "title": "Steering Documents (.kiro/steering/*.md with YAML frontmatter)",
        "max_credits": 250,
        "earned": l2_credits,
        "passed": l2_pass,
        "evidence": f"Found {len(steering_files)} steering file(s), YAML inclusion frontmatter={'Yes' if has_frontmatter else 'No'}",
    })

    # Lesson 3: Hooks (250 credits)
    hooks_dir = repo / ".kiro" / "hooks"
    hook_files = list(hooks_dir.glob("*.json")) if hooks_dir.exists() else []
    valid_hook = False
    for hf in hook_files:
        try:
            data = json.loads(hf.read_text(encoding="utf-8"))
            if "hooks" in data and len(data["hooks"]) > 0 and "trigger" in data["hooks"][0]:
                valid_hook = True
                break
        except Exception:
            pass
    l3_pass = valid_hook
    l3_credits = 250 if l3_pass else 0
    earned_core += l3_credits
    if l3_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 3",
        "title": "Hooks (.kiro/hooks/*.json event automation)",
        "max_credits": 250,
        "earned": l3_credits,
        "passed": l3_pass,
        "evidence": f"Found {len(hook_files)} hook config(s), valid schema={'Yes' if valid_hook else 'No'}",
    })

    # Lesson 4: Property-Based Testing (500 credits)
    pbt_dir = repo / "tests" / "property_tests"
    pbt_files = list(pbt_dir.glob("test_*.py")) if pbt_dir.exists() else list(repo.rglob("*property*.py"))
    l4_pass = len(pbt_files) >= 1
    l4_credits = 500 if l4_pass else 0
    earned_core += l4_credits
    if l4_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 4",
        "title": "Property-Based Testing (Kiro IDE invariant test suite)",
        "max_credits": 500,
        "earned": l4_credits,
        "passed": l4_pass,
        "evidence": f"Found {len(pbt_files)} property test suite(s)",
    })

    # Lesson 5: Powers (500 credits)
    plugin_files = list(repo.rglob("plugin.json"))
    l5_pass = len(plugin_files) >= 1
    l5_credits = 500 if l5_pass else 0
    earned_core += l5_credits
    if l5_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 5",
        "title": "Kiro Powers (Dynamic keyword-activated power & skills)",
        "max_credits": 500,
        "earned": l5_credits,
        "passed": l5_pass,
        "evidence": f"Found {len(plugin_files)} power manifest(s)",
    })

    # Lesson 6: Model Context Protocol (MCP) (1,000 credits)
    mcp_candidates = [repo / ".kiro" / "mcp.json", repo / "mcp.json"] + list(repo.rglob("mcp.json"))
    valid_mcp = False
    for mc in mcp_candidates:
        if mc.exists():
            try:
                data = json.loads(mc.read_text(encoding="utf-8"))
                if "mcpServers" in data and len(data["mcpServers"]) > 0:
                    valid_mcp = True
                    break
            except Exception:
                pass
    l6_pass = valid_mcp
    l6_credits = 1000 if l6_pass else 0
    earned_core += l6_credits
    if l6_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 6",
        "title": "Model Context Protocol (MCP server registered in mcp.json)",
        "max_credits": 1000,
        "earned": l6_credits,
        "passed": l6_pass,
        "evidence": f"Valid mcpServers config={'Yes' if valid_mcp else 'No'}",
    })

    # Lesson 7: Custom Agents (1,000 credits)
    agents_dir = repo / ".kiro" / "agents"
    agent_files = list(agents_dir.glob("*.json")) if agents_dir.exists() else []
    valid_agent = False
    for af in agent_files:
        try:
            data = json.loads(af.read_text(encoding="utf-8"))
            if "name" in data and "tools" in data and "permissions" in data:
                valid_agent = True
                break
        except Exception:
            pass
    l7_pass = valid_agent
    l7_credits = 1000 if l7_pass else 0
    earned_core += l7_credits
    if l7_pass:
        core_lessons_passed += 1
    results.append({
        "id": "Lesson 7",
        "title": "Custom Agents (.kiro/agents/*.json with tools, permissions, resources)",
        "max_credits": 1000,
        "earned": l7_credits,
        "passed": l7_pass,
        "evidence": f"Found {len(agent_files)} custom agent definition(s), valid={'Yes' if valid_agent else 'No'}",
    })

    # Completion Bonus: All 7 Required Lessons (1,000 credits)
    all_7_pass = core_lessons_passed == 7
    comp_credits = 1000 if all_7_pass else 0
    results.append({
        "id": "Completion Award",
        "title": "All 7 Required Lessons Demonstrated in Final Build",
        "max_credits": 1000,
        "earned": comp_credits,
        "passed": all_7_pass,
        "evidence": f"{core_lessons_passed}/7 core lessons passed",
    })

    # Bonus Lesson 1: Cloud Sessions & Cloud Config (250 credits)
    cloud_doc = (repo / ".kiro" / "cloud-config.json").exists() or (repo / "docs" / "CLOUD_SESSION_SYNC.md").exists()
    b1_credits = 250 if cloud_doc else 0
    results.append({
        "id": "Bonus Lesson 1",
        "title": "Kiro Web, Cloud Sessions & Cloud Configuration (Paid plans)",
        "max_credits": 250,
        "earned": b1_credits,
        "passed": cloud_doc,
        "evidence": f"Cloud configuration bundle present={'Yes' if cloud_doc else 'No'}",
    })

    # Bonus Lesson 2: Package a Custom Kiro Power (250 credits)
    valid_custom_power = False
    for pf in plugin_files:
        try:
            data = json.loads(pf.read_text(encoding="utf-8"))
            if "agent-plugins.org" in data.get("$schema", "") and "keywords" in data:
                valid_custom_power = True
                break
        except Exception:
            pass
    b2_credits = 250 if valid_custom_power else 0
    results.append({
        "id": "Bonus Lesson 2",
        "title": "Package a Kiro Power (plugin.json with agent-plugins.org schema)",
        "max_credits": 250,
        "earned": b2_credits,
        "passed": valid_custom_power,
        "evidence": f"Schema-valid custom Kiro Power={'Yes' if valid_custom_power else 'No'}",
    })

    total_earned = earned_core + comp_credits + b1_credits + b2_credits
    git_check = check_git_compliance(repo)

    return {
        "repo": str(repo),
        "total_earned": total_earned,
        "max_possible": 5250,
        "core_lessons_passed": core_lessons_passed,
        "git_compliance": git_check,
        "breakdown": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Grade a repository against the 5,250-credit Kiro University Challenge rubric.")
    parser.add_argument("--repo", required=True, help="Path to the repository root to evaluate.")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        print(f"Error: Path {repo_path} does not exist.")
        sys.exit(1)

    report = grade_repository(repo_path)
    print("=" * 78)
    print(f"🎓 KIRO UNIVERSITY CHALLENGE SELF-GRADER REPORT")
    print(f"Repository: {report['repo']}")
    print("=" * 78)
    for item in report["breakdown"]:
        status = "✅ PASS" if item["passed"] else "❌ MISS"
        print(f"{status} | {item['id']:<16} | {item['earned']:>4} / {item['max_credits']:<4} cr | {item['title']}")
        print(f"       └─ Evidence: {item['evidence']}")
    print("-" * 78)
    git_icon = "✅" if report["git_compliance"]["passed"] else "⚠️"
    print(f"{git_icon} Git Compliance: {report['git_compliance']['message']}")
    print("=" * 78)
    print(f"🏆 PROJECTED FINAL SCORE: {report['total_earned']:,} / {report['max_possible']:,} KIRO CREDITS")
    print("=" * 78)


if __name__ == "__main__":
    main()
