---
inclusion: fileMatch
fileMatchPattern: "**/api/**/*.py"
---

# Steering Example 03: FastAPI OAuth2 JWT & Rate-Limiting Guardrails (`VBC-03`)

## 1. Convention & Standard to Enforce
Every FastAPI route handling state mutations or multi-agent execution MUST declare:
1. OAuth2 Bearer JWT authentication dependency (`Depends(require_jwt_bearer)`).
2. Per-tenant rate-limiting dependency (`Depends(enforce_rate_limit_100_rpm)`).
3. Explicit OpenAPI `responses={401: ..., 403: ..., 429: ...}` metadata so `BlueprintVerifier` rule `VBC-03` and `VBC-07` pass 100% of the time.

## 2. Intent & Context
Rule `VBC-03` treats any unauthenticated or unthrottled public route as a **Critical Security Finding**, immediately capping the readiness score at $\le 78\%$ and blocking release signoff.

## 3. Code Comparison

### ❌ Non-Compliant (Triggers VBC-03 Critical Security Failure)
```python
@router.post("/api/session/start")
def start_session(req: StartSessionRequest):
    # Missing OAuth2 Bearer token and 429 rate limiting
    return create_new_session(req.idea)
```

### ✅ Compliant (Satisfies VBC-03 & VBC-07 Negative Status Contract)
```python
@router.post(
    "/api/session/start",
    summary="Start 8-specialist blueprint session (FR-201, COMP-COORDINATOR, VBC-03)",
    responses={
        401: {"description": "Missing or expired OAuth2 Bearer JWT"},
        403: {"description": "Tenant scope mismatch"},
        429: {"description": "Rate limit exceeded (100 req/min)"},
    },
)
def start_session(
    req: StartSessionRequest,
    principal: TenantPrincipal = Depends(require_jwt_and_rate_limit),
):
    return create_new_session(req.idea, tenant_id=principal.tenant_id)
```
