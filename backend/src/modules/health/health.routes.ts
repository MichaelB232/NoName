import { Router } from "express";
import { ok } from "../../lib/envelope";

const router = Router();

router.get("/", (_req, res) => {
    res.status(200).json(ok({ service: "backend", status: "UP", timestamp: new Date().toISOString() }));
});

export default router;
