# O'Neills product page (tyres): developer handover (Hyvä)

Design for every tyre product page, shown with one sample product: **Yokohama ADVAN Sport V105 245/35ZR19 89W**
(`/yokohama-24535zr19-89w-advan-v105-wrx-subaru-2453519v105sb`). It shares the homepage's header, footer, icon sprite,
brand tokens and component style (`../homepage`), so read `../homepage/DEV-NOTES.md` first.

> **Live site, 23 Oct 2026:** this product page, `/tyres`, `/tyres/sizes`, `/wheels`, `/services`, `/location-belmont` and `/tyres/brand/yokohama` returned **500 "There has been an error processing your request"**. Search then timed out (Cloudflare 524). Only `/` and `/tyres/vehicles/subaru` loaded. Check `var/report/` (record `55fc8461f5d0deb3385a7c781e94021979bfc8c279a3961f9d444e87120e627d`) and the server logs before anything else.

## Files

| File | What it is |
|---|---|
| `src/header.html` | Product page header: copy of `../homepage/src/header.html` with round 3 changes. `tools/build.py` uses this one |
| `src/product-content.html` | Design A body: multi-image product with reviews (between header and footer). Design reference for the Hyvä templates |
| `src/product-content-single.html` | Design B body: single-image product with size options and no reviews yet (sample: Yokohama Geolandar A/T G015) |
| `js/oneills-pdp.js` | Alpine components `ohBuy`, `ohGallery`, `ohReadMore`, `ohTabs`, `ohReview` (CSP-safe, like the homepage). Load after `../homepage/js/oneills-home.js` |
| `schema/product-jsonld.html`, `schema/product-jsonld-single.html` | Product + BreadcrumbList + FAQPage JSON-LD for A and B (generated; FAQ text read from the page). B uses an AggregateOffer and has no aggregateRating |
| `tools/build.py` | Builds `preview.html` (A), `preview-single.html` (B) and both schema files. Run `python3 tools/build.py` from this folder |
| `preview.html` | Single-file preview with a "sample product data" banner. Reference only. Do not deploy |

**Everything product-specific in the preview is sample data:** price ($289), stock, images (Unsplash), other sizes, alternatives and reviews. On the live page these come from Magento (see Data mapping). The tyre facts (245 mm, 35%, 19 inch, load 89 = 580 kg, speed W = 270 km/h, about 654 mm overall) follow from the size itself.

## Page structure (top to bottom)

1. **Breadcrumb:** Home > Tyres > Yokohama tyres > product (unchanged). BreadcrumbList schema matches it.
2. **First screen** (right column, top to bottom, round 11): category eyebrow with car icon ("Car tyres", plain text); H1; rating row (stars, `4.6 · 12 reviews`, links to `#reviews`; only when review count > 0); short description clamped to 2 lines with "Read more" (`ohReadMore`); then the minimal buy section (top divider, no card): price "$289.00 each", "Includes GST and new valves", the store stock line (round 8), quantity stepper (1 to 8, default 1) + one wide "Add tyres to cart" button, "Total $289.00 for 1 tyre · Choose your store and fitting time at checkout." and a plain text BNPL line; under the form one compact trust line (text-sm, slate-600, three small sprite icons): "Free fitting at any O'Neills store", "Wheel balancing included", "Eco tyre disposal included". Stacked on phones, one row (wrapping) from `sm`. 
   - **Gallery:** about 41% of the width on desktop (9fr/13fr grid), pinned while the right column scrolls; thumbnails swap the main image (`ohGallery`). 16:10 on phones.
   - **Mobile sticky bar:** total + "Add to cart", shown only while the main button is off screen (one Add to cart in view at a time). The footer's "Book a service" bar is removed by `tools/build.py`.
   - Checked at 1280 x 800: Add to cart sits inside the first screen.
3. **Product details (one tabbed section, `#details`):** four tabs in a row: About this tyre, Specifications, FAQs, Will it fit? (`ohTabs`). One panel shows at a time; About is the default.
   - **About** (`#about`): description with H3s and internal links, max-w-3xl.
   - **Specifications** (`#specs`): table (about 60%) with a right column (about 40%, thin left divider on desktop) holding two short blocks split by a thin divider, each an H3: "What's included" (check list: fitting at the store you choose, standard wheel balancing, new valves, eco tyre disposal, GST; then "Not included: wheel alignment", link `/wheel-alignment`) and "Fitting and returns" (text, link `/terms`). Stacked under the table below `lg`. The old one-line summary under the table is gone (it said the same thing).
   - **FAQs** (`#faqs`, "Questions about this tyre"): native `<details>`; FAQPage schema is generated from them.
   - **Will it fit?** (`#fit`, "Will it fit my car?"): placard check, how to read the size, "Find tyres for my car", "Ask a store to check". The "Listed for Subaru WRX" mention lives here.
4. **Customer reviews** (`#reviews`, its own section below the tabs): average, breakdown, list, "Write a review" (`ohReview`), empty state in a comment at the end of the source.
4. **Customer reviews** (`#reviews`, its own section below the tabs): see Round 10 (A: sticky summary column beside the list, inline form below; B: empty state with the same inline form).
5. **Related products** (`#related`): H2 "Other tyres in {size}" with a "See all {size} tyres" link (cards are single links to product URLs). The "Other sizes in the range" block was removed in round 9.
No "On this page" pill nav.

## Heading structure

One H1 (product). H2 in order: About the {model}, Specifications, Questions about this tyre, Will it fit my car? (one per tab panel, all in the HTML), then Customer reviews, then one related-products H2 ("Other tyres in 245/35ZR19"). H3 only inside About (sub-topics), Specifications ("What's included", "Fitting and returns"), "How to read your tyre size" (Will it fit?), reviews (review headlines in A; "Write a review" in B) and the related tyre cards (tyre names). No skipped levels, sentence case, no uppercase.

## Head and SEO

- **Title:** `{Brand} {Model} {Size} {LoadSpeed} Tyre | O'Neills`, e.g. `Yokohama ADVAN Sport V105 245/35ZR19 89W Tyre | O'Neills` (56 characters; adds the "Tyre" query term; no em dash).
- **Meta description** (under 160 characters): `{Brand} {Model} {Size} {LoadSpeed}, listed for the {Vehicle}. Price includes fitting, balancing and new tyre valves at 8 O'Neills stores.`
- `og:type` = product, `product:price:amount`, `product:price:currency` = AUD, canonical = the product URL, `lang="en-AU"`.
- **Schema:** Product (`url`, `model`, `brand`, `sku`, `gtin13` and `mpn` only when present, `image` (all gallery images), `category`, `additionalProperty` for size, width, aspect ratio, rim, load index, speed rating, season, pattern; `offers` with AUD price incl. GST, availability, condition, seller, `hasMerchantReturnPolicy` with `applicableCountry` AU and `merchantReturnLink` /terms only; `availableAtOrFrom` is omitted because it expects a Place, not the organization), BreadcrumbList, FAQPage. **`aggregateRating` and `review` only when the product has real, approved product reviews.** Never use the Google store rating in product schema. Remove any duplicate Product microdata the theme outputs.
- Product URLs: keep the existing slugs (or 301 them). Consider a naming convention for product names: `Brand Model Size LoadSpeed` (the live name "Yokohama 245/35ZR19 89W ADVAN V105 WRX Subaru" puts the vehicle in the name; fitment belongs in an attribute).

## Data mapping (Magento)

| On the page | Source |
|---|---|
| Name, SKU, price incl. GST, stock | Product name, SKU, final price (tax display incl. GST), salable status (MSI per store if available) |
| Brand logo and link | Brand attribute with logo (same files as `/tyres/brand`) |
| Size, width, profile, rim, load index, speed rating, season, pattern | Tyre attributes (the size form already has `width`, `profile`, `rim_diameter`). Load in kg and speed in km/h: lookup tables in the template |
| "Listed for" vehicle | Vehicle fitment data (the `/tyres/vehicles` module). Hide the line if there's no fitment |
| Short and long description | `short_description`, `description`. Write benefit-first copy, no fluff, no unverifiable claims |
| Gallery | Product media gallery: tread, sidewall, fitted. Alt text: "{Model} tread pattern", etc. |
| Size options (design B) | Configurable product: one child simple product per size, or a custom option "Size". See Round 9 |
| Other tyres in this size | Products with the same width/profile/rim, other brands, in stock, by popularity or price |
| Reviews, breakdown, form | Magento_Review (enable "Allow guests to write reviews" if wanted). "Verified buyer" and "Fitted at {store}" need a small custom flag from orders (optional) |
| GTIN (`gtin13`) | Magento EAN/barcode attribute. Output only when it holds a valid 13 digit value |
| MPN (`mpn`) | Manufacturer part number attribute. Output only when present |
| Load type, Run-flat | Tyre attributes (XL / standard load, run-flat yes/no). Sample shows Standard load, No |
| Store stock | Per store: MSI source quantity and an "available from" date (see Round 8). Output as `data-stores` JSON on the ohBuy section |
| Quantity default | 1 (client request, round 6; stepper 1 to 8, `data-qty="1"`) |

