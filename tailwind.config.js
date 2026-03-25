/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        command: {
          950: "#040607",
          900: "#071018",
          800: "#0d1b26",
        },
        neon: {
          green: "#38f89a",
          red: "#ff4b6e",
          blue: "#22d3ee",
        },
      },
      boxShadow: {
        glow: "0 0 0.75rem rgba(56, 248, 154, 0.45)",
        "glow-red": "0 0 0.8rem rgba(255, 75, 110, 0.5)",
      },
      keyframes: {
        sonarSweep: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        pulseGlow: {
          "0%, 100%": { opacity: "0.35" },
          "50%": { opacity: "1" },
        },
        alertFlash: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.35" },
        },
      },
      animation: {
        sonarSweep: "sonarSweep 5s linear infinite",
        pulseGlow: "pulseGlow 2.2s ease-in-out infinite",
        alertFlash: "alertFlash 0.8s ease-in-out infinite",
      },
      fontFamily: {
        tech: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
