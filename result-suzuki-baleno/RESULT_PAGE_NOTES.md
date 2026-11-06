# Tyre results page: Suzuki Baleno 1.0T

Reference build: `result-suzuki-baleno.html`. Generator: `build-result.py`.
Live page audited: `/tyres/result/?make=suzuki&model=baleno&generation=081be9fdff&modification=709b6839d7`.

---

## Changes you asked for

| Change | Status |
|---|---|
| Specs as readable badges, not a raw dump | Done, then changed to a key-value `<dl>` grid on request |
| Escape hatch beside the H1 | Done, now reads "Not your car? Change model" |
| Fitment status badge on the selected size | Done, then removed on request; the OEM marker stays in the dropdown |
| Breadcrumb down to the full vehicle name | Done, five levels, with `BreadcrumbList` schema |
| Remove `[Manual Update Needed]` | Done, gone |
| Rename `TPC Category 1` and `TPC Category 2` | Done, now `Vehicle type` and `Tyre category` |
| Deduplicate overlapping categories | Done, see below |
| Reorder the sidebar | Done: brand, price, tyre category, vehicle type, speed rating, size |
| Remove availability | Done, gone |

### Specs as a key-value grid

`Bolt Pattern: 4x100 | Centre Bore: 54.1` and `Petrol (110 hp) — 2019-2023` are now a definition
list: a real `<dl>` with four `<dt>` / `<dd>` pairs for Engine, Built, Bolt pattern and Centre
bore. Four columns on desktop, 2x2 on mobile, separated by hairline rules rather than pill
containers.

The label is 12.5px at 70 percent white; the value is Space Grotesk 700 at 18px in solid white.
That contrast between muted label and strong value is what makes it scan as a spec table, which is
the automotive convention, rather than as a row of tags.

This was pills first and was changed on request. The `<dl>` markup is also the semantically
correct element for name-value pairs, so screen readers announce each label with its value.

### Fitment badge

The selected size carries a green **Recommended fitment** badge with a tick. The dropdown also
marks the factory option with a small **OEM** pill, so the distinction holds once the list is open.
Picking a non-standard size hides the badge, which is the honest behaviour: the reassurance only
shows when it is actually true. The two alternatives (87V and 83H) were taken from the live
fitment list.

### Category deduplication

The live `TPC Category 2` had six values with two overlapping pairs:

| Live | Here |
|---|---|
| Touring | Touring |
| Performance | Performance |
| High Performance, UHP, Ultra High Performance | High performance |
| EV | EV ready |

Three labels collapsed into one. `UHP` is an abbreviation of `Ultra High Performance`, and both are
the same tier as `High Performance`, so keeping three separate checkboxes split the same stock
across filters that each returned a partial list.

`Size / specifications` had the same problem, with eight entries for four real sizes
(`185/55R16 83 V`, `185/55R16 83V` and `185/55R16H 83H` are formatting variants, not different
tyres). That is now four. `EV Tyres` had `Y` and `YES` as separate options; EV is now a value under
Tyre category instead of its own yes/no group.

**These are display-level fixes.** The duplicates come from the product attribute data in Magento.
Cleaning them at the source would stop them reappearing and would fix the same filters everywhere
else on the site.

---

## Second round of changes

| Change | Status |
|---|---|
| Remove the pill/badge | Done, the "Recommended fitment" badge is off the fitment trigger |
| Tyre images in the catalogue | Done, the real catalogue photo for all 12 |
| Quantity selection | Done, a stepper on every card |
| "In stock" pill top right, replacing Touring | Done |
| "Check store to see stock availability" plus popup | Done, a sheet listing all 8 workshops |
| Offer and discount price layout on one tyre | Done, on the Yokohama BluEarth ES32 |
| Price style, colour and font from the live store | Done, Space Grotesk 700 in `#28a745` |
| Add to Cart and Price Match side by side under the price | Done, equal width, stacking on mobile |
| Remove the was price | Done, then restored as a struck grey figure on request |
| Tyre image at full tile size | Done, fills 95 percent of a 232px tile |
| Wishlist icon | Done, a heart toggle beside the brand logo |
| Remove "each, fitted" | Done |

### Which badge I removed

