"use client";
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
