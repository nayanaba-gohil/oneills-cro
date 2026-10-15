"""Generates homepage sections 5 to 9 (stores, reviews, Beresfield TME, brands, about) from one data set.
Usage: python3 tools/lower_sections.py > /tmp/lower.html  (then splice between the section 5 and section 10 markers)
"""
import html

# Store data from the live location pages and Google Business Profiles (9 Oct 2026).
# lat/lng are approximate suburb positions, used only to pick the nearest store. Replace with exact GBP coordinates.
STORES = [
 dict(key="broadmeadow", slug="broadmeadow", name="Broadmeadow", area="Newcastle", street="4 Newton St", suburb="Broadmeadow", pc="2292",
      phone="(02) 4048 0108", tel="0240480108", week="7:30am to 5pm", sat="8am to 12pm", pid="ChIJe1NrzL8Vc2sR_i-Q3Sa9Tv0",
      rating="4.8", count=853, formerly="Formerly Broadmeadow Tyres Newcastle", lat=-32.924, lng=151.735,
      services=["Tyre sales and fitting", "Wheel alignment", "Brake inspection and repair", "Puncture repairs", "Logbook servicing", "Mechanical repairs", "Safety and roadworthy inspections", "Fleet services"]),
 dict(key="beresfield", slug="beresfield", name="Beresfield TME", area="Newcastle", street="2 Babilla Cl", suburb="Beresfield", pc="2322",
      phone="(02) 4966 0444", tel="0249660444", week="7am to 5pm", sat="7:30am to 11:30am", pid="ChIJJ6tn6-VAc2sRX0xVCGpsU4Y",
      rating="4.8", count=131, formerly="Truck, earthmover and industrial tyre centre", lat=-32.800, lng=151.656,
      services=["Tyre sales and fitting", "Wheel alignment", "Wheel balancing", "Wheels", "Truck and bus tyres", "Earthmover and OTR tyres", "Tractor and agricultural tyres", "Forklift and industrial tyres"]),
 dict(key="gateshead", slug="gateshead", name="Gateshead", area="Lake Macquarie", street="1 Navin Cl", suburb="Gateshead", pc="2290",
      phone="(02) 4943 3711", tel="0249433711", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJl87sCXs9c2sRWMRP-lAldcg",
      rating="4.8", count=199, formerly="", lat=-32.983, lng=151.689,
      services=["Tyre sales and fitting", "Wheel alignment", "Tyre balancing and rotation", "Puncture repairs", "Wheels", "Fleet services"]),
 dict(key="warnersBay", slug="warners-bay", name="Warners Bay", area="Lake Macquarie", street="183 Macquarie Rd", suburb="Warners Bay", pc="2282",
      phone="(02) 4956 7577", tel="0249567577", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJAUGelLI9c2sR0d9kZBawfKE",
      rating="4.7", count=122, formerly="", lat=-32.969, lng=151.646,
      services=["Tyre sales and fitting", "Wheel alignment", "Wheel balancing", "Puncture repairs", "Suspension and brake checks", "Mechanical repairs", "Battery replacement", "Vehicle servicing"]),
 dict(key="belmont", slug="belmont", name="Belmont", area="Lake Macquarie", street="3 Herbert St", suburb="Belmont", pc="2280",
      phone="(02) 4945 4945", tel="0249454945", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJUT1R790ic2sRBtAcSOyp2Do",
      rating="4.7", count=214, formerly="", lat=-33.034, lng=151.660,
      services=["Tyre sales and fitting", "Wheel alignment", "Wheel balancing", "Puncture repairs", "Logbook servicing", "Mechanical repairs", "Batteries", "Blue slips"]),
 dict(key="morisset", slug="morisset", name="Morisset", area="Lake Macquarie", street="36 Gateway Blvd", suburb="Morisset", pc="2264",
      phone="(02) 4970 4321", tel="0249704321", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJ56Bc_zMoc2sREeYl_lwClG0",
      rating="4.7", count=136, formerly="Formerly Morisset Batteries", lat=-33.108, lng=151.488,
      services=["Tyre sales and fitting", "Wheel alignment", "Wheel balancing", "Puncture repairs", "Suspension and brake checks", "Mechanical repairs", "Battery replacement", "Vehicle servicing"]),
 dict(key="kurriKurri", slug="kurri-kurri", name="Kurri Kurri", area="Hunter Valley", street="249 Lang St", suburb="Kurri Kurri", pc="2327",
      phone="(02) 4937 5288", tel="0249375288", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJGR8f_cU3c2sRZpaMIv3yCNo",
      rating="4.4", count=112, formerly="", lat=-32.819, lng=151.480,
      services=["Tyres and wheels", "Batteries", "Puncture repairs", "Pink slips", "Blue slips", "Wheel alignment", "Suspension upgrades", "Logbook servicing"]),
 dict(key="cessnock", slug="cessnock", name="Cessnock", area="Hunter Valley", street="256 Maitland Rd", suburb="Cessnock", pc="2325",
      phone="(02) 4990 1455", tel="0249901455", week="7:30am to 5pm", sat="8am to 11:30am", pid="ChIJla38nO40c2sRYiH7itsBNRA",
      rating="4.7", count=388, formerly="", lat=-32.834, lng=151.356,
      services=["Tyre sales and fitting", "Wheel alignment", "Puncture repairs", "Mechanical repairs", "Brake inspections", "Logbook servicing", "Blue slips", "Safety checks"]),
]
AREAS = ["Newcastle", "Lake Macquarie", "Hunter Valley"]
e = lambda s: html.escape(s, quote=True)
def directions(s):
    q = f"O%27Neills%20Tyre%20%26%20Autocare%20{s['suburb'].replace(' ', '%20')}"
    return f"https://www.google.com/maps/dir/?api=1&amp;destination={q}&amp;destination_place_id={s['pid']}"
