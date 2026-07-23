import {
  ShieldAlert,
  CheckCircle2,
  MapPinned,
  Users,
  FileText,
  Brain,
} from "lucide-react";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


import HeroBanner from "../../components/dashboard/HeroBanner";
import StatsCard from "../../components/dashboard/StatsCard";
import ChartCard from "../../components/dashboard/ChartCard";
import AlertCard from "../../components/dashboard/AlertCard";


const stats = [
  {
    title: "Total Crimes",
    value: "1248",
    icon: ShieldAlert,
    color: "text-red-400",
    link: "/reports",
  },

  {
    title: "Solved Cases",
    value: "87%",
    icon: CheckCircle2,
    color: "text-green-400",
    link: "/analytics",
  },

  {
    title: "Crime Hotspots",
    value: "18",
    icon: MapPinned,
    color: "text-yellow-400",
    link: "/heatmap",
  },

  {
    title: "Active Officers",
    value: "245",
    icon: Users,
    color: "text-blue-400",
    link: "/network",
  },
];


const crimeTrend = [
  {
    month:"Jan",
    crimes:80
  },
  {
    month:"Feb",
    crimes:120
  },
  {
    month:"Mar",
    crimes:100
  },
  {
    month:"Apr",
    crimes:160
  },
  {
    month:"May",
    crimes:140
  },
  {
    month:"Jun",
    crimes:190
  },
];


const crimeCategory = [
  {
    name:"Robbery",
    cases:45
  },
  {
    name:"Cyber",
    cases:70
  },
  {
    name:"Fraud",
    cases:35
  },
  {
    name:"Theft",
    cases:60
  },
];



export default function Dashboard(){


return (

<div className="space-y-8">


{/* HERO */}

<HeroBanner />





{/* STATS */}

<div
className="
grid
grid-cols-1
md:grid-cols-2
xl:grid-cols-4
gap-6
"
>


{
stats.map((item)=>(

<StatsCard

key={item.title}

{...item}

/>

))
}


</div>







{/* CHARTS */}


<div
className="
grid
grid-cols-1
xl:grid-cols-2
gap-6
"
>



<ChartCard title="Crime Trend Analysis">


<div className="h-80">


<ResponsiveContainer
width="100%"
height="100%"
>


<LineChart data={crimeTrend}>


<XAxis dataKey="month"/>

<YAxis/>


<Tooltip/>


<Line

type="monotone"

dataKey="crimes"

stroke="#22d3ee"

strokeWidth={3}

/>


</LineChart>


</ResponsiveContainer>


</div>


</ChartCard>







<ChartCard title="Crime Categories">


<div className="h-80">


<ResponsiveContainer
width="100%"
height="100%"
>


<BarChart data={crimeCategory}>


<XAxis dataKey="name"/>

<YAxis/>


<Tooltip/>


<Bar

dataKey="cases"

fill="#3b82f6"

/>


</BarChart>


</ResponsiveContainer>


</div>


</ChartCard>



</div>








{/* AI INSIGHTS */}


<ChartCard title="AI Intelligence Insights">


<div className="space-y-4">


<div
className="
rounded-xl
border
border-red-500/20
bg-red-500/10
p-4
"
>

<div className="flex gap-3 items-center">

<ShieldAlert className="text-red-400"/>

<h3 className="text-white font-bold">
Risk Alert
</h3>

</div>


<p className="text-slate-300 mt-2">
Robbery cases increased in Bengaluru zones.
</p>


</div>





<div
className="
rounded-xl
border
border-cyan-500/20
bg-cyan-500/10
p-4
"
>


<div className="flex gap-3 items-center">

<Brain className="text-cyan-400"/>

<h3 className="text-white font-bold">
AI Prediction
</h3>

</div>


<p className="text-slate-300 mt-2">
AI model detected possible crime hotspots.
</p>


</div>


</div>


</ChartCard>








{/* ALERTS */}


<ChartCard title="Live Crime Alerts">


<AlertCard

title="Armed Robbery"

location="Electronic City"

time="2 mins ago"

color="text-red-400"

/>


<AlertCard

title="Cyber Fraud"

location="Whitefield"

time="15 mins ago"

color="text-yellow-400"

/>


<AlertCard

title="Vehicle Theft"

location="Koramangala"

time="30 mins ago"

color="text-blue-400"

/>


</ChartCard>






</div>


);


}