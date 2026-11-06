# O'Neills Tyre Category Page CRO & SEO Improvement Blueprint

This document details the conversion rate optimization (CRO), user experience (UX), and search engine optimization (SEO) improvements for **O'Neills Tyre & Autocare** category pages, directly mapped to the instructions in `Oniellls Tyre optimization.docx`.

A production-ready reference implementation has been created at `category.html`.

---

## 1. Category Page Core CRO & Layout Architecture

### 1.1 Breadcrumbs (Mandatory Sitewide)
* **Guideline:** Breadcrumbs must be present on every page.
* **CRO & SEO Impact:** Lowers bounce rates by giving users immediate orientation and allowing them to jump one tier up (e.g., from *4WD & All-Terrain Tyres* back to *All Tyres*). Helps search engine crawlers understand site taxonomy.
* **Implementation:** Clean, accessible `<nav aria-label="Breadcrumb">` with structured microdata (`ItemList` schema).

### 1.2 Category Heading & Short Description (The 2-Line Rule)
* **Guideline:**
  * Category must follow the correct heading structure (H1 for category name).
  * Right after H1, there should be short introductory content restricted to 2 lines with a "Read more" toggle in the 2nd line.
* **Why this matters for CRO:**
  * Pushes the product grid and tyre filters higher up the screen on both desktop and mobile.
  * Prevents high drop-off caused by pushing inventory below the first fold with huge blocks of text.
  * Preserves SEO keyword relevance while letting interested users expand the copy smoothly without page reload or layout shift.

### 1.3 Audience-Specific Filters & Sticky Mobile Bar
* **Guideline:** Category pages must have audience-specific filters and sorting options, made sticky on mobile.
* **Tyre-Specific Filter Logic:**
  * Tyre Width (e.g., 245 mm, 265 mm, 285 mm)
  * Profile / Aspect Ratio (e.g., 60, 65, 70, 75)
  * Rim Diameter (e.g., 16", 17", 18", 20")
  * Terrain Suitability (All-Terrain A/T, Mud-Terrain M/T, Highway-Terrain H/T)
  * Brand filter (BFGoodrich, Falken, Toyo, Maxxis, Pirelli, Kumho)
* **Mobile Experience:** Sticky filter and sort buttons on mobile (at `top: 60px` right under header) so shoppers can adjust size or sort without having to scroll all the way back up.

---

## 2. Product Grid & Card CRO Standards

### 2.1 No Hover "Lift Up" Effect
* **Guideline:** Product grid on category or any page does not require the hover effect like lift up.
* **Implementation:** Removed all `transform: translateY(-Xpx)` transitions. Hover interactions use subtle border-color darkening and subtle box-shadow only. This keeps the layout steady, reduces visual friction, and avoids misclicks on touch-enabled hybrid laptops.

### 2.2 Brand and Category Separation
* **Guideline:** Put the brand that the product follows, and also category. Do not put both on the same column or merge them together.
* **Implementation:**
  * Top-left badge: **Brand Name** (e.g., BFGoodrich, Falken, Toyo).
  * Top-right badge: **Terrain / Category Type** (e.g., All-Terrain A/T, Mud-Terrain M/T).
  * Clear visual separation helps users compare brands and terrain classes quickly.

### 2.3 Product Image Visibility Ratio
* **Guideline:** Product image visibility ratio depends on the store/brand. Tyres do not require 50% container visibility for images.
* **Implementation:** Tyre images are sized cleanly at 110px to 140px height inside a dedicated containment container. This leaves ample room for tyre dimensions, technical specifications, load/speed ratings, fitted pricing, and the action button above the fold.

### 2.4 Prevention of Thin Content on Product Cards
* **Guideline:** Sitewide pages and products should not return thin content.
* **High-Utility Tyre Data on Every Card:**
  * Tyre Size Pill (e.g., `265/70 R17 121/118S`)
  * Terrain split / driving usage (e.g., `50% Dirt / 50% Road`)
  * Load and Speed rating index
  * Sidewall construction or wet braking rating
  * Upfront transparent pricing (`Includes fitting, balancing & eco disposal`)

### 2.5 Single, High-Intent Call to Action (CTA)
* **Guideline:**
  * CTA should be placed at the right place, not more than 1 or 2 CTAs on the same section or screen.
  * Using the correct CTA text matters more than anything.
* **Implementation:**
  * Changed vague labels like "Buy Now" or "Submit" to high-intent, action-oriented text: **"Select Fitting Location"** or **"Book Fitting & Reserve"**.
  * Exactly 1 prominent CTA per tyre card to prevent decision paralysis.

---

## 3. SEO & Content Architecture: Post-Grid Long Description

### 3.1 Long Description Placement (After the Product Grid)
* **Guideline:** After the product grid, there should be category's long description. This is best for SEO and internal linking.
* **CRO Benefit:** Tyre shoppers come to see products, sizes, and prices first. Forcing users to scroll through 800 words of text before seeing products causes high bounce rates. Placing the deep guide *after* the grid satisfies crawlers and gives interested buyers the technical knowledge they need.
* **Content Sections Included:**
  * Comparison Table: All-Terrain (A/T) vs Mud-Terrain (M/T) vs Highway-Terrain (H/T).
  * Tyre Sidewall Guide: How to decode width, aspect ratio, rim diameter, load index, and speed rating.
  * Internal Linking: Contextual links to Wheel Alignment, Logbook Servicing, and 4WD Suspension upgrades.

