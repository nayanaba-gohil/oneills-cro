import json, html, os

SC = '/private/tmp/claude-501/-Users-macbook-oniells-category-page/d86eb9c5-c477-4c2f-84e2-b1ee547ebd33/scratchpad/'
OUT = '/Users/macbook/oniells category page/tyres.html'
BASE = 'https://oneillstyres.com.au'

# Where the vehicles category index lives. "vehicles.html" wires the local reference build
# together; set it back to "/tyres/vehicles" for the production paths.
VEHICLES_HREF = "vehicles.html"

chrome_css  = open(SC + 'chrome_css.txt', encoding='utf-8').read().replace('<style>', '', 1)
chrome_html = open(SC + 'chrome_html.txt', encoding='utf-8').read()
menu_html   = open(SC + 'menu_html.txt', encoding='utf-8').read()
menu_js     = open(SC + 'menu_js.txt', encoding='utf-8').read().replace('<script>\n', '', 1)
def unesc(t):
    # the source generator keeps these parts inside an f-string, so braces are doubled there
    return t.replace('{{', '{').replace('}}', '}')

chrome_css, chrome_html, menu_html, menu_js = (unesc(t) for t in (chrome_css, chrome_html, menu_html, menu_js))
for t in (chrome_css, chrome_html, menu_html, menu_js):
    assert t.strip()

# breadcrumb and current-page state belong to this page
chrome_html = chrome_html.replace('<li><a href="/tyres/vehicles" aria-current="page">Vehicles</a></li>',
                                  '<li><a href="/tyres/vehicles">Vehicles</a></li>')
chrome_html = chrome_html.replace('<a class="nav-top" href="/tyres">Tyres<span class="nav-chevron"',
                                  '<a class="nav-top" href="/tyres" aria-current="page">Tyres<span class="nav-chevron"')

chrome_html = chrome_html.replace('href="/tyres/vehicles"', 'href="' + VEHICLES_HREF + '"')
menu_html = menu_html.replace('href="/tyres/vehicles"', 'href="' + VEHICLES_HREF + '"')

makes = json.load(open(SC + 'makes.json', encoding='utf-8'))
MAKE_BY_NAME = {m['n']: m for m in makes}

BRANDS = [
  ("Toyo", "/tyres/brand/toyo", "toyo-logo.png"),
  ("Nitto", "/tyres/brand/nitto", "nitto_1.png"),
  ("Falken", "/tyres/brand/falken", "falken_1_.png"),
  ("Laufenn", "/tyres/brand/laufenn", "laufenn-1_1.png"),
  ("Kumho", "/tyres/brand/kumho", "kumho-tires_4_.png"),
  ("Dunlop", "/tyres/brand/dunlop", "dunlop-1_1.png"),
  ("Hankook", "/tyres/brand/hankook", "Hankook_logo_1.png"),
  ("General Tire", "/tyres/brand/general-tire", "general-tire-logo_1_.png"),
  ("Maxxis", "/tyres/brand/maxxis", "maxxis_1.png"),
  ("Goodyear", "/tyres/brand/goodyear", "goodyear_1_.png"),
  ("Yokohama", "/tyres/brand/yokohama", "yokohama-logo_1_.png"),
  ("BFGoodrich", "/tyres/brand/bfgoodrich", "bfgoodrich-1_1_.png"),
  ("Pirelli", "/tyres/brand/pirelli", "pirelli_1_.png"),
  ("Michelin", "/tyres/brand/michelin", "michelin-15_1_.png"),
  ("Continental", "/tyres/brand/continental", "continental-54_1_.png"),
  ("Triangle", "/tyres/brand/triangle", "20191119210047_5dd3e77fead0a.png"),
  ("Fronway", "/tyres/brand/fronway", "bf8573e7-b462-4740-9cc7-3886a09aa44c.png"),
]
CDN = BASE + '/media/catalog/category/'

WIDTHS = [125,135,145,155,165,175,185,195,205,215,225,235,245,255,265,275,285,295,305,315,325,335,345,355]
PROFILES = [30,35,40,45,50,55,60,65,70,75,80,85]
RIMS = [13,14,15,16,17,18,19,20,21,22]

FAQS = [
  ("What is included in the fitted price?",
   "Every fitted price covers mounting onto your rims, computerised dynamic wheel balancing, new rubber valve stems, and eco-disposal of your old tyres under NSW environmental rules. Nothing is added at collection."),
  ("How do I find the right tyre size for my car?",
   "Read the sidewall of a tyre already on the car, for example 225/65 R17 102H, or check the placard inside the driver's door frame. You can also enter your NSW plate above and we will pull the factory sizes and rim specifications for you."),
  ("How long does tyre fitting take?",
   "A standard set of four is usually fitted and balanced in 45 to 60 minutes. Booking ahead means your tyres are pulled from stock before you arrive, so you are not waiting on a transfer between workshops."),
  ("Do you price match other tyre retailers?",
   "Yes. Send us the competitor's advertised price for the same tyre in the same size through our price match form and we will match it where the tyre is in stock locally."),
  ("How often should tyres be replaced?",
   "Replace a tyre once tread depth reaches the 1.5 mm legal minimum in NSW, and sooner if you see cracking, bulges or uneven wear. Most tyres also reach the end of their useful life at around five to seven years regardless of tread left."),
  ("Which workshop will fit my tyres?",
   "You can choose from 8 workshops across Newcastle, Lake Macquarie and the Hunter: Belmont, Beresfield, Broadmeadow, Cessnock, Gateshead, Kurri Kurri, Morisset and Warners Bay. Pick your preferred location when you book."),
]



