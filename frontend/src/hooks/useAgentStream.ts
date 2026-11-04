"use client";

import { useEffect, useState } from "react";
import { z } from "zod";
import { publicEnv } from "@/lib/env";

const progressEventSchema = z.object({
    current_node: z.string(),
    progress: z.number().min(0).max(100),
    status: z.enum(["RUNNING", "COMPLETED", "FAILED"]),
    message: z.string().optional(),
});

export type AgentProgressEvent = z.infer<typeof progressEventSchema>;

/**
 * Subscribes to the backend SSE relay for one contract's audit progress
 * (frontend-standards skill §3). Events are validated before use.
 */
export function useAgentStream(contractId: string | null): AgentProgressEvent | null {
    const [event, setEvent] = useState<AgentProgressEvent | null>(null);

    useEffect(() => {
        if (!contractId) return;
        const source = new EventSource(`${publicEnv.NEXT_PUBLIC_API_BASE_URL}/contracts/${contractId}/stream`, {
            withCredentials: true,
        });

        source.onmessage = (message: MessageEvent<string>) => {
            const parsed = progressEventSchema.safeParse(JSON.parse(message.data));
            if (!parsed.success) return;
            setEvent(parsed.data);
            if (parsed.data.status !== "RUNNING") source.close();
        };
        source.onerror = () => source.close();

        return () => source.close();
    }, [contractId]);

    return event;
}
