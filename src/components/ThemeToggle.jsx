import { useState, useEffect } from "react";

const themes = ["corporate", "dark", "dracula", "night", "pastel","luxury", "dim", "valentine", "black"];

export default function ThemeToggle() {
  const [theme, setTheme] = useState("corporate");

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initial = saved || (prefersDark ? "dark" : "corporate");
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);

  const toggleTheme = () => {
    const currentIndex = themes.indexOf(theme);
    const next = themes[(currentIndex + 1) % themes.length];
    setTheme(next);
    localStorage.setItem("theme", next);
    document.documentElement.setAttribute("data-theme", next);
  };

  return (
    <button className="btn btn-ghost btn-sm text-md" onClick={toggleTheme}>
      🎨 {theme}
    </button>
  );
}
