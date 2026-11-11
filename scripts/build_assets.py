#!/usr/bin/env python3
"""Genera los recursos gráficos del perfil (assets/*.svg).

El texto se convierte a trazados para que el banner se vea igual en cualquier
sistema: GitHub muestra los SVG como imagen y no carga tipografías externas.

Tipografías (licencia SIL OFL, las mismas del portfolio orpira.es):
    npm i @fontsource/instrument-serif @fontsource/geist-sans @fontsource/geist-mono
Uso:
    pip install fonttools
    python3 scripts/build_assets.py --fonts <carpeta node_modules/@fontsource>

Para cambiar un texto del banner, edita las constantes de abajo y vuelve a ejecutar.
"""
import argparse
import math
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

# ── Contenido ────────────────────────────────────────────────────────────────
NAME = ("Or", "Pi", "Ra")
TAGLINE = "Tecnología con visión de negocio"
ROLES = "FULL STACK · COORDINACIÓN IT · PRODUCTO DIGITAL"
EYEBROW = "ORLANDO PINEDA RAAD · BILBAO"
PI_DIGITS = "3.14159 26535 89793 23846"

# ── Paleta ───────────────────────────────────────────────────────────────────
CYAN, BLUE, VIOLET = "#22D3EE", "#3B82F6", "#8B5CF6"
INK, INK_SOFT, INK_MUTED = "#F4F7FF", "#C3CEE8", "#8B9AC0"
ROLE_COLOR = "#8BE9F8"

FONT_FILES = {
    "serif": "instrument-serif/files/instrument-serif-latin-400-normal.woff",
    "serif-i": "instrument-serif/files/instrument-serif-latin-400-italic.woff",
    "sans": "geist-sans/files/geist-sans-latin-400-normal.woff",
    "sans-m": "geist-sans/files/geist-sans-latin-500-normal.woff",
    "mono": "geist-mono/files/geist-mono-latin-500-normal.woff",
}

# π propio de la marca: trazo geométrico con remates redondeados (caja 100×100).
PI_PATHS = (
    "M14 35C18 26 25 24 34 24H88",
    "M39 24C39 50 35 68 24 80",
    "M66 24V64C66 76 73 81 83 76",
)


class Glyphs:
    """Convierte texto en <use> de glifos definidos una sola vez en <defs>."""

    def __init__(self, font_dir):
        self.fonts = {k: TTFont(os.path.join(font_dir, v)) for k, v in FONT_FILES.items()}
        self.defs = {}

    def _glyph(self, key, ch):
        font = self.fonts[key]
        name = font.getBestCmap()[ord(ch)]
        gid = f"{key}-{ord(ch):x}"
        if gid not in self.defs:
            pen = SVGPathPen(font.getGlyphSet(), ntos=lambda v: str(round(v)))
            font.getGlyphSet()[name].draw(pen)
            self.defs[gid] = pen.getCommands()
        return gid, font["hmtx"][name][0]

    def width(self, key, text, size, tracking=0.0):
        upm = self.fonts[key]["head"].unitsPerEm
        return sum(self._glyph(key, c)[1] * size / upm + tracking for c in text) - tracking

    def text(self, key, text, x, y, size, fill, tracking=0.0, anchor="start", extra=""):
        upm = self.fonts[key]["head"].unitsPerEm
        k = size / upm
        if anchor == "middle":
            x -= self.width(key, text, size, tracking) / 2
        out, cx = [], 0.0
        for ch in text:
            gid, adv = self._glyph(key, ch)
            if ch != " ":
                out.append(f'<use href="#{gid}" x="{cx / k:.0f}"/>')
            cx += adv * k + tracking
        body = "".join(out)
        return (f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})" '
                f'fill="{fill}"{extra}>{body}</g>'), cx - tracking

    def defs_svg(self):
        return "".join(f'<path id="{g}" d="{d}"/>' for g, d in self.defs.items() if d)


def pi_mark(x, y, size, stroke="url(#brand)", width=9.0, extra=""):
    k = size / 100
    paths = "".join(f'<path d="{d}"/>' for d in PI_PATHS)
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{extra}>{paths}</g>')


def cube(g, cx, cy, s):
    """Cubo isométrico de la marca: «Or» arriba, π al frente y «Ra» a la derecha."""
    h, w = s / 2, s * math.cos(math.radians(30))
    T, C, B = (cx, cy - s), (cx, cy), (cx, cy + s)
    L, R = (cx - w, cy - h), (cx + w, cy - h)
    BL, BR = (cx - w, cy + h), (cx + w, cy + h)
    pts = lambda *p: " ".join(f"{a:.1f},{b:.1f}" for a, b in p)
    c30, s30 = math.cos(math.radians(30)), 0.5
    o = [
        f'<polygon points="{pts(T, R, C, L)}" fill="url(#faceTop)"/>',
        f'<polygon points="{pts(L, C, B, BL)}" fill="url(#faceLeft)"/>',
        f'<polygon points="{pts(C, R, BR, B)}" fill="url(#faceRight)"/>',
        f'<g fill="none" stroke="url(#brand)" stroke-width="2.5" stroke-linejoin="round">'
        f'<polygon points="{pts(T, R, BR, B, BL, L)}"/>'
        f'<polyline points="{pts(L, C, R)}"/><line x1="{C[0]}" y1="{C[1]}" x2="{B[0]}" y2="{B[1]}"/></g>',
    ]
    # π en la cara frontal izquierda (plano inclinado 30°).
    m = f"matrix({c30:.4f} {s30} 0 1 {L[0]:.1f} {L[1]:.1f})"
    o.append(f'<g transform="{m}">{pi_mark(s * 0.16, s * 0.14, s * 0.72, width=10)}</g>')
    # «Ra» en la cara derecha.
    m = f"matrix({c30:.4f} {-s30} 0 1 {C[0]:.1f} {C[1]:.1f})"
    t, _ = g.text("serif-i", "Ra", s * 0.5, s * 0.68, s * 0.5, INK, anchor="middle", extra=' opacity=".55"')
    o.append(f'<g transform="{m}">{t}</g>')
    # «Or» en la cara superior.
    m = f"matrix({c30:.4f} {-s30} {c30:.4f} {s30} {L[0]:.1f} {L[1]:.1f})"
    t, _ = g.text("serif-i", "Or", s * 0.5, s * 0.68, s * 0.5, INK, anchor="middle", extra=' opacity=".55"')
    o.append(f'<g transform="{m}">{t}</g>')
    for x, y in (T, L, R, C, BL, BR, B):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#0A1028" stroke="{CYAN}" stroke-width="2"/>')
    return "".join(o)


