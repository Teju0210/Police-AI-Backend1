import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from "reactflow";

import "reactflow/dist/style.css";

import {
  Card,
  CardContent,
} from "@/components/ui/card";

import {
  Badge
} from "@/components/ui/badge";

import {
  Network as NetworkIcon,
  ShieldAlert,
  Users,
} from "lucide-react";


const nodes = [

  {
    id: "1",
    position: { x: 300, y: 50 },
    data: {
      label: (
        <div>
          <b>Rahul Kumar</b>
          <br />
          <span>Primary Suspect</span>
        </div>
      ),
    },
    style: {
      background:"#dc2626",
      color:"white",
      borderRadius:"12px",
      padding:"12px",
      border:"2px solid #ef4444",
    },
  },


  {
    id:"2",
    position:{x:100,y:200},
    data:{
      label:(
        <div>
          <b>Arjun Singh</b>
          <br/>
          Associate
        </div>
      )
    },
    style:{
      background:"#1e293b",
      color:"white",
      borderRadius:"12px",
      padding:"12px",
    },
  },


  {
    id:"3",
    position:{x:500,y:200},
    data:{
      label:(
        <div>
          <b>Gang Alpha</b>
          <br/>
          Organization
        </div>
      )
    },
    style:{
      background:"#2563eb",
      color:"white",
      borderRadius:"12px",
      padding:"12px",
    },
  },


  {
    id:"4",
    position:{x:300,y:350},
    data:{
      label:(
        <div>
          <b>Vehicle Owner</b>
          <br/>
          Evidence Link
        </div>
      )
    },
    style:{
      background:"#16a34a",
      color:"white",
      borderRadius:"12px",
      padding:"12px",
    },
  },


];


const edges = [

  {
    id:"e1-2",
    source:"1",
    target:"2",
    label:"Contact",
    animated:true,
  },

  {
    id:"e1-3",
    source:"1",
    target:"3",
    label:"Member",
    animated:true,
  },

  {
    id:"e1-4",
    source:"1",
    target:"4",
    label:"Evidence",
  },

];


export default function Network(){

  return(

    <div className="space-y-6">


      <div>

        <h1 className="text-4xl font-bold text-white flex items-center gap-3">

          <NetworkIcon className="text-blue-500"/>

          Criminal Network Visualization

        </h1>


        <p className="text-slate-400 mt-2">

          AI-powered relationship analysis between suspects and evidence

        </p>

      </div>



      <Card className="bg-slate-900 border-slate-800">

        <CardContent className="p-0">


          <div
            style={{
              height:"650px",
              width:"100%"
            }}
          >

            <ReactFlow

              nodes={nodes}

              edges={edges}

              fitView

            >

              <Background />

              <Controls />

              <MiniMap />

            </ReactFlow>


          </div>


        </CardContent>

      </Card>



      <div className="grid md:grid-cols-3 gap-5">


        <Card className="bg-slate-900 border-slate-800">

          <CardContent className="p-6">

            <Users className="text-blue-400 mb-3"/>

            <p className="text-slate-400">
              Connected Persons
            </p>

            <h2 className="text-3xl text-white font-bold">
              24
            </h2>

          </CardContent>

        </Card>



        <Card className="bg-slate-900 border-slate-800">

          <CardContent className="p-6">

            <ShieldAlert className="text-red-400 mb-3"/>

            <p className="text-slate-400">
              Risk Level
            </p>

            <Badge className="mt-2 bg-red-600">
              HIGH
            </Badge>

          </CardContent>

        </Card>



        <Card className="bg-slate-900 border-slate-800">

          <CardContent className="p-6">

            <p className="text-slate-400">
              AI Confidence
            </p>

            <h2 className="text-3xl text-green-400 font-bold">
              94%
            </h2>

          </CardContent>

        </Card>


      </div>


    </div>

  );

}