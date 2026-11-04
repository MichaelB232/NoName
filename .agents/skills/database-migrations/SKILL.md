---
name: database-migrations
description: >-
  Use this skill when defining or altering PostgreSQL database schemas, writing Drizzle ORM models, or managing migrations with drizzle-kit.
---

# Database Schemas & Migrations Standards
**Engine:** PostgreSQL 16+  
**ORM / Schema Definition:** Drizzle ORM (TypeScript)  
**Migration Tool:** `drizzle-kit`

---

## 1. Drizzle Schema Standards

All schema tables reside in `src/database/schema.ts` (or modular `src/database/schemas/*.ts`).

```typescript
// src/database/schema.ts
import { pgTable, uuid, text, timestamp, varchar, integer, jsonb, boolean } from "drizzle-orm/pg-core";

// Organizations (Tenants)
export const organizationsTable = pgTable("organizations", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: varchar("name", { length: 255 }).notNull(),
    slug: varchar("slug", { length: 100 }).unique().notNull(),
    tier: varchar("tier", { length: 50 }).default("FREE").notNull(),
    isActive: boolean("is_active").default(true).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Users
export const usersTable = pgTable("users", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id").references(() => organizationsTable.id, { onDelete: "cascade" }).notNull(),
    email: varchar("email", { length: 255 }).unique().notNull(),
    fullName: varchar("full_name", { length: 255 }).notNull(),
    passwordHash: text("password_hash").notNull(),
    role: varchar("role", { length: 50 }).default("LEGAL_COUNSEL").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Contracts
export const contractsTable = pgTable("contracts", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id").references(() => organizationsTable.id, { onDelete: "cascade" }).notNull(),
    uploadedByUserId: uuid("uploaded_by_user_id").references(() => usersTable.id).notNull(),
    title: varchar("title", { length: 255 }).notNull(),
    s3Key: text("s3_key").notNull(),
    fileSizeBytes: integer("file_size_bytes").notNull(),
    mimeType: varchar("mime_type", { length: 50 }).notNull(),
    status: varchar("status", { length: 50 }).default("PENDING_UPLOAD").notNull(), // PENDING_UPLOAD, UPLOADED, PROCESSING, COMPLETED, FAILED
    complianceScore: integer("compliance_score"), // 0 - 100
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Audit Matrix Findings (Per Clause)
export const auditMatrixTable = pgTable("audit_matrix_items", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id").references(() => organizationsTable.id, { onDelete: "cascade" }).notNull(),
    contractId: uuid("contract_id").references(() => contractsTable.id, { onDelete: "cascade" }).notNull(),
    clauseNumber: varchar("clause_number", { length: 50 }).notNull(),
    clauseTopic: varchar("clause_topic", { length: 255 }).notNull(),
    originalText: text("original_text").notNull(),
    status: varchar("status", { length: 50 }).notNull(), // COMPLIANT, VIOLATION, AMBIGUOUS
    violatedRegulation: jsonb("violated_regulation"),
    severity: varchar("severity", { length: 20 }).default("CLEAN").notNull(),
    penaltyEstimateIdr: integer("penalty_estimate_idr").default(0).notNull(),
    suggestedRevision: text("suggested_revision"),
    legalRationale: text("legal_rationale").notNull(),
    isRevisionAccepted: boolean("is_revision_accepted").default(false).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

---

## 2. Migration Commands & Workflow

1. **Generate Migration Files:**
   ```bash
   pnpm drizzle-kit generate
   ```
   Generates timestamped SQL files under `src/database/migrations/`.

2. **Execute Migrations:**
   ```bash
   pnpm drizzle-kit migrate
   ```

3. **Never Manually Alter Live Tables:**
   Never write raw SQL `ALTER TABLE` commands directly in production pgAdmin or DBeaver. Always commit Drizzle migration scripts to git.
