#!/usr/bin/env python3
"""Generate the NOVA logo SVGs with outlined type.

Needs: pip install fonttools brotli uharfbuzz
Fonts: static instances of Space Grotesk Bold (700) and JetBrains Mono Regular (400),
made from the google/fonts variable TTFs with:
  python -m fontTools.varLib.instancer SpaceGrotesk[wght].ttf wght=700 -o SG700.ttf
  python -m fontTools.varLib.instancer JetBrainsMono[wght].ttf wght=400 -o JBM400.ttf
Usage: python build_logos.py <fonts_dir> <brand-kit dir>
"""
import os, sys, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FONTS, OUT = sys.argv[1], sys.argv[2]
SVG_DIR = os.path.join(OUT, "logo", "svg")
TIGHT_DIR = os.path.join(SVG_DIR, "tight")
os.makedirs(TIGHT_DIR, exist_ok=True)

FRAME = "M50 4 L96 50 L50 96 L4 50 Z"
STAR = "M50 22 C52.5 40 60 47.5 78 50 C60 52.5 52.5 60 50 78 C47.5 60 40 52.5 22 50 C40 47.5 47.5 40 50 22 Z"
STAR16 = "M50 20 C52.5 40 60 47.5 80 50 C60 52.5 52.5 60 50 80 C47.5 60 40 52.5 20 50 C40 47.5 47.5 40 50 20 Z"

INK, IGN, IGN_DEEP, BONE, STAR_LIGHT = "#0A0607", "#FF4B2B", "#C42A0E", "#F4EDE8", "#D92E10"
CW = {
    # name: frame, star, word, descriptor, background (None = transparent)
    "dark":       dict(frame=IGN, star=IGN, word=BONE, desc=IGN, bg=INK),
    "light":      dict(frame=INK, star=STAR_LIGHT, word=INK, desc=IGN_DEEP, bg=None),
    "on-red":     dict(frame=INK, star=INK, word=INK, desc=INK, bg=IGN),
    "mono-black": dict(frame=INK, star=INK, word=INK, desc=INK, bg=None),
    "mono-white": dict(frame="#FFFFFF", star="#FFFFFF", word="#FFFFFF", desc="#FFFFFF", bg=None),
}


