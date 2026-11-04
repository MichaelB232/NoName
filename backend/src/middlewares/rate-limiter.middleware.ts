import rateLimit from "express-rate-limit";
import { fail } from "../lib/envelope";

/**
 * In-memory limiter for the template. Before running more than one backend
 * instance, switch to a Redis store so limits are shared (see docs/dependencies.md).
 */
export const writeRateLimiter = rateLimit({
    windowMs: 60_000,
    limit: 30,
    standardHeaders: "draft-8",
    legacyHeaders: false,
    message: fail("RATE_LIMITED", "Too many requests, please slow down"),
});

export const authRateLimiter = rateLimit({
    windowMs: 15 * 60_000,
    limit: 5,
    standardHeaders: "draft-8",
    legacyHeaders: false,
    message: fail("RATE_LIMITED", "Too many authentication attempts"),
});
