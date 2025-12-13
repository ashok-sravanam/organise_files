/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Outfit', 'sans-serif'],
            },
            colors: {
                'brand': {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    900: '#0c4a6e',
                },
                'sigma': {
                    dark: '#0f172a',
                    glass: 'rgba(255, 255, 255, 0.1)',
                    'glass-border': 'rgba(255, 255, 255, 0.2)',
                }
            },
            backgroundImage: {
                'aurora': 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                'aurora-accent': 'conic-gradient(from 90deg at 50% 50%, #0ea5e9 0%, #6366f1 50%, #a855f7 100%)',
            }
        },
    },
    plugins: [],
}
