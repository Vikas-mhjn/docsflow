"use client";
import { useState, useRef, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { createPage, deletePage, toggleFavorite } from "@/actions/page";

function ContextMenu({ page, workspaceId, pos, onClose }) {
  const ref = useRef(null);
  const router = useRouter();
  useEffect(() => {
    const fn = (e) => { if (ref.current && !ref.current.contains(e.target)) onClose(); };
    document.addEventListener("mousedown", fn);
    return () => document.removeEventListener("mousedown", fn);
  }, [onClose]);
  return (
    <div ref={ref} style={{ position: "fixed", left: pos.x, top: pos.y, background: "var(--bg-primary)", border: "1px solid var(--border-color)", borderRadius: "var(--radius-md)", boxShadow: "var(--shadow-lg)", zIndex: 200, minWidth: 190, padding: 4 }}>
      <button style={{ display: "flex", alignItems: "center", gap: 8, width: "100%", padding: "8px 10px", border: "none", background: "transparent", cursor: "pointer", fontSize: 14, textAlign: "left", borderRadius: "var(--radius-sm)", color: "var(--text-primary)" }}
        onMouseEnter={(e) => e.currentTarget.style.background = "var(--bg-secondary)"}
        onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
        onClick={async () => { onClose(); await toggleFavorite(page.id, workspaceId); router.refresh(); }}>
        {page.isFavorited ? "★ Remove from Favorites" : "☆ Add to Favorites"}
      </button>
      <button style={{ display: "flex", alignItems: "center", gap: 8, width: "100%", padding: "8px 10px", border: "none", background: "transparent", cursor: "pointer", fontSize: 14, textAlign: "left", borderRadius: "var(--radius-sm)", color: "var(--accent-red)" }}
        onMouseEnter={(e) => e.currentTarget.style.background = "var(--accent-red-light)"}
        onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
        onClick={async () => { onClose(); if (confirm("Move to trash?")) await deletePage(page.id, workspaceId); }}>
        Move to Trash
      </button>
    </div>
  );
}

function PageTreeItem({ page, workspaceId, depth = 0 }) {
  const [open, setOpen] = useState(false);
  const [menu, setMenu] = useState(null);
  const router = useRouter();
  const pathname = usePathname();
  const isActive = pathname === "/workspace/" + workspaceId + "/" + page.id;
  const hasKids = page.children && page.children.length > 0;

  return (
    <div className="page-tree-item">
      <div className={"page-tree-row" + (isActive ? " active" : "")}
        style={{ paddingLeft: 8 + depth * 16 + "px" }}
        onClick={() => router.push("/workspace/" + workspaceId + "/" + page.id)}>
        <span className={"page-tree-toggle" + (open ? " open" : "")}
          style={{ visibility: hasKids ? "visible" : "hidden" }}
          onClick={(e) => { e.stopPropagation(); setOpen(!open); }}>
          {">"}
        </span>
        <span className="page-tree-icon">{page.icon || "📄"}</span>
        <span className="page-tree-label">{page.title || "Untitled"}</span>
        {page.isFavorited && <span style={{ fontSize: 10, color: "var(--accent-yellow)", flexShrink: 0 }}>★</span>}
        <span className="sidebar-item-actions" onClick={(e) => e.stopPropagation()}>
          <button className="icon-btn" style={{ fontSize: 12, fontWeight: 700 }}
            onClick={async (e) => { e.stopPropagation(); await createPage(workspaceId, page.id); setOpen(true); }}>+</button>
          <button className="icon-btn"
            onClick={(e) => { e.stopPropagation(); const r = e.currentTarget.getBoundingClientRect(); setMenu({ x: r.left, y: r.bottom + 4 }); }}>...</button>
        </span>
      </div>
      {menu && <ContextMenu page={page} workspaceId={workspaceId} pos={menu} onClose={() => setMenu(null)} />}
      {open && hasKids && (
        <div className="page-tree-children">
          {page.children.map((c) => <PageTreeItem key={c.id} page={c} workspaceId={workspaceId} depth={depth + 1} />)}
        </div>
      )}
    </div>
  );
}

export default function PageTree({ pages, workspaceId }) {
  if (!pages || pages.length === 0)
    return <div style={{ padding: "8px 12px", fontSize: 13, color: "var(--text-muted)" }}>No pages yet</div>;
  return <div>{pages.map((p) => <PageTreeItem key={p.id} page={p} workspaceId={workspaceId} depth={0} />)}</div>;
}
