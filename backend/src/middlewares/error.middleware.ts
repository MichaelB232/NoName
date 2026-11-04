import type { NextFunction, Request, Response } from "express";
import { ZodError } from "zod";
import { env } from "../config/env";
import { AppError } from "../errors/AppError";
import { fail } from "../lib/envelope";
import { logger } from "../lib/logger";

/** 404 for unmatched routes — registered after all routers. */
export function notFoundHandler(req: Request, res: Response): void {
    res.status(404).json(fail("NOT_FOUND", `Route ${req.method} ${req.originalUrl} not found`));
}

/**
 * Centralized error handler (error-handling-logging skill).
 * Express 5 forwards rejected promises from async handlers here automatically.
 */
export function errorHandler(err: unknown, req: Request, res: Response, _next: NextFunction): void {
    if (err instanceof ZodError) {
        const details = err.issues.map((issue) => ({ field: issue.path.join("."), message: issue.message }));
        res.status(400).json(fail("VALIDATION_ERROR", "Invalid input provided", details));
        return;
    }

    if (err instanceof AppError) {
        if (!err.isOperational) {
            logger.error({ err, path: req.originalUrl }, "Non-operational AppError");
        }
        res.status(err.httpStatus).json(fail(err.code, err.message, err.details));
        return;
    }

    logger.error({ err, path: req.originalUrl }, "Unexpected server error");
    const message =
        env.NODE_ENV === "production" || !(err instanceof Error) ? "An internal server error occurred" : err.message;
    res.status(500).json(fail("INTERNAL_SERVER_ERROR", message));
}
