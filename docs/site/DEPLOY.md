# Putting LJ RaceLab live at ljracelab.com

**Who this is for:** Justin — a parent who is not a developer — working with LJ (13).
**What you end up with:** `https://ljracelab.com` serving LJ's portfolio, free forever, with every change he has ever made preserved as a dated record.
**Total hands-on time:** about 2 hours, plus waiting. Best split into two sittings — Steps 1–7 one evening, Steps 8–10 the next.

---

## What we are building, in one picture

```
LJ's computer                GitHub (github.com)              GoDaddy
─────────────                ───────────────────              ───────
edit a file                                                   ljracelab.com
      ↓                                                            ↓
python build.py   ──push──>  repository "ljracelab"   <──DNS──  points here
  writes /docs                  /docs folder is
                                served as the website
```

Three moving parts. GoDaddy owns the name. GitHub stores the files and serves them. LJ's computer builds the pages.

### Six words each, for the words that follow

- **Repository (repo)** — a folder GitHub stores and versions.
- **Commit** — one saved snapshot with a message.
- **Push** — send your saved snapshots to GitHub.
- **Branch** — one line of history; ours is `main`.
- **GitHub Pages** — GitHub's free website hosting service.
- **DNS** — the phonebook mapping names to servers.
- **A record** — DNS entry pointing a name at IP.
- **CNAME record** — DNS entry pointing a name at another name.
- **TTL** — how long others cache this record.
- **Apex domain** — the bare name, no `www`.
- **Propagation** — the wait while the world notices.

---

## Why this setup (settled — do not relitigate)

The commit history *is* the portfolio. A database would store LJ's work; a repository stores his work **and a timestamped, public record of him doing it** — five years of "here is what I built, here is the week I built it." That was the deciding factor over Supabase or Firebase, and it is the reason the repo is **public**.

We serve from a folder of already-built files, with no automated build step on GitHub's side. Nothing can break server-side, and there is no build quota to run out of.

### The limits we are working inside (verified against GitHub's own docs, August 2026)

| Limit | Number | Does this matter to us? |
|---|---|---|
| Source repository size | 1 GB (recommended) | No. Text and images. You would need thousands of photos. |
| Published site size | 1 GB (hard maximum) | No. Same reason. |
| Bandwidth | 100 GB per month (soft) | No. That is roughly a million page views of a site like this. |
| Builds | 10 per hour (soft) | Effectively no — see below. |
| Repo visibility on the free plan | Pages works on **public** repos only | Ours is public on purpose. |

"Soft" means GitHub emails you and asks you to slow down rather than switching you off.

**On the 10-builds-per-hour limit:** it is per hour, and it resets. LJ pushing twice while fixing a typo is fine. Pushing eleven times in forty minutes during a frustrated debugging session would get him a warning, not a ban. Wait an hour and continue.

---

## Step 1 — The GitHub accounts (25 minutes)

### The age question, answered directly

GitHub's Terms of Service say: **"You must be age 13 or older."** GitHub does not permit anyone under 13 and terminates under-13 accounts when it finds them. There is no parental-consent exception and no supervised-child account type.

**LJ is 13. He is eligible for his own GitHub account, in his own name, today.** No workaround needed.

### The arrangement to use

Create **two** accounts:

| Account | Owner | Role |
|---|---|---|
| Justin's account | You | **Owns the repository.** Holds recovery. Never used day to day. |
| LJ's account | LJ | Added as a **collaborator**. Does all the actual work. |

**Why this and not one shared account:**

1. **The commits carry LJ's username.** That is the whole point of choosing a repo. If everything commits under "dad," the portfolio evidence says dad built it. Two accounts costs you twenty extra minutes once and buys five years of correctly-attributed history.
2. **A 13-year-old should not be the only recovery path** for five years of irreplaceable work. Lost password, lost phone with the 2FA app, a support ticket that needs an adult — you want to be the account of record.
3. **It transfers cleanly.** When LJ is 16 or 18, Settings → Transfer ownership moves the repo to his account in about ninety seconds. The history comes with it, unchanged.

