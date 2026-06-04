"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { toggleFavorite } from "@/actions/page";

export default function StarButton({ pageId, workspaceId, initialFavorited }) {
  const [fav, setFav] = useState(initialFavorited);
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  async function handle(e) {
    e.stopPropagation();
    const nextFav = !fav;
    setFav(nextFav);
    setBusy(true);
    const r = await toggleFavorite(pageId, workspaceId);
    setBusy(false);
    if (r.error) {
      setFav(fav);
      return;
    }
    setFav(typeof r.isFavorited === "boolean" ? r.isFavorited : nextFav);
  }
  return (
    <button className="icon-btn" onClick={handle} disabled={busy}
      title={fav ? "Remove from Favorites" : "Add to Favorites"}
      style={{ color: fav ? "var(--accent-yellow)" : "var(--text-muted)", fontSize: 16, opacity: busy ? 0.5 : 1 }}>
      {fav ? "★" : "☆"}
    </button>
  );
}
