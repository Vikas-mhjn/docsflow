"use client";
import { useState } from "react";
import { restorePage, permanentlyDeletePage } from "@/actions/page";

export default function TrashPageClient({ pages: init, workspaceId }) {
  const [pages, setPages] = useState(init);

  async function restore(id) {
    const r = await restorePage(id, workspaceId);
    if (r.success) setPages((p) => p.filter((x) => x.id !== id));
  }

  async function perm(id) {
    if (!confirm("Permanently delete? Cannot be undone.")) return;
    const r = await permanentlyDeletePage(id, workspaceId);
    if (r.success) setPages((p) => p.filter((x) => x.id !== id));
  }

  async function emptyAll() {
    if (!confirm("Empty entire trash? Cannot be undone.")) return;
    for (const p of pages) await permanentlyDeletePage(p.id, workspaceId);
    setPages([]);
  }

  if (!pages.length) return (
    <div className="empty-state">
      <div className="empty-state-icon">🗑️</div>
      <div className="empty-state-title">Trash is empty</div>
      <div className="empty-state-desc">Deleted pages will appear here.</div>
    </div>
  );

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 16 }}>
        <button className="danger-btn" onClick={emptyAll}>Empty Trash ({pages.length})</button>
      </div>
      {pages.map((p) => (
        <div key={p.id} className="trash-item">
          <span style={{ fontSize: 20, flexShrink: 0 }}>{p.icon || "📄"}</span>
          <div className="trash-item-info">
            <div className="trash-item-title">{p.title || "Untitled"}</div>
          </div>
          <div className="trash-item-actions">
            <button className="secondary-btn" style={{ fontSize: 13, padding: "5px 12px" }} onClick={() => restore(p.id)}>Restore</button>
            <button className="danger-btn" style={{ fontSize: 13, padding: "5px 12px" }} onClick={() => perm(p.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