def icon(name, cls):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"></use></svg>'

out = []
A = out.append

# ---------- 5. Store finder ----------
A('''  <!-- ========== 5. Store finder ========== -->
  <!-- All 8 store panels are in the HTML for search engines; Alpine (ohStores) shows one at a time. -->
  <section id="stores" class="scroll-mt-20 bg-slate-50 py-12 lg:py-20" aria-labelledby="stores-title" x-data="ohStores">
    <div class="mx-auto max-w-7xl px-4 lg:px-6">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="min-w-0 flex-1">
          <h2 id="stores-title" class="font-display text-2xl font-bold tracking-tight text-navy-900 sm:text-3xl">Find your nearest O'Neills store</h2>
          <p class="mt-2 text-slate-600">Eight workshops across Newcastle, Lake Macquarie and the Hunter Valley, open Monday to Saturday. Pick a store to see its hours and services.</p>
        </div>
        <button type="button" @click="locate" class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-navy-900 hover:border-brand-600 hover:text-brand-700">
          ''' + icon("i-pin", "h-5 w-5 text-brand-600") + ''' <span x-text="locateLabel">Find my nearest store</span>
        </button>
      </div>
      <p class="mt-3 text-sm text-slate-600" x-show="hasLocMsg" x-text="locMsg" x-cloak role="status"></p>

      <div class="mt-8 grid gap-6 lg:grid-cols-[300px_minmax(0,1fr)] lg:gap-8">
        <nav aria-label="Choose a store" class="space-y-5">''')
for area in AREAS:
    A(f'''          <div>
            <p class="text-xs font-semibold text-slate-500">{area}</p>
            <ul class="mt-2 flex flex-wrap gap-2 lg:block lg:space-y-2">''')
    for s in [x for x in STORES if x["area"] == area]:
        A(f'''              <li><button type="button" data-store="{s['key']}" @click="select" :class="tabCls.{s['key']}" :aria-current="current.{s['key']}" aria-controls="store-{s['slug']}" class="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-left text-sm font-semibold ring-1 lg:w-full lg:justify-between">
                <span>{e(s['name'])}</span><span class="h-2 w-2 shrink-0 rounded-full" :class="dotCls.{s['key']}" aria-hidden="true"></span>
              </button></li>''')
    A('''            </ul>
          </div>''')
A('''        </nav>

        <div>''')
