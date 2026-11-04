import { defineConfig } from "vitest/config";

export default defineConfig({
    test: {
        environment: "node",
        include: ["tests/**/*.test.ts", "src/**/*.test.ts"],
        // Tests get their own env file so they never touch dev/prod credentials.
        env: { NODE_ENV: "test" },
        setupFiles: ["./tests/setup-env.ts"],
        coverage: { provider: "v8", reporter: ["text", "html"] },
    },
});
