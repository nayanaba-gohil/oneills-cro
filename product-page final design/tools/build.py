"""Builds the two product page previews and their structured data. Run from the product-page folder:
    python3 tools/build.py
Deliverables (Round 16): final-multi.html (A + "Current offers" carousel) and final-single.html (B + carousel).
Round 22: final-wheel.html (C, ROH Apollo wheel, src/product-content-wheel.html, schema/product-jsonld-wheel.html).
A) multi-image product with reviews (src/product-content.html, schema/product-jsonld.html)
B) single-image product with size options and no reviews (src/product-content-single.html, schema/product-jsonld-single.html)
Also built without the carousel: preview.html and preview-single.html. src/promo-ticker.html is kept but unused (no ticker on any page).
Shares the homepage's icon sprite, footer (header is product-page/src/header.html, a copy of the homepage header with a brand blue utility bar), components and brand tokens (../homepage), so the design stays in step.
"""
import base64, html, json, pathlib, re

P = pathlib.Path(__file__).resolve().parent.parent          # product-page/
HOME = P.parent if (P.parent / 'tools' / 'build.py').exists() else (P.parent / 'homepage')
r = lambda base, rel: (base / rel).read_text()
B = 'https://oneillstyres.com.au'
# Live product images from oneillstyres.com.au (copied into assets/live for the self-contained preview)
LIVE = B + "/media/catalog/product/cache/74c1057f7991b4edb2bc7bdaa94de933"
PH = [LIVE + "/9/0/905936f60175b8bc4f699b30fef0db8ffe1205cecdab350297ebdd2e3d399cf5_17.webp", LIVE + "/9/0/905936f60175b8bc4f699b30fef0db8ffe1205cecdab350297ebdd2e3d399cf5_17.webp", LIVE + "/a/1/a1641cbb57784eaf4cd2bd82393c248d499d94d04ed4ebe294ab6814431999b6_13.webp"]

WHEEL_IMGS = [LIVE + "/r/o/roh-apollo-mb.webp"]
FINISHES = [("Matte Black", "matte-black", "MB"), ("Machined", "machined", "FM")]

