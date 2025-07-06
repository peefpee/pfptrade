import daisyui from "daisyui";

export default {
  content: ["./platform/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [daisyui],
}
