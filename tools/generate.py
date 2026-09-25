#!/usr/bin/env python3
"""Build the animated SVG artwork used by the profile README.

    pip install fonttools brotli
    python tools/generate.py

Writes assets/dark/*.svg and assets/light/*.svg. Each SVG embeds only the
glyphs it uses from Geist and Geist Mono (SIL OFL 1.1, see tools/fonts/OFL.txt),
so it renders identically everywhere without loading anything external.
Brand icons come from Simple Icons (CC0 1.0), stored in tools/icons.json.
Edit the PROJECTS list below and re-run to update the cards.
"""
import base64
import io
import json
import os
from collections import defaultdict
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "tools", "fonts")
ICONS = json.load(open(os.path.join(ROOT, "tools", "icons.json"), encoding="utf-8"))

FONT_FILES = {
    ("sans", 400): "Geist-Regular",
    ("sans", 500): "Geist-Medium",
    ("sans", 600): "Geist-SemiBold",
    ("sans", 700): "Geist-Bold",
    ("mono", 400): "GeistMono-Regular",
    ("mono", 500): "GeistMono-Medium",
}
FAMILY = {
    "sans": "G, 'Segoe UI', system-ui, -apple-system, sans-serif",
    "mono": "GM, ui-monospace, SFMono-Regular, Consolas, monospace",
}
CSS_FAMILY = {"sans": "G", "mono": "GM"}

THEMES = {
    "dark": dict(
        name="dark", bg="#070A1C", bg2="#0C1333", card="#0A0F24", card2="#10173A",
        border="#1D2650", border2="#2B3668", text="#EEF1FF", muted="#9AA4CB", dim="#5F6A98",
        accent="#5B8CFF", accent_hi="#A9C1FF", violet="#A78BFA", cyan="#22D3EE",
        green="#34D399", grid="#FFFFFF", grid_op=0.07, orb1="#2F55FF", orb2="#7C3AED",
        orb_op=0.55, on_accent="#FFFFFF",
    ),
    "light": dict(
        name="light", bg="#F7F9FF", bg2="#E9EEFF", card="#FFFFFF", card2="#F4F6FD",
        border="#DDE3F4", border2="#C7D1EE", text="#0B1024", muted="#4B5577", dim="#8189AC",
        accent="#2856C7", accent_hi="#5B8CFF", violet="#7C3AED", cyan="#0891B2",
        green="#059669", grid="#0B1024", grid_op=0.07, orb1="#6D95FF", orb2="#B79CFF",
        orb_op=0.35, on_accent="#FFFFFF",
    ),
}

REPO = "https://github.com/pranjal-agarwal01"
PROJECTS = [
    dict(slug="stationwatch", title="StationWatch", cat="COMPUTER VISION", live=True,
         accent=("#22D3EE", "#0891B2"),
         desc="Flags stopped escalators straight from existing CCTV footage. No new "
              "hardware, no training data: YOLO11 plus optical flow, running in your browser.",
         metric="0 false alarms across 8 benchmark scenarios",
         chips=["Python", "OpenCV", "YOLO11", "ONNX Web"]),
    dict(slug="supplysense", title="SupplySense AI", cat="FULL-STACK · FORECASTING", live=True,
         accent=("#34D399", "#059669"),
         desc="Forecasts material demand with five from-scratch time-series models, then "
              "turns each forecast into reorder points and purchase orders.",
         metric="30 automated tests · CI on every push",
         chips=["React 19", "Node.js", "Express 5", "MongoDB"]),
    dict(slug="debator", title="Debator", cat="MULTI-AGENT AI", live=True,
         accent=("#FB923C", "#EA580C"),
         desc="Two AI agents debate any motion while a judge scores every turn. Code, not "
              "the model, totals the rubric, so the verdict can't be faked.",
         metric="Output tokens per debate: 27k → 3.8k",
         chips=["Python", "FastAPI", "PostgreSQL", "Azure OpenAI"]),
    dict(slug="everlink", title="Everlink", cat="FULL-STACK", live=False,
         accent=("#5B8CFF", "#2856C7"),
         desc="Short links you can repoint at any time, so the link on a résumé, QR code "
              "or bio never breaks when the destination moves.",
         metric="Atomic click counts · JWT + bcrypt auth",
         chips=["React", "Node.js", "Express", "MongoDB"]),
    dict(slug="booking", title="Event Booking API", cat="BACKEND · CONCURRENCY", live=True,
         accent=("#A78BFA", "#7C3AED"),
         desc="A Spring Boot booking API built for the hardest case: two people grabbing "
              "the last seat in the same millisecond. Exactly one wins.",
         metric="50 threads · 1 seat · 1 winner, tested on Postgres",
         chips=["Java 21", "Spring Boot", "PostgreSQL", "Docker"]),
    dict(slug="newsletter", title="AI Newsletter", cat="AI AUTOMATION", live=False,
         accent=("#F472B6", "#DB2777"),
         desc="Collects AI news from RSS, Hacker News and arXiv, ranks it against a reader "
              "profile and emails an LLM-written digest.",
         metric="Runs twice a day on GitHub Actions, no server",
         chips=["Python", "GitHub Actions", "SQLite", "OpenRouter"]),
    dict(slug="sevcs", title="SEVCS", cat="COMPUTER VISION", live=False,
         accent=("#F87171", "#DC2626"),
         desc="Detects and tracks vehicles in traffic video and flags the ones blocking "
              "an emergency-vehicle lane.",
         metric="YOLOv8 on KITTI · 20-trial Optuna search",
         chips=["Python", "YOLOv8", "PyTorch", "Optuna"]),
    dict(slug="more", title="pranjalagarwal.me", cat="AND MORE", live=False,
         accent=(None, None),
         desc="Case studies, blog posts, client automation work and both résumés, "
              "all in one place.",
         metric="Visit the portfolio",
         chips=["Portfolio", "Blog", "Résumé"]),
]

