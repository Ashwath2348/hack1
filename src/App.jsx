import { useMemo, useState } from "react";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import SonarBackground from "./components/SonarBackground";

const THEME_KEY = "sonar-theme";

function App() {
  const [screen, setScreen] = useState("landing");
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || "dark");

  const appClasses = useMemo(
    () =>
      theme === "dark"
        ? "app-shell bg-command-950 text-slate-100"
        : "app-shell bg-slate-100 text-slate-900",
    [theme]
  );

  const toggleTheme = () => {
    setTheme((current) => {
      const nextTheme = current === "dark" ? "light" : "dark";
      localStorage.setItem(THEME_KEY, nextTheme);
      return nextTheme;
    });
  };

  return (
    <div className={appClasses}>
      <SonarBackground theme={theme} />
      {screen === "landing" ? (
        <LandingPage onStart={() => setScreen("dashboard")} theme={theme} onToggleTheme={toggleTheme} />
      ) : (
        <DashboardPage onBack={() => setScreen("landing")} theme={theme} onToggleTheme={toggleTheme} />
      )}
    </div>
  );
}

export default App;
