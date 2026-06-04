#!/usr/bin/env python3
"""
Recreate ALL component files.
Run from docsflow-demo: python recreate_components.py
"""
import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

# ── components/sidebar/Sidebar.jsx ─────────────────────────
write("components/sidebar/Sidebar.jsx", '''"use client";
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
        <button className="icon-btn" onClick={() => router.push("/dashboard")} title="Dashboard">←</button>
      </div>
      <div className="sidebar-body">
        <div className="sidebar-section">
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }} onClick={openSearch}>
            <span className="sidebar-item-icon">🔍</span>
            <span className="sidebar-item-label">Search</span>
            <span style={{ fontSize: 11, color: "var(--text-muted)", marginLeft: "auto" }}>⌘K</span>
          </button>
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }} onClick={handleNewPage} disabled={creating}>
            <span className="sidebar-item-icon">✏️</span>
            <span className="sidebar-item-label">{creating ? "Creating…" : "New Page"}</span>
          </button>
          <button className="sidebar-item" style={{ width: "100%", textAlign: "left" }}
            onClick={() => router.push("/workspace/" + workspace.id + "/trash")}>
            <span className="sidebar-item-icon">🗑️</span>
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
                  <span style={{ fontSize: 10, color: "var(--accent-yellow)" }}>★</span>
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
''')

# ── components/sidebar/PageTree.jsx ────────────────────────
write("components/sidebar/PageTree.jsx", '''"use client";
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
  const btn = { display:"flex", alignItems:"center", gap:8, width:"100%", padding:"8px 10px", border:"none", background:"transparent", cursor:"pointer", fontSize:14, textAlign:"left", borderRadius:"var(--radius-sm)" };
  return (
    <div ref={ref} style={{ position:"fixed", left:pos.x, top:pos.y, background:"var(--bg-primary)", border:"1px solid var(--border-color)", borderRadius:"var(--radius-md)", boxShadow:"var(--shadow-lg)", zIndex:200, minWidth:190, padding:4 }}>
      <button style={{ ...btn, color:"var(--text-primary)" }}
        onMouseEnter={(e) => e.currentTarget.style.background="var(--bg-secondary)"}
        onMouseLeave={(e) => e.currentTarget.style.background="transparent"}
        onClick={async () => { onClose(); await toggleFavorite(page.id, workspaceId); router.refresh(); }}>
        {page.isFavorited ? "★ Remove from Favorites" : "☆ Add to Favorites"}
      </button>
      <button style={{ ...btn, color:"var(--accent-red)" }}
        onMouseEnter={(e) => e.currentTarget.style.background="var(--accent-red-light)"}
        onMouseLeave={(e) => e.currentTarget.style.background="transparent"}
        onClick={async () => { onClose(); if (confirm("Move to trash?")) await deletePage(page.id, workspaceId); }}>
        🗑️ Move to Trash
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
          onClick={(e) => { e.stopPropagation(); setOpen(!open); }}>▶</span>
        <span className="page-tree-icon">{page.icon || "📄"}</span>
        <span className="page-tree-label">{page.title || "Untitled"}</span>
        {page.isFavorited && <span style={{ fontSize:10, color:"var(--accent-yellow)", flexShrink:0 }}>★</span>}
        <span className="sidebar-item-actions" onClick={(e) => e.stopPropagation()}>
          <button className="icon-btn" style={{ fontSize:12, fontWeight:700 }}
            onClick={async (e) => { e.stopPropagation(); await createPage(workspaceId, page.id); setOpen(true); }}>+</button>
          <button className="icon-btn"
            onClick={(e) => { e.stopPropagation(); const r = e.currentTarget.getBoundingClientRect(); setMenu({ x:r.left, y:r.bottom+4 }); }}>···</button>
        </span>
      </div>
      {menu && <ContextMenu page={page} workspaceId={workspaceId} pos={menu} onClose={() => setMenu(null)} />}
      {open && hasKids && (
        <div className="page-tree-children">
          {page.children.map((c) => <PageTreeItem key={c.id} page={c} workspaceId={workspaceId} depth={depth+1} />)}
        </div>
      )}
    </div>
  );
}

export default function PageTree({ pages, workspaceId }) {
  if (!pages || pages.length === 0)
    return <div style={{ padding:"8px 12px", fontSize:13, color:"var(--text-muted)" }}>No pages yet</div>;
  return <div>{pages.map((p) => <PageTreeItem key={p.id} page={p} workspaceId={workspaceId} depth={0} />)}</div>;
}
''')

