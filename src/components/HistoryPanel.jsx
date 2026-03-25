import Card from "./Card";

function HistoryPanel({ history }) {
  return (
    <Card title="Detection History" subtitle="Latest AI sonar decisions">
      {history.length === 0 ? (
        <p className="text-sm text-slate-300">No detections recorded yet.</p>
      ) : (
        <div className="max-h-72 overflow-auto">
          <table className="w-full text-left text-xs text-slate-200">
            <thead className="sticky top-0 bg-command-900 text-slate-400">
              <tr>
                <th className="px-2 py-2">Time</th>
                <th className="px-2 py-2">Prediction</th>
                <th className="px-2 py-2">Confidence</th>
                <th className="px-2 py-2">Mine %</th>
                <th className="px-2 py-2">Rock %</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item, index) => (
                <tr key={`${item.time}-${index}`} className="border-t border-neon-green/10">
                  <td className="px-2 py-2">{item.time}</td>
                  <td className={`px-2 py-2 font-semibold ${item.prediction === "Mine" ? "text-neon-red" : "text-neon-green"}`}>
                    {item.prediction}
                  </td>
                  <td className="px-2 py-2">{item.confidence}%</td>
                  <td className="px-2 py-2 text-neon-red">{item.mineProbability}%</td>
                  <td className="px-2 py-2 text-neon-green">{item.rockProbability}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}

export default HistoryPanel;
