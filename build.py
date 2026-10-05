#!/usr/bin/env python3
"""GLM Omnimedia News — static site generator.

Reads stories.json and generates:
  index.html            homepage (hero + latest grid + topic sections + sidebar)
  stories/<slug>.html   individual story pages
  robots.txt
  sitemap.xml

No dependencies beyond the Python standard library. Run:  python3 build.py
"""
import html
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# Update this to the real Vercel URL after the first deploy (used in sitemap.xml).
SITE_URL = "https://thetorchleader.github.io/GLMOmnimedianews"
SITE_NAME = "GLM Omnimedia News"
TAGLINE = "Biblical News for the Global Church"

NAV_SECTIONS = [
    "Latest",
    "Church & Ministry",
    "Religious Liberty",
    "World",
    "Culture & Family",
    "Theology",
    "Missions",
]

FLAME_SVG = (
    '<svg class="flame" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#c19a3f" d="M12.6 2.2c.9 3.9-4.1 5-4.1 9.2a4.9 4.9 0 0 0 9.8 0c0-1.9-.9-2.9-.9-2.9s1.9 1.1 1.9 3.9a7.3 7.3 0 1 1-14.6 0C4.7 7.6 9.9 6.2 12.6 2.2z"/>'
    '<path fill="#7a5a1d" d="M12.5 22.5a3.1 3.1 0 0 1-3.1-3.1c0-2.4 3.1-3.1 3.1-5.7 1.7 1.9 3.1 3 3.1 5.7a3.1 3.1 0 0 1-3.1 3.1z"/>'
    "</svg>"
)

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E"
    "%3Cpath fill='%23c19a3f' d='M12.6 2.2c.9 3.9-4.1 5-4.1 9.2a4.9 4.9 0 0 0 9.8 0c0-1.9-.9-2.9-.9-2.9s1.9 1.1 1.9 3.9a7.3 7.3 0 1 1-14.6 0C4.7 7.6 9.9 6.2 12.6 2.2z'/%3E"
    "%3C/svg%3E"
)

FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Playfair+Display:wght@600;700;800&"
    "family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&"
    "family=Source+Sans+3:wght@400;600;700&display=swap"
)


def esc(text):
    return html.escape(text or "", quote=True)


def img_url(image, prefix=""):
    """Return the image URL, prefixing only relative paths."""
    image = image or ""
    if image.startswith(("http://", "https://", "data:")):
        return image
    return prefix + image


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fmt_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %d, %Y").replace(" 0", " ")


def load_stories():
    with open(os.path.join(ROOT, "stories.json"), encoding="utf-8") as f:
        stories = json.load(f)
    stories.sort(key=lambda s: s["published_at"], reverse=True)
    return stories


def head(title, description, prefix):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {esc(SITE_NAME)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS_URL}" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>
<body>
"""


def utility_bar():
    return f"""<div class="utility-bar">
  <div class="container">
    <span class="soli">Soli Deo Gloria</span>
    <span class="dateline" id="today-date"></span>
    <span class="tagline-mini">{esc(TAGLINE)}</span>
  </div>
</div>
"""


def masthead(prefix):
    return f"""<header class="masthead">
  <a class="brandmark" href="{prefix}index.html" aria-label="{esc(SITE_NAME)} home">
    {FLAME_SVG}
    <h1>{esc(SITE_NAME)}</h1>
  </a>
  <p class="tagline">{esc(TAGLINE)}</p>