# ── components/layout/Topbar.jsx ───────────────────────────
write("components/layout/Topbar.jsx", '''"use client";
import { useRouter } from "next/navigation";
import StarButton from "@/components/ui/StarButton";

export default function Topbar({ page, workspaceId, workspaceName }) {
  const router = useRouter();
  return (
    <div className="topbar">
      <div className="topbar-breadcrumb">
        <span className="topbar-breadcrumb-item" style={{ cursor:"pointer" }} onClick={() => router.push("/dashboard")}>Home</span>
        <span className="topbar-breadcrumb-separator">/</span>
        <span className="topbar-breadcrumb-item" style={{ cursor:"pointer" }} onClick={() => router.push("/workspace/" + workspaceId)}>{workspaceName}</span>
        {page && <>
          <span className="topbar-breadcrumb-separator">/</span>
          <span className="topbar-breadcrumb-item" style={{ color:"var(--text-primary)" }}>
            {page.icon && <span style={{ marginRight:4 }}>{page.icon}</span>}
            {page.title || "Untitled"}
          </span>
        </>}
      </div>
      <div className="topbar-actions">
        {page && <StarButton pageId={page.id} workspaceId={workspaceId} initialFavorited={page.isFavorited} />}
      </div>
    </div>
  );
}
''')

# ── components/ui/StarButton.jsx ───────────────────────────
write("components/ui/StarButton.jsx", '''"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { toggleFavorite } from "@/actions/page";

export default function StarButton({ pageId, workspaceId, initialFavorited }) {
  const [fav, setFav] = useState(initialFavorited);
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  async function handle(e) {
    e.stopPropagation();
    setFav(!fav);
    setBusy(true);
    const r = await toggleFavorite(pageId, workspaceId);
    setBusy(false);
    if (r.error) { setFav(fav); return; }
    router.refresh();
  }
  return (
    <button className="icon-btn" onClick={handle} disabled={busy}
      title={fav ? "Remove from Favorites" : "Add to Favorites"}
      style={{ color: fav ? "var(--accent-yellow)" : "var(--text-muted)", fontSize:16, opacity:busy?0.5:1 }}>
      {fav ? "★" : "☆"}
    </button>
  );
}
''')