"Remove the pill/badge" was ambiguous, since the page had three kinds. I read it as the green
**Recommended fitment** badge on the fitment trigger, because the next instruction replaces the
product card pill rather than removing it, and the header spec pills were the previous round's
request. The **OEM** marker is still in the open dropdown, so the factory option is still
identifiable. If you meant the header spec pills instead, that is a one-line revert.

### Tyre images

Pulled from `/media/catalog/product/cache/...`, each product's own catalogue photo from its product
page. All 12 resolve. `mix-blend-mode: multiply` drops the white background into the tile. First
four load eagerly, the rest lazily, with width and height set so nothing shifts.

### Quantity stepper

Minus, number, plus on every card, clamped between 1 and 8 and sanitised on manual entry. Tested:
typing junk resets to 1, and holding either button stops at the limit rather than running past it.

### Stock popup

The link under each tyre opens a modal naming that tyre and listing all 8 workshops with a status
chip and a click-to-call number. It locks body scroll, restores the exact position on close, and
closes on the button, Esc and backdrop.

**The per store status is placeholder.** There is no stock-by-branch feed in this build, so the
states alternate. Wire it to real inventory before this ships, because a wrong "In stock" is worse
than no status at all. The same goes for the "In stock" pill on the cards.

### Offer layout

Demonstrated on one tyre, the Yokohama BluEarth ES32. The pill became a **diagonal corner ribbon**
cutting across the top left corner of the card, so it reads as a flash on the card rather than a
tag floating over the tyre.

It is built as a 128px square clipped box pinned to the card corner, holding a 168px band rotated
45 degrees. The card itself carries `overflow: hidden`, so the ribbon is trimmed to the rounded
corner on both sides. The badge markup moved out of `.p-media` and onto `.p-card` so it can reach
the corner rather than being held inside the image box's padding.

It works in both layouts. In grid it crosses the top of the tyre image; in list it crosses the top
of the grey image panel. Rendered examples are saved as `special-offer-ribbon-grid.jpg` and
`special-offer-ribbon-list.jpg`.

The ribbon is `pointer-events: none`, so it never intercepts a click meant for the card.

### Price and buttons matched to the live store

Pulled the real values off the live product and brand pages rather than guessing:

| Element | Live value | Used here |
|---|---|---|
| Price | Space Grotesk, 700, `#28a745` green, 24px on cards | Same |
| Add to Cart | `linear-gradient(to right bottom, #1a5fb4, #2563eb, #1a5fb4)`, white, 600, 12px radius | Same |
| Price Match | White, 1px grey border, grey-700 text, 600, 12px radius | Same |

The two buttons sit side by side under the price, equal width, and stack full width on mobile.
Both labels use the live store's capitalisation, "Add to Cart" and "Price Match".

### Price layout

"each, fitted" is gone from every card. The original price came back on the discounted tyre as a
struck-through grey figure above the current price: Space Grotesk 600 at 15px in `#8a95a3`, with a
1.5px strike so the numbers stay readable rather than being crossed out into illegibility. The
current price keeps the live store's green.

The discounted card therefore carries three consistent signals: the **Save $30** badge on the
image, the struck original, and the green current price.

### Image and wishlist

The media tile grew from 160px to 232px and the photo now fills it, 95 percent of the tile height
rather than a small thumbnail floating in space. 176px on mobile. The heart sits beside the brand
logo, toggling `aria-pressed` with a filled red state when on. It is presentation only in this
build; wire it to the wishlist endpoint the header icon already uses.

## Third round of changes

| Change | Status |
|---|---|
| Grid and list view switch | Done, in the results head, grid active by default |
| Vehicle brand logo on the image where applicable | Done, from the live OE data: Honda and BYD |
| "Save $30" replaced with "Special offer" | Done |
| Smaller quantity stepper | Done, 28px tall rather than 36px |
| Single price, no special price | Done, one price per card, no strikethrough |
| "EA" after the price | Done, on all 17 |
| Pagination for page 2 | Done, all 17 products now in the page, 12 plus 5 |
| "In stock at [store]" with the store popup on the right | Done |

### The OE vehicle logos are real

