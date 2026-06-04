"use client";
import { useEffect, useRef } from "react";
const BLOCKS = [
  { id:"p",   label:"Text",        desc:"Plain paragraph", icon:"P",  cmd:(e)=>e.chain().focus().setParagraph().run() },
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
        <button key={b.id} onClick={()=>run(b)}
          style={{ display:"flex", alignItems:"center", gap:12, width:"100%", padding:"8px 10px", border:"none", background:"transparent", cursor:"pointer", textAlign:"left", borderRadius:"var(--radius-sm)" }}
          onMouseEnter={(e)=>e.currentTarget.style.background="var(--bg-secondary)"}
          onMouseLeave={(e)=>e.currentTarget.style.background="transparent"}>
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
