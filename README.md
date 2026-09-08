# Elite Eye

Static marketing site for Elite Eye — private luxury gift consulting.
Goal of the site: book complimentary consultation calls. It does not sell products.

## How it works

`content.json` is the single source of truth. `build.py` reads it and generates:

- `index.html` — the one-page pitch
- `services/index.html` + `services/<slug>.html` — one SEO landing page per service
- `sitemap.xml`, `robots.txt`

Edit `content.json`, then:

```bash
python build.py
```

Never hand-edit the generated HTML; the next build overwrites it.

`make_placeholders.py` generates cream placeholder images for any photo that
isn't in `photos/` yet. Drop a real photo at the same path to replace one.

## Deploy

Push to `main`. GitHub Actions publishes the repo root to GitHub Pages.
Add a `CNAME` file containing the domain when one is chosen.

## Still to fill in

Search `content.json` for these placeholders:

- `[FOUNDER_NAME]` — founder's name (appears in bio, portrait caption, schema.org)
- `[FOUNDER_BIO_PLACEHOLDER ...]` — the middle paragraph of the About section
- `[EMAIL]` — contact email
- `[IG_HANDLE]` — Instagram handle
- `[HUBSPOT_MEETINGS_LINK]` — HubSpot meetings URL, used by every CTA on the site
- `photos/hero.jpg`, `photos/founder.jpg` — currently placeholders
- `gallery` — empty array; add `{"image","title","alt"}` entries to fill the work section

## Instagram assets (@eliteeyegifts)

The account has 7 posts, all high resolution (up to 1440x1800), dated Dec 2021 –
May 2022, several tagged in Dallas, Texas. They could not be pulled
automatically: Instagram requires a logged-in session, its CSP blocks in-page
fetching, and a https page cannot relay to a local http receiver (mixed content).

Download them by hand from https://www.instagram.com/eliteeyegifts/ and drop
them in `photos/`, then add entries to the `gallery` array in `content.json`.

Post shortcodes, newest first:
CdyxDjfvyLl, CdywXTBvr6r, CdywAtEPJKs, CXj43TTs1jo, CXjytS8puJu, CWwRVNUPRRY, CWOs-syP4R6
