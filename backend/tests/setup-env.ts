/**
 * Test-only environment. These are NON-SECRET placeholder values that let
 * `src/config/env.ts` validate during unit tests without real infrastructure.
 * Integration tests that need real services must load `backend/.env.test`
 * (git-ignored) instead.
 */
const testDefaults: Record<string, string> = {
    NODE_ENV: "test",
    PORT: "0",
    LOG_LEVEL: "fatal",
    CORS_ORIGINS: "http://localhost:3000",
    DATABASE_URL: "postgres://test:test@localhost:5432/test",
    REDIS_URL: "redis://localhost:6379",
    JWT_SECRET: "test-only-secret-not-used-anywhere-else-000000",
    S3_ENDPOINT: "http://localhost:9000",
    S3_REGION: "test-region",
    S3_BUCKET: "test-bucket",
    S3_ACCESS_KEY_ID: "test",
    S3_SECRET_ACCESS_KEY: "test",
    AGENT_SERVICE_URL: "http://localhost:8000",
    AGENT_SERVICE_TOKEN: "test-only-agent-token-not-used-anywhere-000000",
};

for (const [key, value] of Object.entries(testDefaults)) {
    process.env[key] ??= value;
}
