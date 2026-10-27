# Stories For Movies — project brief

**Stories For Movies** is a free, open-source, non-commercial web app that turns a Letterboxd user's films,
reviews and profile into styled 1080×1920 Instagram Story images. It's a free
alternative to the paid "Stories for Letterboxd" app, with no watermark.

Owner: Akif (CS undergrad, Letterboxd user `meakif`). This brief came out of a
design and research chat. The decisions below are settled unless Akif says otherwise.
The decision log at the bottom of `docs/DECISIONS_AND_AI_WORKFLOW.md` records
everything else that's been decided (framework, styling, state, hosting, name).

Working style: Claude writes most of the code. Akif does some phase items, so
check `docs/BUILD_PHASES.md` and ask before taking over an item marked for Akif.
Export is tested on Android (Chrome) and desktop only, since no iOS device is available.

## Core decisions

1. **No AI at runtime.** Styles are hand-written templates (HTML/CSS/JSX)
   filled with data. Nothing in the app calls Claude or any paid API.
2. **No scraping of letterboxd.com pages.** Letterboxd blocks bots, and scraping is
   fragile and against the spirit of their terms. Use only the sources in
   `docs/DATA_SOURCES.md`.
3. **The official Letterboxd API is not available.** Access is request-only, and
   private, personal and data-viz projects are currently not approved. Design a
   `DataSource` interface so the API could be swapped in later if access is granted.
4. **Images come from TMDB.** It's free for non-commercial use with attribution: the
   TMDB logo plus "This product uses the TMDB API but is not endorsed or certified
   by TMDB." in an About/Credits section. Keep the TMDB key server-side.
5. **Don't look official.** Don't use Letterboxd's logo, and don't pixel-clone the
   paid app's designs. Use them as inspiration.
6. **Render client-side first.** Build the card as a fixed 1080×1920 DOM node and
   export it with `modern-screenshot`. `satori` on a serverless
   function is the fallback if output is inconsistent across phones. Share with the
   Web Share API on mobile and fall back to download.

## Data plan (summary — details in docs/DATA_SOURCES.md)

| Need | Source |
|---|---|
| Last watched / recent diary / reviews / rating / date | Public RSS: `https://letterboxd.com/<username>/rss/` (fetched via our backend because of CORS) |
| Posters, backdrop stills | TMDB API (via backend proxy) |
| Film count, this-year count, ratings histogram, favourites | User uploads their Letterboxd **data export ZIP**, parsed in the browser (JSZip + PapaParse), never uploaded |
| Avatar, followers, anything missing | Manual input / upload, saved in localStorage |

## Architecture

- Frontend: React + Vite + TypeScript. CSS Modules for styling, `useReducer` + Context for state.
- Backend: tiny serverless functions on Vercel. The TMDB key lives in `.env` as
  `TMDB_API_KEY` (no `VITE_` prefix, because Vite bundles `VITE_*` vars into client code). There are only two:
  `GET /api/rss?user=` (fetch and parse RSS) and `GET /api/tmdb/*` (key-hiding proxy).
  Also proxy images so canvas export isn't blocked by CORS.
- `src/styles/<StyleName>.tsx`: one file per style. Each exports
  `{ id, name, supports: ('film'|'review'|'profile')[], options schema, Component }`.
- Shared primitives: `<Stars value>` (supports half stars), `<Grain/>`,
  `<ProfileCard>`, `<PosterRow>`, `<FitText>`.
- Editor UI: style picker, toggles (Rating / Date / Username …), background picker
  (poster vs. TMDB backdrops vs. upload), **draggable card Y-position and background
  crop** (this mattered a lot in testing; auto-placement covered faces), live preview
  scaled to fit the screen.

## Styles (v1)

Already designed with exact specs in `docs/DESIGN_SPEC.md`. Reproduce these first:
1. Last Watched (poster, full-bleed, bottom fade, serif title, optional stars/date, "by user")
2. Profile Stats card (avatar, username, FILMS / THIS YEAR)
3. Profile Favourites card (avatar, username, four posters)

Later: Review card, Ratings histogram card, Recently watched list, Diary list.

## Design rules

- Canvas 1080×1920. Instagram safe zones: keep key content out of the top ~250px
  and bottom ~300px.
- The film grain overlay (~10% opacity) and dark fades are part of the look.
- Pull an accent palette from the poster (`node-vibrant` / `fast-average-color`) for
  optional tinted variants.
- Long titles shrink to fit. Reviews clamp with an ellipsis.

## Reference material in this repo

- `docs/DESIGN_SPEC.md` has the exact colours, sizes and positions of the approved cards.
- `docs/DATA_SOURCES.md` covers data sources, what's verified and what still needs checking.
- `docs/design-reference/reference-screenshots/` has screenshots of the paid app (inspiration only).
- `docs/design-reference/my-renders/`: Akif approved these renders. Match them.
- `docs/design-reference/prototype_build.py` is the working Python + Playwright
  prototype that produced those renders. Its CSS is the source of truth.
- `docs/sample-assets/` has test posters and an avatar (for local dev only; don't commit
  copyrighted posters to the public repo, so add the folder to .gitignore).

## First tasks

1. Scaffold the app and port the three v1 styles from `prototype_build.py` into React
   components, then visually compare them against `my-renders/`.
2. Build the `/api/rss` function, check what fields the RSS actually contains
   (see open questions), and wire it to Last Watched.
3. Add the TMDB proxy and a backdrop picker.
4. Add export ZIP parsing for the profile stats and favourites.
5. Add PNG export and share.
