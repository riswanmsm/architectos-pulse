# Lesson 1 • Example 05: Model Context Protocol (MCP) JSON-RPC 2.0 Bridge

**Spec ID:** `SPEC-L1-EX05`  
**Component Target:** `COMP-MCP-BRIDGE` (`backend/app/mcp/server.py`, `backend/app/mcp/tool_registry.py`)  
**Database Entity:** `ENT-MCP-TRACE` (`mcp_tool_invocations`)

---

## 1. Requirements (`requirements.md` — EARS Notation)

### FR-501: MCP Tool Discovery (`tools/list`)
```text
WHEN Kiro IDE, Kiro CLI, or a Custom Agent sends a JSON-RPC 2.0 `tools/list` request to `/api/mcp/jsonrpc`
THE SYSTEM SHALL return the complete JSON Schema registry for `architectos_generate_blueprint`, `architectos_verify_spec`, `architectos_audit_risk`, `jev_verify_code_drift`, and `jev_route_specialist`.
```

### FR-502: Synchronous MCP Tool Execution (`tools/call`)
```text
WHEN an MCP client invokes `tools/call` with a registered tool `name` and valid `arguments`
THE SYSTEM SHALL execute the target System-1 (Jev) or System-2 (ArchitectOS) handler and return a structured MCP `result.content` array alongside typed telemetry metadata.
```

### FR-503: Parameter Elicitation on Underspecified Prompts
```text
IF a user invokes `architectos_generate_blueprint` with an empty or ambiguous `idea` string (`len(idea.strip()) < 10`)
THEN THE SYSTEM SHALL return an elicitation prompt requesting the target domain, primary user persona, and compliance tier before launching the 8-specialist committee.
```

### FR-504: Standard JSON-RPC 2.0 Error Handling
```text
IF an MCP client calls an unrecognized `method` or invalid tool name
THEN THE SYSTEM SHALL return a compliant JSON-RPC 2.0 error object with code `-32601` (`Method not found`) or `-32603` (`Internal error`) without crashing the server worker.
```

---

## 2. Technical Design (`design.md`)
- **Protocol:** JSON-RPC 2.0 over HTTP POST (`/api/mcp/jsonrpc`) and REST discovery (`/api/mcp/tools`).
- **Workspace Config:** Registered in `.kiro/mcp.json` and `architectos-jev-power/mcp.json`.

## 3. Implementation Tasks (`tasks.md`)
- [x] `TASK-501` (`FR-501`): Register all 5 System-1 & System-2 tools in `MCP_TOOLS`.
- [x] `TASK-502` (`FR-502`): Implement `handle_jsonrpc()` dispatcher in `server.py`.
- [x] `TASK-503` (`FR-503`): Add input validation and elicitation guidance on short ideas.
- [x] `TASK-504` (`FR-504`): Add negative JSON-RPC error code assertions (`-32601`, `-32603`).
