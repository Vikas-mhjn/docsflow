#!/usr/bin/env python3
"""
Prisma 7 Complete Fix v2
Run from inside docsflow-demo: python fix_prisma7_v2.py
"""
import os

files = {}

# ─── prisma/schema.prisma (NO url — Prisma 7 style) ────────
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

# ─── prisma.config.ts (with url for db push AND adapter) ───
files["prisma.config.ts"] = '''import path from "node:path";
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
'''

# ─── lib/prisma.js ──────────────────────────────────────────
files["lib/prisma.js"] = '''import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";
import pg from "pg";

function createPrismaClient() {
  const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

const globalForPrisma = globalThis;
const prisma = globalForPrisma.prisma ?? createPrismaClient();
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma;
'''

# ─── prisma/seed.js ─────────────────────────────────────────
files["prisma/seed.js"] = r'''const { PrismaClient } = require("@prisma/client");
const { PrismaPg } = require("@prisma/adapter-pg");
const { Pool } = require("pg");

// Load env files
try { require("dotenv").config({ path: ".env.local" }); } catch(e) {}
try { require("dotenv").config({ path: ".env" }); } catch(e) {}

const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
  console.error("ERROR: DATABASE_URL not found.");
  console.error("Make sure .env.local contains DATABASE_URL=...");
  process.exit(1);
}

const pool = new Pool({ connectionString: DATABASE_URL });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
  console.log("Connecting to database...");

  const user = await prisma.user.upsert({
    where: { email: "demo@docsflow.app" },
    update: {},
    create: { name: "Demo User", email: "demo@docsflow.app" },
  });

  console.log("User created:", user.id);

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

  console.log("\n========================================");
  console.log("  SEEDING COMPLETE");
  console.log("========================================");
  console.log("\nCopy this line into your .env.local:\n");
  console.log('DEFAULT_USER_ID="' + user.id + '"');
  console.log("\n========================================\n");
}

main()
  .catch((e) => {
    console.error("Seed failed:", e.message);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
    await pool.end();
  });
'''

print("Writing Prisma 7 v2 fix files...")
for path, content in files.items():
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

print("\n✅ Done! Now run these 4 commands in order:\n")
print("  npx prisma generate")
print("  npx prisma db push")
print("  node prisma/seed.js")
print("  npm run dev")
print("\nThe seed output will show your DEFAULT_USER_ID.")
print("Add it to .env.local before running npm run dev.\n")
