import type { NextFunction, Request, Response } from "express";
import * as jose from "jose";
import { z } from "zod";
import { env } from "../config/env";
import { ForbiddenError, UnauthorizedError } from "../errors/AppError";

export const userRoles = ["ORG_ADMIN", "LEGAL_COUNSEL", "COMPLIANCE_AUDITOR", "VIEWER"] as const;
export type UserRole = (typeof userRoles)[number];

/** Claims stored inside the session JWT. `organizationId` drives tenant isolation. */
const sessionClaimsSchema = z.object({
    sub: z.string().uuid(),
    organizationId: z.string().uuid(),
    role: z.enum(userRoles),
});

export interface AuthUser {
    id: string;
    organizationId: string;
    role: UserRole;
}

export interface AuthRequest extends Request {
    user?: AuthUser;
}

const secretKey = new TextEncoder().encode(env.JWT_SECRET);

/**
 * Reads the JWT from the httpOnly cookie, verifies it with `jose` (HS256 enforced),
 * and attaches the tenant-scoped user to `req.user`.
 * Using `jose` eliminates known algorithm confusion and prototype pollution CVEs.
 */
export async function authenticate(req: AuthRequest, _res: Response, next: NextFunction): Promise<void> {
    const cookies = req.cookies as Record<string, string | undefined> | undefined;
    const token = cookies?.[env.AUTH_COOKIE_NAME];
    if (!token) {
        throw new UnauthorizedError();
    }

    let payload: unknown;
    try {
        const verified = await jose.jwtVerify(token, secretKey, {
            algorithms: ["HS256"],
        });
        payload = verified.payload;
    } catch {
        throw new UnauthorizedError("Session is invalid or expired");
    }

    const claims = sessionClaimsSchema.safeParse(payload);
    if (!claims.success) {
        throw new UnauthorizedError("Session payload is malformed");
    }

    req.user = { id: claims.data.sub, organizationId: claims.data.organizationId, role: claims.data.role };
    next();
}

/** RBAC guard (multitenancy-security skill §4). Use after `authenticate`. */
export function requireRole(...allowed: UserRole[]) {
    return (req: AuthRequest, _res: Response, next: NextFunction): void => {
        if (!req.user) {
            throw new UnauthorizedError();
        }
        if (!allowed.includes(req.user.role)) {
            throw new ForbiddenError(`Role ${req.user.role} is not allowed to perform this action`);
        }
        next();
    };
}
