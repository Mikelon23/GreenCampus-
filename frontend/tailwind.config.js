/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Source Sans 3'", "sans-serif"]
      },
      colors: {
        campus: {
          50: "#f2f7f4",
          100: "#d9e7df",
          200: "#b0cfc1",
          300: "#87b6a3",
          400: "#5f9e86",
          500: "#3e856a",
          600: "#2f6a54",
          700: "#214f3e",
          800: "#153428",
          900: "#0a1a14"
        },
        sunlight: {
          100: "#fff4d1",
          200: "#ffe4a3",
          300: "#ffd075",
          400: "#ffba47"
        }
      }
    }
  },
  plugins: []
};
