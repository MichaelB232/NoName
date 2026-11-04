import { z } from "zod";

/**
 * Single source of truth for runtime configuration.
 *
 * - Every credential comes from the environment; nothing is hardcoded.
 * - Validated once at boot. If anything is missing/invalid the process exits
 *   with a readable list of problems (fail-fast, never run half-configured).
 * - Import `env` everywhere instead of reading `process.env` directly.
 */
const envSchema = z.object({
    NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
    PORT: z.coerce.number().int().positive().default(4000),
    LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace"]).default("info"),
    CORS_ORIGINS: z
        .string()
        .min(1)
        .transform((value) => value.split(",").map((origin) => origin.trim()).filter(Boolean)),

    DATABASE_URL: z.string().url(),
    REDIS_URL: z.string().url(),

    JWT_SECRET: z.string().min(32, "JWT_SECRET must be at least 32 characters"),
    JWT_EXPIRES_IN: z.string().min(1).default("8h"),
    AUTH_COOKIE_NAME: z.string().min(1).default("ca_session"),

    S3_ENDPOINT: z.string().url(),
    S3_REGION: z.string().min(1),
    S3_BUCKET: z.string().min(3),
    S3_ACCESS_KEY_ID: z.string().min(1),
    S3_SECRET_ACCESS_KEY: z.string().min(1),
    S3_FORCE_PATH_STYLE: z
        .enum(["true", "false"])
        .default("true")
        .transform((value) => value === "true"),
    S3_PRESIGN_TTL_SECONDS: z.coerce.number().int().positive().max(600).default(600),
    UPLOAD_MAX_BYTES: z.coerce.number().int().positive().default(26_214_400),

    AGENT_SERVICE_URL: z.string().url(),
    AGENT_SERVICE_TOKEN: z.string().min(32, "AGENT_SERVICE_TOKEN must be at least 32 characters"),
});

export type Env = z.infer<typeof envSchema>;

function loadEnv(): Env {
    const parsed = envSchema.safeParse(process.env);
    if (!parsed.success) {
        const problems = parsed.error.issues
            .map((issue) => `  - ${issue.path.join(".")}: ${issue.message}`)
            .join("\n");
        // Logger is not available yet (it depends on env), so use stderr directly.
        process.stderr.write(`\n[config] Invalid environment configuration:\n${problems}\n\n`);
        process.exit(1);
    }
    return parsed.data;
}

export const env: Env = loadEnv();
