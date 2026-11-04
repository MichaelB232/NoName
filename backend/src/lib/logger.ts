import pino from "pino";
import { env } from "../config/env";

/**
 * Structured JSON logger. Pretty-printed in development only.
 * Sensitive fields are redacted so tokens/passwords never reach log storage.
 */
export const logger = pino({
    level: env.LOG_LEVEL,
    redact: {
        paths: [
            "req.headers.authorization",
            "req.headers.cookie",
            "res.headers['set-cookie']",
            "*.password",
            "*.passwordHash",
            "*.token",
        ],
        censor: "[REDACTED]",
    },
    ...(env.NODE_ENV === "development"
        ? { transport: { target: "pino-pretty", options: { colorize: true } } }
        : {}),
});
