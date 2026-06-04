"use client";
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
                {EMOJIS.map((em) => (
                  <button key={em} type="button" onClick={() => setIcon(em)}
                    style={{ fontSize:22, width:36, height:36, display:"flex", alignItems:"center", justifyContent:"center", borderRadius:"var(--radius-sm)", background:icon===em?"var(--accent-blue-light)":"transparent", border:icon===em?"1px solid var(--accent-blue)":"1px solid transparent", cursor:"pointer" }}>
                    {em}
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
              {loading ? "Creating..." : "Create Workspace"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
