import { motion } from "framer-motion";
import Card from "./Card";

function ResultCard({ result }) {
  if (!result) {
    return (
      <Card title="Detection Result" subtitle="Run detection to view current prediction">
        <p className="text-sm text-slate-300">Awaiting sonar processing...</p>
      </Card>
    );
  }

  const isMine = result.prediction === "Mine";

  return (
    <Card title="Detection Result" subtitle="AI classification output">
      <motion.div
        initial={{ opacity: 0.4, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`rounded-lg border p-4 ${
          isMine
            ? "animate-alertFlash border-neon-red/70 bg-neon-red/10 shadow-glow-red"
            : "border-neon-green/50 bg-neon-green/10 shadow-glow"
        }`}
      >
        <p className="text-xs uppercase tracking-widest text-slate-300">Prediction</p>
        <p className={`text-3xl font-bold ${isMine ? "text-neon-red" : "text-neon-green"}`}>
          {result.prediction}
        </p>
        <p className="mt-2 text-sm text-slate-200">Confidence: {result.confidence}%</p>
        <div className="mt-3 space-y-2">
          <div>
            <div className="mb-1 flex justify-between text-[11px] text-slate-300">
              <span>Mine Probability</span>
              <span>{result.mineProbability}%</span>
            </div>
            <div className="h-2 rounded bg-slate-700/70">
              <div
                className="h-2 rounded bg-neon-red transition-all duration-500"
                style={{ width: `${result.mineProbability}%` }}
              />
            </div>
          </div>

          <div>
            <div className="mb-1 flex justify-between text-[11px] text-slate-300">
              <span>Rock Probability</span>
              <span>{result.rockProbability}%</span>
            </div>
            <div className="h-2 rounded bg-slate-700/70">
              <div
                className="h-2 rounded bg-neon-green transition-all duration-500"
                style={{ width: `${result.rockProbability}%` }}
              />
            </div>
          </div>
        </div>
        {isMine && <p className="mt-2 text-xs text-neon-red">⚠ ALERT: Potential underwater mine detected.</p>}
      </motion.div>
    </Card>
  );
}

export default ResultCard;
