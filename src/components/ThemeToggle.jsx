import Button from "./Button";

function ThemeToggle({ theme, onToggle }) {
  return (
    <Button variant="ghost" onClick={onToggle} className="min-w-28">
      {theme === "dark" ? "Light Mode" : "Dark Mode"}
    </Button>
  );
}

export default ThemeToggle;
