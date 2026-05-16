/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        sage: {
          50: "#f5f8f4",
          100: "#e8efe5",
          200: "#cfdfc9",
          300: "#a9c39e",
          400: "#7ea16f",
          500: "#5d8550",
          600: "#476a3e",
          700: "#3a5532",
          800: "#30452a",
          900: "#283924",
        },
      },
      fontFamily: {
        display: ["ui-serif", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
