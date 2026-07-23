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


// Crime Data
const crimes = [
  {
    id: 1,
    type: "Armed Robbery",
    location: "Electronic City",
    lat: 12.8456,
    lng: 77.6603,
    severity: "HIGH",
  },

  {
    id: 2,
    type: "Vehicle Theft",
    location: "Whitefield",
    lat: 12.9698,
    lng: 77.7499,
    severity: "MEDIUM",
  },

  {
    id: 3,
    type: "Cyber Crime",
    location: "Koramangala",
    lat: 12.9352,
    lng: 77.6245,
    severity: "HIGH",
  },

  {
    id: 4,
    type: "Burglary",
    location: "Indiranagar",
    lat: 12.9719,
    lng: 77.6412,
    severity: "LOW",
  },
];


// Police Stations
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
];


export default function Heatmap() {

  return (

    <div className="space-y-6">


      {/* Header */}

      <div>

        <h1 className="text-4xl font-bold text-white">
          Crime Heatmap
        </h1>

        <p className="text-slate-400 mt-2">
          AI-powered crime location analysis across Bengaluru
        </p>

      </div>



      {/* Map Card */}

      <Card className="bg-slate-900 border-slate-800 overflow-hidden">

        <CardContent className="p-0">


          <MapContainer

            center={[12.9716,77.5946]}

            zoom={12}

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

            {crimes.map((crime)=>(

              <Marker

                key={crime.id}

                position={[
                  crime.lat,
                  crime.lng
                ]}

              >

                <Popup>


                  <div className="space-y-2">

                    <h3 className="font-bold">
                      {crime.type}
                    </h3>


                    <p>
                      📍 {crime.location}
                    </p>


                    <Badge>

                      {crime.severity}

                    </Badge>


                  </div>


                </Popup>


              </Marker>


            ))}



            {/* Crime Hotspots */}

            {crimes.map((crime)=>(

              <Circle

                key={
                  "circle-"+crime.id
                }

                center={[
                  crime.lat,
                  crime.lng
                ]}

                radius={500}

                pathOptions={{
                  color:"red",
                  fillColor:"red",
                  fillOpacity:0.25,
                }}

              />

            ))}



            {/* Police Stations */}

            {stations.map((station,index)=>(

              <Marker

                key={index}

                position={[
                  station.lat,
                  station.lng
                ]}

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
              Crime Locations
            </p>

            <h2 className="text-3xl font-bold text-white">
              248
            </h2>

          </CardContent>

        </Card>



        <Card className="bg-slate-900 border-slate-800">

          <CardContent className="p-6">

            <ShieldAlert className="text-red-400 mb-3"/>

            <p className="text-slate-400">
              High Risk Areas
            </p>

            <h2 className="text-3xl font-bold text-white">
              18
            </h2>

          </CardContent>

        </Card>



        <Card className="bg-slate-900 border-slate-800">

          <CardContent className="p-6">

            <p className="text-slate-400">
              AI Prediction Accuracy
            </p>

            <h2 className="text-3xl font-bold text-green-400">
              94%
            </h2>

          </CardContent>

        </Card>


      </div>


    </div>

  );
}