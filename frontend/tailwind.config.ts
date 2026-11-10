import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class', '[data-theme="aurora"]'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        base: 'var(--bg-base)',
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
        },
        accent: {
          lavender: 'var(--accent-lavender)',
          cyan: 'var(--accent-cyan)',
          violet: 'var(--accent-violet)',
          brand: 'var(--accent-brand)',
        },
        status: {
          green: 'var(--status-green)',
          amber: 'var(--status-amber)',
          red: 'var(--status-red)',
        },
        glass: {
          bg: 'var(--glass-bg)',
          fallback: 'var(--glass-fallback)',
          border: 'var(--glass-border)',
          hover: 'var(--glass-hover)',
          highlight: 'var(--glass-highlight)',
        },
      },
      boxShadow: {
        glass: 'var(--glass-shadow)',
        'glass-hover': 'var(--glass-shadow-hover)',
        glow: 'var(--glow-shadow)',
      },
      borderRadius: {
        panel: 'var(--radius-panel)',
      },
      fontFamily: {
        sans: ['var(--font-jakarta)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-space)', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
