/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'leather-brown': '#2c1810',
        'leather-accent': '#d4a574',
        'leather-light': '#f5f5f5',
      },
    },
  },
  plugins: [],
}