for i, s in enumerate(STORES):
    services = "".join(f'<li class="flex items-start gap-2">{icon("i-check", "mt-0.5 h-4 w-4 shrink-0 text-brand-600")}<span>{e(x)}</span></li>' for x in s["services"])
    sub = f'<p class="mt-1 text-sm text-slate-300">{e(s["formerly"])}</p>' if s["formerly"] else ""
    A(f'''          <article id="store-{s['slug']}" x-show="show.{s['key']}"{'' if i == 0 else ' x-cloak'} class="overflow-hidden rounded-2xl bg-white ring-1 ring-slate-200" aria-labelledby="store-{s['slug']}-name">
            <div class="relative flex min-h-[12.5rem] flex-col justify-center bg-navy-900 px-5 py-5 text-white min-[360px]:min-h-[10.5rem] sm:min-h-[7.75rem] sm:px-6">
              <svg class="absolute inset-0 h-full w-full opacity-[0.06]" aria-hidden="true"><rect width="100%" height="100%" fill="url(#p-tread)"></rect></svg>
              <div class="relative flex flex-wrap items-start justify-between gap-x-3 gap-y-2">
                <div>
                  <p class="text-xs font-semibold text-brand-200">{s['area']}</p>
                  <h3 id="store-{s['slug']}-name" class="font-display text-2xl font-bold">O'Neills {e(s['name'])}</h3>
                  {sub}
                </div>
                <span class="rounded-full px-3 py-1 text-xs font-semibold" :class="statusCls.{s['key']}" x-text="status.{s['key']}" x-show="ready" x-cloak></span>
              </div>
            </div>
            <div class="grid gap-6 p-5 sm:p-6 md:grid-cols-2">
              <div class="space-y-4 text-sm">
                <p class="flex gap-3">{icon("i-pin", "mt-0.5 h-5 w-5 shrink-0 text-brand-600")}<span>{e(s['street'])}<br>{e(s['suburb'])} NSW {s['pc']}</span></p>
                <p class="flex gap-3">{icon("i-phone", "mt-0.5 h-5 w-5 shrink-0 text-brand-600")}<a href="tel:{s['tel']}" class="inline-block py-0.5 font-semibold text-navy-900 hover:text-brand-700">{s['phone']}</a></p>
                <div class="flex gap-3">{icon("i-clock", "mt-0.5 h-5 w-5 shrink-0 text-brand-600")}
                  <dl class="grid flex-1 grid-cols-[auto_1fr] gap-x-4 gap-y-1">
                    <dt class="text-slate-500">Mon to Fri</dt><dd class="font-medium text-navy-900">{s['week']}</dd>
                    <dt class="text-slate-500">Saturday</dt><dd class="font-medium text-navy-900">{s['sat']}</dd>
                    <dt class="text-slate-500">Sunday</dt><dd class="font-medium text-navy-900">Closed</dd>
                  </dl>
                </div>
              </div>
              <div>
                <p class="text-sm font-semibold text-navy-900">Services at this store</p>
                <ul class="mt-3 grid gap-x-4 gap-y-2 text-sm text-slate-600 sm:grid-cols-2 md:grid-cols-1 xl:grid-cols-2">{services}</ul>
              </div>
            </div>
            <div class="flex flex-wrap items-center gap-3 border-t border-slate-100 px-5 py-4 sm:px-6">
              <a href="tel:{s['tel']}" class="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700">{icon("i-phone", "h-4 w-4")}Call {e(s['name'])}</a>
              <a href="{directions(s)}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-xl border border-slate-300 px-4 py-2.5 text-sm font-semibold text-navy-900 hover:border-brand-600 hover:text-brand-700">{icon("i-pin", "h-4 w-4")}Directions</a>
              <a href="/location-{s['slug']}" class="ml-auto inline-flex items-center rounded-full border border-brand-200 bg-brand-50 px-3.5 py-1.5 text-sm font-semibold text-brand-700 hover:border-brand-400 hover:bg-brand-100">Store details</a>
            </div>
          </article>''')
A('''        </div>
      </div>
    </div>
  </section>
''')

# ---------- 6. Google reviews ----------
# Row 1: heading + overall Google rating. Row 2: one capsule per store (first selected). Row 3: that store's latest
# Google reviews (ohReviews, from the reviews feed; never hard-coded) plus Read reviews and Write a review on Google.
REV = sorted(STORES, key=lambda x: -x["count"])
total = sum(s["count"] for s in STORES)
avg = sum(float(s["rating"]) * s["count"] for s in STORES) / total
first = REV[0]
def stars(size, pct, empty="text-slate-200"):
    row = lambda extra: "".join(icon("i-star", f"{size} shrink-0{extra}") for _ in range(5))
    return (f'<span class="flex {empty}">{row("")}</span>'
            f'<span class="absolute inset-y-0 left-0 flex w-[{pct}%] overflow-hidden text-amber-400">{row("")}</span>')
