import app from "./app";
import { env } from "./config/env";
import { closeDb } from "./database/db";
import { logger } from "./lib/logger";

const server = app.listen(env.PORT, () => {
    logger.info(`Backend listening on http://localhost:${env.PORT} (${env.NODE_ENV})`);
});

/** Graceful shutdown: stop accepting connections, then release the DB pool. */
function shutdown(signal: string): void {
    logger.info(`${signal} received, shutting down`);
    server.close(() => {
        closeDb()
            .then(() => process.exit(0))
            .catch((error: unknown) => {
                logger.error({ err: error }, "Error while closing DB pool");
                process.exit(1);
            });
    });
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
