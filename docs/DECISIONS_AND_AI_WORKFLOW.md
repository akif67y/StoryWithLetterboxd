# Design decisions and coding with AI

Notes from the planning chat (23 Oct 2026). Part 1 compares the main technical
choices. Part 2 covers how to split work with an AI assistant while still learning.
The build order itself is in `BUILD_PHASES.md`.

**Status:** these are recommendations, not settled decisions. Once Akif decides,
record the result in the Decision log at the bottom and in `CLAUDE.md`.

---

# Part 1: Design choices

## Framework: Vite + React vs Next.js

| | Vite + React SPA + `/api` functions | Next.js |
|---|---|---|
| Pros | Simple model: a website plus two functions. You learn plain React without framework magic. Fast dev server | Frontend and API in one framework. Built-in image optimisation and routing |
| Cons | Two concepts to wire together, though Vercel and Cloudflare handle `/api` next to Vite fine | Server Components, the client/server split and caching rules add a lot of complexity this app doesn't need. Mistakes are hard to debug while still learning React |

**Recommendation: Vite.** The app is almost entirely client-side. Next.js would
mostly teach Next.js, not React.

## Card rendering and export (the most important choice)

| Option | Pros | Cons |
|---|---|---|
| `html-to-image` | Popular. Card is plain DOM + CSS, so the prototype CSS ports 1:1 | Draws through SVG `foreignObject`. iOS Safari sometimes misses images on the first render, and fonts/images must be same-origin or inlined |
| `modern-screenshot` | Same idea as `html-to-image`, maintained more actively, handles fonts better | Smaller community |
| `satori` (serverless) | Same output on every device | Supports only part of CSS (flexbox only, no `mix-blend-mode`, so the grain needs another method). Means writing the cards twice or in a limited style |
| Headless Chrome on a server (like the Python prototype) | Pixel-perfect, and it's known to work | Heavy and slow on serverless, costs money at scale, works against "free and simple" |

**Recommendation:** start with `modern-screenshot` and test it on iOS in phase 2.
Keep satori as the documented fallback.

## Styling

| | CSS Modules / plain CSS | Tailwind | Inline styles |
|---|---|---|---|
| Cards | ✅ Prototype CSS pastes in almost unchanged | ❌ Exact pixel values like `top-[1258px]` everywhere are unreadable | OK for dynamic values such as drag offsets |
| Editor UI | Fine | ✅ Fast to build | ❌ |

**Recommendation:** CSS Modules for cards, inline styles only for user-controlled
positions. Tailwind for the editor is optional.

## State management

- **`useState` / `useReducer` + Context:** no dependencies, and you learn how React
  actually works. The editor state (style, toggles, offsets, data) fits in one reducer.
- **Zustand:** less boilerplate and avoids prop drilling, but it hides the lesson.

**Recommendation:** use `useReducer` first. Switch only if it gets painful, and then
it will be clear *why* Zustand exists.

## Drag-to-position

- **Write it yourself with Pointer Events:** about 40 lines, works for touch and
  mouse, and teaches event handling plus the scaled-coordinate maths
  (screen pixels ÷ preview scale = card pixels).
- **A library (`react-draggable`, `dnd-kit`):** quicker, but built for lists and
  grids, not "offset this one thing".

**Recommendation:** write it yourself. It's the best small learning exercise in the project.

## Local persistence

- **localStorage:** simple, about 5 MB, strings only. Good for stats, toggles and username.
- **IndexedDB** (with the `idb-keyval` wrapper): needed for uploaded avatar and
  background images, which easily go over the localStorage limit once base64-encoded.

## Hosting

Vercel, Netlify and Cloudflare all work on their free tiers. Vercel has the
smoothest Vite + `/api` setup. Cloudflare has the most generous free bandwidth,
which matters if the image proxy gets traffic.

**Recommendation:** start with Vercel. The functions are small enough to move later.

## Testing

- **Vitest unit tests** for the pure logic: RSS parsing, CSV → stats, half-star
  rounding, title matching. Cheap, and they catch real bugs.
