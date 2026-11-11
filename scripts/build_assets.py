#!/usr/bin/env python3
"""Genera los recursos gráficos del perfil (assets/*.svg).

El texto se convierte a trazados para que el banner se vea igual en cualquier
sistema: GitHub muestra los SVG como imagen y no carga tipografías externas.

Tipografías (licencia SIL OFL, las mismas del portfolio orpira.es):
    npm i @fontsource/geist-sans @fontsource/geist-mono
Uso:
    pip install fonttools pillow
    python3 scripts/build_assets.py --fonts <carpeta node_modules/@fontsource> \
        --cube <opr-cubo.png> --wordmark <OrPiRa-SF.png>

El cubo y la marca «OrπRa» son los logotipos originales (PNG con fondo
transparente), incrustados en el SVG porque GitHub no carga imágenes externas
dentro de un SVG.

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
TAGLINE = "Tecnología con visión de negocio"
ROLES = "FULL STACK · COORDINACIÓN IT · PRODUCTO DIGITAL"
PI_DIGITS = "3.14159 26535 89793 23846"

# ── Paleta ───────────────────────────────────────────────────────────────────
CYAN, BLUE, VIOLET = "#22D3EE", "#3B82F6", "#8B5CF6"
INK, INK_SOFT, INK_MUTED = "#F4F7FF", "#C3CEE8", "#8B9AC0"
ROLE_COLOR = "#8BE9F8"

FONT_FILES = {
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


def logo_data(path, px):
    """Logotipo original recortado, reducido y codificado para incrustarlo en el SVG."""
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox())
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
            f'<use href="#cubo" transform="translate({cx - w / 2:.1f} {cy - h / 2:.1f}) scale({h / 100:.4f})"/>')


def banner(g, cube_href, ratio, mark_href, mark_ratio):
    W, H = 1280, 440
    href = cube_href

    def brand(x, y, w):
        return f'<use href="#marca" transform="translate({x:.1f} {y:.1f}) scale({w / mark_ratio / 100:.4f})"/>'

    # Escritorio ─ marca y texto a la izquierda, cubo a la derecha.
    mw = 500
    top = 78
    d = [brand(66, top, mw)]
    t, _ = g.text("sans", TAGLINE, 84, top + mw / mark_ratio + 62, 33, INK_SOFT)
    d.append(t)
    y = top + mw / mark_ratio + 108
    d.append(f'<rect x="84" y="{y - 8:.0f}" width="56" height="3" rx="1.5" fill="url(#brand)"/>')
    t, _ = g.text("mono", ROLES, 158, y, 16.5, ROLE_COLOR, tracking=2.6)
    d.append(t)
    d.append(cube(href, ratio, 1030, 212, 300))
    t, _ = g.text("mono", PI_DIGITS, 1030, 404, 12.5, INK_MUTED, tracking=2.4, anchor="middle",
                  extra=' opacity=".7"')
    d.append(t)

    # Móvil ─ todo centrado y más grande; el cubo acompaña a la marca.
    ch, mw = 180, 600
    mh = mw / mark_ratio
    x0 = (W - (ch * ratio + 30 + mw)) / 2
    m = [cube(href, ratio, x0 + ch * ratio / 2, 22 + mh / 2, ch, shadow=False),
         brand(x0 + ch * ratio + 30, 22, mw)]
    t, _ = g.text("sans-m", TAGLINE, W / 2, 22 + mh + 72, 58, INK_SOFT, anchor="middle")
    m.append(t)
    t, _ = g.text("mono", ROLES, W / 2, 22 + mh + 142, 33, ROLE_COLOR, tracking=3.5, anchor="middle")
    m.append(t)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">OrπRa (OrPiRa), Orlando Pineda Raad · {TAGLINE}</title>
<desc id="d">{ROLES.title()}. Logotipos: marca OrπRa y cubo con las caras Or, π y Ra.</desc>
<style>.m{{display:none}}@media (max-width:560px){{.d{{display:none}}.m{{display:inline}}}}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050916"/><stop offset=".55" stop-color="#0A1129"/><stop offset="1" stop-color="#100F33"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<radialGradient id="shadow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".7"/><stop offset=".6" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7FB2FF" stop-opacity=".42"/><stop offset=".45" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowC" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowV" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".30"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#9DB4FF" fill-opacity=".11"/></pattern>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="dotMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<image id="cubo" href="{href}" width="{100 * ratio:.2f}" height="100"/>
<image id="marca" href="{mark_href}" width="{100 * mark_ratio:.2f}" height="100"/>
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
    ap.add_argument("--cube", required=True, help="cubo original (PNG con transparencia)")
    ap.add_argument("--wordmark", required=True, help="marca OrπRa original (PNG con transparencia)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "assets"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    g = Glyphs(a.fonts)
    im, href = logo_data(a.cube, 420)
    mk, mark_href = logo_data(a.wordmark, 760)
    args = (g, href, im.width / im.height, mark_href, mk.width / mk.height)
    banner(*args)  # primera pasada: registra los glifos que irán en <defs>
    svg = banner(*args)
    with open(os.path.join(a.out, "banner.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("banner.svg", len(svg.encode()), "bytes")
    small = Image.open(a.cube).convert("RGBA")
    small = small.crop(small.getbbox())
    small.thumbnail((160, 160), Image.LANCZOS)
    small.save(os.path.join(a.out, "cubo-orpira.webp"), "WEBP", quality=90, method=6)


if __name__ == "__main__":
    main()
