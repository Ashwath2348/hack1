import { motion } from "framer-motion";
import Button from "../components/Button";
import ThemeToggle from "../components/ThemeToggle";

function LandingPage({ onStart, theme, onToggleTheme }) {
  return (
    <main className="relative z-10 flex min-h-screen flex-col px-4 py-8 md:px-10">
      <div className="mb-12 flex justify-end">
        <ThemeToggle theme={theme} onToggle={onToggleTheme} />
      </div>

      <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col items-center justify-center text-center">
        <motion.h1
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-3xl font-bold tracking-wide text-neon-green md:text-5xl"
        >
          AI Sonar Detection System
        </motion.h1>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="mt-4 max-w-xl text-sm text-slate-300 md:text-base"
        >
          Detect Underwater Threats Using AI
        </motion.p>

        <motion.div
          initial={{ scale: 0.92, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mt-10 flex h-56 w-56 items-center justify-center rounded-full border border-neon-green/40 bg-neon-green/5 shadow-glow md:h-72 md:w-72"
        >
          <div className="relative h-40 w-40 rounded-full border border-neon-green/40">
            <div className="absolute inset-0 animate-sonarSweep rounded-full bg-gradient-to-r from-neon-green/35 to-transparent" />
          </div>
        </motion.div>

        <Button onClick={onStart} className="mt-10 px-8 py-3 text-base">
          Start Mission Dashboard
        </Button>
      </div>
    </main>
  );
}

export default LandingPage;
