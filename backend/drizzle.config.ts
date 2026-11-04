import { defineConfig } from "drizzle-kit";

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
    throw new Error("DATABASE_URL is not set. Copy backend/.env.example to backend/.env and fill it in.");
}

export default defineConfig({
    dialect: "postgresql",
    schema: "./src/database/schema.ts",
    out: "./src/database/migrations",
    dbCredentials: { url: databaseUrl },
    strict: true,
    verbose: true,
});
