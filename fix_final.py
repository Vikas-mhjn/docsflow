#!/usr/bin/env python3
"""
Final fix - run from docsflow-demo folder
python fix_final.py
"""
import os
import shutil

# ─── Step 1: Remove the duplicate (workspace) folder ───────
workspace_group = os.path.join("app", "workspace", "[workspaceId]", "(workspace)")
if os.path.exists(workspace_group):
    shutil.rmtree(workspace_group)
    print(f"✓ Removed duplicate folder: {workspace_group}")
else:
    print(f"  (workspace) folder not found — already clean")

# ─── Step 2: Update next.config.js ─────────────────────────
with open("next.config.js", "w", encoding="utf-8") as f:
    f.write("""/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: ['172.16.0.2'],
};
module.exports = nextConfig;
""")
print("✓ next.config.js updated")

# ─── Step 3: Verify the correct [pageId] folder exists ─────
correct_path = os.path.join("app", "workspace", "[workspaceId]", "[pageId]", "page.js")
if os.path.exists(correct_path):
    print(f"✓ {correct_path} exists — good")
else:
    print(f"  WARNING: {correct_path} not found — check your file structure")

print("\n✅ Done! Now restart the dev server:")
print("   Stop it with Ctrl+C, then run: npm run dev")
print("\n   Then open: http://localhost:3001")