*(If you genuinely only want one account: use LJ's, with you holding the recovery codes. You lose nothing technical. You lose the ability to help him if he is locked out.)*

### Do it

1. Go to **github.com** → **Sign up**. Create **your** account first, with your email. Free plan. Skip every upsell.
2. **Settings → Password and authentication → Enable two-factor authentication.** Use an authenticator app. **Print the recovery codes and put them in a physical drawer.** Not a screenshot on a phone.
3. Sign out. Create **LJ's** account with a second email (a Gmail alias like `yourname+lj@gmail.com` works and lands in your inbox).
4. Choose LJ's username carefully — **it appears on every commit for the next five years and is part of a public URL.** `ljracelab` is a good choice. Avoid a full real name, a birth year, or a school name.
5. Turn on 2FA for LJ's account too. Same drawer, same printout.
6. On **both** accounts: **Settings → Emails →** tick **"Keep my email address private."** Note the `@users.noreply.github.com` address it shows you — this stops your real email being visible in the public commit history.

✅ **Check:** Sign out and back in to both accounts using 2FA. If you cannot get in now, you will not get in in 2031.

⏱ *If setting up 2FA on two accounts is a bridge too far tonight, do LJ's account fully and come back for yours. But do come back.*

---

## Step 2 — Install GitHub Desktop (15 minutes)

**Use GitHub Desktop.** It is a normal app with buttons. This family should not be learning the git command line in week one — that is a separate hobby, and it can wait until LJ actually wants it.

1. Go to **desktop.github.com** → Download for Windows or macOS.
2. Install it and open it.
3. **Sign in with LJ's account** (the collaborator, the one that should be making commits).
4. When it asks for a name and email, use LJ's name and the `@users.noreply.github.com` address from Step 1.6.

GitHub Desktop installs git underneath itself, so there is nothing else to install.

You also need **Python**, because the site is built by `build.py`. If `python --version` in a terminal prints a version number, you already have it. If not: **python.org → Downloads**, and on Windows **tick "Add Python to PATH"** on the first install screen. Missing that tickbox is the single most common Python install problem.

<details>
<summary><strong>If you prefer the terminal</strong></summary>

```bash
# macOS: git ships with Xcode command line tools
xcode-select --install

# Windows: winget install --id Git.Git
# Linux:   sudo apt install git

git config --global user.name "LJ"
git config --global user.email "12345678+ljracelab@users.noreply.github.com"
```
Everything in this guide that says "in GitHub Desktop" has a two-command equivalent, given in the asides below. You can mix freely — Desktop and the terminal are the same thing with different faces.
</details>

---

## Step 3 — Create the repository and push the site (25 minutes)

1. Signed in as **Justin**, go to **github.com/new**.
2. **Repository name:** `ljracelab`
3. **Description:** something plain — "LJ RaceLab — engineering portfolio."
4. **Public.** Required for free GitHub Pages, and it is the point of the project.
5. Leave "Add a README" **unticked**. We are pushing existing files.
6. Click **Create repository**.
7. Still as Justin: **Settings → Collaborators → Add people →** add **LJ's** username. LJ gets an email; he must accept it.

Now put the files in:

8. Open **GitHub Desktop** (signed in as LJ). **File → Clone repository → URL →** paste `https://github.com/JUSTINSUSERNAME/ljracelab` and choose a local folder. This creates an empty folder on the computer that is linked to GitHub.
9. Copy the entire site project — including `build.py` and everything it needs — **into that folder**.
10. Run the build once so `/docs` exists and is current:
    ```
    python build.py
    ```
11. Back in GitHub Desktop, the left panel now lists every file. In the bottom-left box type a commit message: `First version of the site`. Click **Commit to main**.
12. Click **Push origin** at the top.

✅ **Check:** Reload the repo page on github.com. You should see your files, and a **`docs`** folder among them. Click into `docs` — there must be an **`index.html`** directly inside it. If `index.html` is one level deeper (`docs/site/index.html`), fix `build.py`'s output path now; Pages will not find it otherwise.

<details>
<summary><strong>If you prefer the terminal</strong></summary>

```bash
git clone https://github.com/JUSTINSUSERNAME/ljracelab
cd ljracelab
# copy files in, then:
python build.py
git add -A
git commit -m "First version of the site"
git push
```
</details>

---

## Step 4 — Turn on GitHub Pages (5 minutes)

1. On the repo page: **Settings** (top row) → **Pages** (left sidebar).
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Two dropdowns appear. Set them to **`main`** and **`/docs`**.
4. Click **Save**.

Wait about a minute, then reload the Settings → Pages screen. A green banner appears with a URL like `https://justinsusername.github.io/ljracelab/`.

✅ **Check:** Open that URL. The site should load — possibly with broken styling or images if the site's links assume it lives at the root of a domain. **That is expected and it fixes itself** in Step 5 when the custom domain takes over. Do not go hunting for the CSS bug. Just confirm you get LJ's page and not a 404.

⏱ *First publish is usually under a minute but can take up to ten. Reload rather than re-saving.*

---

## Step 5 — Set the custom domain (5 minutes)

Do this **before** touching GoDaddy. GitHub needs to know the name is coming.

1. **Settings → Pages → Custom domain.**
2. Type exactly: `ljracelab.com` — no `https://`, no `www`, no trailing slash.
3. Click **Save**.

GitHub immediately makes a commit on `main` that adds a file called **`CNAME`** inside your publishing source — so for us, **`docs/CNAME`**. It contains one line: `ljracelab.com`. That file is what tells GitHub's servers which domain belongs to this repo.

4. You will see a red "DNS check unsuccessful" message. **That is correct right now** — GoDaddy has not been told anything yet. Ignore it until Step 7.
5. In GitHub Desktop, click **Fetch origin**, then **Pull origin**. This brings GitHub's new `CNAME` commit down to the computer. **Do not skip this** — if LJ's next build pushes without it, the domain unsets itself. (Full explanation in Step 6.)

<details>
<summary><strong>If you prefer the terminal</strong></summary>

```bash
git pull
```
</details>

---

## Step 6 — One-time check on `build.py` (10 minutes, and it saves you an evening later)

This is the single most common way a setup like this breaks, so spend ten minutes now.

**The problem:** if `build.py` wipes the `docs` folder clean before regenerating it, it deletes `docs/CNAME` along with everything else. LJ pushes. GitHub sees the CNAME file is gone and concludes you no longer want the custom domain — so it **clears the Custom domain box in Settings** and the site drops offline. This looks like GitHub "randomly forgetting" your domain, and it will happen every single time until the underlying cause is fixed.

**Two ways to fix it. Pick one:**

**(a) The simple one — never delete `docs/`.** If `build.py` only overwrites files rather than emptying the folder first, `docs/CNAME` survives untouched. Nothing to do.

**(b) The reliable one — have `build.py` write the file itself.** Add this at the end of `build.py`, after `docs` has been written:

```python
from pathlib import Path
Path("docs/CNAME").write_text("ljracelab.com\n")
```

Two lines, and the domain can never be lost by a build again. If you are unsure which case you are in, add the two lines anyway — they are harmless if the file already exists.

✅ **Check:** run `python build.py`, then confirm `docs/CNAME` still exists and still says `ljracelab.com`.

---

## Step 7 — The GoDaddy DNS changes (25 minutes, then waiting)

Nothing is bought here. No GoDaddy plan changes. The nameservers stay at GoDaddy — that is precisely why we chose GitHub Pages over hosts that demand you move them.

### 7a. Get to the right screen

1. Sign in at **godaddy.com**.
2. Go to your **Domain Portfolio** (in the account menu — older accounts may still say "My Products").
3. Click **ljracelab.com** to open **Domain Settings**.
4. Click the **DNS** tab. You are now looking at the DNS records list.

### 7b. Turn off Forwarding first — this is the step people miss

On the DNS screen there is a **Forwarding** section. **Check it before anything else.**

GoDaddy's own documentation is explicit: *"Adding forwarding will automatically update and lock your @ A record."* If forwarding is on, you **cannot edit or delete the apex A record** — the option is simply greyed out or your change silently reverts, with no useful error message. People lose an hour here.

If any forwarding is configured, **remove it** before continuing.

### 7c. Delete the records that will fight you

Look through the record list and **delete**:

- Any **A** record with Name **`@`**. On a domain that has never hosted anything this points at a GoDaddy parking page — commonly **`3.33.130.190`** or **`15.197.148.33`**, or on older domains something starting `50.63.202.` or `3.33.152.` / `15.197.142.`. Whatever the value, delete it. There must be **no** leftover apex A records other than the four we are about to add.
- Any **A** record with Name **`*`** (a wildcard, catching every subdomain), if present.
- Any existing **CNAME** with Name **`www`** — GoDaddy usually ships one pointing to `@`. Delete it; we are replacing it.

**Leave alone:** all **MX** records (that is email — deleting them breaks mail), **TXT** records, **NS** records, and the `_domainconnect` CNAME (harmless GoDaddy plumbing).

### 7d. Add the five records

Click **Add New Record** for each. Field names on this screen are **Type**, **Name**, **Value**, **TTL**.

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 1 hour |
| A | `@` | `185.199.109.153` | 1 hour |
| A | `@` | `185.199.110.153` | 1 hour |
| A | `@` | `185.199.111.153` | 1 hour |
| CNAME | `www` | `JUSTINSUSERNAME.github.io` | 1 hour |

Notes that matter:

- **`@` means the bare domain** — `ljracelab.com` with no prefix. GoDaddy uses this convention in the Name field. Do not type `ljracelab.com` there.
- **All four A records are correct and necessary.** Four entries with the same Name is not a mistake; they are GitHub's four edge servers. Some GoDaddy screens let you paste multiple IPs into one A record — either presentation is fine.
- **The CNAME value ends in `.github.io` and does NOT include the repository name.** `justinsusername.github.io` — not `justinsusername.github.io/ljracelab`. This trips up nearly everyone.
- **Use the repository owner's username** (Justin's), not LJ's — the CNAME points at the account that owns the repo.
- **TTL: leave it at GoDaddy's default of 1 hour.** A shorter TTL sounds appealing while you are waiting, but it does not speed up the *first* lookup and it means more DNS traffic forever. One hour is right.