# ---------- Two required products (tyre and wheel) ----------
PAGES = [
  dict(  # Tyre: reviews, multi-image gallery, promotion badge + carousel, size dropdown selector
    content='src/product-content.html', schema='schema/product-jsonld.html', out='tyres.html', aggregate=True, carousel=True,
    product=dict(
      name="Yokohama ADVAN A052",
      url=B + "/yokohama-advan-a052",
      model="ADVAN A052",
      gtin13=None,  # Magento EAN/barcode attribute. Only output when present (13 digits)
      mpn=None,     # Manufacturer part number attribute. Only output when present
      sku="A052-1856013", brand="Yokohama", category="Car tyres", price="305.00",
      description=("The ADVAN A052 is Yokohama's street-legal motorsport tyre, engineered for ultimate dry and wet grip, extreme cornering stability and precision steering response."),
      images=["assets/live/yokohama-advan-a052.png"],
      rating=("4.8", "6"),  # only output when the product has real, approved reviews
      specs=[("Tyre size", "185/60R13"), ("Width", "185", "MMT"), ("Aspect ratio", "60", None), ("Rim diameter", "13", "INH"),
             ("Load index", "80"), ("Speed rating", "V"), ("Load type", "Standard load"), ("Run-flat", "No"),
             ("Season", "Summer / Motorsport"), ("Tread pattern", "ADVAN A052")]),
    crumbs=[("Home", B + "/"), ("Tyres", B + "/tyres"), ("Yokohama tyres", B + "/tyres/brand/yokohama"), ("ADVAN A052", None)],
    title_name="Yokohama ADVAN A052", pm=("Yokohama ADVAN A052", "A052-1856013", "185/60R13 80V"),
    desc="Yokohama ADVAN A052 street-legal motorsport tyre. Free fitting, balancing and eco tyre disposal at 8 O'Neills stores."),
  dict(  # Wheel: empty reviews, single image, no promotion, finish/size options
    content='src/product-content-wheel.html', schema='schema/product-jsonld-wheel.html', out='wheels.html', aggregate=True, wheel=True, carousel=False,
    product=dict(
      name="ROH Apollo 4WD wheel", url=B + "/apollo", model="Apollo", gtin13=None, mpn=None,
      sku=None,   # parent SKU of the configurable product: output it when Magento has one (children carry the APO... SKUs)
      brand="ROH", category="4WD wheels", price="429.00",
      description=("The Apollo is a clean, minimalist spoke wheel from the exclusive LITEFORGED series, made for 4WD and off-road use. "
                   "Flow-formed construction reduces weight for better performance without compromising strength. Available in 6x139.7 fitments only, in a Machined or Matte Black finish."),
      images=WHEEL_IMGS[:1], rating=("4.9", "6"),
      specs=[("Stud pattern (PCD)", "6x139.7"), ("Rim width", "9", "INH"), ("Rim diameter", "17, 18", "INH"), ("Offset", "+12, +25, +40", "MMT"),
             ("Wheel finish", "Matte Black, Machined"), ("Wheel type", "4WD / off-road"), ("Construction", "Flow-formed (LITEFORGED series)"), ("Load rating", "1500 kg per wheel")]),
    crumbs=[("Home", B + "/"), ("Wheels", B + "/wheels"), ("ROH Apollo", None)],
    title="ROH Apollo 4WD Wheel 17 and 18 inch 6x139.7 | O'Neills",
    pm=("ROH Apollo", "APO18925MB", "18x9 6x139.7 +25, Matte Black"),
    desc="ROH Apollo flow-formed 4WD wheels in 17 and 18 inch, 6x139.7, Machined or Matte Black. Fitted at 8 O'Neills stores in Newcastle and the Hunter.")
]

home_build = r(HOME, 'tools/build.py')
tw = re.search(r'<script>\ntailwind\.config = .*?</script>\n', home_build, re.S).group(0)   # same brand tokens as the homepage
clean = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def prop(s):
    d = {"@type": "PropertyValue", "name": s[0], "value": s[1]}
    if len(s) > 2 and s[2]: d["unitCode"] = s[2]
    return d

