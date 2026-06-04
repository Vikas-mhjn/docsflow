export default function DashboardLoading() {
  return (
    <div className="dashboard-layout">
      <div className="dashboard-header">
        <div className="skeleton" style={{ width: 200, height: 32, marginBottom: 8 }} />
        <div className="skeleton" style={{ width: 300, height: 18 }} />
      </div>
      <div className="dashboard-grid" style={{ marginTop: 24 }}>
        {[1, 2, 3].map((i) => (
          <div key={i} className="workspace-card" style={{ cursor: "default" }}>
            <div className="skeleton" style={{ width: 44, height: 44, borderRadius: 8 }} />
            <div className="skeleton" style={{ width: "70%", height: 20, marginTop: 8 }} />
            <div className="skeleton" style={{ width: "50%", height: 14, marginTop: 8 }} />
          </div>
        ))}
      </div>
    </div>
  );
}