Click **Save** (or **Save All Records**).

✅ **Check:** the DNS list shows exactly four `@` A records with the 185.199.x addresses, and one `www` CNAME. No other A records at all.

---

## Step 8 — Wait for DNS, and check it properly (10 minutes of work, up to 24 hours of waiting)

**Realistic timing:** most people see it working in **10 to 60 minutes**. GoDaddy says up to 48 hours and GitHub says up to 24; those are worst cases involving stubborn upstream caches. If it is not live after **two hours**, something is genuinely wrong — go to the troubleshooting table rather than waiting another day in hope.

### Checking it

On **macOS or Linux**, open Terminal:

```
dig ljracelab.com +short
```

**Success looks exactly like this** (order will vary — that is normal and irrelevant):

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Then check www:

```
dig www.ljracelab.com +short
```

**Success:**

```
justinsusername.github.io.
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

The first line being a name rather than a number is correct — that is the CNAME doing its job, and the four IPs beneath it are the answer it resolved to.

**Failure looks like:** nothing at all (records not visible yet — wait), or an IP that is not on the 185.199.x list (an old GoDaddy record survived — go back to Step 7c).

**On Windows**, `dig` is not installed. Use either:

```
nslookup ljracelab.com
```

(look for the four IPs under "Addresses"), or the simpler option — go to **whatsmydns.net**, enter `ljracelab.com`, choose **A**, and you get a world map of which servers have caught up. That map is genuinely the friendliest tool here, and it works on any machine.

### Then, back on GitHub

Reload **Settings → Pages**. The red "DNS check unsuccessful" should now be a green **"DNS check successful."** If it still shows red after DNS is clearly correct, click the ✏️ next to the custom domain, remove it, save, re-enter `ljracelab.com`, save. That forces a re-check.

✅ **Check:** `http://ljracelab.com` loads LJ's site in a browser. HTTPS may not work yet — that is Step 9.

