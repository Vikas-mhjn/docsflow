"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import CreateWorkspaceModal from "./CreateWorkspaceModal";

function formatDate(date) {
  return new Date(date).toLocaleDateString("en-US", { year:"numeric", month:"long", day:"numeric" });
}

export default function WorkspaceGrid({ initialWorkspaces, userId }) {
  const [workspaces, setWorkspaces] = useState(initialWorkspaces);
  const [showModal, setShowModal] = useState(false);
  const router = useRouter();

  function handleCreated(ws) {
    const s = { ...ws, createdAt: ws.createdAt instanceof Date ? ws.createdAt.toISOString() : ws.createdAt, updatedAt: ws.updatedAt instanceof Date ? ws.updatedAt.toISOString() : ws.updatedAt };
    setWorkspaces((prev) => [s, ...prev]);
    setShowModal(false);
  }

  return (
    <>
      <div className="dashboard-grid">
        {workspaces.length === 0 && (
          <div className="empty-state" style={{ gridColumn: "1 / -1" }}>
            <div className="empty-state-icon">📁</div>
            <div className="empty-state-title">No workspaces yet</div>
            <div className="empty-state-desc">Create your first workspace to get started.</div>
            <button className="primary-btn" onClick={() => setShowModal(true)}>Create Workspace</button>
          </div>
        )}
        {workspaces.map((w) => (
          <div key={w.id} className="workspace-card" onClick={() => router.push("/workspace/" + w.id)}>
            <div className="workspace-card-icon">{w.icon}</div>
            <div className="workspace-card-name">{w.name}</div>
            <div className="workspace-card-meta">Updated {formatDate(w.updatedAt)}</div>
          </div>
        ))}
        <div className="workspace-card-add" onClick={() => setShowModal(true)}>
          <span style={{ fontSize: 20 }}>+</span>
          <span>New Workspace</span>
        </div>
      </div>
      {showModal && <CreateWorkspaceModal userId={userId} onCreated={handleCreated} onClose={() => setShowModal(false)} />}
    </>
  );
}
