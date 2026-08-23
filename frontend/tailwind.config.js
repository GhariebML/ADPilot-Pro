/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Plus Jakarta Sans', 'Poppins', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        primary: {
          DEFAULT: '#0284c7',
          50: '#EFF6FF',
          100: '#DBEEFF',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        accent: {
          DEFAULT: '#00f0ff',
          hover: '#00c8d6',
        },
        cyber: {
          cyan: '#00f0ff',
          blue: '#3b82f6',
          indigo: '#6366f1',
          purple: '#8b5cf6',
          pink: '#ec4899',
          emerald: '#10b981',
          amber: '#f59e0b',
          rose: '#f43f5e',
        },
        obsidian: {
          950: '#030712',
          900: '#07090e',
          850: '#0c111d',
          800: '#111827',
          700: '#1f2937',
        },
        bgLight: '#F4F5F6',
        sidebar: '#FFFFFF',
        surface: '#FFFFFF',
        card: '#FFFFFF',
        muted: '#6B7280',
      },
      boxShadow: {
        soft: '0 8px 24px rgba(15,23,42,0.06)',
        glass: '0 4px 30px rgba(0, 0, 0, 0.1)',
        glow: '0 0 20px rgba(31, 111, 235, 0.3)',
        'neon-cyan': '0 0 25px rgba(0, 240, 255, 0.35)',
        'neon-indigo': '0 0 25px rgba(99, 102, 241, 0.35)',
        'neon-purple': '0 0 25px rgba(139, 92, 246, 0.35)',
        'neon-emerald': '0 0 25px rgba(16, 185, 129, 0.35)',
        'neon-amber': '0 0 25px rgba(245, 158, 11, 0.35)',
        'obsidian-glow': '0 12px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 240, 255, 0.08)',
      },
      borderRadius: {
        xl: '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      animation: {
        blob: "blob 7s infinite",
        float: "float 6s ease-in-out infinite",
        'float-slow': "float-slow 6s ease-in-out infinite",
        'pulse-slow': "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        'laser-scan': "laser-scan 4s cubic-bezier(0.4, 0, 0.2, 1) infinite",
        'border-pulse': "border-pulse 2.5s ease-in-out infinite",
      },
      keyframes: {
        blob: {
          "0%": { transform: "translate(0px, 0px) scale(1)" },
          "33%": { transform: "translate(30px, -50px) scale(1.1)" },
          "66%": { transform: "translate(-20px, 20px) scale(0.9)" },
          "100%": { transform: "translate(0px, 0px) scale(1)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        'float-slow': {
          "0%, 100%": { transform: "translateY(0px) rotate(0deg)" },
          "50%": { transform: "translateY(-8px) rotate(0.5deg)" },
        },
        'laser-scan': {
          "0%": { transform: "translateY(-100%)", opacity: "0" },
          "50%": { opacity: "0.8" },
          "100%": { transform: "translateY(1000%)", opacity: "0" },
        },
        'border-pulse': {
          "0%, 100%": { borderColor: "rgba(0, 240, 255, 0.3)" },
          "50%": { borderColor: "rgba(99, 102, 241, 0.6)" },
        }
      },
    },
  },
  plugins: [],
}