# ── components/ui/IconPicker.jsx ───────────────────────────
write("components/ui/IconPicker.jsx", '''"use client";
import { useEffect, useRef } from "react";

const GROUPS = {
  "Documents": ["📄","📝","📋","📊","📈","📉","📃","📑"],
  "Objects":   ["💡","🔬","🔭","🎯","🏗️","⚙️","🔧","🔑"],
  "Nature":    ["🌿","🌸","🌊","🌙","⭐","🔥","🌈","🍀"],
  "Tech":      ["💻","🖥️","📱","🤖","⚡","🛸","🔮","🎮"],
  "Fun":       ["🚀","🎨","🎵","🎬","🌍","🎉","🦋","🦁"],
};

export default function IconPicker({ onSelect, onClose, currentIcon }) {
  const ref = useRef(null);
  useEffect(() => {
    const click = (e) => { if (ref.current && !ref.current.contains(e.target)) onClose(); };
    const key = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("mousedown", click);
    document.addEventListener("keydown", key);
    return () => { document.removeEventListener("mousedown", click); document.removeEventListener("keydown", key); };
  }, [onClose]);
  return (
    <div ref={ref} style={{ position:"absolute", top:"calc(100% + 8px)", left:0, background:"var(--bg-primary)", border:"1px solid var(--border-color)", borderRadius:"var(--radius-lg)", boxShadow:"var(--shadow-xl)", width:300, zIndex:100, padding:12, maxHeight:360, overflowY:"auto" }}>
      {currentIcon && (
        <button onClick={() => onSelect(null)} style={{ width:"100%", textAlign:"center", padding:6, fontSize:12, color:"var(--text-muted)", marginBottom:8, borderRadius:"var(--radius-sm)", border:"1px solid var(--border-color)", background:"transparent", cursor:"pointer" }}>
          Remove icon
        </button>
      )}
      {Object.entries(GROUPS).map(([g, emojis]) => (
        <div key={g} style={{ marginBottom:12 }}>
          <div style={{ fontSize:11, fontWeight:600, color:"var(--text-muted)", textTransform:"uppercase", letterSpacing:"0.06em", marginBottom:6 }}>{g}</div>
          <div style={{ display:"flex", flexWrap:"wrap", gap:4 }}>
            {emojis.map((em) => (
              <button key={em} onClick={() => onSelect(em)}
                style={{ width:34, height:34, display:"flex", alignItems:"center", justifyContent:"center", fontSize:20, borderRadius:"var(--radius-sm)", border:currentIcon===em?"2px solid var(--accent-blue)":"2px solid transparent", background:currentIcon===em?"var(--accent-blue-light)":"transparent", cursor:"pointer" }}
                onMouseEnter={(e) => { if (currentIcon!==em) e.currentTarget.style.background="var(--bg-secondary)"; }}
                onMouseLeave={(e) => { if (currentIcon!==em) e.currentTarget.style.background="transparent"; }}>
                {em}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
''')

# ── components/ui/CoverPicker.jsx ──────────────────────────
write("components/ui/CoverPicker.jsx", '''"use client";
import { useEffect, useRef } from "react";

const PHOTOS = [
  { id:"p1", url:"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600&q=80" },
  { id:"p2", url:"https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=1600&q=80" },
  { id:"p3", url:"https://images.unsplash.com/photo-1448375240586-882707db888b?w=1600&q=80" },
  { id:"p4", url:"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=80" },
  { id:"p5", url:"https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&q=80" },
  { id:"p6", url:"https://images.unsplash.com/photo-1558591710-4b4a1ae0f664?w=1600&q=80" },
];
const GRADS = [
  "linear-gradient(135deg,#667eea,#764ba2)",
  "linear-gradient(135deg,#f093fb,#f5576c)",
  "linear-gradient(135deg,#4facfe,#00f2fe)",
  "linear-gradient(135deg,#43e97b,#38f9d7)",
  "linear-gradient(135deg,#fa709a,#fee140)",
];

export default function CoverPicker({ onSelect, onClose, currentCover }) {
  const ref = useRef(null);
  useEffect(() => {
    const click = (e) => { if (ref.current && !ref.current.contains(e.target)) onClose(); };
    const key = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("mousedown", click);
    document.addEventListener("keydown", key);
    return () => { document.removeEventListener("mousedown", click); document.removeEventListener("keydown", key); };
  }, [onClose]);
  return (
    <>
      <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.4)", zIndex:99 }} onClick={onClose} />
      <div ref={ref} style={{ position:"fixed", top:"50%", left:"50%", transform:"translate(-50%,-50%)", background:"var(--bg-primary)", border:"1px solid var(--border-color)", borderRadius:"var(--radius-xl)", boxShadow:"var(--shadow-xl)", width:480, maxWidth:"90vw", zIndex:100, padding:20, maxHeight:"80vh", overflowY:"auto" }}>
        <div style={{ display:"flex", justifyContent:"space-between", marginBottom:16 }}>
          <h3 style={{ fontSize:16, fontWeight:600 }}>Choose Cover</h3>
          {currentCover && <button className="ghost-btn" style={{ color:"var(--accent-red)", fontSize:13 }} onClick={() => onSelect(null)}>Remove</button>}
        </div>
        <div style={{ marginBottom:16 }}>
          <div style={{ fontSize:11, fontWeight:600, color:"var(--text-muted)", textTransform:"uppercase", letterSpacing:"0.06em", marginBottom:8 }}>Photos</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:8 }}>
            {PHOTOS.map((p) => (
              <div key={p.id} onClick={() => onSelect(p.url)}
                style={{ height:64, borderRadius:"var(--radius-md)", overflow:"hidden", cursor:"pointer", border:currentCover===p.url?"2px solid var(--accent-blue)":"2px solid transparent" }}>
                <img src={p.url} alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
              </div>
            ))}
          </div>
        </div>
        <div>
          <div style={{ fontSize:11, fontWeight:600, color:"var(--text-muted)", textTransform:"uppercase", letterSpacing:"0.06em", marginBottom:8 }}>Gradients</div>
          <div style={{ display:"flex", gap:8 }}>
            {GRADS.map((g) => (
              <div key={g} onClick={() => onSelect(g)}
                style={{ flex:1, height:40, borderRadius:"var(--radius-sm)", background:g, cursor:"pointer", border:currentCover===g?"2px solid var(--accent-blue)":"2px solid transparent" }} />
            ))}
          </div>
        </div>
        <input type="url" className="form-input" placeholder="Or paste an image URL…" style={{ marginTop:16 }}
          onKeyDown={(e) => { if (e.key === "Enter") onSelect(e.target.value); }} />
      </div>
    </>
  );
}
''')

