---
inclusion: fileMatch
fileMatchPattern: "**/*.tsx"
---

# Steering Example 05: React Telemetry UI — System-1 (Jev) vs. System-2 (ArchitectOS)

## 1. Convention & Standard to Enforce
Every dashboard component displaying verification or agent status MUST visually distinguish:
1. **System-1 (Jev Guardrail Telemetry):** Emerald/Purple badge displaying `Noul Probability`, `VBC Score %`, `Routed Specialist`, and sub-200ms latency (`e.g., 14.2 ms`).
2. **System-2 (ArchitectOS 8-Specialist Pipeline):** Step-by-step discipline progress bar with `Human Architect Gate` approval controls.

## 2. Intent & Context
Judges watching the 3-minute demo video need immediate visual proof of how **Jev (System 1)** and **ArchitectOS (System 2)** work together inside Kiro. Displaying live latency and VBC badges makes the architectural value unmistakable in under 10 seconds.

## 3. Code Comparison

### ❌ Non-Compliant (Opaque Generic Status Text)
```tsx
export const StatusBanner = ({ score }: { score: number }) => (
  <div>Score: {score}</div>
);
```

### ✅ Compliant (Explicit System-1 Jev & System-2 ArchitectOS Telemetry Badges)
```tsx
export const TelemetryBanner = ({ noulProb, vbcScore, latencyMs, specialist }: TelemetryProps) => (
  <div className="flex items-center gap-4 rounded-xl border border-purple-500/30 bg-slate-900 p-4 text-slate-100">
    <span className="rounded bg-purple-600/20 px-2.5 py-1 font-mono text-xs text-purple-300">
      ⚡ System-1 Jev Noul: {(noulProb * 100).toFixed(1)}% ({latencyMs}ms)
    </span>
    <span className="rounded bg-emerald-600/20 px-2.5 py-1 font-mono text-xs text-emerald-300">
      🛡️ System-2 VBC Coverage: {vbcScore.toFixed(1)}%
    </span>
    <span className="font-mono text-xs text-slate-400">
      Router Choice: {specialist}
    </span>
  </div>
);
```