pills = "\n".join(
    f'''          <button type="button" role="tab" id="rv-tab-{s['slug']}" data-store="{s['key']}" data-name="{e(s['name'])}" data-pid="{s['pid']}" data-count="{s['count']}" aria-controls="rv-panel" :aria-selected="selected.{s['key']}" :tabindex="tabIndex.{s['key']}" :class="pillCls.{s['key']}" @click="pick" class="inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-2 text-sm font-semibold">{e(s['name'])}<span class="inline-flex items-center gap-0.5 text-xs font-medium opacity-80">{icon("i-star", "h-3.5 w-3.5 text-amber-400")}{s['rating']}</span></button>'''
    for s in REV)
reviews_url = lambda pid: f"https://search.google.com/local/reviews?placeid={pid}"
write_url = lambda pid: f"https://search.google.com/local/writereview?placeid={pid}"
A(f'''  <!-- ========== 6. Google reviews ========== -->
  <!-- Ratings and counts are as at October 2026 (update monthly, or render from the Places API). The review cards come from
       data-endpoint (see DEV-NOTES); with no feed connected they stay hidden and only the Google links show. -->
  <section id="reviews" class="scroll-mt-20 py-12 lg:py-20" aria-labelledby="reviews-title" x-data="ohReviews" data-endpoint="">
    <div class="mx-auto max-w-7xl px-4 lg:px-6">
      <!-- Heading and the Google summary box, vertically centred on one line from 1024px -->
      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between lg:gap-12">
        <div class="max-w-2xl">
          <h2 id="reviews-title" class="font-display text-2xl font-bold tracking-tight text-navy-900 sm:text-3xl">Rated {avg:.1f} by Hunter drivers on Google</h2>
          <p class="mt-2 text-slate-600">Every store has its own Google Business Profile. Read what local customers say about the workshop you'll use.</p>
        </div>
        <div class="self-start rounded-2xl bg-slate-50 px-5 py-4 ring-1 ring-slate-200 lg:shrink-0 lg:self-auto">
          <div class="flex items-center gap-4">
            <p class="font-display text-5xl font-bold leading-none text-navy-900">{avg:.1f}</p>
            <div>
              <p class="flex items-center gap-2 text-sm font-semibold text-slate-700">{icon("i-google", "h-5 w-5")} Google reviews</p>
              <div class="relative mt-1.5 inline-flex" role="img" aria-label="{avg:.1f} out of 5 stars">{stars("h-5 w-5", round(avg / 5 * 100))}</div>
              <p class="mt-1 text-sm text-slate-600">{total:,} reviews across 8 stores</p>
            </div>
          </div>
          <p class="mt-3 border-t border-slate-200 pt-2.5 text-xs text-slate-500">From each store's Google Business Profile, October 2026.</p>
        </div>
      </div>

      <!-- One capsule per store, most reviewed first. Scrolls sideways on phones. -->
      <div class="-mx-4 mt-8 overflow-x-auto px-4 [scrollbar-width:none] sm:mx-0 sm:overflow-visible sm:px-0 [&::-webkit-scrollbar]:hidden">
        <div role="tablist" aria-label="Choose a store" class="flex gap-2 sm:flex-wrap" @keydown.arrow-left.prevent="prevKey" @keydown.arrow-right.prevent="nextKey">
{pills}
        </div>
      </div>

      <div id="rv-panel" role="tabpanel" aria-labelledby="rv-tab-{first['slug']}" class="mt-6">
        <ul class="grid gap-5 md:grid-cols-3" x-show="hasCards" x-cloak aria-live="polite">
          <template x-for="r in cards" :key="r.id">
            <li class="relative flex flex-col rounded-2xl bg-white p-6 shadow-[0_10px_30px_-12px_rgba(10,22,40,0.18)] ring-1 ring-slate-200/70 sm:p-7">
              {icon("i-quote", "absolute right-6 top-5 h-10 w-10 text-slate-100")}
              <span class="relative inline-flex self-start" role="img" :aria-label="r.ratingLabel"><span class="flex text-slate-200">{"".join(icon("i-star", "h-5 w-5 shrink-0") for _ in range(5))}</span><span class="absolute inset-y-0 left-0 flex overflow-hidden text-amber-400" :style="r.starStyle">{"".join(icon("i-star", "h-5 w-5 shrink-0") for _ in range(5))}</span></span>
              <p class="mt-4 line-clamp-4 leading-relaxed text-slate-700" x-text="r.text"></p>
              <div class="mt-auto flex items-center gap-3 border-t border-slate-100 pt-5">
                <img x-show="r.hasPhoto" :src="r.photo" alt="" width="44" height="44" loading="lazy" referrerpolicy="no-referrer" class="h-11 w-11 shrink-0 rounded-full object-cover">
                <span x-show="r.noPhoto" class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brand-100 font-semibold text-brand-700" x-text="r.initial" aria-hidden="true"></span>
                <div class="min-w-0">
                  <a :href="r.authorUrl" target="_blank" rel="noopener nofollow" class="block truncate font-semibold text-navy-900 hover:underline" x-text="r.author"></a>
                  <p class="truncate text-sm"><span class="text-brand-700" x-text="r.store"></span> <span class="text-slate-500" x-text="r.when"></span></p>
                </div>
                <span class="ml-auto shrink-0" title="Posted on Google">{icon("i-google", "h-5 w-5")}<span class="sr-only">Posted on Google</span></span>
              </div>
            </li>
          </template>
        </ul>

        <!-- Two buttons, same height and radius. They follow the selected store. -->
        <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
          <a href="{reviews_url(first['pid'])}" :href="readUrl" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-5 py-3 font-semibold text-navy-900 hover:border-brand-600 hover:text-brand-700">{icon("i-google", "h-5 w-5")}<span x-text="readLabel">Read all {first['count']:,} reviews</span><span class="sr-only" x-text="storeSr"> for O'Neills {e(first['name'])} on Google (opens in a new tab)</span></a>
          <a href="{write_url(first['pid'])}" :href="writeUrl" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 rounded-xl border border-brand-200 bg-brand-50 px-5 py-3 font-semibold text-brand-700 hover:border-brand-400 hover:bg-brand-100">{icon("i-star", "h-5 w-5 text-amber-400")}Write a review<span class="sr-only" x-text="storeSr"> for O'Neills {e(first['name'])} on Google (opens in a new tab)</span></a>
        </div>
      </div>
    </div>
  </section>
''')

