# GLM Omnimedia News — 4x-Daily Auto-Posting Pipeline

**Standing permission (granted 2026-10-04, GLM Omnimedia News ONLY):**
Muse may find, retitle, and rewrite Christian news stories and post them to
this site 4 times daily — **5:00 AM, 10:00 AM, 3:00 PM, 7:00 PM Central** —
without asking permission each time. This permission does NOT extend to
blackchristiannews.com or bcnn1.com (per-story approval still required there)
and does NOT include emailing any subscriber list.

## Source rotation

One story per run, rotating through sources so coverage stays fresh.
Keep a small rotation log (e.g. `pipeline-log.md`, git-committed) recording
`run time → source → story slug` so the next run picks the next source.

| #  | Source             | RSS endpoint (verified 2026-10-04)                              | Status      |
|----|--------------------|-----------------------------------------------------------------|-------------|
| 1  | Christian Post     | `https://www.christianpost.com/rss`                             | ✅ 200      |
| 2  | ChurchLeaders      | `https://churchleaders.com/feed`                                | ✅ 200      |
| 3  | Protestia          | `https://protestia.com/feed`                                    | ✅ 200      |
| 4  | Christianity Today | `https://www.christianitytoday.com/rss`                         | ✅ 200      |
| 5  | Charisma News      | `https://www.charismanews.com/feed`                             | ✅ 200      |
| 6  | CBN News           | `https://www1.cbn.com/cbnnews/feed`                             | ✅ 200      |
| 7  | Religion News (RNS)| `https://religionnews.com/feed`                                 | ⚠️ 403 to bots — check manually in browser if needed |
| 8  | Google News — Christianity | `https://news.google.com/rss/search?q=Christianity&hl=en-US&gl=US&ceid=US:en` | ✅ 200 (vary the query: `Christian persecution`, `church`, `religious liberty`) |
| 9  | MailOnline faith stories | *(no public RSS)* — use Google News query `site:dailymail.co.uk faith OR church OR Christian` or check manually | manual |

## Per-run steps (each scheduled run)

1. **Fetch** the newest items from the next source in the rotation
   (`curl` the RSS, or read the feed via the browser tools).
2. **Pick one** fresh, newsworthy story **not already in `stories.json`**
   (check by slug/URL). Prefer: church & ministry, religious liberty,
   missions, theology, family/culture, world Christianity.
3. **Read the full article** (browser fetch of the article URL).
4. **Rewrite**: new headline + full article in the theologically biblical
   biblical evangelical voice, with attribution ("according to…",
   "reported by…") and the original source linked. **Never copy the full
   text** — rewrite in your own words; short quotes with credit are fine.
5. **Image**: use a legally usable image with credit (Wikimedia Commons,
   outlet-provided, or original illustration). Never hotlink; never generate
   fake photos of real people. Save under `images/`.
6. **Append** the story object to `stories.json` (schema in README.md).
7. **Run** `python3 build.py`; verify `index.html` + the new story page exist
   and the image path resolves.
8. **Commit & push**: `git add -A && git commit -m "Auto: <slug> (<run time> CT)" && git push`
   — Vercel auto-deploys in ~1 minute.
9. **Log** the run in `pipeline-log.md`.

## Rewrite rules (every story, every time)

- **Factual first.** Report what the source actually says; link the original.
- **Allegation ≠ finding.** Distinguish accusations, investigations, and
  established findings explicitly ("is accused of…", "investigators allege…",
  "no formal charges have been filed"). Never present an accusation as fact.
- **Fairness.** Include the other side's response when the source reports one
  (or note "did not respond to requests for comment").
- **Biblical lens.** Every story gets a `takeaway` — one or two sentences of
  Scripture-grounded perspective (cite the reference).
- **Commentary.** Only include a Daniel Whyte III `commentary` when he has
  supplied one for that story. **Never invent his commentary.**
- **Voice.** Theologically biblical; plain, direct, pastoral.
  No sensationalism, no gossip framing.
- **Dates.** `published_at` = the run date (ISO). Display is always a fixed
  date — never relative ("x hours ago").
- **Attribution.** Every card and story page shows "Source: [outlet]" with a
  live link, plus "Read the original at [outlet]" on the story page.

## Failure handling

- If a feed is down or a story can't be verified, **skip that source** and
  take the next one in rotation. Never publish an unverified story.
- If an image download fails, use a styled placeholder (CSS gradient block
  with the credit line), never a broken `<img>` or an unreliable hotlink.
- If `git push` fails, leave the built files in place and report the failure
  to the site owner — do not retry pushes blindly more than twice.
