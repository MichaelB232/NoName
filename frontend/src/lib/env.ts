import { z } from "zod";

/**
 * Public (browser-safe) configuration. Only NEXT_PUBLIC_* values belong here,
 * and they must never contain secrets. Next.js inlines them at build time,
 * so each one must be referenced explicitly (no dynamic `process.env[key]`).
 */
const publicEnvSchema = z.object({
    NEXT_PUBLIC_API_BASE_URL: z.string().url(),
});

export const publicEnv = publicEnvSchema.parse({
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
});
