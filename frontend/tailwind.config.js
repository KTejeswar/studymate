/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#05050A',
        surface: '#0B0B14',
        card: '#121222',
        border: '#1F1F38',
        lavender: '#B794FF',
        cyan: '#22E4FF',
        violet: '#5B21B6',
      },
    },
  },
  plugins: [],
}
