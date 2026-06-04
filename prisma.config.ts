import path from "node:path";
import { defineConfig } from "prisma/config";
import { config } from "dotenv";

// Load .env.local first, fall back to .env
config({ path: ".env.local" });
config({ path: ".env" });

const DATABASE_URL = process.env.DATABASE_URL;

export default defineConfig({
  earlyAccess: true,
  schema: path.join("prisma", "schema.prisma"),
  migrate: {
    adapter: async () => {
      const { PrismaPg } = await import("@prisma/adapter-pg");
      const pg = await import("pg");
      const pool = new pg.Pool({ connectionString: DATABASE_URL });
      return new PrismaPg(pool);
    },
  },
  // This is required for prisma db push in Prisma 7
  datasource: {
    url: DATABASE_URL,
  },
});
