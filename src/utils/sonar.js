const SIGNAL_LENGTH = 60;

function clamp01(value) {
  return Math.min(1, Math.max(0, value));
}

function roundTo3(value) {
  return Number(clamp01(value).toFixed(3));
}

function smoothSignal(values, smoothingFactor = 0.2) {
  const output = [...values];
  for (let index = 1; index < output.length - 1; index += 1) {
    const center = output[index] * (1 - smoothingFactor);
    const sides = ((output[index - 1] + output[index + 1]) / 2) * smoothingFactor;
    output[index] = center + sides;
  }
  return output;
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function getAverageDelta(values) {
  const deltas = [];
  for (let index = 1; index < values.length; index += 1) {
    deltas.push(Math.abs(values[index] - values[index - 1]));
  }
  return mean(deltas);
}

function getVariance(values, avg) {
  return mean(values.map((value) => (value - avg) ** 2));
}

function getPeak(values) {
  return Math.max(...values);
}

function normalize(raw, min, max) {
  if (max === min) {
    return 0;
  }
  return clamp01((raw - min) / (max - min));
}

function randomNoise(scale) {
  return (Math.random() - 0.5) * scale;
}

export function sanitizeNumericInput(rawValue) {
  const cleaned = rawValue.replace(/[^0-9.]/g, "");
  const firstDot = cleaned.indexOf(".");

  if (firstDot === -1) {
    return cleaned.slice(0, 4);
  }

  const whole = cleaned.slice(0, firstDot).slice(0, 1) || "0";
  const fractional = cleaned
    .slice(firstDot + 1)
    .replace(/\./g, "")
    .slice(0, 3);

  return `${whole}.${fractional}`;
}

export function generateMineSignal() {
  const phasePrimary = Math.random() * Math.PI;
  const phaseSecondary = Math.random() * Math.PI;

  const rawSignal = Array.from({ length: SIGNAL_LENGTH }, (_, index) => {
    const position = index / SIGNAL_LENGTH;
    const envelope = 0.7 + 0.2 * Math.sin(position * Math.PI);
    const wavePrimary = 0.17 * Math.sin(position * Math.PI * 3 + phasePrimary);
    const waveSecondary = 0.1 * Math.sin(position * Math.PI * 7 + phaseSecondary);
    const base = 0.58 + wavePrimary + waveSecondary;
    const structuredSignal = base * envelope + 0.12;
    return roundTo3(structuredSignal + randomNoise(0.04));
  });

  return smoothSignal(rawSignal, 0.33).map(roundTo3);
}

export function generateRockSignal() {
  const phasePrimary = Math.random() * Math.PI;
  const rawSignal = Array.from({ length: SIGNAL_LENGTH }, (_, index) => {
    const position = index / SIGNAL_LENGTH;
    const lowFrequency = 0.12 * Math.sin(position * Math.PI * 2.8 + phasePrimary);
    const roughness = 0.06 * Math.sin(position * Math.PI * 17);
    const jitter = index % 3 === 0 ? randomNoise(0.14) : randomNoise(0.08);
    const base = 0.33 + lowFrequency + roughness + jitter;
    return roundTo3(base);
  });

  return rawSignal.map(roundTo3);
}

export function validateSonarValues(values) {
  if (!Array.isArray(values) || values.length !== SIGNAL_LENGTH) {
    return "Exactly 60 sonar values are required.";
  }

  for (let index = 0; index < values.length; index += 1) {
    const numericValue = Number(values[index]);
    if (values[index] === "" || Number.isNaN(numericValue)) {
      return `Value ${index + 1} must be a valid number.`;
    }
    if (numericValue < 0 || numericValue > 1) {
      return `Value ${index + 1} must be between 0 and 1.`;
    }
  }

  return "";
}
