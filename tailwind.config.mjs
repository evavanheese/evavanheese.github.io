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
                    "neutral":          "#2A2F1A",
                    "neutral-content":  "#FFFFFF",
                    "base-100":         "#3D4523",
                    "base-200":         "#535E30",
                    "base-300":         "#606D37",
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