def build(pg):
    # Optional extras: pg['ticker'] injects src/promo-ticker.html before the header; pg['carousel'] injects src/promo-carousel.html before the tabs section
    PRODUCT, CRUMBS = pg['product'], pg['crumbs']
    content = r(P, pg['content'])
    # Price match dialog (src/pricematch.html) is shared by both pages: product name, SKU and default size are filled in here
    pm = r(P, 'src/pricematch.html')
    if pg.get('wheel'):
        # Wheel wording, and the SKU follows the selected finish (ohPriceMatch.onSize reads detail.sku)
        for a, b in (('this tyre cheaper', 'this wheel cheaper'), ('identical tyres', 'identical wheels'),
                     ('<input type="hidden" name="sku" value="{{sku}}">', '<input type="hidden" name="sku" :value="sku" value="{{sku}}">')):
            assert a in pm, a
            pm = pm.replace(a, b)
    for k, v in zip(('name', 'sku', 'size'), pg['pm']):
        pm = pm.replace('{{' + k + '}}', html.escape(v, quote=True))
    assert '<!-- @include pricematch -->' in content
    content = content.replace('<!-- @include pricematch -->', pm.strip('\n').lstrip(), 1)
    paylater = r(P, 'src/paylater-modal.html')
    assert '<!-- @include paylater -->' in content
    content = content.replace('<!-- @include paylater -->', paylater.strip('\n').lstrip(), 1)
    # Availability from the per-store sample data (data-stores): InStock if any store has stock, else BackOrder
    stores = json.loads(re.search(r"data-stores='(\[.*?\])'", content).group(1))
    avail = "https://schema.org/" + ("InStock" if any((s.get("qty") or 0) > 0 for s in stores) else "BackOrder")
    faq = [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
           for q, a in re.findall(r'<summary[^>]*>(.*?)<svg.*?</summary>\s*<p[^>]*>(.*?)</p>', content, re.S)]
    common = {"priceCurrency": "AUD", "availability": avail, "itemCondition": "https://schema.org/NewCondition",
              # Return window and category are NOT set: they need client confirmation (DEV-NOTES). availableAtOrFrom is omitted:
              # it expects a Place, and the organization @id is not one.
              "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "AU", "merchantReturnLink": B + "/terms"},
              "seller": {"@type": "AutomotiveBusiness", "@id": B + "/#organization", "name": "O'Neills Tyre & Autocare"}}
    if pg['aggregate']:
        # Configurable product: one AggregateOffer across the sizes (data-sizes on the buy box)
        sizes = json.loads(re.search(r"data-sizes='(\[.*?\])'", content).group(1))
        # Charged price = offer (Magento special_price while active) else regular price. Sizes with an offer also carry the regular price
        # as a StrikethroughPrice (Google merchant listing sale price markup).
        eff = lambda s: s.get("offer") or s["price"]
        if pg.get('wheel'):
            # One offer per child product: size x finish (10). Child URL: /roh-apollo-{finish}-{d}x{w}-{pcd without the dot}-{offset}-{sku}.
            per = [{"@type": "Offer", "name": "ROH Apollo %s %s" % (fn, s["label"]), "sku": s["sku"] + sfx,
                    "url": "%s/roh-apollo-%s-%dx%d-6x1397-%d-%s%s" % (B, slug, s["d"], s["w"], s["off"], s["sku"].lower(), sfx.lower()),
                    "price": "%.2f" % s["price"], "priceCurrency": "AUD"} for s in sizes for fn, slug, sfx in FINISHES]
            sizes = per
            eff = lambda s: float(s["price"])
        prices = [eff(s) for s in sizes]
        per = per if pg.get('wheel') else []
        for s in ([] if pg.get('wheel') else sizes):
            o = {"@type": "Offer", "name": PRODUCT["model"] + " " + s["label"], "price": "%.2f" % eff(s), "priceCurrency": "AUD"}
            if s.get("offer"):
                o["priceSpecification"] = [{"@type": "UnitPriceSpecification", "priceType": "https://schema.org/StrikethroughPrice", "price": "%.2f" % s["price"], "priceCurrency": "AUD"}]
            per.append(o)
        offers = dict({"@type": "AggregateOffer", "url": PRODUCT["url"], "lowPrice": "%.2f" % min(prices), "highPrice": "%.2f" % max(prices), "offerCount": len(sizes), "offers": per}, **common)
    else:
        offers = dict({"@type": "Offer", "url": PRODUCT["url"], "price": PRODUCT["price"]}, **common)
    product = {
        "@type": "Product", "@id": PRODUCT["url"] + "#product", "url": PRODUCT["url"], "name": PRODUCT["name"], "model": PRODUCT["model"], "description": PRODUCT["description"],
        "image": PRODUCT["images"], "category": PRODUCT["category"],
        "brand": {"@type": "Brand", "name": PRODUCT["brand"]},
        "additionalProperty": [prop(s) for s in PRODUCT["specs"]],
        "offers": offers,
    }
    if PRODUCT.get("sku"): product["sku"] = PRODUCT["sku"]
    for k in ("gtin13", "mpn"):
        if PRODUCT.get(k): product[k] = PRODUCT[k]
    if PRODUCT["rating"]:
        product["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": PRODUCT["rating"][0], "reviewCount": PRODUCT["rating"][1]}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i + 1, "name": n}, **({"item": u} if u else {})) for i, (n, u) in enumerate(CRUMBS)]}
    graph = [product, crumbs] + ([{"@type": "FAQPage", "mainEntity": faq}] if faq else [])
    schema = ('<!-- Product page structured data. Product (with spec properties and the AUD offer), BreadcrumbList and FAQPage.\n'
              '     aggregateRating only when the product has real, approved product reviews (never Google store ratings). -->\n'
              '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n</script>\n')
    (P / pg['schema']).write_text(schema)

    title = pg.get('title') or f"{pg['title_name']} Tyre | O'Neills"   # {Brand} {Model} {Size} {LoadSpeed} Tyre | O'Neills (configurable products: no size)
    desc = pg['desc']
    head = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{PRODUCT['url']}">