def opts(values, label):
    o = [f'<option value="">{label}</option>']
    o += [f'<option value="{v}">{v}</option>' for v in values]
    return '\n            '.join(o)



TOP_MAKES = ["Toyota", "Ford", "Mazda", "Hyundai", "Kia", "Mitsubishi",
             "Subaru", "Isuzu", "Volkswagen", "Nissan", "BMW", "MG"]

BRANCHES = [
    ("Belmont", "/location-belmont", "0249454945", "(02) 4945 4945"),
    ("Beresfield", "/location-beresfield", "0249660444", "(02) 4966 0444"),
    ("Broadmeadow", "/location-broadmeadow", "0240480108", "(02) 4048 0108"),
    ("Cessnock", "/location-cessnock", "0249901455", "(02) 4990 1455"),
    ("Gateshead", "/location-gateshead", "0249433711", "(02) 4943 3711"),
    ("Kurri Kurri", "/location-kurri-kurri", "0249375288", "(02) 4937 5288"),
    ("Morisset", "/location-morisset", "0249704321", "(02) 4970 4321"),
    ("Warners Bay", "/location-warners-bay", "0249567577", "(02) 4956 7577"),
]

# Placeholder social proof. Replace with the real aggregate before publishing.
REVIEW_SCORE = "4.8"
REVIEW_COUNT = "800+"

VEHICLE_CATS = [
    ("Passenger and car tyres", "Everyday driving",
     '<path d="M3 13l1.8-5.2A2 2 0 0 1 6.7 6.5h10.6a2 2 0 0 1 1.9 1.3L21 13v5h-3v-2H6v2H3z" stroke-linejoin="round"/><circle cx="7.5" cy="14.5" r="1.3"/><circle cx="16.5" cy="14.5" r="1.3"/>'),
    ("SUV and 4WD tyres", "Control under load",
     '<path d="M3 14l1.4-5.4A2 2 0 0 1 6.3 7h11.4a2 2 0 0 1 1.9 1.6L21 14v4h-3v-2H6v2H3z" stroke-linejoin="round"/><path d="M8 7V4.5h8V7"/><circle cx="7.5" cy="15" r="1.4"/><circle cx="16.5" cy="15" r="1.4"/>'),
    ("Light truck tyres", "Higher load ratings",
     '<path d="M2 6h11v10H2zM13 9h4.6l2.9 3.4V16H13z" stroke-linejoin="round"/><circle cx="6" cy="17.5" r="1.5"/><circle cx="17" cy="17.5" r="1.5"/>'),
    ("Performance tyres", "Handling and speed",
     '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3"/><path d="M12 3.5V9M12 15v5.5M3.5 12H9M15 12h5.5"/>'),
]

BRAND_VISIBLE = 12



def brand_cards(items, hidden=False):
    out = []
    for i, (n, u, img) in enumerate(items):
        cls = ' tile-item-extra' if hidden else ''
        hid = ' hidden' if hidden else ''
        out.append(f'''        <li class="tile-item{cls}"{hid}>
          <a class="tile" href="{u}" aria-label="Shop {html.escape(n)} tyres">
            <span class="tile-logo"><img src="{CDN}{img}" alt="{html.escape(n)} logo" width="110" height="52" loading="{'eager' if i < 6 and not hidden else 'lazy'}" decoding="async"></span>
            <h3 class="tile-name">{html.escape(n)}</h3>
            <span class="tile-link">Shop now<svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true" focusable="false"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          </a>
        </li>''')
    return '\n'.join(out)


def make_cards(names):
    out = []
    for n in names:
        m = MAKE_BY_NAME[n]
        e = html.escape(n)
        out.append(f'''        <li class="tile-item">
          <a class="tile" href="{html.escape(m['u'])}" aria-label="Shop tyres for {e}">
            <span class="tile-logo"><img src="{html.escape(m['i'])}" alt="{e} logo" width="72" height="52" loading="lazy" decoding="async"></span>
            <h3 class="tile-name">{e}</h3>
          </a>
        </li>''')
    return '\n'.join(out)


def make_options():
    o = ['<option value="">Select your vehicle make...</option>']
    o += [f'<option value="{html.escape(m["u"])}">{html.escape(m["n"])}</option>' for m in makes]
    return '\n              '.join(o)


def vehicle_cards():
    out = []
    for name, sub, path in VEHICLE_CATS:
        out.append(f'''        <li class="cat-card">
          <span class="cat-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6" focusable="false">{path}</svg></span>
          <span class="cat-body">
            <span class="cat-name">{html.escape(name)}</span>
            <span class="cat-sub">{html.escape(sub)}</span>
          </span>
        </li>''')
    return '\n'.join(out)


