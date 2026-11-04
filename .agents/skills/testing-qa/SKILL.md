---
name: testing-qa
description: >-
  Use this skill when writing or running unit tests with Vitest, integration tests with Supertest, or verifying deterministic financial calculations and OJK regulatory compliance logic.
---

# Testing & Quality Assurance Standards
**Test Runner:** Vitest  
**HTTP Assertion:** Supertest  
**Strategy:** Dual-Layer Testing (Unit Tests for Isolated Logic + Integration Tests for Full HTTP/DB Slices)

---

## 1. Test Architecture Matrix

```
tests/
├── unit/                        # Instant, purely in-memory (No real DB, No network)
│   ├── services/
│   └── calculations/
│       └── ojk-penalty.test.ts
├── integration/                 # Tests real Express routing, DB queries & transactions
│   ├── helpers/
│   │   ├── test-db.ts           # Clean test DB, truncate tables
│   │   └── test-auth.ts         # Generate tenant admin JWT & auth cookies
│   └── modules/
│       ├── contracts.test.ts
│       └── audit-matrix.test.ts
└── vitest.config.ts
```

---

## 2. Unit Testing Standard (Pure Logic Isolation)

Unit tests **MUST NEVER** connect to PostgreSQL or MinIO. Mock all repositories, network calls, or third-party SDKs:

```typescript
// tests/unit/calculations/ojk-penalty.test.ts
import { describe, it, expect } from "vitest";
import { evaluateInterestRateCompliance } from "../../../src/modules/audit/evaluators/interest.evaluator";

describe("evaluateInterestRateCompliance (POJK 10/2022 Rules)", () => {
    it("should flag VIOLATION if daily interest exceeds 0.3% per day", () => {
        const result = evaluateInterestRateCompliance({
            dailyInterestRatePercent: 0.45,
            loanAmountIdr: 10_000_000,
            tenorDays: 30,
        });

        expect(result.status).toBe("VIOLATION");
        expect(result.violatedArticle).toBe("POJK No. 10/POJK.05/2022 Pasal 29");
        expect(result.excessDailyRatePercent).toBeCloseTo(0.15);
    });

    it("should pass COMPLIANT if daily interest is within legal cap (<= 0.3%)", () => {
        const result = evaluateInterestRateCompliance({
            dailyInterestRatePercent: 0.28,
            loanAmountIdr: 5_000_000,
            tenorDays: 60,
        });

        expect(result.status).toBe("COMPLIANT");
        expect(result.excessDailyRatePercent).toBe(0);
    });
});
```

---

## 3. Integration Testing Standard (HTTP & DB Flow)

Integration tests verify that routes, middleware, validation, and multi-tenant scoping work harmoniously:

```typescript
// tests/integration/modules/contracts.test.ts
import { describe, it, expect, beforeEach, afterAll } from "vitest";
import request from "supertest";
import app from "../../../src/app";
import { cleanDatabase, closeDb } from "../helpers/test-db";
import { createTenantAndUser } from "../helpers/test-auth";

afterAll(async () => {
    await closeDb();
});

describe("POST /api/v1/contracts/presign-upload", () => {
    beforeEach(async () => {
        await cleanDatabase();
    });

    it("should return presigned URL when request is valid and authenticated", async () => {
        const { cookie, orgId } = await createTenantAndUser("Fintech A");

        const res = await request(app)
            .post("/api/v1/contracts/presign-upload")
            .set("Cookie", cookie)
            .send({
                fileName: "Perjanjian_Pinjaman_P2P.pdf",
                fileSizeBytes: 2048576,
                mimeType: "application/pdf",
                contractType: "P2P_BORROWER_AGREEMENT",
            });

        expect(res.status).toBe(201);
        expect(res.body.success).toBe(true);
        expect(res.body.data.uploadUrl).toBeDefined();
        expect(res.body.data.s3Key).toContain(orgId); // Enforce tenant prefix in S3 key
    });

    it("should reject unauthenticated requests with 401", async () => {
        const res = await request(app)
            .post("/api/v1/contracts/presign-upload")
            .send({
                fileName: "Test.pdf",
                fileSizeBytes: 1024,
                mimeType: "application/pdf",
                contractType: "P2P_BORROWER_AGREEMENT",
            });

        expect(res.status).toBe(401);
        expect(res.body.error.code).toBe("UNAUTHORIZED");
    });

    it("should reject files larger than 25MB with 400 validation error", async () => {
        const { cookie } = await createTenantAndUser("Fintech B");

        const res = await request(app)
            .post("/api/v1/contracts/presign-upload")
            .set("Cookie", cookie)
            .send({
                fileName: "Huge_File.pdf",
                fileSizeBytes: 30 * 1024 * 1024, // 30MB
                mimeType: "application/pdf",
                contractType: "P2P_BORROWER_AGREEMENT",
            });

        expect(res.status).toBe(400);
        expect(res.body.error.code).toBe("VALIDATION_ERROR");
        expect(res.body.error.fields["fileSizeBytes"]).toBeDefined();
    });
});
```
