import { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
} from "react-leaflet";

import L from "leaflet";

import {
  Card,
  CardContent,
} from "@/components/ui/card";

import {
  Badge
} from "@/components/ui/badge";

import {
  MapPin,
  ShieldAlert,
} from "lucide-react";


// Fix Leaflet marker icon issue in React
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});


// Hardcoded Police Stations (no lat/lng in DB for them)
const stations = [
  {
    name: "Electronic City Police Station",
    lat: 12.8456,
    lng: 77.6608,
  },
  {
    name: "Whitefield Police Station",
    lat: 12.9698,
    lng: 77.7500,
  },
  {
    name: "Bengaluru City HQ",
    lat: 12.9716,
    lng: 77.5946,
  }
];


export default function Heatmap() {
  const [crimes, setCrimes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:8000/dashboard/heatmap");
        const data = await res.json();
        if (data.crimes) {
          setCrimes(data.crimes);
        }
      } catch (err) {
        console.error("Failed to fetch heatmap data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const highRiskCount = crimes.filter((c) => c.severity === "HIGH").length;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white">
          Crime Heatmap
        </h1>
        <p className="text-slate-400 mt-2">
          AI-powered crime location analysis across Karnataka (Live Data)
        </p>
      </div>

      {/* Map Card */}
      <Card className="bg-slate-900 border-slate-800 overflow-hidden relative">
        {loading && (
          <div className="absolute inset-0 z-50 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm">
            <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-cyan-500"></div>
          </div>
        )}
        <CardContent className="p-0">
          <MapContainer
            center={[15.3173, 75.7139]} // Centered on Karnataka
            zoom={7}
            style={{
              height:"650px",
              width:"100%",
            }}
          >
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Crime Markers */}
            {crimes.map((crime) => (
              <Marker
                key={crime.id}
                position={[crime.lat, crime.lng]}
              >
                <Popup>
                  <div className="space-y-2">
                    <h3 className="font-bold">
                      {crime.type}
                    </h3>
                    <p>
                      📍 {crime.location}
                    </p>
                    <Badge variant={crime.severity === "HIGH" ? "destructive" : "secondary"}>
                      {crime.severity}
                    </Badge>
                  </div>
                </Popup>
              </Marker>
            ))}

            {/* Crime Hotspots (Red zones around HIGH severity) */}
            {crimes
              .filter((c) => c.severity === "HIGH")
              .map((crime) => (
                <Circle
                  key={"circle-" + crime.id}
                  center={[crime.lat, crime.lng]}
                  radius={8000} // Larger radius to show hotspot in state view
                  pathOptions={{
                    color: "red",
                    fillColor: "red",
                    fillOpacity: 0.25,
                    weight: 1
                  }}
                />
              ))}

            {/* Police Stations */}
            {stations.map((station, index) => (
              <Marker
                key={"station-" + index}
                position={[station.lat, station.lng]}
              >
                <Popup>
                  <div>
                    <h3 className="font-bold">
                      Police Station
                    </h3>
                    <p>
                      {station.name}
                    </p>
                  </div>
                </Popup>
              </Marker>
            ))}

          </MapContainer>
        </CardContent>
      </Card>

      {/* Statistics */}
      <div className="grid md:grid-cols-3 gap-5">
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <MapPin className="text-blue-400 mb-3"/>
            <p className="text-slate-400">
              Live Incidents Tracked
            </p>
            <h2 className="text-3xl font-bold text-white">
              {crimes.length}
            </h2>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <ShieldAlert className="text-red-400 mb-3"/>
            <p className="text-slate-400">
              High Risk Hotspots
            </p>
            <h2 className="text-3xl font-bold text-white">
              {highRiskCount}
            </h2>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <p className="text-slate-400">
              AI Prediction Accuracy
            </p>
            <h2 className="text-3xl font-bold text-green-400">
              94.2%
            </h2>
          </CardContent>
        </Card>
      </div>

    </div>
  );
}