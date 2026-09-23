---
inclusion: fileMatch
fileMatchPattern: "**/*.sql"
---

# Steering Example 04: PostgreSQL DDL & Relational Entity Integrity (`VBC-04`)

## 1. Convention & Standard to Enforce
All SQL schema files (`.kiro/specs/schema.sql` and migrations) MUST:
1. Precede every table with a `-- Entity: ENT-X (<Description>)` comment header.
2. Use `UUID PRIMARY KEY DEFAULT gen_random_uuid()`.
3. Include `tenant_id UUID NOT NULL` with a `FOREIGN KEY ... ON DELETE CASCADE` and a composite index `idx_<table>_tenant_created`.
4. Include `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`.

## 2. Intent & Context
`BlueprintVerifier.extract_entities()` (`VBC-04`) parses `ENT-X` identifiers and `CREATE TABLE` statements to verify that every API payload maps to a concrete relational table with multi-tenant isolation.

## 3. Code Comparison

### ❌ Non-Compliant (No ENT-X Header, Integer ID, Missing Tenant Isolation)
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    idea TEXT
);
```

### ✅ Compliant (Enforces VBC-04 Entity Traceability & Tenant Isolation)
```sql
-- Entity: ENT-1 (Multi-Tenant Blueprint Sessions)
CREATE TABLE IF NOT EXISTS blueprint_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    idea_prompt TEXT NOT NULL,
    vbc_score NUMERIC(5,2) NOT NULL DEFAULT 0.0,
    readiness_score INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_blueprint_sessions_tenant_created
    ON blueprint_sessions (tenant_id, created_at DESC);
```