## Audit: what was applied, changed or not used

| Audit point | Decision |
|---|---|
| Price, CTA, short description above the fold | Applied (checked at 1280 x 800; phones get the sticky bar from the first screen) |
| Specific CTA text | Applied as "Add tyres to cart" + "Choose your store and fitting time at checkout". "Buy & Book Fitting" wasn't used because booking happens at checkout today |
| One sticky action on mobile | Applied; the footer's Book a service bar is off on product pages |
| BNPL under the price | Applied (Afterpay instalments, Zip, humm) |
| Brand and category in separate columns | Applied |
| Fitment reassurance | Applied ("Listed for", placard check, how to read the size, other sizes). A rego lookup needs a data provider; not included |
| Long description, What's included, FAQs, fitting and returns | Applied |
| Reviews: display, breakdown, submit | Applied (Magento reviews) |
| Breadcrumb + BreadcrumbList, Product schema, FAQ schema | Applied (aggregateRating only with real product reviews) |
| Title with em dash ("... V105 [em dash] Subaru WRX") | Changed: no em dashes (copy rule) |
| "Developed at the Nürburgring", "factory fitment for the WRX STi", OE year ranges | **Not used: unverified.** Add only if Yokohama or O'Neills confirms them (EEAT: claims need proof) |
| FAQ "Can I book mobile fitting at home?" | Not used: mobile fitting is unconfirmed (homepage confirmation 3) |
| FAQ "V105 vs V107" | Not used without verified product data |
| "8 Hunter Valley stores" | Corrected to "Newcastle, Lake Macquarie and the Hunter" (Belmont, Gateshead etc. aren't in the Hunter Valley) |
| Eco-disposal in What's included | Used from round 6 (confirmed by client) |
| Hover lift on cards | Not used (CRO rule); border colour change only |

## Client confirmations

1. Price display: price **each** including GST and fitting? (The preview assumes yes, as on the homepage.)
2. Old tyre disposal: **confirmed by client (round 6): included, eco disposal.** Free fitting also confirmed.
3. Changes and returns policy for tyre orders (the page links to `/terms`; a dedicated returns page would be better).
4. Is the V105 in this size OE (factory fitted) on any Subaru model and year? If yes, say so with the model years.
5. Product reviews: moderate in Magento (default) and show "Verified buyer"?
6. Per-store stock: confirm each of the 8 stores is its own MSI source, and where the "available from" date comes from (a per-source restock/transfer date attribute, or an ETA from the stock system). Without a date, the row reads "Ask in store".
7. Manufacturer warranty: link to Yokohama Australia's warranty page once confirmed, then replace "Ask any store for the terms" with the link.
8. Return policy: return window in days and `returnPolicyCategory` for the schema (not output until confirmed).
9. Order-in lead time: "usually ready in 2 to 4 business days" is a placeholder, confirm with suppliers.
10. GTIN availability: does the catalogue hold EAN/barcodes for these tyres? Schema output stays off without them.
11. Free tyre checks: the homepage doesn't state them, so the replace-your-tyres FAQ says "any O'Neills store can check your tyres" without "free". Confirm before adding it.

## Regenerating

Edit `src/product-content.html`, `src/product-content-single.html` or `js/oneills-pdp.js` (or the shared files in `../homepage`), then from this folder:

```bash
python3 tools/build.py
```

## Round 2 changes (26 Oct 2026)

1. **Title tag** `{Brand} {Model} {Size} {LoadSpeed} Tyre | O'Neills`: SEO, adds the "Tyre" term and stays under 60 characters. Meta description is 142 characters.
2. **Product JSON-LD**: `url`, `model`, three images, optional `gtin13`/`mpn`, return policy link, Run-flat and Load type properties. SEO: richer merchant listing data without unconfirmed claims. Output validated as JSON.
3. **Specifications**: Load type, Run-flat and Manufacturer warranty rows. CRO/SEO: answers common fitment questions in the table. Warranty links to nothing until confirmed (client confirmation 7).
4. **FAQs**: ZR vs R, and when to replace tyres (NSW 1.5 mm). SEO: long-tail questions, picked up by FAQPage schema (8 now).
5. **Reviews form (`ohReview`)**: fetch submit with an inline, `aria-live` confirmation and error that keeps the inputs. CRO: no page reload or lost scroll position. Without JS the native form post works. Set the real action to Magento's `review/product/post/id/{id}` and output `form_key` in the template.
6. **Reviews empty state**: a commented, ready-to-use section at the end of `src/product-content.html` (form open by default, text "No reviews for this tyre yet. Bought it from us? Tell other drivers how it performs."). CRO: first reviews are asked for in place. **With no reviews the rating stars and count next to the H1 are not rendered**, and the Product schema has no `aggregateRating`.
7. **Stock states:** replaced by per-store stock in round 8 (the in/low/order pill and `data-stock` attributes are gone).
8. **Breadcrumb on phones**: earlier crumbs `shrink-0`, last crumb `min-w-0 truncate`, list no longer scrolls. CRO: no hidden sideways scroll. Checked at 390 px.
9. **Other tyres in {size}** cards: each card is one link (name, type and price read as its accessible name), logo has width/height, `loading="lazy"` and a fixed 28 px wrapper. CRO/CWV: no layout shift, one tap target.

## Round 3: minimal layout (26 Oct 2026)

1. **Header** (`product-page/src/header.html`, copied from the homepage header): menu now matches the live site: Tyres, Wheels, Servicing & Repairs (dropdowns, contents unchanged), Community (`/community`), Specials, Contact (`/contact`). Stores and About removed from the menu, "Book a service" header button removed. Icons in order: search, favourites, cart, account. Mobile drawer has the same item order; the phone button is unchanged. **Apply the same header to `../homepage/src/header.html` for sitewide consistency** (homepage files were not edited).
2. **Utility bar:** brand blue (`bg-brand-600`, #1A5FB4) with white text (about 6.4:1 contrast). Content unchanged.
3. **First screen:** brand logo moved under the H1 (the bordered Brand/Category box and the word "Brand" are gone); rating and "Car tyres" share one row with a divider; "Listed for Subaru WRX. Check it fits" removed from the first screen (it stays in "Will it fit my car?").
4. **Buy section:** no card or border box. Removed: quantity pill buttons, favourites heart next to the button, BNPL logo row, key spec tiles, trust row (8 stores, since 1961, licence) and the separate total block. Added: stepper and a text-only BNPL line. `ohBuy` now has argument-free `inc()` / `dec()` and getters `decDisabled` / `incDisabled`, `payText` (Afterpay limit logic kept; above the limit it reads "Pay over time with Zip or humm at checkout"). The stock badge is a small pill (`stockCls` getter classes changed: safelist `bg-emerald-50 bg-amber-50 bg-slate-100 text-emerald-700 text-amber-800 text-slate-700 ring-emerald-200 ring-amber-200 ring-slate-200`).
5. **Sections:** only Description, Specifications, FAQs, Will it fit my car? and Customer reviews, each an H2 with `py-12 lg:py-16`, white backgrounds with slate-50 on Specifications and Fitment only, single `max-w-7xl` container, long text at `max-w-3xl`. "What's included" and "Fitting and returns" cards replaced by one line under the specifications table.
6. **Related products removed:** "Other sizes in the range" and "Other tyres in {size}" no longer render, which **loses internal links** to sibling sizes and competing tyres (SEO and cross-sell). The markup is in one HTML comment at the end of `src/product-content.html`; move it back above the FAQs to re-enable.
7. **Build:** `tools/build.py` reads `src/header.html`. Schema is unchanged (Product, BreadcrumbList, FAQPage; 8 FAQs; valid JSON).

## Round 4: tabs (26 Oct 2026)

1. **One tabbed section** replaces the stacked About, Specifications, FAQs and Will it fit my car? sections. CRO: shorter page, the four reference topics are one tap away. Customer reviews stays below as its own section (`#reviews`, so the rating link still works).
2. **`ohTabs`** (`js/oneills-pdp.js`): WAI-ARIA tabs (`role` tablist/tab/tabpanel, `aria-selected`, `aria-controls`, `aria-labelledby`, roving `tabindex`). Click, tap, Enter and Space open a tab; Left/Right arrows move between tabs. Switching is instant (no fetch). Templates only use properties, getters (`on`, `sel`, `idx`, `cls`) and argument-free methods (`pick`, `hover`, `leave`, `prev`, `next`); the tab comes from `data-tab`.
3. **Hover to open is desktop only:** `mouseenter` opens a tab after 120 ms (cancelled on `mouseleave`, so passing over tabs does not flicker) only when `(min-width: 1024px) and (hover: hover) and (pointer: fine)` matches. On touch and small screens tap is the only trigger.
4. **Why all four panels stay in the HTML (SEO):** inactive panels are hidden with `x-show` (display none), never `x-if` or removed. Crawlers and the FAQPage schema extraction (`tools/build.py` reads the `<details>` markup) still see all the content. Without JavaScript every panel is visible and the tab row stays hidden (it only appears once Alpine starts).
5. **Deep links:** `#about`, `#specs`, `#faqs`, `#fit` (the panel ids; the old `#specifications`, `#faq`, `#fitment` map to them) or any element inside a panel open that tab on load and on `hashchange`, then scroll to it. The page had no other links to these sections.
6. **Tab row:** minimal underline bar. Active: 2px `brand-600` bottom border, navy text, semibold. Inactive: slate-600, navy on hover. No pills, no hover lift. At 390 px the row scrolls sideways inside its own container (hidden scrollbar) so nothing is clipped and the page does not overflow.
7. **Headings:** each panel keeps a visible H2 (`text-xl sm:text-2xl`), H3s unchanged. Section backgrounds are white (slate-50 bands removed).
8. **Tailwind safelist:** classes applied only from the `ohTabs` getter: `border-brand-600 text-navy-900 border-transparent text-slate-600 hover:text-navy-900 font-semibold`. Also the arbitrary classes `[scrollbar-width:none] [&::-webkit-scrollbar]:hidden` (in the template, not JS).

- **No layout shift on load:** the tab row renders from the start and the Specifications, FAQs and Will it fit? panels ship with `style="display:none"` (Alpine's `x-show` takes over). They stay in the HTML, so Google still reads them and the FAQ schema still extracts. Trade-off: without JS only About shows, which is fine on Hyvä (Alpine is required sitewide).

## Round 5: restored content (26 Oct 2026)

Three things came back, keeping the minimal look (thin borders, white, no hover lift, sentence case, no em dashes).

1. **What's included and Fitting and returns** now sit inside the Specifications panel, beside the table (60/40 grid from `lg`, stacked below). Original copy, check icons from the sprite, "Not included: wheel alignment" links to `/wheel-alignment`, fitting text links to `/terms`. The one-line summary under the table was removed. SEO/CRO: the answer to "what do I get for the price" is next to the specs, not hidden.
2. **Trust line** under the Add to cart area (see Page structure). Replaces the three-column trust row removed in round 3 with one compact line. Add to cart still ends at about 623 px at 1280 x 800.
3. **Related products** restored below the reviews as one section with two sub-blocks (see Page structure) and the HTML comment block was deleted. Restores internal links to sibling sizes and competing tyres. No horizontal overflow at 390 px (cards are a 2-column grid).

**Tailwind safelist:** unchanged. Everything added is static markup (no new classes come from JS getters), so only the round 2, 3 and 4 safelist entries above apply.

## Round 6 (26 Oct 2026)

1. **Header back to the original:** `src/header.html` is a fresh copy of `../homepage/src/header.html` (menu Tyres, Wheels, Servicing & repairs, Specials, About; icons search, account, favourites, cart; "Book a service" button; original mobile drawer). Only changes: utility bar stays brand blue (`bg-brand-600`, white text) and the original's "Stores" dropdown is removed to match the requested menu (re-add it from the homepage header if wanted). Round 3 header changes (Community, Contact, no Book button) are reverted.
2. **Self-contained preview:** `tools/build.py` inlines every local `assets/*.png` (O'Neills logo, brand logos) as base64 data URIs in `preview.html`. `src/` files keep normal `assets/` paths. Header logo is the original `oneills-logo.png` (400 x 174).
3. **CTA and quantity:** default quantity 1 (`data-qty="1"`), stepper 1 to 8, button always "Add tyres to cart" (sticky bar too); order state stays "Order tyres". Total reads "Total $289.00 for 1 tyre" (singular/plural) and updates live; initial HTML matches qty 1 (no flash). Afterpay logic unchanged. Trade-off: sets of 4 are common, so 4 tyres is now two taps more than before (three taps from 1).
4. **Trust line** under Add to cart: "Free fitting at any O'Neills store", "Wheel balancing included", "Eco tyre disposal included" (sprite icons wrench, balance, check). One row from `sm`, one per line on phones. The 8 stores, family owned and licence points were removed from here.
5. **Less repetition:** line under the price is "Includes GST and new valves". What's included gains "Eco tyre disposal". FAQ "Does the price include fitting?" and "Other tyres in {size}" subtitle mention eco disposal. Meta description now "Free fitting, balancing and eco tyre disposal at 8 O'Neills stores."
6. **Data mapping:** quantity default is 1.

## Round 7: pay later logos (26 Oct 2026)

- The text line "or 4 interest-free payments of $X with Afterpay" is removed (and its `payText` / `showAfterpay` getters and `AFTERPAY_MAX`).
- In its place, under the total line: "Pay your way:" with Afterpay, Zip and humm logos (sprite `#pay-afterpay`, `#pay-zip`, `#pay-humm`) and a "Details" link to `/finance`. Client confirmed these are the only three pay later options. No amounts are shown, so nothing depends on provider limits.
- Arbitrary class `bg-[#b2fce4]` (Afterpay mint) is in the template, so Tailwind picks it up without a safelist.

## Round 8: store stock (26 Oct 2026)

- The "In stock" pill on the price row is removed. Between "Includes GST and new valves" and the quantity row there is a store stock line: rounded thin-border box (emerald tint when the selected store can supply the quantity, slate otherwise), status dot, "In stock at **Belmont** · fit from today", smaller "Other stores from Wed 28 Oct", and a "Check all 8 stores" text button with chevron. At 390 px the button wraps below the text. Initial HTML is pre-rendered for the sample at quantity 1 (no flash before Alpine).
- The button opens a native `<dialog>` (`showModal`: focus trap, Escape, backdrop click, close button with `#i-close`). Centred modal from `sm`, bottom sheet (full width, rounded top) on phones. Title is a `<p id="stores-title">` referenced by `aria-labelledby`, so the page heading outline is unchanged. Rows are plain list items: green dot (or amber) for stock, `#i-clock` for dated rows, navy medium name, status right aligned. Order: in stock, partial stock, then soonest date. Footer note "Pick your store and fitting time at checkout."
- Logic (`ohBuy`, reads `data-stores` JSON: `name`, `qty` number or null, `date` ISO or null; first store = selected store): store with qty >= chosen quantity shows "In stock, {n} tyres" (green); fewer shows "{n} in stock" (amber). Headline = first store that can supply the quantity, else "Available from {earliest date}" with slate styling; "Other stores from {date}" shows only with a stock headline. If no store has any stock the CTA reads "Order {qty} tyres" (sticky bar "Order tyres"). Dates format as "Wed 28 Oct".
- **Data mapping:** one Magento MSI source per store. `qty` = source quantity (salable, minus reservations). `date` = "available from" per source: needs a per-source restock/transfer date attribute or an ETA from the stock system (client to confirm, see Client confirmations 6). Selected store = the customer's saved or nearest store, else Belmont.
- **Schema:** Offer availability is InStock if any store has stock, else BackOrder (`tools/build.py` derives it from `data-stores`; the sample stays InStock).
- **Tailwind safelist** (classes applied only from JS getters): `border-emerald-200 bg-emerald-50/60 border-slate-200 bg-slate-50 bg-emerald-500 bg-slate-400 bg-amber-500 font-medium text-emerald-700 text-amber-800 text-slate-600`. Also add `overflow-hidden` (toggled on `body` while the dialog is open). Arbitrary `basis-56`, `backdrop:bg-navy-900/50` and `-rotate-90` are in the template. Replaces the round 4 stock pill safelist entries.
- OE badge and wheel alignment add-on: not used (client decision).

## Round 9 (26 Oct 2026)

Two designs, both built by `tools/build.py` (shared header, footer, icons, image inlining):

| | A: `preview.html` | B: `preview-single.html` |
|---|---|---|
| Magento product type | Simple product with a media gallery (3 images) | Configurable product (one child simple product per size) or a simple product with a custom option "Size"; one image |
| Sample | Yokohama ADVAN Sport V105 245/35ZR19 89W | Yokohama Geolandar A/T G015, default 225/60R17 99H, $259.00 |
| Reviews | 12 sample reviews, average 4.6 | None yet: empty state with the inline form |
| Source | `src/product-content.html` | `src/product-content-single.html` |
| Schema | Offer + aggregateRating | AggregateOffer (`lowPrice`, `highPrice`, `offerCount` from the sizes), no aggregateRating |

**Changes in both**

1. Brand logo moved from under the title to directly below the gallery (below the thumbnails in A, below the single image in B). Left aligned, `h-7`, links to `/tyres/brand/yokohama`, alt "Yokohama" plus sr-only " tyres". The title is followed straight by the rating and category row.
2. Category next to the rating is plain text (no link), car icon kept. B reads "SUV and 4WD tyres".
3. Stock line shows only "In stock at {store}" and a "Check all stores" button. "fit from today", "Other stores from ..." and the getters `storeTail`, `storeSub`, `storeCountLabel` are removed. Fallback "Available from {date}" stays. The stock dialog is unchanged.
4. FAQ line "Can't see your question? ..." removed.
5. Will it fit?: H3 "How to read your tyre size" (`text-lg sm:text-xl`) in a bordered panel. Desktop: large size capsule (`text-4xl`, key parts navy) on the left, six item legend (3 x 2) on the right; phones stack (capsule `text-3xl`, legend 2 x 3). Buttons: "Find tyres for my car" (`https://oneillstyres.com.au/tyres/vehicles`) and "Ask a store to check" (`/contact`). Legend values follow the size (B: 225 width, 60 profile, R radial, 17 rim, 99 = 775 kg, H = 210 km/h). On the live site the template derives them from the product size attributes (for a configurable product, the default child). The legend does not change when another size is picked in the select.
6. "Other sizes in the ADVAN Sport V105 range" removed.
7. "Other tyres in {size}": each card is one link (no nested links) to a product URL. Sample slugs follow the live pattern `/{brand}-{size}-{loadspeed}-{model}-{sku}`, e.g. `/michelin-24535zr19-93y-pilot-sport-4s-2453519ps4s` (marked as sample in a comment; live: product URL key). Beside the H2 a text link "See all {size} tyres" goes to `/catalogsearch/result/?q=245%2F35R19` (the live tyre size search pattern from `../homepage/DEV-NOTES.md`; add the width/profile/rim params if the search module needs them). B: "Other tyres in 225/60R17", BFGoodrich, Toyo, Falken, Maxxis, link `q=225%2F60R17`.
8. "Most customers buy 4" (small slate text) under the quantity stepper.

**Reviews, design A (has reviews)**

- Header row: H2 "Customer reviews", average, stars, "Based on 12 reviews", compact breakdown bars and one outline button "Write a review" that opens a native `<dialog>` (centred modal from `sm`, bottom sheet on phones; Escape, backdrop and X close). The dialog holds the form: "You're reviewing {product name}", Your rating (one overall 5 star radio group, required), Nickname (placeholder "Your name"), Summary ("Sum it up in a line"), Review ("How do they grip, wear and ride? Would you buy them again?"), Submit review (brand blue). The `ohReview` fetch submit is unchanged; success replaces the form in the dialog with the thanks message and a Close button.
- List: each review has stars, bold headline, name, date ("18 Sep 2026"), "Verified purchase" pill and text. The first 3 show, then "Show more reviews" reveals 5 per click (3, 8, 12) with a counter "Showing 3 of 12"; the button hides at the end. All reviews stay in the HTML (SEO); hidden ones are `x-show` with an initial `style="display:none"`. The sort select (Most recent, Highest rated, Lowest rated) is handled by `ohReviews`: it ranks the reviews and applies the rank as CSS `order` plus visibility, so the HTML order never changes. Sample reviews are labelled as samples in a comment.
- Live data: reviews come from Magento_Review. For products with 50 or more reviews, paginate server-side (load the next page by fetch and keep the first page in the HTML) instead of rendering them all.

**Reviews, design B (no reviews yet)**

- H2 "Customer reviews", the line "No reviews yet. Bought these tyres from us? Tell other drivers how they perform." and the form inline in a light bordered panel: two columns from `lg` (left: rating, nickname, summary; right: review and submit), stacked on phones. No stars near the H1; a text link "No reviews yet" goes to `#reviews`. No aggregateRating in the schema. When the first review is approved the page switches to design A's reviews block.

**Size options (design B)**

- Native `<select>` in the buy box, between the price block and the stock line, labelled "Size" with a pill showing the selected size. Each option shows the full price ("225/60R17 99H · $259.00"), not "+$" deltas. Helper: "Not sure? Check the size on your tyre sidewall or door placard." with a link "How to read your tyre size" to `#fit` (opens the Will it fit tab).
- Data mapping: configurable product, one option per child simple product (label = size + load and speed rating, price = the child's final price incl. GST, id = the child's option id). With a custom option, use the option values (price type fixed; show the resulting full price, not the delta). Output as `data-sizes` JSON on the `ohBuy` section: `[{ "id": 101, "label": "225/60R17 99H", "price": 259, "default": true }]`. The hidden field `super_attribute[size]` carries the id (use the real attribute id on Hyvä). The H1 stays the product name without the size.
- `ohBuy` gains `pickSize` (`@change="pickSize"`; the event arrives as the first argument, same pattern as `ohGallery.pick`), and getters `sizeLabel`, `sizeValue`, `priceLabel`. The price, total and sticky bar follow the selected size. Stock per size comes from each child's MSI data: reload `data-stores` when the size changes (the sample uses one store list for all sizes).

**Review rating fields.** The live form uses three ratings (Value, Quality, Price). Recommendation: one overall rating, to reduce drop-offs. Ratings are configured in Stores > Rating (disable Value, Quality and Price, add "Overall" or keep a single rating active for the store view). The average and breakdown then come from that one rating.

**Internal link patterns used:** brand `/tyres/brand/yokohama`, vehicle `/tyres/vehicles` and `/tyres/vehicles/subaru`, size search `/catalogsearch/result/?q=245%2F35R19`, product `/{brand}-{size}-{loadspeed}-{model}-{sku}`, `/contact`, `/finance`, `/terms`.

**Tailwind safelist:** no new classes come from JS (the review ranks use inline `order` styles). Existing round 2 to 8 entries stand.

**Page and heading structure:** unchanged order (breadcrumb, first screen, tabs, reviews, other tyres). One H1. H2s: About, Specifications, Questions about this tyre, Will it fit my car?, Customer reviews, Other tyres in {size}. H3s: About sub-topics, What's included, Fitting and returns, How to read your tyre size, review headlines (A) or "Write a review" (B), and tyre card names.

## Round 10 (26 Oct 2026)

**Page structure now:** breadcrumb, first screen (gallery column | buy box column), tabs (About, Specifications, FAQs, Will it fit?), customer reviews (A: two columns, then the inline form; B: empty state with the form), related tyres.

1. **Gallery** (both): main image in a white box with a thin slate border and rounded corners, `object-contain` with padding (tyre shots on white). A: thumbnails in a 4 column grid of equal square bordered boxes (all breakpoints); the active one has a 2px `brand-600` border, others slate (`thumbCls` in `ohGallery` now returns border classes, not rings). Under the image (and thumbnails) a thin divider, then the brand logo at the full width of the column (`w-full h-auto`), still a link to `/tyres/brand/yokohama` with alt "Yokohama" and sr-only " tyres". **Brand logo files should be wide, transparent PNG or SVG (ideally 600px wide or more, or SVG)** so they fill the column cleanly; the current 175 px PNGs are upscaled and look soft.
2. **Buy box** (both): the divider between "Read more" and the price is gone. The right column is `flex flex-col gap-6 lg:justify-between`: group 1 (title to total line), thin divider, "Pay your way" row (moved out of the form, no inputs in it), thin divider, trust points. From `lg` the free height is split evenly between those groups so the column ends level with the gallery column. Trust points are three equal columns from `sm` (icon above text), a single column with inline icons on phones. B: the gallery column also stretches (image box grows, logo stays at the bottom), so both columns end together; the sticky gallery is not used there. Measured at 1280 x 800 and 1440 x 900: A left and right bottoms both at 962 px (difference 0), B both at 1006 px. Add to cart bottom: A 622 px, B 734 px (inside the 800 px first screen). At 1024 px A's right column is taller than the left (about 135 px); acceptable, nothing stretches.
3. **Will it fit?** "How to read your tyre size": heading `font-display text-xl sm:text-2xl` bold with the size capsule on the same row to the right (`flex flex-wrap justify-between`; on phones the capsule wraps under the heading). Legend (3 x 2, 2 x 3 on phones) below, full width. B keeps the 225/60R17 99H values.
4. **CTAs:** "Ask a store to check" goes to `https://oneillstyres.com.au/contact`; "Find tyres for my car" stays `https://oneillstyres.com.au/tyres/vehicles`. No other links changed.
5. **Reviews, design A:** from `lg` two columns. Left (`lg:w-1/3`, `lg:sticky lg:top-28`): H2, large 4.6, stars, "Based on 12 reviews", five breakdown bars, Google stores line. Right: toolbar (count and sort), list (3 shown, then 5 more per click), "Showing n of 12" and "Show more reviews". The "Write a review" button and the dialog are removed. Below both columns is the inline "Write a review" panel, the same markup as B (rating, nickname, summary on the left; review, submit and "Reviews are checked before they appear." on the right), wired to `ohReview` with inline success and error. Phones: summary, list, form, stacked. `openForm`, `closeForm` and `onFormClose` were removed from `ohReview` (no dialog remains in either design); `ohReviews` is unchanged.
6. **Reviews, design B:** unchanged; its form markup is the shared pattern (A reuses it with the product name changed).

## Round 11 (26 Oct 2026)

**Page structure now (first screen):** left gallery column (about 38%: `lg:grid-cols-[minmax(0,5fr)_minmax(0,8fr)]`, `lg:gap-16`), right column in natural top-aligned flow: category eyebrow (small car icon, text-sm semibold slate-600, plain text: "Car tyres" in A, "SUV and 4WD tyres" in B), H1, rating row (A only), short description with Read more, price block, (B: size select), stock line, quantity + Add to cart, "Most customers buy 4", total line, "Pay your way", three trust points. Then tabs, reviews, related tyres as before.

1. **Rating row rule:** show the rating row near the title only when the review count is above 0 (A: stars, 4.6, 12 reviews). With no reviews, render nothing there (B: the "No reviews yet" link is removed). The reviews section at the bottom keeps its empty state and inline form. Product schema keeps `aggregateRating` only with real reviews.
2. **Category eyebrow** above the H1 with the small car icon; removed from the rating row.
3. **Dividers removed** between the total line, "Pay your way" and the trust points; spacing is `mt-4` (total), `mt-5` (pay row, trust points).
4. **Hero like JBI:** gallery column narrower with a wider gap; main image box landscape (`aspect-[4/3]`, white, thin border, rounded, `object-contain`, padding `p-4 sm:p-6`); A: 4 column square thumbnails, thin divider, full-width brand logo (kept); B: image, divider, logo. The Round 10 `lg:justify-between` and equal-height stretching are gone (both columns); the left column may end shorter or longer than the right. A's gallery is still sticky from `lg`. H1 size unchanged.
5. **Will it fit?** two columns from `lg` (`lg:grid-cols-2 gap-10 items-start`): left the "How to read your tyre size" box (`lg:order-first`; H3 and capsule share a row if they fit, otherwise the capsule wraps under the heading, which it does at this column width; legend 3 x 2), right the H2 "Will it fit my car?", paragraph and the two buttons. DOM order keeps the H2 first, so on phones it reads: text and buttons, then the how-to-read box, and the outline stays H2 then H3.
6. Measured at 1280 x 800: Add to cart bottom A 650 px, B 726 px (both inside the first screen). Tailwind safelist unchanged (all new classes are static).

## Round 12 (26 Oct 2026)

1. **Will it fit?** (both designs): columns swapped. Left: H2 "Will it fit my car?", paragraph and the two buttons. Right: the "How to read your tyre size" box. DOM order now matches the visual order (the `lg:order-first` hack is gone), so on phones it reads text, then the box. Inside the box the heading (`text-xl`) and the size capsule (`text-xl sm:text-2xl`, `px-5 py-2`, nowrap) share one row (`flex items-center justify-between gap-4`, no wrap from `sm`); on narrow phones the capsule wraps under the heading. Legend unchanged. Measured at 1280: heading and capsule centres 0 px apart.
2. **Trust points** (both): back to one inline row, icon (`h-5 w-5 text-brand-600`) left of the text, `gap-2`, `gap-x-6 gap-y-2`, `flex-wrap` from `sm`; one per line on phones.
3. **Short description:** "Read more" now sits at the end of line 2. Wrapper is `relative`, the text is `line-clamp-2`, and while collapsed the button is absolutely positioned at the bottom right of the text with a white background and a left fade (`bg-gradient-to-r from-transparent via-white via-30% to-white pl-8`). Expanded, "Show less" is static, after the text. `ohReadMore` gains the getter `toggleCls`. Collapsed block is exactly 2 lines (52 px) at 1280 and 390.
4. **Promotion strip** above the utility bar (in `src/header.html`, so both designs): `bg-navy-900`, 36 px high, centred, one promo at a time (fade), rotates every 5 s, pauses on hover and focus, stays on the first promo with `prefers-reduced-motion`, prev and next chevron buttons with aria-labels, each promo links to `https://oneillstyres.com.au/specials` with the suffix " · See specials". One line with truncate on phones. `aria-live` is `off` while auto-rotating and `polite` after a manual change. New CSP-safe component `ohPromo` in `js/oneills-pdp.js` (getters `cls`, `hid`, `tab`, `live`; methods `next`, `prev`, `pause`, `resume`). The three promos are samples from the live homepage. Add to cart bottom at 1280 x 800: A 662 px, B 738 px (inside the first screen; no spacing changes needed).
5. **Live links** (absolute): "See all 245/35R19 tyres" (A) and "See all 225/60R17 tyres" (B) go to `/catalogsearch/result/?q=...`; every Yokohama link (breadcrumb, brand logo, About text, specs) goes to `https://oneillstyres.com.au/tyres/brand/yokohama`; Subaru links to `/tyres/vehicles/subaru`; every "wheel alignment" link (About tab and What's included) goes to `https://oneillstyres.com.au/contact`. The header servicing menus keep `/services/wheel-alignment` so navigation matches the homepage.
6. **Tailwind safelist additions** (classes applied only from JS getters): `absolute bottom-0 right-0 bg-gradient-to-r from-transparent via-white via-30% to-white pl-8 mt-1 text-base leading-relaxed opacity-100 opacity-0 pointer-events-none`.

**Font.** The client says the official font may be "Fontana". It is not on Google Fonts, so we need the licensed web font files (woff2) and the exact family name and weights. Once supplied, swap `font-display` (and `font-sans` if they want it for body text) in the Tailwind config and add the `@font-face` rules. Everything uses these tokens, so it is a one place change.

**Promotions (not used; the strip was removed in Round 13).** Promo copy, dates and terms come from the client through a CMS block (a Magento CMS block or a Hyvä widget) that renders the `data-promo` links. Keep to 3 or 4 promos at most, and each needs a real terms page to link to (today all link to `/specials`).
- **Brand logo on phones:** full gallery width only from `lg`. Below that it is 160px wide (`w-40`), so the product name stays near the top of the first screen on phones.

## Round 13 (26 Oct 2026)

1. **Special offer price (design B only).** Price block order: "Limited trade offer" (`text-sm font-semibold text-red-600`, no border or badge), then the regular price (`text-lg text-slate-500 line-through`) with "12% off" beside it (`rounded bg-red-50 px-2 py-0.5 text-sm font-semibold text-red-700`, no border), then the offer price (`font-display text-4xl font-bold text-navy-900`) with "each", then "Includes GST and new valves". No tag on the image, no border boxes. Design A has no offer and is unchanged.
   - Sample data: every size in `data-sizes` has `price` (regular) and `offer` (`round(price * 0.88, 2)`), except the last size (245/50R20), which has `"offer": null` to show the no-offer state. The select option text shows the price charged (offer, or regular when there is no offer).
   - `ohBuy` gains `regular`, `apply` (sets regular and charged price) and the getters `hasOffer`, `originalLabel`, `discountLabel` (percentage is computed: `round((1 - offer / regular) * 100)`). Total, sticky bar and the cart price use the charged price. With no offer the two offer lines are hidden (`x-show="hasOffer"`).
   - Magento: the offer is `special_price` (with `special_from_date` / `special_to_date`) or a catalog price rule. Show the offer lines only while it is active (offer lower than regular). The label "Limited trade offer" is static copy; the percentage is always computed, never typed.
   - Schema: `AggregateOffer` `lowPrice` / `highPrice` use the charged prices. Each size is an `Offer` in `offers`; those with a special price carry `priceSpecification` with a `UnitPriceSpecification` of `priceType` `https://schema.org/StrikethroughPrice` (the regular price), which Google merchant listings use for sale prices. Add `priceValidUntil` from `special_to_date` when it is set. `product:price:amount` is the default size offer price.
2. **Promotion strip removed** (both designs) at client request: the navy strip is gone from `src/header.html`, the `ohPromo` component is gone from `js/oneills-pdp.js`, and the Round 12 safelist classes `opacity-100`, `opacity-0` and `pointer-events-none` are no longer needed for it (`opacity-0`/`pointer-events-none` were used only by the strip). The Promotions note above is kept for reference but is not used.
3. **Reviews footer (design A)**: "Showing 3 of 12" and "Show more reviews" are replaced by a footer row under the list: the count on the left ("12 reviews", slate text) and "Show" with a native select (5, 10, 20, 50; default 5) on the right. The sort select stays at the top. All reviews stay in the HTML (hidden ones are `display:none`); `ohReviews` now has `setShown` and `countLabel`, and `canMore`, `more` and the 3/5 step logic are removed. For more than 50 reviews add server-side pages (keep the first page in the HTML).

## Round 14: promo variants (26 Oct 2026)

Two optional previews, built by `tools/build.py` from partials. `preview.html` and `preview-single.html` keep the same markup (only the inlined `js/oneills-pdp.js` grew by the harmless `ohCarousel` component). Schema files are unchanged.

1. **`preview-promo-ticker.html`** = design A plus `src/promo-ticker.html`, injected before the header (above the blue utility bar). Thin navy-900 ribbon (`h-10`, `text-sm`, white), items scrolling right to left in an endless loop (40 s per loop, no JS). The track holds the list twice and animates `translateX(0)` to `-50%`; the second copy is `aria-hidden="true"` and its links have `tabindex="-1"`. Items: Buy 3 tyres get the 4th free (`/specials`), Free fitting and balancing, Afterpay, Zip and humm available (`/finance`), Rated 4.7 on Google (`/#reviews`), Eco tyre disposal included. The store count is not repeated (it is in the blue bar).
   - Hyvä: render as a CMS static block in the `header.panel` area (or the top of the header container) so it sits above the utility bar. The `<style>` in the partial (keyframes plus `.oh-ticker-*` helpers) belongs in the theme CSS.
2. **`preview-promo-carousel.html`** = design B plus `src/promo-carousel.html`, injected after the hero (buy box) section and before the tabs, so Add to cart stays in the first screen. H2 "Current offers", prev and next round buttons at the right of the heading, five cards (rounded-2xl, `bg-brand-50`, thin border, no shadow or hover lift). Cards per view: 3 desktop, 2 tablet, 1.15 phone (`w-[87%]`, peek of the next). Swipe is native CSS scroll-snap. `ohCarousel` (in `js/oneills-pdp.js`, CSP-safe) provides `prev`, `next` (one card, wraps at the ends), `pause`, `resume`; 5 s auto-advance that loops to the start.
   - Hyvä: a product page CMS widget or static block placed after the product info main block (before the tabs).
3. **Content source.** Both use sample copy mirroring the live homepage promos. In production it comes from one CMS block per component; the client confirms copy, dates and terms, and every card needs a real terms page. Not used because not confirmed: "Free wheel alignment" and "$100 cash back on Pirelli". The 4.7 Google rating must match the live reviews figure.
4. **Accessibility.** Ticker: wrapped in `<section aria-label="Current offers">`; hover and keyboard focus pause it; with `prefers-reduced-motion` it does not animate, shows each item once and scrolls sideways. Carousel: auto-advance pauses on hover, focus and touch and while the tab is hidden, and never starts with `prefers-reduced-motion` (buttons then jump without smooth scrolling); buttons have `aria-label`s ("Previous offer", "Next offer"); each "See offer" link carries the card title as `sr-only` text. Cards are `relative` so the `sr-only` text does not widen the page.
5. **Recommendation.** Use one promo pattern sitewide, not both on the same page: the ticker if offers should be seen on every page, the carousel if they belong on product pages only.

## Round 15 (27 Oct 2026)

1. **About this tyre: "At a glance" column (A and B).** The About panel is now `grid gap-10 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)] lg:gap-16` (the `max-w-3xl` wrapper is gone): existing text on the left, `<aside aria-label="At a glance">` on the right. The aside has three rounded `bg-slate-50` cards (icon tile, bold value, small label), a subtext ("For {size}.") and a "Built for" 2 column grid of thin-border chips with sprite icons.
   - **B:** load index and speed rating follow the selected size. The tabs sit outside the buy box section, so a small `ohGlance` component (in `js/oneills-pdp.js`) reads the default size from `data-sizes` and listens for the `oh-size` window event that `ohBuy.pickSize` dispatches. Getters: `loadIndex`, `loadKg`, `speed`, `speedKmh`, `loadLabel`, `speedLabel`, `glanceNote`, `hasLoad`, `hasSpeed`. Each `data-sizes` entry gains `li`, `kg`, `sp`, `kmh` (standard load index and speed rating tables). Default values are pre-rendered in the HTML. Terrain card: "All-terrain", "Sealed roads, gravel and light off-road".
   - **A:** static values ("89 · 580 kg", "W · 270 km/h", "Summer performance", "Sealed roads, dry and wet").
   - **Data source:** cards come from tyre attributes (load index, speed rating, tyre type or season) and an "applications" multiselect attribute for "Built for". Hide a card when its attribute is empty (B already does for load and speed via `hasLoad` and `hasSpeed`), and hide "Built for" when there are no applications. kg and km/h are looked up from the load index and speed rating, not typed.
2. **Category eyebrow icon:** the car icon is replaced by `#i-tyre` (A, "Car tyres") and `#i-4wd` (B, "SUV and 4WD tyres"), `h-5 w-5 text-brand-600`.
3. **Product image:** main image box has no border or padding; the image is `aspect-square h-full w-full rounded-2xl object-contain` on `bg-white`. A thumbnails: inactive have `border-transparent bg-slate-50`, active keep `border-brand-600`. Divider and brand logo unchanged.
4. **Pay later label:** "Pay your way:" is now a small lock icon (`h-4 w-4 text-slate-500`, `aria-hidden`) plus "Secure checkout. Pay later with:". Logos and "Details" unchanged.
5. **"new tyre valves":** the price note, What's included, the FAQ answer (page and schema) and the meta description template now say "new tyre valves" (the word is correct; "tyre valves" makes it clear).

## Round 16: final previews (27 Oct 2026)

Deliverables, built by `python3 tools/build.py`: **`final-multi.html`** (design A, Yokohama ADVAN Sport V105, plus the carousel) and **`final-single.html`** (design B, Geolandar A/T G015, plus the carousel). `preview.html` and `preview-single.html` (same pages without the carousel) still build. The two Round 14 promo previews are no longer built and their files are removed.

1. **Promotions.** Both designs show the "Current offers" card carousel (`src/promo-carousel.html`) after the hero and before the tabs. There is no ticker bar on any page. `src/promo-ticker.html` stays in the repo, unused (`build.py` still supports `pg['ticker']`, no page sets it).
2. **Category eyebrow icon (A and B):** solid car silhouette SVG (`viewBox="2 4 60 28"`, `h-4 w-8 shrink-0 text-brand-600`, `aria-hidden`) replaces the `#i-tyre` / `#i-4wd` sprite icons. Text unchanged ("Car tyres", "SUV and 4WD tyres"). Not used in the mobile menu.
3. **About this tyre panel (A and B).** Top row `grid items-start gap-10 lg:grid-cols-2 lg:gap-16`: left H2 and intro, right `<aside aria-labelledby="rated-title">` with H3 "Rated for your drive", the size as subtext and three cards (`grid grid-cols-3 gap-3`, each: icon in a white rounded square, bold value, small label, centred, `bg-slate-50 rounded-2xl`). Below a `border-t` divider: left "Is it the right tyre for you?" list, right "Get the most from new tyres". "Built for" and "At a glance" are removed. Mobile: stacked, cards stay in one row with `text-base` values and `text-xs` labels (no overflow at 390px).
   - **A (static):** "580 kg" / "Per tyre, load index 89"; "270 km/h" / "Top speed, rating W"; "Summer performance" / "Sealed roads, dry and wet"; subtext "245/35ZR19 89W".
   - **B (bound to the selected size):** `ohGlance` getters are now `loadLabel` ("{kg} kg"), `loadNote` ("Per tyre, load index {li}"), `speedLabel` ("{kmh} km/h"), `speedNote` ("Top speed, rating {sp}") and `glanceNote` (the size label). Third card is static "All-terrain" / "Road, gravel and tracks". Same `oh-size` event and `data-sizes` fields (`li`, `kg`, `sp`, `kmh`); default 225/60R17 99H values are pre-rendered. Cards still hide via `hasLoad` / `hasSpeed` when the attribute is empty.
4. **Reviews (A).** Three sample reviews (5, 5, 4 stars): average 4.7 (rounded from 4.67, star fill 93%), "Based on 3 reviews", breakdown 5 stars 2, 4 stars 1, others 0. Rating row near the H1 reads 4.7 and "3 reviews". `aggregateRating` in the schema is 4.7 / 3 (`build.py`). The footer row (count and "Show" select 5, 10, 20, 50) is only rendered when the product has **more than 5 reviews**; its markup is kept in an HTML comment in `src/product-content.html`. The sort select stays; the inline write-a-review form is unchanged. Design B is unchanged (no reviews: empty state and inline form, no rating row).
5. **Prices.** A: regular price only. B: limited trade offer as in Round 13. No change.
6. **Images: PLACEHOLDERS, replace with product photos.** The finals no longer use `images.unsplash.com` (blocked on the host). Three simple SVG illustrations in `assets/placeholders/`: `tyre-side.svg` (side view, tread blocks, 5-spoke alloy), `tyre-tread.svg` (tread close-up), `tyre-angle.svg` (simplified three-quarter view). A uses all three (main image and thumbnails: side view, tread close-up, three-quarter view); B uses `tyre-angle.svg`. `build.py` inlines them as data URIs (like the PNG logos). The schema `image` array and `og:image` point at `https://oneillstyres.com.au/assets/placeholders/*.svg`, which is a placeholder path only: on the live page they come from the Magento gallery (use JPG or WebP, at least 1200 px, for Google). "Other tyres in {size}" cards use brand logos only, no photos.
7. **Unchanged:** header, blue bar, buy box, stock, Will it fit, FAQs, specs, related tyres, footer and the sample-data banner.

## Round 17: live product images (27 Oct 2026)

- Placeholder tyre drawings replaced with the live product photos from oneillstyres.com.au, copied into `assets/live/` and inlined by `tools/build.py` for the self-contained previews:
  - A: `yokohama-advan-v105.webp` (live main image). The live product has one image, so the two extra thumbnails are crops of it (`-tread`, `-sidewall`). On the live page the gallery shows whatever images the product has in Magento.
  - B: `yokohama-geolandar-g015.webp` (from the live G015 products).
- Schema `image` now points at the live image URLs.
- The live wide Yokohama logo (`/media/meetanshi/brand/yokohama-symbol-450x60-cropped.webp`) has light text for dark backgrounds, so it isn't used on the white gallery column. The brand logo below the gallery still needs a high-resolution dark version.

## Round 18 (27 Oct 2026)

- Multi-image page: main image back in a bordered 4:3 box with padding, so the gallery column (image, thumbnails, logo) ends level with the buy box at 1280px.
- About this tyre (both): one text column on the left with no divider lines between paragraphs; on the right "Rated for your drive" with only the size code under it and the 3 cards stacked (icon left, value, label). "Built for" removed.
- "Rated for your drive" cards in About this tyre show on desktop only (`hidden lg:block`). On phones the same load and speed values are in the Specifications tab, so nothing is lost and the tab stays shorter.

## Round 19 (27 Oct 2026), single page (final-single.html)

1. **Size pill removed** next to the "Size" label. The select and helper line stay (`sizeLabel` getter is still used by other parts).
2. **Stores dialog:** each row is store name (bold), full address (text-sm slate-500) and a "Directions" text link (Google Maps search URL from the homepage footer), with the stock status on the right. `data-stores` gains `address` and `map`; `rows` in `ohBuy` passes them through. The dialog scrolls inside itself (`max-h-[88vh] overflow-y-auto`). The multi page uses the same markup and JS, so it got the same addresses.
   **Data mapping:** the live store list comes from Magento MSI sources. `address` = source `street` + `city` + `region` + `postcode` joined as "3 Herbert St, Belmont NSW 2280". `map` = the store's Google Maps URL (same one as the footer, built from the store name and place id; keep one list of these in config).
3. **Hero grid** is 30% image / 70% info on desktop (`lg:grid-cols-[minmax(0,3fr)_minmax(0,7fr)]`), same gap. At 1280x800 Add to cart bottom is at y=760.
4. **Thumbnail strip** under the main image even with one image (same markup as the multi page, 4-column grid, active thumb `border-brand-600` 2px), driven by `ohGallery`; add one `li` per extra image.
5. **Price match:** secondary "Price match" button beside Add to cart (stacked, full width on phones). It fires `oh-pricematch` (`openPriceMatch` in `ohBuy`); the `ohPriceMatch` component (js/oneills-pdp.js, markup in `src/pricematch.html`, included in the single page) opens a native dialog (bottom sheet on phones; Escape, backdrop and X close). Fields: name*, phone*, email, competitor price*, competitor link, screenshot or quote (`image/*,.pdf`), hidden `product_name`, `sku`, `size`. The mobile sticky bar stays Add to cart only.
   **Backend:** placeholder action `/pricematch/request/submit` (multipart POST via fetch). The live site already has a price match modal (name, email optional, phone, competitor link optional, competitor price, file upload): reuse its controller and field names, and replace the placeholder action and the field names above with the live ones.
   **Client confirmation needed:** the response time "within one business day" in the success message, and the terms link https://oneillstyres.com.au/terms for "Conditions apply" (and the wording of the one-line terms note).
6. **Brand logo:** `assets/brands/yokohama.svg` (official Yokohama logo) replaces the PNG on both pages, `max-w-[220px] w-full` on the single page. `build.py` inlines `assets/brands/*.svg` as `image/svg+xml` data URIs.
- Round 20 (28 Oct 2026): "Directions" links removed from the store stock popup (address only). Single page: Add tyres to cart and Price match buttons are equal width from `sm` (`flex-1 basis-0` on both); on phones Price match stays full width under Add to cart.

## Round 21 (28 Oct 2026): approved hero, About and Specifications drafts (both pages)

1. **Hero grid** is 3/7 on both (`lg:grid-cols-[minmax(0,3fr)_minmax(0,7fr)] lg:gap-12`; A was 5/8). Gallery: main image box `aspect-square rounded-2xl bg-slate-50 p-6` (no border), 4-column thumbnails `aspect-square rounded-xl bg-slate-50 p-1.5`, active thumb `ring-2 ring-brand-600` (`ohGallery` `thumbCls` now returns the ring classes), divider, Yokohama logo `max-w-[200px]`. B keeps its single thumbnail.
2. **Right column order (A and B):** H1 (`font-display text-2xl sm:text-3xl font-semibold`); row of rating, thin divider (hidden on phones) and car icon with the category text (the eyebrow above the H1 is gone); stock line (ohBuy, "Check all stores"); short description with Read more; B only: Size label, select and helper line; price card; "Secure checkout. Pay later with:" row plus Details link (outside the card); three trust points.
   - **Rating row:** A shows stars, 4.7, "3 reviews" (links to #reviews). B has no reviews: five grey stars and a "Be the first to review" link (`font-medium text-brand-700`) to `#write-review`, the inline review form (B's form wrapper now has `id="write-review"` and `scroll-mt-24`).
   - **Price card** (`rounded-2xl border border-slate-200 bg-white p-5 sm:p-6` plus soft shadow): price in live-site green `text-[#28a745]` with "each" and "Includes GST and new tyre valves". B: right block "Limited trade offer", struck original price and "12% off" pill, bound to `hasOffer`, `originalLabel` and `discountLabel`; the whole block hides when the size has no offer (stacks under the price on phones). Then quantity stepper, Add tyres to cart and Price match (`flex-1 basis-0` from `sm`; on phones the stepper and Add to cart share a row and Price match is full width below). One small line: "Most customers buy 4 · Total $X for N tyres · Choose your store and fitting time at checkout." (bound to `totalLabel` and `qtyLabel`). The form (`#pdp-form`) now wraps the size select (B) and the price card; the stock box and dialogs sit outside it.
   - **Trust points** (replace free fitting, balancing and disposal): store icon "Fitted at 8 local stores", check icon "Family owned since 1961", safety icon "NSW licence MVRL61864" (underlined link to the NSW licence checker). Three columns from `sm`, stacked on phones.
3. **Price match on A too.** `src/pricematch.html` is now a shared template with `{{name}}`, `{{sku}}` and `{{size}}` tokens. Both content files contain `<!-- @include pricematch -->`; `tools/build.py` fills it from `pm=(name, sku, default size)` per page. `ohPriceMatch` now reads its default size from the hidden input's `value` attribute in `init` (before this the size field was blank until a size was picked). Live: replace the three values with the real product data.
4. **About tab (both):** "Rated for your drive" and its `ohGlance` component are removed (the JS component is deleted; the `oh-size` event stays because `ohPriceMatch` uses it). The right column is now a light panel (`rounded-2xl bg-slate-50 p-6`, shown at all sizes, stacked under the text on phones) with "What's included" (including the not-included wheel alignment note) and, under a divider, "Fitting and returns". Section ids `#included` and `#fitting` are kept, so existing anchors still open the About tab.
5. **Specifications tab (both):** What's included and Fitting and returns removed; the 16 rows are split 8 and 8 into two side-by-side tables (`lg:grid-cols-2 lg:gap-8`, stacked on phones).
6. **Check at 1280x800 (preview, includes the 36 px sample-data banner):** Add to cart bottom at y=604 (A) and y=724 (B, size select sits above the price card); both inside the first screen.

## Round 22: wheel product page (28 Oct 2026)

New design C: **`final-wheel.html`** (ROH Apollo, configurable wheel), built by `python3 tools/build.py` from `src/product-content-wheel.html` with `schema/product-jsonld-wheel.html` (`preview-wheel.html` is the same page without the carousel). Template: the approved single-image tyre page (Round 21). Same header, footer, breadcrumb style, sample-data banner, "Current offers" carousel, tabs, price match dialog (shared `src/pricematch.html`, wheel wording applied by `build.py`), stores dialog (same sample store data) and reviews (no reviews yet: grey stars, empty state, inline form).

**Structure.** Breadcrumb (Home > Wheels > ROH Apollo), hero (30/70: gallery with one image per finish, thumbnail strip, divider, ROH logo at natural size `max-w-[140px]`), tabs (About this wheel, Specifications, FAQs, Will it fit?), customer reviews, "Tyres for 18 inch wheels", "Other ROH wheels in 6x139.7". Hero right column: H1 "ROH Apollo 4WD wheel", rating row with "4WD wheels", stock line, two line description, **Wheel finish** (two segmented buttons with colour swatch, selected = brand ring), **Size** select (full price per option, e.g. "18x9 6x139.7 +25 · $429.00"), price card (green price, "each", "Includes GST", stepper, Add wheels to cart, Price match, total line), pay later row, three trust points. No offer block (the product has no special price); reuse the tyre page's offer block if a wheel gets one. Add wheels to cart bottom at 1280x800 with the preview banner: y = 778.

**JS (`js/oneills-pdp.js`, Alpine CSP style, tyre pages unchanged).**
- `ohBuy` reads `data-noun` (default "tyre", wheel page sets "wheel": "1 wheel", "Add wheels to cart", "Order wheels", store status "In stock, 4 wheels") and `data-finishes` (`[{ "id", "label", "sfx", "default" }]`). `pickFinish(e)` reads `e.currentTarget.dataset.finish` (index). Getters: `finishLabel`, `finishValue`, `skuLabel`, `finishCls`, `finishOn`, `sizeDetail`. `data-sizes` entries for wheels carry `d`, `w`, `pcd`, `off` and `sku` (size part, e.g. `APO18925`); the child SKU is `sku + finish.sfx` (`MB` or `FM`).
- Events (window): `oh-size` (now also fired on a finish change; detail adds `finish`, `sku`, `pm`), `oh-finish` (buy box to gallery: show that finish's image) and `oh-pick` (gallery thumbnail click to buy box: thumbnail n selects finish n).
- `ohGallery` gained `onFinish` and `pick` now also dispatches `oh-pick` (nothing listens on the tyre pages).
- `ohPriceMatch` also tracks `sku` (the wheel page binds the hidden `sku` input, so the SKU follows the finish) and uses `detail.pm` ("18x9 6x139.7 +25, Matte Black") for the size when present.
- New `ohWheelSpec`: the spec tables and the "How to read your wheel size" capsule and legend follow the selected size and finish (diameter, width, PCD, studs, offset, SKU, finish).
- `build.py` inlines `assets/brands/*.webp` too, writes the wheel schema (Product with brand ROH, model Apollo, AggregateOffer low 405.00, high 429.00, 10 offers = 5 sizes x 2 finishes, each with its own SKU and child URL; BreadcrumbList; FAQPage; no aggregateRating) and takes a per page `title` (tyre titles still append " Tyre"). Tailwind: the `finishCls` classes only exist in the JS getter, so they are listed in a safelist comment at the top of the content file; add them to the Hyvä safelist.

**Data mapping (Magento).** Configurable product "ROH Apollo" with two super attributes: `wheel_finish` (Matte Black, Machined) and the size / specifications attribute (live labels like "18x9 6x139.7 +25"). Children are simple products (SKU `APO` + diameter + width + offset + `MB`/`FM`, e.g. APO18925MB; URL `/roh-apollo-matte-black-18x9-6x1397-25-apo18925mb`). The page needs the label parsed into diameter, width, PCD and offset: either separate attributes (preferred: rim diameter, rim width, PCD, offset) or parse the specifications label with `^(\d+)x(\d+) (\d+x[\d.]+) ([+-]\d+)$`. Images: one per finish (live `roh-apollo-mb.webp` and `roh-apollo-fm.webp`); the gallery order must match the finish order. Prices are per child; show the full price in each option. Default child: Matte Black, 18x9 6x139.7 +25, $429.00. Parent SKU is not known, so the schema omits `sku` on the parent (children carry theirs). Product URL in the schema is `/apollo` (live).

**Copy decisions.** Description and key features rewritten from the live text (no claims added). Brand page for ROH is unknown: "ROH wheels" links to `/wheels`. The Apollo is 6x139.7 only; "common on many dual-cab utes and 4WDs" names no vehicles. The related heading is "Other ROH wheels in 6x139.7" (not 18x9) because the only confirmed live Arc URLs are 17x9 +12.

**Client confirmations (not stated on the page unless noted).**
1. **Load rating unit.** Live shows "Load index 1500". The page says "Load rating: 1500 kg per wheel" (also in the schema). Confirm it is kg per wheel.
2. **Inclusions for wheels** (shown, mark as confirm): "Fitting at the O'Neills store you choose", "Wheel balancing when fitted with tyres", "GST", and the FAQ "Do you fit and balance the wheels? Yes, at any O'Neills store". Also confirm "Fitted at 8 local stores" (trust point) applies to wheels, the fitting and returns copy (the tyre page's "30 to 45 minutes for a set of four" was dropped as unverified), and "Ask our team to check wheel nut torque after the first drive".
3. **Not shown, unknown:** centre bore, weight, TPMS compatibility, wheel nuts or caps included, warranty. Add rows when the data exists (centre bore matters for fitment).
4. **Not shown:** "Fitted and balanced with your tyres at any O'Neills store" in the price card. Add it only if confirmed.
5. **Live site problems to avoid.** The live wheel page shows tyre perks ("Old tyre disposal") which must not appear on wheels. The live size dropdown shows "17x9 ... - $24.00", which reads like an extra charge but is $24 cheaper than the 18 inch; this page shows full prices instead.
6. **Related and offers.** The two ROH Arc cards use a neutral box with the ROH logo because no Arc images are available; replace with the product photos (Magento related or same-pattern products). The "Current offers" carousel is the tyre copy ("Buy 3 tyres, get the 4th free" and so on): confirm which offers apply to wheels, or hide it for wheels.
7. **Price match.** Wording changed to "this wheel" and "identical wheels". Same backend and confirmations as Round 19.
- Round 23: review form fields forced to white (bg-white, color-scheme light, autofill override) so browser autofill or dark mode never paints them grey/black.
- Round 24: Specifications show as one continuous table on phones (two side-by-side tables from lg).

## Store picker

The global store picker (`ohStorePicker`) is shared with the homepage: this build pulls `../src/store-picker.html`
(via `HOME`), and the trigger buttons are in this folder's own `src/header.html`, in the utility bar before
"Find a store" and in the mobile drawer. The choice is kept in localStorage under `oh-store`. See the homepage
DEV-NOTES for the full description.

**Open point:** the buy box has its own "In stock at {store} / Change store" control, which opens the per-product
stock dialog. That answers a different question from the global picker, but the two can currently disagree.
Make the buy box default to the store saved in `oh-store`.
