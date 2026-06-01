/** @type {import('tailwindcss').Config} */
export default {
    content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
    theme: {
        extend: {},
    },
    plugins: [require("@tailwindcss/typography"), require("daisyui")],
    daisyui: {
        themes: [
            {
                eva: {
                    "primary":          "#CA530C",
                    "primary-content":  "#FFFFFF",
                    "secondary":        "#CA530C",
                    "secondary-content":"#FFFFFF",
                    "accent":           "#F69960",
                    "accent-content":   "#000000",
                    "neutral":          "#1A2E26",
                    "neutral-content":  "#FFFFFF",
                    "base-100":         "#0F1A0F",
                    "base-200":         "#1A2E1A",
                    "base-300":         "#2A4A2A",
                    "base-content":     "#FFFFFF",
                    "info":             "#8F250C",
                    "info-content":     "#FFFFFF",
                    "success":          "#84964C",
                    "success-content":  "#FFFFFF",
                    "warning":          "#8F250C",
                    "warning-content":  "#FFFFFF",
                    "error":            "#8F250C",
                    "error-content":    "#FFFFFF",
                },
            },
        ],
    },
};
