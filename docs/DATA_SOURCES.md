# Data sources — research notes (October 2026)

## Letterboxd official API: not available to us

- https://letterboxd.com/api-beta/ says access is by request (email api@letterboxd.com,
  with the project name as the subject). There's no guaranteed reply.
- They're currently **not** approving data-analysis/visualization, LLM, private or
  personal projects, or anything that recreates features of their paid tiers.
- The paid app "Stories for Letterboxd" (Gianpiero Spinelli) added "support for the
  Letterboxd APIs" in 2022, which is likely how it gets stats. Its access was probably
  granted before the current restrictions.
- Plan: build without the API. Optionally email them anyway, and keep a
  `DataSource` interface so the API could be added later.

## Public RSS feed (allowed; Letterboxd points developers to it)

- URL: `https://letterboxd.com/<username>/rss/`
- It covers recent diary entries, reviews and lists. It does not include profile
  stats, favourites, followers or the ratings histogram.
- It has to be fetched server-side (CORS). Cache it for a few minutes.

### Verified against `meakif`'s real feed (28 Oct 2026)

- HTTP 200, `application/rss+xml`, **50 items** (the newest 50 diary entries; for
  meakif that reaches back about a year). There were no list items in this feed.
- Item fields (namespaces `letterboxd:` = `https://letterboxd.com`, `tmdb:` = `https://themoviedb.org`):

  | Field | Example | Notes |
  |---|---|---|
  | `title` | `The Batman, 2022 - ★★★★` | Display string. Don't parse it, use the fields below |
  | `link` | `https://letterboxd.com/meakif/film/the-batman/` | |
  | `guid` | `letterboxd-watch-1549593383` / `letterboxd-review-1553667782` | **Prefix tells watch vs review** |
  | `pubDate` | `Fri, 23 Oct 2026 07:28:33 +1300` | When it was *logged*, not watched |
  | `letterboxd:watchedDate` | `2026-10-23` | Plain date, no time zone |
  | `letterboxd:rewatch` | `Yes` / `No` | |
  | `letterboxd:filmTitle` | `The Batman` | |
  | `letterboxd:filmYear` | `2022` | |
  | `letterboxd:memberRating` | `4.0`, `2.5` | **Missing entirely when unrated** (2 of 50 items) |
  | `letterboxd:memberLike` | `Yes` / `No` | |
  | `tmdb:movieId` | `414906` | Present for films (48 of 50) |
  | `tmdb:tvId` | `42821` | **Used instead of `movieId` for TV** (2 of 50). Use TMDB `/tv/{id}` |
  | `description` | CDATA HTML | `<p><img src=…poster…></p>` then the review paragraphs, or `<p>Watched on Friday October 23, 2026.</p>` when there's no review |
  | `dc:creator` | `Ahnaf Akif` | Display name, not the username |

- **The feed is ordered by `pubDate` (log time), not by watched date.** Example: an
  entry watched on 19 Oct but logged on 25 Oct is first, above a film watched on 25 Oct.
  "Last watched" must sort by `watchedDate` (tie-break by `pubDate`), or the user picks
  the entry.
- The poster in `description` is on Letterboxd's CDN (`a.ltrbxd.com`). Don't use it
  (see below). Use the TMDB id instead, so **no title matching is needed for RSS items**.
- Review text: only trust it when the guid starts with `letterboxd-review-`. Strip the
  first `<p><img></p>` and decode HTML entities (`&#039;`).

## Letterboxd data export ZIP (allowed; uploaded by the user)

- Settings → Data → Export. The ZIP contains CSV files.
- Parse it in the browser with JSZip + PapaParse, and don't upload it anywhere.
- I expect these files (**verify against a real export**): `watched.csv`, `diary.csv`
  (with watch dates), `ratings.csv`, `reviews.csv`, `watchlist.csv`, and `profile.csv`
  (should hold the favourite films, but this is unconfirmed).
- Derived stats:
  - Films count = rows in `watched.csv`
  - This year = diary rows with this year's watched date (may differ slightly from
    Letterboxd's count because of rewatches)
  - Ratings histogram = count of each value (0.5–5) in `ratings.csv`
- It's a snapshot, so the user re-exports to refresh it. Store the derived stats in
  localStorage.
- It doesn't include followers or following. Use manual input for those.
- The CSVs reference films by Letterboxd URI and name/year, not by TMDB ID. Match
  them to TMDB by title and year through search, and let the user correct mismatches.

## TMDB

- It's free for non-commercial use with attribution. Use an approved TMDB logo
  (less prominent than our own branding), the notice "This product uses the TMDB API
  but is not endorsed or certified by TMDB.", and refer to them only as "TMDB" or
  "The Movie Database". Commercial use would need a paid license.
- Use `/movie/{id}/images` for posters and backdrops, and `/search/movie` for matching.
- The studios own the poster images. Fan share cards are fine for a free, personal-use
  tool, but don't bundle posters in the repo.

## What not to do

- Don't scrape letterboxd.com profile pages. They actively block bots (we hit this),
  it's fragile, and an open-source scraper risks a takedown.
- Don't hotlink Letterboxd CDN images. CORS blocks canvas export, and it's their bandwidth.
