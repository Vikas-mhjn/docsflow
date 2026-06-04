import prisma from "@/lib/prisma";
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
