---
inclusion: fileMatch
fileMatchPattern: "**/*jev*.py"
---

# Steering Example 02: Jev System-1 Typed Decision Contracts (`Noul`, `Score`, `Choice`)

## 1. Convention & Standard to Enforce
All Jev System-1 guardrail functions MUST return strictly typed dictionaries enforcing:
1. `noul_probability` clamped strictly to `float` in $[0.0, 1.0]$.
2. `vbc_score` clamped strictly to `float` in $[0.0, 100.0]$.
3. `routed_choice` strictly validated against the allowed specialist enum set.
4. A zero-dependency deterministic offline fallback whenever `JEV_API_KEY` is unset.

## 2. Intent & Context
Jev acts as our sub-200ms System-1 gate inside `.kiro/hooks/`. If a Jev call raises an unhandled network exception or returns an out-of-range probability, Kiro `PostFileSave` hooks and `pytest` property tests will break in offline CI/judging environments.

## 3. Code Comparison

### ❌ Non-Compliant (Unclamped Floats & Hard API Key Dependency)
```python
def check_drift(spec: str, code: str) -> float:
    # Fails in offline judging environments if JEV_API_KEY is missing!
    resp = requests.post("https://api.typesafe.ai/jev/noul", headers={"Authorization": os.environ["JEV_API_KEY"]})
    return resp.json()["prob"]
```

### ✅ Compliant (Clamped Bounds + Deterministic Offline Fallback)
```python
def check_drift(spec: str, code: str) -> dict:
    """Implements FR-101 & FR-104: Clamped System-1 Noul + deterministic fallback."""
    raw_prob = evaluate_heuristic_or_jev_api(spec, code)
    clamped_prob = round(min(1.0, max(0.0, float(raw_prob))), 4)
    return {
        "noul_probability": clamped_prob,
        "compliant": clamped_prob >= 0.85,
        "routed_choice": "none" if clamped_prob >= 0.85 else "risk_engineering",
    }
```
