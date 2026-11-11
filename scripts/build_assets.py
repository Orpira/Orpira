#!/usr/bin/env python3
"""Genera los recursos gráficos del perfil (assets/*.svg).

El texto se convierte a trazados para que el banner se vea igual en cualquier
sistema: GitHub muestra los SVG como imagen y no carga tipografías externas.

Tipografías (licencia SIL OFL, las mismas del portfolio orpira.es):
    npm i @fontsource/instrument-serif @fontsource/geist-sans @fontsource/geist-mono
Uso:
    pip install fonttools pillow
    python3 scripts/build_assets.py --fonts <carpeta node_modules/@fontsource> \
        --cube <opr-cubo.png, el logotipo original con fondo transparente>

El cubo es el logotipo original de OrPiRa, incrustado en el SVG (GitHub no
carga imágenes externas dentro de un SVG).

Para cambiar un texto del banner, edita las constantes de abajo y vuelve a ejecutar.
"""
import argparse
import base64
import io
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image

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


def cube_data(path, px):
    """Logotipo original reducido y codificado para incrustarlo en el SVG."""
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    im.thumbnail((px, px), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=86, method=6)
    return im, "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def cube(href, ratio, cx, cy, h, shadow=True):
    """Cubo original centrado en (cx, cy), con halo y sombra para separarlo del fondo."""
    w = h * ratio
    floor = (f'<ellipse cx="{cx}" cy="{cy + h * 0.5:.0f}" rx="{h * 0.46:.0f}" ry="{h * 0.07:.0f}" fill="url(#shadow)"/>'
             if shadow else "")
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{h * 0.95:.0f}" ry="{h * 0.8:.0f}" fill="url(#halo)"/>{floor}'
            f'<image href="{href}" x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}"/>')


def wordmark(g, x, y, size, anchor="start"):
    w = [g.width("serif", NAME[0], size), g.width("serif-i", NAME[1], size), g.width("serif", NAME[2], size)]
    gap = size * 0.012
    if anchor == "middle":
        x -= (sum(w) + 2 * gap) / 2
    a, _ = g.text("serif", NAME[0], x, y, size, "url(#silver)")
    b, _ = g.text("serif-i", NAME[1], x + w[0] + gap, y, size, "url(#brandText)")
    c, _ = g.text("serif", NAME[2], x + w[0] + w[1] + 2 * gap, y, size, "url(#silver)")
    return a + b + c, sum(w) + 2 * gap


def banner(g, href, ratio):
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
    d.append(cube(href, ratio, 1030, 212, 300))
    t, _ = g.text("mono", PI_DIGITS, 1030, 404, 12.5, INK_MUTED, tracking=2.4, anchor="middle",
                  extra=' opacity=".7"')
    d.append(t)

    # Móvil ─ todo centrado y más grande; el cubo acompaña al nombre.
    ch = 190
    ww = wordmark(g, 0, 0, 200)[1]
    x0 = (W - (ch * ratio + 34 + ww)) / 2
    m = [cube(href, ratio, x0 + ch * ratio / 2, 128, ch, shadow=False)]
    wm, _ = wordmark(g, x0 + ch * ratio + 34, 196, 200)
    m.append(wm)
    t, _ = g.text("sans-m", TAGLINE, W / 2, 284, 60, INK_SOFT, anchor="middle")
    m.append(t)
    m.append(f'<rect x="{W / 2 - 60}" y="318" width="120" height="5" rx="2.5" fill="url(#brand)"/>')
    t, _ = g.text("mono", ROLES, W / 2, 384, 33, ROLE_COLOR, tracking=3.5, anchor="middle")
    m.append(t)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">OrPiRa · {TAGLINE}</title>
<desc id="d">{EYEBROW.title().replace(" · ", ", ")}. {ROLES.title()}. Logotipo: cubo con las caras Or, π y Ra.</desc>
<style>.m{{display:none}}@media (max-width:560px){{.d{{display:none}}.m{{display:inline}}}}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050916"/><stop offset=".55" stop-color="#0A1129"/><stop offset="1" stop-color="#100F33"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="brandText" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4FE3F7"/><stop offset=".55" stop-color="#6AA5FF"/><stop offset="1" stop-color="#A78BFA"/></linearGradient>
<linearGradient id="silver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#E8EDF7"/><stop offset="1" stop-color="#AEB9CF"/></linearGradient>
<radialGradient id="shadow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".7"/><stop offset=".6" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7FB2FF" stop-opacity=".42"/><stop offset=".45" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="carpeta node_modules/@fontsource")
    ap.add_argument("--cube", required=True, help="logotipo original (PNG con transparencia)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "assets"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    g = Glyphs(a.fonts)
    im, href = cube_data(a.cube, 420)
    ratio = im.width / im.height
    banner(g, href, ratio)  # primera pasada: registra los glifos que irán en <defs>
    svg = banner(g, href, ratio)
    with open(os.path.join(a.out, "banner.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("banner.svg", len(svg.encode()), "bytes")
    small = Image.open(a.cube).convert("RGBA")
    small = small.crop(small.getbbox())
    small.thumbnail((160, 160), Image.LANCZOS)
    small.save(os.path.join(a.out, "cubo-orpira.webp"), "WEBP", quality=90, method=6)


if __name__ == "__main__":
    main()
