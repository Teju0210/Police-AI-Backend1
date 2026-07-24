import { motion } from "framer-motion";
import Tilt from "react-parallax-tilt";

import { Card, CardContent } from "@/components/ui/card";

export default function ChartCard({ title, children }) {
  return (
    <Tilt
      tiltMaxAngleX={8}
      tiltMaxAngleY={8}
      perspective={1200}
      transitionSpeed={1500}
      glareEnable={true}
      glareMaxOpacity={0.15}
      glareColor="#38bdf8"
      glarePosition="all"
    >
      <motion.div
        initial={{ opacity: 0, y: 25 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        whileHover={{
          y: -8,
          scale: 1.02,
        }}
      >
        <Card
          className="
          relative
          overflow-hidden
          rounded-3xl

          border
          border-cyan-500/20

          bg-white/5

          backdrop-blur-2xl

          shadow-[0_0_30px_rgba(59,130,246,0.12)]

          transition-all
          duration-500

          hover:border-cyan-400/40
          hover:shadow-[0_0_50px_rgba(34,211,238,0.25)]
        "
        >
          {/* Animated Glow 1 */}
          <motion.div
            className="
            absolute
            -top-24
            -left-24
            h-56
            w-56
            rounded-full
            bg-cyan-500/20
            blur-[90px]
            "
            animate={{
              x: [0, 40, 0],
              y: [0, 20, 0],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />

          {/* Animated Glow 2 */}
          <motion.div
            className="
            absolute
            -bottom-24
            -right-24
            h-56
            w-56
            rounded-full
            bg-blue-600/20
            blur-[90px]
            "
            animate={{
              x: [0, -40, 0],
              y: [0, -20, 0],
            }}
            transition={{
              duration: 12,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />

          <CardContent className="relative z-10 p-6">

            <div className="mb-6 flex items-center justify-between">

              <h2 className="text-xl font-bold tracking-wide text-white">
                {title}
              </h2>

              <motion.div
                animate={{
                  scale: [1, 1.6, 1],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                }}
                className="
                h-3
                w-3
                rounded-full
                bg-cyan-400
                shadow-[0_0_15px_#22d3ee]
                "
              />

            </div>

            {children}

          </CardContent>
        </Card>
      </motion.div>
    </Tilt>
  );
}
