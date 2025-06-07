export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: ["lofi", "forest"],
  },
  plugins: [require("daisyui")], // ✅ 이 줄 추가
}
