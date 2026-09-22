---
inclusion: always
---

# ArchitectOS & Jev System-1/System-2 Engineering Standards

## 1. Convention & Standard to Enforce
Every feature, API route, database schema, and verification module generated or modified by Kiro MUST strictly satisfy **Verified Blueprint Coverage (`VBC-01` through `VBC-07`)** and route all fast guardrails through the **Jev System-1 Decision Interface** (`noul`, `score`, `choice`).

Specifically:
1. **EARS Traceability (`VBC-01`, `VBC-02`):** Every module docstring and API endpoint must reference its upstream functional requirement (`FR-X`), component (`COMP-X`), and verification test (`TEST-X`).
2. **Zero Unauthenticated Protected Routes (`VBC-03`):** Every state-mutating REST/JSON-RPC route must declare OAuth2/JWT Bearer security and rate-limiting (`401`/`403`/`429` negative test coverage).
3. **Typed System-1 Guardrail Outputs:** All Jev System-1 calls (`noul`, `score`, `choice`) must return strictly bounded, typed dictionaries (`probability` $\in [0.0, 1.0]$, `score` $\in [0.0, 100.0]$, `choice` $\in \text{valid\_options}$) with a deterministic offline fallback so tests never fail without network access.

---

## 2. Engineering Intent & Context
In multi-agent software engineering, unconstrained LLM code generation suffers from the **"Fluent Hallucination" Trap**: code looks syntactically valid in isolation, but silently diverges from `.kiro/specs/requirements.md`, `.kiro/specs/schema.sql`, and `.kiro/specs/api.yaml`. By enforcing explicit `FR-X`/`COMP-X`/`ENT-X` markers and running sub-200ms Jev System-1 checks on every file save, Kiro catches architectural drift and missing authentication *before* code is committed.

---

## 3. Code Comparison (Compliant vs. Non-Compliant)

### ❌ Non-Compliant (Missing VBC Traceability, Auth Controls & Bounds)
```python
@router.post("/blueprint/deploy")
def deploy_blueprint(payload: dict):
    # Bad: No FR-X traceability, no auth/rate-limit guard, untyped output
    return {"status": "deployed"}
```

### ✅ Compliant (Enforces VBC-01, VBC-03, and Jev System-1 Verification)
```python
@router.post(
    "/blueprint/deploy",
    summary="Deploy verified blueprint (FR-1, COMP-3, TEST-1)",
    responses={401: {"description": "Unauthorized JWT"}, 429: {"description": "Rate limit exceeded"}},
)
def deploy_blueprint(
    payload: DeployRequest,
    auth_token: str = Depends(verify_jwt_bearer_and_rate_limit),
) -> DeployResponse:
    """
    Implements FR-1 & VBC-03: Verifies Jev System-1 Noul gate before deployment.
    """
    jev_gate = JevSystemOneEngine.noul(
        spec_text=payload.requirements_ears,
        code_or_artifact=payload.api_yaml,
        invariant_prompt="Does api.yaml enforce OAuth2 Bearer JWT and rate limiting?",
    )
    if jev_gate["probability"] < 0.85:
        raise HTTPException(status_code=422, detail=f"Jev System-1 Gate blocked deployment: {jev_gate['reason']}")
    return DeployResponse(status="deployed", vbc_score=jev_gate["vbc_score"])
```
