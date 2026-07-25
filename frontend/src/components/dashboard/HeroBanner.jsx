import {
  Shield,
  Brain,
  Bell,
  Sparkles,
} from "lucide-react";

import { motion } from "framer-motion";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function HeroBanner() {
  const officer =
    localStorage.getItem("officerName") || "Officer";

  const today = new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.8,
        ease: "easeOut",
      }}
    >
      <Card
        className="
          relative
          overflow-hidden
          rounded-3xl
          border
          border-cyan-500/20
          bg-gradient-to-r
          from-slate-950
          via-slate-900
          to-blue-950
          shadow-[0_0_60px_rgba(59,130,246,0.25)]
          backdrop-blur-xl
        "
      >
        {/* Animated Glow */}
        <div className="absolute inset-0">

          <motion.div
            className="absolute -top-28 -left-28 h-80 w-80 rounded-full bg-cyan-500/20 blur-[120px]"
            animate={{
              x: [0, 60, 0],
              y: [0, 40, 0],
            }}
            transition={{
              duration: 12,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />

          <motion.div
            className="absolute -bottom-28 -right-28 h-80 w-80 rounded-full bg-blue-600/20 blur-[120px]"
            animate={{
              x: [0, -60, 0],
              y: [0, -40, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />

        </div>

        <CardContent className="relative z-10 p-8">

          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">

            {/* Left Section */}
            <div>

              <Badge className="mb-4 bg-cyan-600 hover:bg-cyan-500">
                🚔 CrimeVision AI
              </Badge>

              <h1 className="text-4xl font-extrabold text-white">
                Welcome, {officer} 👮
              </h1>

              <p className="mt-3 text-lg text-slate-300">
                Karnataka Police Crime Analytics
              </p>

              <p className="mt-2 text-slate-400">
                {today}
              </p>

            </div>

            {/* Right Stats */}
            <div className="grid grid-cols-2 gap-4">

              <motion.div
                whileHover={{
                  scale: 1.05,
                  y: -5,
                }}
                className="
                  rounded-2xl
                  border
                  border-cyan-500/20
                  bg-slate-900/50
                  p-5
                  text-center
                  backdrop-blur-md
                "
              >
                <Shield
                  className="mx-auto mb-2 text-cyan-400"
                  size={34}
                />

                <p className="text-3xl font-bold text-white">
                  86
                </p>

                <p className="text-sm text-slate-400">
                  Active Cases
                </p>

              </motion.div>

              <motion.div
                whileHover={{
                  scale: 1.05,
                  y: -5,
                }}
                className="
                  rounded-2xl
                  border
                  border-red-500/20
                  bg-slate-900/50
                  p-5
                  text-center
                  backdrop-blur-md
                "
              >
                <Bell
                  className="mx-auto mb-2 text-red-400"
                  size={34}
                />

                <p className="text-3xl font-bold text-white">
                  12
                </p>

                <p className="text-sm text-slate-400">
                  Alerts
                </p>

              </motion.div>

              <motion.div
                whileHover={{
                  scale: 1.05,
                  y: -5,
                }}
                className="
                  rounded-2xl
                  border
                  border-green-500/20
                  bg-slate-900/50
                  p-5
                  text-center
                  backdrop-blur-md
                "
              >
                <Brain
                  className="mx-auto mb-2 text-green-400"
                  size={34}
                />

                <p className="text-3xl font-bold text-white">
                  94%
                </p>

                <p className="text-sm text-slate-400">
                  AI Accuracy
                </p>

              </motion.div>

              <motion.div
                whileHover={{
                  scale: 1.05,
                  y: -5,
                }}
                className="
                  rounded-2xl
                  border
                  border-yellow-500/20
                  bg-slate-900/50
                  p-5
                  text-center
                  backdrop-blur-md
                "
              >
                <Sparkles
                  className="mx-auto mb-2 text-yellow-400"
                  size={34}
                />

                <p className="text-3xl font-bold text-white">
                  LIVE
                </p>

                <p className="text-sm text-slate-400">
                  Monitoring
                </p>

              </motion.div>

            </div>

          </div>

        </CardContent>

      </Card>
    </motion.div>
  );
}
