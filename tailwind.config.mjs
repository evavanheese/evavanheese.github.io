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
                evaLight: {
                    "primary":      "#CA530C",
                    "secondary":    "#606D37",
                    "accent":       "#8F250C",
                    "neutral":      "#353D24",
                    "base-100":     "#D7DFBF",
                    "base-200":     "#B8C58D",
                    "base-300":     "#A1B369",
                    "base-content": "#000000",
                },
            },
            {
                evaDark: {
                    "primary":      "#E8763A",
                    "secondary":    "#7A8B47",
                    "accent":       "#C4442A",
                    "neutral":      "#353D24",
                    "base-100":     "#1C1F14",
                    "base-200":     "#2A2F1C",
                    "base-300":     "#353D24",
                    "base-content": "#E8EDD6",
                },
            },
        ],
    },
};
