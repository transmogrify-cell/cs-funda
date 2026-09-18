#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_readme_assets.py  —  cs-funda README asset generator
=========================================================
Generates every animated SVG used by README.md, in matching dark + light
blueprint variants. Zero third-party services: the SVGs live in this repo
and animate entirely on their own (SMIL + CSS inside the SVG).

    python3 tools/gen_readme_assets.py

Outputs into ./assets/. Edit PROGRESS below and re-run to refresh the
progress schedule chart.
"""

import os
import math
import argparse

# --------------------------------------------------------------------------
# EDIT ME — module completion, 0..100. Re-run the script to refresh the chart.
# --------------------------------------------------------------------------
PROGRESS = [
    ("MOD-01", "Data Structures & Algorithms", 18),
    ("MOD-02", "Operating Systems",            12),
    ("MOD-03", "Database Systems",              9),
    ("MOD-04", "Computer Networks",             7),
    ("MOD-05", "OOP & Design Patterns",        15),
    ("MOD-06", "System Design",                22),
]

TYPING_PHRASES = [
    "Data Structures & Algorithms",
    "Operating Systems",
    "Database Management Systems",
    "Computer Networks",
    "Object-Oriented Design",
    "System Design at Scale",
]

AUTHOR = "@transmogrify-cell"
PROJECT = "CS-FUNDA"
DRAWING_NO = "CSF-2026-01"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"

THEMES = {
    "dark": dict(
        bg="#071a2f", bg2="#0d2f52", panel="#0a2542",
        grid="#7fd4ff", gridMinorOp=0.055, gridMajorOp=0.13,
        ink="#e8f5ff", inkDim="#a8cde9", inkFaint="#5f8cb0",
        line="#9ecbec", lineOp=0.55,
        accent="#5eead4", accent2="#38bdf8", amber="#fbbf24",
        glow=1,
    ),
    "light": dict(
        bg="#f5f9fd", bg2="#e2edf7", panel="#eaf2fa",
        grid="#0a2540", gridMinorOp=0.07, gridMajorOp=0.16,
        ink="#0a2540", inkDim="#2f5b80", inkFaint="#6d8da8",
        line="#14456e", lineOp=0.55,
        accent="#0d9488", accent2="#0369a1", amber="#b45309",
        glow=0,
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(x):
    """Trim floats so the SVG source stays readable."""
    return f"{x:.2f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------
# shared fragments
# --------------------------------------------------------------------------

def defs_common(t, p):
    """Grid patterns, glow filter, gradients. `p` namespaces the ids."""
    glow = ""
    if t["glow"]:
        glow = f'''
    <filter id="{p}-glow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}-glow-s" x="-90%" y="-90%" width="280%" height="280%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>'''
    else:
        glow = f'''
    <filter id="{p}-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="0"/>
    </filter>
    <filter id="{p}-glow-s" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="0"/>
    </filter>'''

    return f'''    <pattern id="{p}-gmin" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0H0V20" fill="none" stroke="{t['grid']}" stroke-width="0.7" stroke-opacity="{t['gridMinorOp']}"/>
    </pattern>
    <pattern id="{p}-gmaj" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#{p}-gmin)"/>
      <path d="M100 0H0V100" fill="none" stroke="{t['grid']}" stroke-width="1.1" stroke-opacity="{t['gridMajorOp']}"/>
    </pattern>
    <linearGradient id="{p}-title" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0%" stop-color="{t['ink']}"/>
      <stop offset="55%" stop-color="{t['accent']}"/>
      <stop offset="100%" stop-color="{t['accent2']}"/>
    </linearGradient>
    <linearGradient id="{p}-bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent2']}"/>
      <stop offset="100%" stop-color="{t['accent']}"/>
    </linearGradient>
    <linearGradient id="{p}-sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset="72%" stop-color="{t['accent']}" stop-opacity="{0.10 if t['glow'] else 0.07}"/>
      <stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="{p}-vig" cx="0.5" cy="0.42" r="0.78">
      <stop offset="0%" stop-color="{t['bg2']}" stop-opacity="{0.85 if t['glow'] else 0.55}"/>
      <stop offset="100%" stop-color="{t['bg']}" stop-opacity="0"/>
    </radialGradient>
{glow}'''


def bg_layers(t, p, w, h):
    return (f'  <rect width="{w}" height="{h}" fill="{t["bg"]}"/>\n'
            f'  <rect width="{w}" height="{h}" fill="url(#{p}-vig)"/>\n'
            f'  <rect width="{w}" height="{h}" fill="url(#{p}-gmaj)"/>\n')


def corner_marks(t, pts, r=7, cls="cm"):
    """Drafting registration crosshairs."""
    out = []
    for i, (x, y) in enumerate(pts):
        out.append(
            f'  <g class="{cls}" style="animation-delay:{0.9 + i * 0.12:.2f}s">'
            f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="none" stroke="{t["line"]}" stroke-width="1" stroke-opacity=".7"/>'
            f'<path d="M{fmt(x - r - 5)} {fmt(y)}H{fmt(x + r + 5)}M{fmt(x)} {fmt(y - r - 5)}V{fmt(y + r + 5)}" '
            f'stroke="{t["line"]}" stroke-width="1" stroke-opacity=".7"/></g>')
    return "\n".join(out) + "\n"


def edge_ticks(t, x0, y0, x1, y1, step=40, size=5):
    """Ruler ticks along the inside of a drafting frame."""
    d = []
    x = x0 + step
    while x < x1:
        d.append(f"M{fmt(x)} {fmt(y0)}v{size}")
        d.append(f"M{fmt(x)} {fmt(y1)}v-{size}")
        x += step
    y = y0 + step
    while y < y1:
        d.append(f"M{fmt(x0)} {fmt(y)}h{size}")
        d.append(f"M{fmt(x1)} {fmt(y)}h-{size}")
        y += step
    return (f'  <path class="fade" style="animation-delay:1.1s" d="{"".join(d)}" '
            f'stroke="{t["line"]}" stroke-width="1" stroke-opacity=".38" fill="none"/>\n')


def dim_line(t, x0, x1, y, label, p, delay=1.6, fs=10.5):
    """Dimension line with arrow terminators and a centred caption."""
    a = 5.0
    mid = (x0 + x1) / 2
    lw = len(label) * (fs * 0.6 + 1.6) + 22
    return f'''  <g class="fade" style="animation-delay:{delay}s">
    <path d="M{fmt(x0)} {fmt(y - 6)}v12M{fmt(x1)} {fmt(y - 6)}v12" stroke="{t['line']}" stroke-width="1" stroke-opacity=".6"/>
    <path d="M{fmt(x0)} {fmt(y)}H{fmt(mid - lw / 2)}M{fmt(mid + lw / 2)} {fmt(y)}H{fmt(x1)}" stroke="{t['line']}" stroke-width="1" stroke-opacity=".6"/>
    <path d="M{fmt(x0)} {fmt(y)}l{fmt(a * 1.7)} -{fmt(a * 0.7)}v{fmt(a * 1.4)}z" fill="{t['line']}" fill-opacity=".75"/>
    <path d="M{fmt(x1)} {fmt(y)}l-{fmt(a * 1.7)} -{fmt(a * 0.7)}v{fmt(a * 1.4)}z" fill="{t['line']}" fill-opacity=".75"/>
    <text x="{fmt(mid + 0.8)}" y="{fmt(y + 3.6)}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" letter-spacing="1.6" fill="{t['inkFaint']}">{esc(label)}</text>
  </g>
'''


BASE_CSS = """
    .fade{opacity:0;animation:fade .9s ease-out forwards}
    .cm{opacity:0;animation:fade .7s ease-out forwards}
    .draw{stroke-dasharray:var(--d,420);stroke-dashoffset:var(--d,420);animation:draw 1.8s ease-out forwards}
    @keyframes fade{to{opacity:1}}
    @keyframes draw{to{stroke-dashoffset:0}}
    @keyframes blink{0%,45%{opacity:1}55%,100%{opacity:.12}}
    @keyframes sweep{0%{transform:translate(var(--s,-300px),0)}100%{transform:translate(var(--e,1300px),0)}}
