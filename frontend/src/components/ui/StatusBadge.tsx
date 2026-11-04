import { cn } from "@/lib/cn";

export type ComplianceStatus = "COMPLIANT" | "VIOLATION" | "AMBIGUOUS" | "REVISED";

const statusStyles: Record<ComplianceStatus, string> = {
    COMPLIANT: "bg-status-compliant-bg text-status-compliant border-status-compliant/20",
    VIOLATION: "bg-status-violation-bg text-status-violation border-status-violation/20",
    AMBIGUOUS: "bg-status-ambiguous-bg text-status-ambiguous border-status-ambiguous/20",
    REVISED: "bg-status-revised-bg text-status-revised border-status-revised/20",
};

/** Muted compliance status badge (design-system skill §1, DESIGN.md §2). */
export function StatusBadge({ status, className }: { status: ComplianceStatus; className?: string }) {
    return (
        <span
            className={cn(
                "inline-flex items-center rounded-full border px-2 py-0.5 font-mono text-[11px] tracking-wide",
                statusStyles[status],
                className,
            )}
        >
            {status}
        </span>
    );
}
