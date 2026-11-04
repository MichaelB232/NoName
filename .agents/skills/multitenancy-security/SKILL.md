---
name: multitenancy-security
description: >-
  Use this skill when enforcing multi-tenant isolation, ensuring organization_id scoping in database queries, securing MinIO/S3 pre-signed URLs, or setting tenant-isolated vector collections.
---

# Multi-Tenancy & Data Security Standards
**Model:** Shared Database, Hard Logical Isolation by `organization_id`  
**Storage:** MinIO / S3 Tenant-Prefixed Paths  
**Vector DB:** Tenant Payload Filtering & Isolated Collections

---

## 1. Golden Rules of Multi-Tenancy

1. **Every Business Table Must Have `organization_id`:**  
   No tenant-owned table shall exist without a non-nullable `organization_id uuid REFERENCES organizations(id)`.
2. **Every Database Query Must Enforce `organization_id` in the `WHERE` Clause:**  
   Even if an item is queried by primary key `id`, the query **MUST** be:  
   `WHERE id = $1 AND organization_id = $2`.
3. **No Direct S3 Access:**  
   Clients never receive persistent MinIO credentials. Uploads and downloads use short-lived Presigned URLs with tenant-enforced keys.

---

## 2. PostgreSQL Query Pattern with Drizzle ORM

```typescript
// src/modules/contracts/contracts.repository.ts
import { db } from "../../database/db";
import { contractsTable } from "../../database/schema";
import { eq, and } from "drizzle-orm";

// ✅ CORRECT: Both ID and organization_id checked
export async function getContractById(id: string, organizationId: string) {
    const [contract] = await db
        .select()
        .from(contractsTable)
        .where(
            and(
                eq(contractsTable.id, id),
                eq(contractsTable.organizationId, organizationId)
            )
        );
    return contract || null;
}

// ❌ FORBIDDEN: Missing organization_id check allows IDOR vulnerability!
export async function unsafeGetContractById(id: string) {
    return db.select().from(contractsTable).where(eq(contractsTable.id, id));
}
```

---

## 3. MinIO / S3 Storage Path Isolation

All uploaded files are organized by organization prefix:

```
Bucket: /compliance-contracts/
├── org_a1b2c3d4/
│   ├── contracts/
│   │   └── 9c8a7b6d-uuid.pdf
│   └── reports/
│       └── 9c8a7b6d-audit-report.json
└── org_e5f6g7h8/
    └── contracts/
        └── 11223344-uuid.pdf
```

### Presigned URL Security Policy
* **Expiration TTL:** Max 10 minutes (600 seconds).
* **Content-Type Restriction:** Header must match `application/pdf` exactly.
* **Max Payload Size:** 25MB enforced via presigned post policy or client-size check.

---

## 4. RBAC (Role-Based Access Control) Matrix

| User Role | View Audit Matrix | Upload Contracts | Accept Redline Revisions | Manage Org Users |
| :--- | :---: | :---: | :---: | :---: |
| `ORG_ADMIN` | ✅ | ✅ | ✅ | ✅ |
| `LEGAL_COUNSEL` | ✅ | ✅ | ✅ | ❌ |
| `COMPLIANCE_AUDITOR` | ✅ | ✅ | ❌ | ❌ |
| `VIEWER` | ✅ | ❌ | ❌ | ❌ |
