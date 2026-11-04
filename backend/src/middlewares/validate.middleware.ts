import type { NextFunction, Request, Response } from "express";
import type { ZodTypeAny } from "zod";

type RequestPart = "body" | "params" | "query";

/**
 * Validates one part of the request against a Zod schema.
 *
 * - body / params: replaced with the parsed (coerced, stripped) value.
 * - query: Express 5 exposes `req.query` as a read-only getter, so the parsed
 *   value is stored in `res.locals.query` instead.
 *
 * ZodErrors bubble up to the centralized error handler (VALIDATION_ERROR).
 */
export function validate(schema: ZodTypeAny, part: RequestPart = "body") {
    return (req: Request, res: Response, next: NextFunction): void => {
        const parsed: unknown = schema.parse(req[part]);
        if (part === "query") {
            res.locals.query = parsed;
        } else {
            req[part] = parsed;
        }
        next();
    };
}
