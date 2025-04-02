/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: "class", // <--- Ensure this is set to 'class'
    content: [
      './pages/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './app/**/*.{js,ts,jsx,tsx,mdx}',
      './src/**/*.{js,ts,jsx,tsx,mdx}', // Adjust paths as needed
    ],
    theme: {
      extend: {
         // Your theme extensions from shadcn/ui setup
      },
    },
    plugins: [require("tailwindcss-animate")],
  }