"""


def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t d" preserveAspectRatio="xMidYMid meet">\n'
            f'  <title id="t">{esc(title)}</title>\n  <desc id="d">{esc(desc)}</desc>\n')


# ==========================================================================
# 1. BANNER
# ==========================================================================

def banner(t, p="b"):
    W, H = 1000, 320
    fx0, fy0, fx1, fy1 = 24, 24, 976, 296

    s = svg_open(W, H, "cs-funda — computer science engineering notebook",
                 "Animated blueprint banner: drafting frame, CS-FUNDA title, module list and a rotating technical rosette.")
    s += f'  <defs>\n{defs_common(t, p)}\n'
    s += f'''    <linearGradient id="{p}-wedge" x1="0" y1="0" x2="0.8" y2="0.8">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="{0.42 if t['glow'] else 0.3}"/>
      <stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="{p}-clip"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
  </defs>
'''
    s += f'''  <style>{BASE_CSS}
    .ttl-s{{fill:none;stroke:{t['ink']};stroke-width:1.15;stroke-opacity:.9;stroke-dasharray:400;stroke-dashoffset:400;animation:draw 2.3s ease-out forwards}}
    .ttl-f{{opacity:0;animation:fade 1.5s ease-out 1.25s forwards}}
    .rule{{stroke-dasharray:520;stroke-dashoffset:520;animation:draw 1.5s ease-out .35s forwards}}
    .frm{{stroke-dasharray:2450;stroke-dashoffset:2450;animation:draw 2.6s ease-out forwards}}
    .led{{animation:blink 1.7s ease-in-out infinite}}
    .swp{{--s:-300px;--e:1320px;animation:sweep 7s cubic-bezier(.4,0,.2,1) 1.6s infinite}}
  </style>
'''
    s += bg_layers(t, p, W, H)

    # drafting frame
    s += (f'  <rect class="frm" x="{fx0}" y="{fy0}" width="{fx1 - fx0}" height="{fy1 - fy0}" rx="2" fill="none" '
          f'stroke="{t["line"]}" stroke-width="1.3" stroke-opacity=".55"/>\n')
    s += edge_ticks(t, fx0, fy0, fx1, fy1, step=40, size=5)
    s += corner_marks(t, [(fx0 + 22, fy0 + 22), (fx1 - 22, fy0 + 22), (fx0 + 22, fy1 - 22), (fx1 - 22, fy1 - 22)])

    # top metadata row
    s += f'''  <g class="fade" style="animation-delay:1.25s" font-family="{MONO}" font-size="10.5" letter-spacing="2.1" fill="{t['inkFaint']}">
    <text x="80" y="62">DRAWING No. {DRAWING_NO}</text>
    <text x="560" y="62">SCALE 1:1</text>
    <text x="700" y="62">SHEET 01 / 06</text>
  </g>
  <g class="fade" style="animation-delay:1.45s">
    <circle class="led" cx="880" cy="58" r="3.6" fill="{t['accent']}" filter="url(#{p}-glow-s)"/>
    <text x="893" y="62" font-family="{MONO}" font-size="10.5" letter-spacing="2.1" fill="{t['inkDim']}">ACTIVE</text>
  </g>
'''

    # title
    tspans = (f'<tspan fill="{t["ink"]}">CS</tspan>'
              f'<tspan fill="{t["amber"]}"> · </tspan>'
              f'<tspan fill="url(#{p}-title)">FUNDA</tspan>')
    s += f'''  <g font-family="{SANS}" font-size="80" font-weight="800" letter-spacing="7">
    <text class="ttl-s" x="80" y="166">CS · FUNDA</text>
    <text class="ttl-f" x="80" y="166">{tspans}</text>
  </g>
  <path class="rule" d="M80 186H600" stroke="{t['line']}" stroke-width="1.4" stroke-opacity=".6"/>
  <text class="fade" style="animation-delay:1.55s" x="80" y="213" font-family="{SANS}" font-size="14.5" letter-spacing="5.2" fill="{t['inkDim']}">COMPUTER SCIENCE · ENGINEERING NOTEBOOK</text>
  <text class="fade" style="animation-delay:1.75s" x="80" y="241" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="{t['accent']}">DSA ▸ OS ▸ DBMS ▸ NETWORKS ▸ OOP ▸ SYSTEM DESIGN</text>
'''
    s += dim_line(t, 80, 600, 272, "SCOPE — 6 MODULES / 120+ TOPICS", p, delay=2.0)

    # technical rosette
    cx, cy = 832, 160
    ticks = []
    for i in range(36):
        a = math.radians(i * 10)
        r0 = 62 if i % 3 else 56
        ticks.append(f"M{fmt(cx + r0 * math.cos(a))} {fmt(cy + r0 * math.sin(a))}"
                     f"L{fmt(cx + 72 * math.cos(a))} {fmt(cy + 72 * math.sin(a))}")
    wx, wy = 70 * math.cos(math.radians(42)), 70 * math.sin(math.radians(42))

    s += f'''  <g class="fade" style="animation-delay:.6s">
    <circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{t['line']}" stroke-width="1" stroke-opacity=".28" stroke-dasharray="5 7">
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="64s" repeatCount="indefinite"/>
    </circle>
    <g stroke="{t['line']}" stroke-width="1.1" stroke-opacity=".5">
      <path d="{''.join(ticks)}"/>
      <animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="90s" repeatCount="indefinite"/>
    </g>
    <circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{t['line']}" stroke-width="1" stroke-opacity=".45"/>
    <circle cx="{cx}" cy="{cy}" r="26" fill="{t['accent']}" fill-opacity=".07" stroke="{t['accent']}" stroke-width="1" stroke-opacity=".5"/>
    <path d="M{cx - 96} {cy}h{192}M{cx} {cy - 96}v192" stroke="{t['line']}" stroke-width="1" stroke-opacity=".3"/>
    <g>
      <path d="M0 0L70 0A70 70 0 0 1 {fmt(wx)} {fmt(wy)}Z" fill="url(#{p}-wedge)" transform="translate({cx},{cy})"/>
      <path d="M{cx} {cy}h70" stroke="{t['accent']}" stroke-width="1.3" stroke-opacity=".8" filter="url(#{p}-glow-s)"/>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/>
    </g>
    <circle cx="{cx}" cy="{cy}" r="3" fill="{t['amber']}"/>
    <circle r="3.4" fill="{t['accent2']}" filter="url(#{p}-glow-s)">
      <animateMotion dur="11s" repeatCount="indefinite" path="M{cx + 50} {cy}A50 50 0 1 1 {cx - 50} {cy}A50 50 0 1 1 {cx + 50} {cy}"/>
    </circle>
  </g>
  <g clip-path="url(#{p}-clip)"><rect class="swp" x="-300" y="24" width="300" height="272" fill="url(#{p}-sweep)"/></g>
</svg>
'''
    return s


# ==========================================================================
# 2. TYPING
# ==========================================================================

def typing(t, p="y"):
    W, H = 900, 96
    FS = 26.0
    CW = FS * 0.6
    TX = 214.0
    SLOT = 3.6
    total = SLOT * len(TYPING_PHRASES)

    # build a (time, visible-char-count) timeline per phrase
    tracks, cursor = [], []
    for i, ph in enumerate(TYPING_PHRASES):
        n = len(ph)
        t0 = i * SLOT
        pts = [(0.0, 0)] if i == 0 else [(0.0, 0), (max(0.0, t0 - 0.001), 0)]
        step = 1.55 / n
        for k in range(n + 1):
            pts.append((t0 + k * step, k))
        pts.append((t0 + 2.95, n))
        back = max(1, math.ceil(n / 12))
        k, tt = n, t0 + 2.95
        while k > 0:
            k = max(0, k - back)
            tt += 0.042
            pts.append((tt, k))
        pts.append((min(total, t0 + SLOT - 0.05), 0))
        if i == len(TYPING_PHRASES) - 1:
            pts.append((total, 0))
        # de-duplicate / clamp
        clean = []
        for tt, k in pts:
            tt = min(max(tt, 0.0), total)
            if clean and abs(tt - clean[-1][0]) < 1e-6:
                clean[-1] = (tt, k)
            else:
                clean.append((tt, k))
        tracks.append((ph, n, clean))
        cursor.extend([(tt, k) for tt, k in clean if t0 - 0.05 <= tt <= t0 + SLOT])

    cursor.sort(key=lambda z: z[0])
    if cursor[0][0] > 0:
        cursor.insert(0, (0.0, 0))
    if cursor[-1][0] < total:
        cursor.append((total, 0))

    def anim(seq, mapper):
        vals = ";".join(fmt(mapper(k)) for _, k in seq)
        keys = ";".join(f"{tt / total:.5f}" for tt, _ in seq)
        return vals, keys

    s = svg_open(W, H, "cs-funda modules, typed",
                 "Terminal-style annotation typing out the six computer science modules in a loop.")
    s += f'  <defs>\n{defs_common(t, p)}\n'
    for i, (ph, n, seq) in enumerate(tracks):
        v, k = anim(seq, lambda c: c * CW)
        s += (f'    <clipPath id="{p}-c{i}"><rect x="{fmt(TX)}" y="26" width="0" height="46">'
              f'<animate attributeName="width" values="{v}" keyTimes="{k}" calcMode="discrete" '
              f'dur="{fmt(total)}s" repeatCount="indefinite"/></rect></clipPath>\n')
    s += '  </defs>\n'
    s += f'''  <style>{BASE_CSS}
    .box{{stroke-dasharray:1900;stroke-dashoffset:1900;animation:draw 1.9s ease-out forwards}}
    .cur{{animation:blink 1.05s steps(1,end) infinite}}
  </style>
'''
    s += bg_layers(t, p, W, H)
    s += (f'  <rect class="box" x="12" y="12" width="876" height="72" rx="3" fill="{t["bg2"]}" fill-opacity="{.4 if t["glow"] else .55}" '
          f'stroke="{t["line"]}" stroke-width="1.2" stroke-opacity=".5" stroke-dasharray="1900"/>\n')
    s += corner_marks(t, [(30, 30), (870, 30), (30, 66), (870, 66)], r=4)
    s += (f'  <text class="fade" style="animation-delay:.7s" x="36" y="60" font-family="{MONO}" font-size="21" '
          f'fill="{t["amber"]}">~/cs-funda $</text>\n')

    for i, (ph, n, seq) in enumerate(tracks):
        s += (f'  <g clip-path="url(#{p}-c{i})"><text x="{fmt(TX)}" y="60" font-family="{MONO}" font-size="{fmt(FS)}" '
              f'fill="{t["ink"]}" textLength="{fmt(n * CW)}" lengthAdjust="spacingAndGlyphs">{esc(ph)}</text></g>\n')

    cv, ck = anim(cursor, lambda c: TX + c * CW + 2)
    s += f'''  <rect class="cur" x="{fmt(TX + 2)}" y="37" width="12" height="30" fill="{t['accent']}" fill-opacity=".85">
    <animate attributeName="x" values="{cv}" keyTimes="{ck}" calcMode="discrete" dur="{fmt(total)}s" repeatCount="indefinite"/>
  </rect>
</svg>
'''
    return s


# ==========================================================================
# 3. SPEC STAMPS  (self-hosted badge strip)
# ==========================================================================

def stamps(t, p="s"):
    chips = [
        ("LANG", "C++ · PY", t["accent"]),
        ("MODULES", "06", t["ink"]),
        ("TOPICS", "120+", t["ink"]),
        ("STATUS", "IN PROGRESS", t["amber"]),
        ("LICENSE", "MIT", t["accent2"]),
    ]
    pad, gap, H = 16, 14, 62
    widths, boxes = [], []
    for lab, val, _ in chips:
        # advance width = chars x (0.6em + letter-spacing); label 8.2/1.9, value 12.5/1.1
        lw = len(lab) * (8.2 * 0.6 + 1.9)
        vw = len(val) * (12.5 * 0.6 + 1.1)
        w = max(lw, vw) + pad * 2 + (22 if lab == "STATUS" else 0)
        widths.append(w)
    total = sum(widths) + gap * (len(chips) - 1)
    W = 900
    x = (W - total) / 2
    for i, ((lab, val, col), w) in enumerate(zip(chips, widths)):
        boxes.append((x, w, lab, val, col))
        x += w + gap

    s = svg_open(W, H, "cs-funda spec stamps",
                 "Blueprint specification chips: language, module count, topic count, status and licence.")
    s += f'  <defs>\n{defs_common(t, p)}\n  </defs>\n'
    s += f'''  <style>{BASE_CSS}
    .chip{{opacity:0;animation:fade .55s ease-out forwards}}
    .cdraw{{stroke-dasharray:var(--d,400);stroke-dashoffset:var(--d,400);animation:draw 1s ease-out forwards}}
    .led{{animation:blink 1.5s ease-in-out infinite}}
  </style>
'''
    for i, (x, w, lab, val, col) in enumerate(boxes):
        d = 0.15 + i * 0.13
        led, inner = "", w
        if lab == "STATUS":
            inner = w - 22                      # reserve the right strip for the lamp
            led = (f'<circle class="led" cx="{fmt(x + w - 14)}" cy="31" r="3.4" fill="{t["amber"]}" '
                   f'filter="url(#{p}-glow-s)"/>')
        dash = 2 * (w + 38) + 24                # full perimeter, so the box closes
        s += f'''  <g class="chip" style="animation-delay:{d:.2f}s">
    <rect class="cdraw" style="--d:{fmt(dash)};animation-delay:{d:.2f}s" x="{fmt(x)}" y="12" width="{fmt(w)}" height="38" rx="2"
      fill="{t['bg2']}" fill-opacity="{.55 if t['glow'] else .7}" stroke="{t['line']}" stroke-width="1.1" stroke-opacity=".7"/>
    <path d="M{fmt(x + 5)} 12v5M{fmt(x + w - 5)} 12v5M{fmt(x + 5)} 50v-5M{fmt(x + w - 5)} 50v-5" stroke="{t['line']}" stroke-width="1" stroke-opacity=".45"/>
    <text x="{fmt(x + inner / 2 + 0.95)}" y="26" text-anchor="middle" font-family="{MONO}" font-size="8.2" letter-spacing="1.9" fill="{t['inkFaint']}">{esc(lab)}</text>
    <text x="{fmt(x + inner / 2 + 0.55)}" y="42" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.1" fill="{col}">{esc(val)}</text>
    {led}
  </g>
'''
    s += "</svg>\n"
    return s


# ==========================================================================
# 4. PROGRESS SCHEDULE
# ==========================================================================

def roadmap(t, p="r"):
    W, H = 940, 500
    fx0, fy0, fx1, fy1 = 20, 20, 920, 480
    BX, BW = 420, 400
    rows = PROGRESS

    s = svg_open(W, H, "cs-funda progress schedule",
                 "Animated blueprint bar chart of completion for each of the six computer science modules.")
    s += f'  <defs>\n{defs_common(t, p)}\n  </defs>\n'
    s += f'''  <style>{BASE_CSS}
    .frm{{stroke-dasharray:2720;stroke-dashoffset:2720;animation:draw 2.4s ease-out forwards}}
    .flash{{opacity:0;animation:flash .144s linear forwards}}
    .settle{{opacity:0;animation:fade .35s ease-out forwards}}
    @keyframes flash{{0%{{opacity:1}}99%{{opacity:1}}100%{{opacity:0}}}}
  </style>
'''
    s += bg_layers(t, p, W, H)
    s += (f'  <rect class="frm" x="{fx0}" y="{fy0}" width="{fx1 - fx0}" height="{fy1 - fy0}" rx="2" fill="none" '
          f'stroke="{t["line"]}" stroke-width="1.3" stroke-opacity=".55"/>\n')
    s += corner_marks(t, [(fx0 + 20, fy0 + 20), (fx1 - 20, fy0 + 20), (fx0 + 20, fy1 - 20), (fx1 - 20, fy1 - 20)], r=6)

    s += f'''  <g class="fade">
    <text x="48" y="60" font-family="{SANS}" font-size="19" font-weight="700" letter-spacing="3.4" fill="{t['ink']}">PROGRESS SCHEDULE</text>
    <text x="48" y="80" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">MODULE COMPLETION — SELF ASSESSED</text>
    <text x="892" y="60" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">SHEET 03 / 06</text>
    <text x="892" y="80" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">REV 1.0</text>
  </g>
  <path class="fade" style="animation-delay:.3s" d="M48 92H892" stroke="{t['line']}" stroke-width="1" stroke-opacity=".4"/>
'''
    # scale
    for j in range(5):
        gx = BX + BW * j / 4
        s += (f'  <g class="fade" style="animation-delay:.45s">'
              f'<path d="M{fmt(gx)} 104v{fmt(302)}" stroke="{t["line"]}" stroke-width="1" stroke-opacity=".18" stroke-dasharray="2 5"/>'
              f'<text x="{fmt(gx)}" y="{fmt(100)}" text-anchor="middle" font-family="{MONO}" font-size="9" '
              f'fill="{t["inkFaint"]}">{j * 25}{"%" if j == 4 else ""}</text></g>\n')

    for i, (code, name, pct) in enumerate(rows):
        cy = 124 + i * 48
        d = 0.55 + i * 0.16
        fw = BW * pct / 100.0
        s += f'''  <g class="fade" style="animation-delay:{d:.2f}s">
    <text x="48" y="{fmt(cy + 4)}" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="{t['inkFaint']}">{code}</text>
    <text x="116" y="{fmt(cy + 4)}" font-family="{SANS}" font-size="14.5" fill="{t['ink']}">{esc(name)}</text>
    <rect x="{BX}" y="{fmt(cy - 7)}" width="{BW}" height="14" rx="2" fill="{t['ink']}" fill-opacity=".05" stroke="{t['line']}" stroke-width="1" stroke-opacity=".3" stroke-dasharray="3 3"/>
  </g>
  <rect x="{BX}" y="{fmt(cy - 7)}" width="0" height="14" rx="2" fill="url(#{p}-bar)" fill-opacity=".9">
    <animate attributeName="width" from="0" to="{fmt(fw)}" dur="1.3s" begin="{d + .25:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22 1 .36 1"/>
  </rect>
  <rect x="{BX}" y="{fmt(cy - 10)}" width="2" height="20" fill="{t['accent']}" filter="url(#{p}-glow-s)" opacity="0">
    <animate attributeName="x" from="{BX}" to="{fmt(BX + fw)}" dur="1.3s" begin="{d + .25:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22 1 .36 1"/>
    <animate attributeName="opacity" values="0;1;1;.75" keyTimes="0;.08;.9;1" dur="1.3s" begin="{d + .25:.2f}s" fill="freeze"/>
  </rect>
'''
        # count-up numerals
        steps = 8
        for k in range(steps):
            v = round(pct * (k + 1) / (steps + 1))
            s += (f'  <text class="flash" style="animation-delay:{d + .3 + k * (1.15 / steps):.3f}s" x="892" y="{fmt(cy + 4)}" '
                  f'text-anchor="end" font-family="{MONO}" font-size="13.5" font-weight="700" fill="{t["accent"]}">{v}%</text>\n')
        s += (f'  <text class="settle" style="animation-delay:{d + 1.5:.2f}s" x="892" y="{fmt(cy + 4)}" text-anchor="end" '
              f'font-family="{MONO}" font-size="13.5" font-weight="700" fill="{t["accent"]}">{pct}%</text>\n')

    # aggregate
    avg = sum(r[2] for r in rows) / len(rows)
    ay = 124 + len(rows) * 48 + 14
    ad = 0.55 + len(rows) * 0.16
    s += f'''  <path class="fade" style="animation-delay:{ad:.2f}s" d="M48 {fmt(ay - 24)}H892" stroke="{t['line']}" stroke-width="1" stroke-opacity=".4"/>
  <g class="fade" style="animation-delay:{ad + .1:.2f}s">
    <text x="48" y="{fmt(ay + 4)}" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="{t['amber']}">TOTAL</text>
    <text x="116" y="{fmt(ay + 4)}" font-family="{SANS}" font-size="14.5" font-weight="700" fill="{t['ink']}">Aggregate completion</text>
    <rect x="{BX}" y="{fmt(ay - 7)}" width="{BW}" height="14" rx="2" fill="{t['ink']}" fill-opacity=".05" stroke="{t['amber']}" stroke-width="1" stroke-opacity=".45" stroke-dasharray="3 3"/>
  </g>
  <rect x="{BX}" y="{fmt(ay - 7)}" width="0" height="14" rx="2" fill="{t['amber']}" fill-opacity=".85">
    <animate attributeName="width" from="0" to="{fmt(BW * avg / 100)}" dur="1.4s" begin="{ad + .3:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22 1 .36 1"/>
  </rect>
  <text class="settle" style="animation-delay:{ad + 1.6:.2f}s" x="892" y="{fmt(ay + 4)}" text-anchor="end" font-family="{MONO}" font-size="13.5" font-weight="700" fill="{t['amber']}">{avg:.0f}%</text>
  <text class="fade" style="animation-delay:{ad + 1.8:.2f}s" x="66" y="466" font-family="{MONO}" font-size="9.5" letter-spacing="1.4" fill="{t['inkFaint']}">△ VALUES MAINTAINED IN tools/gen_readme_assets.py — RE-RUN TO REGENERATE</text>
</svg>
'''
    return s


# ==========================================================================
# 5. REFERENCE ARCHITECTURE
# ==========================================================================

NODES = [
    # key,        col, row, title,              sub
    ("cli",  0, 1, "CLIENTS",        "web · mobile · cli"),
    ("cdn",  1, 0, "CDN / EDGE",     "static · tls"),
    ("lb",   1, 1, "LOAD BALANCER",  "l4 · health check"),
    ("obs",  1, 2, "OBSERVABILITY",  "logs · traces"),
    ("auth", 2, 0, "AUTH · LIMIT", "jwt · token bucket"),
    ("gw",   2, 1, "API GATEWAY",    "routing · retry"),
    ("cache", 3, 0, "CACHE",         "lru · write-through"),
    ("app",  3, 1, "APP SERVICES",   "stateless · n×"),
    ("mq",   3, 2, "MESSAGE QUEUE",  "at-least-once"),
    ("db",   4, 1, "PRIMARY DB",     "acid · wal"),
    ("rep",  4, 0, "READ REPLICA",   "async · lag"),
    ("wrk",  4, 2, "WORKERS",        "idempotent"),
]

EDGES = [
    ("cli", "lb", "h", "https"),
    ("lb", "gw", "h", ""),
    ("gw", "app", "h", "rpc"),
    ("app", "db", "h", "sql"),
    ("lb", "cdn", "v", ""),
    ("lb", "obs", "v", ""),
    ("gw", "auth", "v", ""),
    ("app", "cache", "v", ""),
    ("app", "mq", "v", ""),
    ("db", "rep", "v", ""),
    ("mq", "wrk", "h", "jobs"),
]


def architecture(t, p="a"):
    W, H = 960, 540
    NW, NH = 146, 54
    COLS = [28, 218, 408, 598, 788]
    ROWS = [112, 236, 360]

    pos = {}
    for key, c, r, title, sub in NODES:
        pos[key] = (COLS[c], ROWS[r], title, sub)

    s = svg_open(W, H, "cs-funda reference architecture",
                 "Animated blueprint of a scalable web system: clients, load balancer, gateway, services, cache, queue and databases, with request packets flowing between them.")
    s += f'  <defs>\n{defs_common(t, p)}\n  </defs>\n'
    s += f'''  <style>{BASE_CSS}
    .frm{{stroke-dasharray:2900;stroke-dashoffset:2900;animation:draw 2.5s ease-out forwards}}
    .nd{{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 1s ease-out forwards}}
    .lnk{{stroke-dasharray:var(--l,120);stroke-dashoffset:var(--l,120);animation:draw .8s ease-out forwards}}
  </style>
'''
    s += bg_layers(t, p, W, H)
    s += (f'  <rect class="frm" x="16" y="16" width="928" height="508" rx="2" fill="none" '
          f'stroke="{t["line"]}" stroke-width="1.3" stroke-opacity=".55"/>\n')
    s += corner_marks(t, [(36, 36), (924, 36), (36, 504), (924, 504)], r=6)
    s += f'''  <g class="fade">
    <text x="44" y="56" font-family="{SANS}" font-size="19" font-weight="700" letter-spacing="3.4" fill="{t['ink']}">REFERENCE ARCHITECTURE</text>
    <text x="44" y="76" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">READ-HEAVY WEB SYSTEM — REQUEST PATH ▸ LEFT TO RIGHT</text>
    <text x="916" y="56" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">SHEET 05 / 06</text>
    <text x="916" y="76" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="{t['inkFaint']}">MOD-06</text>
  </g>
'''

    # ---- edges (drawn first, under the nodes)
    delay0 = 0.9
    motions = []
    for i, (a, b, kind, lab) in enumerate(EDGES):
        ax, ay, _, _ = pos[a]
        bx, by, _, _ = pos[b]
        acx, acy = ax + NW / 2, ay + NH / 2
        bcx, bcy = bx + NW / 2, by + NH / 2
        if kind == "h":
            x0, x1 = (ax + NW, bx) if bx > ax else (ax, bx + NW)
            d = f"M{fmt(x0)} {fmt(acy)}H{fmt(x1)}"
            length = abs(x1 - x0)
            lx, ly = (x0 + x1) / 2, acy - 8
        else:
            y0, y1 = (ay, by + NH) if by < ay else (ay + NH, by)
            d = f"M{fmt(acx)} {fmt(y0)}V{fmt(y1)}"
            length = abs(y1 - y0)
            lx, ly = acx + 6, (y0 + y1) / 2
        dly = delay0 + i * 0.09
        s += (f'  <path class="lnk" style="--l:{fmt(length)};animation-delay:{dly:.2f}s" d="{d}" fill="none" '
              f'stroke="{t["line"]}" stroke-width="1.2" stroke-opacity=".55"/>\n')
        if lab:
            s += (f'  <text class="fade" style="animation-delay:{dly + .5:.2f}s" x="{fmt(lx)}" y="{fmt(ly)}" '
                  f'text-anchor="{"middle" if kind == "h" else "start"}" font-family="{MONO}" font-size="8.5" '
                  f'letter-spacing="1.2" fill="{t["inkFaint"]}">{esc(lab)}</text>\n')
        motions.append((d, length, dly))

    # ---- nodes
    for i, (key, c, r, title, sub) in enumerate(NODES):
        x, y, _, _ = pos[key]
        dly = 0.25 + i * 0.07
        spine = key in ("cli", "lb", "gw", "app", "db")
        col = t["accent"] if spine else t["line"]
        s += f'''  <g class="fade" style="animation-delay:{dly:.2f}s">
    <rect class="nd" style="animation-delay:{dly:.2f}s" x="{fmt(x)}" y="{fmt(y)}" width="{NW}" height="{NH}" rx="3"
      fill="{t['bg2']}" fill-opacity="{.5 if t['glow'] else .62}" stroke="{col}" stroke-width="1.2" stroke-opacity="{.85 if spine else .5}"/>
    <path d="M{fmt(x + 6)} {fmt(y)}v6M{fmt(x + NW - 6)} {fmt(y)}v6M{fmt(x + 6)} {fmt(y + NH)}v-6M{fmt(x + NW - 6)} {fmt(y + NH)}v-6"
      stroke="{col}" stroke-width="1" stroke-opacity=".55"/>
    <text x="{fmt(x + NW / 2)}" y="{fmt(y + 24)}" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="700" letter-spacing="1.3" fill="{t['ink']}">{esc(title)}</text>
    <text x="{fmt(x + NW / 2)}" y="{fmt(y + 40)}" text-anchor="middle" font-family="{MONO}" font-size="8.6" letter-spacing=".7" fill="{t['inkFaint']}">{esc(sub)}</text>
  </g>
'''

    # ---- travelling packets on every edge
    for i, (d, length, dly) in enumerate(motions):
        dur = max(1.4, length / 95.0)
        for k in range(2):
            s += f'''  <circle r="3.2" fill="{t['amber']}" opacity="0" filter="url(#{p}-glow-s)">
    <animate attributeName="opacity" values="0;0;.95;.95;0" keyTimes="0;.02;.12;.82;1" dur="{fmt(dur)}s" begin="{dly + 1.1 + k * dur / 2:.2f}s" repeatCount="indefinite"/>
    <animateMotion dur="{fmt(dur)}s" begin="{dly + 1.1 + k * dur / 2:.2f}s" repeatCount="indefinite" path="{d}" rotate="auto"/>
  </circle>
'''

    # ---- legend
    leg = [("request path", t["accent"]), ("supporting service", t["line"]), ("data in flight", t["amber"])]
    lx = 44
    s += f'  <path class="fade" style="animation-delay:2.4s" d="M44 {fmt(452)}H916" stroke="{t["line"]}" stroke-width="1" stroke-opacity=".35"/>\n'
    for lab, col in leg:
        s += (f'  <g class="fade" style="animation-delay:2.55s">'
              f'<rect x="{fmt(lx)}" y="{fmt(474)}" width="18" height="3" rx="1.5" fill="{col}"/>'
              f'<text x="{fmt(lx + 26)}" y="{fmt(479)}" font-family="{MONO}" font-size="9.5" letter-spacing="1.3" '
              f'fill="{t["inkFaint"]}">{esc(lab.upper())}</text></g>\n')
        lx += len(lab) * 7.2 + 64
    s += (f'  <text class="fade" style="animation-delay:2.7s" x="916" y="479" text-anchor="end" font-family="{MONO}" '
          f'font-size="9.5" letter-spacing="1.3" fill="{t["inkFaint"]}">SCALE 1:1 · NOT TO DIMENSION</text>\n')
    s += "</svg>\n"
    return s


# ==========================================================================
# 6. DIVIDER
# ==========================================================================

def divider(t, p="d"):
    W, H = 900, 34
    cy = H / 2
    ticks = "".join(f"M{fmt(x)} {fmt(cy - 4)}v8" for x in range(60, W - 40, 60))
    s = svg_open(W, H, "section divider", "Blueprint drafting rule with a travelling highlight.")
    s += f'  <defs>\n{defs_common(t, p)}\n'
    s += f'''    <linearGradient id="{p}-gl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['accent']}" stop-opacity=".95"/>
      <stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="{p}-cp"><rect x="40" y="0" width="{W - 80}" height="{H}"/></clipPath>
  </defs>
'''
    s += f'''  <style>{BASE_CSS}
    .rule{{stroke-dasharray:{W};stroke-dashoffset:{W};animation:draw 1.4s ease-out forwards}}
    .gl{{--s:-160px;--e:{W}px;animation:sweep 4.6s linear infinite}}
  </style>
  <path class="rule" d="M40 {fmt(cy)}H{W - 40}" stroke="{t['line']}" stroke-width="1.2" stroke-opacity=".5" fill="none"/>
  <path class="fade" style="animation-delay:.8s" d="{ticks}" stroke="{t['line']}" stroke-width="1" stroke-opacity=".3"/>
  <g class="fade" style="animation-delay:1s">
    <path d="M{fmt(W / 2)} {fmt(cy - 7)}l7 7-7 7-7-7z" fill="none" stroke="{t['amber']}" stroke-width="1.2"/>
    <circle cx="{fmt(W / 2)}" cy="{fmt(cy)}" r="1.8" fill="{t['amber']}"/>
  </g>
  <g clip-path="url(#{p}-cp)"><rect class="gl" x="-160" y="{fmt(cy - 1)}" width="160" height="2" fill="url(#{p}-gl)"/></g>
</svg>
'''
    return s


# ==========================================================================
# 7. TITLE BLOCK FOOTER
# ==========================================================================

def footer(t, p="f"):
    W, H = 940, 150
    cells = [
        ("PROJECT", PROJECT, 132),
        ("DRAWN BY", AUTHOR, 178),
        ("SCALE", "1:1", 78),
        ("REV", "1.0", 68),
        ("SHEET", "06 / 06", 100),
    ]
    tw = sum(c[2] for c in cells)
    x0 = 900 - tw
    s = svg_open(W, H, "cs-funda title block",
                 "Engineering drawing title block listing project, author, scale, revision and sheet number.")
    s += f'  <defs>\n{defs_common(t, p)}\n  </defs>\n'
    s += f'''  <style>{BASE_CSS}
    .frm{{stroke-dasharray:1900;stroke-dashoffset:1900;animation:draw 2s ease-out forwards}}
    .sig{{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 2.2s ease-out .6s forwards}}
    .led{{animation:blink 2s ease-in-out infinite}}
  </style>
'''
    s += bg_layers(t, p, W, H)
    s += (f'  <rect class="frm" x="20" y="18" width="900" height="114" rx="2" fill="none" '
          f'stroke="{t["line"]}" stroke-width="1.3" stroke-opacity=".55"/>\n')

    # left: wordmark + hand-drawn signature flourish
    s += f'''  <g class="fade" style="animation-delay:.3s">
    <text x="48" y="58" font-family="{SANS}" font-size="22" font-weight="800" letter-spacing="5" fill="{t['ink']}">CS · FUNDA</text>
    <text x="48" y="78" font-family="{MONO}" font-size="9.8" letter-spacing="2.1" fill="{t['inkFaint']}">COMPUTER SCIENCE FUNDAMENTALS</text>
  </g>
  <path class="sig" d="M48 96c22-14 34 10 52 2s20-18 38-12 18 20 36 12 24-16 42-8" fill="none"
    stroke="{t['accent']}" stroke-width="1.5" stroke-opacity=".8" stroke-linecap="round"/>
  <path class="fade" style="animation-delay:1.6s" d="M48 108h228" stroke="{t['line']}" stroke-width="1" stroke-opacity=".45"/>
  <g class="fade" style="animation-delay:1.7s">
    <circle class="led" cx="52" cy="122" r="3.2" fill="{t['amber']}" filter="url(#{p}-glow-s)"/>
    <text x="64" y="126" font-family="{MONO}" font-size="8.6" letter-spacing="1.8" fill="{t['inkFaint']}">STUDY IN PROGRESS · BUILT WITH CURIOSITY</text>
  </g>
'''
    # right: title block grid
    x = x0
    for i, (lab, val, w) in enumerate(cells):
        d = 0.5 + i * 0.12
        s += f'''  <g class="fade" style="animation-delay:{d:.2f}s">
    <rect x="{fmt(x)}" y="42" width="{w}" height="66" fill="{t['bg2']}" fill-opacity="{.35 if t['glow'] else .5}" stroke="{t['line']}" stroke-width="1" stroke-opacity=".45"/>
    <text x="{fmt(x + 10)}" y="{fmt(62)}" font-family="{MONO}" font-size="8.4" letter-spacing="1.8" fill="{t['inkFaint']}">{esc(lab)}</text>
    <text x="{fmt(x + 10)}" y="{fmt(88)}" font-family="{MONO}" font-size="{12 if len(val) < 14 else 10.4}" font-weight="700" letter-spacing=".8" fill="{t['ink']}">{esc(val)}</text>
  </g>
'''
        x += w
    s += (f'  <text class="fade" style="animation-delay:1.4s" x="900" y="{fmt(126)}" text-anchor="end" font-family="{MONO}" '
          f'font-size="8.6" letter-spacing="1.8" fill="{t["inkFaint"]}">ALL ASSETS SELF-HOSTED · NO THIRD-PARTY SERVICES</text>\n')
    s += "</svg>\n"
    return s


# ==========================================================================

BUILDERS = {
    "banner": banner,
    "typing": typing,
    "stamps": stamps,
    "roadmap": roadmap,
    "architecture": architecture,
    "divider": divider,
    "footer": footer,
}


def main():
    ap = argparse.ArgumentParser(description="Generate cs-funda README assets")
    ap.add_argument("-o", "--out", default="assets", help="output directory (default: assets)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    made = []
    for name, fn in BUILDERS.items():
        for mode, theme in THEMES.items():
            path = os.path.join(args.out, f"{name}-{mode}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(fn(theme, p=f"{name[0]}{mode[0]}"))
            made.append(path)

    total = sum(os.path.getsize(m) for m in made)
    for m in sorted(made):
        print(f"  {os.path.getsize(m):>7,} B  {m}")
    print(f"\n{len(made)} files · {total / 1024:.1f} KB total")


if __name__ == "__main__":
    main()