LIVE_DEMOS = [
    ("stationwatch", "StationWatch"),
    ("supplysense", "SupplySense AI"),
    ("debator", "Debator"),
    ("booking", "Booking API"),
]

BUTTONS = [
    ("portfolio", "Portfolio", "globe", True),
    ("linkedin", "LinkedIn", "linkedin", False),
    ("email", "Email", "mail", False),
    ("resume-swe", "Résumé · SWE", "doc", False),
    ("resume-ml", "Résumé · ML/CV", "doc", False),
]

TOOLBOX = [
    ("LANGUAGES", [("Python", "python"), ("Java", "openjdk"), ("JavaScript", "javascript"),
                   ("TypeScript", "typescript"), ("SQL", "db")]),
    ("FRONTEND", [("React", "react"), ("Next.js", "nextdotjs"), ("Tailwind CSS", "tailwindcss"),
                  ("Vite", "vite")]),
    ("BACKEND & DATA", [("Node.js", "nodedotjs"), ("Express", "express"), ("FastAPI", "fastapi"),
                        ("Spring Boot", "springboot"), ("MongoDB", "mongodb"),
                        ("PostgreSQL", "postgresql")]),
    ("AI & VISION", [("PyTorch", "pytorch"), ("OpenCV", "opencv"), ("YOLO", "ultralytics"),
                     ("LangChain", "langchain"), ("Hugging Face", "huggingface"),
                     ("Optuna", "optuna")]),
    ("CLOUD & TOOLS", [("Docker", "docker"), ("GitHub Actions", "githubactions"), ("Git", "git"),
                       ("Vercel", "vercel"), ("Render", "render"), ("n8n", "n8n")]),
]

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

# ---------------------------------------------------------------- fonts

_fonts = {}
_faces = {}


def font(key):
    if key not in _fonts:
        _fonts[key] = TTFont(os.path.join(FONT_DIR, FONT_FILES[key] + ".woff2"))
    return _fonts[key]


def measure(s, fam="sans", w=400, size=14, ls=0.0):
    f = font((fam, w))
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    width = sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else upm // 2 for c in s)
    return width * size / upm + ls * len(s)


def wrap(s, fam, w, size, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if measure(trial, fam, w, size) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def font_face(key, chars):
    chars = "".join(sorted(set(chars) | {" "}))
    if (key, chars) not in _faces:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        opts.name_IDs = []
        opts.notdef_outline = True
        opts.hinting = False
        opts.drop_tables += ["meta", "DSIG", "STAT", "gasp"]
        f = TTFont(os.path.join(FONT_DIR, FONT_FILES[key] + ".woff2"))
        sub = subset.Subsetter(opts)
        sub.populate(text=chars)
        sub.subset(f)
        buf = io.BytesIO()
        f.flavor = "woff2"
        f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        _faces[(key, chars)] = (
            f"@font-face{{font-family:{CSS_FAMILY[key[0]]};font-weight:{key[1]};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        )
    return _faces[(key, chars)]


# ---------------------------------------------------------------- svg document


class Svg:
    def __init__(self, w, h, theme, title):
        self.w, self.h, self.t, self.title = w, h, theme, title
        self.used = defaultdict(set)
        self.css, self.defs, self.body = [], [], []
        self._n = 0

    def uid(self, prefix="u"):
        self._n += 1
        return f"{prefix}{self._n}"

    def text(self, x, y, s, fam="sans", w=400, size=14, fill=None, anchor=None, ls=None,
             extra=""):
        self.used[(fam, w)].update(s)
        a = f' text-anchor="{anchor}"' if anchor else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[fam]}" font-weight="{w}" '
                f'font-size="{size}" fill="{fill or self.t["text"]}"{a}{l}{extra}>{escape(s)}</text>')

    def spans(self, x, y, parts, size, anchor=None, ls=None, extra=""):
        """parts: list of (string, family, weight, fill)."""
        inner = ""
        for s, fam, w, fill in parts:
            self.used[(fam, w)].update(s)
            inner += (f'<tspan font-family="{FAMILY[fam]}" font-weight="{w}" '
                      f'fill="{fill}">{escape(s)}</tspan>')
        a = f' text-anchor="{anchor}"' if anchor else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" xml:space="preserve"{a}{l}'
                f'{extra}>{inner}</text>')

    def render(self):
        faces = "".join(font_face(k, "".join(v)) for k, v in sorted(self.used.items()) if v)
        style = faces + "".join(self.css) + REDUCED_MOTION
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(self.title)}</title>'
            f"<style>{style}</style><defs>{''.join(self.defs)}</defs>{''.join(self.body)}</svg>"
        )


# ---------------------------------------------------------------- helpers


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in hex_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def darken(h, k):
    r, g, b = hex_rgb(h)
    return "#%02X%02X%02X" % tuple(int(c * (1 - k) * 255) for c in (r, g, b))


