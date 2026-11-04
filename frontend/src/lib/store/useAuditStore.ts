import { create } from "zustand";

interface AuditState {
    activeClauseId: string | null;
    setActiveClauseId: (clauseId: string | null) => void;
    jumpToClause: (clauseNumber: string) => void;
}

const HIGHLIGHT_CLASS = "clause-jump-highlight";
const HIGHLIGHT_MS = 2500;

/**
 * Bi-directional jump between the compliance matrix and the document viewer
 * (frontend-standards skill §2). Clause DOM ids follow `clause-<number>` (DESIGN.md §4).
 */
export const useAuditStore = create<AuditState>((set) => ({
    activeClauseId: null,
    setActiveClauseId: (clauseId) => set({ activeClauseId: clauseId }),
    jumpToClause: (clauseNumber) => {
        set({ activeClauseId: clauseNumber });
        const element = document.getElementById(`clause-${clauseNumber}`);
        if (!element) return;
        element.scrollIntoView({ behavior: "smooth", block: "center" });
        element.classList.add(HIGHLIGHT_CLASS);
        window.setTimeout(() => element.classList.remove(HIGHLIGHT_CLASS), HIGHLIGHT_MS);
    },
}));
