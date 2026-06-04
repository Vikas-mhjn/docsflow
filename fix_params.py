#!/usr/bin/env python3
"""Fix Next.js 16 async params. Run from docsflow-demo folder."""
import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

# ── app/workspace/[workspaceId]/layout.js ──────────────────
write("app/workspace/[workspaceId]/layout.js", '''import prisma from "@/lib/prisma";
import { notFound } from "next/navigation";
import WorkspaceSidebar from "@/components/sidebar/Sidebar";
import SearchProvider from "@/components/search/SearchProvider";

export default async function WorkspaceLayout({ children, params }) {
  const { workspaceId } = await params;

  const workspace = await prisma.workspace.findUnique({
    where: { id: workspaceId },
    include: {
      pages: {
        where: { isDeleted: false },
        orderBy: { createdAt: "asc" },
      },
    },
  });

  if (!workspace) notFound();

  const serializedPages = workspace.pages.map((p) => ({
    ...p,
    createdAt: p.createdAt.toISOString(),
    updatedAt: p.updatedAt.toISOString(),
  }));

  const serializedWorkspace = {
    ...workspace,
    createdAt: workspace.createdAt.toISOString(),
    updatedAt: workspace.updatedAt.toISOString(),
    pages: serializedPages,
  };

  return (
    <SearchProvider workspaceId={workspaceId}>
      <div className="app-layout">
        <WorkspaceSidebar workspace={serializedWorkspace} pages={serializedPages} />
        <div className="main-content">{children}</div>
      </div>
    </SearchProvider>
  );
}
''')

# ── app/workspace/[workspaceId]/page.js ────────────────────
write("app/workspace/[workspaceId]/page.js", '''export default async function WorkspaceHome({ params }) {
  await params; // Next.js 16 requires this
  return (
    <div className="page-content">
      <div className="empty-state">
        <div className="empty-state-icon">✍️</div>
        <div className="empty-state-title">No page selected</div>
        <div className="empty-state-desc">
          Select a page from the sidebar, or create a new one to get started.
        </div>
      </div>
    </div>
  );
}
''')

# ── app/workspace/[workspaceId]/[pageId]/page.js ───────────
write("app/workspace/[workspaceId]/[pageId]/page.js", '''import prisma from "@/lib/prisma";
import { notFound } from "next/navigation";
import PageEditor from "@/components/editor/PageEditor";
import Topbar from "@/components/layout/Topbar";
import TrashPageClient from "@/components/trash/TrashPageClient";

export default async function PageView({ params }) {
  const { pageId, workspaceId } = await params;

  if (pageId === "trash") {
    const trashedPages = await prisma.page.findMany({
      where: { workspaceId, isDeleted: true },
      orderBy: { updatedAt: "desc" },
    });
    const serialized = trashedPages.map((p) => ({
      ...p,
      createdAt: p.createdAt.toISOString(),
      updatedAt: p.updatedAt.toISOString(),
    }));
    return (
      <div className="page-content">
        <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>🗑️ Trash</h1>
        <p style={{ color: "var(--text-secondary)", fontSize: 14, marginBottom: 32 }}>
          Pages in trash will be permanently deleted after 30 days.
        </p>
        <TrashPageClient pages={serialized} workspaceId={workspaceId} />
      </div>
    );
  }

  const [page, workspace] = await Promise.all([
    prisma.page.findUnique({ where: { id: pageId, isDeleted: false } }),
    prisma.workspace.findUnique({
      where: { id: workspaceId },
      select: { name: true, icon: true },
    }),
  ]);

  if (!page || !workspace) notFound();

  const serializedPage = {
    ...page,
    createdAt: page.createdAt.toISOString(),
    updatedAt: page.updatedAt.toISOString(),
  };

  return (
    <>
      <Topbar page={serializedPage} workspaceId={workspaceId} workspaceName={workspace.name} />
      <PageEditor page={serializedPage} />
    </>
  );
}
''')

# ── app/dashboard/page.js ───────────────────────────────────
write("app/dashboard/page.js", '''import prisma from "@/lib/prisma";
import WorkspaceGrid from "@/components/workspace/WorkspaceGrid";

export default async function DashboardPage() {
  const userId = process.env.DEFAULT_USER_ID;

  const workspaces = await prisma.workspace.findMany({
    where: { userId },
    orderBy: { updatedAt: "desc" },
  });

  const serialized = workspaces.map((w) => ({
    ...w,
    createdAt: w.createdAt.toISOString(),
    updatedAt: w.updatedAt.toISOString(),
  }));

  return (
    <div className="dashboard-layout">
      <div className="dashboard-header">
        <h1 className="dashboard-title">My Workspaces</h1>
        <p className="dashboard-subtitle">
          Select a workspace or create a new one to get started.
        </p>
      </div>
      <WorkspaceGrid initialWorkspaces={serialized} userId={userId} />
    </div>
  );
}
''')

# ── app/api/search/route.js ─────────────────────────────────
write("app/api/search/route.js", '''import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q");
  const workspaceId = searchParams.get("workspaceId");

  if (!query || query.trim().length < 2) return NextResponse.json({ results: [] });
  if (!workspaceId) return NextResponse.json({ error: "workspaceId required" }, { status: 400 });

  try {
    const results = await prisma.page.findMany({
      where: {
        workspaceId,
        isDeleted: false,
        title: { contains: query.trim(), mode: "insensitive" },
      },
      select: { id: true, title: true, icon: true, parentId: true, updatedAt: true },
      orderBy: { updatedAt: "desc" },
      take: 10,
    });
    return NextResponse.json({
      results: results.map((p) => ({ ...p, updatedAt: p.updatedAt.toISOString() })),
    });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: "Search failed" }, { status: 500 });
  }
}
''')

print("\n✅ All files fixed for Next.js 16 async params!")
print("\nNow run:  npm run dev")