def pulse_dot(cx, cy, color, r=3.5, dur=2.2):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5">'
        f'<animate attributeName="r" values="{r};{r * 3.2}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.8;0" dur="{dur}s" repeatCount="indefinite"/>'
        f"</circle>"
    )


def sweep_gradient(doc, color, width, span, dur, begin=0.0, pause=0.55):
    gid = doc.uid("sw")
    doc.defs.append(
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{span}" y2="0">'
        f'<stop offset="0" stop-color="{color}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{color}" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" '
        f'values="{-span} 0;{-span} 0;{width + span} 0" keyTimes="0;{pause};1" dur="{dur}s" '
        f'begin="{begin}s" repeatCount="indefinite"/></linearGradient>'
    )
    return gid


def icon(name, x, y, size, color):
    if name == "db":  # generic database glyph for SQL
        s = size / 24
        return (f'<g transform="translate({x},{y}) scale({s:.4f})" fill="none" stroke="{color}" '
                f'stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="5" rx="8" ry="3"/>'
                f'<path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></g>')
    s = size / 24
    return f'<path transform="translate({x},{y}) scale({s:.4f})" fill="{color}" d="{ICONS[name]["path"]}"/>'


def ui_icon(kind, x, y, color, size=16):
    s = size / 24
    common = (f'transform="translate({x},{y}) scale({s:.4f})" fill="none" stroke="{color}" '
              f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"')
    if kind == "globe":
        return (f'<g {common}><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/>'
                f'<path d="M12 2.5c2.6 2.8 3.9 6 3.9 9.5s-1.3 6.7-3.9 9.5c-2.6-2.8-3.9-6-3.9-9.5S9.4 5.3 12 2.5z"/></g>')
    if kind == "mail":
        return (f'<g {common}><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/>'
                f'<path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></g>')
    if kind == "doc":
        return (f'<g {common}><path d="M14 2.5H6.5A2 2 0 0 0 4.5 4.5v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/>'
                f'<path d="M14 2.5V8h5.5"/><path d="M8.5 13h7M8.5 17h5"/></g>')
    if kind == "linkedin":
        return (f'<path transform="translate({x},{y}) scale({s:.4f})" fill="{color}" d="M20.45 20.45h-3.55'
                "v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9"
                " 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06"
                " 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0"
                ' 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/>')
    raise ValueError(kind)


# ---------------------------------------------------------------- header


def typing_track(phrases, char_w, slot, type_dt=0.045, del_dt=0.018, del_step=2):
    """Discrete SMIL timeline that types and backspaces each phrase in turn."""
    total = slot * len(phrases)
    events = []
    for i, p in enumerate(phrases):
        t0 = i * slot + 0.35
        n = len(p)
        for k in range(n + 1):
            events.append((t0 + k * type_dt, i, k))
        dels = -(-n // del_step)
        t_del = (i + 1) * slot - 0.3 - dels * del_dt
        k, j = n, 0
        while k > 0:
            k, j = max(0, k - del_step), j + 1
            events.append((t_del + j * del_dt, i, k))
    events.sort()
    times, widths = [0.0], [[0] * len(phrases)]
    cur = [0] * len(phrases)
    for t, i, k in events:
        cur[i] = k
        t = round(t, 3)
        if t == times[-1]:
            widths[-1] = cur[:]
        else:
            times.append(t)
            widths.append(cur[:])
    key_times = ";".join(f"{t / total:.5f}" for t in times)
    per_phrase = [";".join(f"{w[i] * char_w:.1f}" for w in widths) for i in range(len(phrases))]
    caret = ";".join(f"{sum(w) * char_w:.1f}" for w in widths)
    return total, key_times, per_phrase, caret


def header(t):
    W, H = 1200, 360
    d = Svg(W, H, t, "Pranjal Agarwal: products that ship, not demos that die in notebooks")
    d.css.append(
        "@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(-70px,36px)}}"
        "@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(50px,-30px)}}"
        "@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}"
        "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
        ".o1{animation:d1 16s ease-in-out infinite}.o2{animation:d2 19s ease-in-out infinite}"
        ".l0{animation:fl 6s ease-in-out infinite}.l1{animation:fl 6s ease-in-out -2s infinite}"
        ".l2{animation:fl 6s ease-in-out -4s infinite}.bl{animation:bl 1.05s step-end infinite}"
    )
    d.defs.append(
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="24"/></clipPath>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg"]}"/>'
        f'<stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
        f'<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.1" fill="{t["grid"]}" fill-opacity="{t["grid_op"]}"/></pattern>'
        f'<radialGradient id="fade" cx="0.72" cy="0.45" r="0.75"><stop offset="0" stop-color="#fff"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>'
        f'<radialGradient id="stackglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{t["accent"]}" '
        f'stop-opacity="0.35"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="620" y2="0">'
        f'<stop offset="0" stop-color="{t["text"]}"/><stop offset="0.4" stop-color="{t["text"]}"/>'
        f'<stop offset="0.5" stop-color="{t["accent_hi"]}"/><stop offset="0.6" stop-color="{t["text"]}"/>'
        f'<stop offset="1" stop-color="{t["text"]}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" values="-700 0;-700 0;760 0" '
        f'keyTimes="0;0.55;1" dur="7s" repeatCount="indefinite"/></linearGradient>'
    )
    b = d.body
    b.append('<g clip-path="url(#card)">')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    b.append(f'<g filter="url(#blur)" opacity="{t["orb_op"]}">'
             f'<circle class="o1" cx="930" cy="80" r="190" fill="{t["orb1"]}"/>'
             f'<circle class="o2" cx="1110" cy="320" r="160" fill="{t["orb2"]}"/>'
             f'<circle class="o2" cx="210" cy="-60" r="150" fill="{t["accent"]}" opacity="0.5"/></g>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#gridmask)"/>')
    b.append("</g>")
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" '
             f'stroke="{t["border"]}"/>')

    # status chip
    label = "OPEN TO SDE · FULL-STACK · ML ROLES"
    cw = measure(label, "mono", 500, 12, 1.4) + 44
    b.append(f'<rect x="64" y="42" width="{cw:.1f}" height="30" rx="15" fill="{t["green"]}" '
             f'fill-opacity="0.1" stroke="{t["green"]}" stroke-opacity="0.35"/>')
    b.append(pulse_dot(82, 57, t["green"]))
    b.append(d.text(96, 61.5, label, "mono", 500, 12, t["green"], ls=1.4))

    # name, tagline
    b.append(d.text(62, 152, "Pranjal Agarwal", "sans", 700, 78, "url(#name)", ls=-2.4))
    b.append(d.spans(64, 200, [("Products that ship. ", "sans", 500, t["text"]),
                                ("Not demos that die in notebooks.", "sans", 400, t["muted"])], 27))

    # typing line
    phrases = [
        "shipping full-stack products that stay deployed",
        "turning CCTV footage into escalator fault alerts",
        "making AI agents debate, and judging them fairly",
        "forecasting demand before the stock runs out",
    ]
    size = 19
    char_w = measure("m", "mono", 400, size)
    x0, y0 = 90, 258
    total, kt, per, caret = typing_track(phrases, char_w, slot=4.6)
    b.append(d.text(64, y0, "$", "mono", 500, size, t["green"]))
    for i, p in enumerate(phrases):
        cid = d.uid("tc")
        base_w = len(p) * char_w if i == 0 else 0
        d.defs.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0 - 22}" width="{base_w:.1f}" height="32">'
                      f'<animate attributeName="width" values="{per[i]}" keyTimes="{kt}" dur="{total}s" '
                      f'calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>')
        b.append(f'<g clip-path="url({"#" + cid})">'
                 + d.text(x0, y0, p, "mono", 400, size, t["accent_hi"] if t["name"] == "dark" else t["accent"])
                 + "</g>")
    b.append(f'<g class="bl"><rect x="{x0 + len(phrases[0]) * char_w:.1f}" y="{y0 - 16}" width="10" height="21" '
             f'rx="1.5" fill="{t["green"]}">'
             f'<animate attributeName="x" values="{";".join(f"{x0 + float(v):.1f}" for v in caret.split(";"))}" '
             f'keyTimes="{kt}" dur="{total}s" calcMode="discrete" repeatCount="indefinite"/></rect></g>')

    b.append(d.text(64, 318, "B.TECH CSE · LOVELY PROFESSIONAL UNIVERSITY · CLASS OF 2027 · INDIA",
                    "mono", 400, 12, t["dim"], ls=1.6))

    # isometric stack: ui / api / ml
    cx, a, bh, th = 985, 122, 58, 14
    layers = [("ui · react", t["accent"]), ("api · data", t["violet"]), ("ml · vision", t["green"])]
    ys = [112, 186, 260]
    b.append(f'<ellipse cx="{cx}" cy="186" rx="230" ry="170" fill="url(#stackglow)"/>')
    for sx in (cx - a, cx + a):
        b.append(f'<line x1="{sx}" y1="{ys[0]}" x2="{sx}" y2="{ys[2] + th}" stroke="{t["border2"]}" '
                 f'stroke-width="1.5" stroke-dasharray="3 7"><animate attributeName="stroke-dashoffset" '
                 f'values="20;0" dur="1.2s" repeatCount="indefinite"/></line>')
        for k in range(2):
            b.append(f'<circle r="2.6" fill="{t["accent_hi"]}"><animateMotion path="M{sx},{ys[2] + th} '
                     f'L{sx},{ys[0]}" dur="2.8s" begin="{k * 1.4 + (0.7 if sx > cx else 0)}s" '
                     f'repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" '
                     f'dur="2.8s" begin="{k * 1.4 + (0.7 if sx > cx else 0)}s" repeatCount="indefinite"/></circle>')
    for i in (2, 1, 0):
        lab, col = layers[i]
        y = ys[i]
        top = f"M{cx},{y - bh} L{cx + a},{y} L{cx},{y + bh} L{cx - a},{y} Z"
        left = f"M{cx - a},{y} L{cx},{y + bh} L{cx},{y + bh + th} L{cx - a},{y + th} Z"
        right = f"M{cx},{y + bh} L{cx + a},{y} L{cx + a},{y + th} L{cx},{y + bh + th} Z"
        inner = f"M{cx},{y - bh + 16} L{cx + a - 32},{y} L{cx},{y + bh - 16} L{cx - a + 32},{y} Z"
        b.append(f'<g class="l{i}">'
                 f'<path d="{left}" fill="{col}" fill-opacity="0.22"/>'
                 f'<path d="{right}" fill="{col}" fill-opacity="0.38"/>'
                 f'<path d="{top}" fill="{t["card"]}"/>'
                 f'<path d="{top}" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.85" '
                 f'stroke-width="1.5" stroke-linejoin="round"/>'
                 f'<path d="{inner}" fill="none" stroke="{col}" stroke-opacity="0.3" stroke-dasharray="2 5"/>'
                 + d.text(cx, y + 4.5, lab, "mono", 500, 13, col, anchor="middle", ls=0.5)
                 + "</g>")
    return d.render()