---

## Step 9 — Enforce HTTPS (2 minutes of work, up to 24 hours of waiting)

HTTPS is the padlock in the address bar. GitHub provides the certificate free, but it has to request one from Let's Encrypt after your DNS is correct, and it cannot start until then.

1. **Settings → Pages.** Find the **Enforce HTTPS** tickbox.
2. If it is greyed out with "unavailable for your site" — **that is normal.** GitHub says this can take **up to 24 hours** after the custom domain is configured. Usually it is 15 minutes to an hour.
3. Come back later and **tick it.**

Once ticked, anyone typing `http://ljracelab.com` is automatically sent to `https://`. Leave it ticked forever.

⏱ *Do not repeatedly remove and re-add the custom domain trying to hurry this. Each removal restarts the certificate request. Set a reminder for tomorrow morning and walk away.*

✅ **Check:** `https://ljracelab.com` shows a padlock, and `https://www.ljracelab.com` redirects to it.

---

## Step 10 — The weekly routine

**This is the part you will use forty times. It is three things and it takes ninety seconds.**

1. LJ writes his journal entry or adds his project — editing the source files, however the project is set up.
2. He runs the build:
   ```
   python build.py
   ```
3. He opens **GitHub Desktop**. The changed files are listed on the left. He types a short message in the bottom-left box — *"Week 12 journal: brake bias testing"* — and clicks **Commit to main**.
4. He clicks **Push origin** at the top.