- **Playwright visual tests** that screenshot each card and compare it to
  `my-renders/`. Playwright is already familiar from the prototype, and this is the
  best defence against AI quietly breaking the design.

---

# Part 2: Coding with AI

## Things you need to understand yourself

1. **The data flow and trust boundaries.** What runs in the browser, what runs on
   the server, and why the TMDB key must never reach the client. Why the ZIP is
   never uploaded. AI will happily put a secret in frontend code if nobody notices.
2. **React's mental model.** Rendering, state, props, why effects run. Without it
   you can't judge whether AI code is right or just looks right.
3. **CSS positioning and layout.** The whole product is CSS. The visual fine-tuning
   is yours, because the AI can't see what you see.
4. **Git.** Small commits after every working step make AI experiments safe to undo.
5. **Debugging with browser DevTools.** Network tab (CORS errors, failed proxies),
   Elements (why it's misaligned), Console.
6. **TypeScript types as contracts.** Design the `DataSource` interface and the
   style-module shape yourself. Those types are the architecture.
7. **The legal and ethical lines.** ToS, TMDB attribution, not looking official.
   AI won't enforce these for you.

## Things AI handles well (review, don't write)

- Scaffolding and config: Vite, tsconfig, ESLint, deploy files
- Porting the prototype CSS into components
- Boilerplate parsing with JSZip and PapaParse
- Writing unit tests once you've described the expected behaviour
- The SVG star and grain components, TypeScript types from sample data

## Where AI is unreliable, so you verify

- **Facts about external services.** RSS field names, CSV column names, TMDB
  endpoints, current library APIs. `DATA_SOURCES.md` already marks several as
  "to verify". Check against real responses.
- **Cross-browser behaviour,** especially iOS Safari. Only a real phone tells you.
- **Visual correctness.** "It matches the design" means nothing until the
  screenshots have been compared.
- **Security.** Have AI review for leaked secrets or an open proxy, but don't trust
  it to get this right on its own. For example, `/api/tmdb/*` should only forward
  allowed paths, not act as an open relay.

## Habits that make AI-assisted work go well

- **Give the AI a way to check its work.** "Port this card, then screenshot it and
  compare it to `my-renders/1-...jpg`" gets much better results than "port this card".
- **Work one phase at a time, and commit between steps.** Big multi-feature
  requests produce code that's hard to review.
- **Keep `CLAUDE.md` current.** Record each settled decision so future sessions
  don't argue it again.
- **For the parts you want to learn, write first and then ask for a review.**
  Good candidates: the drag handler, the editor reducer, the stats calculation.
  For the rest, let AI write and ask it to explain anything unclear.
- **Ask "what could go wrong with this?"** after AI writes something. It's often
  better at spotting problems than at avoiding them the first time.

---

# Decision log

| Decision | Options | Chosen | Date | Why |
|---|---|---|---|---|
| Framework | Vite / Next.js | Vite + React + TS, with `/api` functions | 2026-10-28 | The app is almost all client-side, so plain React is enough |
| Export moved to phase 2 | Yes / No | No, export stays near the end (phase 5) | 2026-10-28 | Akif doesn't think iOS Safari handling is needed. Testing is on Android + desktop only |
| Export library | modern-screenshot / html-to-image / satori | modern-screenshot | 2026-10-28 | Keeps the prototype CSS, handles fonts better. satori stays the fallback |
| Card styling | CSS Modules / Tailwind | CSS Modules (cards and editor), inline styles only for drag offsets | 2026-10-28 | Prototype CSS ports almost 1:1 |
| State | useReducer / Zustand | `useReducer` + Context | 2026-10-28 | No dependency, and teaches React state |
| Hosting | Vercel / Netlify / Cloudflare | Vercel | 2026-10-28 | Smoothest Vite + `/api` setup |
| Name | — | **Stories For Movies** | 2026-10-28 | Doesn't use "Letterboxd" in the name, so it doesn't look official |
| Work split | — | Claude writes most code. Akif does some phase items | 2026-10-28 | Mix of speed and learning |
| Device testing | — | Android (Chrome) + desktop. No iOS device available | 2026-10-28 | |
| Licence | MIT / AGPL-3.0 / … | *pending* | | |