# ---------------------------------------------------------------- terminal


# The terminal's final state is its static state: every animation starts at 0s, hides content
# until its turn and then freezes on "visible". A viewer that skips SMIL still sees all the text.
TERM_DUR = 6.0


def type_clip(d, x, y, n, char_w, begin, dt=0.06, h=26):
    cid = d.uid("c")
    times = [0.0] + [begin + i * dt for i in range(n + 1)]
    vals = ";".join(["0"] + [f"{i * char_w:.1f}" for i in range(n + 1)])
    kt = ";".join(f"{tt / TERM_DUR:.4f}" for tt in times)
    d.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y - h + 6}" width="{n * char_w:.1f}" height="{h}">'
                  f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{TERM_DUR}s" '
                  f'calcMode="discrete" fill="freeze"/></rect></clipPath>')
    return cid, begin + n * dt + dt


def appear(begin):
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{begin / TERM_DUR:.4f}" '
            f'dur="{TERM_DUR}s" calcMode="discrete" fill="freeze"/>')


def terminal(t):
    W, H = 1200, 300
    d = Svg(W, H, t, "Terminal: whoami. Pranjal Agarwal, final-year B.Tech CSE at Lovely Professional "
                     "University. Focus: full-stack, computer vision, AI agents, automation. Open to SDE, "
                     "full-stack and ML roles, and freelance n8n automation.")
    d.css.append("@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.bl{animation:bl 1.05s step-end infinite}")
    b = d.body
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{t["card"]}" '
             f'stroke="{t["border"]}"/>')
    b.append(f'<path d="M0.5 18.5a18 18 0 0 1 18-18h{W - 37}a18 18 0 0 1 18 18V44H0.5z" fill="{t["card2"]}"/>')
    b.append(f'<line x1="0.5" y1="44" x2="{W - 0.5}" y2="44" stroke="{t["border"]}"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{26 + i * 20}" cy="22" r="6" fill="{c}"/>')
    b.append(d.text(W / 2, 27, "pranjal@lpu: ~/about", "mono", 400, 12.5, t["dim"], anchor="middle"))

    size = 17
    cw = measure("m", "mono", 400, size)
    x, y, lh = 32, 84, 31
    prompt_w = measure("~ $ ", "mono", 500, size)
    folder_cols = [t["accent_hi"] if t["name"] == "dark" else t["accent"], t["cyan"], t["violet"], t["green"]]
    script = [
        ("whoami", [("Pranjal Agarwal", t["text"], 500),
                    (" · final-year B.Tech CSE @ Lovely Professional University", t["muted"], 400)]),
        ("ls focus/", [("full-stack/", folder_cols[0], 400), ("    computer-vision/", folder_cols[1], 400),
                       ("    ai-agents/", folder_cols[2], 400), ("    automation/", folder_cols[3], 400)]),
        ("cat status.txt", [("Open to SDE, full-stack & ML roles", t["green"], 500),
                            (" · freelance n8n automation for clients", t["muted"], 400)]),
    ]
    tt = 0.5
    for cmd, out in script:
        b.append(f'<g>{appear(tt)}'
                 + d.text(x, y, "~ $", "mono", 500, size, t["green"]) + "</g>")
        cid, end = type_clip(d, x + prompt_w, y, len(cmd), cw, tt + 0.25)
        b.append(f'<g clip-path="url(#{cid})">' + d.text(x + prompt_w, y, cmd, "mono", 400, size, t["text"])
                 + "</g>")
        y += lh
        parts = [(s, "mono", w, col) for s, col, w in out]
        b.append(f'<g>{appear(end + 0.25)}' + d.spans(x, y, parts, size) + "</g>")
        y += lh + 6
        tt = end + 0.75
    b.append(f'<g>{appear(tt)}' + d.text(x, y, "~ $", "mono", 500, size, t["green"])
             + f'<rect class="bl" x="{x + prompt_w + 2:.1f}" y="{y - 15}" width="10" height="19" rx="1.5" '
               f'fill="{t["green"]}"/></g>')
    return d.render()