# ---------- 7. Beresfield TME ----------
TME = [("i-truck", "Truck and bus"), ("i-loader", "Earthmover and OTR"), ("i-loader", "Loader, grader and scraper"), ("i-skidsteer", "Skid steer and Bobcat"),
       ("i-forklift", "Forklift and industrial"), ("i-tractor", "Tractor and agricultural"), ("i-crane", "Crane")]
U = "https://images.unsplash.com/photo-1751054786365-4b02b690d301"
tme_items = "".join(f'<li class="flex items-center gap-3">{icon(i, "h-7 w-7 shrink-0 text-brand-300")}<span class="text-sm">{t}</span></li>' for i, t in TME)

# ---------- 8. Brands ----------
BRANDS = [("michelin", "Michelin"), ("continental", "Continental"), ("bfgoodrich", "BFGoodrich"), ("toyo", "Toyo"), ("yokohama", "Yokohama"),
          ("pirelli", "Pirelli"), ("goodyear", "Goodyear"), ("dunlop", "Dunlop"), ("falken", "Falken"), ("nitto", "Nitto"), ("hankook", "Hankook"),
          ("kumho", "Kumho"), ("maxxis", "Maxxis"), ("general-tire", "General Tire"), ("laufenn", "Laufenn"), ("triangle", "Triangle"), ("fronway", "Fronway")]
BRANDS.sort(key=lambda b: b[1].lower())  # A to Z, so shoppers can scan for their brand
# Logos saved from the live /tyres/brand page into assets/brands (self-hosted, no Cloudflare hot-link issues).
brand_items = "".join(
    f'<li class="border-b border-r border-slate-200"><a href="/tyres/brand/{slug}" class="flex h-20 items-center justify-center p-4 hover:bg-slate-50 sm:h-24">'
    f'<img src="assets/brands/{slug}.png" alt="{n} logo" width="175" height="50" loading="lazy" class="max-h-9 w-auto max-w-[85%] object-contain sm:max-h-10">'
    f'<span class="sr-only">{n} tyres</span></a></li>' for slug, n in BRANDS)
