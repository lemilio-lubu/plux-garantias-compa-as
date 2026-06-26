import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/modules/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // ── Service-bay console palette ───────────────────────────────────
      // Legacy token names are re-pointed to the new values so every existing
      // screen re-skins automatically; new names below are for new work.
      colors: {
        // New, explicit names
        ink:      "#15171C", // diesel graphite — primary text / dark rail
        graphite: "#22262F", // panel dark
        steel:    "#69707E", // secondary text / blueprint slate
        mist:     "#E2E5E9", // hairline borders
        paper:    "#F4F5F3", // off-white workshop surface
        amber: {
          DEFAULT: "#F5B301", // hazard amber — the single brand accent
          dark:    "#C98F00",
          soft:    "#FFF4D1", // tint for badges / lit surfaces
        },

        // Legacy aliases (re-pointed) — keep existing markup working
        black:        "#15171C",
        "dark-gray":  "#22262F",
        "mid-gray":   "#69707E",
        "light-gray": "#E2E5E9",
        "off-white":  "#F4F5F3",
        white:        "#FFFFFF",

        text: {
          primary:   "#15171C",
          secondary: "#22262F",
          tertiary:  "#69707E",
        },
        border: {
          DEFAULT: "#E2E5E9",
        },
        bg: {
          base:   "#FFFFFF",
          subtle: "#F4F5F3",
        },

        // Cohesive, muted status hues (the SRG state machine)
        status: {
          proceso:     "#5B6B9E",
          pendiente:   "#B57A1F",
          preaprobado: "#3F7D5B",
          aprobado:    "#2E6B4A",
          retornado:   "#A23B4A",
          negado:      "#6B7280",
        },
      },

      // ── Typography ────────────────────────────────────────────────────
      fontFamily: {
        sans:    ['"IBM Plex Sans"', "-apple-system", "BlinkMacSystemFont", '"Segoe UI"', "sans-serif"],
        display: ['"Space Grotesk"', '"IBM Plex Sans"', "sans-serif"],
        mono:    ['"IBM Plex Mono"', "ui-monospace", "SFMono-Regular", "monospace"],
      },
      fontSize: {
        h1: ["46px", { lineHeight: "1.05", fontWeight: "600", letterSpacing: "-0.02em" }],
        h2: ["34px", { lineHeight: "1.1",  fontWeight: "600", letterSpacing: "-0.015em" }],
        h3: ["26px", { lineHeight: "1.2",  fontWeight: "600", letterSpacing: "-0.01em" }],
        h4: ["20px", { lineHeight: "1.35", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "1.6", fontWeight: "400" }],
        body:      ["15px", { lineHeight: "1.6", fontWeight: "400" }],
        small:     ["13px", { lineHeight: "1.5", fontWeight: "400" }],
        caption:   ["11px", { lineHeight: "1.45", fontWeight: "500" }],
      },

      // ── Engineered radii (tighter, more precise) ──────────────────────
      borderRadius: {
        sm: "4px",
        md: "6px",
        lg: "10px",
        xl: "14px",
      },

      // ── Crisp panel shadows ───────────────────────────────────────────
      boxShadow: {
        card:  "0 1px 0 rgba(21,23,28,0.02), 0 1px 2px rgba(21,23,28,0.06)",
        panel: "0 1px 3px rgba(21,23,28,0.08), 0 8px 24px -12px rgba(21,23,28,0.18)",
        rail:  "inset -1px 0 0 rgba(255,255,255,0.04)",
        sm:    "0 1px 2px rgba(21,23,28,0.05)",
        amber: "0 0 0 3px rgba(245,179,1,0.28)",
      },

      // ── Spacing (multiples of 8) ──────────────────────────────────────
      spacing: {
        "0.5": "4px",
        "1":   "8px",
        "2":   "16px",
        "3":   "24px",
        "4":   "32px",
        "6":   "48px",
        "8":   "64px",
        "12":  "96px",
      },

      maxWidth: {
        layout:  "1280px",
        content: "1080px",
      },

      backgroundImage: {
        // Hazard stripe — the signature accent, used very sparingly
        hazard:
          "repeating-linear-gradient(-45deg, #F5B301 0 10px, #15171C 10px 20px)",
      },
    },
  },
  plugins: [],
};

export default config;
