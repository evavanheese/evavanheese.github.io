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
                    "primary":      "#CA530C",
                    "secondary":    "#CA530C",
                    "accent":       "#8F250C",
                    "neutral":      "#2A2F1A",
                    "base-100":     "#3D4523",
                    "base-200":     "#535E30",
                    "base-300":     "#606D37",
                    "base-content": "#FFFFFF",
                },
            },
        ],
    },
};
