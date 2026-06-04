import prisma from "@/lib/prisma";
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
