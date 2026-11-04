import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import { env } from "../config/env";
import * as schema from "./schema";

/** Shared connection pool. DATABASE_URL comes from env — never hardcoded. */
export const pool = new Pool({ connectionString: env.DATABASE_URL, max: 10 });

export const db = drizzle(pool, { schema });

export async function closeDb(): Promise<void> {
    await pool.end();
}
