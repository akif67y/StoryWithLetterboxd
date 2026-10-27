# Design spec — approved v1 cards

All values are in px on a 1080×1920 canvas. Akif reviewed and approved these renders
(`design-reference/my-renders/`). `prototype_build.py` has the full working CSS.

## Global

- Fonts: **Inter** (UI/sans) and **Lora** (serif titles/numbers). They're close
  substitutes for the reference app's fonts. Load them from Google Fonts.
- Letterboxd green for stars: `#00e054`
- Grain overlay: SVG `feTurbulence` fractalNoise, baseFrequency 0.9, numOctaves 2,
  desaturated, `opacity:.10; mix-blend-mode:overlay`, full canvas.
- Background image: `background-size:cover`, with the position adjustable per card.

## 1. Last Watched

- Background: poster, `background-size:auto 1920px; background-position:50% 0`.
- Shade layer:
  - `linear-gradient(180deg, rgba(0,0,0,.35) 0%, transparent 14%, transparent 46%, rgba(0,0,0,.55) 62%, rgba(0,0,0,.92) 80%, #000 92%)`
  - plus a vignette `radial-gradient(120% 70% at 50% 40%, transparent 55%, rgba(0,0,0,.45) 100%)`
- Info block: `left:75px; right:75px; top:1258px` (with rating) or `top:1348px` (username-only variant).
  - Kicker "LAST WATCHED": Inter 500, 34px, letter-spacing 1.6px, `#a9b9c8`
  - Title: Lora 700, 112px, line-height 1.1, margin-top 22px, letter-spacing -0.5px, white
  - Stars: 58px each, gap 4px, margin-top 22px, half-star supported
  - Meta: Inter 400, 39px, `#b4bcc5`, margin-top 30px (24px in the username-only variant);
    format `23 Oct · by <b>meakif</b>`, with the username in white 600 and the dot in `#8a929c` with 8px margin
- Toggles: Rating, Date, Username (each can be on or off independently).

## Shared profile card (styles 2 & 3)

- Card: `left:172px; width:736px; background:#435666; border-radius:54px;
  border:1.5px solid rgba(255,255,255,.07);
  box-shadow:0 18px 50px rgba(0,0,0,.28), 0 2px 8px rgba(0,0,0,.18)`
- Avatar: 212px circle, centred, overlapping the card's top edge by half (top -106px),
  `box-shadow:0 10px 30px rgba(0,0,0,.35)`
- Username: Inter 700, 62px, white, centred, margin-top 132px, letter-spacing -0.5px
- Divider: 2px `#5f6d7f`, margin 44px 23px 0

## 2. Profile Stats

- Card height 432px. Default top is 1010px. **The user should be able to drag it**
  so it doesn't cover faces in the background.
- Two columns (FILMS / THIS YEAR), each 50% wide, padding 0 40px, margin-top 34px
  - Number: Lora 700, 64px, white
  - Label: Inter 400, 28px, letter-spacing 1px, white, margin-top 22px

## 3. Profile Favourites

- Card height 606px. Default top is 1120px. Draggable. One approved variant has the card
  shifted left (`left:44px; top:1115px`) to cover part of the background.
- Label "FAVOURITE FILMS": Inter 30px, `#a7b9ca`, letter-spacing .8px, margin-top 40px, centred
- Poster row: 4 posters in a flex row, gap 13px, padding 0 22px, margin-top 30px,
  aspect 2:3, radius 13px,
  `box-shadow: inset 0 0 0 1px rgba(255,255,255,.12), 0 4px 10px rgba(0,0,0,.25)`

## Lessons from iterating with Akif

- Placement matters more than anything: a card covering a character's face ruined
  the design. Give the user a drag handle for the card's Y-position (and X-position for the
  shifted variant) and a background pan control. Don't try to auto-place.
- Low-resolution stills (e.g. 625px tall) look soft at 1920px. Prefer the largest
  TMDB size (`original`), and warn when the upscale is more than about 2×.
- Akif likes a minimal variant (just "by meakif") as much as the full one.
