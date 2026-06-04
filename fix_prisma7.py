#!/usr/bin/env python3
"""
Fix for Prisma 7 - Run this from inside docsflow-demo folder
python fix_prisma7.py
"""
import os

files = {}

# ─── prisma/schema.prisma (Prisma 7 style - NO url in datasource) ──
files["prisma/schema.prisma"] = '''generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
}

model User {
  id         String      @id @default(cuid())
  name       String
  email      String      @unique
  image      String?
  workspaces Workspace[]
  createdAt  DateTime    @default(now())
  updatedAt  DateTime    @updatedAt
}

model Workspace {
  id        String   @id @default(cuid())
  name      String
  icon      String   @default("📁")
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  pages     Page[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Page {
  id          String    @id @default(cuid())
  title       String    @default("Untitled")
  icon        String?
  coverImage  String?
  content     Json?
  isDeleted   Boolean   @default(false)
  isFavorited Boolean   @default(false)
  workspaceId String
  workspace   Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  parentId    String?
  parent      Page?     @relation("PageChildren", fields: [parentId], references: [id], onDelete: SetNull)
  children    Page[]    @relation("PageChildren")
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
}
'''

# ─── prisma.config.ts (Prisma 7 config file) ───────────────
files["prisma.config.ts"] = '''import path from "node:path";
import { defineConfig } from "prisma/config";

export default defineConfig({
  earlyAccess: true,
  schema: path.join("prisma", "schema.prisma"),
  migrate: {
    adapter: async () => {
      const { PrismaPg } = await import("@prisma/adapter-pg");
      const { default: pg } = await import("pg");
      
      const connectionString = process.env.DATABASE_URL;
      const pool = new pg.Pool({ connectionString });
      return new PrismaPg(pool);
    },
  },
});
'''

# ─── lib/prisma.js (Prisma 7 client with adapter) ──────────
files["lib/prisma.js"] = '''import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";
import pg from "pg";

function createPrismaClient() {
  const connectionString = process.env.DATABASE_URL;
  const pool = new pg.Pool({ connectionString });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

const globalForPrisma = globalThis;
const prisma = globalForPrisma.prisma ?? createPrismaClient();
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma;
'''

