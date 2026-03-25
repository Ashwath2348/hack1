function SonarBackground({ theme }) {
  const colorRing = theme === "dark" ? "border-neon-green/15" : "border-cyan-500/20";
  const colorSweep = theme === "dark" ? "from-neon-green/40" : "from-cyan-500/30";

  return (
    <div className="pointer-events-none absolute inset-0 flex items-center justify-center overflow-hidden">
      <div className={`sonar-ring ${colorRing}`} />
      <div className={`sonar-ring ${colorRing}`} style={{ inset: "18%" }} />
      <div className={`sonar-ring ${colorRing}`} style={{ inset: "26%" }} />
      <div className="absolute h-[60vmin] w-[60vmin] rounded-full border border-white/5" />
      <div
        className={`absolute h-[60vmin] w-[60vmin] origin-center animate-sonarSweep bg-gradient-to-r ${colorSweep} to-transparent`}
        style={{ clipPath: "polygon(50% 50%, 100% 42%, 100% 58%)" }}
      />
    </div>
  );
}

export default SonarBackground;
