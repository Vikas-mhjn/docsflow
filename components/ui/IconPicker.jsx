"use client";
import { useEffect, useRef } from "react";
const GROUPS = {
  "Documents": ["📄","📝","📋","📊","📈","📃","📑","📌"],
  "Objects":   ["💡","🔬","🔭","🎯","⚙️","🔧","🔑","🏆"],
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
    <div ref={ref} style={{ position: "absolute", top: "calc(100% + 8px)", left: 0, background: "var(--bg-primary)", border: "1px solid var(--border-color)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-xl)", width: 300, zIndex: 100, padding: 12, maxHeight: 360, overflowY: "auto" }}>
      {currentIcon && (
        <button onClick={() => onSelect(null)} style={{ width: "100%", textAlign: "center", padding: 6, fontSize: 12, color: "var(--text-muted)", marginBottom: 8, borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)", background: "transparent", cursor: "pointer" }}>
          Remove icon
        </button>
      )}
      {Object.entries(GROUPS).map(([g, emojis]) => (
        <div key={g} style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>{g}</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
            {emojis.map((em) => (
              <button key={em} onClick={() => onSelect(em)}
                style={{ width: 34, height: 34, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, borderRadius: "var(--radius-sm)", border: currentIcon === em ? "2px solid var(--accent-blue)" : "2px solid transparent", background: currentIcon === em ? "var(--accent-blue-light)" : "transparent", cursor: "pointer" }}
                onMouseEnter={(e) => { if (currentIcon !== em) e.currentTarget.style.background = "var(--bg-secondary)"; }}
                onMouseLeave={(e) => { if (currentIcon !== em) e.currentTarget.style.background = "transparent"; }}>
                {em}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