# ---------------------------------------------------------------- section titles


def section(t, idx, title, hint):
    W, H = 1200, 70
    d = Svg(W, H, t, f"{idx} {title}. {hint}")
    b = d.body
    b.append(d.text(2, 44, idx, "mono", 500, 15, t["accent_hi"] if t["name"] == "dark" else t["accent"],
                    ls=1))
    b.append(d.text(40, 45, title, "sans", 600, 30, t["text"], ls=-0.6))
    tw = 40 + measure(title, "sans", 600, 30, -0.6) + 22
    hw = measure(hint, "mono", 400, 13, 0.6)
    b.append(d.text(W - 2, 44, hint, "mono", 400, 13, t["dim"], anchor="end", ls=0.6))
    x2 = W - hw - 24
    gid = sweep_gradient(d, t["accent"], x2, 220, 6.5)
    b.append(f'<line x1="{tw:.1f}" y1="35" x2="{x2:.1f}" y2="35" stroke="{t["border2"]}" stroke-width="1.2"/>')
    b.append(f'<rect x="{tw:.1f}" y="34" width="{x2 - tw:.1f}" height="2.2" fill="url(#{gid})"/>')
    return d.render()


# ---------------------------------------------------------------- project cards


def card(t, p, idx):
    W, H = 420, 240
    dark = t["name"] == "dark"
    acc = p["accent"][0 if dark else 1] or (t["accent_hi"] if dark else t["accent"])
    d = Svg(W, H, t, f'{p["title"]}: {p["desc"]} {p["metric"]}. Built with {", ".join(p["chips"])}.')
    d.css.append("@keyframes br{0%,100%{opacity:.65}50%{opacity:1}}.br{animation:br 7s ease-in-out infinite}"
                 "@keyframes nu{0%,70%,100%{transform:translate(0,0)}80%{transform:translate(2px,-2px)}}"
                 ".nu{animation:nu 3.2s ease-in-out infinite}")
    d.defs.append(f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
                  f'<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="30" cy="0" r="300">'
                  f'<stop offset="0" stop-color="{acc}" stop-opacity="{0.2 if dark else 0.12}"/>'
                  f'<stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient>')
    sw = sweep_gradient(d, acc, W, 180, 6, begin=idx * 0.75)
    b = d.body
    b.append('<g clip-path="url(#cc)">'
             f'<rect width="{W}" height="{H}" fill="{t["card"]}"/>'
             f'<rect class="br" width="{W}" height="{H}" fill="url(#glow)"/>'
             f'<rect width="{W}" height="2" fill="url(#{sw})"/></g>')
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="15.5" fill="none" stroke="{t["border"]}"/>')

    cat = p["cat"] if p["slug"] == "more" else f'{idx + 1:02d} · {p["cat"]}'
    b.append(d.text(24, 37, cat, "mono", 500, 11, acc, ls=1.3))
    if p["live"]:
        lw = measure("LIVE", "mono", 500, 10.5, 1.2) + 34
        x = W - 22 - lw
        b.append(f'<rect x="{x:.1f}" y="21" width="{lw:.1f}" height="22" rx="11" fill="{t["green"]}" '
                 f'fill-opacity="0.12" stroke="{t["green"]}" stroke-opacity="0.35"/>')
        b.append(pulse_dot(round(x + 13, 1), 32, t["green"], r=3))
        b.append(d.text(x + 23, 35.8, "LIVE", "mono", 500, 10.5, t["green"], ls=1.2))

    b.append(d.text(23, 78, p["title"], "sans", 600, 25, t["text"], ls=-0.5))
    lines = wrap(p["desc"], "sans", 400, 13.5, W - 48)[:3]
    y = 104
    for ln in lines:
        b.append(d.text(24, y, ln, "sans", 400, 13.5, t["muted"]))
        y += 19.5
    b.append(d.text(24, y + 8, "→ " + p["metric"], "mono", 500, 11.5, acc))

    x, cy = 24, H - 46
    for c in p["chips"]:
        w = measure(c, "mono", 400, 10.5) + 18
        if x + w > W - 60:
            break
        b.append(f'<rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="23" rx="6" fill="{t["card2"]}" '
                 f'stroke="{t["border"]}"/>')
        b.append(d.text(x + w / 2, cy + 15.5, c, "mono", 400, 10.5, t["muted"], anchor="middle"))
        x += w + 6
    b.append(f'<circle cx="{W - 36}" cy="{cy + 11.5}" r="15" fill="{t["card2"]}" stroke="{t["border"]}"/>')
    b.append('<g class="nu">' + d.text(W - 36, cy + 17, "↗", "sans", 500, 15, acc, anchor="middle") + "</g>")
    return d.render()


