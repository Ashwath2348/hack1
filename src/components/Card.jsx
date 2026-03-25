function Card({ title, subtitle, children, className = "" }) {
  return (
    <section
      className={`rounded-xl border border-neon-green/20 bg-command-900/75 p-4 backdrop-blur-sm md:p-5 ${className}`}
    >
      {(title || subtitle) && (
        <header className="mb-3">
          {title && <h2 className="text-base font-semibold tracking-wide text-neon-green">{title}</h2>}
          {subtitle && <p className="text-xs text-slate-300/80">{subtitle}</p>}
        </header>
      )}
      {children}
    </section>
  );
}

export default Card;
