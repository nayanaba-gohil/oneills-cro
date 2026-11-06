import json, html

SC = '/private/tmp/claude-501/-Users-macbook-oniells-category-page/d86eb9c5-c477-4c2f-84e2-b1ee547ebd33/scratchpad/'
BASE = 'https://oneillstyres.com.au'
OUT = '/Users/macbook/oniells category page/result-suzuki-baleno.html'

# Local reference wiring. Swap for production paths at handover.
VEHICLES_HREF = "vehicles.html"
MAKE_HREF = "suzuki.html"
MODEL_HREF = "suzuki-baleno.html"

VEHICLE = {
    "make": "Suzuki", "model": "Baleno", "trim": "1.0T",
    "body": "Hatchback", "fuel": "Petrol", "hp": 110,
    "years": "2019 to 2023",
    "bolt": "4x100", "bore": "54.1",
}
CRUMB_VEHICLE = "%(make)s %(model)s %(body)s %(trim)s %(fuel)s (%(years)s)" % VEHICLE

FITMENTS = [
    {"size": "185/55R16 83V", "rim": "6Jx16", "et": "ET45", "pos": "All Round", "oem": True},
    {"size": "185/55R16 87V", "rim": "6Jx16", "et": "ET45", "pos": "All Round", "oem": False},
    {"size": "185/55R16 83H", "rim": "6Jx16", "et": "ET45", "pos": "All Round", "oem": False},
]

# 12 of the 17 results the live page returns, with their real prices and URLs.
IMG = BASE + "/media/catalog/product/cache/b3324c89e0e19838a4838fa9f936ad20/"
OEM = BASE + "/media/meetanshi/oem/"

# All 17 results the live page returns across both pages, with their real prices, images and URLs.
# "oe" is the original-equipment vehicle brand the live listing shows on that tyre.
# "offer" flags a tyre as a special offer. Price is unchanged, the badge is the only signal.
PRODUCTS = [
    ("Yokohama", "BluEarth ES32", "185/55R16 83V", 239.00, None, True, "yokohama", "Touring",
     "/yokohama-18555r16-83v-bluearth-es32-1855516es32",
     IMG + "4/d/4d8bedb6073adbc58a4c0e11305bd632acd4395a46a2d441a2e04bdb637dac90_11.webp"),
    ("Yokohama", "BluEarth AE51", "185/55R16 83V", 255.00, None, False, "yokohama", "Touring",
     "/yokohama-18555r16-83v-bluearth-ae51-1855516ae51", IMG + "4/d/4d8bedb6073adbc58a4c0e11305bd632acd4395a46a2d441a2e04bdb637dac90_10.webp"),
    ("Triangle", "TE307 ReliaXTouring", "185/55R16 87V", 115.00, None, False, "triangle", "Touring",
     "/triangle-te307-reliaxtouring-18555r16-87v-cbpte30718j16vfj", IMG + "t/r/triangle-te307-reliaxtouring.webp"),
    ("Dunlop", "SP Touring R1", "185/55R16 83H", 129.00, None, False, "dunlop", "Touring",
     "/dunlop-18555r16-83h-sp-touring-r1-au10327164", IMG + "d/u/dunlop-sp-touring-r1.webp"),
    ("Dunlop", "SP Sport LM705", "185/55R16 83V", 155.00, None, False, "dunlop", "Touring",
     "/dunlop-18555r16-83v-sp-sport-lm705-au10335419", IMG + "d/u/dunlop-sp-sport-lm705.webp"),
    ("Falken", "ZE310R", "185/55R16 83V", 165.00, None, False, "falken", "Performance",
     "/falken-18555r16-83v-ze310r-au10353124", IMG + "0/8/081aacb00e26d456fad1d70772662fc07182607ddd352bdce37a6c0e7546abe8_42.webp"),
    ("Dunlop", "Blue Response TG", "185/55R16 83V", 179.00, None, False, "dunlop", "Touring",
     "/dunlop-18555r16-83v-blue-response-tg-au10361095",
     IMG + "2/4/24c90ab0422ec312346aa76344c5c1264da78e78932db1ee2a3a26385064ddc1_28.webp"),
    ("Kumho", "Ecsta PA51", "185/55R16 83V", 179.00, None, False, "kumho", "Performance",
     "/kumho-ecsta-pa51-18555r16-83v-phase-out-2265043", IMG + "4/b/4bea1cecfb379c4abb67d4a5a07becd52d329e0c4de27897f2fd07dd7dcd4581_49.webp"),
    ("Hankook", "Ventus Prime4 K135", "185/55R16 83H", 185.00, None, False, "hankook", "Performance",
     "/hankook-18555r16-83h-ventus-prime4-k135-1034272",
     IMG + "5/3/537c9251837d4ab72bce1c7026242e8a0c72609f5fa56d1ec5ce0e605a3291db_62.webp"),
    ("Maxxis", "HP5 Premitra", "185/55R16 83V", 185.00, None, False, "maxxis", "Performance",
     "/18555r16-maxxis-hp5-premitra-83v-tyre-8000953",
     IMG + "5/7/5722b8fe38867cc326f8a54ee71ab2b0817917864fa3936d4b3d087fb5a88908_16.webp"),
    ("BFGoodrich", "Advantage Touring", "185/55R16 87H", 199.00, None, False, "bfgoodrich", "Touring",
     "/bfgoodrich-advantage-touring-18555r16-87-h-858101",
     IMG + "6/0/60163106572d9bec72ad4d6f4b84af124cea082285de629a414a9b1f2df39059_29.webp"),
    ("Dunlop", "SP Sport 2030", "185/55R16 83H", 199.00, "Honda", False, "dunlop", "Performance",
     "/dunlop-18555r16-83h-sp-sport-2030-au10281385",
     IMG + "7/6/7688336d809698e6cb96f96bd2882e9d1479cc54a92573d31322e49cb589e208_8.webp"),
    ("Hankook", "iON ST AS IH61 XL", "185/55R16 87V", 199.00, "BYD", False, "hankook", "EV",
     "/hankook-18555r16-87v-ion-st-as-ih61-xl-ev-1037512",
     IMG + "2/4/24c8082d3b5549b752b0602b46d6e5d3fbce57b7c5cec198d76f7a4404ac9d4c_7.webp"),
    ("Toyo", "Proxes CR1", "185/55R16 87H", 235.00, None, False, "toyo", "Touring",
     "/toyo-proxes-cr1-18555r16-87h-1111767", IMG + "1/1/11d5d3188c4b44036136fe7cf5f30a02a504a52fc8886efddd457b3abee2b737_34.webp"),
    ("Michelin", "Energy XM2 +", "185/55R16 83V", 239.00, None, False, "michelin", "Touring",
     "/michelin-energy-xm2-plus-18555r16-83-v-890588",
     IMG + "3/b/3b3b2c00e31e3d6807cc2551fd214931373b49bb44bf83b19f3a1f2560f08b66_19.webp"),
    ("Goodyear", "Assurance Maxguard EV Ready", "185/55R16 83V", 245.00, None, False, "goodyear", "EV",
     "/18555r16-goodyear-assurance-maxguard-ev-ready-83v-tyre-8000952",
     IMG + "5/0/50317d5364d68336a072226cf772cebc286f7522abe46e1ae63344e00257ad99_10.webp"),
    ("Continental", "UltraContact UC7", "185/55R16 83V", 255.00, None, False, "continental", "Performance",
     "/continental-ultracontact-uc7-18555r16-83v-03120170000",
     IMG + "c/o/continental-ultracontact-uc7.webp"),
]