# ---------------------------------------------------------------- buttons and pills


def button(t, label, kind, primary):
    h = 44
    tw = measure(label, "sans", 600, 14.5)
    W = int(20 + 16 + 10 + tw + 22)
    d = Svg(W, h, t, label)
    b = d.body
    if primary:
        d.defs.append('<clipPath id="bc"><rect width="100%" height="100%" rx="12"/></clipPath>'
                      '<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#fff" '
                      'stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.35"/>'
                      '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        b.append(f'<rect width="{W}" height="{h}" rx="12" fill="{t["accent"]}"/>')
        b.append(f'<g clip-path="url(#bc)"><rect x="-80" y="0" width="60" height="{h}" fill="url(#sh)" '
                 f'transform="skewX(-20)"><animate attributeName="x" values="-80;-80;{W + 40}" '
                 f'keyTimes="0;0.7;1" dur="4.5s" repeatCount="indefinite"/></rect></g>')
        fg = t["on_accent"]
    else:
        b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="11.5" fill="{t["card"]}" '
                 f'stroke="{t["border2"]}"/>')
        fg = t["text"]
    b.append(ui_icon(kind, 20, 14, fg))
    b.append(d.text(46, 27, label, "sans", 600, 14.5, fg))
    return d.render(), W


def live_pill(t, name, idx):
    W, H = 206, 50
    d = Svg(W, H, t, f"{name}: open the live demo")
    b = d.body
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["card"]}" '
             f'stroke="{t["border2"]}"/>')
    b.append(pulse_dot(22, 25, t["green"], r=4))
    b.append(d.text(40, 22.5, name, "sans", 600, 14.5, t["text"]))
    b.append(d.text(40, 38, "LIVE DEMO", "mono", 500, 10, t["green"], ls=1.2))
    b.append('<g class="nu">' + d.text(W - 20, 31, "↗", "sans", 500, 16, t["muted"], anchor="middle") + "</g>")
    d.css.append("@keyframes nu{0%,70%,100%{transform:translate(0,0)}80%{transform:translate(2px,-2px)}}"
                 f".nu{{animation:nu 3.2s ease-in-out {idx * 0.4}s infinite}}")
    return d.render()


