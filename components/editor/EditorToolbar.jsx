"use client";
export default function EditorToolbar({ editor }) {
  if (!editor) return null;
  const tools = [
    { l:"B",  t:"Bold",      a:()=>editor.chain().focus().toggleBold().run(),          active:editor.isActive("bold") },
    { l:"I",  t:"Italic",    a:()=>editor.chain().focus().toggleItalic().run(),        active:editor.isActive("italic") },
    { l:"H1", t:"Heading 1", a:()=>editor.chain().focus().setHeading({level:1}).run(), active:editor.isActive("heading",{level:1}) },
    { l:"H2", t:"Heading 2", a:()=>editor.chain().focus().setHeading({level:2}).run(), active:editor.isActive("heading",{level:2}) },
    { l:"H3", t:"Heading 3", a:()=>editor.chain().focus().setHeading({level:3}).run(), active:editor.isActive("heading",{level:3}) },
    { l:"☑",  t:"Todo",      a:()=>editor.chain().focus().toggleTaskList().run(),      active:editor.isActive("taskList") },
    { l:"•",  t:"Bullets",   a:()=>editor.chain().focus().toggleBulletList().run(),   active:editor.isActive("bulletList") },
    { l:"1.", t:"Numbered",  a:()=>editor.chain().focus().toggleOrderedList().run(),  active:editor.isActive("orderedList") },
  ];
  return (
    <div style={{ display:"flex", gap:2, padding:6, borderBottom:"1px solid var(--border-color)", background:"var(--bg-secondary)", flexWrap:"wrap" }}>
      {tools.map((t) => (
        <button key={t.l} title={t.t} onClick={t.a}
          style={{ width:30, height:28, display:"flex", alignItems:"center", justifyContent:"center", borderRadius:"var(--radius-sm)", fontSize:13, fontWeight:700, background:t.active?"var(--bg-active)":"transparent", color:t.active?"var(--text-primary)":"var(--text-secondary)", border:"none", cursor:"pointer" }}
          onMouseEnter={(e)=>{ if(!t.active) e.currentTarget.style.background="var(--bg-hover)"; }}
          onMouseLeave={(e)=>{ if(!t.active) e.currentTarget.style.background="transparent"; }}>
          {t.l}
        </button>
      ))}
    </div>
  );
}
