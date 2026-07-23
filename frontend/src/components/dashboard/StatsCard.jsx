import { motion } from "framer-motion";
import CountUp from "react-countup";
import Tilt from "react-parallax-tilt";
import { useNavigate } from "react-router-dom";

import { Card, CardContent } from "@/components/ui/card";

export default function StatsCard({
  title,
  value,
  icon: Icon,
  color,
  link,
}) {
  const navigate = useNavigate();

  // Extract only numbers for CountUp
  const numericValue = parseInt(
    String(value).replace(/[^0-9]/g, "")
  );

  const isPercentage = String(value).includes("%");

  return (
    <Tilt
      tiltMaxAngleX={8}
      tiltMaxAngleY={8}
      perspective={1200}
      transitionSpeed={1500}
      glareEnable
      glareMaxOpacity={0.15}
      glareColor="#38bdf8"
    >
      <motion.div
        initial={{ opacity: 0, y: 25 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        whileHover={{
          y: -8,
          scale: 1.02,
        }}
        transition={{ duration: 0.5 }}
      >
        <Card
          onClick={() => link && navigate(link)}
          className="
            relative
            cursor-pointer
            overflow-hidden
            rounded-3xl
            border
            border-white/10
            bg-white/5
            backdrop-blur-xl
            transition-all
            duration-300
            hover:border-cyan-500/40
            hover:shadow-[0_0_35px_rgba(34,211,238,0.25)]
          "
        >
          {/* Glow */}
          <div className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-cyan-500/20 blur-3xl" />

          <CardContent className="relative z-10 p-6">
            <div className="flex items-center justify-between">

              <motion.div
                animate={{
                  y: [0, -5, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                }}
                className={color}
              >
                <Icon size={34} />
              </motion.div>

              <div className="h-3 w-3 rounded-full bg-green-400 animate-pulse" />

            </div>

            <h4 className="mt-5 text-sm text-slate-400">
              {title}
            </h4>

            <h2 className="mt-2 text-3xl font-bold text-white">
              {value}
            </h2>

            <p className="mt-4 text-xs text-cyan-400">
              Click to view details →
            </p>

          </CardContent>
        </Card>
      </motion.div>
    </Tilt>
  );
}