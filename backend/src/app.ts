import cookieParser from "cookie-parser";
import cors from "cors";
import express, { type Express } from "express";
import helmet from "helmet";
import { pinoHttp } from "pino-http";
import { env } from "./config/env";
import { logger } from "./lib/logger";
import { errorHandler, notFoundHandler } from "./middlewares/error.middleware";
import { apiRouter } from "./routes";

/**
 * Builds the Express app without binding a port, so Supertest can import it.
 * Middleware order matters: security → parsing → logging → routes → 404 → errors.
 */
export function createApp(): Express {
    const app = express();

    app.disable("x-powered-by");
    app.use(helmet());
    app.use(cors({ origin: env.CORS_ORIGINS, credentials: true }));
    app.use(express.json({ limit: "1mb" }));
    app.use(cookieParser());
    app.use(pinoHttp({ logger }));

    app.use("/api/v1", apiRouter);

    app.use(notFoundHandler);
    app.use(errorHandler);

    return app;
}

const app = createApp();
export default app;
