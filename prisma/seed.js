const { PrismaClient } = require("@prisma/client");
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
