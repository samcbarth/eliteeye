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

## Photos

`photos/ig/` holds the untouched originals saved from the @eliteeyegifts
Instagram. `prep_photos.py` derives everything the site serves from them:

```bash
python prep_photos.py
```

It writes the hero crop, gallery images and square thumbnails into `photos/`
and `photos/thumbs/`. Add a source file plus a line in that script's `MAP` to
publish another one.

## Placeholder handling

Any `content.json` string still written as `[SOMETHING]` counts as unresolved.
`build.py` treats those carefully so nothing half-finished goes public:

- every page gets `<meta name="robots" content="noindex">` while the email or
  meetings link is still a placeholder
- booking CTAs fall back to the Instagram profile instead of a dead link
- bracketed paragraphs are dropped from the rendered copy
- the founder portrait is omitted entirely when `brand.founderPhoto` is `null`,
  and the about section runs full width instead

So the site is publishable at every stage, and it starts indexing itself the
moment the last placeholder is filled.

## Still to fill in

- `brand.email` — currently `[EMAIL]`, keeps the site on noindex
- `brand.meetingUrl` — currently `[HUBSPOT_MEETINGS_LINK]`, keeps the site on
  noindex and sends every CTA to Instagram
- `about.body[1]` — Rachel's bio paragraph, currently omitted from the page
- `brand.founderPhoto` — set to a path once there is a portrait
- `brand.founder` — set to "Rachel" from the Instagram display name; confirm
  whether a surname should appear
