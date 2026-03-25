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
  sanitizeNumericInput,
  validateSonarValues,
} from "../utils/sonar";
import { fetchPredictionHistory, predictSonarFeatures } from "../utils/api";

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

  const handleRunDetection = async () => {
    const validationMessage = validateSonarValues(values);
    if (validationMessage) {
      setError(validationMessage);
      return;
    }

    setError("");
    setLoading(true);

    try {
      const features = values.map((entry) => Number(entry));
      const output = await predictSonarFeatures(features);
      const normalizedResult = {
        prediction: output.prediction,
        confidence: output.confidence,
        mineProbability: Math.round(output.probabilities.mine * 100),
        rockProbability: Math.round(output.probabilities.rock * 100),
        debug: {
          ...output.debug,
          fallbackPrediction: output?.debug?.fallbackRule,
        },
      };

      setResult(normalizedResult);
      console.log("[FRONTEND] Prediction response:", output);

      setHistory((previous) => [
        {
          time: output.timestamp ? new Date(output.timestamp).toLocaleTimeString() : new Date().toLocaleTimeString(),
          prediction: normalizedResult.prediction,
          confidence: normalizedResult.confidence,
          mineProbability: normalizedResult.mineProbability,
          rockProbability: normalizedResult.rockProbability,
        },
        ...previous,
      ]);

      if (normalizedResult.prediction === "Mine") {
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

      const backendHistory = await fetchPredictionHistory();
      if (backendHistory?.items?.length) {
        setHistory(
          backendHistory.items.slice(0, 10).map((item) => ({
            time: item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : "--",
            prediction: item.prediction,
            confidence: item.confidence,
            mineProbability: Math.round(item.probabilities.mine * 100),
            rockProbability: Math.round(item.probabilities.rock * 100),
          }))
        );
      }
    } catch (requestError) {
      setError(requestError.message || "Backend prediction failed.");
    } finally {
      setLoading(false);
    }
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
              Using realistic sonar patterns as input. Prediction generated using backend model.
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