class Face:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        self.cap = self.tt["OS/2"].sCapHeight
        self.order = self.tt.getGlyphOrder()
        self.hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(path)))

    def run(self, text, size, tracking_em):
        """Shape text (with kerning), apply tracking between glyphs (not after the last).
        Returns (svg path d, ink bounds) with baseline at y=0, pen start at x=0, y down."""
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": False})
        s = size / self.upem
        track = tracking_em * size
        x = 0.0
        pen = SVGPathPen(self.gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        bp = BoundsPen(self.gs)
        n = len(buf.glyph_infos)
        for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            name = self.order[info.codepoint]
            t = (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s)
            self.gs[name].draw(TransformPen(pen, t))
            self.gs[name].draw(TransformPen(bp, t))
            x += pos.x_advance * s
            if i < n - 1:
                x += track
        return pen.getCommands(), bp.bounds  # bounds: xmin, ymin, xmax, ymax (y down)


SG = Face(os.path.join(FONTS, "SG700.ttf"))
JB = Face(os.path.join(FONTS, "JBM400.ttf"))

F = 100.0                       # wordmark font size in user units
CAP = SG.cap / SG.upem * F      # 70
WORD_D, WORD_B = SG.run("NOVA", F, 0.16)
DESC_SIZE = F * 11 / 44         # stacked descriptor: 11px label against 44px wordmark (brand guide)
DESC_D, DESC_B = JB.run("THE NOVA AGENCY", DESC_SIZE, 0.34)


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def mark_group(x, y, size, c, sw=4.5, star=STAR):
    k = size / 100.0
    return (f'<g transform="translate({f(x)} {f(y)}) scale({("%.5f" % k).rstrip("0").rstrip(".")})">'
            f'<path d="{FRAME}" fill="none" stroke="{c["frame"]}" stroke-width="{sw}" stroke-linejoin="miter" stroke-miterlimit="10"/>'
            f'<path d="{star}" fill="{c["star"]}"/></g>')


def text_group(d, dx, dy, fill):
    return f'<path transform="translate({f(dx)} {f(dy)})" d="{d}" fill="{fill}"/>'


def svg_doc(w, h, body, c, title, bg=True):
    rect = f'<rect width="{f(w)}" height="{f(h)}" fill="{c["bg"]}"/>' if (bg and c["bg"]) else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" width="{f(w)}" height="{f(h)}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{rect}{body}</svg>\n')


def layouts(c):
    """Each layout returns (content_w, content_h, body, clear) with content at origin."""
    out = {}
    # Mark alone: 100 x 100 box, clear space = half mark height.
    M = 100.0
    out["mark"] = (M, M, mark_group(0, 0, M, c), M / 2)

    # Wordmark alone: ink box of NOVA; clear space = half of the mark height it would have in a lockup.
    x0, y0, x1, y1 = WORD_B
    ww, wh = x1 - x0, y1 - y0
    out["wordmark"] = (ww, wh, text_group(WORD_D, -x0, -y0, c["word"]), 1.35 * CAP / 2)

    # Horizontal: mark = 1.35 x cap height, gap = 0.4 x mark, cap centred on mark.
    Mh = 1.35 * CAP
    gap = 0.4 * Mh
    base = Mh / 2 + CAP / 2           # baseline so cap height is centred on mark
    body = mark_group(0, 0, Mh, c) + text_group(WORD_D, Mh + gap - x0, base, c["word"])
    out["horizontal"] = (Mh + gap + ww, Mh, body, Mh / 2)

    # Stacked: mark above NOVA above descriptor, centred (proportions from the brand guide:
    # 84px mark / 44px wordmark / 11px descriptor, 18px gaps).
    Ms = F * 84 / 44
    dx0, dy0, dx1, dy1 = DESC_B
    dw = dx1 - dx0
    W = max(Ms, ww, dw)
    g1 = F * 18 / 44 + 0.146 * F       # mark bottom -> cap top (gap + half-leading above caps)
    word_base = Ms + g1 + CAP
    desc_cap_top = word_base + 0.154 * F + F * 18 / 44 + 0.29 * DESC_SIZE
    desc_base = desc_cap_top + JB.cap / JB.upem * DESC_SIZE
    body = (mark_group((W - Ms) / 2, 0, Ms, c)
            + text_group(WORD_D, (W - ww) / 2 - x0, word_base, c["word"])
            + text_group(DESC_D, (W - dw) / 2 - dx0, desc_base, c["desc"]))
    out["stacked"] = (W, desc_base, body, Ms / 2)
    return out


manifest = []
for cw, c in CW.items():
    for kind, (w, h, body, clear) in layouts(c).items():
        title = {"mark": "Nova mark", "wordmark": "NOVA", "horizontal": "The Nova Agency",
                 "stacked": "The Nova Agency"}[kind]
        # Padded master: artboard edge = clear-space boundary.
        W, H = w + 2 * clear, h + 2 * clear
        padded = f'<g transform="translate({f(clear)} {f(clear)})">{body}</g>'
        name = f"nova-{kind}-{cw}.svg"
        open(os.path.join(SVG_DIR, name), "w").write(svg_doc(W, H, padded, c, title))
        # Tight crop, never a background (for code/layout use).
        open(os.path.join(TIGHT_DIR, name), "w").write(svg_doc(w, h, body, c, title, bg=False))
        manifest.append(dict(file=name, kind=kind, colourway=cw, w=round(W, 2), h=round(H, 2),
                             bg=c["bg"] is not None))

# Small-size marks: tight 0 0 100 100 box, full-bleed background for dark / on-red.
for tier, sw, star in (("48", 7, STAR), ("24", 10, STAR), ("16", 12, STAR16)):
    for cw, c in CW.items():
        body = mark_group(0, 0, 100, c, sw=sw, star=star)
        name = f"nova-mark-small-{tier}-{cw}.svg"
        open(os.path.join(SVG_DIR, name), "w").write(svg_doc(100, 100, body, c, "Nova mark"))

# Plain alias requested in the brief: 24px-tier Ignition mark on transparent.
c = dict(CW["dark"]); c["bg"] = None
open(os.path.join(SVG_DIR, "mark-small.svg"), "w").write(
    svg_doc(100, 100, mark_group(0, 0, 100, c, sw=10), c, "Nova mark", bg=False))

json.dump(dict(manifest=manifest, word=dict(d=WORD_D, bounds=WORD_B), desc=dict(d=DESC_D, bounds=DESC_B, size=DESC_SIZE),
               cap=CAP), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-manifest.json"), "w"))
print("ok", len(manifest), "lockups; word bounds", WORD_B, "desc bounds", DESC_B)