# ---------------------------------------------------------------- toolbox


def toolbox(t):
    W, H = 1200, 368
    labels = ", ".join(f'{grp}: {", ".join(n for n, _ in items)}' for grp, items in TOOLBOX)
    d = Svg(W, H, t, "Toolbox. " + labels)
    d.css.append("@keyframes ri{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
                 ".it{animation:ri .7s cubic-bezier(.2,.7,.2,1) both}")
    b = d.body
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{t["card"]}" '
             f'stroke="{t["border"]}"/>')
    colw = (W - 64) / 5
    for ci, (grp, items) in enumerate(TOOLBOX):
        x0 = 36 + ci * colw
        b.append(d.text(x0, 46, grp, "mono", 500, 11.5, t["dim"], ls=1.6))
        if ci:
            b.append(f'<line x1="{x0 - 16:.1f}" y1="30" x2="{x0 - 16:.1f}" y2="{H - 30}" stroke="{t["border"]}"/>')
        for ri, (name, ic) in enumerate(items):
            y = 70 + ri * 47
            col = "#" + ICONS[ic]["hex"] if ic in ICONS else t["text"]
            lum = luminance(col)
            if t["name"] == "dark" and lum < 0.07:
                col = t["text"]
            if t["name"] == "light" and lum > 0.55:
                col = darken(col, 0.28)
            delay = 0.15 + ci * 0.09 + ri * 0.07
            b.append(f'<g class="it" style="animation-delay:{delay:.2f}s">'
                     f'<rect x="{x0:.1f}" y="{y}" width="32" height="32" rx="9" fill="{t["card2"]}" '
                     f'stroke="{t["border"]}"/>' + icon(ic, x0 + 7, y + 7, 18, col)
                     + d.text(x0 + 44, y + 21.5, name, "sans", 500, 15, t["text"]) + "</g>")
    return d.render()


# ---------------------------------------------------------------- footer


def wave_path(width, amp, wl, base):
    d = f"M0 {base}"
    x = 0
    while x < width:
        d += f" q{wl / 4} {-amp} {wl / 2} 0 t{wl / 2} 0"
        x += wl
    return d + f" V{base + 60} H0 Z"


def footer(t):
    W, H = 1200, 170
    d = Svg(W, H, t, "Let's build something that ships. pranjalagarwal.me")
    d.css.append("@keyframes wv{from{transform:translateX(0)}to{transform:translateX(-300px)}}"
                 ".w1{animation:wv 9s linear infinite}.w2{animation:wv 13s linear infinite reverse}"
                 ".w3{animation:wv 17s linear infinite}")
    d.defs.append(f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    b = d.body
    b.append('<g clip-path="url(#fc)">')
    for cls, col, amp, base, op in (("w1", t["accent"], 10, 128, 0.22), ("w2", t["violet"], 13, 138, 0.18),
                                    ("w3", t["green"], 8, 150, 0.16)):
        b.append(f'<path class="{cls}" d="{wave_path(W + 600, amp, 300, base)}" fill="{col}" fill-opacity="{op}"/>')
    b.append("</g>")
    b.append(d.text(W / 2, 56, "Let's build something that ships.", "sans", 600, 28, t["text"], anchor="middle",
                    ls=-0.5))
    b.append(d.text(W / 2, 88, "PRANJALAGARWAL.ME  ·  AGARWALPRANJAL2006@GMAIL.COM", "mono", 400, 12.5,
                    t["muted"], anchor="middle", ls=1.6))
    return d.render()


# ---------------------------------------------------------------- README

RAW = "https://raw.githubusercontent.com/pranjal-agarwal01/pranjal-agarwal01/main/assets"
SNAKE = "https://raw.githubusercontent.com/pranjal-agarwal01/pranjal-agarwal01/output"
LINKS = {
    "stationwatch": (f"{REPO}/Station-Facility-Monitor-Escalator-using-Computer-Vision-",
                     "https://stationwatch.pranjalagarwal.me"),
    "supplysense": (f"{REPO}/SupplySenseAI---Prototype-Phase1", "https://supplysenseai.pranjalagarwal.me"),
    "debator": (f"{REPO}/Debator", "https://debator.pranjalagarwal.me"),
    "everlink": (f"{REPO}/Everlink", None),
    "booking": (f"{REPO}/Event-Booking", "https://booking-api-rdhs.onrender.com"),
    "newsletter": (f"{REPO}/AI_Newsletter", None),
    "sevcs": (f"{REPO}/Smart-Emergency-Vehicle-Clearance-System-SEVCS-", None),
    "more": ("https://pranjalagarwal.me", None),
}
CONTACT = {
    "portfolio": "https://pranjalagarwal.me",
    "linkedin": "https://www.linkedin.com/in/pranjal-agarwal01",
    "email": "mailto:agarwalpranjal2006@gmail.com",
    "resume-swe": "https://drive.google.com/file/d/10pPUyGeQlVScCIfxFWTPyAespluQnyCc/view",
    "resume-ml": "https://drive.google.com/file/d/1MHN6AeDM0Cld79VZSwS21Gejd-SE_MJv/view",
}


def pic(name, alt, width=None, height=None, base=RAW, dark=None, light=None):
    dark = dark or f"{base}/dark/{name}.svg"
    light = light or f"{base}/light/{name}.svg"
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
            f'<img alt="{escape(alt, {chr(34): "&quot;"})}" src="{light}"{size}></picture>')