def wordmark(g, x, y, size, anchor="start"):
    w = [g.width("serif", NAME[0], size), g.width("serif-i", NAME[1], size), g.width("serif", NAME[2], size)]
    gap = size * 0.012
    if anchor == "middle":
        x -= (sum(w) + 2 * gap) / 2
    a, _ = g.text("serif", NAME[0], x, y, size, INK)
    b, _ = g.text("serif-i", NAME[1], x + w[0] + gap, y, size, "url(#brandText)")
    c, _ = g.text("serif", NAME[2], x + w[0] + w[1] + 2 * gap, y, size, INK)
    return a + b + c, sum(w) + 2 * gap


def banner(g):
    W, H = 1280, 440
    # Escritorio ─ texto a la izquierda, cubo a la derecha.
    d = []
    t, _ = g.text("mono", EYEBROW, 84, 112, 15, INK_MUTED, tracking=3.2)
    d.append(t)
    wm, _ = wordmark(g, 78, 248, 156)
    d.append(wm)
    t, _ = g.text("sans", TAGLINE, 84, 308, 33, INK_SOFT)
    d.append(t)
    d.append(f'<rect x="84" y="346" width="56" height="3" rx="1.5" fill="url(#brand)"/>')
    t, _ = g.text("mono", ROLES, 158, 354, 16.5, ROLE_COLOR, tracking=2.6)
    d.append(t)
    d.append(cube(g, 1040, 222, 132))
    t, _ = g.text("mono", PI_DIGITS, 1040, 404, 12.5, INK_MUTED, tracking=2.4, anchor="middle",
                  extra=' opacity=".7"')
    d.append(t)

    # Móvil ─ todo centrado y más grande; el π queda como marca de agua.
    m = [pi_mark(930, 30, 380, width=5, extra=' opacity=".13"')]
    wm, _ = wordmark(g, W / 2, 196, 200, anchor="middle")
    m.append(wm)
    t, _ = g.text("sans-m", TAGLINE, W / 2, 284, 60, INK_SOFT, anchor="middle")
    m.append(t)
    m.append(f'<rect x="{W / 2 - 60}" y="318" width="120" height="5" rx="2.5" fill="url(#brand)"/>')
    t, _ = g.text("mono", ROLES, W / 2, 384, 33, ROLE_COLOR, tracking=3.5, anchor="middle")
    m.append(t)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">OrPiRa · {TAGLINE}</title>
<desc id="d">{EYEBROW.title().replace(" · ", ", ")}. {ROLES.title()}. Marca con el símbolo π sobre un cubo.</desc>
<style>.m{{display:none}}@media (max-width:560px){{.d{{display:none}}.m{{display:inline}}}}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050916"/><stop offset=".55" stop-color="#0A1129"/><stop offset="1" stop-color="#100F33"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="brandText" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4FE3F7"/><stop offset=".55" stop-color="#6AA5FF"/><stop offset="1" stop-color="#A78BFA"/></linearGradient>
<linearGradient id="faceTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".20"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".10"/></linearGradient>
<linearGradient id="faceLeft" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="#0A1129" stop-opacity=".5"/></linearGradient>
<linearGradient id="faceRight" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".06"/></linearGradient>
<radialGradient id="glowC" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowV" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".30"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#9DB4FF" fill-opacity=".11"/></pattern>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="dotMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="28"/></clipPath>
{g.defs_svg()}
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<ellipse cx="1040" cy="200" rx="420" ry="330" fill="url(#glowC)"/>
<ellipse cx="1210" cy="430" rx="460" ry="330" fill="url(#glowV)"/>
<ellipse cx="120" cy="-20" rx="520" ry="300" fill="url(#glowB)"/>
<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dotMask)"/>
<g class="d">{"".join(d)}</g>
<g class="m">{"".join(m)}</g>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="27.25" fill="none" stroke="#7C9BFF" stroke-opacity=".28" stroke-width="1.5"/>
</svg>
'''


def mark():
    """Sello π para el pie del README."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" role="img" aria-label="π, símbolo de OrPiRa">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050916"/><stop offset="1" stop-color="#100F33"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>
<rect width="96" height="96" rx="22" fill="url(#bg)"/>
<rect x=".75" y=".75" width="94.5" height="94.5" rx="21.25" fill="none" stroke="#7C9BFF" stroke-opacity=".3" stroke-width="1.5"/>
{pi_mark(15, 13, 66, width=10)}
</svg>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="carpeta node_modules/@fontsource")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "assets"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    g = Glyphs(a.fonts)
    banner(g)  # primera pasada: registra los glifos que irán en <defs>
    for name, svg in (("banner.svg", banner(g)), ("pi-mark.svg", mark())):
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(name, len(svg.encode()), "bytes")


if __name__ == "__main__":
    main()
