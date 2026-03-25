function Button({ children, variant = "primary", className = "", ...props }) {
  const variants = {
    primary:
      "bg-neon-green text-command-950 hover:brightness-110 shadow-glow border border-neon-green/40",
    danger: "bg-neon-red text-white hover:brightness-110 shadow-glow-red border border-neon-red/50",
    ghost:
      "bg-transparent text-neon-green border border-neon-green/50 hover:bg-neon-green/10",
  };

  return (
    <button
      className={`rounded-lg px-4 py-2 text-sm font-semibold tracking-wide transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-60 ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
