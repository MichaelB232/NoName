import { boolean, integer, jsonb, pgTable, text, timestamp, uuid, varchar } from "drizzle-orm/pg-core";

/**
 * Drizzle schema (database-migrations skill).
 *
 * RULES
 * - Every tenant-owned table has a NOT NULL `organization_id` FK (multitenancy-security skill).
 * - Never alter tables by hand: edit this file, then `pnpm db:generate` + `pnpm db:migrate`.
 */

export const organizationsTable = pgTable("organizations", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: varchar("name", { length: 255 }).notNull(),
    slug: varchar("slug", { length: 100 }).unique().notNull(),
    tier: varchar("tier", { length: 50 }).default("FREE").notNull(),
    isActive: boolean("is_active").default(true).notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
});

export const usersTable = pgTable("users", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id")
        .references(() => organizationsTable.id, { onDelete: "cascade" })
        .notNull(),
    email: varchar("email", { length: 255 }).unique().notNull(),
    fullName: varchar("full_name", { length: 255 }).notNull(),
    passwordHash: text("password_hash").notNull(),
    role: varchar("role", { length: 50 }).default("LEGAL_COUNSEL").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

export const contractsTable = pgTable("contracts", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id")
        .references(() => organizationsTable.id, { onDelete: "cascade" })
        .notNull(),
    uploadedByUserId: uuid("uploaded_by_user_id")
        .references(() => usersTable.id)
        .notNull(),
    title: varchar("title", { length: 255 }).notNull(),
    s3Key: text("s3_key").notNull(),
    fileSizeBytes: integer("file_size_bytes").notNull(),
    mimeType: varchar("mime_type", { length: 100 }).notNull(),
    // PENDING_UPLOAD | UPLOADED | PROCESSING | COMPLETED | FAILED
    status: varchar("status", { length: 50 }).default("PENDING_UPLOAD").notNull(),
    complianceScore: integer("compliance_score"),
    createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
});

export const auditMatrixTable = pgTable("audit_matrix_items", {
    id: uuid("id").primaryKey().defaultRandom(),
    organizationId: uuid("organization_id")
        .references(() => organizationsTable.id, { onDelete: "cascade" })
        .notNull(),
    contractId: uuid("contract_id")
        .references(() => contractsTable.id, { onDelete: "cascade" })
        .notNull(),
    clauseNumber: varchar("clause_number", { length: 50 }).notNull(),
    clauseTopic: varchar("clause_topic", { length: 255 }).notNull(),
    originalText: text("original_text").notNull(),
    // COMPLIANT | VIOLATION | AMBIGUOUS
    status: varchar("status", { length: 50 }).notNull(),
    violatedRegulation: jsonb("violated_regulation"),
    // HIGH | MEDIUM | LOW | CLEAN
    severity: varchar("severity", { length: 20 }).default("CLEAN").notNull(),
    penaltyEstimateIdr: integer("penalty_estimate_idr").default(0).notNull(),
    suggestedRevision: text("suggested_revision"),
    legalRationale: text("legal_rationale").notNull(),
    isRevisionAccepted: boolean("is_revision_accepted").default(false).notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});
