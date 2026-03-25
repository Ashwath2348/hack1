import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Card from "./Card";

function ChartsPanel({ values, signalType }) {
  const lineData = values.map((value, index) => ({
    index: index + 1,
    signal: Number(value) || 0,
  }));

  const barData = Array.from({ length: 6 }, (_, chunkIndex) => {
    const chunk = lineData.slice(chunkIndex * 10, chunkIndex * 10 + 10);
    const avg = chunk.reduce((sum, entry) => sum + entry.signal, 0) / (chunk.length || 1);
    return { segment: `S${chunkIndex + 1}`, intensity: Number(avg.toFixed(2)) };
  });

  const lineColor = signalType === "mine" ? "#ff4b6e" : "#38f89a";
  const barColor = signalType === "mine" ? "#fb7185" : "#22d3ee";

  return (
    <Card title="Signal Visualization" subtitle="Real-time sonar feature view">
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="h-52 w-full rounded-lg border border-neon-green/20 bg-command-800/40 p-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1c3c32" />
              <XAxis dataKey="index" stroke="#94a3b8" tick={{ fontSize: 10 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 10 }} domain={[0, 1]} />
              <Tooltip
                contentStyle={{ background: "#071018", border: "1px solid rgba(56,248,154,0.35)" }}
              />
              <Line
                type="monotone"
                dataKey="signal"
                stroke={lineColor}
                strokeWidth={2}
                dot={false}
                isAnimationActive
                animationDuration={1400}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="h-52 w-full rounded-lg border border-neon-green/20 bg-command-800/40 p-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1c3c32" />
              <XAxis dataKey="segment" stroke="#94a3b8" tick={{ fontSize: 10 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 10 }} domain={[0, 1]} />
              <Tooltip
                contentStyle={{ background: "#071018", border: "1px solid rgba(56,248,154,0.35)" }}
              />
              <Bar dataKey="intensity" fill={barColor} radius={[4, 4, 0, 0]} isAnimationActive animationDuration={1200} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Card>
  );
}

export default ChartsPanel;