brand_items += ('<li class="border-b border-r border-slate-200"><a href="/tyres/brand" class="flex h-20 flex-col items-center justify-center gap-1 p-4 text-sm font-semibold text-brand-700 hover:bg-slate-50 sm:h-24">'
                + '<svg class="h-5 w-5" aria-hidden="true"><use href="#i-arrow-right"></use></svg>All brands</a></li>')

# ---------- 9. About ----------
CLUBS = [("newcastle-jets.svg", "Newcastle Jets"), ("cardiff-cobras.webp", "Cardiff Cobras"), ("cdcc.webp", "CDCC"),
         ("butcher-boys.webp", "Central Newcastle Butcher Boys"), ("weston-bears.webp", "Weston Bears FC"), ("redhead-tennis.webp", "Redhead Tennis Club")]
club_items = "".join(f'<li><img src="assets/community/{f}" alt="{n} logo" title="{n}" width="56" height="56" loading="lazy" class="h-12 w-auto sm:h-14"></li>' for f, n in CLUBS)
M = "https://oneillstyres.com.au/media/wysiwyg/meetanshi/images/"
# NSW Fair Trading public register entry for licence MVRL61864 (client supplied)
LICENCE_URL = "https://verify.licence.nsw.gov.au/details/Motor%20Vehicle%20Repairers%20Licence/1-44OLQ4G"

