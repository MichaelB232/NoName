---
name: design-system
description: >-
  Use this skill when building or styling UI components, applying compliance status badges and color tokens (Tailwind CSS v4 / shadcn/ui), or structuring the interactive compliance matrix table.
---

# Design System & UI/UX Standards
**CSS Engine:** Tailwind CSS v4  
**Component Library:** Radix UI primitives + shadcn/ui  
**Icons:** Lucide React  
**Theme:** Professional Legal/FinTech (Deep Slate & Muted Amber/Emerald/Rose Status Badges)

---

## 1. Compliance Status Badges & Color Tokens

In legal compliance auditing, clear visual hierarchy prevents audit fatigue:

| Status | Badge Color (Tailwind) | Hex | Meaning |
| :--- | :--- | :--- | :--- |
| **COMPLIANT** | `bg-emerald-500/10 text-emerald-600 border-emerald-500/20` | `#10b981` | Fully aligned with POJK & UU PDP regulations. |
| **VIOLATION** | `bg-rose-500/10 text-rose-600 border-rose-500/20` | `#f43f5e` | Explicit breach of law (e.g., interest > 0.3%/day). |
| **AMBIGUOUS** | `bg-amber-500/10 text-amber-600 border-amber-500/20` | `#f59e0b` | Vague wording, multi-interpretable liability. |
| **REVISED** | `bg-blue-500/10 text-blue-600 border-blue-500/20` | `#3b82f6` | AI redline revision accepted by legal counsel. |

---

## 2. Interactive Compliance Matrix Component Spec

The table component must support:
1. **Interactive Column Headers:** Sorting by Severity (`HIGH` $\rightarrow$ `LOW`), Status, Clause Number.
2. **Clickable Clause Pill:** Jumping to the left-hand original document location.
3. **One-Click Redraft Action:** A direct button `[Review Revision]` opening the side-by-side diff modal.

```tsx
// frontend/src/components/canvas/audit-matrix-row.tsx
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useAuditStore } from "@/lib/store/use-audit-store";

interface RowProps {
    clauseNumber: string;
    topic: string;
    status: "COMPLIANT" | "VIOLATION" | "AMBIGUOUS";
    violatedRegulation?: string;
    penaltyEstimateIdr: number;
    onOpenRedraft: () => void;
}

export function AuditMatrixRow({ clauseNumber, topic, status, violatedRegulation, penaltyEstimateIdr, onOpenRedraft }: RowProps) {
    const jumpToClause = useAuditStore((s) => s.jumpToClause);

    return (
        <tr className="border-b hover:bg-muted/50 transition-colors">
            <td className="p-3 font-mono text-xs">
                <button 
                    onClick={() => jumpToClause(clauseNumber)}
                    className="text-primary hover:underline font-semibold flex items-center gap-1"
                >
                    {clauseNumber}
                </button>
            </td>
            <td className="p-3 font-medium text-sm">{topic}</td>
            <td className="p-3">
                <Badge variant={status === "COMPLIANT" ? "default" : status === "VIOLATION" ? "destructive" : "secondary"}>
                    {status}
                </Badge>
            </td>
            <td className="p-3 text-xs text-muted-foreground">{violatedRegulation || "—"}</td>
            <td className="p-3 font-mono text-xs text-right">
                {penaltyEstimateIdr > 0 ? `Rp ${penaltyEstimateIdr.toLocaleString("id-ID")}` : "Rp 0"}
            </td>
            <td className="p-3 text-right">
                {status !== "COMPLIANT" && (
                    <Button size="sm" variant="outline" onClick={onOpenRedraft}>
                        Review Redline
                    </Button>
                )}
            </td>
        </tr>
    );
}
```

---

## 3. Git-Style Legal Redline Diff View

When reviewing a suggested revision:
* **Original clause text (Removed):** Red background highlight (`bg-rose-500/15 line-through text-rose-700 dark:text-rose-400`).
* **Revised compliant text (Added):** Green background highlight (`bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 font-medium`).
* **Action Buttons:** `[Accept Revision]` (replaces the clause in the active document and marks row as resolved) and `[Reject]`.