# ── components/editor/EditorToolbar.jsx ────────────────────
write("components/editor/EditorToolbar.jsx", '''"use client";
export default function EditorToolbar({ editor }) {
  if (!editor) return null;
  const tools = [
    { l:"B",  t:"Bold",      a:()=>editor.chain().focus().toggleBold().run(),           active:editor.isActive("bold") },
    { l:"I",  t:"Italic",    a:()=>editor.chain().focus().toggleItalic().run(),         active:editor.isActive("italic") },
    { l:"H1", t:"Heading 1", a:()=>editor.chain().focus().setHeading({level:1}).run(),  active:editor.isActive("heading",{level:1}) },
    { l:"H2", t:"Heading 2", a:()=>editor.chain().focus().setHeading({level:2}).run(),  active:editor.isActive("heading",{level:2}) },
    { l:"H3", t:"Heading 3", a:()=>editor.chain().focus().setHeading({level:3}).run(),  active:editor.isActive("heading",{level:3}) },
    { l:"☑",  t:"Todo",      a:()=>editor.chain().focus().toggleTaskList().run(),       active:editor.isActive("taskList") },
    { l:"•",  t:"Bullets",   a:()=>editor.chain().focus().toggleBulletList().run(),    active:editor.isActive("bulletList") },
    { l:"1.", t:"Numbered",  a:()=>editor.chain().focus().toggleOrderedList().run(),   active:editor.isActive("orderedList") },
  ];
  return (
    <div style={{ display:"flex", gap:2, padding:6, borderBottom:"1px solid var(--border-color)", background:"var(--bg-secondary)", flexWrap:"wrap" }}>
      {tools.map((t) => (
        <button key={t.l} title={t.t} onClick={t.a}
          style={{ width:30, height:28, display:"flex", alignItems:"center", justifyContent:"center", borderRadius:"var(--radius-sm)", fontSize:13, fontWeight:700, background:t.active?"var(--bg-active)":"transparent", color:t.active?"var(--text-primary)":"var(--text-secondary)", border:"none", cursor:"pointer" }}
          onMouseEnter={(e) => { if (!t.active) e.currentTarget.style.background="var(--bg-hover)"; }}
          onMouseLeave={(e) => { if (!t.active) e.currentTarget.style.background="transparent"; }}>
          {t.l}
        </button>
      ))}
    </div>
  );
}
''')

