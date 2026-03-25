const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export async function predictSonarFeatures(features) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ features }),
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload?.error || "Prediction request failed.");
  }

  return payload;
}

export async function fetchPredictionHistory() {
  const response = await fetch(`${API_BASE_URL}/history`);
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload?.error || "Failed to fetch backend history.");
  }

  return payload;
}
