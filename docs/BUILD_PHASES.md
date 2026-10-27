# Build phases

The build order for the app. Each phase lists what gets built, what it teaches, and
how to tell it's finished. Tick items off as you go.

Export stays near the end, as in the "First tasks" in `CLAUDE.md` (decided
2026-10-28). Testing is on Android + desktop only; iOS Safari isn't a target.

## Overview

| Phase | What gets built | What you learn | Done when |
|---|---|---|---|
| 0. Groundwork | Git repo, check the real data sources | Git habits, reading raw XML/CSV | Real field names are written down in `DATA_SOURCES.md` |
| 1. Static cards | Scaffold the app, port the 3 v1 styles with hardcoded data | React components and props, CSS positioning, `transform: scale` | Side-by-side screenshots match `my-renders/` |
| 2. Editor | Style picker, toggles, drag, background pan, upload | State management, pointer events, controlled inputs | The Holdovers card can be made without touching code |
| 3. Backend | `/api/rss`, `/api/tmdb/*`, image proxy, `DataSource` | Serverless functions, env secrets, HTTP caching, TS interfaces | Typing `meakif` fills in Last Watched |
| 4. Export ZIP | JSZip + PapaParse, stats, TMDB matching | File APIs, data transformation, fuzzy matching | Stats and Favourites cards fill in from the ZIP |
| 5. Export + share | PNG export, Web Share API, download fallback | Canvas/CORS rules, font embedding, browser quirks | A card exported on an Android phone matches the desktop one |
| 6. Ship | Attribution, polish, README, licence, deploy | Deployment, open-source hygiene | Live URL that a friend can use |
| 7. Later | More styles | Building with less help | — |

---

## Phase 0: Groundwork

- [ ] `git init`, first commit, create the GitHub repo (Akif)
- [ ] Check that `docs/sample-assets/` and `private/` stay out of the repo (both are in `.gitignore`)
- [x] Install Node LTS (Node 24.11, npm 11.8)
- [x] Fetch the real RSS feed for `meakif` and record the actual field names
- [ ] Request a real Letterboxd data export, put it in `private/`, and record the CSV
      file names and columns. Is there a `profile.csv` with favourites?
- [ ] Get a TMDB API key and put it in `.env` (see `.env.example`)
- [ ] Update `DATA_SOURCES.md` with what was verified (RSS done, ZIP pending)
- [x] Decide: Vite vs Next.js, and whether export moves to phase 2 (Vite; no)
- [ ] Choose a licence

**Why first:** several later phases depend on these unverified assumptions. The
RSS feed does include `tmdb:movieId` (or `tmdb:tvId`), so Last Watched needs no
title matching at all.

## Phase 1: Static cards

- [ ] Scaffold React + TypeScript (Vite or Next.js, depending on the decision)
- [ ] Load Inter and Lora from Google Fonts
- [ ] `<Stage>`: fixed 1080×1920 node, scaled to fit the screen with `transform: scale`
- [ ] Shared primitives: `<Stars value>` (half stars), `<Grain/>`, `<ProfileCard>`, `<PosterRow>`
- [ ] Port style 1, Last Watched (full and username-only variants)
- [ ] Port style 2, Profile Stats
- [ ] Port style 3, Profile Favourites (centred and shifted-left variants)
- [ ] Style module shape: `{ id, name, supports, options schema, Component }`
- [ ] Playwright visual test: screenshot each card and compare to `my-renders/`

**Done when:** the screenshots match the approved renders.

## Phase 2: Editor

- [ ] Editor state in one `useReducer` (style, toggles, offsets, data)
- [ ] Style picker
- [ ] Toggles: Rating / Date / Username
- [ ] Hand-written pointer-event drag for card Y (and X for the shifted variant).
      Convert screen pixels ÷ preview scale = card pixels
- [ ] Background pan / crop control
- [ ] Background picker: poster / upload (TMDB backdrops come in phase 3)
- [ ] Avatar upload
- [ ] Persistence: settings in localStorage, uploaded images in IndexedDB (`idb-keyval`)

**Done when:** you can make the Holdovers card without touching code.

## Phase 3: Backend

- [ ] `DataSource` TypeScript interface (designed by Akif)
- [ ] `GET /api/rss?user=`: fetch, parse, return clean JSON. Cache headers (`s-maxage`)
- [ ] `RssSource` implementation, wired to Last Watched
- [ ] `GET /api/tmdb/*`: key-hiding proxy that **only allows the endpoints we use** (not an open relay)
- [ ] Image proxy, so canvas export isn't blocked by CORS (first check whether TMDB's
      image CDN already sends CORS headers)
- [ ] Backdrop picker using `/movie/{id}/images`, preferring `original` size
- [ ] Warn when a background image is upscaled more than about 2×
- [ ] TMDB key in `.env` and in the host's env settings, never in client code

**Done when:** typing `meakif` fills in Last Watched with a real poster.

## Phase 4: Export ZIP

- [ ] File picker for the ZIP, parsed in the browser with JSZip + PapaParse (never uploaded)
- [ ] Films count = rows in `watched.csv`
- [ ] This year = diary rows with this year's watched date
- [ ] Ratings histogram = count of each value in `ratings.csv`
- [ ] Favourites (from `profile.csv` if it exists, otherwise picked by hand)
- [ ] Match films to TMDB by title + year through `/search/movie`
- [ ] "Wrong film? Fix it" picker for mismatches
- [ ] Save the derived stats in localStorage
- [ ] Vitest unit tests for the CSV → stats logic

**Done when:** the Stats and Favourites cards fill in from your own ZIP.

## Phase 5: Export + share

- [ ] Export the stage node to PNG at full 1080×1920 (not the scaled preview size)
- [ ] Make sure fonts and images are embedded and same-origin
- [ ] Web Share API on mobile (`navigator.share` with files), download fallback
- [ ] Test on a real Android phone (Chrome) and desktop browsers
- [ ] If client-side export is unreliable, write down the decision to fall back to satori

**Done when:** a card exported on an Android phone matches the desktop one.

## Phase 6: Ship

- [ ] About/Credits page with the TMDB logo and notice
- [ ] `<FitText>` for long titles, ellipsis clamp for reviews
- [ ] Optional accent palette from the poster (`node-vibrant` / `fast-average-color`)
- [ ] Check the Instagram safe zones (top ~250px, bottom ~300px)
- [ ] Manual inputs for anything missing (followers, etc.)
- [ ] README, open-source licence, screenshots (without copyrighted posters in the repo)
- [ ] Deploy (Vercel to start)
- [ ] Ask an AI to do a security review: leaked secrets, open proxy

**Done when:** there's a live URL a friend can use.

## Phase 7: Later

- [ ] Review card
- [ ] Ratings histogram card
- [ ] Recently watched list
- [ ] Diary list
- [ ] Optionally email `api@letterboxd.com` and add an `ApiSource` if access is granted
