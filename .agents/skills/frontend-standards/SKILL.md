---
name: frontend-standards
description: >-
  Use this skill when developing frontend features in Next.js 15, managing client state with Zustand, handling Server-Sent Events (SSE) streaming, or building the split-screen document viewer.
---

# Frontend Architecture & Standards
**Framework:** Next.js 15 (App Router, React 19, TypeScript)  
**State Management:** Zustand (Client UI & Active Clause Tracking) + TanStack Query (Server State)  
**Streaming:** Server-Sent Events (SSE) for Real-Time Agent Progress  
**Document Workspace:** Split-Screen Synchronized Canvas (Tiptap / Lexical + Audit Matrix)

---

## 1. Directory Structure

```
frontend/src/
├── app/
│   ├── (auth)/                  # Login, Register, Org Select
│   ├── (dashboard)/             # Main Authenticated Shell
│   │   ├── contracts/
│   │   │   ├── page.tsx         # Contract List & Upload Dialog
│   │   │   └── [id]/
│   │   │       └── page.tsx     # Split-Screen Audit Canvas
│   │   └── layout.tsx
├── components/
│   ├── ui/                      # shadcn/ui primitives
│   ├── canvas/                  # Split-Screen document viewer & editor
│   │   ├── document-viewer.tsx
│   │   ├── audit-matrix-panel.tsx
│   │   └── diff-redline-modal.tsx
│   └── agent/
│       └── live-agent-stepper.tsx # Real-time SSE Agent progress
├── lib/
│   ├── api-client.ts            # Fetch wrapper with auto CSRF & cookie handling
│   └── store/
│       └── use-audit-store.ts   # Zustand active clause & highlight sync
```

---

## 2. Split-Screen Bi-Directional Jump State (Zustand)

When a user clicks on an audit finding in the right-hand panel, the left-hand document viewer must smoothly scroll and highlight the exact corresponding clause:

```typescript
// frontend/src/lib/store/use-audit-store.ts
import { create } from "zustand";

interface AuditState {
    activeClauseId: string | null;
    setActiveClauseId: (clauseId: string | null) => void;
    jumpToClause: (clauseNumber: string) => void;
}

export const useAuditStore = create<AuditState>((set) => ({
    activeClauseId: null,
    setActiveClauseId: (id) => set({ activeClauseId: id }),
    jumpToClause: (clauseNumber) => {
        set({ activeClauseId: clauseNumber });
        const element = document.getElementById(`clause-${clauseNumber}`);
        if (element) {
            element.scrollIntoView({ behavior: "smooth", block: "center" });
            element.classList.add("bg-amber-100", "dark:bg-amber-950/40");
            setTimeout(() => {
                element.classList.remove("bg-amber-100", "dark:bg-amber-950/40");
            }, 2500);
        }
    },
}));
```

---

## 3. Server-Sent Events (SSE) Agent Streaming Consumer

```typescript
// frontend/src/components/agent/use-agent-stream.ts
import { useEffect, useState } from "react";

export function useAgentStream(contractId: string) {
    const [agentStep, setAgentStep] = useState<string>("INITIALIZING");
    const [progressPercent, setProgressPercent] = useState<number>(0);

    useEffect(() => {
        const eventSource = new EventSource(`/api/v1/contracts/${contractId}/stream`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setAgentStep(data.current_node); // e.g. 'auditor_rag', 'risk_evaluator'
            setProgressPercent(data.progress);
            if (data.status === "COMPLETED") {
                eventSource.close();
            }
        };

        eventSource.onerror = () => {
            eventSource.close();
        };

        return () => eventSource.close();
    }, [contractId]);

    return { agentStep, progressPercent };
}
```
