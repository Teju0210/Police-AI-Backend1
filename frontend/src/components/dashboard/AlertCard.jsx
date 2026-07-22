import { AlertTriangle } from "lucide-react";

export default function AlertCard({
  title,
  location,
  time,
  color,
}) {
  return (
    <div className="flex items-center justify-between bg-slate-800 rounded-xl p-4 mb-3">

      <div className="flex items-center gap-4">

        <AlertTriangle
          className={color}
          size={22}
        />

        <div>

          <h3 className="text-white font-semibold">
            {title}
          </h3>

          <p className="text-slate-400 text-sm">
            {location}
          </p>

        </div>

      </div>

      <span className="text-xs text-slate-500">
        {time}
      </span>

    </div>
  );
}