PER_PAGE = 12

# Workshops, for the stock availability sheet.
STORES = [
    ("Belmont", "/location-belmont", "0249454945", "(02) 4945 4945"),
    ("Beresfield", "/location-beresfield", "0249660444", "(02) 4966 0444"),
    ("Broadmeadow", "/location-broadmeadow", "0240480108", "(02) 4048 0108"),
    ("Cessnock", "/location-cessnock", "0249901455", "(02) 4990 1455"),
    ("Gateshead", "/location-gateshead", "0249433711", "(02) 4943 3711"),
    ("Kurri Kurri", "/location-kurri-kurri", "0249375288", "(02) 4937 5288"),
    ("Morisset", "/location-morisset", "0249704321", "(02) 4970 4321"),
    ("Warners Bay", "/location-warners-bay", "0249567577", "(02) 4956 7577"),
]

BRAND_LOGOS = {
    "falken": BASE + "/media/meetanshi/brand/falken-logo-350x60-cropped.webp",
    "kumho": BASE + "/media/meetanshi/brand/kumho-logo-400x60-padded.webp",
    "toyo": BASE + "/media/meetanshi/brand/toyo-tires-logo-400x41.webp",
    "triangle": BASE + "/media/meetanshi/brand/cache/160x40/20191119210047_5dd3e77fead0a.png",
    "yokohama": BASE + "/media/meetanshi/brand/yokohama-symbol-450x60-cropped.webp",
    "dunlop": BASE + "/media/meetanshi/brand/dunlop-logo-350x60-cropped.webp",
    "bfgoodrich": BASE + "/media/meetanshi/brand/cache/160x40/bfgoodrich-1.png",
    "michelin": BASE + "/media/meetanshi/brand/michelin-logo-350x60-cropped.webp",
    "hankook": BASE + "/media/meetanshi/brand/hankook-logo-450x60-cropped.webp",
    "continental": BASE + "/media/meetanshi/brand/continental-logo-400x109.webp",
    "goodyear": BASE + "/media/meetanshi/brand/goodyear-logo-350x60-cropped.webp",
    "maxxis": BASE + "/media/meetanshi/brand/maxxis-logo-350x60-cropped.webp",
}

# Sidebar order: brand, price, tyre category, speed rating, size.
# "Manual Update Needed" and "Availability" are dropped. "TPC Category 1/2" are renamed and
# deduplicated: High Performance absorbs UHP and Ultra High Performance.
PRICE_BRACKETS = [("Under $150", "u150"), ("$150 to $250", "150-250"), ("$250 and over", "250plus")]
TYRE_CATEGORIES = ["Touring", "Performance", "High performance", "EV ready"]
VEHICLE_TYPES = ["Passenger"]
SPEED_RATINGS = ["H", "V"]
SIZES = ["185/55R16 83H", "185/55R16 83V", "185/55R16 87H", "185/55R16 87V"]

chrome_css = open(SC + 'chrome_css.txt', encoding='utf-8').read().replace('<style>', '', 1)
chrome_html = open(SC + 'chrome_html.txt', encoding='utf-8').read()
menu_html = open(SC + 'menu_html.txt', encoding='utf-8').read()
menu_js = open(SC + 'menu_js.txt', encoding='utf-8').read().replace('<script>\n', '', 1)


def unesc(t):
    return t.replace('{{', '{').replace('}}', '}')


chrome_css, chrome_html, menu_html, menu_js = (unesc(t) for t in (chrome_css, chrome_html, menu_html, menu_js))
chrome_html = chrome_html.replace('<li><a href="/tyres/vehicles" aria-current="page">Vehicles</a></li>',
                                  '<li><a href="/tyres/vehicles">Vehicles</a></li>')
chrome_html = chrome_html.replace('href="/tyres/vehicles"', 'href="' + VEHICLES_HREF + '"')
menu_html = menu_html.replace('href="/tyres/vehicles"', 'href="' + VEHICLES_HREF + '"')


def bracket(p):
    if p < 150:
        return "u150"
    if p < 250:
        return "150-250"
    return "250plus"


def fitment_options():
    out = []
    for i, f in enumerate(FITMENTS):
        badge = ' <span class="opt-oem">OEM</span>' if f["oem"] else ''
        out.append('''            <li><button class="fit-opt%s" type="button" role="option" aria-selected="%s" data-size="%s">
              <span class="opt-size">%s%s</span>
              <span class="opt-meta">%s &middot; %s &middot; %s</span>
            </button></li>''' % (
            ' is-on' if i == 0 else '', 'true' if i == 0 else 'false',
            f["size"], f["size"], badge, f["rim"], f["et"], f["pos"]))
    return '\n'.join(out)


def checks(name, items, group):
    out = []
    for i, it in enumerate(items):
        label, value = (it if isinstance(it, tuple) else (it, it))
        fid = '%s-%d' % (group, i)
        out.append('''          <li><label class="check" for="%s">
            <input type="checkbox" id="%s" name="%s" value="%s">
            <span>%s</span>
          </label></li>''' % (fid, fid, group, html.escape(value), html.escape(label)))
    return '\n'.join(out)


