# GLM Omnimedia News

**Biblical News for the Global Church — Soli Deo Gloria**

A pure static Christian news aggregation website: HTML + CSS + JavaScript only.
No build step, no frameworks, no npm, no database. It deploys to Vercel as-is
for **$0**.

## How it works

All stories live in one data file: **`stories.json`**.
The Python script **`build.py`** reads it and generates:

- `index.html` — homepage (hero story, Latest Stories grid, topic sections, sidebar)
- `stories/<slug>.html` — one page per story
- `robots.txt` and `sitemap.xml`

To publish or update anything, you edit `stories.json` (or append a new story
object to it) and re-run the generator. Vercel redeploys automatically on
every `git push`.

## Local preview

```bash
cd glmomnimedianews
python3 build.py
python3 -m http.server 8000
# open http://localhost:8000
```

## Adding a story

1. Add a new object to the array in `stories.json` (see schema below).
2. Place the story image under `images/` (JPG/PNG/WebP; ~1200px wide is ideal).
3. Run `python3 build.py`.
4. `git add -A && git commit -m "Add: <headline>" && git push` — Vercel deploys.

### stories.json schema

| Field          | Required | Description                                                        |
|----------------|----------|--------------------------------------------------------------------|
| `slug`         | yes      | URL-safe id, e.g. `marvin-winans-nonprofit-pay-questions`          |
| `title`        | yes      | Full headline                                                      |
| `category`     | yes      | One of: Latest*, Church & Ministry, Religious Liberty, World, Culture & Family, Theology, Missions (*Latest is auto-generated; don't use it as a category) |
| `summary`      | yes      | 2–3 sentence summary shown on cards                                |
| `body_html`    | yes      | Full article as HTML paragraphs (`<p>…</p>`)                       |
| `commentary`   | no       | Daniel Whyte III quote (renders a highlighted commentary box); `null` if none |
| `takeaway`     | yes      | Biblical Worldview Takeaway box text                               |
| `source_name`  | yes      | Original outlet, e.g. `The Center Square`                          |
| `source_url`   | yes      | Link to the original article                                       |
| `image`        | yes      | Path under `images/`, e.g. `images/winans-editorial.jpg`           |
| `image_credit` | yes      | Credit line shown under the image                                  |
| `published_at` | yes      | ISO date, e.g. `2026-10-04` (always shown as a fixed date)         |

## Deploy to Vercel ($0)

1. Create a repo on GitHub (e.g. `glmomnimedianews`) and push this folder:
   ```bash
   git init && git add -A && git commit -m "Launch GLM Omnimedia News" 
   git branch -M main && git remote add origin https://github.com/<you>/glmomnimedianews.git
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com) → **Add New… → Project** → **Import** the repo.
3. Framework Preset: **Other**. Build Command: *(leave empty)*. Output Directory: *(leave empty / `.`)*.
4. Click **Deploy**. Done — free tier, custom domain optional later.
5. After deploy, update `SITE_URL` at the top of `build.py` to the real URL
   (e.g. `https://glmomnimedianews.vercel.app`), re-run `python3 build.py`,
   commit, and push so `sitemap.xml` carries the correct domain.

## Project layout

```
glmomnimedianews/
├── stories.json          # ALL story data — edit this to publish
├── build.py              # static site generator (stdlib only)
├── index.html            # generated homepage (commit it)
├── stories/              # generated story pages (commit them)
├── assets/css/style.css  # original editorial design
├── assets/js/main.js     # live date + verse-of-the-day (client side)
├── images/               # story images (committed)
├── robots.txt            # generated
├── sitemap.xml           # generated
├── vercel.json           # static deploy config
├── README.md
└── PIPELINE.md           # the 4x-daily auto-posting workflow
```

## Design notes

Editorial structure (masthead, section nav, hero, grids, sidebar, footer) is
modeled on the conventions of Christianity Today; every visual element, word,
and pixel of this design is original. Headlines: Playfair Display. Body:
Source Serif 4. UI: Source Sans 3 (all free Google Fonts).

**Standing rules:** fixed publication dates only (never "x hours ago");
every story links its original source; images are licensed or original with
credit lines — never hotlinked, never AI-faked photos of real people.
