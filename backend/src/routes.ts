import { Router } from "express";
import healthRoutes from "./modules/health/health.routes";

/**
 * Versioned API router. Register each vertical slice here:
 *   apiRouter.use("/contracts", contractsRoutes);
 */
export const apiRouter = Router();

apiRouter.use("/health", healthRoutes);