# ─── prisma/seed.js (CommonJS - works with node directly) ──
files["prisma/seed.js"] = r'''const { PrismaClient } = require("@prisma/client");
const { PrismaPg } = require("@prisma/adapter-pg");
const { Pool } = require("pg");

require("dotenv").config({ path: ".env.local" });
// also try .env
if (!process.env.DATABASE_URL) {
  require("dotenv").config({ path: ".env" });
}

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  console.error("ERROR: DATABASE_URL not found in .env.local or .env");
  process.exit(1);
}

const pool = new Pool({ connectionString });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
  const user = await prisma.user.upsert({
    where: { email: "demo@docsflow.app" },
    update: {},
    create: { name: "Demo User", email: "demo@docsflow.app" },
  });

  console.log("✅ User created:", user.id);

  const ws1 = await prisma.workspace.create({
    data: { name: "Personal Notes", icon: "📝", userId: user.id },
  });

  await prisma.workspace.create({
    data: { name: "Work Projects", icon: "🚀", userId: user.id },
  });

  const p1 = await prisma.page.create({
    data: {
      title: "Getting Started",
      icon: "🌟",
      workspaceId: ws1.id,
      isFavorited: true,
      content: {
        type: "doc",
        content: [
          { type: "heading", attrs: { level: 1 }, content: [{ type: "text", text: "Welcome to DocsFlow" }] },
          { type: "paragraph", content: [{ type: "text", text: "This is your workspace. Start writing and organizing your knowledge base." }] },
          { type: "heading", attrs: { level: 2 }, content: [{ type: "text", text: "What you can do" }] },
          { type: "taskList", content: [
            { type: "taskItem", attrs: { checked: true },  content: [{ type: "paragraph", content: [{ type: "text", text: "Create a workspace" }] }] },
            { type: "taskItem", attrs: { checked: false }, content: [{ type: "paragraph", content: [{ type: "text", text: "Write your first page" }] }] },
            { type: "taskItem", attrs: { checked: false }, content: [{ type: "paragraph", content: [{ type: "text", text: "Add sub-pages" }] }] },
            { type: "taskItem", attrs: { checked: false }, content: [{ type: "paragraph", content: [{ type: "text", text: "Star your favorite pages" }] }] },
          ]},
        ],
      },
    },
  });

  const p2 = await prisma.page.create({
    data: {
      title: "Installation Guide",
      icon: "⚙️",
      workspaceId: ws1.id,
      parentId: p1.id,
      content: {
        type: "doc",
        content: [
          { type: "heading", attrs: { level: 1 }, content: [{ type: "text", text: "Installation" }] },
          { type: "paragraph", content: [{ type: "text", text: "Follow these steps to set up your environment." }] },
          { type: "bulletList", content: [
            { type: "listItem", content: [{ type: "paragraph", content: [{ type: "text", text: "Node.js 18+" }] }] },
            { type: "listItem", content: [{ type: "paragraph", content: [{ type: "text", text: "PostgreSQL database" }] }] },
          ]},
        ],
      },
    },
  });

  await prisma.page.create({
    data: {
      title: "Quick Start",
      icon: "⚡",
      workspaceId: ws1.id,
      parentId: p2.id,
      content: {
        type: "doc",
        content: [
          { type: "heading", attrs: { level: 1 }, content: [{ type: "text", text: "Quick Start" }] },
          { type: "paragraph", content: [{ type: "text", text: "Get up and running in under 5 minutes." }] },
        ],
      },
    },
  });

  await prisma.page.create({
    data: {
      title: "Meeting Notes",
      icon: "📋",
      workspaceId: ws1.id,
      isFavorited: true,
      content: {
        type: "doc",
        content: [
          { type: "heading", attrs: { level: 1 }, content: [{ type: "text", text: "Weekly Sync" }] },
          { type: "taskList", content: [
            { type: "taskItem", attrs: { checked: false }, content: [{ type: "paragraph", content: [{ type: "text", text: "Review pull requests" }] }] },
            { type: "taskItem", attrs: { checked: true },  content: [{ type: "paragraph", content: [{ type: "text", text: "Update documentation" }] }] },
          ]},
        ],
      },
    },
  });

  await prisma.page.create({
    data: {
      title: "Old Draft",
      icon: "📄",
      workspaceId: ws1.id,
      isDeleted: true,
      content: { type: "doc", content: [{ type: "paragraph", content: [{ type: "text", text: "This page was deleted." }] }] },
    },
  });

  console.log("\n✅ All demo data seeded!");
  console.log("\n👉 Add this line to your .env.local:");
  console.log('DEFAULT_USER_ID="' + user.id + '"');
}

main().catch(console.error).finally(async () => {
  await prisma.$disconnect();
  await pool.end();
});
'''

# ─── .env.local template ───────────────────────────────────
# We write instructions only — user fills in their actual URL
files["ENV_INSTRUCTIONS.txt"] = '''Your .env.local should contain:

DATABASE_URL="postgres://postgres:postgres@localhost:51214/template1?sslmode=disable&connection_limit=10&connect_timeout=0&max_idle_connection_lifetime=0&pool_timeout=0&socket_timeout=0"
DEFAULT_USER_ID="fill_this_in_after_running_seed"
NEXT_PUBLIC_APP_NAME="DocsFlow"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

IMPORTANT: The DATABASE_URL above is from `npx prisma dev`.
Run `npx prisma dev` in a SEPARATE terminal, keep it running,
copy the DATABASE_URL it prints, paste into .env.local.
Then in THIS terminal run the rest of the commands.
'''

print("Applying Prisma 7 fixes...")
for path, content in files.items():
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

print("\n✅ Prisma 7 fix applied!")
print("\nNow run these commands IN ORDER:")
print("")
print("TERMINAL 1 (keep open):")
print("  npx prisma dev")
print("  (copy the DATABASE_URL it prints)")
print("")
print("TERMINAL 2:")
print("  1. Paste DATABASE_URL into .env.local")
print("  2. npm install @prisma/adapter-pg pg dotenv")
print("  3. npx prisma generate")
print("  4. npx prisma db push")
print("  5. node prisma/seed.js")
print("  6. Paste DEFAULT_USER_ID into .env.local")
print("  7. npm run dev")
