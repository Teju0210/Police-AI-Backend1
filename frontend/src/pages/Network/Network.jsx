import { useState, useEffect } from "react";
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


export default function Network(){
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNetwork() {
      try {
        const res = await fetch("http://localhost:8000/dashboard/network");
        const data = await res.json();
        
        if (data.nodes && data.edges) {
          // ReactFlow requires labels inside data to be strings or React nodes.
          // Since we sent strings with \n from the backend, we convert them to simple HTML to render multiline
          const formattedNodes = data.nodes.map(n => ({
            ...n,
            data: {
              ...n.data,
              label: (
                <div style={{ textAlign: "center" }}>
                  {n.data.label.split('\n').map((line, i) => (
                    <div key={i} style={i === 0 ? { fontWeight: "bold", marginBottom: "4px" } : { fontSize: "11px" }}>
                      {line}
                    </div>
                  ))}
                </div>
              )
            }
          }));
          
          setNodes(formattedNodes);
          setEdges(data.edges);
        }
      } catch (err) {
        console.error("Failed to fetch criminal network:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchNetwork();
  }, []);


  return(

    <div className="space-y-6">


      <div>

        <h1 className="text-4xl font-bold text-white flex items-center gap-3">

          <NetworkIcon className="text-blue-500"/>

          Repeated Offenders Visualization

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