<meta property="og:type" content="product">
<meta property="og:locale" content="en_AU">
<meta property="og:site_name" content="O'Neills Tyre &amp; Autocare">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{PRODUCT['url']}">
<meta property="og:image" content="{html.escape(PRODUCT['images'][0])}">
<meta property="product:price:amount" content="{PRODUCT['price']}">
<meta property="product:price:currency" content="AUD">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<!-- PREVIEW ONLY: Tailwind Play CDN. In Hyvä the classes compile from the theme build. -->
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
{tw}<style>
[x-cloak]{{display:none!important}}
dialog:not([open]){{display:none!important}}
.stock-sheet {{ width: min(94vw, 448px); max-width: none; max-height: 80vh; padding: 0; border: 0; border-radius: 16px; background: #fff; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, .25); margin: auto; }}
.stock-sheet::backdrop {{ background: rgba(11, 20, 32, .55); }}
.stock-inner {{ display: flex; flex-direction: column; max-height: 80vh; padding: 24px; }}
.stock-head {{ flex: 0 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 16px; }}
.stock-head h2, #stockTitle {{ font-family: "Space Grotesk", sans-serif; font-size: 18px; font-weight: 700; color: #000000; margin: 0; }}
.stock-head p, #stockSub {{ margin: 4px 0 0; font-size: 14.5px; font-weight: 600; color: #000000 !important; }}
.stock-close {{ background: none; border: 0; padding: 0; cursor: pointer; color: #9ca3af; transition: color .15s ease; }}
.stock-close:hover, .stock-close:focus-visible {{ color: #4b5563; }}
.stock-scroll {{ flex: 1 1 auto; min-height: 0; overflow-y: auto; overscroll-behavior: contain; margin: 0 -4px; padding: 0 4px calc(2px + env(safe-area-inset-bottom)); }}
.stock-scroll ul {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }}
.store-row {{ display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px; font-size: 14px; cursor: pointer; transition: opacity .15s ease, transform .15s ease; }}
.store-row:hover {{ opacity: 0.88; transform: translateY(-0.5px); }}
.store-row svg {{ flex: 0 0 auto; }}
.store-name {{ font-weight: 600; }}
.store-state {{ margin-left: auto; font-size: 12px; opacity: .8; font-weight: 500; }}
.store-row.is-today {{ background: rgba(34, 197, 94, .08); color: #16a34a; }}
.store-row.is-soon {{ background: rgba(26, 95, 180, .08); color: #1a5fb4; }}
.store-row.is-out {{ background: #fff0f0; color: #dc3545; }}
@media (max-width: 600px) {{
  .stock-sheet {{ width: 100%; max-width: none; margin: auto auto 0; border-radius: 16px 16px 0 0; }}
}}

/* Promotional offer banner: yellow gradient */
.promo-offer-banner {{
  background: linear-gradient(to left, #FFEB3B 0%, rgb(237, 226, 126) 50%, rgba(255, 255, 255, 0.95) 100%) !important;
  border: 1px solid #FFEB3B !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}}
.promo-offer-banner:hover {{
  background: linear-gradient(to left, #fdd835 0%, rgb(232, 218, 105) 50%, #ffffff 100%) !important;
  border-color: #fbc02d !important;
}}
.from-brand-100\/90 {{
  --tw-gradient-from: #FFEB3B var(--tw-gradient-from-position) !important;
  --tw-gradient-to: rgb(217 230 248 / 0) var(--tw-gradient-to-position) !important;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to) !important;
}}
.via-blue-50\/60 {{
  --tw-gradient-to: rgb(239 246 255 / 0) var(--tw-gradient-to-position) !important;
  --tw-gradient-stops: var(--tw-gradient-from), rgb(237 226 126) var(--tw-gradient-via-position), var(--tw-gradient-to) !important;
}}
.border-brand-200\/80 {{
  border-color: #FFEB3B !important;
}}
</style>
{schema}</head>
<body class="bg-white font-sans text-slate-700 antialiased">
"""
    banner = ('<div class="bg-amber-100 px-4 py-2 text-center text-sm text-amber-900">Design preview with <strong>sample product data</strong>. '
              'On the live page the name, price, stock, images, sizes, alternatives and reviews come from Magento.</div>\n')
    footer = r(HOME, 'src/footer.html')
    # The product page has its own sticky Add to cart bar, so drop the footer's "Book a service" bar (one floating action per page)
    footer = re.sub(r'\n  <div class="fixed inset-x-0 bottom-0 z-40.*?</a>\n  </div>\n', '\n', footer, count=1, flags=re.S)
    if pg.get('carousel'):
        marker_details = '  <!-- ========== 2. Product details'
        assert marker_details in content
        content = content.replace(marker_details, r(P, 'src/promo-carousel.html') + marker_details, 1)
        marker_reviews = '  <!-- ========== 3. Customer reviews'
        assert marker_reviews in content
        content = content.replace(marker_reviews, r(P, 'src/why-in-pairs.html') + marker_reviews, 1)
    ticker = r(P, 'src/promo-ticker.html') if pg.get('ticker') else ''
    body = r(HOME, 'src/icons.html') + banner + ticker + r(P, 'src/header.html') + r(HOME, 'src/store-picker.html') + content + footer
    def inline(m):
        f = (P / m.group(1)) if (P / m.group(1)).exists() else (HOME / m.group(1))
        return '"data:image/png;base64,' + base64.b64encode(f.read_bytes()).decode() + '"'
    # Preview is self-contained: every local image becomes a data URI (src/ files keep normal assets/ paths for developers)
    body = re.sub(r'"(assets/[\w./-]+\.png)"', inline, body)
    body = re.sub(r'"(assets/live/[\w.-]+\.webp)"', lambda m: '"data:image/webp;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/live/[\w.-]+\.png)"', lambda m: '"data:image/png;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/offers/[\w.-]+\.webp)"', lambda m: '"data:image/webp;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/education/[\w.-]+\.webp)"', lambda m: '"data:image/webp;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/brands/[\w.-]+\.svg)"', lambda m: '"data:image/svg+xml;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/brands/[\w.-]+\.webp)"', lambda m: '"data:image/webp;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    body = re.sub(r'"(assets/placeholders/[\w.-]+\.svg)"', lambda m: '"data:image/svg+xml;base64,' + base64.b64encode((P / m.group(1)).read_bytes()).decode() + '"', body)
    tail = ('<script>\n' + r(HOME, 'js/oneills-home.js') + '</script>\n<script>\n' + r(P, 'js/oneills-pdp.js') + '</script>\n'
            '<!-- PREVIEW ONLY: Alpine is already loaded by Hyvä. -->\n<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/cdn.min.js"></script>\n</body>\n</html>\n')
    (P / pg['out']).write_text(head + body + tail)
    if pg['out'] == 'wheels.html':
        (P / 'wheel.html').write_text(head + body + tail)
    print('built', pg['out'], (P / pg['out']).stat().st_size, 'bytes;', len(faq), 'FAQs in schema;', pg['schema'])

# Build only the two required product pages: tyres.html and wheel.html
for pg in PAGES:
    build(pg)
