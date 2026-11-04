---
name: error-handling-logging
description: >-
  Use this skill when implementing error classes (AppError), error handling middlewares, standard RESTful error response envelopes, or logging mechanisms.
---

# Error Handling & Logging Standards
**Error Hierarchy:** Custom `AppError` Base Class  
**HTTP Protocol:** Standard RESTful Error Payloads  
**Middleware:** Centralized Express Error Handler

---

## 1. AppError Class Hierarchy

All expected business logic errors inherit from `AppError`:

```typescript
// src/errors/AppError.ts
export class AppError extends Error {
    public readonly code: string;
    public readonly httpStatus: number;
    public readonly isOperational: boolean;

    constructor(code: string, message: string, httpStatus: number, isOperational = true) {
        super(message);
        this.code = code;
        this.httpStatus = httpStatus;
        this.isOperational = isOperational;
        Error.captureStackTrace(this, this.constructor);
    }
}

export class NotFoundError extends AppError {
    constructor(message = "Resource not found") {
        super("NOT_FOUND", message, 404);
    }
}

export class UnauthorizedError extends AppError {
    constructor(message = "Authentication required") {
        super("UNAUTHORIZED", message, 401);
    }
}

export class ForbiddenError extends AppError {
    constructor(message = "Access forbidden for this tenant or role") {
        super("FORBIDDEN", message, 403);
    }
}

export class ValidationError extends AppError {
    public readonly fields?: Record<string, string>;
    constructor(message = "Validation failed", fields?: Record<string, string>) {
        super("VALIDATION_ERROR", message, 400);
        this.fields = fields;
    }
}

export class ConflictError extends AppError {
    constructor(message = "Resource state conflict") {
        super("CONFLICT", message, 409);
    }
}

export class AgentExecutionError extends AppError {
    constructor(message = "AI Agent pipeline processing failure") {
        super("AGENT_EXECUTION_ERROR", message, 502);
    }
}
```

---

## 2. Centralized Error Handler Middleware

```typescript
// src/middlewares/error.middleware.ts
import { Request, Response, NextFunction } from "express";
import { AppError } from "../errors/AppError";
import { ZodError } from "zod";

export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
    // 1. Handle Zod Validation Errors
    if (err instanceof ZodError) {
        const fields: Record<string, string> = {};
        err.errors.forEach((issue) => {
            const fieldPath = issue.path.join(".");
            fields[fieldPath] = issue.message;
        });

        return res.status(400).json({
            success: false,
            error: {
                code: "VALIDATION_ERROR",
                message: "Invalid input provided",
                fields,
            },
        });
    }

    // 2. Handle Known AppErrors
    if (err instanceof AppError) {
        return res.status(err.httpStatus).json({
            success: false,
            error: {
                code: err.code,
                message: err.message,
                ...((err as any).fields && { fields: (err as any).fields }),
            },
        });
    }

    // 3. Handle Unexpected 500 Crashes (Mask internal traces in production)
    console.error("💥 [UNEXPECTED_SERVER_CRASH]:", err);
    return res.status(500).json({
        success: false,
        error: {
            code: "INTERNAL_SERVER_ERROR",
            message: process.env.NODE_ENV === "production" 
                ? "An internal server error occurred" 
                : err.message,
        },
    });
}
```
