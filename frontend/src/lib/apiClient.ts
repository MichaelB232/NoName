import { publicEnv } from "./env";

/** Mirrors the backend response envelope (.agents/AGENTS.md §2.A). */
export interface ApiSuccess<T> {
    success: true;
    data: T;
    message: string;
}

export interface ApiFailure {
    success: false;
    error: { code: string; message: string; details: unknown[] };
}

export class ApiError extends Error {
    constructor(
        public readonly code: string,
        message: string,
        public readonly status: number,
        public readonly details: unknown[] = [],
    ) {
        super(message);
        this.name = "ApiError";
    }
}

/**
 * Browser fetch wrapper. Sends the httpOnly session cookie automatically
 * (`credentials: "include"`) — the frontend never stores tokens itself.
 */
export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await fetch(`${publicEnv.NEXT_PUBLIC_API_BASE_URL}${path}`, {
        ...init,
        credentials: "include",
        headers: { "Content-Type": "application/json", ...init.headers },
    });

    const body = (await response.json()) as ApiSuccess<T> | ApiFailure;
    if (!body.success) {
        throw new ApiError(body.error.code, body.error.message, response.status, body.error.details);
    }
    return body.data;
}
