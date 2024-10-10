/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',

        transparent: 'transparent',
        milk: '#fff',

        perfReview: {
          DEFAULT: '#8b5cf6',
          500: '#8b5cf6',
          600: '#7c3aed'
        },
        selfReview: {
          DEFAULT: '#14b8a6',
          500: '#14b8a6',
          600: '#0d9488'
        },
        elephant: {
          DEFAULT: '#12344d',
          900: '#12344d',
          800: '#264966',
          700: '#345C7C',
          600: '#447093',
          500: '#415D71',
          400: '#576C7D',
          300: '#C0CEEE',
          200: '#A2C0DE',
          100: '#BEDBF5',
          50: '#dff0ff',
        },
        azure: {
          DEFAULT: '#2c5cc5',
          900: '#283DA5',
          800: '#2c5cc5',
          700: '#2e6ed8',
          600: '#2F80EB',
          500: '#2E8EFA',
          400: '#459FFC',
          300: '#64B0FC',
          200: '#90C6FE',
          100: '#bbdcfe',
          50: '#e5f2fd',
        },
        smoke: {
          DEFAULT: '#ebeff3',
          900: '#27313a',
          800: '#384551',
          700: '#475867',
          500: '#647A8E',
          600: '#576C7D',
          400: '#7B8E9F',
          300: '#92A2B1',
          200: '#97a4af',
          100: '#cfd7df',
          75: '#313D48',
          50: '#ebeff3',
          25: '#f5f7f9',
        },
      },
    },
  },
  plugins: [],
};
