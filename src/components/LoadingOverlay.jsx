import { motion } from "framer-motion";

function LoadingOverlay() {
  return (
    <div className="absolute inset-0 z-20 flex items-center justify-center rounded-xl bg-black/70 backdrop-blur-sm">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1.3, ease: "linear" }}
        className="h-16 w-16 rounded-full border-4 border-neon-green/30 border-t-neon-green"
      />
      <p className="ml-4 animate-pulse text-sm text-neon-green">AI MODEL PROCESSING SONAR SIGNALS...</p>
    </div>
  );
}

export default LoadingOverlay;