def faq_items():
    out = []
    for q, a in FAQS:
        out.append(f'''        <details class="faq-item">
          <summary class="faq-question">
            <span>{html.escape(q)}</span>
            <span class="faq-arrow" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span>
          </summary>
          <div class="faq-answer">{html.escape(a)}</div>
        </details>''')
    return '\n'.join(out)


def branch_dialog_rows():
    out = []
    for name, url, tel, pretty in BRANCHES:
        out.append(f'''        <li><a href="tel:{tel}">
          <span class="branch-name">{html.escape(name)}</span>
          <span class="branch-tel">{html.escape(pretty)}</span>
        </a></li>''')
    return '\n'.join(out)

breadcrumb = {
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Tyres", "item": BASE + "/tyres"},
    ],
}

brand_list = {
    "@context": "https://schema.org", "@type": "ItemList",
    "@id": BASE + "/tyres#brands", "name": "Tyre brands",
    "numberOfItems": len(BRANDS),
    "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n + " Tyres", "url": BASE + u, "image": CDN + img}
        for i, (n, u, img) in enumerate(BRANDS, start=1)
    ],
}

faq_schema = {
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in FAQS
    ],
}

business = {
    "@context": "https://schema.org",
    "@type": ["AutoRepair", "TireShop"],
    "@id": BASE + "/#business",
    "name": "O'Neills Tyre & Autocare",
    "url": BASE + "/",
    "description": "Locally owned tyre retailer and mechanical workshop group serving Newcastle, Lake Macquarie and the Hunter since 1961.",
    "foundingDate": "1961",
    "areaServed": [
        {"@type": "City", "name": "Newcastle"},
        {"@type": "City", "name": "Lake Macquarie"},
        {"@type": "AdministrativeArea", "name": "Hunter Region"},
    ],
    "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "NSW Motor Vehicle Repairers Licence",
        "identifier": "MVRL61864",
    },
    "identifier": {"@type": "PropertyValue", "name": "NSW Motor Vehicle Repairers Licence", "value": "MVRL61864"},
    "department": [
        {
            "@type": ["AutoRepair", "TireShop"],
            "@id": BASE + url + "#branch",
            "name": "O'Neills Tyre & Autocare " + name,
            "url": BASE + url,
            "telephone": "+61" + tel[1:],
            "identifier": {"@type": "PropertyValue", "name": "NSW Motor Vehicle Repairers Licence", "value": "MVRL61864"},
            "address": {"@type": "PostalAddress", "addressLocality": name, "addressRegion": "NSW", "addressCountry": "AU"},
        }
        for name, url, tel, pretty in BRANCHES
    ],
}

doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tyres in Newcastle &amp; the Hunter Valley | O'Neills Tyre &amp; Autocare</title>
<meta name="description" content="Quality tyres from leading global brands with all inclusive fitted pricing. Search by rego, tyre size or vehicle, with certified mounting and digital wheel balancing across the Hunter.">
<link rel="canonical" href="{BASE}/tyres">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(breadcrumb, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(business, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(brand_list, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
</script>
<style>
{chrome_css}
/* One corner radius across the page, matching the live site's 12px */
:root {{
  --radius: 12px;
  --btn-radius: 12px;
}}

/* Hero */
.hero {{ background: linear-gradient(135deg, #1a5fb4 0%, #144a8f 100%); color: #fff; padding: 40px 0; }}
.hero h1 {{ font-size: 34px; font-weight: 700; letter-spacing: -0.6px; line-height: 1.2; color: #fff; }}
.hero-copy {{ margin: 12px 0 0; max-width: 84ch; font-size: 16.5px; line-height: 1.7; color: rgba(255,255,255,.92); }}

/* Search band: rating and trust badges, on white below the hero */
.search-band {{ padding: 26px 0 0; }}

/* Social proof */
.rating {{ display: inline-flex; align-items: center; gap: 9px; padding: 7px 14px 7px 11px; border-radius: 999px; background: #f2f6fc; border: 1px solid #d6e3f5; color: var(--ink); font-size: 14px; }}
.rating:hover, .rating:focus-visible {{ border-color: var(--blue-600); }}
.rating-stars {{ display: inline-flex; gap: 1px; color: #f0a500; }}
.rating strong {{ font-weight: 600; }}
.rating span {{ color: var(--ink-soft); }}

/* Trust badges */
.badges {{ list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }}
.badges li {{ display: flex; gap: 11px; align-items: flex-start; padding: 14px 16px; border-radius: var(--radius); background: var(--surface); border: 1px solid var(--line); }}
.badges svg {{ flex: 0 0 auto; margin-top: 1px; color: var(--blue-600); }}
.badge-title {{ display: block; font-size: 14.5px; font-weight: 600; color: var(--ink); }}
.badge-sub {{ display: block; margin-top: 2px; font-size: 13px; color: var(--ink-soft); }}

.field label {{ display: block; margin-bottom: 7px; font-size: 13.5px; font-weight: 600; color: var(--ink); }}
.field select {{
  width: 100%; height: 52px; padding: 0 14px;
  font-family: Inter, sans-serif; font-size: 16px; font-weight: 500; color: var(--ink);
  background: #fff; border: 1px solid #c2cedd; border-radius: var(--btn-radius);
}}
.field select:focus-visible, .plate-input:focus-visible {{ outline: 3px solid rgba(26, 95, 180, .35); outline-offset: 1px; }}
.plate-input {{
  width: 100%; height: 52px;
  font-family: "Space Grotesk", sans-serif; font-size: 21px; font-weight: 700; letter-spacing: 3px; text-align: center;
  color: var(--ink); text-transform: uppercase;
  background: #fff; border: 2px solid var(--blue-900); border-radius: var(--btn-radius);
}}
.plate-input::placeholder {{ color: #9aa6b4; font-weight: 500; letter-spacing: 2px; }}
.finder-row {{ display: grid; gap: 12px; align-items: end; }}
.finder-row.size-row {{ grid-template-columns: repeat(3, minmax(0, 1fr)) auto; }}
.finder-row .btn-primary {{ height: 52px; font-size: 15.5px; }}
.finder-note {{ margin: 14px 0 0; font-size: 13px; color: var(--ink-soft); }}
.finder-error {{ margin: 12px 0 0; font-size: 13.5px; font-weight: 500; color: #b3261e; }}
.finder-error[hidden] {{ display: none; }}

/* Rego block */
.rego {{ background: #f0f5fc; border: 1px solid #d6e3f5; border-radius: var(--radius); padding: 26px 24px; }}
.rego h2 {{ font-size: 23px; font-weight: 600; letter-spacing: -0.2px; }}
.rego > p {{ margin: 8px 0 0; font-size: 15px; color: var(--ink-soft); max-width: 72ch; }}
.rego-form {{ display: grid; gap: 14px; margin-top: 20px; grid-template-columns: minmax(0, 1fr) 150px auto; align-items: end; }}
.plate-input {{
  width: 100%%; height: 56px;
  font-family: "Space Grotesk", sans-serif; font-size: 22px; font-weight: 700; letter-spacing: 3px; text-align: center;
  color: var(--ink); text-transform: uppercase;
  background: #fff; border: 2px solid var(--blue-900); border-radius: var(--btn-radius);
}}
.plate-input::placeholder {{ color: #9aa6b4; font-weight: 500; letter-spacing: 2px; }}
.plate-input:focus-visible {{ outline: 3px solid rgba(26, 95, 180, .35); outline-offset: 1px; }}
.rego-state select {{ height: 56px; }}
.rego-form .btn-primary {{ height: 56px; }}
.rego-note {{ margin: 14px 0 0; font-size: 13.5px; color: var(--ink-soft); }}
.finder-error {{ margin: 12px 0 0; font-size: 13.5px; font-weight: 500; color: #b3261e; }}
.finder-error[hidden] {{ display: none; }}

/* Finder intro */
.finders {{ padding: 34px 0 0; }}
.finders h2 {{ font-size: 21px; font-weight: 600; letter-spacing: -0.2px; }}
.finders p {{ margin: 8px 0 0; max-width: 88ch; font-size: 15.5px; color: var(--ink-soft); }}
.finders a {{ color: var(--blue-700); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }}
.finders a:hover {{ color: var(--blue-900); }}

/* Sections */
.section {{ padding: 34px 0; }}
.section + .section {{ padding-top: 0; }}
.section-head {{ margin-bottom: 18px; }}
.section-head h2 {{ font-size: 21px; font-weight: 600; letter-spacing: -0.2px; }}
.section-head p {{ margin: 6px 0 0; font-size: 14.5px; color: var(--ink-soft); }}
.section-foot {{ margin-top: 16px; font-size: 14.5px; }}
.section-foot a {{ color: var(--blue-700); font-weight: 500; }}
.section-foot a:hover {{ text-decoration: underline; text-underline-offset: 3px; }}

/* Vehicle category cards */
.cat-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; grid-template-columns: repeat(4, minmax(0, 1fr)); }}
.cat-card {{
  display: flex; align-items: center; gap: 13px; height: 100%;
  padding: 16px 18px; border-radius: var(--radius);
  background: var(--surface); border: 1px solid var(--line);
}}
.cat-icon {{ flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: var(--btn-radius); background: #eef3fa; color: var(--blue-600); }}
.cat-body {{ flex: 1 1 auto; min-width: 0; }}
.cat-name {{ display: block; font-size: 15px; font-weight: 700; color: var(--ink); line-height: 1.3; }}
.cat-sub {{ display: block; margin-top: 3px; font-size: 13px; color: var(--ink-soft); }}

/* Logo tiles */
.tile-grid {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(158px, 1fr)); }}
.tile {{
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  height: 100%; padding: 20px 14px 18px;
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  transition: border-color .18s ease, box-shadow .18s ease;
}}
.tile:hover, .tile:focus-visible {{ border-color: var(--blue-600); box-shadow: 0 4px 14px rgba(26, 95, 180, .14); }}
.tile-logo {{ display: flex; align-items: center; justify-content: center; width: 100%; height: 80px; }}
.tile-logo img {{ width: auto; max-width: 118px; max-height: 68px; object-fit: contain; }}
.tile-name {{ font-size: 15.5px; font-weight: 600; text-align: center; line-height: 1.25; }}
.tile-link {{ display: inline-flex; align-items: center; gap: 3px; margin-top: auto; font-size: 13px; font-weight: 500; color: var(--blue-700); }}
.tile-item[hidden] {{ display: none; }}

.tile-grid.brand-grid {{ gap: 16px; grid-template-columns: repeat(auto-fill, minmax(186px, 1fr)); }}
.brand-grid .tile {{ align-items: stretch; gap: 0; padding: 0; }}
.brand-grid .tile-logo {{ height: 112px; padding: 16px 16px 0; }}
.brand-grid .tile-logo img {{ max-width: 100%; max-height: 72px; }}
.brand-grid .tile-name {{ margin: 14px 20px 0; font-size: 17px; font-weight: 600; text-align: left; }}
.brand-grid .tile-link {{ margin: 6px 20px 16px; font-size: 14px; }}

/* Search by size card */
.size-card {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 24px; }}
.size-card h2 {{ font-size: 23px; font-weight: 600; letter-spacing: -0.2px; }}
.size-card > p {{ margin: 6px 0 0; font-size: 15.5px; color: var(--ink-soft); }}
.size-card .finder-row {{ margin-top: 20px; }}

/* Expander */
.expander {{
  display: inline-flex; align-items: center; gap: 7px; margin-top: 18px;
  padding: 11px 20px; border: 1px solid var(--blue-900); border-radius: var(--btn-radius);
  background: transparent; color: var(--blue-900); cursor: pointer;
  font-family: Inter, sans-serif; font-size: 14.5px; font-weight: 600;
  transition: background .18s ease, color .18s ease;
}}
.expander:hover, .expander:focus-visible {{ background: var(--blue-900); color: #fff; }}
.expander svg {{ transition: transform .2s ease; }}
.expander[aria-expanded="true"] svg {{ transform: rotate(180deg); }}

/* Long description */
.prose {{ text-align: left; }}
.prose > * {{ max-width: 90ch; margin-left: 0; margin-right: auto; }}
.prose h2 {{ font-size: 21px; font-weight: 600; letter-spacing: -0.2px; margin-top: 28px; }}
.prose h2:first-child {{ margin-top: 0; }}
.prose p {{ margin: 10px 0 0; color: var(--ink-soft); font-size: 15.5px; }}
.prose a {{ color: var(--blue-700); font-weight: 500; text-decoration: underline; text-underline-offset: 2px; }}

/* FAQ */
.faq-list {{ display: flex; flex-direction: column; gap: 10px; max-width: 900px; }}
.faq-item {{ border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); overflow: hidden; }}
.faq-question {{
  display: flex; justify-content: space-between; align-items: center; gap: 14px;
  padding: 15px 18px; cursor: pointer; list-style: none;
  font-size: 15px; font-weight: 600; color: var(--ink);
  transition: background .15s ease;
}}
.faq-question::-webkit-details-marker {{ display: none; }}
.faq-question:hover {{ background: #f6f8fb; }}
.faq-arrow {{ display: inline-flex; flex: 0 0 auto; color: var(--blue-700); transition: transform .2s ease; }}
.faq-item[open] .faq-arrow {{ transform: rotate(180deg); }}
.faq-answer {{ padding: 0 18px 16px; font-size: 14.5px; line-height: 1.65; color: var(--ink-soft); }}

/* Mobile sticky conversion bar */
.sticky-bar {{ display: none; }}
.call-sheet {{ border: 0; padding: 0; margin: auto auto 0; width: 100%; max-width: 520px; border-radius: var(--radius) var(--radius) 0 0; background: var(--surface); }}
.call-sheet::backdrop {{ background: rgba(11, 20, 32, .55); }}
.call-head {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 16px 18px; border-bottom: 1px solid var(--line); }}
.call-head h2 {{ font-size: 17px; font-weight: 600; }}
.call-sheet ul {{ list-style: none; margin: 0; padding: 8px 10px calc(14px + env(safe-area-inset-bottom)); max-height: 60vh; overflow-y: auto; overscroll-behavior: contain; }}
.call-sheet li a {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 14px; border-radius: var(--btn-radius); }}
.call-sheet li a:hover {{ background: #f3f6fb; }}
.branch-name {{ font-size: 15px; font-weight: 600; color: var(--ink); }}
.branch-tel {{ font-size: 15px; font-weight: 600; color: var(--blue-700); }}

@media (max-width: 1100px) and (min-width: 761px) {{
  .cat-list {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}

@media (max-width: 1023px) {{
  .sticky-bar {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 30;
    padding: 10px 12px calc(10px + env(safe-area-inset-bottom));
    background: var(--surface); border-top: 1px solid var(--line);
    box-shadow: 0 -4px 16px rgba(10, 22, 40, .1);
  }}
  .sticky-bar button {{
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    height: 48px; border-radius: var(--btn-radius); cursor: pointer;
    font-family: Inter, sans-serif; font-size: 15px; font-weight: 600;
  }}
  .sticky-primary {{ background: var(--blue-900); color: #fff; border: 0; }}
  .sticky-secondary {{ background: transparent; color: var(--blue-900); border: 1px solid var(--blue-900); }}
  body {{ padding-bottom: 76px; }}
}}

@media (max-width: 760px) {{
  .hero {{ padding: 28px 0; }}
  .hero h1 {{ font-size: 26px; }}
  .hero-copy {{ font-size: 15.5px; }}
  .search-band {{ padding-top: 22px; }}
  .rego {{ padding: 20px 16px; }}
  .rego h2 {{ font-size: 20px; }}
  .rego-form {{ grid-template-columns: 1fr; }}
  .rego-form .btn-primary {{ width: 100%%; justify-content: center; }}
  .cat-list {{ grid-template-columns: 1fr; }}
  .section {{ padding: 26px 0; }}
  .finder-tabs {{ padding: 5px 5px 0; }}
  .finder-tab {{ padding: 12px 6px; font-size: 13px; }}
  .finder-panel {{ padding: 18px 16px; }}
  .finder-row.rego-row, .finder-row.size-row, .finder-row.make-row {{ grid-template-columns: 1fr; }}
  .finder-row .btn-primary {{ width: 100%; justify-content: center; }}
  .tile-grid {{ grid-template-columns: repeat(auto-fill, minmax(142px, 1fr)); gap: 12px; }}
  .tile {{ padding: 16px 10px 14px; }}
  .tile-logo {{ height: 64px; }}
  .tile-logo img {{ max-height: 54px; }}
  .size-card {{ padding: 20px 16px; }}
  .size-card h2 {{ font-size: 20px; }}
  .brand-grid {{ grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }}
  .brand-grid .tile-logo {{ height: 88px; }}
  .brand-grid .tile-name {{ margin: 12px 14px 0; font-size: 15px; }}
  .brand-grid .tile-link {{ margin: 6px 14px 14px; }}
  .expander {{ width: 100%; justify-content: center; }}
}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{chrome_html}

{menu_html}

<nav class="crumbs" aria-label="Breadcrumb">
  <div class="wrap">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/tyres" aria-current="page">Tyres</a></li>
    </ol>
  </div>
</nav>

<main id="main">
  <section class="hero">
    <div class="wrap">
      <h1>Tyres in Newcastle &amp; the Hunter Valley</h1>
      <p class="hero-copy">
        Browse quality tyres from leading global brands with certified mounting, digital wheel balancing, and local warranty support across the Hunter.
      </p>
    </div>
  </section>

  <section class="search-band" aria-label="Find your tyres">
    <div class="wrap">
      <!-- Placeholder aggregate. Replace REVIEW_SCORE and REVIEW_COUNT with the real figures before publishing. -->
      <a class="rating" href="#reviews">
        <span class="rating-stars" aria-hidden="true">
          <svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor"><path d="M10 1.6l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></svg>
          <svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor"><path d="M10 1.6l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></svg>
          <svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor"><path d="M10 1.6l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></svg>
          <svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor"><path d="M10 1.6l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></svg>
          <svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor"><path d="M10 1.6l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></svg>
        </span>
        <strong>{REVIEW_SCORE}/5</strong>
        <span>across {REVIEW_COUNT} local Hunter reviews</span>
      </a>

      <ul class="badges" role="list">
        <li>
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>
            <span class="badge-title">All inclusive fitted pricing</span>
            <span class="badge-sub">Mounting, digital balancing and casing disposal</span>
          </span>
        </li>
        <li>
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><path d="M12 3l7.5 3v5.4c0 4.4-3 8.1-7.5 9.6-4.5-1.5-7.5-5.2-7.5-9.6V6z" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>
            <span class="badge-title">Local warranty and tyre safety guarantee</span>
            <span class="badge-sub">Claims handled here, not sent interstate</span>
          </span>
        </li>
        <li>
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><circle cx="12" cy="9" r="4"/><path d="M8.5 13.2L7 22l5-2.6L17 22l-1.5-8.8" stroke-linejoin="round"/></svg>
          <span>
            <span class="badge-title">Serving Newcastle and the Hunter since 1961</span>
            <span class="badge-sub">NSW licence MVRL61864</span>
          </span>
        </li>
      </ul>

    </div>
  </section>

  <section class="section" aria-labelledby="typesHeading">
    <div class="wrap">
      <div class="section-head">
        <h2 id="typesHeading">Tyres for every vehicle</h2>
        <p>Every driver has different priorities. Some want long tread life, some want wet grip, and many need load capacity for towing.</p>
      </div>
      <ul class="cat-list" role="list">
{vehicle_cards()}
      </ul>
    </div>
  </section>

  <section class="finders" aria-labelledby="findersHeading">
    <div class="wrap">
      <h2 id="findersHeading">Find tyres online with our tyre finders</h2>
      <p>Browse by brand catalogue, enter your rego, pick your vehicle manufacturer, or search straight by tyre size. Whichever details you already have, you land on a filtered list with fitted pricing and your choice of workshop. The <a href="/">tyre finder on our homepage</a> does the same job in one step if you would rather start there.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="brandsHeading">
    <div class="wrap">
      <div class="section-head">
        <h2 id="brandsHeading">Browse tyre catalogues</h2>
        <p>We stock the brands below at competitive fitted prices. If you cannot see the brand you want, call your nearest workshop and ask.</p>
      </div>
      <ul class="tile-grid brand-grid" role="list" id="brandGrid">
{brand_cards(BRANDS[:BRAND_VISIBLE])}
{brand_cards(BRANDS[BRAND_VISIBLE:], hidden=True)}
      </ul>
      <button class="expander" type="button" id="brandToggle" aria-expanded="false" aria-controls="brandGrid">
        <span id="brandToggleLabel">Show all {len(BRANDS)} brands</span>
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg>
      </button>
    </div>
  </section>

  <section class="section" aria-labelledby="regoHeading">
    <div class="wrap">
      <div class="rego">
        <h2 id="regoHeading">Search tyres by rego</h2>
        <p>Enter your plate number to automatically pull your factory tyre sizes and rim specifications.</p>
        <form class="rego-form" id="regoForm" action="/tyres/rego" method="get" novalidate>
          <div class="field plate-field">
            <label for="regoPlate">Registration plate</label>
            <input class="plate-input" id="regoPlate" name="plate" type="text" autocomplete="off" spellcheck="false" maxlength="8" placeholder="ABC 12D" aria-describedby="regoNote">
          </div>
          <div class="field rego-state">
            <label for="regoState">State</label>
            <select id="regoState" name="state">
              <option value="NSW" selected>NSW</option>
              <option value="ACT">ACT</option>
              <option value="QLD">QLD</option>
              <option value="VIC">VIC</option>
            </select>
          </div>
          <button class="btn-primary" type="submit">
            <svg viewBox="0 0 18 18" width="17" height="17" aria-hidden="true" focusable="false"><circle cx="8" cy="8" r="5.4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12.2 12.2L16 16" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
            Find my tyres
          </button>
        </form>
        <p class="finder-error" id="regoError" role="alert" hidden>Enter your plate number to continue.</p>
        <p class="rego-note" id="regoNote">We use your plate only to look up the factory fitment for your vehicle.</p>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="makesHeading">
    <div class="wrap">
      <div class="section-head">
        <h2 id="makesHeading">Pick your vehicle manufacturer</h2>
        <p>The makes we fit most across the Hunter.</p>
      </div>
      <ul class="tile-grid" role="list">
{make_cards(TOP_MAKES)}
      </ul>
      <p class="section-foot"><a href="{VEHICLES_HREF}">Browse all {len(makes)} manufacturers</a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="sizeCardHeading">
    <div class="wrap">
      <div class="size-card">
        <h2 id="sizeCardHeading">Search tyres by size</h2>
        <p>Already know your size? Read it off the sidewall, for example 225/65 R17.</p>
        <form class="finder-row size-row" action="/tyres/sizes" method="get">
          <div class="field">
            <label for="cardWidth">Width</label>
            <select id="cardWidth" name="width">
              {opts(WIDTHS, 'Any width')}
            </select>
          </div>
          <div class="field">
            <label for="cardProfile">Profile</label>
            <select id="cardProfile" name="profile">
              {opts(PROFILES, 'Any profile')}
            </select>
          </div>
          <div class="field">
            <label for="cardRim">Rim diameter</label>
            <select id="cardRim" name="rim_diameter">
              {opts(RIMS, 'Any rim')}
            </select>
          </div>
          <button class="btn-primary" type="submit">Find tyres</button>
        </form>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="aboutHeading">
    <div class="wrap prose">
      <h2 id="aboutHeading">Quality tyres Newcastle can rely on</h2>
      <p>O'Neills Tyre &amp; Autocare is locally owned and operated, with workshops at <a href="/location-belmont">Belmont</a>, <a href="/location-beresfield">Beresfield</a>, <a href="/location-broadmeadow">Broadmeadow</a>, <a href="/location-cessnock">Cessnock</a>, <a href="/location-gateshead">Gateshead</a>, <a href="/location-kurri-kurri">Kurri Kurri</a>, <a href="/location-morisset">Morisset</a> and <a href="/location-warners-bay">Warners Bay</a>. Whether you drive a car, SUV, ute or light truck, our team will match you to a tyre that suits how and where you actually drive.</p>
      <p>We stock trusted brands including Michelin, Pirelli, Yokohama, Hankook and Kumho, from everyday passenger tyres through to premium performance options, and we will tell you plainly when a cheaper tyre is the right call for your vehicle.</p>

      <h2>Locally owned and committed to safety</h2>
      <p>Alongside tyre fitting we offer wheel balancing and alignments, puncture repairs and rotations, pressure checks and safety inspections, plus full mechanical servicing and pink slips. That means your tyres, wheels and ongoing servicing are handled in one place, under NSW licence MVRL61864.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="faqHeading">
    <div class="wrap">
      <div class="section-head">
        <h2 id="faqHeading">Frequently asked questions about tyres</h2>
      </div>
      <div class="faq-list">
{faq_items()}
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-cols">
      <div>
        <p class="foot-h">Shop tyres</p>
        <ul>
          <li><a href="{VEHICLES_HREF}">Tyres by vehicle</a></li>
          <li><a href="/tyres/sizes">Tyres by size</a></li>
          <li><a href="/tyres/brand">Tyres by brand</a></li>
          <li><a href="/tyres">All tyres</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Services</p>
        <ul>
          <li><a href="/tyre-fitting">Tyre fitting</a></li>
          <li><a href="/wheel-alignment">Wheel alignment</a></li>
          <li><a href="/wheel-balancing">Wheel balancing</a></li>
          <li><a href="/services/puncture-repair">Puncture repairs</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Company</p>
        <ul>
          <li><a href="/about-us">About us</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/reviews" id="reviews">Reviews</a></li>
          <li><a href="/faqs">FAQs</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Talk to us</p>
        <ul>
          <li><a href="/location-belmont">Belmont</a></li>
          <li><a href="/location-cessnock">Cessnock</a></li>
          <li><a href="https://booking.oneillstyres.com.au">Book online</a></li>
        </ul>
      </div>
    </div>
    <p class="foot-base">Serving Newcastle and the Hunter Region since 1961. Licence MVRL61864.</p>
  </div>
</footer>

<div class="sticky-bar">
  <button class="sticky-primary" type="button" id="stickyRego">
    <svg viewBox="0 0 18 18" width="16" height="16" aria-hidden="true" focusable="false"><circle cx="8" cy="8" r="5.4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12.2 12.2L16 16" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
    Find tyres by rego
  </button>
  <button class="sticky-secondary" type="button" id="stickyCall" aria-haspopup="dialog" aria-controls="callSheet">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><path d="M21.5 16.9v2.8a2 2 0 0 1-2.2 2 19.6 19.6 0 0 1-8.5-3 19.3 19.3 0 0 1-6-6 19.6 19.6 0 0 1-3-8.6 2 2 0 0 1 2-2.2h2.8a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Call nearest workshop
  </button>
</div>

<dialog class="call-sheet" id="callSheet" aria-labelledby="callSheetTitle">
  <div class="call-head">
    <h2 id="callSheetTitle">Call your nearest workshop</h2>
    <button class="icon-btn" type="button" id="callSheetClose" aria-label="Close">
      <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
  </div>
  <ul>
{branch_dialog_rows()}
  </ul>
</dialog>

<script>
{menu_js}
(function () {{
  // Rego form
  var regoForm = document.getElementById('regoForm');
  var plate = document.getElementById('regoPlate');
  var regoErr = document.getElementById('regoError');
  if (regoForm) {{
    regoForm.addEventListener('submit', function (e) {{
      if (!plate.value.trim()) {{ e.preventDefault(); regoErr.hidden = false; plate.focus(); }}
    }});
    plate.addEventListener('input', function () {{
      plate.value = plate.value.toUpperCase();
      if (!regoErr.hidden && plate.value.trim()) regoErr.hidden = true;
    }});
  }}

  // Brand expander
  var bToggle = document.getElementById('brandToggle');
  var bLabel = document.getElementById('brandToggleLabel');
  if (bToggle) {{
    bToggle.addEventListener('click', function () {{
      var open = bToggle.getAttribute('aria-expanded') === 'true';
      bToggle.setAttribute('aria-expanded', open ? 'false' : 'true');
      Array.prototype.forEach.call(document.querySelectorAll('.tile-item-extra'), function (li) {{
        li.hidden = open;
      }});
      bLabel.textContent = open ? 'Show all {len(BRANDS)} brands' : 'Show fewer brands';
    }});
  }}

  // Mobile sticky bar
  var stickyRego = document.getElementById('stickyRego');
  if (stickyRego) {{
    stickyRego.addEventListener('click', function () {{
      var block = document.querySelector('.rego');
      if (block) block.scrollIntoView({{ block: 'center' }});
      window.setTimeout(function () {{ if (plate) plate.focus({{ preventScroll: true }}); }}, 340);
    }});
  }}

  var sheet = document.getElementById('callSheet');
  var sheetOpen = document.getElementById('stickyCall');
  var sheetClose = document.getElementById('callSheetClose');
  if (sheet && sheetOpen) {{
    var sheetScroll = 0;
    function lockSheet() {{
      sheetScroll = window.scrollY || 0;
      document.body.style.top = '-' + sheetScroll + 'px';
      document.body.classList.add('body-scroll-locked');
    }}
    function unlockSheet() {{
      document.body.classList.remove('body-scroll-locked');
      document.body.style.top = '';
      var prev = document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, sheetScroll);
      document.documentElement.style.scrollBehavior = prev;
    }}
    function closeSheet() {{
      if (sheet.open) {{ try {{ sheet.close(); }} catch (err) {{ sheet.removeAttribute('open'); }} }}
      unlockSheet();
    }}
    sheetOpen.addEventListener('click', function () {{
      if (sheet.open) return;
      lockSheet();
      try {{ sheet.showModal(); }} catch (err) {{ unlockSheet(); }}
    }});
    if (sheetClose) sheetClose.addEventListener('click', closeSheet);
    sheet.addEventListener('close', unlockSheet);
    sheet.addEventListener('cancel', function () {{ window.setTimeout(unlockSheet, 0); }});
    sheet.addEventListener('click', function (e) {{ if (e.target === sheet) closeSheet(); }});
    Array.prototype.forEach.call(sheet.querySelectorAll('a'), function (a) {{
      a.addEventListener('click', closeSheet);
    }});
  }}
}})();
</script>
</body>
</html>
'''

open(OUT, 'w', encoding='utf-8').write(doc)
print('wrote', OUT, len(doc), 'bytes |', len(BRANDS), 'brands |', len(makes), 'makes |', len(FAQS), 'faqs |', len(BRANCHES), 'branches')
