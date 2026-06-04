"use client";
import { useRouter } from "next/navigation";
import StarButton from "@/components/ui/StarButton";

export default function Topbar({ page, workspaceId, workspaceName }) {
  const router = useRouter();
  return (
    <div className="topbar">
      <div className="topbar-breadcrumb">
        <span className="topbar-breadcrumb-item" style={{ cursor: "pointer" }} onClick={() => router.push("/dashboard")}>Home</span>
        <span className="topbar-breadcrumb-separator">/</span>
        <span className="topbar-breadcrumb-item" style={{ cursor: "pointer" }} onClick={() => router.push("/workspace/" + workspaceId)}>{workspaceName}</span>
        {page && (
          <>
            <span className="topbar-breadcrumb-separator">/</span>
            <span className="topbar-breadcrumb-item" style={{ color: "var(--text-primary)" }}>
              {page.icon && <span style={{ marginRight: 4 }}>{page.icon}</span>}
              {page.title || "Untitled"}
            </span>
          </>
        )}
      </div>
      <div className="topbar-actions">
        {page && <StarButton pageId={page.id} workspaceId={workspaceId} initialFavorited={page.isFavorited} />}
      </div>
    </div>
  );
}