# ── components/editor/BlockMenu.jsx ────────────────────────
write("components/editor/BlockMenu.jsx", '''"use client";
import { useEffect, useRef } from "react";

const BLOCKS = [
  { id:"p",   label:"Text",        desc:"Plain paragraph", icon:"¶",  cmd:(e)=>e.chain().focus().setParagraph().run() },
  { id:"h1",  label:"Heading 1",   desc:"Large title",     icon:"H1", cmd:(e)=>e.chain().focus().setHeading({level:1}).run() },
  { id:"h2",  label:"Heading 2",   desc:"Medium title",    icon:"H2", cmd:(e)=>e.chain().focus().setHeading({level:2}).run() },
  { id:"h3",  label:"Heading 3",   desc:"Small title",     icon:"H3", cmd:(e)=>e.chain().focus().setHeading({level:3}).run() },
  { id:"todo",label:"Todo",        desc:"Checkbox item",   icon:"☑",  cmd:(e)=>e.chain().focus().toggleTaskList().run() },
  { id:"ul",  label:"Bullet List", desc:"Unordered list",  icon:"•",  cmd:(e)=>e.chain().focus().toggleBulletList().run() },
  { id:"ol",  label:"Numbered",    desc:"Ordered list",    icon:"1.", cmd:(e)=>e.chain().focus().toggleOrderedList().run() },
];

export default function BlockMenu({ editor, position, onClose }) {
  const ref = useRef(null);
  useEffect(() => {
    const click = (e) => { if (ref.current && !ref.current.contains(e.target)) onClose(); };
    const key = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("mousedown", click);
    document.addEventListener("keydown", key);
    return () => { document.removeEventListener("mousedown", click); document.removeEventListener("keydown", key); };
  }, [onClose]);
  function run(b) {
    editor.commands.deleteRange({ from:editor.state.selection.from-1, to:editor.state.selection.from });
    b.cmd(editor);
    onClose();
  }
  return (
    <div ref={ref} style={{ position:"fixed", left:position.x, top:position.y, background:"var(--bg-primary)", border:"1px solid var(--border-color)", borderRadius:"var(--radius-lg)", boxShadow:"var(--shadow-lg)", width:260, zIndex:50, padding:6 }}>
      <div style={{ fontSize:11, fontWeight:600, color:"var(--text-muted)", textTransform:"uppercase", letterSpacing:"0.06em", padding:"4px 8px 8px" }}>Turn into</div>
      {BLOCKS.map((b) => (
        <button key={b.id} onClick={() => run(b)}
          style={{ display:"flex", alignItems:"center", gap:12, width:"100%", padding:"8px 10px", border:"none", background:"transparent", cursor:"pointer", textAlign:"left", borderRadius:"var(--radius-sm)" }}
          onMouseEnter={(e) => e.currentTarget.style.background="var(--bg-secondary)"}
          onMouseLeave={(e) => e.currentTarget.style.background="transparent"}>
          <div style={{ width:32, height:32, display:"flex", alignItems:"center", justifyContent:"center", background:"var(--bg-secondary)", borderRadius:"var(--radius-sm)", fontSize:13, fontWeight:700, color:"var(--text-secondary)", flexShrink:0 }}>{b.icon}</div>
          <div>
            <div style={{ fontSize:14, fontWeight:500, color:"var(--text-primary)" }}>{b.label}</div>
            <div style={{ fontSize:12, color:"var(--text-muted)" }}>{b.desc}</div>
          </div>
        </button>
      ))}
    </div>
  );
}
''')

