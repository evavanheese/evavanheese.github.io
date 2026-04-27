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
                    "primary":      "#4A5C28",
                    "secondary":    "#7A8B47",
                    "accent":       "#CA530C",
                    "neutral":      "#353D24",
                    "base-100":     "#606D37",
                    "base-200":     "#D7DFBF",
                    "base-300":     "#B8C58D",
                    "base-content": "#FFFFFF",
                },
            },
        ],
    },
};
