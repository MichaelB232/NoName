import "server-only";
import { z } from "zod";

/** Server-only configuration. Importing this from a Client Component fails the build. */
const serverEnvSchema = z.object({
    BACKEND_INTERNAL_URL: z.string().url(),
});

export const serverEnv = serverEnvSchema.parse({
    BACKEND_INTERNAL_URL: process.env.BACKEND_INTERNAL_URL,
});
