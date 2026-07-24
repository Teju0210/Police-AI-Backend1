import { motion } from "framer-motion";

export default function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-[#030712]">
      {/* Blue Glow */}
      <motion.div
        className="absolute w-150 h-150 rounded-full bg-cyan-500/20 blur-[120px]"
        animate={{
          x: [0, 200, 0],
          y: [0, 100, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        style={{
          top: "-150px",
          left: "-150px",
        }}
      />

      {/* Purple Glow */}
      <motion.div
        className="absolute w-125 h-125 rounded-full bg-blue-600/10 blur-[100px]"
        animate={{
          x: [0, -150, 0],
          y: [0, 150, 0],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        style={{
          bottom: "-120px",
          right: "-120px",
        }}
      />
    </div>
  );
}