Done. The site updates in **under a minute**, usually about twenty seconds.

**That is the whole workflow.** Not a simplified version of it — that is genuinely all of it, every week, for the next five years.

A few things worth LJ knowing:

- **The commit message is part of the portfolio.** "Week 12 journal: brake bias testing" reads well to a future admissions officer or employer. "asdf" and "update" do not. It costs four seconds to write a real one.
- **Nothing he does here can break the site.** The worst case is that a page looks wrong, and Step 12 undoes it in two clicks.
- **If he forgets `python build.py`,** he will commit his source edits but the built pages will not change, so the live site stays the same. No harm — run the build and push again.
- **If GitHub Desktop shows no changes,** the build did not write anything. Usually that means he edited a file the build does not read, or saved it in the wrong folder.

<details>
<summary><strong>If you prefer the terminal</strong></summary>

```bash
python build.py
git add -A
git commit -m "Week 12 journal: brake bias testing"
git push
```
</details>

---

## Step 11 — Troubleshooting

| Symptom | What is actually happening | Fix |
|---|---|---|
| **Site shows 404** | GitHub cannot find `index.html` at the top of the publishing folder. Either Pages is pointed at the wrong branch/folder, or `build.py` writes `index.html` one level too deep. | Settings → Pages: confirm **`main`** + **`/docs`**. Then on github.com click into `docs` and confirm **`index.html`** is directly inside it, not in a subfolder. |
| **Site shows the README instead of the site** | There is no `index.html` in `docs/`, so Pages falls back to rendering `README.md` as the page. | Run `python build.py` and confirm it produced `docs/index.html`. Commit and push it. |
| **Custom domain keeps unsetting itself** | `build.py` deletes the `docs` folder each run, taking `docs/CNAME` with it. GitHub sees the file vanish and clears the domain setting. **This is the classic failure of this exact setup.** | Do Step 6. Either stop the build emptying `docs/`, or have it write `docs/CNAME` on every run. Then re-enter the domain in Settings → Pages once. |
| **Custom domain unset itself right after the first push** | Same cause, different trigger: GitHub's `CNAME` commit was never pulled down, so the next push from the computer overwrote history without it. | GitHub Desktop → **Fetch origin** → **Pull origin** *before* pushing. Then re-enter the domain. |
| **"Enforce HTTPS" is greyed out** | The certificate has not been issued yet. It cannot be issued until DNS is correct, and can take up to 24 hours after that. | Confirm DNS is right (Step 8), then wait. Do not re-add the domain repeatedly — that restarts the clock each time. |
| **HTTPS still unavailable after 48 hours** | Usually a **CAA record** at GoDaddy that does not permit Let's Encrypt. A CAA record lists who may issue certificates for your domain. | GoDaddy DNS: if any CAA records exist, either delete them all, or add one with value `letsencrypt.org`. If none exist, any issuer is allowed and this is not your problem. |
| **Changes pushed but site not updating** | Three usual causes, in order of likelihood. | (1) `python build.py` was not run — the source changed, `docs/` did not. (2) Browser cache — hard-reload with **Ctrl+Shift+R** / **Cmd+Shift+R**, or try a private window. (3) Push failed — check GitHub Desktop's top button doesn't still say "Push origin (1)". |
| **Site updated for LJ but not for you** | Browser or ISP caching an old copy. | Private window. If a private window shows the new version, it is cache and it clears itself within minutes. |
| **DNS not propagating after 2+ hours** | Almost always a leftover record fighting the new ones, or Forwarding still switched on and locking `@`. | GoDaddy → DNS → **Forwarding**: must be off. Then confirm there are exactly four `@` A records, all 185.199.x, no wildcard `*` A record, and one `www` CNAME ending `.github.io` with no repo name after it. |
| **Domain loads a GoDaddy parking page** | An old parking A record or a forwarding rule survived. | Step 7b and 7c again. Look specifically for `3.33.130.190`, `15.197.148.33`, or anything starting `50.63.202.`. |
| **`www.ljracelab.com` works, bare `ljracelab.com` does not** | The four A records are missing or wrong. The CNAME only handles `www`. | Re-add all four A records on `@` from the Step 7d table. |
| **Everything broke and nothing changed** | If it worked for months and then stopped — check the domain renewal date first. | GoDaddy → Domains → renewal date. **Turn on autorenew.** An expired domain is by far the most likely way to lose this site, and it has nothing to do with any technical choice here. |

