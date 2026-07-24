export default function Dashboard() {
  return (
    <div className="w-full h-[calc(100vh-4rem)] overflow-hidden rounded-xl border border-slate-800 bg-[#0A0E14]">
      <iframe
        src="/preksha_dashboard.html"
        className="w-full h-full border-none"
        title="Legacy Dashboard"
      />
    </div>
  );
}