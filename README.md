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

## Stock photography

`photos/pexels/` holds licensed stock from Pexels used for section atmosphere
only - her own photography carries the credibility, these are texture. Sources,
photographers and links are in `photos/pexels/CREDITS.json`. Pexels does not
require attribution; the file exists so the origin of every image is traceable.

`prep_photos.py` derives the service lead images and the parallax band from
them via its `STOCK` map.

## Motion

Hover and scroll motion live in `styles.css` and `script.js`:

- buttons wipe their fill left-to-right, nav links grow an underline
- service cards lift, sweep a hairline across the top and slide in an arrow
- gallery tiles zoom under a caption overlay
- process steps lift and fill their rule with the accent
- the headline rises word by word on load
- the hero, the service lead images and the silk band drift against the scroll
- sections and grids fade in, grid children staggered 90ms apart

Two rules govern all of it:

1. **Content is never hidden by CSS unless JS is running.** The hiding rules are
   scoped to `.js-motion`, a class `script.js` sets on `<html>`. A script error,
   a blocked file or an observer that never fires costs the animation, never the
   content. A 2.2s failsafe reveals everything regardless.
2. **`prefers-reduced-motion: reduce` disables all of it** - no parallax, no
   reveal, no hover transitions.

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
