"use client";
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
      <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", zIndex: 99 }} onClick={onClose} />
      <div ref={ref} style={{ position: "fixed", top: "50%", left: "50%", transform: "translate(-50%,-50%)", background: "var(--bg-primary)", border: "1px solid var(--border-color)", borderRadius: "var(--radius-xl)", boxShadow: "var(--shadow-xl)", width: 480, maxWidth: "90vw", zIndex: 100, padding: 20, maxHeight: "80vh", overflowY: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <h3 style={{ fontSize: 16, fontWeight: 600 }}>Choose Cover</h3>
          {currentCover && <button className="ghost-btn" style={{ color: "var(--accent-red)", fontSize: 13 }} onClick={() => onSelect(null)}>Remove</button>}
        </div>
        <div style={{ marginBottom: 16 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", marginBottom: 8 }}>Photos</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8 }}>
            {PHOTOS.map((p) => (
              <div key={p.id} onClick={() => onSelect(p.url)} style={{ height: 64, borderRadius: "var(--radius-md)", overflow: "hidden", cursor: "pointer", border: currentCover === p.url ? "2px solid var(--accent-blue)" : "2px solid transparent" }}>
                <img src={p.url} alt="" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              </div>
            ))}
          </div>
        </div>
        <div>
          <div style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", marginBottom: 8 }}>Gradients</div>
          <div style={{ display: "flex", gap: 8 }}>
            {GRADS.map((g) => (
              <div key={g} onClick={() => onSelect(g)} style={{ flex: 1, height: 40, borderRadius: "var(--radius-sm)", background: g, cursor: "pointer", border: currentCover === g ? "2px solid var(--accent-blue)" : "2px solid transparent" }} />
            ))}
          </div>
        </div>
        <input type="url" className="form-input" placeholder="Or paste an image URL..." style={{ marginTop: 16 }}
          onKeyDown={(e) => { if (e.key === "Enter") onSelect(e.target.value); }} />
      </div>
    </>
  );
}
