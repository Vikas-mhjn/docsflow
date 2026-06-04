export default async function WorkspaceHome({ params }) {
  await params; // Next.js 16 requires this
  return (
    <div className="page-content">
      <div className="empty-state">
        <div className="empty-state-icon">✍️</div>
        <div className="empty-state-title">No page selected</div>
        <div className="empty-state-desc">
          Select a page from the sidebar, or create a new one to get started.
        </div>
      </div>
    </div>
  );
}
