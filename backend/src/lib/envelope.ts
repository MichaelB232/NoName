/**
 * Standard response envelope (.agents/AGENTS.md §2.A).
 * Use these helpers so every endpoint returns the exact same shape.
 */
export interface SuccessEnvelope<T> {
    success: true;
    data: T;
    message: string;
}

export interface ErrorEnvelope {
    success: false;
    error: {
        code: string;
        message: string;
        details: unknown[];
    };
}

export function ok<T>(data: T, message = "OK"): SuccessEnvelope<T> {
    return { success: true, data, message };
}

export function fail(code: string, message: string, details: unknown[] = []): ErrorEnvelope {
    return { success: false, error: { code, message, details } };
}
