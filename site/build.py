#!/usr/bin/env python3
"""
LJ RaceLab — static site generator.

    python build.py

Reads everything in content/ and writes a complete website into docs/.
GitHub Pages serves docs/ on the main branch, so there is no server, no
build step in the cloud, and nothing that can break while you sleep.

Adding a journal entry or a project = adding a markdown file in content/
and running this script. The git history of that folder IS the portfolio.
"""

import json, re, shutil, sys
from datetime import date, datetime
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Need the markdown package:  pip install markdown")

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

MD = markdown.Markdown(extensions=["tables", "sane_lists"])


# ─────────────────────────────────────────────────────────── content loading

def parse(path):
    """Split a markdown file into front-matter dict + rendered HTML body."""
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    MD.reset()
    return meta, MD.convert(body.strip())


def load(folder):
    items = []
    d = CONTENT / folder
    if not d.exists():
        return items
    for f in sorted(d.glob("*.md")):
        meta, html = parse(f)
        meta["_body"] = html
        meta["_file"] = f.name
        items.append(meta)
    return items


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def nice_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%-d %B %Y")
    except Exception:
        return s


# ─────────────────────────────────────────────────────────────── the styles

CSS = """
:root{
  --ink:#0b0d10; --panel:#12161b; --panel-2:#171d24;
  --paper:#f7f8fa; --paper-2:#eef1f5; --paper-3:#e4e9ef;
  --line:#c9d2dc; --line-2:#adb9c6; --line-3:#7d8b99;
  --text:#131a21; --text-2:#4c5967; --text-3:#7a8794;
  --accent:#c8202a; --accent-2:#a8161f; --accent-soft:rgba(200,32,42,.09);
  --ok:#1a7a4b; --ok-soft:rgba(26,122,75,.10);
  --amber:#8f5c05; --amber-soft:rgba(143,92,5,.11);
  --grid:rgba(19,26,33,.05);
  --shadow:0 1px 2px rgba(19,26,33,.05),0 10px 28px -14px rgba(19,26,33,.2);
  --disp:"Space Grotesk",system-ui,sans-serif;
  --cond:"IBM Plex Sans Condensed","Helvetica Neue",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Consolas,monospace;
  --shell:1120px;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0e1319; --paper-2:#131a21; --paper-3:#1a222b;
  --line:#243039; --line-2:#31404d; --line-3:#4a5b6b;
  --text:#e4ebf2; --text-2:#93a3b3; --text-3:#6a7988;
  --accent:#ff3d3d; --accent-2:#ff6a6a; --accent-soft:rgba(255,61,61,.12);
  --ok:#3ecb8b; --ok-soft:rgba(62,203,139,.11);
  --amber:#e6a944; --amber-soft:rgba(230,169,68,.12);
  --grid:rgba(130,175,215,.055);
  --shadow:0 1px 2px rgba(0,0,0,.5),0 12px 30px -16px rgba(0,0,0,.8);
}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--paper);color:var(--text);
  font-family:var(--cond);font-size:16.5px;line-height:1.62;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),
                   linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:24px 24px;-webkit-font-smoothing:antialiased;
}
a{color:inherit;text-decoration:none}
.shell{width:min(var(--shell),calc(100% - 36px));margin:0 auto}
img{max-width:100%;height:auto;display:block}

/* header */
.topline{height:3px;background:var(--accent)}
header.site{
  position:sticky;top:0;z-index:50;background:var(--ink);color:#fff;
  border-bottom:1px solid rgba(255,255,255,.09);backdrop-filter:blur(12px);
}
.nav{min-height:66px;display:flex;align-items:center;gap:22px;flex-wrap:wrap;padding:9px 0}
.brand{display:inline-flex;align-items:center;gap:11px;margin-right:auto}
.brand b{display:block;font-family:var(--disp);font-size:14px;letter-spacing:.14em;font-weight:700}
.brand b i{color:#ff4040;font-style:normal}
.brand span{display:block;font-size:9.5px;letter-spacing:.2em;color:#8d99a6;text-transform:uppercase;font-weight:600;margin-top:2px}
nav.main{display:flex;gap:20px;flex-wrap:wrap}
nav.main a{font-size:14px;color:#c3ccd6;transition:color .13s}
nav.main a:hover,nav.main a[aria-current="page"]{color:#fff}
nav.main a[aria-current="page"]{border-bottom:2px solid var(--accent);padding-bottom:2px}

/* hero */
.hero{background:var(--ink);color:#fff;padding:60px 0 54px}
.eyebrow{color:#ff4040;letter-spacing:.2em;font-size:10.5px;font-weight:700;text-transform:uppercase;margin:0}
.hero h1{
  font-family:var(--disp);font-weight:700;font-size:clamp(38px,6.4vw,74px);
  line-height:.98;letter-spacing:-.038em;margin:16px 0 0;text-wrap:balance;
}
.hero h1 em{color:#ff4040;font-style:normal}
.hero .lead{color:#b3bdc8;font-size:19px;line-height:1.6;max-width:60ch;margin:22px 0 0}
.mission{margin-top:30px;padding-left:17px;border-left:3px solid var(--accent);max-width:62ch}
.mission span{color:#7f8b98;font-size:10px;letter-spacing:.18em;font-weight:700;text-transform:uppercase}
.mission p{margin:6px 0 0;font-size:16.5px;color:#dbe2e9}

/* stat strip */
.stats{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin:-30px 0 0;position:relative;z-index:2}
@media(min-width:640px){.stats{grid-template-columns:repeat(4,1fr)}}
.stat{background:var(--paper);padding:16px 18px}
.stat b{display:block;font-family:var(--mono);font-size:30px;font-weight:600;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1}
.stat span{display:block;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-3);font-weight:700;margin-top:7px}
.stat i{display:block;font-style:normal;font-size:12px;color:var(--text-3);font-family:var(--mono);margin-top:3px}

/* sections */
main{padding:0 0 90px}
section.band{padding:54px 0 0}
h2.sec{
  font-family:var(--disp);font-weight:700;font-size:26px;letter-spacing:-.028em;
  margin:0 0 4px;display:flex;align-items:baseline;gap:12px;text-wrap:balance;
}
h2.sec .n{font-family:var(--mono);font-size:11px;color:var(--accent);font-weight:600;letter-spacing:.12em}
.sub{color:var(--text-2);max-width:64ch;margin:6px 0 22px}
.rule{border:0;border-top:1.5px solid var(--line-3);margin:0 0 22px}

/* project cards */
.grid{display:grid;gap:16px}
@media(min-width:700px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1000px){.grid.three{grid-template-columns:repeat(3,1fr)}}
.card{
  background:var(--paper);border:1px solid var(--line);box-shadow:var(--shadow);
  display:flex;flex-direction:column;transition:border-color .14s,transform .14s;
}
a.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card .thumb{aspect-ratio:16/9;background:var(--paper-3);border-bottom:1px solid var(--line);overflow:hidden}
.card .thumb img{width:100%;height:100%;object-fit:cover}
.card .thumb.none{
  display:flex;align-items:center;justify-content:center;
  background-image:repeating-linear-gradient(-45deg,transparent 0 7px,var(--line) 7px 8px);
}
.card .thumb.none span{font-family:var(--mono);font-size:10.5px;color:var(--text-3);letter-spacing:.14em;background:var(--paper);padding:4px 9px;border:1px solid var(--line)}
.card .body{padding:15px 17px 17px;display:flex;flex-direction:column;gap:7px;flex:1}
.card .pid{font-family:var(--mono);font-size:11px;color:var(--accent);font-weight:600;letter-spacing:.11em}
.card h3{font-family:var(--disp);font-size:18px;margin:0;letter-spacing:-.015em;line-height:1.25}
.card p{margin:0;font-size:14.5px;color:var(--text-2);line-height:1.5}
.card .foot{margin-top:auto;padding-top:10px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}

.pill{
  font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:700;
  padding:3px 8px;border:1px solid;white-space:nowrap;
}
.p-complete{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}
.p-progress{color:var(--amber);border-color:var(--amber);background:var(--amber-soft)}
.p-planned{color:var(--text-3);border-color:var(--line-2);background:var(--paper-2)}
.wk{font-family:var(--mono);font-size:11px;color:var(--text-3)}

/* journal */
.entries{display:flex;flex-direction:column;gap:0;border-top:1px solid var(--line)}
a.entry{
  display:grid;grid-template-columns:112px 1fr;gap:18px;padding:17px 0;
  border-bottom:1px solid var(--line);align-items:baseline;transition:background .12s;
}
a.entry:hover{background:var(--paper-2)}
a.entry .d{font-family:var(--mono);font-size:12px;color:var(--text-3);font-variant-numeric:tabular-nums}
a.entry h3{font-family:var(--disp);font-size:18px;margin:0 0 4px;letter-spacing:-.015em}
a.entry p{margin:0;color:var(--text-2);font-size:14.5px}
@media(max-width:600px){a.entry{grid-template-columns:1fr;gap:5px}}

/* article */
article.doc{max-width:70ch;margin:0 auto}
article.doc h2{font-family:var(--disp);font-size:21px;margin:34px 0 4px;letter-spacing:-.015em;padding-bottom:6px;border-bottom:1px solid var(--line)}
article.doc h3{font-family:var(--disp);font-size:17px;margin:26px 0 2px}
article.doc p{margin:13px 0}
article.doc ul,article.doc ol{padding-left:21px}
article.doc li{margin:6px 0}
article.doc img{margin:22px 0;border:1px solid var(--line)}
article.doc table{border-collapse:collapse;width:100%;font-size:14.5px;margin:18px 0;display:block;overflow-x:auto}
article.doc th,article.doc td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
article.doc th{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--text-3);font-weight:700;background:var(--paper-2);white-space:nowrap}
article.doc code{font-family:var(--mono);font-size:.88em;background:var(--paper-2);border:1px solid var(--line);padding:1px 5px}
article.doc pre{font-family:var(--mono);font-size:13px;background:var(--paper-2);border:1px solid var(--line);border-left:2px solid var(--accent);padding:13px 15px;overflow-x:auto}
article.doc blockquote{margin:20px 0;border-left:3px solid var(--accent);padding-left:16px;color:var(--text-2)}

.phead{border-bottom:1.5px solid var(--line-3);padding-bottom:20px;margin-bottom:8px}
.phead .pid{font-family:var(--mono);font-size:12px;color:var(--accent);font-weight:600;letter-spacing:.14em}
.phead h1{font-family:var(--disp);font-weight:700;font-size:clamp(30px,5vw,44px);letter-spacing:-.032em;margin:10px 0 0;line-height:1.03;text-wrap:balance}
.phead .meta{display:flex;gap:9px;flex-wrap:wrap;margin-top:16px;align-items:center}
.skills{display:flex;gap:6px;flex-wrap:wrap;margin-top:14px}
.skills span{font-family:var(--mono);font-size:11px;border:1px solid var(--line);background:var(--paper-2);padding:3px 8px;color:var(--text-2)}

/* roadmap + skills */
.tw{overflow-x:auto;border:1px solid var(--line);background:var(--paper)}
table.grid-t{border-collapse:collapse;width:100%;font-size:14px}
table.grid-t th,table.grid-t td{padding:9px 13px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
table.grid-t th{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--text-3);font-weight:700;background:var(--paper-2)}
table.grid-t tr:last-child td{border-bottom:0}
table.grid-t td.n{font-family:var(--mono);font-variant-numeric:tabular-nums}
tr.now{background:var(--accent-soft)}
tr.now td:first-child{box-shadow:inset 3px 0 0 var(--accent)}

.skillrow{display:grid;grid-template-columns:minmax(150px,1.1fr) 120px 1fr;gap:15px;align-items:center;padding:13px 0;border-bottom:1px solid var(--line)}
.skillrow:last-child{border-bottom:0}
.skillrow b{font-size:15px}
.pips{display:flex;gap:4px}
.pip{width:17px;height:9px;border:1px solid var(--line-2);background:var(--paper-2)}
.pip.on{background:var(--accent);border-color:var(--accent)}
.skillrow i{font-style:normal;font-size:13.5px;color:var(--text-3);line-height:1.45}
@media(max-width:640px){.skillrow{grid-template-columns:1fr;gap:6px}}

/* resources */
.res{display:grid;gap:12px}
@media(min-width:640px){.res{grid-template-columns:repeat(2,1fr)}}
a.rescard{border:1px solid var(--line);background:var(--paper);padding:13px 15px;transition:border-color .13s}
a.rescard:hover{border-color:var(--accent)}
a.rescard b{display:block;font-family:var(--disp);font-size:15px}
a.rescard span{display:block;font-size:13.5px;color:var(--text-3);margin-top:2px}

.backlink{font-family:var(--mono);font-size:12px;color:var(--text-3);display:inline-block;margin-bottom:20px}
.backlink:hover{color:var(--accent)}

footer.site{border-top:1px solid var(--line);margin-top:70px;padding:26px 0 44px;background:var(--paper-2)}
.fwrap{display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--text-3);font-weight:600}
.fwrap .d{color:var(--accent)}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Space+Grotesk:wght@500;700&family=IBM+Plex+Mono:wght@400;500;600'
         '&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&display=swap">')

MARK = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true">'
        '<circle cx="17" cy="17" r="12.5" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="1"/>'
        '<path d="M17 1.5v31M1.5 17h31" stroke="rgba(255,255,255,.13)" stroke-width="1" stroke-dasharray="3 2.5"/>'
        '<path d="M9 8.5v11.5h11.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="square"/>'
        '<path d="M25 8.5v9.5h-5" fill="none" stroke="#ff4040" stroke-width="2.4" stroke-linecap="square"/>'
        '<circle cx="17" cy="17" r="2.6" fill="none" stroke="#ff4040" stroke-width="1.2"/></svg>')

NAVLINKS = [("/", "Home"), ("/garage/", "Garage"), ("/journal/", "Journal"),
            ("/progress/", "Progress"), ("/about/", "About")]


def page(site, title, body, current="/", desc="", depth=0):
    CUR = ' aria-current="page"'
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, CUR if h == current else "", n)
        for h, n in NAVLINKS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {site['name']}</title>
<meta name="description" content="{desc or site['intro']}">
<meta property="og:title" content="{title} · {site['name']}">
<meta property="og:description" content="{desc or site['intro']}">
<meta property="og:type" content="website">
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="topline"></div>
<header class="site"><div class="shell nav">
  <a class="brand" href="/">{MARK}<span><b>LJ <i>RACELAB</i></b><span>{site['tagline']}</span></span></a>
  <nav class="main">{nav}</nav>
</div></header>
{body}
<footer class="site"><div class="shell fwrap">
  <span>Design <span class="d">•</span> Build <span class="d">•</span> Test <span class="d">•</span> Evolve</span>
  <span style="margin-left:auto;text-transform:none;letter-spacing:0;font-weight:400">
    {site['name']} · {site['location']} · Season {site['season']}
  </span>
</div></footer>
</body>
</html>
"""


