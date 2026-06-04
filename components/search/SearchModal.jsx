"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { debounce } from "@/lib/utils";

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
    if (e.key === "ArrowDown") { e.preventDefault(); setSel((i) => Math.min(i + 1, results.length - 1)); }
    if (e.key === "ArrowUp") { e.preventDefault(); setSel((i) => Math.max(i - 1, 0)); }
    if (e.key === "Enter" && results[sel]) go(results[sel].id);
  }

  return (
    <div className="search-modal" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="search-box">
        <div className="search-input-row">
          <span style={{ fontSize: 16, color: "var(--text-muted)" }}>🔍</span>
          <input ref={inputRef} className="search-input" placeholder="Search pages..."
            value={q} onChange={(e) => { setQ(e.target.value); ds(e.target.value); }} onKeyDown={onKey} />
          {loading && <span style={{ fontSize: 12, color: "var(--text-muted)" }}>Searching...</span>}
          <button className="ghost-btn" onClick={onClose} style={{ fontSize: 11 }}>Esc</button>
        </div>
        <div className="search-results">
          {q.length < 2 && <div className="search-empty">Type at least 2 characters to search</div>}
          {!loading && q.length >= 2 && results.length === 0 && <div className="search-empty">No results for "{q}"</div>}
          {results.map((p, i) => (
            <div key={p.id} className="search-result-item"
              style={{ background: i === sel ? "var(--bg-secondary)" : "transparent" }}
              onClick={() => go(p.id)} onMouseEnter={() => setSel(i)}>
              <span className="search-result-icon">{p.icon || "📄"}</span>
              <div style={{ flex: 1, overflow: "hidden" }}>
                <div className="search-result-title">{p.title || "Untitled"}</div>
              </div>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Enter</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
