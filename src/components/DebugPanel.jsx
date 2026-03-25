import Card from "./Card";

function DebugPanel({ values, result, signalType }) {
  return (
    <Card title="Debug Panel" subtitle="Simulation diagnostics (frontend-only)">
      <div className="space-y-3 text-xs text-slate-200">
        <div className="rounded border border-neon-green/20 bg-command-800/55 p-2">
          <p className="text-[11px] uppercase tracking-wider text-neon-green">Signal Profile</p>
          <p className="mt-1">
            {signalType === "mine"
              ? "Preset Mine Signal"
              : signalType === "rock"
                ? "Preset Rock Signal"
                : "Manual/Custom Signal"}
          </p>
        </div>

        <div className="rounded border border-neon-green/20 bg-command-800/55 p-2">
          <p className="text-[11px] uppercase tracking-wider text-neon-green">Raw Input Array</p>
          <p className="mt-1 max-h-20 overflow-auto break-words text-[11px] text-slate-300">
            [{values.map((value) => value.toFixed(3)).join(", ")}]
          </p>
        </div>

        <div className="rounded border border-neon-green/20 bg-command-800/55 p-2">
          <p className="text-[11px] uppercase tracking-wider text-neon-green">Simulated Probabilities</p>
          <p className="mt-1 text-slate-300">
            Mine: {result ? `${result.mineProbability}%` : "--"} | Rock: {result ? `${result.rockProbability}%` : "--"}
          </p>
          <p className="mt-1 text-slate-300">
            Signal Nature: {result?.debug?.signalNature || "--"} | Fallback Rule: {result?.debug?.fallbackPrediction || "--"}
          </p>
        </div>
      </div>
    </Card>
  );
}

export default DebugPanel;
