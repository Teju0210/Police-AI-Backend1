export default function GlassCard({ children, className = "" }) {
  return (
    <div
      className={`
        bg-white/5
        backdrop-blur-xl
        border
        border-white/10
        rounded-2xl
        shadow-xl
        hover:border-blue-500/40
        hover:shadow-blue-500/20
        transition-all
        duration-300
        ${className}
      `}
    >
      {children}
    </div>
  );
}