# ── components/editor/PageEditor.jsx ───────────────────────
write("components/editor/PageEditor.jsx", '''"use client";
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import TaskList from "@tiptap/extension-task-list";
import TaskItem from "@tiptap/extension-task-item";
import Placeholder from "@tiptap/extension-placeholder";
import { useState, useCallback, useRef, useEffect } from "react";
import { updatePage } from "@/actions/page";
import { debounce } from "@/lib/utils";
import IconPicker from "@/components/ui/IconPicker";
import CoverPicker from "@/components/ui/CoverPicker";
import EditorToolbar from "./EditorToolbar";
import BlockMenu from "./BlockMenu";

export default function PageEditor({ page }) {
  const [title, setTitle] = useState(page.title || "");
  const [icon, setIcon] = useState(page.icon || null);
  const [cover, setCover] = useState(page.coverImage || null);
  const [status, setStatus] = useState("saved");
  const [showIcon, setShowIcon] = useState(false);
  const [showCover, setShowCover] = useState(false);
  const [blockMenu, setBlockMenu] = useState(null);
  const [hoverHeader, setHoverHeader] = useState(false);
  const idRef = useRef(page.id);

  async function save(field, value) {
    setStatus("saving");
    await updatePage(idRef.current, { [field]: value });
    setStatus("saved");
  }

  const debouncedContent = useCallback(debounce((json) => save("content", json), 600), []);

  const editor = useEditor({
    extensions: [
      StarterKit,
      TaskList,
      TaskItem.configure({ nested: true }),
      Placeholder.configure({ placeholder: "Start writing, or press / for commands…" }),
    ],
    content: page.content || "",
    editorProps: {
      attributes: { class: "editor-body" },
      handleKeyDown(view, e) {
        if (e.key === "/") {
          const { from } = view.state.selection;
          const c = view.coordsAtPos(from);
          setBlockMenu({ x: c.left, y: c.bottom + 8 });
          return false;
        }
        return false;
      },
    },
    onUpdate: ({ editor }) => { setStatus("unsaved"); debouncedContent(editor.getJSON()); },
    onBlur: ({ editor }) => { save("content", editor.getJSON()); },
  });

  useEffect(() => {
    const fn = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        if (editor) save("content", editor.getJSON());
        save("title", title);
      }
    };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [editor, title]);

  const sc = { saved:"var(--text-muted)", saving:"var(--accent-blue)", unsaved:"var(--accent-yellow)" };
  const st = { saved:"✓ Saved", saving:"Saving…", unsaved:"Unsaved" };
  const isGrad = cover && cover.startsWith("linear-gradient");

  return (
    <div style={{ flex:1, overflowY:"auto" }}>
      <div style={{ position:"fixed", top:12, right:24, fontSize:12, color:sc[status], zIndex:10 }}>{st[status]}</div>
      <div style={{ position:"relative" }} onMouseEnter={() => setHoverHeader(true)} onMouseLeave={() => setHoverHeader(false)}>
        {cover && (
          <div style={{ width:"100%", height:200, background:isGrad?cover:undefined }}>
            {!isGrad && <img src={cover} alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />}
          </div>
        )}
        {hoverHeader && (
          <div style={{ position:"absolute", bottom:8, right:16 }}>
            <button className="secondary-btn" style={{ fontSize:12, padding:"4px 10px", background:"rgba(255,255,255,0.9)" }} onClick={() => setShowCover(true)}>
              {cover ? "Change Cover" : "+ Add Cover"}
            </button>
          </div>
        )}
      </div>
      <div className="editor-wrapper">
        <div className="editor-icon-row">
          <div style={{ position:"relative" }}>
            {icon
              ? <span className="editor-icon" onClick={() => setShowIcon(!showIcon)} style={{ cursor:"pointer" }}>{icon}</span>
              : <button className="ghost-btn" onClick={() => setShowIcon(true)}>+ Add Icon</button>
            }
            {showIcon && <IconPicker currentIcon={icon} onSelect={(v) => { setIcon(v); setShowIcon(false); save("icon", v); }} onClose={() => setShowIcon(false)} />}
          </div>
          {!cover && <button className="ghost-btn" onClick={() => setShowCover(true)}>+ Add Cover</button>}
        </div>
        <textarea className="editor-title" placeholder="Untitled" value={title}
          onChange={(e) => { setTitle(e.target.value); setStatus("unsaved"); e.target.style.height="auto"; e.target.style.height=e.target.scrollHeight+"px"; }}
          onBlur={() => save("title", title)}
          onKeyDown={(e) => { if (e.key==="Enter") { e.preventDefault(); editor?.commands.focus("start"); } }}
          rows={1} style={{ display:"block", width:"100%", overflow:"hidden", resize:"none" }} />
        <div style={{ border:"1px solid var(--border-color)", borderRadius:"var(--radius-md)", overflow:"hidden", marginTop:8 }}>
          <EditorToolbar editor={editor} />
          <div style={{ padding:16 }}><EditorContent editor={editor} /></div>
        </div>
        {blockMenu && <BlockMenu editor={editor} position={blockMenu} onClose={() => setBlockMenu(null)} />}
      </div>
      {showCover && <CoverPicker currentCover={cover} onSelect={(v) => { setCover(v); setShowCover(false); save("coverImage", v); }} onClose={() => setShowCover(false)} />}
    </div>
  );
}
''')