def product_cards():
    out = []
    for i, (brand, name, size, price, oe, offer, slug, cat, url, img) in enumerate(PRODUCTS):
        logo = BRAND_LOGOS.get(slug, '')
        money = lambda v: ('%.2f' % v)
        oe_badge = ''
        if oe:
            oe_badge = ('<span class="p-oe" title="Original equipment on %s">'
                        '<img src="%s%s.png" alt="Original equipment on %s" width="30" height="30" loading="lazy" decoding="async">'
                        '</span>') % (html.escape(oe), OEM, oe.lower(), html.escape(oe))
        offer_badge = '<span class="p-offer"><span>Special offer</span></span>' if offer else ''
        store = STORES[i % len(STORES)]
        out.append('''        <li class="p-item" data-brand="%s" data-price="%s" data-cat="%s" data-size="%s" data-page="%d">
          <article class="p-card">
            %s<div class="p-media">
              <img class="p-photo" src="%s" alt="%s %s tyre" width="240" height="240" loading="%s" decoding="async"%s>
              %s
            </div>
            <div class="p-top">
              <span class="p-brand"><img src="%s" alt="%s" width="104" height="28" loading="lazy" decoding="async"></span>
              <button class="p-wish" type="button" aria-pressed="false" aria-label="Save %s %s to your wishlist">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21.2l7.8-7.7 1-1.1a5.5 5.5 0 0 0 0-7.8z" stroke-linejoin="round"/></svg>
              </button>
            </div>
            <h3 class="p-name"><a href="%s">%s %s</a></h3>
            <p class="p-size">%s</p>
            <div class="p-avail">
              <span class="p-instock">
                <svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true" focusable="false"><path d="M3 8.5l3.2 3.2L13 5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                In stock at %s
              </span>
              <button class="p-stores" type="button" data-product="%s" aria-haspopup="dialog" aria-label="See stock at all workshops for %s %s">All stores</button>
            </div>
            <div class="p-qty">
              <span class="qty-label">Qty</span>
              <div class="qty-box">
                <button type="button" class="qty-btn" data-step="-1" aria-label="Decrease quantity for %s %s">&minus;</button>
                <input id="qty-%d" class="qty-input" type="number" inputmode="numeric" min="1" max="8" step="1" value="1" aria-label="Quantity of %s %s">
                <button type="button" class="qty-btn" data-step="1" aria-label="Increase quantity for %s %s">+</button>
              </div>
            </div>
            <div class="p-foot">
              <span class="p-price"><span class="p-amount">$%s</span> <span class="p-unit">EA</span></span>
              <div class="p-actions">
                <a class="p-cta" href="%s">Add to Cart</a>
                <button class="p-pm" type="button">Price Match</button>
              </div>
            </div>
          </article>
        </li>''' % (slug, bracket(price), cat.lower().replace(' ', '-'), size, i // PER_PAGE + 1,
                    offer_badge,
                    img, html.escape(brand), html.escape(name),
                    'eager' if i < 4 else 'lazy', ' fetchpriority="high"' if i < 2 else '',
                    oe_badge,
                    logo, html.escape(brand), html.escape(brand), html.escape(name),
                    url, html.escape(brand), html.escape(name),
                    html.escape(size),
                    html.escape(store[0]),
                    html.escape('%s %s %s' % (brand, name, size)), html.escape(brand), html.escape(name),
                    html.escape(brand), html.escape(name), i, html.escape(brand), html.escape(name),
                    html.escape(brand), html.escape(name),
                    money(price), url))
    return '\n'.join(out)


def store_rows():
    out = []
    for i, (name, url, tel, pretty) in enumerate(STORES):
        state = 'In stock' if i % 3 else 'Order in, 2 to 3 days'
        cls = 'ok' if i % 3 else 'wait'
        out.append('''        <li>
          <div class="store-row">
            <span class="store-name"><a href="%s">%s</a></span>
            <span class="store-state %s">%s</span>
            <a class="store-tel" href="tel:%s">%s</a>
          </div>
        </li>''' % (url, html.escape(name), cls, state, tel, html.escape(pretty)))
    return '\n'.join(out)


breadcrumb = {
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Tyres", "item": BASE + "/tyres"},
        {"@type": "ListItem", "position": 3, "name": VEHICLE["make"], "item": BASE + "/tyres/vehicles/suzuki"},
        {"@type": "ListItem", "position": 4, "name": VEHICLE["model"], "item": BASE + "/tyres/vehicles/suzuki/baleno"},
        {"@type": "ListItem", "position": 5, "name": CRUMB_VEHICLE},
    ],
}

product_list = {
    "@context": "https://schema.org", "@type": "ItemList",
    "name": "Tyres for " + CRUMB_VEHICLE,
    "numberOfItems": len(PRODUCTS),
    "itemListElement": [
        {"@type": "ListItem", "position": i,
         "item": {"@type": "Product", "name": "%s %s %s" % (b, n, s), "url": BASE + u,
                  "brand": {"@type": "Brand", "name": b},
                  "offers": {"@type": "Offer", "price": "%.2f" % p, "priceCurrency": "AUD",
                             "availability": "https://schema.org/InStock", "url": BASE + u}}}
        for i, (b, n, s, p, oe, off, slug, c, u, im) in enumerate(PRODUCTS, start=1)
    ],
}

