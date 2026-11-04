import request from "supertest";
import { describe, expect, it } from "vitest";
import app from "../../src/app";

describe("GET /api/v1/health", () => {
    it("returns the standard success envelope", async () => {
        const res = await request(app).get("/api/v1/health");

        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
        expect(res.body.data.status).toBe("UP");
    });

    it("returns the standard error envelope for unknown routes", async () => {
        const res = await request(app).get("/api/v1/does-not-exist");

        expect(res.status).toBe(404);
        expect(res.body.success).toBe(false);
        expect(res.body.error.code).toBe("NOT_FOUND");
    });
});