# ── components/search/SearchProvider.jsx ───────────────────
write("components/search/SearchProvider.jsx", '''"use client";
import { useState, useEffect } from "react";
import SearchModal from "./SearchModal";

export default function SearchProvider({ children, workspaceId }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const fn = (e) => { if ((e.ctrlKey || e.metaKey) && e.key === "k") { e.preventDefault(); setOpen(true); } };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, []);
  return (
    <>
      {children}
      {open && <SearchModal workspaceId={workspaceId} onClose={() => setOpen(false)} />}
    </>
  );
}
''')

# ── components/search/SearchModal.jsx ──────────────────────
write("components/search/SearchModal.jsx", '''"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { debounce } from "@/lib/utils";

function highlight(text, q) {
  if (!q) return text;
  const i = text.toLowerCase().indexOf(q.toLowerCase());
  if (i === -1) return text;
  return <>{text.slice(0,i)}<mark style={{ background:"var(--accent-blue-light)", color:"var(--accent-blue)", borderRadius:2, padding:"0 1px" }}>{text.slice(i,i+q.length)}</mark>{text.slice(i+q.length)}</>;
}

export default function SearchModal({ workspaceId, onClose }) {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sel, setSel] = useState(0);
  const inputRef = useRef(null);
  const router = useRouter();

  useEffect(() => { inputRef.current?.focus(); }, []);
  useEffect(() => {
    const fn = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  async function search(query) {
    if (!query || query.length < 2) { setResults([]); return; }
    setLoading(true);
    try {
      const r = await fetch("/api/search?" + new URLSearchParams({ q: query, workspaceId }));
      const d = await r.json();
      setResults(d.results || []);
      setSel(0);
    } catch { setResults([]); }
    finally { setLoading(false); }
  }

  const ds = useCallback(debounce(search, 300), [workspaceId]);

  function go(pageId) { router.push("/workspace/" + workspaceId + "/" + pageId); onClose(); }

  function onKey(e) {
    if (e.key === "ArrowDown") { e.preventDefault(); setSel((i) => Math.min(i+1, results.length-1)); }
    if (e.key === "ArrowUp")   { e.preventDefault(); setSel((i) => Math.max(i-1, 0)); }
    if (e.key === "Enter" && results[sel]) go(results[sel].id);
  }

  return (
    <div className="search-modal" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="search-box">
        <div className="search-input-row">
          <span style={{ fontSize:16, color:"var(--text-muted)" }}>🔍</span>
          <input ref={inputRef} className="search-input" placeholder="Search pages…"
            value={q} onChange={(e) => { setQ(e.target.value); ds(e.target.value); }} onKeyDown={onKey} />
          {loading && <span style={{ fontSize:12, color:"var(--text-muted)" }}>Searching…</span>}
          <button className="ghost-btn" onClick={onClose} style={{ fontSize:11 }}>Esc</button>
        </div>
        <div className="search-results">
          {q.length < 2 && <div className="search-empty">Type at least 2 characters to search</div>}
          {!loading && q.length >= 2 && results.length === 0 && <div className="search-empty">No results for "{q}"</div>}
          {results.map((p, i) => (
            <div key={p.id} className="search-result-item"
              style={{ background: i===sel ? "var(--bg-secondary)" : "transparent" }}
              onClick={() => go(p.id)} onMouseEnter={() => setSel(i)}>
              <span className="search-result-icon">{p.icon || "📄"}</span>
              <div style={{ flex:1, overflow:"hidden" }}>
                <div className="search-result-title">{highlight(p.title || "Untitled", q)}</div>
              </div>
              <span style={{ fontSize:11, color:"var(--text-muted)" }}>↵</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
''')