---

## Step 12 — If it all goes wrong

**Start here: nothing is lost. Nothing has ever been lost.**

Every version of every file LJ has ever committed is stored permanently in the repository. Not the latest version — *all* of them, each with its date and message. Deleting a file, mangling a page, or pushing something broken does not destroy the previous version; it adds a new one on top. The old one sits underneath, intact, forever.

This is worth saying to LJ explicitly, once, and meaning it: **he cannot break this by experimenting.** That is the entire reason a repository was chosen.

### Undoing the last commit (GitHub Desktop, 30 seconds)

1. Open GitHub Desktop → **History** tab (top left).
2. Find the commit that caused the problem.
3. **Right-click it → Revert changes in commit.**
4. This creates a *new* commit that undoes it. Click **Push origin.**
5. The site is back to how it was, within a minute.

Reverting adds to history rather than erasing it — so the mistake, and the fix, are both on the record. That is the correct behaviour, and it is also honest.

### Going back further

1. **History** tab → click any older commit to see exactly what changed and when.
2. To recover one file as it was: on github.com, open the file → **History** → pick a version → **Raw** → copy the contents back over the current file.
3. For a serious mess, revert several commits one at a time, newest first.

### The panic checklist

If the site is down and you do not know why, in this order:

1. Is the domain still registered? (GoDaddy → renewal date)
2. Does `https://justinsusername.github.io/ljracelab/` load? If **yes**, the site is fine and it is a DNS problem. If **no**, it is a GitHub Pages problem.
3. Is the custom domain still filled in at Settings → Pages? If it emptied itself, go to Step 6.
4. Is `docs/index.html` on github.com?

Those four questions distinguish between every failure mode in the table above.

### The genuinely irrecoverable failure

There is exactly one: **losing both GitHub accounts** — password and 2FA device, on both, at once. That is why the recovery codes are printed and in a drawer. It is also why the repository can be cloned to a local folder that is itself backed up: GitHub Desktop already keeps a complete copy of everything on the computer, so a full local backup of that folder is a full backup of the project's entire history. Copy that folder to a drive or cloud folder once a term and the "irrecoverable" case stops existing.

---

## What this setup does not do

This is a **static site** — a set of finished pages served exactly as written. There is no login, no user accounts, no server-side code, no database, no comment section, no contact form that emails you, and no analytics unless you add them later. Nobody can sign in, submit anything, or store anything. Every visitor sees byte-for-byte the same pages LJ built on his laptop.

**That is the right trade here, and not a compromise.** A portfolio's job is to be readable, permanent, and fast — and a static site is the most durable form a website takes. There is no server to be patched, no database to corrupt, no dependency to go unmaintained, no monthly bill to lapse, and no free tier to be discontinued. A thirteen-year-old can understand the whole system in an afternoon, which means he can fix it himself, which means it will still be running when he is eighteen. Every feature we left out — accounts, comments, a backend — is a thing that could break unattended, cost money, expose a minor's data, or require a grown-up to maintain it. If LJ later wants a contact form, a third-party embed adds one in an afternoon without changing anything here. If he wants visitor stats, a privacy-respecting analytics snippet is one line in the template. Neither is needed to put five years of good work in front of the people who should see it.

---

## Quick reference

| | |
|---|---|
| Live site | `https://ljracelab.com` |
| GitHub fallback URL | `https://JUSTINSUSERNAME.github.io/ljracelab/` |
| Repo settings for Pages | Settings → Pages → Deploy from a branch → `main` / `/docs` |
| Domain file | `docs/CNAME`, containing one line: `ljracelab.com` |
| GoDaddy DNS | Domain Portfolio → ljracelab.com → DNS tab |
| Apex A records | 185.199.108.153 · 185.199.109.153 · 185.199.110.153 · 185.199.111.153 |
| www CNAME | `JUSTINSUSERNAME.github.io` |
| TTL | 1 hour (GoDaddy default) |
| Weekly routine | `python build.py` → commit → **Push origin** |
| Check DNS | `dig ljracelab.com +short` → the four 185.199.x IPs |

---

*Facts in this guide (GitHub Pages limits, GitHub's minimum age, GoDaddy's DNS screens and default TTL, GitHub's apex IP addresses) were verified against GitHub's and GoDaddy's own documentation in August 2026. If something on screen does not match what is written here, the vendor changed their UI — the shape of the task has not changed.*
