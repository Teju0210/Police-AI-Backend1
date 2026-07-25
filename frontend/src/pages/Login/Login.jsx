import { Shield, Lock, User } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [officerId, setOfficerId] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!officerId || !password) {
      alert("Please enter Officer ID and Password");
      return;
    }

    // Temporary login
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("officerName", officerId);

    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-6">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">

        <div className="flex justify-center mb-6">
          <div className="bg-blue-600 p-4 rounded-full">
            <Shield size={36} className="text-white" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-white text-center">
          CrimeVision Analytics
        </h1>



        <form onSubmit={handleLogin} className="mt-8 space-y-5">

          <div className="relative">
            <User className="absolute left-3 top-3.5 text-slate-400" size={20} />

            <input
              type="text"
              placeholder="Officer ID"
              value={officerId}
              onChange={(e) => setOfficerId(e.target.value)}
              className="w-full pl-11 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white outline-none focus:border-blue-500"
            />
          </div>

          <div className="relative">
            <Lock className="absolute left-3 top-3.5 text-slate-400" size={20} />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-11 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white outline-none focus:border-blue-500"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg text-white font-semibold transition"
          >
            Secure Login
          </button>

        </form>
      </div>
    </div>
  );
}