# ── components/trash/TrashPageClient.jsx ───────────────────
write("components/trash/TrashPageClient.jsx", '''"use client";
import { useState } from "react";
import { restorePage, permanentlyDeletePage } from "@/actions/page";
import { formatDate } from "@/lib/utils";

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
      <div style={{ display:"flex", justifyContent:"flex-end", marginBottom:16 }}>
        <button className="danger-btn" onClick={emptyAll}>Empty Trash ({pages.length})</button>
      </div>
      {pages.map((p) => (
        <div key={p.id} className="trash-item">
          <span style={{ fontSize:20, flexShrink:0 }}>{p.icon || "📄"}</span>
          <div className="trash-item-info">
            <div className="trash-item-title">{p.title || "Untitled"}</div>
            <div className="trash-item-meta">Last updated {formatDate(p.updatedAt)}</div>
          </div>
          <div className="trash-item-actions">
            <button className="secondary-btn" style={{ fontSize:13, padding:"5px 12px" }} onClick={() => restore(p.id)}>Restore</button>
            <button className="danger-btn"    style={{ fontSize:13, padding:"5px 12px" }} onClick={() => perm(p.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
''')

# ── components/workspace/WorkspaceGrid.jsx ─────────────────
write("components/workspace/WorkspaceGrid.jsx", '''"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import CreateWorkspaceModal from "./CreateWorkspaceModal";
import { formatDate } from "@/lib/utils";

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
          <div className="empty-state" style={{ gridColumn:"1 / -1" }}>
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
          <span style={{ fontSize:20 }}>+</span>
          <span>New Workspace</span>
        </div>
      </div>
      {showModal && <CreateWorkspaceModal userId={userId} onCreated={handleCreated} onClose={() => setShowModal(false)} />}
    </>
  );
}
''')

# ── components/workspace/CreateWorkspaceModal.jsx ──────────
write("components/workspace/CreateWorkspaceModal.jsx", '''"use client";
import { useState, useEffect } from "react";
import { createWorkspace } from "@/actions/workspace";

const EMOJIS = ["📁","📂","🗂️","📝","💡","🚀","⚡","🎯","🌟","🔥","🎨","🔬","📊","🏗️","🌍","💎"];

export default function CreateWorkspaceModal({ userId, onCreated, onClose }) {
  const [name, setName] = useState("");
  const [icon, setIcon] = useState("📁");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fn = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (!name.trim()) { setError("Please enter a name"); return; }
    setLoading(true);
    const result = await createWorkspace({ name, icon, userId });
    setLoading(false);
    if (result.error) { setError(result.error); return; }
    onCreated(result.workspace);
  }

  return (
    <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="modal">
        <h2 className="modal-title">Create Workspace</h2>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label">Icon</label>
              <div style={{ display:"flex", flexWrap:"wrap", gap:6, padding:12, background:"var(--bg-secondary)", borderRadius:"var(--radius-md)", border:"1px solid var(--border-color)" }}>
                {EMOJIS.map((e) => (
                  <button key={e} type="button" onClick={() => setIcon(e)}
                    style={{ fontSize:22, width:36, height:36, display:"flex", alignItems:"center", justifyContent:"center", borderRadius:"var(--radius-sm)", background:icon===e?"var(--accent-blue-light)":"transparent", border:icon===e?"1px solid var(--accent-blue)":"1px solid transparent", cursor:"pointer" }}>
                    {e}
                  </button>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Name</label>
              <input className="form-input" type="text" placeholder="e.g., Personal Notes" value={name}
                onChange={(e) => setName(e.target.value)} autoFocus maxLength={100} />
            </div>
            {error && <p style={{ color:"var(--accent-red)", fontSize:13 }}>{error}</p>}
          </div>
          <div className="modal-footer">
            <button type="button" className="secondary-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="primary-btn" disabled={loading || !name.trim()}>
              {loading ? "Creating…" : "Create Workspace"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
''')

print("\n✅ ALL 14 component files created successfully!")
print("\nNow run:")
print("  npm run dev")
print("\nThen open: http://localhost:3001")
