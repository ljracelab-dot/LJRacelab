# ljracelab.com

The LJ RaceLab engineering portfolio. Season 1: **Design & Build**, 1 Sep – 5 Dec 2026.

Everything on the site is generated from plain text files in this repository. There is
no database and no server. **The commit history of this repo is part of the portfolio** —
it shows when the work actually happened, which is exactly what a Formula SAE team lead
or an admissions reader wants to see.

---

## Adding something to the site

### The easy way — use the tool

Open **`tools/new-entry.html`** in a browser. Fill in the form, click *Copy the text* or
*Download the file*, and save it where the tool tells you. You never touch HTML and you
never have to remember the format.

### Then, every time

```
python build.py
```

Then open **GitHub Desktop**, write one line saying what you did, and click
**Commit** → **Push**. The site updates in about a minute.

To look at it before pushing:

```
python build.py --serve
```

---

## Where things live

```
content/
  site.json            mission, season dates, resource links
  weeks.json           the 13-week roadmap and each week's status
  skills.json          the skill matrix (levels 0–5)
  projects/*.md        one file per project
  journal/*.md         one file per logbook entry
assets/                photos — reference them as /assets/whatever.jpg
docs/                  THE BUILT SITE. Generated. Don't hand-edit it.
tools/new-entry.html   the form that writes entry files for you
build.py               the generator
```

**Never edit anything inside `docs/`.** It gets wiped and rebuilt every time. Edit
`content/` and run the build.

## Photos

Drop image files into `assets/`. In a project's front matter:

```
hero: assets/004-hero.jpg
```

Inside the writing, anywhere:

```
![The break at the inside corner](/assets/004-break.jpg)
```

Take photos **while the part is still on the bench**. Everyone forgets afterwards, and
an undocumented project is, for portfolio purposes, one that didn't happen.

## Marking progress

Two files drive the numbers on the home page, and they are the only bookkeeping:

- **`content/weeks.json`** — change a week's `status` to `complete`. Weeks complete and
  engineering hours update themselves.
- **`content/projects/*.md`** — change `status:` to `in-progress` or `complete`.

Nothing is typed in twice. If a number on the site is wrong, the fix is in `content/`.

## Updating the skill matrix

`content/skills.json`, at each 30-day checkpoint. Be honest — the point of the matrix is
that it moves, and a matrix that starts at 5 has nowhere to go.

## Deploying

See **DEPLOY.md**. Short version: GitHub Pages serves the `docs/` folder on `main`, and
GoDaddy points `ljracelab.com` at GitHub with four A records.

## If something breaks

Nothing is ever lost — every version of every file is in the git history. In GitHub
Desktop, **History** shows every commit and you can revert any one of them.
