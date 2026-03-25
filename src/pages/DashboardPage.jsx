import { useMemo, useState } from "react";
import Button from "../components/Button";
import Card from "../components/Card";
import ChartsPanel from "../components/ChartsPanel";
import DebugPanel from "../components/DebugPanel";
import HistoryPanel from "../components/HistoryPanel";
import InputGrid from "../components/InputGrid";
import LoadingOverlay from "../components/LoadingOverlay";
import ResultCard from "../components/ResultCard";
import ThemeToggle from "../components/ThemeToggle";
import {
  generateMineSignal,
  generateRockSignal,
  runDetectionSimulation,
  sanitizeNumericInput,
  validateSonarValues,
} from "../utils/sonar";

function DashboardPage({ onBack, theme, onToggleTheme }) {
  const [mode, setMode] = useState("manual");
  const [signalType, setSignalType] = useState("manual");
  const [values, setValues] = useState(Array.from({ length: 60 }, () => ""));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const numericValues = useMemo(() => values.map((entry) => Number(entry) || 0), [values]);

  const handleInputChange = (index, rawValue) => {
    setSignalType("manual");
    const cleanValue = sanitizeNumericInput(rawValue);
    setValues((previous) => {
      const next = [...previous];
      next[index] = cleanValue;
      return next;
    });
  };

  const applySignal = (signalGenerator, nextSignalType) => {
    setMode("manual");
    setSignalType(nextSignalType);
    setValues(signalGenerator().map((num) => num.toFixed(3)));
    setError("");
  };

  const handleRunDetection = () => {
    const validationMessage = validateSonarValues(values);
    if (validationMessage) {
      setError(validationMessage);
      return;
    }

    setError("");
    setLoading(true);

    const processingDelay = 2000 + Math.floor(Math.random() * 1000);

    // Frontend-only AI simulation: no backend calls.
    window.setTimeout(() => {
      const output = runDetectionSimulation(values.map((entry) => Number(entry)));
      setResult(output);
      setHistory((previous) => [
        {
          time: new Date().toLocaleTimeString(),
          prediction: output.prediction,
          confidence: output.confidence,
          mineProbability: output.mineProbability,
          rockProbability: output.rockProbability,
        },
        ...previous,
      ]);

      if (output.prediction === "Mine") {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();
        oscillator.type = "square";
        oscillator.frequency.value = 680;
        gain.gain.value = 0.03;
        oscillator.connect(gain);
        gain.connect(audioContext.destination);
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.2);
      }

      setLoading(false);
    }, processingDelay);
  };

  return (
    <main className="relative z-10 px-4 py-5 md:px-8 md:py-7">
      <div className="mx-auto flex w-full max-w-7xl flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-neon-green md:text-2xl">AI Sonar Detection Dashboard</h1>
          <p className="text-xs text-slate-300">Submarine Rock vs Mine classification simulation</p>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
          <Button variant="ghost" onClick={onBack}>
            Back
          </Button>
        </div>
      </div>

      <div className="mx-auto mt-5 grid w-full max-w-7xl gap-4 xl:grid-cols-3">
        <div className="space-y-4 xl:col-span-2">
          <Card title="Sonar Input" subtitle="Use manual values or realistic mine/rock simulation presets" className="relative">
            {loading && <LoadingOverlay />}

            <div className="mb-3 flex flex-wrap items-center gap-2">
              <Button
                variant={mode === "manual" ? "primary" : "ghost"}
                onClick={() => {
                  setMode("manual");
                  setError("");
                }}
              >
                Manual Input
              </Button>
              <Button variant="ghost" onClick={() => applySignal(generateMineSignal, "mine") }>
                Generate Mine Signal
              </Button>
              <Button variant="ghost" onClick={() => applySignal(generateRockSignal, "rock") }>
                Generate Rock Signal
              </Button>
              <Button variant="primary" onClick={handleRunDetection} disabled={loading}>
                Run Detection
              </Button>
            </div>

            <p className="mb-3 text-xs text-neon-green/90">
              Using simulated realistic sonar data for prediction.
            </p>

            <InputGrid values={values} onChange={handleInputChange} mode={mode} />
            {error && <p className="mt-3 text-xs text-neon-red">{error}</p>}
          </Card>

          <ChartsPanel values={numericValues} signalType={signalType} />
          <DebugPanel values={numericValues} result={result} signalType={signalType} />
        </div>

        <div className="space-y-4">
          <ResultCard result={result} />
          <HistoryPanel history={history} />
        </div>
      </div>
    </main>
  );
}

export default DashboardPage;
