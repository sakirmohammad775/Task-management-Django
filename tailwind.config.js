/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',
  ],
  safelist: [
    'text-red-500',
    'bg-orange-100',
    'focus:ring-rose-500',
    'rounded-lg',
    'w-full',
    'text-center',
    'space-y-4',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
