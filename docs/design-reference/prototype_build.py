"""Render Letterboxd-style Instagram story cards at 1080x1920."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.resolve()
IMG = (ROOT / "img").as_uri()
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

USER = "meakif"
GREEN = "#00e054"

GRAIN = """<svg class="grain" xmlns="http://www.w3.org/2000/svg" width="1080" height="1920">
<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix type="saturate" values="0"/></filter>
<rect width="100%" height="100%" filter="url(#n)"/></svg>"""

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
body{position:relative;font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.grain{position:absolute;inset:0;opacity:.10;mix-blend-mode:overlay;pointer-events:none}
.serif{font-family:'Lora',serif}

/* profile card */
.card{position:absolute;left:172px;width:736px;background:#435666;border-radius:54px;
  box-shadow:0 18px 50px rgba(0,0,0,.28),0 2px 8px rgba(0,0,0,.18);
  border:1.5px solid rgba(255,255,255,.07)}
.avatar{position:absolute;left:50%;top:0;width:212px;height:212px;margin:-106px 0 0 -106px;
  border-radius:50%;background:url(%IMG%/avatar.jpg) center/cover;
  box-shadow:0 10px 30px rgba(0,0,0,.35)}
.name{margin-top:132px;text-align:center;color:#fff;font-weight:700;font-size:62px;
  letter-spacing:-0.5px;line-height:1}
.rule{height:2px;background:#5f6d7f;margin:44px 23px 0}
"""


def page(body: str, extra_css: str = "") -> str:
    css = (BASE_CSS + extra_css).replace("%IMG%", IMG)
    return f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>{body}</body></html>"


def stars(n: float, size: int) -> str:
    full = int(n)
    half = n - full >= 0.5
    star = (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"><path fill="{GREEN}" '
            'd="M12 1.8l3.1 6.6 7.1.9-5.2 4.9 1.3 7.1L12 17.8l-6.3 3.5 1.3-7.1L1.8 9.3l7.1-.9z"/></svg>')
    h = ""
    if half:
        h = (f'<svg width="{size//2+2}" height="{size}" viewBox="0 0 13 24"><path fill="{GREEN}" '
             'd="M12 1.8v16L5.7 21.3l1.3-7.1L1.8 9.3l7.1-.9z"/></svg>')
    return star * full + h


# 1. Last Watched — The Batman
last_watched = page(f"""
<div class="bg" style="background-image:url({IMG}/batman.jpg);background-size:auto 1920px;background-position:50% 0"></div>
<div class="shade"></div>
{GRAIN}
<div class="info">
  <div class="kicker">LAST WATCHED</div>
  <div class="title serif">The Batman</div>
  <div class="stars">{stars(4, 58)}</div>
  <div class="meta">23 Oct <span class="dot">·</span> by <b>{USER}</b></div>
</div>
""", """
.shade{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 14%,rgba(0,0,0,0) 46%,rgba(0,0,0,.55) 62%,rgba(0,0,0,.92) 80%,#000 92%),
  radial-gradient(120% 70% at 50% 40%,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)}
.info{position:absolute;left:75px;right:75px;top:1258px}
.kicker{color:#a9b9c8;font-weight:500;font-size:34px;letter-spacing:1.6px}
.title{color:#fff;font-weight:700;font-size:112px;line-height:1.1;margin-top:22px;letter-spacing:-0.5px}
.stars{margin-top:22px;display:flex;gap:4px}
.meta{margin-top:30px;color:#b4bcc5;font-size:39px;font-weight:400}
.meta b{color:#fff;font-weight:600;margin-left:4px}
.dot{margin:0 8px;color:#8a929c}
""")

# 2. Profile stats — Princess Mononoke
stats = page(f"""
<div class="bg" style="background-image:url({IMG}/mononoke.jpg)"></div>
{GRAIN}
<div class="card" style="top:1010px;height:432px">
  <div class="avatar"></div>
  <div class="name">{USER}</div>
  <div class="rule"></div>
  <div class="stats">
    <div><div class="num serif">246</div><div class="lab">FILMS</div></div>
    <div><div class="num serif">27</div><div class="lab">THIS YEAR</div></div>
  </div>
</div>
""", """
.stats{display:flex;justify-content:space-around;padding:0 40px;margin-top:34px;text-align:center}
.stats>div{width:50%}
.num{color:#fff;font-weight:700;font-size:64px;line-height:1}
.lab{color:#fff;font-size:28px;font-weight:400;letter-spacing:1px;margin-top:22px}
""")

# 3. Profile + four favourites — The Holdovers
favs = "".join(f'<div class="p" style="background-image:url({IMG}/{f}.jpg)"></div>'
               for f in ["mononoke", "silence", "holdovers", "bruges"])
favourites = page(f"""
<div class="bg" style="background-image:url({IMG}/holdovers.jpg);background-position:80% 50%"></div>
{GRAIN}
<div class="card" style="top:1120px;height:606px">
  <div class="avatar"></div>
  <div class="name">{USER}</div>
  <div class="rule"></div>
  <div class="lab">FAVOURITE FILMS</div>
  <div class="row">{favs}</div>
</div>
""", """
.lab{text-align:center;color:#a7b9ca;font-size:30px;letter-spacing:.8px;margin-top:40px}
.row{display:flex;gap:13px;padding:0 22px;margin-top:30px}
.p{flex:1;aspect-ratio:2/3;border-radius:13px;background-size:cover;background-position:center;
  box-shadow:0 0 0 1px rgba(255,255,255,.12) inset,0 4px 10px rgba(0,0,0,.25)}
""")

favourites_mononoke = favourites.replace(
    f"url({IMG}/holdovers.jpg);background-position:80% 50%",
    f"url({IMG}/mononoke-still.jpg);background-position:48.5% 50%",
).replace('style="top:1120px;height:606px"', 'style="top:660px;height:606px"')

last_watched_simple = (last_watched
    .replace(f'<div class="stars">{stars(4, 58)}</div>\n', '')
    .replace(f'23 Oct <span class="dot">·</span> by <b>{USER}</b>', f'by <b>{USER}</b>')
    .replace('top:1258px', 'top:1348px')
    .replace('.meta{margin-top:30px', '.meta{margin-top:24px'))

favourites_mononoke2 = favourites.replace(
    f"url({IMG}/holdovers.jpg);background-position:80% 50%",
    f"url({IMG}/mononoke-poster2.jpg);background-position:50% 50%",
).replace('style="top:1120px;height:606px"', 'style="top:%CARDTOP%px;height:606px"')

cards = {
    "1b-last-watched-the-batman-simple": last_watched_simple,
    "5-favourite-films-mononoke-poster": favourites_mononoke2.replace("%CARDTOP%", "1000"),
    "6-favourite-films-mononoke-left": favourites_mononoke2.replace("%CARDTOP%px;", "1115px;left:44px;"),
    "4-favourite-films-mononoke": favourites_mononoke,
    "1-last-watched-the-batman": last_watched,
    "2-profile-stats-mononoke": stats,
    "3-favourite-films-holdovers": favourites,
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    for name, html in cards.items():
        f = ROOT / f"{name}.html"
        f.write_text(html)
        pg.goto(f.as_uri())
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(OUT / f"{name}.png"), full_page=False)
        print("wrote", name)
    b.close()
