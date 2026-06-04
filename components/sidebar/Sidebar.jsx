"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import PageTree from "./PageTree";
import { buildPageTree } from "@/lib/utils";
import { createPage } from "@/actions/page";

export default function WorkspaceSidebar({ workspace, pages }) {
  const router = useRouter();
  const [creating, setCreating] = useState(false);
  const rootPages = buildPageTree(pages);
  const favs = pages.filter((p) => p.isFavorited);

  async function handleNewPage() {
    setCreating(true);
    await createPage(workspace.id, null);
    setCreating(false);
  }

  function openSearch() {
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "k", ctrlKey: true, bubbles: true }));
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span style={{ fontSize: 18 }}>{workspace.icon}</span>
        <span className="sidebar-workspace-name">{workspace.name}</span>
        <button className="icon-btn" onClick={() => router.push("/dashboard")} title="Dashboard">
          {"<-"}
        </button>
      </div>
      <div className="sidebar-body">
        <div className="sidebar-section">
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }} onClick={openSearch}>
            <span className="sidebar-item-icon">{"🔍"}</span>
            <span className="sidebar-item-label">Search</span>
          </button>
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }} onClick={handleNewPage} disabled={creating}>
            <span className="sidebar-item-icon">{"✏️"}</span>
            <span className="sidebar-item-label">{creating ? "Creating..." : "New Page"}</span>
          </button>
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }}
            onClick={() => router.push("/workspace/" + workspace.id + "/trash")}>
            <span className="sidebar-item-icon">{"🗑️"}</span>
            <span className="sidebar-item-label">Trash</span>
          </button>
        </div>
        <div className="divider" />
        {favs.length > 0 && (
          <>
            <div className="sidebar-section">
              <div className="sidebar-section-label">Favorites</div>
              {favs.map((p) => (
                <button key={p.id} className="sidebar-item" style={{ width: "100%", textAlign: "left" }}
                  onClick={() => router.push("/workspace/" + workspace.id + "/" + p.id)}>
                  <span className="sidebar-item-icon">{p.icon || "📄"}</span>
                  <span className="sidebar-item-label">{p.title || "Untitled"}</span>
                </button>
              ))}
            </div>
            <div className="divider" />
          </>
        )}
        <div className="sidebar-section">
          <div className="sidebar-section-label">Pages</div>
          <PageTree pages={rootPages} workspaceId={workspace.id} />
        </div>
      </div>
    </aside>
  );
}
