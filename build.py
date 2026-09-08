#!/usr/bin/env python3
"""Static build step for Elite Eye.

Reads content.json (the single source of truth) and generates:
  - index.html                 the one-page pitch
  - services/<slug>.html       one SEO landing page per service
  - services/index.html        the service index
  - sitemap.xml
  - robots.txt

Re-run after any edit to content.json:  python build.py

No dependencies. Stdlib only.
"""
import html
import json
import pathlib
from datetime import date

ROOT = pathlib.Path(__file__).parent
C = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))

BRAND = C["brand"]
BASE = BRAND["site"].rstrip("/")
NAME = BRAND["name"]
SERVICES = C["services"]

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Cormorant+Garamond:wght@300;400&family=Jost:wght@300;400&display=swap\">"
)


def e(s):
    return html.escape(str(s), quote=True)


def head(title, description, canonical, depth=0, schema=None):
    """<head> plus the opening body/header. depth = how many dirs deep the page sits."""
    up = "../" * depth
    blocks = ""
    for obj in schema or []:
        blocks += (
            '\n<script type="application/ld+json">'
            + json.dumps(obj, indent=2)
            + "</script>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(BASE)}/{e(C['hero']['image'])}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="{up}styles.css">{blocks}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="{up}index.html">{e(NAME)}</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav">
      <a href="{up}index.html#services">Services</a>
      <a href="{up}index.html#process">Process</a>
      <a href="{up}index.html#about">About</a>
      <a href="{up}index.html#faq">FAQ</a>
      <a class="btn" href="{e(BRAND['meetingUrl'])}">Book a call</a>
    </nav>
  </div>
</header>
<main>
"""


def foot(depth=0):
    up = "../" * depth
    year = date.today().year
    areas = " &middot; ".join(e(a) for a in BRAND["serviceArea"])
    links = "\n".join(
        f'      <li><a href="{up}services/{e(s["slug"])}.html">{e(s["title"])}</a></li>'
        for s in SERVICES
    )
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="wordmark" style="margin:0 0 .75rem">{e(NAME)}</p>
        <p style="margin:0;max-width:32ch">{e(BRAND['tagline'])}</p>
      </div>
      <div>
        <p class="eyebrow" style="margin-bottom:.75rem">Services</p>
        <ul style="list-style:none;margin:0;padding:0;line-height:2">
{links}
        </ul>
      </div>
      <div>
        <p class="eyebrow" style="margin-bottom:.75rem">Contact</p>
        <p style="margin:0;line-height:2">
          <a href="mailto:{e(BRAND['email'])}">{e(BRAND['email'])}</a><br>
          <a href="{e(BRAND['instagram'])}" rel="noopener">{e(BRAND['instagramHandle'])}</a><br>
          <a href="{e(BRAND['meetingUrl'])}">Book a consultation</a>
        </p>
      </div>
    </div>
    <div class="footer-legal">
      <span>&copy; {year} {e(BRAND['legalName'])}. All rights reserved.</span>
      <span>{areas}</span>
    </div>
  </div>
</footer>
<script src="{up}script.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- schema.org

def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": NAME,
        "legalName": BRAND["legalName"],
        "url": BASE + "/",
        "description": BRAND["description"],
        "image": f"{BASE}/{C['hero']['image']}",
        "email": BRAND["email"],
        "founder": {"@type": "Person", "name": BRAND["founder"]},
        "sameAs": [BRAND["instagram"]],
        "areaServed": [{"@type": "Place", "name": a} for a in BRAND["serviceArea"]],
        "priceRange": "$$$$",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Gift consulting services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "url": f"{BASE}/services/{s['slug']}.html",
                    "itemOffered": {
                        "@type": "Service",
                        "name": s["title"],
                        "description": s["summary"],
                    },
                }
                for s in SERVICES
            ],
        },
    }


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in C["faq"]
        ],
    }


def service_schema(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["title"],
        "serviceType": s["title"],
        "description": s["summary"],
        "url": f"{BASE}/services/{s['slug']}.html",
        "provider": {"@type": "ProfessionalService", "name": NAME, "url": BASE + "/"},
        "areaServed": [{"@type": "Place", "name": a} for a in BRAND["serviceArea"]],
        "audience": {"@type": "Audience", "audienceType": s["audience"]},
    }


def crumbs(s):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": NAME, "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": BASE + "/services/"},
            {"@type": "ListItem", "position": 3, "name": s["title"]},
        ],
    }


# ---------------------------------------------------------------- partials

def paragraphs(items):
    """content.json allows inline <em>, so these are intentionally not escaped."""
    return "\n".join(f"<p>{p}</p>" for p in items)


def cta_block():
    c = C["cta"]
    return f"""<section class="closing">
  <div class="wrap">
    <h2>{e(c['heading'])}</h2>
    <p class="lede">{e(c['body'])}</p>
    <div class="btn-row">
      <a class="btn" href="{e(BRAND['meetingUrl'])}">{e(c['button'])}</a>
    </div>
  </div>
</section>"""


def gallery_block():
    works = C.get("gallery") or []
    if not works:
        inner = (
            '<div class="gallery-empty">Selected work is being photographed. '
            "In the meantime, ask on the call &mdash; there is plenty to show.</div>"
        )
    else:
        cards = "\n".join(
            f"""      <figure>
        <img src="{e(w['image'])}" alt="{e(w.get('alt', w.get('title', '')))}" loading="lazy" width="800" height="800">
        <figcaption>{e(w.get('title', ''))}</figcaption>
      </figure>"""
            for w in works
        )
        inner = f'<div class="gallery-grid">\n{cards}\n    </div>'
    return f"""<section id="work" class="reveal">
  <div class="wrap">
    <div class="section-head narrow">
      <p class="eyebrow">Selected work</p>
      <h2>A record of what has been given</h2>
    </div>
    {inner}
  </div>
</section>
<hr class="rule">"""


# ---------------------------------------------------------------- pages

def build_index():
    hero = C["hero"]
    prob = C["problem"]
    about = C["about"]

    cards = "\n".join(
        f"""    <a class="service-card" href="services/{e(s['slug'])}.html">
      <span class="audience">{e(s['audience'])}</span>
      <h3>{e(s['title'])}</h3>
      <p>{e(s['summary'])}</p>
      <p class="price-note">{e(s['priceNote'])}</p>
    </a>"""
        for s in SERVICES
    )

    steps = "\n".join(
        f"""      <div class="process-step">
        <span class="num">{e(p['step'])}</span>
        <h3>{e(p['title'])}</h3>
        <p>{e(p['body'])}</p>
      </div>"""
        for p in C["process"]
    )

    faqs = "\n".join(
        f"""      <details class="faq-item">
        <summary>{e(f['q'])}</summary>
        <div class="faq-answer"><p>{e(f['a'])}</p></div>
      </details>"""
        for f in C["faq"]
    )

    body = f"""<section class="hero">
  <div class="wrap">
    <p class="eyebrow">{e(hero['eyebrow'])}</p>
    <h1>{e(hero['headline'])}</h1>
    <p class="lede">{e(hero['subhead'])}</p>
    <div class="btn-row">
      <a class="btn" href="{e(BRAND['meetingUrl'])}">{e(hero['primaryCta'])}</a>
      <a class="btn btn--ghost" href="#services">{e(hero['secondaryCta'])}</a>
    </div>
    <figure class="hero-figure" style="margin-inline:0">
      <img src="{e(hero['image'])}" alt="{e(hero['imageAlt'])}" width="1600" height="900">
    </figure>
  </div>
</section>

<div class="proof">
  <div class="wrap"><p>{e(C['proof']['line'])}</p></div>
</div>

<section id="why" class="reveal">
  <div class="wrap narrow">
    <p class="eyebrow">Why this exists</p>
    <h2>{e(prob['heading'])}</h2>
    <div class="lede" style="margin-top:2rem">
      {paragraphs(prob['body'])}
    </div>
  </div>
</section>
<hr class="rule">

<section id="services" class="reveal">
  <div class="wrap">
    <div class="section-head narrow">
      <p class="eyebrow">Services</p>
      <h2>Four ways to work together</h2>
    </div>
    <div class="services-grid">
{cards}
    </div>
  </div>
</section>

<section id="process" class="process reveal">
  <div class="wrap">
    <div class="section-head narrow">
      <p class="eyebrow">How it works</p>
      <h2>Four steps, and only one of them is yours</h2>
    </div>
    <div class="process-grid">
{steps}
    </div>
  </div>
</section>

<section id="about" class="reveal">
  <div class="wrap">
    <div class="about-grid">
      <figure class="about-portrait" style="margin:0">
        <img src="{e(BRAND['founderPhoto'])}" alt="{e(BRAND['founderPhotoAlt'])}" width="800" height="1000">
        <figcaption>{e(BRAND['founder'])}, founder</figcaption>
      </figure>
      <div>
        <p class="eyebrow">About</p>
        <h2>{e(about['heading'])}</h2>
        <div class="lede" style="margin-top:2rem">
          {paragraphs(about['body'])}
        </div>
      </div>
    </div>
  </div>
</section>
<hr class="rule">

{gallery_block()}

<section id="faq" class="reveal">
  <div class="wrap">
    <div class="section-head narrow">
      <p class="eyebrow">Questions</p>
      <h2>Before you book</h2>
    </div>
    <div class="faq-list">
{faqs}
    </div>
  </div>
</section>

{cta_block()}
"""

    page = (
        head(
            f"{NAME} — {BRAND['tagline']}",
            BRAND["description"],
            BASE + "/",
            depth=0,
            schema=[org_schema(), faq_schema()],
        )
        + body
        + foot(0)
    )
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def build_service(s):
    other = [x for x in SERVICES if x["slug"] != s["slug"]]
    more = "\n".join(
        f'      <a class="service-card" href="{e(x["slug"])}.html">'
        f'<span class="audience">{e(x["audience"])}</span>'
        f"<h3>{e(x['title'])}</h3><p>{e(x['summary'])}</p>"
        f'<p class="price-note">{e(x["priceNote"])}</p></a>'
        for x in other
    )
    includes = "\n".join(f"        <li>{e(i)}</li>" for i in s["includes"])

    body = f"""<section class="detail-hero">
  <div class="wrap">
    <p class="breadcrumb"><a href="../index.html">{e(NAME)}</a> / <a href="index.html">Services</a> / {e(s['title'])}</p>
    <p class="eyebrow">{e(s['audience'])}</p>
    <h1>{e(s['title'])}</h1>
    <p class="lede" style="max-width:50ch">{e(s['summary'])}</p>
    <div class="btn-row">
      <a class="btn" href="{e(BRAND['meetingUrl'])}">{e(BRAND['meetingCta'])}</a>
    </div>
  </div>
</section>
<hr class="rule">

<section>
  <div class="wrap">
    <div class="detail-body">
      <div class="lede">
        {paragraphs(s['detail'])}
        <p class="price-note" style="color:var(--accent);letter-spacing:.1em;text-transform:uppercase;font-size:.8rem">{e(s['priceNote'])}</p>
      </div>
      <aside class="includes">
        <h3>What is included</h3>
        <ul>
{includes}
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="process">
  <div class="wrap">
    <div class="section-head narrow">
      <p class="eyebrow">Also available</p>
      <h2>Other ways to work together</h2>
    </div>
    <div class="services-grid">
{more}
    </div>
  </div>
</section>

{cta_block()}
"""

    page = (
        head(
            f"{s['title']} — {NAME}",
            s["summary"],
            f"{BASE}/services/{s['slug']}.html",
            depth=1,
            schema=[service_schema(s), crumbs(s)],
        )
        + body
        + foot(1)
    )
    (ROOT / "services" / f"{s['slug']}.html").write_text(page, encoding="utf-8")


def build_service_index():
    cards = "\n".join(
        f"""      <a class="service-card" href="{e(s['slug'])}.html">
        <span class="audience">{e(s['audience'])}</span>
        <h3>{e(s['title'])}</h3>
        <p>{e(s['summary'])}</p>
        <p class="price-note">{e(s['priceNote'])}</p>
      </a>"""
        for s in SERVICES
    )
    body = f"""<section class="detail-hero">
  <div class="wrap">
    <p class="breadcrumb"><a href="../index.html">{e(NAME)}</a> / Services</p>
    <h1>Services</h1>
    <p class="lede" style="max-width:52ch">{e(BRAND['description'])}</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="services-grid">
{cards}
    </div>
  </div>
</section>
{cta_block()}
"""
    page = (
        head(
            f"Services — {NAME}",
            BRAND["description"],
            f"{BASE}/services/",
            depth=1,
            schema=[org_schema()],
        )
        + body
        + foot(1)
    )
    (ROOT / "services" / "index.html").write_text(page, encoding="utf-8")


def build_sitemap():
    urls = [(BASE + "/", "1.0"), (BASE + "/services/", "0.8")]
    urls += [(f"{BASE}/services/{s['slug']}.html", "0.7") for s in SERVICES]
    today = date.today().isoformat()
    entries = "\n".join(
        f"  <url><loc>{e(u)}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>"
        for u, p in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8"
    )


def main():
    (ROOT / "services").mkdir(exist_ok=True)
    (ROOT / "photos").mkdir(exist_ok=True)
    build_index()
    build_service_index()
    for s in SERVICES:
        build_service(s)
    build_sitemap()
    print(f"built index.html, services/index.html, {len(SERVICES)} service pages, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