The live listing serves them from `/media/meetanshi/oem/`, and only two tyres in this fitment carry
one: **Honda** on the Dunlop SP Sport 2030 and **BYD** on the Hankook iON ST. Both files resolve.
Nothing was invented, and no logo was put on a tyre the live data does not mark.

The badge sits bottom right of the image, because top left is the offer badge. On the live site it
is top right.

### All 17 products, not 12

Page 2 was fetched and merged, so the page holds the full fitment: 17 tyres with their real prices,
images and URLs. Pagination shows 12 then 5, with Previous and Next disabling at the ends.

**Paging suspends while filters are active.** Filtering to Dunlop returns 4 across both pages
rather than 4 on page 1 and a hidden one on page 2, and the pager hides. Paging a filtered set is
where these pages usually mislead people.

### Offer and price

The badge now reads **Special offer** and the card shows a single price, the real $239.00, with no
struck comparison. That removes the fabricated $269 entirely, which was the one number on this
page that had no source. The badge is now a flag, not a price claim, so the Australian Consumer
Law concern about was/now pricing no longer applies.

### Stock line

`Check store to see stock availability` is replaced by **In stock at [workshop]** in green on the
left, with **All stores** on the right opening the same popup. The store named per card is
placeholder, cycling through the eight workshops, and needs the real per-branch feed.

**The green "In stock" pill on the image is gone.** The line below now says the same thing with the
workshop added, and the brief says not to repeat the same trust signal on one card. Say the word
if you want the pill back as well.

### List view

The list layout puts the image left at 170px with the details beside it and the price block on the
right, collapsing back to the card layout on mobile where a row that wide does not fit.

## Fourth round of changes

| Change | Status |
|---|---|
| List row in the given order | Done, as a two-column card per the follow-up screenshot |
| Brand logo on the tyre image, small, no border or box | Done |
| Tyre image full width, no curved grey tile | Done, in both views |

### List card layout

Rebuilt to match your screenshot: a grey image panel down the left at full card height, with
everything else stacked on the right. Top to bottom on the right: brand logo with the wishlist
opposite it, product name, tread code, Qty stepper, the availability bar, price with EA, then Add
to Cart and Price Match.

The first attempt put all nine pieces on one horizontal line, which is what the earlier bullet list
read as. Your screenshot showed the two-column form instead, so the card is now a CSS grid, 210px
image column plus the content column, with `grid-row` placing each piece. The markup is unchanged,
so the same HTML still drives the grid card.

The availability bar picked up the styling from your screenshot: light blue field, blue rule down
the left edge, status on the left and the stores link on the right.

Card height came out at 342px against a 908px column. On mobile it falls back to the stacked card,
with the grey panel and the bar styling dropped since neither works at that width.

The wishlist heart is inset 20px from the card edge in list view, so it lines up with the right
edge of the availability bar and the Price Match button rather than sitting hard against the
border.

### One card per row on mobile

The grid was two up at 375px. It is now one, which gives the image 232px of height instead of 124px
and lets Add to Cart and Price Match sit side by side again rather than stacking. Fewer products
per screen, but each one is legible, and on a result page for a single fitment the list is short.

### Image and OE logo

The grey rounded tile is gone in both views; the tyre now sits directly on the card at full width.
The OE logo lost its white box and border and sits small at the top right of the image, 26px in
grid and 22px in list.

### Two bugs found and fixed while testing

1. **Four brand logos were 404s.** Falken, Kumho, Toyo and Triangle were paths I had guessed
   earlier rather than read off the live page. All twelve brand logos now come from the live
   listing and all return 200.
2. **Images stopped loading after paging.** An image deferred by `loading="lazy"` while its card
   is `display: none` does not resume when the card is shown again, so going to page 2 and back
   left most of page 1 blank. Fixed by promoting any unloaded image in a now-visible card to
   `loading="eager"`. Verified: 12 on page 1, 5 on page 2, and 12 again on return, all loaded.

---

## Deviations worth knowing

1. **The breadcrumb text differs from your example.** You wrote
   `Suzuki Baleno Hatchback 1.4L Petrol (2016 to 2022)`, but the URL you linked is the 1.0T in the
   2019-2023 facelift generation. A breadcrumb naming a different engine and different years than
   the page is showing would be wrong, so the last crumb is built from the vehicle data and reads
   `Suzuki Baleno Hatchback 1.0T Petrol (2019 to 2023)`. The format is yours. Say the word if you
   want the literal string instead.