### 3.2 Non-Repetitive EEAT & Trust Factors
* **Guideline:**
  * Site should suggest EEAT factors with proof.
  * Do not show similar trust factors repeatedly as it makes nonsense.
* **Implementation:** Single dedicated trust strip with 4 distinct, meaningful credentials:
  1. *Licensed Tyre Technicians:* Digital wheel balancing and mounting by certified mechanics.
  2. *100% Genuine Warranties:* Australian manufacturer warranty coverage.
  3. *8 Local Hunter Locations:* 35+ years serving Belmont, Cessnock, Gateshead, Kurri Kurri, Maitland, Rutherford, and Warners Bay.
  4. *Transparent Fitting Package:* New rubber valves, balancing, and eco-disposal included.

---

## 4. Typography, Copywriting & Design Consistency

### 4.1 Strict Punctuation & Style Rules
* **No Em Dash:** Zero em dash characters throughout content, headings, and metadata.
* **No Uppercase Body Text:** Sentence case and clean title case used throughout. No uppercase blocks for paragraph copy.
* **Consistent Brand Styling:** Standardized 4px button border radii, cohesive hex palette (`#c82026` primary red, `#1a2430` dark slate), and unified padding scales.
* **Zero Lucid Icons:** 100% inline bespoke SVGs tailored for tyre tread, phone, map pin, funnel, wrenches, and checkmarks.
* **Localization:** Australian English terminology throughout (`Tyres`, `Autocare`, `Rego`, `NSW`, `kilometres`).

### 4.2 Interactive Zero-Lag Elements
* **Instant Accordion:** FAQ accordion triggers instantly with vanilla JS without external layout shifts.
* **Container Overflow Safety:** Every section is bounded within max-width containers with zero horizontal scroll on mobile viewports.

---

## 5. Summary Checklist of Applied Rules

| Rule from Document | Implementation Status in `category.html` |
|---|---|
| No lucid icons sitewide, use right SVGs | Applied: 100% pure inline SVGs for all icons |
| No em dash in content | Applied: Zero em dashes used anywhere |
| Right heading structure | Applied: H1 category title -> H2 product names & section titles -> H3 card sub-specs |
| Font sizes visible desktop & mobile | Applied: Base 16px font, clear contrast ratios |
| Sitewide pages shouldn't return thin content | Applied: Rich tyre specs, load ratings, terrain split, fitting inclusions |
| Each section should not overflow container | Applied: `max-width: 1240px` and responsive auto-wrap |
| Context should not mismatch (EEAT factors) | Applied: Authentic Hunter Valley locations, warranty terms, certified fitting |
| CTA placed correctly, max 1 to 2 per screen | Applied: 1 clear CTA per card, no overlapping sticky buttons |
| No uppercase for content | Applied: Clean readable sentence case |
| Correct CTA text | Applied: "Select Fitting Location", "Find My Tyre Size" |
| Category filters & sorting with sticky mobile | Applied: Audience-specific filters (width, profile, rim, terrain), sticky on mobile |
| Product grid NO hover lift up effect | Applied: Flat design with subtle border/shadow highlight only |
| Right after H1: 2 lines content with Read more | Applied: CSS line clamp with interactive toggle in line 2 |
| Long description after product grid | Applied: Detailed tyre buying guide placed directly after grid |
| Breadcrumbs present | Applied: Semantic breadcrumb navigation at top |
| Product image visibility ratio for tyres | Applied: Balanced 110px-140px tyre imagery (not oversized) |
| Brand and Category not on same column | Applied: Brand badge left, Category badge right on separate tags |
| Don't show similar trust factors repeatedly | Applied: 4 distinct proof points (technicians, warranty, local, no hidden fees) |

---

## 6. Technical Filter Architecture & Core Web Vitals Refactoring

The category page filter engine has been refactored into an isolated island architecture with the following guarantees:

1. **Server-Rendered First Page (Zero CSR Delay):**
   * The first 6 products render directly in the HTML payload with complete semantic markup (`<ul role="list">` and `<li><article>`).
   * Crawlers and low-bandwidth users view complete product listings with zero client-side JavaScript execution required.

2. **Core Web Vitals Protections:**
   * **LCP:** Top 2 product cards feature `fetchpriority="high"` and `loading="eager"`. Remaining cards use `loading="lazy"` and `decoding="async"`.
   * **CLS:** Image containers enforce an explicit `aspect-ratio: 1 / 1` and fixed bounding box, completely eliminating layout shifts.
   * **INP:** Filter inputs are debounced by 300ms. List updates are scheduled through `requestAnimationFrame` to yield the main thread between user input and DOM mutation.

3. **URL State Synchronization & Crawl Budget Safeguards:**
   * Filter updates sync cleanly to `window.location.search` via `history.replaceState` for continuous changes and `history.pushState` for definitive selections.
   * Deep linking is fully supported: loading `?width=265&profile=70&rim=17` automatically synchronizes the UI controls and applies the filter slice.
   * If 3 or more faceted parameters are applied, the page dynamically injects `<meta name="robots" content="noindex, follow">` and points the canonical link to the root category, preventing combinatorial crawl explosion.

4. **Bot-Friendly Hybrid Pagination:**
   * An accessible standard link `<nav class="pagination-nav"><a href="?page=2" rel="next">...</a></nav>` provides indexable crawl paths for search engine spiders.
   * For human visitors, an `IntersectionObserver` sentinel automatically streams subsequent product batches while updating the address bar to `?page=2` dynamically.

5. **Structured Data:**
   * Valid `BreadcrumbList` and `ItemList` JSON-LD schemas are embedded directly in the `<head>` of the document.