def readme(button_widths):
    out = []
    out.append(f'<a href="{CONTACT["portfolio"]}">'
               + pic("header", "Pranjal Agarwal. Products that ship, not demos that die in notebooks. "
                               "Open to SDE, full-stack and ML roles.", width="100%") + "</a>")
    out.append("")
    out.append('<p align="center">')
    for slug, label, _, _ in BUTTONS:
        out.append(f'  <a href="{CONTACT[slug]}">' + pic(f"btn-{slug}", label, height=40) + "</a>")
    out.append("</p>")
    out.append("")
    out.append(pic("terminal", "whoami: Pranjal Agarwal, final-year B.Tech CSE at Lovely Professional "
                               "University. Focus: full-stack, computer vision, AI agents and automation. "
                               "Open to SDE, full-stack and ML roles, and freelance n8n automation.",
                   width="100%"))
    out.append("")
    out.append("<br>")
    out.append("")
    out.append(pic("section-featured", "01 Featured work", width="100%"))
    out.append("")
    out.append('<p align="center">')
    for p in PROJECTS:
        href = LINKS[p["slug"]][0]
        alt = f'{p["title"]}: {p["desc"]} {p["metric"]}.'
        out.append(f'  <a href="{href}">' + pic(f'card-{p["slug"]}', alt, width="49%") + "</a>")
    out.append("</p>")
    out.append("")
    out.append(pic("section-live", "02 Try it live", width="100%"))
    out.append("")
    out.append('<p align="center">')
    for slug, label in LIVE_DEMOS:
        out.append(f'  <a href="{LINKS[slug][1]}">' + pic(f"live-{slug}", f"{label} live demo", width="23.5%")
                   + "</a>")
    out.append("</p>")
    out.append('<p align="center"><sub>Demos run on free hosting, so the first visit can take up to a '
               "minute to wake up.</sub></p>")
    out.append("")
    out.append(pic("section-toolbox", "03 Toolbox", width="100%"))
    out.append("")
    tools = "; ".join(f'{g.title()}: {", ".join(n for n, _ in items)}' for g, items in TOOLBOX)
    out.append(pic("toolbox", "Toolbox. " + tools, width="100%"))
    out.append("")
    out.append(pic("section-activity", "04 Activity", width="100%"))
    out.append("")
    out.append(pic("snake", "A snake eating my GitHub contribution graph", width="100%",
                   dark=f"{SNAKE}/snake-dark.svg", light=f"{SNAKE}/snake-light.svg"))
    out.append("")
    out.append("<details>")
    out.append("<summary><b>Text version of the projects</b> (for screen readers and quick copying)</summary>")
    out.append("")
    out.append("| Project | What it does | Links |")
    out.append("| --- | --- | --- |")
    for p in PROJECTS:
        if p["slug"] == "more":
            continue
        repo, demo = LINKS[p["slug"]]
        links = (f"[Live demo]({demo}) · " if demo else "") + f"[Code]({repo})"
        out.append(f'| **{p["title"]}** | {p["desc"]} {p["metric"]}. | {links} |')
    out.append("")
    out.append("</details>")
    out.append("")
    out.append(f'<a href="{CONTACT["portfolio"]}">'
               + pic("footer", "Let's build something that ships. pranjalagarwal.me", width="100%") + "</a>")
    out.append("")
    out.append("<!-- Artwork is generated by tools/generate.py; edit the data there and re-run. -->")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- main


def write(theme, name, svg):
    out = os.path.join(ROOT, "assets", theme, name + ".svg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return os.path.getsize(out)


def main():
    total = 0
    widths = {}
    for name, t in THEMES.items():
        total += write(name, "header", header(t))
        total += write(name, "terminal", terminal(t))
        for key, title, hint in (("featured", "Featured work", "7 PROJECTS · CLICK A CARD FOR THE CODE"),
                                 ("live", "Try it live", "RUNS IN YOUR BROWSER · NO SIGN-UP"),
                                 ("toolbox", "Toolbox", "WHAT I'VE SHIPPED WITH"),
                                 ("activity", "Activity", "UPDATED DAILY BY GITHUB ACTIONS")):
            idx = {"featured": "01", "live": "02", "toolbox": "03", "activity": "04"}[key]
            total += write(name, f"section-{key}", section(t, idx, title, hint))
        for i, p in enumerate(PROJECTS):
            total += write(name, f"card-{p['slug']}", card(t, p, i))
        for i, (slug, label) in enumerate(LIVE_DEMOS):
            total += write(name, f"live-{slug}", live_pill(t, label, i))
        for slug, label, kind, primary in BUTTONS:
            svg, w = button(t, label, kind, primary)
            widths[slug] = w
            total += write(name, f"btn-{slug}", svg)
        total += write(name, "toolbox", toolbox(t))
        total += write(name, "footer", footer(t))
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(readme(widths))
    print(f"wrote assets ({total / 1024:.0f} KB total) and README.md")


if __name__ == "__main__":
    main()
