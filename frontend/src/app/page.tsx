import { StatusBadge } from "@/components/ui/StatusBadge";

/** Placeholder landing page proving the design tokens and fonts are wired. */
export default function HomePage() {
    return (
        <main className="flex min-h-screen items-center justify-center p-12">
            <section className="w-full max-w-md rounded-xl border border-hairline bg-surface p-10">
                <p className="font-mono text-xs text-tertiary">§ INSTITUTIONAL LEGAL-TECH VAULT</p>
                <h1 className="mt-3 font-display text-3xl font-medium">Compliance-Agent</h1>
                <p className="mt-2 text-sm text-secondary">Template scaffold — frontend is running.</p>
                <div className="mt-6 flex flex-wrap gap-2">
                    <StatusBadge status="COMPLIANT" />
                    <StatusBadge status="VIOLATION" />
                    <StatusBadge status="AMBIGUOUS" />
                    <StatusBadge status="REVISED" />
                </div>
            </section>
        </main>
    );
}
