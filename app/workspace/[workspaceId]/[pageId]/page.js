import prisma from "@/lib/prisma";
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