doc = '''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tyres for %(crumbveh)s | O'Neills Tyre &amp; Autocare</title>
<meta name="description" content="Tyres that fit the %(crumbveh)s, with all inclusive fitted pricing, digital wheel balancing and your choice of workshop across Newcastle and the Hunter.">
<meta name="robots" content="noindex, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
%(breadcrumb)s
</script>
<script type="application/ld+json">
%(productlist)s
</script>
<style>
%(chromecss)s
:root { --radius: 12px; --btn-radius: 12px; }

.crumbs { background: var(--surface); border-bottom: 0; }
.crumbs ol { justify-content: flex-start; padding: 16px 0 4px; }
.crumbs li:last-child { color: var(--ink); font-weight: 600; }

/* Vehicle header */
.veh { background: linear-gradient(135deg, #1a5fb4 0%%, #144a8f 100%%); color: #fff; padding: 26px 0 28px; }
.veh-top { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.veh h1 { font-size: 27px; font-weight: 700; letter-spacing: -0.4px; color: #fff; }
.change-veh { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: #fff; text-decoration: underline; text-underline-offset: 3px; }
.change-veh:hover, .change-veh:focus-visible { color: #fff; text-decoration-thickness: 2px; }
.spec-grid {
  display: grid; margin: 18px 0 0; padding: 0;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-top: 1px solid rgba(255, 255, 255, .22);
}
.spec-cell { padding: 14px 20px 2px 0; border-left: 1px solid rgba(255, 255, 255, .22); padding-left: 20px; }
.spec-cell:first-child { border-left: 0; padding-left: 0; }
.spec-grid dt { font-size: 12.5px; font-weight: 500; letter-spacing: .3px; color: rgba(255, 255, 255, .7); }
.spec-grid dd { margin: 4px 0 0; font-family: "Space Grotesk", sans-serif; font-size: 18px; font-weight: 700; line-height: 1.2; color: #fff; }

/* Fitment */
.fitment { padding: 22px 0 0; }
.fit-card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 20px; }
.fit-head { display: flex; align-items: baseline; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
.fit-head h2 { font-size: 17px; font-weight: 600; }
.fit-head p { margin: 3px 0 0; font-size: 13.5px; color: var(--ink-soft); }
.fit-picker { position: relative; margin-top: 14px; max-width: 460px; }
.fit-trigger {
  width: 100%%; display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 13px 15px; cursor: pointer; text-align: left;
  background: #fff; border: 1px solid #c2cedd; border-radius: var(--btn-radius);
  font-family: Inter, sans-serif;
}
.fit-trigger:focus-visible { outline: 3px solid rgba(26, 95, 180, .35); outline-offset: 1px; }
.fit-sel { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
.fit-size { font-size: 16px; font-weight: 700; color: var(--ink); }
.fit-meta { font-size: 13px; color: var(--ink-soft); }
.badge-oem { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 999px; background: #e7f4ec; color: #1b6b3a; font-size: 12px; font-weight: 700; }
.badge-oem svg { flex: 0 0 auto; }
.fit-list { position: absolute; z-index: 20; top: calc(100%% + 6px); left: 0; right: 0; margin: 0; padding: 6px; list-style: none; background: #fff; border: 1px solid var(--line); border-radius: var(--radius); box-shadow: 0 14px 30px -12px rgba(10, 22, 40, .34); }
.fit-list[hidden] { display: none; }
.fit-opt { width: 100%%; display: block; padding: 10px 12px; text-align: left; background: none; border: 0; border-radius: var(--btn-radius); cursor: pointer; font-family: Inter, sans-serif; }
.fit-opt:hover, .fit-opt:focus-visible { background: #f3f6fb; }
.fit-opt.is-on { background: #eef3fa; }
.opt-size { display: block; font-size: 15px; font-weight: 600; color: var(--ink); }
.opt-oem { margin-left: 6px; padding: 2px 8px; border-radius: 999px; background: #e7f4ec; color: #1b6b3a; font-size: 11px; font-weight: 700; }
.opt-meta { display: block; margin-top: 2px; font-size: 12.5px; color: var(--ink-soft); }

/* Layout */
.results { padding: 22px 0 46px; }
.results-grid { display: grid; gap: 24px; grid-template-columns: 268px minmax(0, 1fr); align-items: start; }
.filters { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }
.filters > h2 { padding: 15px 18px; border-bottom: 1px solid var(--line); font-size: 16px; font-weight: 600; }
.fgroup { border-bottom: 1px solid var(--line); }
.fgroup:last-child { border-bottom: 0; }
.fgroup > summary { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 14px 18px; cursor: pointer; list-style: none; font-size: 14.5px; font-weight: 600; color: var(--ink); }
.fgroup > summary::-webkit-details-marker { display: none; }
.fgroup > summary svg { flex: 0 0 auto; color: var(--ink-soft); transition: transform .2s ease; }
.fgroup[open] > summary svg { transform: rotate(180deg); }
.fgroup ul { list-style: none; margin: 0; padding: 0 18px 14px; display: grid; gap: 9px; }
.check { display: flex; align-items: center; gap: 9px; font-size: 14px; color: var(--ink-soft); cursor: pointer; }
.check input { width: 17px; height: 17px; accent-color: var(--blue-600); cursor: pointer; }
.check:hover span { color: var(--ink); }

.results-head { display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap; margin-bottom: 16px; }
.results-count { font-size: 14.5px; color: var(--ink-soft); }
.results-count strong { color: var(--ink); font-weight: 600; }
.sort { display: flex; align-items: center; gap: 9px; font-size: 14px; color: var(--ink-soft); }
.sort select { height: 42px; padding: 0 12px; font-family: Inter, sans-serif; font-size: 14.5px; color: var(--ink); background: #fff; border: 1px solid #c2cedd; border-radius: var(--btn-radius); }

.p-grid { list-style: none; margin: 0; padding: 0; display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(236px, 1fr)); }
.p-card { display: flex; flex-direction: column; height: 100%%; padding: 14px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); transition: border-color .18s ease, box-shadow .18s ease; }
.p-card:hover { border-color: var(--blue-600); box-shadow: 0 6px 18px -8px rgba(26, 95, 180, .3); }
.p-media { position: relative; display: flex; align-items: center; justify-content: center; height: 232px; margin-bottom: 10px; }
.p-photo { width: 100%%; height: 100%%; object-fit: contain; mix-blend-mode: multiply; }
.p-stock { position: absolute; top: 9px; right: 9px; display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 999px; background: #e7f4ec; color: #1b6b3a; font-size: 11.5px; font-weight: 700; }
.p-stock::before { content: ""; width: 6px; height: 6px; border-radius: 50%%; background: #1f9254; }
.p-card { position: relative; overflow: hidden; }
.p-offer {
  position: absolute; z-index: 2; top: 0; left: 0;
  width: 128px; height: 128px; pointer-events: none;
  overflow: hidden;
}
.p-offer > span {
  position: absolute; top: 26px; left: -40px;
  display: block; width: 168px; padding: 6px 0;
  transform: rotate(-45deg);
  background: #c82026; color: #fff;
  font-size: 11.5px; font-weight: 700; letter-spacing: .2px; text-align: center;
  box-shadow: 0 2px 6px rgba(10, 22, 40, .22);
}
.p-oe { position: absolute; top: 2px; right: 4px; display: inline-flex; align-items: center; justify-content: center; }
.p-oe img { width: 26px; height: 26px; object-fit: contain; }
.p-top { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.p-brand img { max-width: 104px; max-height: 28px; width: auto; object-fit: contain; }
.p-wish {
  flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; padding: 0; cursor: pointer;
  background: #fff; border: 1px solid var(--line); border-radius: var(--btn-radius);
  color: var(--ink-soft); transition: color .16s ease, border-color .16s ease, background .16s ease;
}
.p-wish:hover, .p-wish:focus-visible { color: #c82026; border-color: #e7b7b9; background: #fdf4f4; }
.p-wish[aria-pressed="true"] { color: #c82026; border-color: #e7b7b9; background: #fdf4f4; }
.p-wish[aria-pressed="true"] svg { fill: #c82026; }
.p-name { margin: 10px 0 0; font-size: 15px; font-weight: 600; line-height: 1.35; }
.p-name a { color: var(--ink); }
.p-name a:hover { color: var(--blue-700); }
.p-size { margin: 5px 0 0; font-family: "Space Grotesk", sans-serif; font-size: 14px; font-weight: 600; color: var(--ink-soft); }
.p-avail { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 10px; }
.p-instock { display: inline-flex; align-items: center; gap: 5px; min-width: 0; font-size: 12.5px; font-weight: 600; color: #1b6b3a; }
.p-instock svg { flex: 0 0 auto; }
.p-stores { flex: 0 0 auto; padding: 0; background: none; border: 0; cursor: pointer; font-family: Inter, sans-serif; font-size: 12.5px; font-weight: 600; color: var(--blue-700); text-decoration: underline; text-underline-offset: 3px; }
.p-stores:hover, .p-stores:focus-visible { color: var(--blue-900); }
.p-qty { display: flex; align-items: center; gap: 8px; margin-top: 10px; }
.qty-label { font-size: 12.5px; font-weight: 600; color: var(--ink-soft); }
.qty-box { display: inline-flex; align-items: center; border: 1px solid #c2cedd; border-radius: var(--btn-radius); overflow: hidden; }
.qty-btn { width: 26px; height: 28px; background: #f7f9fc; border: 0; cursor: pointer; font-size: 14px; line-height: 1; color: var(--ink); }
.qty-btn:hover { background: #eef3fa; color: var(--blue-900); }
.qty-input { width: 32px; height: 28px; border: 0; border-left: 1px solid #c2cedd; border-right: 1px solid #c2cedd; text-align: center; font-family: Inter, sans-serif; font-size: 13px; font-weight: 600; color: var(--ink); -moz-appearance: textfield; }
.qty-input::-webkit-outer-spin-button, .qty-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.qty-input:focus-visible { outline: 2px solid rgba(26, 95, 180, .4); outline-offset: -2px; }
.p-foot { margin-top: auto; padding-top: 13px; display: flex; flex-direction: column; gap: 11px; }
.p-price { display: flex; align-items: baseline; gap: 6px; }
.p-amount { font-family: "Space Grotesk", sans-serif; font-size: 24px; font-weight: 700; line-height: 1; color: #28a745; }
.p-unit { font-size: 12.5px; font-weight: 600; color: var(--ink-soft); }
.p-actions { display: flex; gap: 8px; }
.p-cta, .p-pm {
  flex: 1 1 0; min-width: 0;
  display: inline-flex; align-items: center; justify-content: center;
  height: 44px; padding: 0 10px; border-radius: var(--btn-radius);
  font-family: Inter, sans-serif; font-size: 13.5px; font-weight: 600; white-space: nowrap;
  cursor: pointer;
}
.p-cta { background-image: linear-gradient(to right bottom, #1a5fb4, #2563eb, #1a5fb4); color: #fff; border: 0; }
.p-cta:hover, .p-cta:focus-visible { background-image: linear-gradient(to right bottom, #154d93, #1d4fd8, #154d93); color: #fff; }
.p-pm { background: #fff; border: 1px solid var(--line); color: #4a5868; }
.p-pm:hover, .p-pm:focus-visible { border-color: var(--blue-600); color: var(--blue-900); }

.p-item[hidden] { display: none; }

/* Layout switch */
.head-tools { display: flex; align-items: center; gap: 12px; }
.view-switch { display: inline-flex; border: 1px solid #c2cedd; border-radius: var(--btn-radius); overflow: hidden; }
.view-btn { display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 42px; background: #fff; border: 0; cursor: pointer; color: var(--ink-soft); }
.view-btn + .view-btn { border-left: 1px solid #c2cedd; }
.view-btn:hover { background: #f3f6fb; color: var(--blue-900); }
.view-btn.is-on { background: var(--blue-600); color: #fff; }

/* List layout: image panel on the left, details stacked on the right */
.p-grid.is-list { grid-template-columns: 1fr; gap: 14px; }
.is-list .p-card {
  display: grid; grid-template-columns: 210px minmax(0, 1fr);
  column-gap: 26px; row-gap: 0; align-items: start;
  padding: 0; overflow: hidden;
}
.is-list .p-media {
  grid-row: 1 / 7; grid-column: 1; align-self: stretch;
  height: auto; min-height: 196px; margin-bottom: 0; padding: 16px;
  background: #f7f9fc; border-right: 1px solid var(--line);
}
.is-list .p-top { grid-column: 2; grid-row: 1; margin: 18px 20px 0 0; }
.is-list .p-brand img { max-width: 132px; max-height: 32px; }
.is-list .p-name { grid-column: 2; grid-row: 2; margin: 8px 0 0; font-size: 18px; font-weight: 700; }
.is-list .p-size { grid-column: 2; grid-row: 3; margin: 4px 0 0; font-size: 14.5px; }
.is-list .p-qty { grid-column: 2; grid-row: 4; margin: 12px 0 0; gap: 10px; }
.is-list .qty-label { font-size: 14px; color: var(--ink); }
.is-list .qty-btn { width: 34px; height: 36px; font-size: 17px; }
.is-list .qty-input { width: 42px; height: 36px; font-size: 15px; }
.is-list .p-avail {
  grid-column: 2; grid-row: 5; margin: 12px 20px 0 0;
  padding: 10px 14px; gap: 12px;
  background: #eff6ff; border-left: 4px solid var(--blue-600); border-radius: 0 var(--btn-radius) var(--btn-radius) 0;
}
.is-list .p-instock { font-size: 14px; }
.is-list .p-stores { font-size: 13.5px; }
.is-list .p-foot { grid-column: 2; grid-row: 6; margin: 14px 20px 18px 0; padding-top: 0; gap: 12px; }
.is-list .p-amount { font-size: 26px; }
.is-list .p-unit { font-size: 14px; }
.is-list .p-actions { gap: 12px; }
.is-list .p-cta { flex: 1.25 1 0; height: 46px; font-size: 15px; }
.is-list .p-pm { flex: 1 1 0; height: 46px; font-size: 15px; }
.is-list .p-wish { width: 40px; height: 40px; }
.is-list .p-wish svg { width: 20px; height: 20px; }
.is-list .p-oe { top: 10px; right: 10px; }
.is-list .p-oe img { width: 28px; height: 28px; }

/* Pagination */
.pager { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 26px; }
.pager ol { display: flex; gap: 6px; list-style: none; margin: 0; padding: 0; }
.pager-num, .pager-step {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 40px; height: 40px; padding: 0 13px; border-radius: var(--btn-radius);
  border: 1px solid var(--line); background: #fff;
  font-size: 14px; font-weight: 600; color: var(--ink);
}
.pager-num:hover, .pager-step:hover { border-color: var(--blue-600); color: var(--blue-900); }
.pager-num.is-on { background: var(--blue-600); border-color: var(--blue-600); color: #fff; }
.pager-step.is-off { opacity: .45; pointer-events: none; }
.pager[hidden] { display: none; }
.no-match { margin: 0; padding: 26px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); font-size: 15px; color: var(--ink-soft); }
.no-match[hidden] { display: none; }

/* Store stock sheet */
.stock-sheet { width: min(94vw, 560px); max-width: none; max-height: 86vh; padding: 0; border: 0; border-radius: var(--radius); background: var(--surface); overflow: hidden; }
.stock-sheet::backdrop { background: rgba(11, 20, 32, .55); }
.stock-inner { display: flex; flex-direction: column; max-height: 86vh; }
.stock-head { flex: 0 0 auto; display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; padding: 18px 20px; border-bottom: 1px solid var(--line); }
.stock-head h2 { font-size: 17px; font-weight: 600; }
.stock-head p { margin: 3px 0 0; font-size: 13.5px; color: var(--ink-soft); }
.stock-scroll { flex: 1 1 auto; min-height: 0; overflow-y: auto; overscroll-behavior: contain; padding: 10px 12px calc(16px + env(safe-area-inset-bottom)); }
.stock-scroll ul { list-style: none; margin: 0; padding: 0; }
.store-row { display: grid; align-items: center; gap: 10px; grid-template-columns: minmax(0, 1fr) auto auto; padding: 12px 10px; border-radius: var(--btn-radius); }
.store-row:hover { background: #f7f9fc; }
.store-name a { font-size: 15px; font-weight: 600; color: var(--ink); }
.store-name a:hover { color: var(--blue-700); }
.store-state { padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; white-space: nowrap; }
.store-state.ok { background: #e7f4ec; color: #1b6b3a; }
.store-state.wait { background: #fdf1e3; color: #8a5213; }
.store-tel { font-size: 14px; font-weight: 600; color: var(--blue-700); white-space: nowrap; }
.stock-foot { flex: 0 0 auto; padding: 13px 20px; border-top: 1px solid var(--line); font-size: 13px; color: var(--ink-soft); }

.filter-toggle { display: none; }

@media (max-width: 900px) {
  .results-grid { grid-template-columns: 1fr; }
  .filter-toggle {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%%;
    padding: 13px 18px; margin-bottom: 14px; cursor: pointer;
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    font-family: Inter, sans-serif; font-size: 15px; font-weight: 600; color: var(--ink);
  }
  .filters[hidden] { display: none; }
}
@media (max-width: 640px) {
  .veh h1 { font-size: 21px; }
  .veh { padding: 20px 0 22px; }
  .spec-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 14px; }
  .spec-cell { padding: 12px 14px 4px 14px; border-top: 1px solid rgba(255, 255, 255, .22); }
  .spec-cell:nth-child(-n+2) { border-top: 0; }
  .spec-cell:nth-child(odd) { border-left: 0; padding-left: 0; }
  .spec-grid dd { font-size: 16px; }
  .p-grid { grid-template-columns: 1fr; gap: 14px; }
  .p-card { padding: 11px; }
  .p-media { height: 232px; }
  .p-oe img { width: 24px; height: 24px; }
  .p-cta, .p-pm { height: 46px; font-size: 14.5px; }
  .head-tools { width: 100%%; justify-content: space-between; }
  .is-list .p-card { display: flex; flex-direction: column; align-items: stretch; padding: 11px; overflow: visible; }
  .is-list .p-media { min-height: 0; height: 232px; margin-bottom: 10px; padding: 0; background: none; border-right: 0; }
  .is-list .p-top { margin-top: 0; }
  .is-list .p-brand img { max-width: 104px; max-height: 28px; }
  .is-list .p-name { font-size: 15px; margin-top: 10px; }
  .is-list .p-size { font-size: 14px; }
  .is-list .p-qty { margin: 10px 0 0; gap: 8px; }
  .is-list .qty-btn { width: 26px; height: 28px; font-size: 14px; }
  .is-list .qty-input { width: 32px; height: 28px; font-size: 13px; }
  .is-list .p-avail { margin: 10px 0 0; padding: 0; background: none; border-left: 0; border-radius: 0; gap: 8px; }
  .is-list .p-instock, .is-list .p-stores { font-size: 12.5px; }
  .is-list .p-foot { margin: auto 0 0; padding-top: 13px; gap: 11px; }
  .is-list .p-amount { font-size: 24px; }
  .is-list .p-unit { font-size: 12.5px; }
  .is-list .p-cta, .is-list .p-pm { height: 46px; font-size: 14.5px; flex: 1 1 0; }
  .is-list .p-wish { width: 36px; height: 36px; }
  .is-list .p-oe { top: 2px; right: 4px; }
  .p-stock-check { font-size: 12px; }
  .stock-sheet { width: 100%%; max-width: none; margin: auto auto 0; border-radius: var(--radius) var(--radius) 0 0; }
  .store-row { grid-template-columns: minmax(0, 1fr) auto; row-gap: 6px; }
  .store-tel { grid-column: 1 / -1; }
}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

%(chromehtml)s

%(menuhtml)s

<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb">
    <div class="wrap">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="tyres.html">Tyres</a></li>
        <li><a href="%(makehref)s">%(make)s</a></li>
        <li><a href="%(modelhref)s">%(model)s</a></li>
        <li aria-current="page">%(crumbveh)s</li>
      </ol>
    </div>
  </nav>

  <section class="veh">
    <div class="wrap">
      <div class="veh-top">
        <h1>%(make)s %(model)s %(trim)s</h1>
        <a class="change-veh" href="%(modelhref)s">
          <svg viewBox="0 0 20 20" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><path d="M3 10a7 7 0 0 1 12-4.9M17 10a7 7 0 0 1-12 4.9" stroke-linecap="round"/><path d="M15 2v3.5h-3.5M5 18v-3.5h3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Not your car? Change model
        </a>
      </div>
      <dl class="spec-grid">
        <div class="spec-cell">
          <dt>Engine</dt>
          <dd>%(fuel)s, %(hp)d hp</dd>
        </div>
        <div class="spec-cell">
          <dt>Built</dt>
          <dd>%(years)s</dd>
        </div>
        <div class="spec-cell">
          <dt>Bolt pattern</dt>
          <dd>%(bolt)s</dd>
        </div>
        <div class="spec-cell">
          <dt>Centre bore</dt>
          <dd>%(bore)s</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="fitment" aria-labelledby="fitHeading">
    <div class="wrap">
      <div class="fit-card">
        <div class="fit-head">
          <div>
            <h2 id="fitHeading">Select fitment</h2>
            <p>Choose the fitment that matches your vehicle.</p>
          </div>
        </div>
        <div class="fit-picker">
          <button class="fit-trigger" type="button" id="fitTrigger" aria-haspopup="listbox" aria-expanded="false" aria-controls="fitList">
            <span class="fit-sel">
              <span class="fit-size" id="fitSize">%(fitsize)s</span>
              <span class="fit-meta" id="fitMeta">%(fitmeta)s</span>
            </span>
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <ul class="fit-list" id="fitList" role="listbox" aria-labelledby="fitHeading" hidden>
%(fitoptions)s
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="results" aria-label="Tyre results">
    <div class="wrap">
      <div class="results-grid">
        <button class="filter-toggle" type="button" id="filterToggle" aria-expanded="false" aria-controls="filterPanel">
          <svg viewBox="0 0 20 20" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><path d="M2 5h16M5 10h10M8 15h4" stroke-linecap="round"/></svg>
          Filters
        </button>

        <aside class="filters" id="filterPanel">
          <h2>Filters</h2>

          <details class="fgroup" open>
            <summary>Brand<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(brandchecks)s
            </ul>
          </details>

          <details class="fgroup" open>
            <summary>Price range<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(pricechecks)s
            </ul>
          </details>

          <details class="fgroup" open>
            <summary>Tyre category<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(catchecks)s
            </ul>
          </details>

          <details class="fgroup">
            <summary>Vehicle type<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(vehchecks)s
            </ul>
          </details>

          <details class="fgroup">
            <summary>Speed rating<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(speedchecks)s
            </ul>
          </details>

          <details class="fgroup">
            <summary>Size<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg></summary>
            <ul>
%(sizechecks)s
            </ul>
          </details>
        </aside>

        <div>
          <div class="results-head">
            <p class="results-count">Showing <strong id="shownCount">%(count)d</strong> of <strong>%(total)d</strong> tyres that fit</p>
            <div class="head-tools">
              <label class="sort" for="sortBy">Sort by
                <select id="sortBy">
                  <option value="price-asc">Price, low to high</option>
                  <option value="price-desc">Price, high to low</option>
                  <option value="brand">Brand</option>
                </select>
              </label>
              <div class="view-switch" role="group" aria-label="Result layout">
                <button class="view-btn is-on" type="button" data-view="grid" aria-pressed="true" aria-label="Grid view">
                  <svg viewBox="0 0 20 20" width="17" height="17" fill="currentColor" aria-hidden="true" focusable="false"><rect x="2.5" y="2.5" width="6" height="6" rx="1.4"/><rect x="11.5" y="2.5" width="6" height="6" rx="1.4"/><rect x="2.5" y="11.5" width="6" height="6" rx="1.4"/><rect x="11.5" y="11.5" width="6" height="6" rx="1.4"/></svg>
                </button>
                <button class="view-btn" type="button" data-view="list" aria-pressed="false" aria-label="List view">
                  <svg viewBox="0 0 20 20" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true" focusable="false"><path d="M3 5h14M3 10h14M3 15h14" stroke-linecap="round"/></svg>
                </button>
              </div>
            </div>
          </div>
          <ul class="p-grid" role="list" id="productGrid">
%(products)s
          </ul>
          <nav class="pager" id="pager" aria-label="Pagination">
            <a class="pager-step is-off" href="?p=1" id="pagerPrev" aria-disabled="true">Previous</a>
            <ol>
              <li><a class="pager-num is-on" href="?p=1" data-page="1" aria-current="page">1</a></li>
              <li><a class="pager-num" href="?p=2" data-page="2">2</a></li>
            </ol>
            <a class="pager-step" href="?p=2" id="pagerNext">Next</a>
          </nav>
          <p class="no-match" id="noMatch" hidden>No tyres match those filters. Clear one and try again, or call your nearest workshop and we will check stock for you.</p>
        </div>
      </div>
    </div>
  </section>
</main>

<dialog class="stock-sheet" id="stockSheet" aria-labelledby="stockTitle">
  <div class="stock-inner">
    <div class="stock-head">
      <div>
        <h2 id="stockTitle">Stock by workshop</h2>
        <p id="stockSub"></p>
      </div>
      <button class="icon-btn" type="button" id="stockClose" aria-label="Close">
        <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </button>
    </div>
    <div class="stock-scroll">
      <ul role="list">
%(storerows)s
      </ul>
    </div>
    <p class="stock-foot">Stock moves between workshops daily. Call ahead and we will hold a set for you.</p>
  </div>
</dialog>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-cols">
      <div>
        <p class="foot-h">Shop tyres</p>
        <ul>
          <li><a href="%(vehicleshref)s">Tyres by vehicle</a></li>
          <li><a href="/tyres/sizes">Tyres by size</a></li>
          <li><a href="/tyres/brand">Tyres by brand</a></li>
          <li><a href="tyres.html">All tyres</a></li>
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
          <li><a href="/reviews">Reviews</a></li>
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

<script>
%(menujs)s
(function () {
  var FITS = %(fitdata)s;

  // Fitment picker
  var trigger = document.getElementById('fitTrigger');
  var list = document.getElementById('fitList');
  if (trigger && list) {
    function setOpen(on) {
      list.hidden = !on;
      trigger.setAttribute('aria-expanded', on ? 'true' : 'false');
    }
    trigger.addEventListener('click', function () { setOpen(list.hidden); });
    document.addEventListener('click', function (e) {
      if (!trigger.contains(e.target) && !list.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !list.hidden) { setOpen(false); trigger.focus(); }
    });
    Array.prototype.forEach.call(list.querySelectorAll('.fit-opt'), function (opt) {
      opt.addEventListener('click', function () {
        var size = opt.getAttribute('data-size');
        var f = FITS[size];
        Array.prototype.forEach.call(list.querySelectorAll('.fit-opt'), function (o) {
          o.classList.remove('is-on');
          o.setAttribute('aria-selected', 'false');
        });
        opt.classList.add('is-on');
        opt.setAttribute('aria-selected', 'true');
        document.getElementById('fitSize').textContent = size;
        document.getElementById('fitMeta').textContent = f.meta;
        setOpen(false);
        trigger.focus();
      });
    });
  }

  // Filters and sort
  var grid = document.getElementById('productGrid');
  var items = Array.prototype.slice.call(grid.querySelectorAll('.p-item'));
  var shown = document.getElementById('shownCount');
  var noMatch = document.getElementById('noMatch');

  function picked(group) {
    return Array.prototype.slice.call(
      document.querySelectorAll('input[name="' + group + '"]:checked')
    ).map(function (i) { return i.value; });
  }

  var page = 1;
  var pager = document.getElementById('pager');

  function apply() {
    var b = picked('brand'), p = picked('price'), c = picked('cat'),
        v = picked('veh'), sp = picked('speed'), sz = picked('size');
    var filtering = b.length || p.length || c.length || v.length || sp.length || sz.length;
    var n = 0;
    items.forEach(function (li) {
      var size = li.getAttribute('data-size');
      var ok = (!b.length || b.indexOf(li.getAttribute('data-brand')) > -1)
        && (!p.length || p.indexOf(li.getAttribute('data-price')) > -1)
        && (!c.length || c.indexOf(li.getAttribute('data-cat')) > -1)
        && (!v.length || v.indexOf('Passenger') > -1)
        && (!sp.length || sp.indexOf(size.slice(-1)) > -1)
        && (!sz.length || sz.indexOf(size) > -1);
      if (ok) n++;
      // while filtering, paging is suspended so every match is visible
      li.hidden = !ok || (!filtering && parseInt(li.getAttribute('data-page'), 10) !== page);
      li.setAttribute('data-match', ok ? '1' : '0');
    });
    shown.textContent = filtering ? n : items.filter(function (li) { return !li.hidden; }).length;
    noMatch.hidden = n > 0;
    if (pager) pager.hidden = !!filtering;
    loadVisible();
  }

  // An image deferred with loading="lazy" while its card was display:none does not resume
  // when the card is shown again, so nudge anything visible that has not loaded.
  function loadVisible() {
    items.forEach(function (li) {
      if (li.hidden) return;
      Array.prototype.forEach.call(li.querySelectorAll('img[loading="lazy"]'), function (img) {
        if (!img.complete || img.naturalWidth === 0) img.loading = 'eager';
      });
    });
  }

  function goTo(n) {
    page = n;
    Array.prototype.forEach.call(document.querySelectorAll('.pager-num'), function (a) {
      var on = parseInt(a.getAttribute('data-page'), 10) === n;
      a.classList.toggle('is-on', on);
      if (on) { a.setAttribute('aria-current', 'page'); } else { a.removeAttribute('aria-current'); }
    });
    var prev = document.getElementById('pagerPrev');
    var next = document.getElementById('pagerNext');
    if (prev) prev.classList.toggle('is-off', n === 1);
    if (next) next.classList.toggle('is-off', n === 2);
    apply();
    var head = document.querySelector('.results-head');
    if (head) head.scrollIntoView({ block: 'start' });
  }

  Array.prototype.forEach.call(document.querySelectorAll('.pager-num, .pager-step'), function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var n = a.getAttribute('data-page');
      if (!n) n = a.id === 'pagerNext' ? 2 : 1;
      goTo(parseInt(n, 10));
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.filters input[type=checkbox]'), function (i) {
    i.addEventListener('change', apply);
  });

  goTo(1);

  var sortBy = document.getElementById('sortBy');
  if (sortBy) {
    sortBy.addEventListener('change', function () {
      var v = sortBy.value;
      var sorted = items.slice().sort(function (a, b) {
        if (v === 'brand') return a.getAttribute('data-brand').localeCompare(b.getAttribute('data-brand'));
        var pa = parseFloat(a.querySelector('.p-amount').textContent.replace('$', ''));
        var pb = parseFloat(b.querySelector('.p-amount').textContent.replace('$', ''));
        return v === 'price-desc' ? pb - pa : pa - pb;
      });
      sorted.forEach(function (li) { grid.appendChild(li); });
    });
  }

  // Quantity steppers
  Array.prototype.forEach.call(document.querySelectorAll('.qty-box'), function (box) {
    var input = box.querySelector('.qty-input');
    Array.prototype.forEach.call(box.querySelectorAll('.qty-btn'), function (btn) {
      btn.addEventListener('click', function () {
        var step = parseInt(btn.getAttribute('data-step'), 10);
        var min = parseInt(input.min, 10) || 1;
        var max = parseInt(input.max, 10) || 99;
        var next = (parseInt(input.value, 10) || min) + step;
        input.value = Math.min(max, Math.max(min, next));
      });
    });
    input.addEventListener('change', function () {
      var min = parseInt(input.min, 10) || 1;
      var max = parseInt(input.max, 10) || 99;
      var v = parseInt(input.value, 10);
      input.value = isNaN(v) ? min : Math.min(max, Math.max(min, v));
    });
  });

  // Store stock sheet
  var sheet = document.getElementById('stockSheet');
  var sheetSub = document.getElementById('stockSub');
  var sheetClose = document.getElementById('stockClose');
  if (sheet) {
    var sheetScroll = 0;
    var sheetOpener = null;
    function lockSheet() {
      sheetScroll = window.scrollY || 0;
      document.body.style.top = '-' + sheetScroll + 'px';
      document.body.classList.add('body-scroll-locked');
    }
    function unlockSheet() {
      document.body.classList.remove('body-scroll-locked');
      document.body.style.top = '';
      var prev = document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, sheetScroll);
      document.documentElement.style.scrollBehavior = prev;
    }
    function closeSheet() {
      if (sheet.open) { try { sheet.close(); } catch (err) { sheet.removeAttribute('open'); } }
      unlockSheet();
      if (sheetOpener) { sheetOpener.focus(); sheetOpener = null; }
    }
    Array.prototype.forEach.call(document.querySelectorAll('.p-stores'), function (btn) {
      btn.addEventListener('click', function () {
        if (sheet.open) return;
        sheetOpener = btn;
        sheetSub.textContent = btn.getAttribute('data-product');
        lockSheet();
        try { sheet.showModal(); } catch (err) { unlockSheet(); return; }
        var first = sheet.querySelector('a');
        if (first) first.focus();
      });
    });
    if (sheetClose) sheetClose.addEventListener('click', closeSheet);
    sheet.addEventListener('close', unlockSheet);
    sheet.addEventListener('cancel', function () { window.setTimeout(closeSheet, 0); });
    sheet.addEventListener('click', function (e) { if (e.target === sheet) closeSheet(); });
  }

  // Grid and list switch
  Array.prototype.forEach.call(document.querySelectorAll('.view-btn'), function (btn) {
    btn.addEventListener('click', function () {
      var list = btn.getAttribute('data-view') === 'list';
      Array.prototype.forEach.call(document.querySelectorAll('.view-btn'), function (b) {
        var on = b === btn;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      grid.classList.toggle('is-list', list);
    });
  });

  // Wishlist toggle
  Array.prototype.forEach.call(document.querySelectorAll('.p-wish'), function (btn) {
    btn.addEventListener('click', function () {
      btn.setAttribute('aria-pressed', btn.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    });
  });

  // Mobile filter toggle
  var ft = document.getElementById('filterToggle');
  var panel = document.getElementById('filterPanel');
  if (ft && panel) {
    function sync() {
      if (window.matchMedia('(max-width: 900px)').matches) {
        var on = ft.getAttribute('aria-expanded') === 'true';
        panel.hidden = !on;
      } else {
        panel.hidden = false;
      }
    }
    ft.addEventListener('click', function () {
      ft.setAttribute('aria-expanded', ft.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
      sync();
    });
    window.addEventListener('resize', sync);
    sync();
  }
})();
</script>
</body>
</html>
''' % {
    'make': VEHICLE['make'], 'model': VEHICLE['model'], 'trim': VEHICLE['trim'],
    'fuel': VEHICLE['fuel'], 'hp': VEHICLE['hp'], 'years': VEHICLE['years'],
    'bolt': VEHICLE['bolt'], 'bore': VEHICLE['bore'],
    'crumbveh': CRUMB_VEHICLE,
    'vehicleshref': VEHICLES_HREF, 'makehref': MAKE_HREF, 'modelhref': MODEL_HREF,
    'breadcrumb': json.dumps(breadcrumb, ensure_ascii=False, indent=2),
    'productlist': json.dumps(product_list, ensure_ascii=False, indent=2),
    'chromecss': chrome_css, 'chromehtml': chrome_html,
    'menuhtml': menu_html, 'menujs': menu_js,
    'fitsize': FITMENTS[0]['size'],
    'fitmeta': '%s · %s · %s' % (FITMENTS[0]['rim'], FITMENTS[0]['et'], FITMENTS[0]['pos']),
    'fitoptions': fitment_options(),
    'fitdata': json.dumps({f['size']: {'meta': '%s · %s · %s' % (f['rim'], f['et'], f['pos']),
                                       'oem': f['oem']} for f in FITMENTS}, ensure_ascii=False),
    'brandchecks': checks('Brand', [(b, s) for b, s in sorted({(p[0], p[6]) for p in PRODUCTS})], 'brand'),
    'pricechecks': checks('Price', PRICE_BRACKETS, 'price'),
    'catchecks': checks('Tyre category', [(c, c.lower().replace(' ', '-')) for c in TYRE_CATEGORIES], 'cat'),
    'vehchecks': checks('Vehicle type', VEHICLE_TYPES, 'veh'),
    'speedchecks': checks('Speed rating', SPEED_RATINGS, 'speed'),
    'sizechecks': checks('Size', SIZES, 'size'),
    'products': product_cards(),
    'storerows': store_rows(),
    'count': PER_PAGE,
    'total': len(PRODUCTS),
}

open(OUT, 'w', encoding='utf-8').write(doc)
print('wrote', OUT, len(doc), 'bytes |', len(PRODUCTS), 'products |', len(FITMENTS), 'fitments')
