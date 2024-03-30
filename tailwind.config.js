/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/templates/**/*.{html,js}',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    colors: {
      'lt-l': 'fafafa', // light --- low zinc-50
      'lt-m': '#f4f4f5', // light --- medium zinc-100
      'lt-h': '#e4e4e7', // light --- high zinc-200
      'dk-l': '#404040', // dark --- low neutral-700
      'dk-m': '#262626', // dark --- medium neutral-800
      'dk-h': '#171717', // dark --- high neutral-900
      'accent-l': '#059669', // --- emerald-600
      'accent-r': '#38bdf8', // --- sky-400
    },
    extend: {
    },
  },
  plugins: [require('flowbite/plugin')],
  darkMode: 'media',
  darkMode: 'class',
}
