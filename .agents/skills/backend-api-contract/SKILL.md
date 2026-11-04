---
name: backend-api-contract
description: >-
  Use this skill when implementing or modifying backend API routes, Express.js controllers, services, repositories, Zod validation schemas, or vertical slice architecture.
---

# Backend API & Architecture Standards
**Framework:** Express.js (TypeScript)  
**Architecture:** Vertical Slice Architecture (Feature-Based Modular Structure)  
**Validation:** Zod Schema (Single Source of Truth)  
**Data Access:** Drizzle ORM / SQL Query Builder (PostgreSQL)

---

## 1. Vertical Slice Directory Pattern

Each business domain resides in its own isolated module under `src/modules/<feature-name>/`:

```
src/modules/contracts/
├── contracts.controller.ts      # HTTP Request/Response Parsing & Status Codes
├── contracts.service.ts         # Pure Domain Logic & Transaction Management
├── contracts.repository.ts      # Drizzle Database Queries (Multi-tenant scoped)
├── contracts.schema.ts          # Zod Schemas & Inferred TypeScript Types
├── contracts.routes.ts          # Express Router definition with Middlewares
└── contracts.test.ts            # Feature-specific Integration & Unit tests
```

---

## 2. Inter-Slice Communication Rules

1. **Service-to-Service Only:** If Module A needs functionality or data from Module B, it **MUST ONLY** call `moduleB.service.ts`.
2. **Never Cross-Import Repositories:** Never import `moduleB.repository.ts` directly into Module A.
3. **Specific Named Imports Preferred:** Untuk komunikasi antar-modul, import function secara spesifik (contoh: `import { getOrganizationById } from "../organizations/organizations.service"`). Hindari import wildcard (`* as ...`) kecuali hampir semua/seluruh function dari service tersebut memang dibutuhkan.
4. **Circular Dependency Prohibition:** If Module A and Module B need each other, extract the shared logic into a shared helper service or domain event.

```typescript
// ✅ ALLOWED (src/modules/contracts/contracts.service.ts)
// Import function secara spesifik untuk komunikasi antar-modul (Direkomendasikan):
import { getOrganizationById } from "../organizations/organizations.service";

// Wildcard (*) hanya diperbolehkan jika hampir seluruh function pada modul tersebut memang dipakai:
// import * as orgService from "../organizations/organizations.service";

import * as contractRepo from "./contracts.repository"; // Import internal slice tetap diperbolehkan

export async function createContract(orgId: string, input: CreateContractInput) {
    const org = await getOrganizationById(orgId);
    if (!org.isActive) throw new ForbiddenError("Organization is suspended");
    return contractRepo.insertContract({ ...input, orgId });
}

// ❌ PROHIBITED
import * as orgRepo from "../organizations/organizations.repository"; // NEVER BYPASS SERVICE!
import * as orgService from "../organizations/organizations.service"; // DILARANG jika hanya memakai 1-2 function saja
```

---

## 3. Zod Schema & Type Derivation Standard

**Rule:** Every endpoint request body, URL param, and query string must have a corresponding Zod schema. **DO NOT** manually write TypeScript interfaces for incoming requests—infer them from Zod!

```typescript
// src/modules/contracts/contracts.schema.ts
import { z } from "zod";

export const uploadContractSchema = z.object({
    fileName: z.string().trim().min(3).max(255),
    fileSizeBytes: z.number().int().positive().max(25 * 1024 * 1024, "Max file size is 25MB"),
    mimeType: z.literal("application/pdf"),
    contractType: z.enum(["P2P_BORROWER_AGREEMENT", "P2P_LENDER_AGREEMENT", "VENDOR_SLA"]),
}).strict();

export const contractIdParamSchema = z.object({
    id: z.string().uuid("Invalid contract UUID format"),
});

// Auto-infer TypeScript types
export type UploadContractInput = z.infer<typeof uploadContractSchema>;
export type ContractIdParam = z.infer<typeof contractIdParamSchema>;
```

---

## 4. Controller & Middleware Pattern

Controllers must remain thin: they validate input, extract user/tenant context from `req`, call the service, and format the response.

```typescript
// src/modules/contracts/contracts.controller.ts
import { Response, NextFunction } from "express";
import { AuthRequest } from "../../middlewares/auth.middleware";
import * as contractService from "./contracts.service";
import { UploadContractInput } from "./contracts.schema";

export async function requestContractUpload(req: AuthRequest, res: Response, next: NextFunction) {
    try {
        const orgId = req.user!.organizationId;
        const input: UploadContractInput = req.body;
        
        const result = await contractService.initiateContractUpload(orgId, req.user!.id, input);
        
        res.status(201).json({
            success: true,
            message: "Presigned upload URL generated successfully",
            data: result,
        });
    } catch (error) {
        next(error);
    }
}
```

---

## 5. Standard Route Registration with Middleware Chaining

```typescript
// src/modules/contracts/contracts.routes.ts
import { Router } from "express";
import { authenticate } from "../../middlewares/auth.middleware";
import { validate } from "../../middlewares/validate.middleware";
import { writeRateLimiter } from "../../middlewares/rate-limiter.middleware";
import * as controller from "./contracts.controller";
import { uploadContractSchema, contractIdParamSchema } from "./contracts.schema";

const router = Router();

router.post(
    "/presign-upload",
    writeRateLimiter,
    authenticate,
    validate(uploadContractSchema, "body"),
    controller.requestContractUpload
);

router.post(
    "/:id/analyze",
    authenticate,
    validate(contractIdParamSchema, "params"),
    controller.triggerContractAnalysis
);

export default router;
```
