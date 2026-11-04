export class AppError extends Error {
    public readonly code: string;
    public readonly httpStatus: number;
    public readonly isOperational: boolean;
    public readonly details: unknown[];

    constructor(code: string, message: string, httpStatus: number, details: unknown[] = [], isOperational = true) {
        super(message);
        this.name = new.target.name;
        this.code = code;
        this.httpStatus = httpStatus;
        this.details = details;
        this.isOperational = isOperational;
        Error.captureStackTrace(this, new.target);
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
    constructor(message = "Validation failed", details: unknown[] = []) {
        super("VALIDATION_ERROR", message, 400, details);
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
