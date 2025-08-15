/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Tidal brand colors (exact PRD colors)
        'tidal-purple': '#7B61FF',
        'tidal-aqua': '#00C6A2',
        'dark-navy-text': '#1A1A1A',
        'medium-gray-text': '#555555',
        'light-gray-bg': '#F7F7F9',
        'card-border-gray': '#E5E5E7',
        'success-green': '#16A34A',
        'gradient-purple-start': '#7B61FF',
        'gradient-purple-end': '#9F7FFF',
        
        // Tidal brand color palette (for legacy compatibility)
        tidal: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          // Primary brand colors
          purple: '#7B61FF',
          aqua: '#00C6A2',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      screens: {
        'mobile': {'max': '767px'},
        'tablet': {'min': '768px', 'max': '1199px'},
        'desktop': {'min': '1200px'},
        // Standard Tailwind breakpoints (for compatibility)
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
}