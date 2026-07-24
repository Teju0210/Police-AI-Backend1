import { Mic } from "lucide-react";

export default function VoiceButton() {

  const startListening = () => {

    const recognition =
      new window.webkitSpeechRecognition();

    recognition.lang = "en-IN";

    recognition.start();

    recognition.onresult = (event) => {
      alert(event.results[0][0].transcript);
    };

  };

  return (
    <button
      onClick={startListening}
      className="bg-red-600 hover:bg-red-700 rounded-xl p-4"
    >
      <Mic />
    </button>
  );
}
