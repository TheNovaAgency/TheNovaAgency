# NOVA brand kit

Production assets for **The Nova Agency** (brand name **NOVA**), Ignition identity v1.0.
Open `preview.png` for a contact sheet of everything below.

## What's in here

| Path | What it is |
|---|---|
| `logo/svg/nova-{horizontal,stacked,mark,wordmark}-{colourway}.svg` | Master logo files. Type is **outlined** (no font dependency). The artboard includes the clear space, so the file edge is the clear-space boundary. `dark` and `on-red` have a background rect; the rest are transparent. |
| `logo/svg/tight/…` | The same 20 files cropped tight to the artwork, never with a background. Use these in code and layout tools where you add spacing yourself. |
| `logo/svg/nova-mark-small-{16,24,48}-{colourway}.svg` | Heavier-stroke marks for small sizes. `48` = 32–48 px (stroke 7), `24` = 17–31 px (stroke 10), `16` = 16 px only (stroke 12, larger star). Tight 100×100 box. |
| `logo/svg/mark-small.svg` | Shorthand: 24 px-tier mark in Ignition on transparent. |
| `logo/png/…-{512,1024,2048}.png` | PNG renders of every lockup × colourway at 512, 1024 and 2048 px wide. Transparent where the SVG has no background. |
| `logo/png/nova-mark-small-light-56.png` | Tight light mark at 56 px, used by the email signature at 28 px (2×). |
| `icons/` | `favicon.svg` (adapts to dark mode), `favicon.ico` (16/32/48, each hand-tuned), `favicon-32.png`, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, `icon-512-maskable.png`, `site.webmanifest`. |
| `social/avatar-{dark,light}.png` | 400×400 profile images (also `-400` and `-1080` sizes). Mark at 50% width, safe for circular crops. |
| `tokens/tokens.css` | Theme variables. Dark is the default; OS light preference switches to light; `data-theme="light"`/`"dark"` on `<html>` forces either. Includes the verbatim `.nv-dark` / `.nv-light` classes plus type, space, radius and motion variables. |
| `tokens/tokens.json` | Same tokens in W3C design-token (DTCG) format: `color.core`, `color.dark`, `color.light`, `font.family`, `font.scale`, `space`, `radius`, `motion`. |
| `tokens/tailwind.preset.js` | Tailwind preset. Semantic colours (`bg-bg`, `text-text-2`, `bg-accent`…) read the CSS variables, so load `tokens.css` once. Fixed swatches live under `nova-*`; spacing steps are `nv-4`…`nv-96` so Tailwind's own scale is untouched. |
| `web/index.html` | Holding page for thenovaagency.com in the new identity. Self-contained: favicon set and manifest are copied alongside it, so deploy the whole `web/` folder to the site root. Needs a `POST /api/lead` endpoint accepting `{email, source}` JSON. |
| `email/signature.html` | Table-based email signature with `[Name]`, `[Role]`, `[Phone]`, `[Email]` placeholders. |
| `preview.png` | Contact sheet. |
| `_build/` | Scripts that regenerate everything (see bottom). |

## Which variant where

| Situation | Use |
|---|---|
| Website header, documents, decks | Horizontal. `dark` on dark surfaces, `light` on light ones. |
| Square or centred spaces: title slides, merch, signage, cover pages | Stacked. |
| App icons, favicons, avatars, watermarks, anywhere under 96 px wide | Mark alone. Under 48 px use the `mark-small` files. |
| When the mark already appears nearby (e.g. a page footer under a header lockup) | Wordmark. |
| On an Ignition red field | `on-red` (everything Ink). Never put Ignition on red. |
| One-colour print, embossing, foil, fax, partner logo walls | `mono-black` or `mono-white`. |
| Photography or busy backgrounds | `mono-white` on dark images, `mono-black` on light, only where contrast holds; otherwise put the logo on an Ink or Paper panel. |

## Colour

| Name | Hex | RGB | Use | Contrast on Ink / Paper |
|---|---|---|---|---|
| Ink | `#0A0607` | 10 6 7 | Dark background, text on light | n/a / 18.3:1 |
| Ignition | `#FF4B2B` | 255 75 43 | Mark and accent on dark; buttons; rules | 6.0:1 / 3.0:1 (graphics and large text only on light) |
| Ignition Deep | `#C42A0E` | 196 42 14 | Red **text** on light backgrounds | n/a / 5.2:1 |
| Bone | `#F4EDE8` | 244 237 232 | Text and wordmark on dark | 17.4:1 / n/a |
| Paper | `#F7F3F0` | 247 243 240 | Light background | 18.3:1 / n/a |
| Ember | `#FFB547` | 255 181 71 | Highlight and focus ring on dark | 11.5:1 / n/a |
| Ember Deep | `#8A5300` | 138 83 0 | Ember text on light | n/a / 5.7:1 |
| Star red (light logo only) | `#D92E10` | 217 46 16 | Star in the light colourway | n/a / 4.4:1 |

Colourways: **dark** Ignition frame and star, Bone wordmark, on Ink. **light** Ink frame, `#D92E10` star, Ink wordmark, Ignition Deep descriptor. **on-red** all Ink on Ignition. **mono-black** all Ink. **mono-white** all white.

## Clear space and minimum size

- **Clear space:** half the mark's height (x = ½ mark) on every side, including from the edge of a page, screen or crop. The master SVG/PNG artboards already include it.
- **Minimum size:** mark **16 px / 6 mm** tall; horizontal lockup **96 px / 25 mm** wide. Below 48 px use the `mark-small` files, which have heavier strokes.
- Lockup geometry, for rebuilding: horizontal mark height ≈ 1.35 × the wordmark's cap height, gap ≈ 0.4 × mark, cap height centred on the mark. Wordmark is Space Grotesk 700, tracking 0.16 em; descriptor is JetBrains Mono 400, tracking 0.34 em.

## Don'ts

- Don't recolour the logo outside the five colourways, or put Ignition on red.
- Don't stretch, squash, skew or rotate it; scale proportionally only.
- Don't add effects: shadows, glows, gradients, bevels, outlines, textures.
- Don't outline the wordmark or set NOVA in another typeface or tracking. Use the supplied files instead of retyping it.
- Don't rearrange the lockups or change the mark/wordmark proportions.
- Don't place it on low-contrast or busy backgrounds; use a mono version or an Ink/Paper panel.
- Don't crowd it inside its clear space or use it below minimum size.

## Web notes

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Fonts: Space Grotesk (400–700) and JetBrains Mono (400–500) from Google Fonts.

## Email signature

`email/signature.html` points its image at `../logo/png/nova-mark-small-light-56.png` so it previews locally. **Before use, host that PNG on a public HTTPS URL** (e.g. `https://thenovaagency.com/brand/nova-mark-small-light-56.png`) and change the `src`; mail clients can't load relative paths. Then copy the table between the `SIGNATURE START/END` comments into the mail client. Most mail clients don't load web fonts, so it falls back to Arial and Consolas by design.

## Regenerating

```bash
pip install fonttools brotli uharfbuzz pillow
# static instances from the google/fonts variable TTFs
python -m fontTools.varLib.instancer "SpaceGrotesk[wght].ttf" wght=700 -o fonts/SG700.ttf
python -m fontTools.varLib.instancer "JetBrainsMono[wght].ttf" wght=400 -o fonts/JBM400.ttf
python _build/build_logos.py fonts .           # SVGs (shaped with kerning, outlined)
python _build/build_tokens.py path/to/nova.css .
node _build/render.js .                        # PNGs, icons, avatars (Playwright)
python _build/make_ico.py .
```