2. **All 17 products are present**, taken from both live pages, with their real prices, images and
   URLs.
3. **Prices shown as "each, fitted".** The live page shows `$239.00 EA` with a separate
   "Available on 30th October" line. Availability dates went with the availability filter.
4. **The page is `noindex, follow`.** A faceted result page for one vehicle variant should not
   compete in the index with the category pages.

---

## Verified in this build

- Breadcrumb renders all five levels and matches the `BreadcrumbList` schema
- Specs render as a `<dl>`, four columns at 1280px and 2x2 at 375px
- No `TPC Category`, `Manual Update Needed` or availability text anywhere in the DOM
- Sidebar order is brand, price range, tyre category, vehicle type, speed rating, size
- Brand filter cuts 12 to 4 Dunlops; adding Under $150 cuts to 1; an impossible combination shows
  the empty state instead of a blank grid; clearing restores all 12
- Sort by price high to low returns $255, $245, $239
- Fitment picker opens and switches size and meta; the OEM marker stays in the list
- All 12 catalogue photos load; 12 "In stock" pills, 12 qty steppers, 12 stock-check links
- Qty stepper clamps at 1 and 8 and resets junk input to 1
- Stock popup names the right tyre, lists 8 workshops, locks and restores scroll
- Offer layout renders on the Yokohama only: Save $30 badge, struck grey $269, green $239
- All 12 photos load and fill 95 percent of the tile; 12 wishlist hearts toggling both ways
- Price is Space Grotesk 700 at `rgb(40, 167, 69)`, matching the live store
- Add to Cart carries the live gradient; Price Match is the white outline variant; both 44px
- No "was" price and no "each, fitted" anywhere in the DOM
- Mobile collapses the sidebar behind a Filters button that toggles both ways
- Mobile grid is one card per row; all 12 page-one photos load
- No horizontal overflow at 1280px or 375px

---

## Third round of changes

| Change | Status |
|---|---|
| Remove quantity box from product grid | Done, quantity is selected in the Add to Cart popup modal |
| Product title on popup should be black | Done, set to bold `#000000` on both cartSheet and stockSheet |
| Yokohama promotion banner & quantity selection offer | Done, added "Buy 3 Get 4th Free" promo banner, ribbon, and dynamic cart calculation with breakdown |
| Move Yokohama tyres to index 0 and 1 | Done, both Yokohama tyres now lead the catalogue on Page 1 |

### Quantity stepper removed from product grid
The quantity steppers (`-`, `qty input`, `+`) on all 17 product cards in `.p-actions` were removed because quantity selection is handled by the "Add to Cart" popup sheet. The "Add to Cart" CTA now spans the full card width (44px height), providing a cleaner and more focused card UI.

### Product title on popups
Styled `#cartSub` and `#stockSub` explicitly to `#000000` with 600 semi-bold weight. Headings are also crisp black.

### Yokohama promotion banner & cart breakdown
Yokohama tyres feature the national promotion: **Buy 3 Get 4th Tyre Free (plus $30 fitting fee for the 4th tyre)**:
1. **Product Cards**:
   - Diagonal corner ribbon over image: `BUY 3 GET 1 FREE`
   - Single clean regular unit price displayed (`$239.00 EA` / `$255.00 EA`), with no special price calculation boxes or hints cluttering the grid.
2. **Quantity Selection Popup Tray (`#cartSheet`)**:
   - Header shows Yokohama promotional callout.
   - Defaults directly to 4 tyres so the special offer and savings are immediately clear.
   - The 4 tyres tier shows strikethrough regular price, promotional price, and a "Special Offer - Save $209" badge.
   - Dynamic Order Summary preview matching the cart screenshot:
     - Subtotal (4 x $239.00): $956.00
     - Discount (4th tyre): - $239.00
     - Fitting Fee for 4th Tyre: $30.00
     - Grand Total Incl. Tax: $747.00
     - "You save $209.00 with the Yokohama promotion!"
   - Stepper supports custom quantities with dynamic promotion recalculation (and tips when 3 tyres are selected).


