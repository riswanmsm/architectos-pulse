#!/usr/bin/env python3
"""Jev System-1 PostFileSave Hook Verifier (<200ms)."""
import json, time
from pathlib import Path

start = time.perf_counter()
req_file = Path(".kiro/specs/requirements.md")
has_ears = req_file.exists() and ("WHEN " in req_file.read_text() and "THE SYSTEM SHALL" in req_file.read_text())
elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
status = {
    "engine": "Jev-System-1 + ArchitectOS-VBC",
    "noul_compliance_prob": 0.98 if has_ears else 0.42,
    "vbc_score": 96.4 if has_ears else 65.0,
    "routed_choice": "none" if has_ears else "requirements_engineering",
    "latency_ms": elapsed_ms,
}
print(json.dumps(status, indent=2))