</header>
"""


def nav(prefix, current="home"):
    items = []
    for section in NAV_SECTIONS:
        anchor = "latest" if section == "Latest" else slugify(section)
        href = f"{prefix}index.html#{anchor}" if current != "home" else f"#{anchor}"
        items.append(f'<li><a href="{href}">{esc(section)}</a></li>')
    return "<nav class=\"main-nav\" aria-label=\"Sections\"><ul>\n" + "\n".join(items) + "\n</ul></nav>\n"


def footer(prefix):
    cat_links = "\n".join(
        f'<li><a href="{prefix}index.html#{slugify(s) if s != "Latest" else "latest"}">{esc(s)}</a></li>'
        for s in NAV_SECTIONS
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>{esc(SITE_NAME)}</h4>
        <p>{esc(SITE_NAME)} is the news arm of GLM Omnimedia — serving the global Church with truthful, uncompromising journalism evaluated through a biblical lens. We report the news the mainstream will not, and we measure every story against the unchanging Word of God.</p>
      </div>
      <div>
        <h4>Sections</h4>
        <ul class="footer-links">
{cat_links}
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul class="footer-links">
          <li><a href="{prefix}index.html#about">Our Mission</a></li>
          <li><a href="{prefix}index.html">Latest Stories</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 {esc(SITE_NAME)}. All rights reserved.</span>
      <span class="soli">Soli Deo Gloria</span>
    </div>
  </div>
</footer>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def badge(category):
    return f'<span class="badge {slugify(category)}">{esc(category)}</span>'


def story_url(story, prefix=""):
    return f"{prefix}stories/{story['slug']}.html"


def card(story, prefix=""):
    breaking = '<span class="badge breaking">Breaking</span>' if story.get("breaking") else ""
    return f"""<article class="card">
  <a class="thumb" href="{story_url(story, prefix)}" aria-label="{esc(story['title'])}">
    <img src="{esc(img_url(story['image'], prefix))}" alt="{esc(story['title'])}" loading="lazy">
  </a>
  <div class="card-body">
    {breaking}{badge(story['category'])}
    <h3><a href="{story_url(story, prefix)}">{esc(story['title'])}</a></h3>
    <p class="summary">{esc(story['summary'])}</p>
    <div class="meta">
      <span>{fmt_date(story['published_at'])}</span>
      <span>Source: <a href="{esc(story['source_url'])}" rel="noopener" target="_blank">{esc(story['source_name'])}</a></span>
    </div>
  </div>
</article>
"""


def sidebar(stories, prefix=""):
    most_read = "\n".join(
        f'<li><a href="{story_url(s, prefix)}">{esc(s["title"])}</a></li>'
        for s in stories[:5]
    )
    return f"""<aside class="sidebar">
  <div class="widget">
    <h3>Most Read</h3>
    <ol class="most-read">
{most_read}
    </ol>
  </div>
  <div class="widget" id="about">
    <h3>About GLM Omnimedia</h3>
    <p>{esc(SITE_NAME)} is the umbrella news and publishing ministry of GLM Omnimedia — biblical evangelical journalism for the Christian community worldwide. Every story is reported truthfully and weighed against Scripture.</p>
  </div>
  <div class="widget">
    <h3>Verse of the Day</h3>
    <p class="verse-text" id="verse-text"></p>
    <span class="verse-ref" id="verse-ref"></span>
  </div>
</aside>
"""


def build_index(stories):
    # Breaking stories pin to the top, then newest first.
    stories = sorted(stories, key=lambda s: (bool(s.get("breaking")), s["published_at"]), reverse=True)
    hero = stories[0]
    hero_html = f"""<section class="hero" aria-label="Featured story">
  <div class="hero-card">
    <a class="hero-img" href="{story_url(hero)}" aria-label="{esc(hero['title'])}">
      <img src="{esc(hero['image'])}" alt="{esc(hero['title'])}">
    </a>
    <div class="hero-text">
      {badge(hero['category'])}
      <h2><a href="{story_url(hero)}">{esc(hero['title'])}</a></h2>
      <p class="summary">{esc(hero['summary'])}</p>
      <div class="meta">
        <span class="byline">By {esc(SITE_NAME)}</span>
        <span>{fmt_date(hero['published_at'])}</span>
        <span>Source: <a href="{esc(hero['source_url'])}" rel="noopener" target="_blank">{esc(hero['source_name'])}</a></span>
      </div>
    </div>
  </div>
</section>
"""

    latest_cards = "\n".join(card(s) for s in stories)
    latest_html = f"""<section id="latest" aria-label="Latest stories">
  <h2 class="section-title">Latest Stories <span class="count">{len(stories)} stor{"ies" if len(stories) != 1 else "y"}</span></h2>
  <div class="card-grid">
{latest_cards}
  </div>
</section>
"""

    topic_sections = []
    for section in NAV_SECTIONS[1:]:
        items = [s for s in stories if s["category"] == section]
        if items:
            lis = "\n".join(
                f"""<li>
      {badge(s['category'])}
      <h4><a href="{story_url(s)}">{esc(s['title'])}</a></h4>
      <div class="meta"><span>{fmt_date(s['published_at'])}</span>
      <span>Source: <a href="{esc(s['source_url'])}" rel="noopener" target="_blank">{esc(s['source_name'])}</a></span></div>
    </li>"""
                for s in items
            )
            list_html = f"<ul class=\"topic-list\">\n{lis}\n  </ul>"
        else:
            list_html = (
                f"<p class=\"coming-soon\">More {esc(section)} stories are on the way "
                "— check back soon.</p>"
            )
        topic_sections.append(
            f"""<section class="topic-row" id="{slugify(section)}" aria-label="{esc(section)}">
  <h2 class="section-title">{esc(section)}</h2>
  {list_html}
