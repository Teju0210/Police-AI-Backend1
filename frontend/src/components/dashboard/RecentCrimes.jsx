import {
  AlertTriangle,
  ShieldAlert,
  Car,
  Users,
} from "lucide-react";

const crimes = [
  {
    id: "FIR-1023",
    type: "Robbery",
    location: "Bengaluru",
    status: "Active",
    icon: ShieldAlert,
  },
  {
    id: "FIR-1044",
    type: "Vehicle Theft",
    location: "Mysuru",
    status: "Investigating",
    icon: Car,
  },
  {
    id: "FIR-1082",
    type: "Assault",
    location: "Hubballi",
    status: "Closed",
    icon: Users,
  },
  {
    id: "FIR-1101",
    type: "Cyber Crime",
    location: "Mangaluru",
    status: "Active",
    icon: AlertTriangle,
  },
];

export default function RecentCrimes() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <h2 className="text-xl font-bold text-white mb-6">
        Recent Crime Activity
      </h2>

      <div className="space-y-4">
        {crimes.map((crime) => (
          <div
            key={crime.id}
            className="flex items-center justify-between bg-slate-800 rounded-xl p-4 hover:bg-slate-700 transition"
          >
            <div className="flex items-center gap-4">
              <crime.icon className="text-blue-500" size={26} />

              <div>
                <h3 className="font-semibold text-white">
                  {crime.type}
                </h3>

                <p className="text-sm text-slate-400">
                  {crime.location}
                </p>
              </div>
            </div>

            <div className="text-right">
              <p className="text-sm text-slate-300">
                {crime.id}
              </p>

              <span
                className={`text-xs px-3 py-1 rounded-full ${
                  crime.status === "Active"
                    ? "bg-red-500/20 text-red-400"
                    : crime.status === "Closed"
                    ? "bg-green-500/20 text-green-400"
                    : "bg-yellow-500/20 text-yellow-400"
                }`}
              >
                {crime.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
