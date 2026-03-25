import { useMemo } from "react";

function InputGrid({ values, onChange, mode }) {
  const totalCells = useMemo(() => Array.from({ length: 60 }, (_, index) => index), []);

  return (
    <div className="grid grid-cols-5 gap-2 sm:grid-cols-6 md:grid-cols-10">
      {totalCells.map((index) => (
        <input
          key={index}
          value={values[index]}
          onChange={(event) => onChange(index, event.target.value)}
          disabled={mode !== "manual"}
          className="h-9 rounded border border-neon-green/30 bg-command-800/70 px-2 text-center text-xs text-slate-100 outline-none ring-neon-green transition focus:ring-2 disabled:opacity-50"
          inputMode="decimal"
          min="0"
          max="1"
          step="0.001"
          placeholder={`${index + 1}`}
          aria-label={`Sonar value ${index + 1}`}
        />
      ))}
    </div>
  );
}

export default InputGrid;
