# Freigeist – design notes (variant C, "fine cut")

Status: **accepted draft**. The design may still change before the blog goes live.

## Concept

Copper engraving meets HUD/glitch. Fine engraved lines, a serif title and a delicate blossom are cut through by harsh, misaligned accent bars, a crosshair readout and 1-bit pixel areas. The page should feel like an old plate that is being scanned. The quiet half carries the reading; the loud half carries the signal.

## Blossom mark

- The blossom is split along a **diagonal**. The upper-left half is drawn as a fine engraving, and the lower-right half is pixelated, 1-bit and uncoloured (ink only).
- **Bud:** cross-hatched on the engraved side (no stipple dots). On the pixel side it is an **even pattern**: an X every 4 px on desktop and a checkerboard on mobile, so that it follows the bud contour.
- An accent-coloured cut line runs along the diagonal.
- Files: `assets/freigeist-mark.svg` (on paper) and `assets/freigeist-mark-transparent.svg`. The theme uses the mark as an SVG `<symbol id="fg-mark">` with its cut line set to `var(--accent)`.
- Small-size check: at 28–44 px (header, list kicker, footer, favicon) the diagonal split and the cut line still read clearly. The pixel half turns into a texture, which is intended. Don't use the mark below 24 px.

## Colour

Base palette:

| Role | Hex |
|---|---|
| Paper | `#f8f3ea` |
| Ink | `#2b2724` |
| Body ink | `#3a332e` |
| Muted / meta | `#6b625a`, `#8a8079` |
| HUD black | `#111111` |

### Accent pairs

Each page load picks one pair at random. Force a pair with `?accent=<name>`, for example `index.html?accent=cobalt`. The picker sets three CSS variables on `<html>`, plus `data-accent="<name>"`:

- `--accent`: bars, stabs, the cut line and the header underline
- `--hud`: crosshair readouts, the HUD text and the glitch RGB split
- `--acc-text`: accent text on black (only differs where the accent is too dark on `#111`)

| name | `--accent` | `--hud` | `--acc-text` |
|---|---|---|---|
| acid-green | `#C0FE04` | `#ff3d7f` | `#C0FE04` |
| signal-orange | `#ff5a1f` | `#2f3cff` | `#ff5a1f` |
| hot-magenta | `#ff2e88` | `#0fa3b1` | `#ff2e88` |
| cobalt | `#2f3cff` | `#ff5a1f` | `#9aa3ff` |
| warning-red | `#e8231b` | `#1f3fbf` | `#e8231b` |
| safety-yellow | `#ffd400` | `#e8231b` | `#ffd400` |

Accents are never used for running text on paper. Use them only for shapes, and for text on `#111`.

## Typography

- **Cormorant Garamond** (300–700, plus italic) for the title, headlines (italic), body and teasers
- **IBM Plex Mono** (400/600/700) for meta lines, HUD readouts, nav buttons and the kicker/footer, in uppercase with letter-spacing of .12–.14em
- **Unbounded** (900, outline only) for the large "FG/06" plate number

All three fonts are under the SIL Open Font License. They ship in `theme/fonts/` so the site works offline.

## Background

Continuous **wavy engraving lines** run down the whole page. They are a pre-rendered SVG tile, `theme/waves-desktop.svg` (mobile: `waves-mobile.svg`), repeated vertically so there is no hard break between the hero and the content. Teasers and post text sit on semi-transparent paper (`rgba(248,243,234,.88–.92)`) so the waves show through.

## Header

- **Hero:** a full-viewport SVG plate (`theme/hero-desktop.svg`, `theme/hero-mobile.svg`) with the title, the blossom, the HUD crosshair, the right sidebar and the two newest posts as cards.
- **Shrinking sticky header:** on scroll, the title scales smoothly into a compact bar, about 78 px tall. The bar contains:
  - fine dense waves (`waves-bar.svg`)
  - a dashed rule with a tick scale on the bottom edge
  - the mini blossom mark
  - a HUD readout `FG-06 · 52.52N 13.40E · NNN%` showing the live scroll position (the coordinates are placeholder text and can be changed)
  - navigation
- **Navigation:** Posts / Notes / Projects / About.
  - Desktop: small mono uppercase buttons with a thin ink frame, inverted to black with accent text on hover.
  - Mobile: a black menu button with three accent lines that opens a vertical list.
- There is no skewed accent bar in the compact header. It was removed on purpose.

## Motion

- **Glitch bursts** every 1.8–4.8 s, hitting only the harsh elements: accent bars (`.g-bar`), pixel areas (`.g-pix`), the HUD beam (`.g-beam`), the title RGB split (`.g-title`) and an occasional scanline tear. The engraved parts never glitch.
- With `prefers-reduced-motion: reduce`, there are no glitch bursts and the header switches between its two states without interpolation.

## Checks

- Small sizes: the mark is checked at 28/34/44 px.
- Mobile: checked at 390 px.
- Dark mode: **not designed yet.** The plate concept relies on paper. If needed, an "inked plate" variant (paper `#1a1816`, lines `#e9e1d3`, same accents) is the suggested direction. That is still open.
- Contrast: body ink `#3a332e` on paper passes WCAG AA. The muted meta colour `#8a8079` is only used for small uppercase meta lines.

## Assets

| Path | What |
|---|---|
| `assets/freigeist-mark.svg` / `-transparent.svg` | Logo mark (88×88) |
| `assets/design-reference-*.png` | Reference mockups (desktop, mobile, accent overview) |
| `theme/base.html` | Page shell: CSS, accent picker, shrinking header, glitch script |
| `theme/hero-desktop.svg`, `theme/hero-mobile.svg` | Hero plates; `{{CARDS}}` is filled by `build.py` |
| `theme/content.css` | Post page and listing additions |
| `theme/waves-*.svg` | Background tiles |
| `theme/fonts/` | Font files (OFL) |
| `tools/make_theme.py` | Regenerates the theme from the design source files (designer use only) |