# ───────────────────────────────────────────────────────────────── fragments

def status_pill(s):
    cls = {"complete": "p-complete", "in-progress": "p-progress"}.get(s, "p-planned")
    label = {"complete": "Complete", "in-progress": "In progress"}.get(s, "Planned")
    return f'<span class="pill {cls}">{label}</span>'


def project_card(p):
    slug = p["_slug"]
    hero = p.get("hero", "").strip()
    thumb = (f'<div class="thumb"><img src="/{hero}" alt="{p["title"]}" loading="lazy"></div>'
             if hero else
             '<div class="thumb none"><span>NO PHOTO YET</span></div>')
    return f"""<a class="card" href="/projects/{slug}/">
  {thumb}
  <div class="body">
    <span class="pid">PROJECT {p['id']}</span>
    <h3>{p['title']}</h3>
    <p>{p.get('summary','')}</p>
    <div class="foot">{status_pill(p.get('status','planned'))}<span class="wk">Week {p.get('week','—')}</span></div>
  </div>
</a>"""


def stat(value, label, note=""):
    return (f'<div class="stat"><b>{value}</b><span>{label}</span>'
            f'{f"<i>{note}</i>" if note else ""}</div>')


# ─────────────────────────────────────────────────────────────────── builder

def build():
    site = json.loads((CONTENT / "site.json").read_text())
    skills = json.loads((CONTENT / "skills.json").read_text())
    weeks = json.loads((CONTENT / "weeks.json").read_text())
    projects = load("projects")
    journal = load("journal")

    for p in projects:
        p["_slug"] = f"{p['id']}-{slugify(p['title'])}"
    for j in journal:
        j["_slug"] = f"{j['date']}-{slugify(j['title'])}"
    journal.sort(key=lambda j: j["date"], reverse=True)

    # ---- derived numbers, never hand-maintained
    done_weeks = sum(1 for w in weeks if w["status"] == "complete")
    done_projects = sum(1 for p in projects if p.get("status") == "complete")
    hours = done_weeks * site["hours_per_week"]
    today = date.today().isoformat()
    current = None
    for w in weeks:
        if w["tue"] <= today:
            current = w
    pct = round(done_weeks / site["season_weeks"] * 100)

    # ---- keep CNAME across rebuilds (deleting it unsets the custom domain)
    cname = (DOCS / "CNAME").read_text().strip() if (DOCS / "CNAME").exists() else site["domain"]
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    (DOCS / "CNAME").write_text(cname + "\n")
    (DOCS / ".nojekyll").write_text("")
    if ASSETS.exists():
        shutil.copytree(ASSETS, DOCS / "assets", dirs_exist_ok=True)

    def write(rel, html):
        f = DOCS / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html, encoding="utf-8")

    # ── home ────────────────────────────────────────────────────────────
    featured = [p for p in projects if p.get("status") == "complete"][:3]
    if len(featured) < 3:
        featured += [p for p in projects if p not in featured][:3 - len(featured)]
    latest = journal[:3]

    home = f"""<section class="hero"><div class="shell">
  <p class="eyebrow">Season {site['season']} — {site['season_name']} · {site['location']}</p>
  <h1>Design. Build.<br>Test. <em>Evolve.</em></h1>
  <p class="lead">{site['intro']}</p>
  <div class="mission"><span>Mission</span><p>{site['mission']}</p></div>
</div></section>

<div class="shell"><div class="stats">
  {stat(f"{done_weeks}/{site['season_weeks']}", "Weeks complete", f"{pct}% of Season 1")}
  {stat(f"{done_projects}/{len(projects)}", "Projects complete")}
  {stat(hours, "Engineering hours", "logged this season")}
  {stat(f"W{current['n']}" if current else "—", "Current week", current['title'] if current else 'Starts 1 September')}
</div></div>

<main>
<section class="band"><div class="shell">
  <h2 class="sec"><span class="n">01</span> The garage</h2>
  <p class="sub">Every project, finished or not. The ones that failed are the ones worth reading.</p>
  <hr class="rule">
  <div class="grid three">{"".join(project_card(p) for p in featured)}</div>
  <p style="margin-top:20px"><a href="/garage/" style="font-family:var(--mono);font-size:13px;color:var(--accent)">See all {len(projects)} projects →</a></p>
</div></section>

<section class="band"><div class="shell">
  <h2 class="sec"><span class="n">02</span> Latest from the logbook</h2>
  <p class="sub">What got built, what broke, and what the numbers said.</p>
  <hr class="rule">
  <div class="entries">{"".join(entry_row(j) for j in latest)}</div>
  <p style="margin-top:20px"><a href="/journal/" style="font-family:var(--mono);font-size:13px;color:var(--accent)">All entries →</a></p>
</div></section>
</main>"""
    write("index.html", page(site, "Junior Race Engineer", home, "/",
                             site["intro"]))

    # ── garage ──────────────────────────────────────────────────────────
    body = f"""<main><section class="band"><div class="shell">
  <h2 class="sec"><span class="n">—</span> The garage</h2>
  <p class="sub">Eight projects across Season 1, from a reverse-engineered bracket to a
  load-cell force balance precise enough to prove a 10% difference in drag.</p>
  <hr class="rule">
  <div class="grid three">{"".join(project_card(p) for p in projects)}</div>
</div></section></main>"""
    write("garage/index.html", page(site, "Garage", body, "/garage/",
                                    "Every LJ RaceLab engineering project."))

    # ── project pages ───────────────────────────────────────────────────
    for p in projects:
        hero = p.get("hero", "").strip()
        heroimg = f'<img src="/{hero}" alt="{p["title"]}">' if hero else ""
        sk = "".join(f"<span>{s.strip()}</span>"
                     for s in p.get("skills", "").split(",") if s.strip())
        body = f"""<main><div class="shell" style="padding-top:40px">
  <a class="backlink" href="/garage/">← back to the garage</a>
  <article class="doc">
    <div class="phead">
      <span class="pid">PROJECT {p['id']}</span>
      <h1>{p['title']}</h1>
      <div class="meta">{status_pill(p.get('status','planned'))}
        <span class="wk">Week {p.get('week','—')}</span></div>
      <div class="skills">{sk}</div>
    </div>
    {heroimg}
    {p['_body']}
  </article>
</div></main>"""
        write(f"projects/{p['_slug']}/index.html",
              page(site, p["title"], body, "/garage/", p.get("summary", "")))

    # ── journal ─────────────────────────────────────────────────────────
    body = f"""<main><section class="band"><div class="shell">
  <h2 class="sec"><span class="n">—</span> Engineering logbook</h2>
  <p class="sub">Written as it happened. Problem, prediction, what the data actually said,
  and what changed next.</p>
  <hr class="rule">
  <div class="entries">{"".join(entry_row(j) for j in journal)}</div>
</div></section></main>"""
    write("journal/index.html", page(site, "Journal", body, "/journal/",
                                     "The LJ RaceLab engineering logbook."))

    for j in journal:
        tags = "".join(f"<span>{t.strip()}</span>"
                       for t in j.get("tags", "").split(",") if t.strip())
        body = f"""<main><div class="shell" style="padding-top:40px">
  <a class="backlink" href="/journal/">← all entries</a>
  <article class="doc">
    <div class="phead">
      <span class="pid">{nice_date(j['date']).upper()} · WEEK {j.get('week','—')}</span>
      <h1>{j['title']}</h1>
      <div class="skills">{tags}</div>
    </div>
    {j['_body']}
  </article>
</div></main>"""
        write(f"journal/{j['_slug']}/index.html",
              page(site, j["title"], body, "/journal/"))

    # ── progress ────────────────────────────────────────────────────────
    rows = ""
    for w in weeks:
        is_now = current and w["n"] == current["n"]
        rows += (f'<tr class="{"now" if is_now else ""}">'
                 f'<td class="n">{w["n"]}</td>'
                 f'<td>{w["title"]}</td>'
                 f'<td class="n">{nice_date(w["tue"])}</td>'
                 f'<td class="n">{w["project"]}</td>'
                 f'<td>{status_pill(w["status"])}</td></tr>')
    srows = ""
    for s in skills:
        pips = "".join(f'<span class="pip{" on" if i < s["level"] else ""}"></span>'
                       for i in range(s["max"]))
        srows += (f'<div class="skillrow"><b>{s["name"]}</b>'
                  f'<span class="pips">{pips}</span><i>{s["note"]}</i></div>')

    body = f"""<main><section class="band"><div class="shell">
  <h2 class="sec"><span class="n">01</span> Season 1 roadmap</h2>
  <p class="sub">Thirteen weeks plus a build week. Three sessions a week, about three hours.</p>
  <hr class="rule">
  <div class="tw"><table class="grid-t">
    <thead><tr><th>Wk</th><th>Focus</th><th>Starts</th><th>Project</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div></section>

<section class="band"><div class="shell">
  <h2 class="sec"><span class="n">02</span> Skill matrix</h2>
  <p class="sub">Honest self-assessment, updated at each 30-day checkpoint. Aerodynamics
  starts at zero on purpose — it was the weakest subject on the baseline diagnostic,
  and it's what the back half of the season is built around.</p>
  <hr class="rule">
  <div>{srows}</div>
</div></section>

<section class="band"><div class="shell">
  <h2 class="sec"><span class="n">03</span> Tools &amp; resources</h2>
  <p class="sub">What this is actually built with.</p>
  <hr class="rule">
  <div class="res">{"".join(f'<a class="rescard" href="{r["url"]}" rel="noopener">'
                            f'<b>{r["name"]}</b><span>{r["note"]}</span></a>'
                            for r in site["resources"])}</div>
</div></section></main>"""
    write("progress/index.html", page(site, "Progress", body, "/progress/",
                                      "Season 1 roadmap, skill matrix and tools."))

    # ── about ───────────────────────────────────────────────────────────
    body = f"""<main><div class="shell" style="padding-top:44px">
  <article class="doc">
    <div class="phead">
      <span class="pid">ABOUT</span>
      <h1>Why this site exists</h1>
    </div>
    <p>I'm {site['owner']}, I'm 13, and I live near {site['location']}. I want to be an
    engineer on a Formula 1 team.</p>
    <p>Lots of people say that. The difference I'm trying to build is evidence. Every
    project on this site has a problem, a prediction I wrote down <em>before</em> I had
    data, what actually happened, what broke, and what I changed. Where I got something
    wrong, it's still here — those are usually the interesting ones.</p>

    <h2>How it works</h2>
    <p>The program runs in seasons of thirteen weeks. Three sessions a week: design on
    Tuesday, build and test on Thursday, and a short review on Saturday. Every session
    has to end with at least one number I calculated myself. A session that produces no
    number didn't really happen.</p>

    <h2>The rules I test by</h2>
    <ul>
      <li>Write the prediction down first, with units.</li>
      <li>Change one thing at a time.</li>
      <li>Three trials minimum, five is better.</li>
      <li>Record what I <em>didn't</em> change, not just what I did.</li>
      <li><strong>If the error bars overlap, I haven't proved anything.</strong> Saying so
      is a result, not a failure.</li>
      <li>Re-run the baseline at the end. If it moved, the session is suspect.</li>
    </ul>

    <h2>Where this goes</h2>
    <p>Charlotte is an unusually good place to be doing this — the motorsports industry
    is concentrated here, UNC Charlotte runs a Formula SAE team about half an hour away,
    and GM's motorsports engineering presence is tied to Cadillac's F1 programme.</p>
    <p>Season 1 is design and build. Season 2 is data and telemetry. Season 3 is vehicle
    development on an RC test bed. Season 4 is competition and a public body of work.</p>

    <h2>Colophon</h2>
    <p>This site is generated from plain text files in a public git repository. Nothing
    is stored in a database and nothing can silently disappear — the commit history is
    part of the record.</p>
  </article>
</div></main>"""
    write("about/index.html", page(site, "About", body, "/about/",
                                   "Why LJ RaceLab exists and how the program works."))

    # ── sitemap + robots ────────────────────────────────────────────────
    urls = ["/", "/garage/", "/journal/", "/progress/", "/about/"]
    urls += [f"/projects/{p['_slug']}/" for p in projects]
    urls += [f"/journal/{j['_slug']}/" for j in journal]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>https://{site['domain']}{u}</loc></url>\n" for u in urls)
          + "</urlset>\n")
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: https://{site['domain']}/sitemap.xml\n")

    print(f"built {len(urls)} pages into docs/")
    print(f"  projects {len(projects)} ({done_projects} complete)")
    print(f"  journal  {len(journal)}")
    print(f"  weeks    {done_weeks}/{site['season_weeks']} complete, {hours} h logged")
    print(f"  CNAME    {cname}")


def entry_row(j):
    excerpt = re.sub(r"<[^>]+>", " ", j["_body"])
    excerpt = re.sub(r"\s+", " ", excerpt).strip()[:150]
    return f"""<a class="entry" href="/journal/{j['_slug']}/">
  <span class="d">{nice_date(j['date'])}<br>Week {j.get('week','—')}</span>
  <span><h3>{j['title']}</h3><p>{excerpt}…</p></span>
</a>"""


def serve(port=8000):
    """python build.py --serve  → look at the site before pushing it."""
    import http.server, socketserver, functools, webbrowser
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(DOCS))
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/"
        print(f"\nServing the site at {url}   (Ctrl+C to stop)")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        try:
            serve()
        except KeyboardInterrupt:
            print("\nstopped.")
