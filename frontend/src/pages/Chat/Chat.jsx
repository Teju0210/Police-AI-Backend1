import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

import {
  Bot,
  User,
  Mic,
  Send,
  Sparkles,
  Loader2
} from "lucide-react";

import api from "../../services/api";

import {
  Card,
  CardContent,
} from "@/components/ui/card";

import {
  Button
} from "@/components/ui/button";

import {
  Badge
} from "@/components/ui/badge";

import {
  ScrollArea
} from "@/components/ui/scroll-area";


export default function Chat() {

  const [messages, setMessages] = useState([
    {
      sender:"ai",
      text:"Hello Officer. I am CrimeVision AI. How can I assist with your investigation today?",
      time:"Now",
    },
  ]);


  const [input,setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const chatEnd = useRef(null);


  useEffect(()=>{

    chatEnd.current?.scrollIntoView({
      behavior:"smooth"
    });

  },[messages]);



  const sendMessage = async () => {

    if(!input.trim()) return;


    const userMessage = {
      sender:"user",
      text:input,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev=>[...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      if (input.startsWith("/fir ")) {
        const summary = input.replace("/fir ", "");
        const res = await api.post("/ai/draft_fir", { raw_summary: summary });
        setMessages(prev=>[
          ...prev,
          {
            sender:"ai",
            text: res.data.response,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      } else {
        const res = await api.post("/ai/chat", { message: input });
        
        setMessages(prev=>[
          ...prev,
          {
            sender:"ai",
            text: res.data.response,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      }
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev=>[
        ...prev,
        {
          sender:"ai",
          text: "Error connecting to AI backend. Please try again.",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setIsTyping(false);
    }

  };



  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support Speech Recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(prev => (prev + " " + transcript).trim());
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const suggestions=[

    "Show recent crime trends",

    "Find suspect connections",

    "Analyze FIR report",

    "Predict crime hotspots",

    "/fir "

  ];



  return (

    <div className="space-y-6">


      <div>

        <h1 className="text-4xl font-bold text-white flex items-center gap-3">

          <Bot className="text-blue-500"/>

          CrimeVision AI Assistant

        </h1>


        <p className="text-slate-400 mt-2">

          Intelligent crime investigation assistant

        </p>

      </div>



      <Card className="bg-slate-900 border-slate-800">


        <CardContent className="p-0">


          <ScrollArea className="h-[500px] p-6">


            <div className="space-y-5">


              {messages.map((msg,index)=>(


                <div

                  key={index}

                  className={`flex gap-3 ${
                    msg.sender==="user"
                    ?"justify-end"
                    :"justify-start"
                  }`}

                >


                  {msg.sender==="ai" && (

                    <div className="bg-blue-600 p-3 rounded-full h-fit">

                      <Bot size={22}/>

                    </div>

                  )}



                  <div

                    className={`max-w-lg p-4 rounded-2xl ${
                      
                      msg.sender==="user"

                      ?"bg-blue-600 text-white"

                      :"bg-slate-800 text-slate-200"

                    }`}

                  >

                    <div className="text-sm">
                      <ReactMarkdown>{msg.text}</ReactMarkdown>
                    </div>

                    <p className="text-xs opacity-60 mt-2">
                      {msg.time}
                    </p>

                  </div>



                  {msg.sender==="user" && (

                    <div className="bg-slate-700 p-3 rounded-full h-fit">

                      <User size={22}/>

                    </div>

                  )}



                </div>


              ))}

              {isTyping && (
                <div className="flex gap-3 justify-start">
                  <div className="bg-blue-600 p-3 rounded-full h-fit">
                    <Bot size={22}/>
                  </div>
                  <div className="max-w-lg p-4 rounded-2xl bg-slate-800 text-slate-200 flex items-center gap-2">
                    <Loader2 size={18} className="animate-spin text-cyan-400" />
                    <p className="text-sm opacity-80">AI is thinking...</p>
                  </div>
                </div>
              )}

              <div ref={chatEnd}/>


            </div>


          </ScrollArea>



          <div className="border-t border-slate-800 p-4">


            <div className="flex flex-wrap gap-2 mb-4">


              {suggestions.map((item)=>(

                <Badge

                  key={item}

                  className="cursor-pointer bg-slate-800 hover:bg-blue-600"

                  onClick={()=>setInput(item)}

                >

                  {item}

                </Badge>

              ))}


            </div>



            <div className="flex gap-3">


              <Button

                variant="outline"

                className={`border-slate-700 ${isListening ? "bg-red-500 text-white hover:bg-red-600 animate-pulse" : ""}`}

                onClick={startListening}

              >

                <Mic size={20}/>

              </Button>



              <input

                value={input}

                onChange={(e)=>setInput(e.target.value)}

                onKeyDown={(e)=>{

                  if(e.key==="Enter")
                    sendMessage();

                }}

                placeholder="Ask CrimeVision AI..."

                className="
                flex-1
                bg-slate-800
                border
                border-slate-700
                rounded-xl
                px-4
                text-white
                outline-none
                focus:border-blue-500
                "

              />



              <Button

                onClick={sendMessage}

                className="bg-blue-600 hover:bg-blue-700"

              >

                <Send size={20}/>

              </Button>


            </div>


          </div>


        </CardContent>


      </Card>


    </div>

  );

}