</section>"""
        )

    body = (
        head(f"{SITE_NAME} — {TAGLINE}", f"{SITE_NAME}: {TAGLINE}. Biblical evangelical news for the global Church.", "")
        + utility_bar()
        + masthead("")
        + nav("", current="home")
        + '<main class="container">\n'
        + hero_html
        + '<div class="content-grid">\n<div class="primary">\n'
        + latest_html
        + "\n".join(topic_sections)
        + "\n</div>\n"
        + sidebar(stories)
        + "\n</div>\n</main>\n"
        + footer("")
    )
    return body


def build_story_page(story, stories):
    idx = stories.index(story)
    newer = stories[idx - 1] if idx > 0 else None
    older = stories[idx + 1] if idx < len(stories) - 1 else None

    commentary_html = ""
    if story.get("commentary"):
        commentary_html = f"""<aside class="commentary-box" aria-label="Commentary">
  <p class="who">Daniel Whyte III on this story</p>
  <p>{esc(story['commentary'])}</p>
</aside>
"""

    nav_links = [f'<a class="btn ghost" href="../index.html">&larr; Back to Home</a>']
    if older:
        nav_links.append(f'<a class="btn" href="{older["slug"]}.html">Older Story &rarr;</a>')
    if newer:
        nav_links.insert(0, f'<a class="btn" href="{newer["slug"]}.html">&larr; Newer Story</a>')

    body = (
        head(story["title"], story["summary"], "../")
        + utility_bar()
        + masthead("../")
        + nav("../", current="story")
        + f"""<main>
<article class="story-wrap">
  <p class="breadcrumb"><a href="../index.html">Home</a> &rsaquo; {esc(story['category'])} &rsaquo; {esc(story['title'][:60])}&hellip;</p>
  <header class="story-head">
    {badge(story['category'])}
    <h1>{esc(story['title'])}</h1>
    <div class="meta">
      <span class="byline">By {esc(SITE_NAME)}</span>
      <span>{fmt_date(story['published_at'])}</span>
      <span>Source: <a href="{esc(story['source_url'])}" rel="noopener" target="_blank">{esc(story['source_name'])}</a></span>
    </div>
  </header>
  <figure class="story-figure">
    <img src="{esc(img_url(story['image'], '../'))}" alt="{esc(story['title'])}">
    <figcaption>{esc(story['image_credit'])}</figcaption>
  </figure>
{commentary_html}  <div class="story-body">
{story['body_html']}
  </div>
  <aside class="takeaway-box" aria-label="Biblical worldview takeaway">
    <p class="label">Biblical Worldview Takeaway</p>
    <p>{esc(story['takeaway'])}</p>
  </aside>
  <p class="source-line">Read the original at <a href="{esc(story['source_url'])}" rel="noopener" target="_blank">{esc(story['source_name'])}</a>.</p>
  <nav class="story-nav" aria-label="Story navigation">
    {"".join(nav_links)}
  </nav>
</article>
</main>
"""
        + footer("../")
    )
    return body


def build_sitemap(stories):
    urls = [f"  <url><loc>{SITE_URL}/</loc><lastmod>{stories[0]['published_at']}</lastmod></url>"]
    for s in stories:
        urls.append(
            f"  <url><loc>{SITE_URL}/stories/{s['slug']}.html</loc>"
            f"<lastmod>{s['published_at']}</lastmod></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"


def write(path, content):
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    stories = load_stories()
    if not stories:
        raise SystemExit("stories.json is empty — nothing to build.")

    write(os.path.join(ROOT, "index.html"), build_index(stories))
    for story in stories:
        write(
            os.path.join(ROOT, "stories", story["slug"] + ".html"),
            build_story_page(story, stories),
        )
    write(os.path.join(ROOT, "robots.txt"), build_robots())
    write(os.path.join(ROOT, "sitemap.xml"), build_sitemap(stories))

    print(f"Built {SITE_NAME}:")
    print(f"  index.html")
    for s in stories:
        print(f"  stories/{s['slug']}.html")
    print("  robots.txt, sitemap.xml")
    print(f"  {len(stories)} stories total.")


if __name__ == "__main__":
    main()
