export default function Dashboard() {
  return (
    <div className="w-full h-[calc(100vh-4rem)] overflow-hidden rounded-xl">
      <iframe
        src="/preksha_dashboard.html"
        className="w-full h-full border-none"
        title="Legacy Dashboard"
      />
    </div>
  );
}