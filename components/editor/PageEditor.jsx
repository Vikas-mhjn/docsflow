"use client";
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
      Placeholder.configure({ placeholder: "Start writing, or press / for commands..." }),
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

  const sc = { saved: "var(--text-muted)", saving: "var(--accent-blue)", unsaved: "var(--accent-yellow)" };
  const st = { saved: "Saved", saving: "Saving...", unsaved: "Unsaved" };
  const isGrad = cover && cover.startsWith("linear-gradient");

  return (
    <div style={{ flex: 1, overflowY: "auto" }}>
      <div style={{ position: "fixed", top: 12, right: 24, fontSize: 12, color: sc[status], zIndex: 10 }}>{st[status]}</div>
      <div style={{ position: "relative" }}
        onMouseEnter={() => setHoverHeader(true)}
        onMouseLeave={() => setHoverHeader(false)}>
        {cover && (
          <div style={{ width: "100%", height: 200, background: isGrad ? cover : undefined }}>
            {!isGrad && <img src={cover} alt="" style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
          </div>
        )}
        {hoverHeader && (
          <div style={{ position: "absolute", bottom: 8, right: 16 }}>
            <button className="secondary-btn" style={{ fontSize: 12, padding: "4px 10px", background: "rgba(255,255,255,0.9)" }} onClick={() => setShowCover(true)}>
              {cover ? "Change Cover" : "+ Add Cover"}
            </button>
          </div>
        )}
      </div>
      <div className="editor-wrapper">
        <div className="editor-icon-row">
          <div style={{ position: "relative" }}>
            {icon
              ? <span className="editor-icon" onClick={() => setShowIcon(!showIcon)} style={{ cursor: "pointer" }}>{icon}</span>
              : <button className="ghost-btn" onClick={() => setShowIcon(true)}>+ Add Icon</button>
            }
            {showIcon && <IconPicker currentIcon={icon} onSelect={(v) => { setIcon(v); setShowIcon(false); save("icon", v); }} onClose={() => setShowIcon(false)} />}
          </div>
          {!cover && <button className="ghost-btn" onClick={() => setShowCover(true)}>+ Add Cover</button>}
        </div>
        <textarea className="editor-title" placeholder="Untitled" value={title}
          onChange={(e) => { setTitle(e.target.value); setStatus("unsaved"); e.target.style.height = "auto"; e.target.style.height = e.target.scrollHeight + "px"; }}
          onBlur={() => save("title", title)}
          onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); editor?.commands.focus("start"); } }}
          rows={1} style={{ display: "block", width: "100%", overflow: "hidden", resize: "none" }} />
        <div style={{ border: "1px solid var(--border-color)", borderRadius: "var(--radius-md)", overflow: "hidden", marginTop: 8 }}>
          <EditorToolbar editor={editor} />
          <div style={{ padding: 16 }}><EditorContent editor={editor} /></div>
        </div>
        {blockMenu && <BlockMenu editor={editor} position={blockMenu} onClose={() => setBlockMenu(null)} />}
      </div>
      {showCover && <CoverPicker currentCover={cover} onSelect={(v) => { setCover(v); setShowCover(false); save("coverImage", v); }} onClose={() => setShowCover(false)} />}
    </div>
  );
}