A(f'''  <!-- ========== 7. Truck, earthmover and farm ========== -->
  <!-- Photo is a free Unsplash placeholder. Replace with a photo of the Beresfield TME heavy vehicle bay. -->
  <section class="relative overflow-hidden bg-navy-900 text-white" aria-labelledby="tme-title">
    <div class="relative h-56 sm:h-72 lg:absolute lg:inset-y-0 lg:right-0 lg:h-auto lg:w-1/2">
      <img src="{U}?auto=format&amp;fit=crop&amp;w=1200&amp;q=70" srcset="{U}?auto=format&amp;fit=crop&amp;w=640&amp;q=70 640w, {U}?auto=format&amp;fit=crop&amp;w=1200&amp;q=70 1200w" sizes="(min-width: 1024px) 50vw, 100vw" alt="Wheel loader working on a construction site" width="1200" height="800" loading="lazy" class="absolute inset-0 h-full w-full object-cover">
      <div class="absolute inset-0 bg-gradient-to-t from-navy-900 via-navy-900/10 to-transparent lg:bg-gradient-to-r lg:from-navy-900 lg:via-navy-900/20 lg:to-transparent" aria-hidden="true"></div>
    </div>
    <svg class="absolute inset-0 h-full w-full opacity-[0.05] lg:w-1/2" aria-hidden="true"><rect width="100%" height="100%" fill="url(#p-tread)"></rect></svg>
    <div class="relative mx-auto max-w-7xl px-4 pb-12 pt-8 lg:px-6 lg:py-20">
      <div class="lg:w-1/2 lg:pr-12">
        <h2 id="tme-title" class="font-display text-2xl font-bold tracking-tight sm:text-3xl">Truck, earthmover and farm tyres at Beresfield TME</h2>
        <p class="mt-3 leading-relaxed text-slate-300">Our Beresfield TME workshop supplies, fits and repairs <a href="/services/truck-tyres" class="font-semibold text-white underline decoration-brand-300 underline-offset-4 hover:decoration-white">truck tyres</a>, bus tyres and tyres for earthmoving machinery and farm equipment, alongside passenger car servicing. Businesses running utes, vans or trucks can set up <a href="/services/fleet-services" class="font-semibold text-white underline decoration-brand-300 underline-offset-4 hover:decoration-white">fleet services</a> for tyres, alignments and servicing across all 8 stores. Beresfield TME serves Thornton, Raymond Terrace and the Lower Hunter.</p>
        <ul class="mt-6 grid grid-cols-2 gap-x-6 gap-y-4">{tme_items}</ul>
        <a href="tel:0249660444" class="mt-8 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-3 font-semibold text-white hover:bg-brand-500">{icon("i-phone", "h-5 w-5")}Call Beresfield TME (02) 4966 0444</a>
      </div>
    </div>
  </section>

  <!-- ========== 8. Brands ========== -->
  <section class="py-12 lg:py-20" aria-labelledby="brands-title">
    <div class="mx-auto max-w-7xl px-4 lg:px-6">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div class="min-w-0 flex-1">
          <h2 id="brands-title" class="font-display text-2xl font-bold tracking-tight text-navy-900 sm:text-3xl">Tyre brands we fit</h2>
          <p class="mt-2 text-slate-600">Choose a brand to see every tyre we stock from it, fitted and balanced at your nearest store.</p>
        </div>
        
      </div>
      <ul class="mt-8 grid grid-cols-3 border-l border-t border-slate-200 sm:grid-cols-6">{brand_items}</ul>
    </div>
  </section>

  <!-- ========== 9. About and community (E-E-A-T) ========== -->
  <section class="overflow-hidden bg-slate-50 py-12 lg:py-20" aria-labelledby="about-title">
    <div class="mx-auto grid max-w-7xl items-center gap-12 px-4 lg:grid-cols-2 lg:gap-16 lg:px-6">
      <div class="relative pt-4">
        <img src="assets/oneills-store-front.jpg" srcset="assets/oneills-store-front-800.jpg 800w, assets/oneills-store-front.jpg 1600w" sizes="(min-width: 1024px) 600px, 100vw" alt="O'Neills Tyre &amp; Autocare store front with blue O'Neills signage" width="1600" height="1065" loading="lazy" class="aspect-[3/2] w-full rounded-2xl object-cover shadow-xl">
        <!-- "Since 1961" sticker (client artwork). Decorative: the heading and the stats below already say 1961. -->
        <img src="assets/since-1961-badge.png" alt="" width="240" height="240" loading="lazy" class="absolute -left-2 top-0 h-24 w-24 drop-shadow-lg sm:-left-4 sm:h-28 sm:w-28">
      </div>
      <div>
        <h2 id="about-title" class="font-display text-2xl font-bold tracking-tight text-navy-900 sm:text-3xl">Family owned in the Hunter since 1961</h2>
        <p class="mt-4 leading-relaxed text-slate-600">O'Neills Tyre &amp; Autocare started as a small family business in 1961 and has grown to 8 workshops across Newcastle, Lake Macquarie and the Hunter Valley. We are still local and family owned, and all repair work is carried out under our NSW motor vehicle repairer licence.</p>
        <dl class="mt-8 grid grid-cols-3 divide-x divide-slate-200 border-y border-slate-200 py-5 text-center">
          <div class="px-2"><dt class="text-xs text-slate-500 sm:text-sm">Established</dt><dd class="mt-1 font-display text-2xl font-bold text-navy-900 sm:text-3xl">1961</dd></div>
          <div class="px-2"><dt class="text-xs text-slate-500 sm:text-sm">Workshops</dt><dd class="mt-1 font-display text-2xl font-bold text-navy-900 sm:text-3xl">8</dd></div>
          <div class="px-2"><dt class="text-xs text-slate-500 sm:text-sm">Repairer licence</dt><dd class="mt-1 font-display text-base font-bold text-navy-900 sm:text-xl"><a href="{LICENCE_URL}" target="_blank" rel="noopener" class="underline decoration-brand-300 decoration-2 underline-offset-4 hover:text-brand-700 hover:decoration-brand-600">MVRL61864<span class="sr-only"> (check this licence on the NSW Government register, opens in a new tab)</span></a></dd></div>
        </dl>
        <h3 class="mt-8 font-display text-lg font-bold text-navy-900">Backing local sport</h3>
        <p class="mt-1 text-slate-600">Official partner of the Newcastle Jets and sponsor of clubs across the region.</p>
        <ul class="mt-5 flex flex-wrap items-center gap-x-6 gap-y-4">{club_items}</ul>
        <!-- Two buttons, same height and the sitewide button radius (rounded-xl). Stacked full width on phones. -->
        <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
          <a href="/about" class="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-5 py-3 font-semibold text-navy-900 hover:border-brand-600 hover:text-brand-700">Read our story</a>
          <a href="/community" class="inline-flex items-center justify-center rounded-xl border border-brand-200 bg-brand-50 px-5 py-3 font-semibold text-brand-700 hover:border-brand-400 hover:bg-brand-100">Community partners</a>
        </div>
      </div>
    </div>
  </section>
''')
print("\n".join(out))
