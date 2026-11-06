/**
 * O'Neills product page Alpine components (tyres).
 * Written for Hyvä's Alpine CSP build, like js/oneills-home.js: templates only reference properties, getters and
 * argument-free methods. Load after the homepage components (ohHeader and ohSticky's call sheet are shared).
 */
(function () {
  'use strict';

  var QTY_MIN = 1, QTY_MAX = 8; // stepper range 1 to 8 (default 1 at client request)
  var money = new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' });

  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  // ISO date (2026-10-28) to the AU short form "Wed 28 Oct"
  function fmtDate(iso) {
    var d = new Date(iso + 'T00:00:00Z');
    return isNaN(d.getTime()) ? '' : DAYS[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()];
  }
  function fmtLongDate(iso) {
    var d = new Date(iso + 'T00:00:00Z');
    if (isNaN(d.getTime())) return '';
    var day = d.getUTCDate();
    var sfx = (day === 1 || day === 21 || day === 31) ? 'st' : (day === 2 || day === 22) ? 'nd' : (day === 3 || day === 23) ? 'rd' : 'th';
    var fullMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return day + sfx + ' ' + fullMonths[d.getUTCMonth()];
  }

  function getCookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function setCookie(name, val, days) {
    var maxAge = (days || 90) * 86400;
    document.cookie = name + '=' + encodeURIComponent(val) + ';path=/;max-age=' + maxAge + ';SameSite=Lax';
  }

  function register() {
    // Buy box: quantity stepper 1 to 8 (inc/dec), live total, BNPL text, and the mobile sticky bar.
    // data-price = price each incl. GST; data-qty = starting quantity.
    Alpine.data('ohBuy', function () {
      return {
        price: 0, regular: 0, qty: 1, barShown: false, sizeOpen: false, stores: [], sizes: [], sizeIdx: 0, finishes: [], finishIdx: 0, noun: 'tyre',
        init: function () {
          var self = this, ticking = false;
          try { this.stores = JSON.parse(this.$el.dataset.stores || '[]'); } catch (e) { this.stores = []; }
          // Personalized user location cookie (90 days)
          var savedStore = getCookie('oneills_selected_store');
          if (savedStore && this.stores.length) {
            var matched = this.stores.find(function (s) { return s.name.toLowerCase() === savedStore.toLowerCase(); });
            if (matched) {
              this.stores = [matched].concat(this.stores.filter(function (s) { return s.name.toLowerCase() !== savedStore.toLowerCase(); }));
            }
          }
          this.regular = parseFloat(this.$el.dataset.price) || 0;
          this.price = this.regular;
          // Optional size options (configurable product): data-sizes = [{ "id": 101, "label": "225/60R17 99H", "price": 259, "offer": 227.92, "default": true }, ...].
          // price = regular price each incl. GST; offer = active special price (Magento special_price within its dates), omitted or null when there is none.
          try { this.sizes = JSON.parse(this.$el.dataset.sizes || '[]'); } catch (e2) { this.sizes = []; }
          this.sizes.forEach(function (s, i) { if (s.default) { self.sizeIdx = i; self.apply(s); } });
          // Wheels: data-noun="wheel" changes the wording ("1 wheel", "Add wheels to cart"); tyre pages leave it unset.
          this.noun = this.$el.dataset.noun || 'tyre';
          // Optional finish options (wheel page): data-finishes = [{ "id": 300, "label": "Matte Black", "sfx": "MB", "default": true }, ...]. sfx is the SKU suffix.
          try { this.finishes = JSON.parse(this.$el.dataset.finishes || '[]'); } catch (e3) { this.finishes = []; }
          this.finishes.forEach(function (f, i) { if (f.default) { self.finishIdx = i; } });
          this.qty = parseInt(this.$el.dataset.qty, 10) || 1;
          // Sticky bar (phones and tablets) shows whenever the main Add to cart button is off screen, above or below,
          // so there is always exactly one way to add to cart in view, never two
          function check() {
            var cta = self.$refs.cta, r = cta ? cta.getBoundingClientRect() : null;
            self.barShown = !!r && (r.bottom < 0 || r.top > window.innerHeight);
            ticking = false;
          }
          function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(check); } }
          window.addEventListener('scroll', onScroll, { passive: true });
          window.addEventListener('resize', onScroll, { passive: true });
          check();
        },
        get decDisabled() { return this.qty <= QTY_MIN; },
        get incDisabled() { return this.qty >= QTY_MAX; },
        dec: function () { if (this.qty > QTY_MIN) { this.qty -= 1; } },
        inc: function () { if (this.qty < QTY_MAX) { this.qty += 1; } },
        setQty: function (n) {
          var val = Math.max(QTY_MIN, Math.min(QTY_MAX, parseInt(n, 10) || 1));
          this.qty = val;
        },
        selectStore: function (name) {
          if (!name) { return; }
          setCookie('oneills_selected_store', name, 90);
          var matched = this.stores.find(function (s) { return s.name.toLowerCase() === name.toLowerCase(); });
          if (matched) {
            this.stores = [matched].concat(this.stores.filter(function (s) { return s.name.toLowerCase() !== name.toLowerCase(); }));
          }
          this.closeStores();
        },
        toggleSize: function () { this.sizeOpen = !this.sizeOpen; },
        closeSize: function () { this.sizeOpen = false; },
        selectSize: function (i) {
          var s = this.sizes[i];
          if (s) { this.sizeIdx = i; this.apply(s); this.announce(); this.sizeOpen = false; }
        },
        // Sets the regular price and the price actually charged (the offer when there is one)
        apply: function (s) { this.regular = s.price; this.price = (s.offer && s.offer < s.price) ? s.offer : s.price; },
        // Size select: @change="pickSize" receives the event as its first argument (same pattern as the gallery's pick); the option value is the index into data-sizes.
        pickSize: function (e) {
          var i = parseInt(e.currentTarget.value, 10), s = this.sizes[i];
          if (s) { this.sizeIdx = i; this.apply(s); this.announce(); this.sizeOpen = false; }
        },
        // Tells the price match dialog and the spec tables which size (and finish) is selected: window event "oh-size".
        // On tyre pages the detail is the size entry itself. With finishes it also carries finish, sku and pm (the price match size text).
        get sizeDetail() {
          var s = this.sizes[this.sizeIdx] || {}, f = this.finishes[this.finishIdx];
          return f ? Object.assign({}, s, { finish: f.label, sku: (s.sku || '') + (f.sfx || ''), pm: s.label + ', ' + f.label }) : s;
        },
        announce: function () { window.dispatchEvent(new CustomEvent('oh-size', { detail: this.sizeDetail })); },
        // Finish buttons: @click="pickFinish" reads data-finish (index into data-finishes). "oh-finish" tells the gallery to show that finish's image.
        pickFinish: function (e) { this.setFinish(parseInt(e.currentTarget.dataset.finish, 10)); },
        setFinish: function (i) {
          if (this.finishes[i]) {
            this.finishIdx = i;
            this.announce();
            window.dispatchEvent(new CustomEvent('oh-finish', { detail: { index: i } }));
          }
        },
        // A gallery thumbnail was clicked ("oh-pick"): thumbnail n is finish n
        onPick: function (e) { var i = (e.detail || {}).index; if (i !== this.finishIdx) { this.setFinish(i); } },
        get finishLabel() { return (this.finishes[this.finishIdx] || {}).label || ''; },
        get finishValue() { return (this.finishes[this.finishIdx] || {}).id || ''; },
        get skuLabel() { return this.sizeDetail.sku || ''; },
        map: function (on, off) {
          var c = this.finishIdx, o = {};
          this.finishes.forEach(function (_, i) { o['f' + i] = i === c ? on : off; });
          return o;
        },
        get finishCls() { return this.map('border-brand-600 ring-2 ring-brand-600', 'border-slate-300 hover:border-slate-400'); },
        get finishOn() { return this.map('true', 'false'); },
        get sizeLabel() { return (this.sizes[this.sizeIdx] || {}).label || ''; },
        get sizeValue() { return (this.sizes[this.sizeIdx] || {}).id || ''; },
        get hasOffer() { return this.price < this.regular; },
        get originalLabel() { return money.format(this.regular); },
        get discountLabel() { return this.hasOffer ? Math.round((1 - this.price / this.regular) * 100) + '% off' : ''; },
        get priceLabel() { return money.format(this.price); },
        get total() { return this.price * this.qty; },
        get totalLabel() { return money.format(this.total); },
        get installment() { return money.format(this.total / 4); },
        get setOf4Savings() {
          var reg4 = this.regular * 4, promo4 = 131.25 * 4;
          return reg4 > promo4 ? money.format(reg4 - promo4) : '$631.00';
        },
        get currentSize() { return this.sizes[this.sizeIdx] || {}; },
        get currentLiSp() { var s = this.currentSize; return (s.li || '') + (s.sp || ''); },
        get currentSpeedText() { var s = this.currentSize; return s.kmh ? s.kmh + ' km/h' : ''; },
        get currentLoadText() { var s = this.currentSize; return s.kg ? s.kg + ' kg' : ''; },
        get qtyLabel() { return this.qty + ' ' + this.noun + (this.qty === 1 ? '' : 's'); },
        get ctaLabel() { return this.ordering ? 'Order ' + this.qtyLabel : 'Add ' + this.noun + 's to cart'; },
        get barCtaLabel() { return this.ordering ? 'Order ' + this.noun + 's' : 'Add ' + this.noun + 's to cart'; },
        // Store stock. data-stores on the ohBuy section is JSON: [{ "name": "Belmont", "qty": 6, "date": null }, { "name": "Cessnock", "qty": null, "date": "2026-10-28" }].
        // qty = source quantity (number or null), date = ISO "available from" date when the store has none. The first store is the selected one.
        // Everything reacts to the chosen quantity: a store with fewer than that shows "{n} in stock" in amber.
        get ordering() { return !this.stores.some(function (s) { return (s.qty || 0) > 0; }); },
        get firstStore() {
          var q = this.qty;
          return this.stores.filter(function (s) { return (s.qty || 0) >= q; })[0] || null;
        },
        // Earliest "available from" date among stores that cannot supply the chosen quantity (ISO strings sort correctly)
        get earliestDate() {
          var q = this.qty, ds = this.stores.filter(function (s) { return (s.qty || 0) < q && s.date; }).map(function (s) { return s.date; }).sort();
          return ds[0] || '';
        },
        get hasStock() { return !!this.firstStore; },
        get storeLead() { return this.firstStore ? 'In stock at ' : (this.earliestDate ? 'Available from ' : 'Out of stock at all stores'); },
        get storeBold() { return this.firstStore ? this.firstStore.name : (this.earliestDate ? fmtDate(this.earliestDate) : ''); },
        get storeBoxCls() { return this.hasStock ? 'border-emerald-200 bg-emerald-50/60' : 'border-slate-200 bg-slate-50'; },
        get storeDotCls() { return this.hasStock ? 'bg-emerald-500' : 'bg-slate-400'; },
        get rows() {
          var q = this.qty;
          return this.stores.map(function (s, i) {
            var have = s.qty || 0, r = { name: s.name, i: i, date: s.date || '~', address: s.address || '', map: s.map || '#', directionsFor: ' to ' + s.name };
            if (have >= q) {
              r.tier = 0;
              r.state = 'today';
              r.rowCls = 'store-row is-today';
              r.statusText = 'In stock today';
            } else if (have > 0) {
              r.tier = 1;
              r.state = 'today';
              r.rowCls = 'store-row is-today';
              r.statusText = have + ' in stock';
            } else if (s.date && s.date !== '~') {
              r.tier = 2;
              r.state = 'soon';
              r.rowCls = 'store-row is-soon';
              r.statusText = 'Available on ' + (typeof fmtLongDate === 'function' ? fmtLongDate(s.date) : fmtDate(s.date));
            } else {
              r.tier = 3;
              r.state = 'out';
              r.rowCls = 'store-row is-out';
              r.statusText = 'Out of stock';
            }
            return r;
          }).sort(function (a, b) { return a.tier - b.tier || (a.date < b.date ? -1 : a.date > b.date ? 1 : 0) || a.i - b.i; });
        },
        // Price match button: the ohPriceMatch dialog lives outside the add to cart form and listens for this window event
        openPriceMatch: function () { window.dispatchEvent(new CustomEvent('oh-pricematch')); },
        openPayLater: function (tab) { window.dispatchEvent(new CustomEvent('oh-paylater', { detail: { tab: tab || 'afterpay' } })); },
        openStores: function () { var d = this.$refs.stores; if (d && !d.open) { d.showModal(); document.body.classList.add('overflow-hidden'); } },
        closeStores: function () { var d = this.$refs.stores; if (d && d.open) { d.close(); } },
        onStoresClose: function () { document.body.classList.remove('overflow-hidden'); }
      };
    });

    // Gallery: thumbnails swap the main image (data-index, data-src, data-alt on each thumbnail button)
    Alpine.data('ohGallery', function () {
      return {
        current: 0, items: [],
        init: function () {
          var self = this;
          this.$el.querySelectorAll('[data-src]').forEach(function (b) { self.items.push({ src: b.dataset.src, alt: b.dataset.alt || '' }); });
        },
        get mainSrc() { return (this.items[this.current] || this.items[0] || {}).src; },
        get mainAlt() { return (this.items[this.current] || this.items[0] || {}).alt; },
        map: function (on, off) {
          var c = this.current, o = {};
          this.items.forEach(function (_, i) { o['t' + i] = i === c ? on : off; });
          return o;
        },
        get thumbCls() { return this.map('ring-2 ring-brand-600', ''); },
        get thumbOn() { return this.map('true', null); },
        pick: function (e) {
          this.current = parseInt(e.currentTarget.dataset.index, 10) || 0;
          // Wheel page: a thumbnail is a finish, so ohBuy listens for "oh-pick" to select it. Harmless where nothing listens.
          window.dispatchEvent(new CustomEvent('oh-pick', { detail: { index: this.current } }));
        },
        // Finish chosen in the buy box ("oh-finish"): show that image
        onFinish: function (e) { var i = (e.detail || {}).index; if (i >= 0 && i < this.items.length) { this.current = i; } }
      };
    });

    // Short description: clamped to two lines; "Read more" only appears when the text is longer than that
    Alpine.data('ohReadMore', function () {
      return {
        expanded: false, canToggle: false,
        init: function () {
          var self = this;
          this.$nextTick(function () {
            var t = self.$refs.text;
            self.canToggle = !!t && t.scrollHeight > t.clientHeight + 2;
          });
        },
        get textCls() { return this.expanded ? '' : 'line-clamp-2'; },
        // Collapsed: the button sits at the end of line 2 (absolute, white background with a fade on its left). Expanded: inline after the text.
        get toggleCls() { return this.expanded ? 'mt-1 text-base leading-relaxed' : 'absolute bottom-0 right-0 bg-gradient-to-r from-transparent via-white via-30% to-white pl-8 text-base leading-relaxed'; },
        get toggleLabel() { return this.expanded ? 'Show less' : 'Read more'; },
        toggle: function () { this.expanded = !this.expanded; }
      };
    });

    // Tabs: About, Specifications, FAQs, Will it fit? All panels stay in the HTML (SEO), x-show only toggles them.
    // Buttons carry data-tab; panel ids are the deep-link hashes (#about, #specs, #faqs, #fit; older hashes map to them).
    // Hover opens a tab on desktop only (fine pointer, lg and up) after a short intent delay; click, tap, Enter and Space always open.
    Alpine.data('ohTabs', function () {
      var KEYS = ['about', 'specs', 'faqs', 'fit'];
      var ALIAS = { specifications: 'specs', faq: 'faqs', fitment: 'fit' };
      var ON = 'border-brand-600 font-semibold text-navy-900', OFF = 'border-transparent font-semibold text-slate-600 hover:text-navy-900';
      return {
        active: 'about', ready: false, timer: 0,
        init: function () {
          var self = this;
          this.ready = true;
          this.fromHash(false);
          window.addEventListener('hashchange', function () { self.fromHash(true); });
        },
        map: function (on, off) {
          var a = this.active, o = {};
          KEYS.forEach(function (k) { o[k] = k === a ? on : off; });
          return o;
        },
        get on() { return this.map(true, false); },
        get sel() { return this.map('true', 'false'); },
        get idx() { return this.map('0', '-1'); },
        get cls() { return this.map(ON, OFF); },
        // Opens the tab for the URL hash (or for the panel that contains the hash target) and scrolls to the tab section
        fromHash: function (scroll) {
          var id = decodeURIComponent(window.location.hash.slice(1)), key = ALIAS[id] || id, el, panel, self = this;
          if (!id) { return; }
          if (KEYS.indexOf(key) < 0) {
            el = document.getElementById(id);
            panel = el && el.closest ? el.closest('[role="tabpanel"]') : null;
            key = panel ? panel.id : '';
          }
          if (KEYS.indexOf(key) < 0) { return; }
          this.active = key;
          this.$nextTick(function () {
            var target = (el && el !== document.getElementById(key)) ? el : self.$el;
            target.scrollIntoView();
          });
        },
        pick: function (e) {
          this.active = e.currentTarget.dataset.tab;
        },
        hover: function () {},
        leave: function () {},
        step: function (e, by) {
          var tabs = e.currentTarget.parentElement.querySelectorAll('[role="tab"]'), i = KEYS.indexOf(e.currentTarget.dataset.tab), n = tabs[(i + by + KEYS.length) % KEYS.length];
          this.active = n.dataset.tab;
          n.focus();
        },
        prev: function (e) { this.step(e, -1); },
        next: function (e) { this.step(e, 1); }
      };
    });

    // Price match request: native dialog opened by ohBuy's openPriceMatch (window event "oh-pricematch"); posts with fetch, shows the result inline.
    // Real endpoint: reuse the live site's price match backend (DEV-NOTES round 19). Without JS the form posts natively to the same action.
    Alpine.data('ohPriceMatch', function () {
      return {
        status: '', busy: false, size: '', sku: '',
        // Default size comes from the hidden input's value attribute (A: the product size; B: the default size, then follows oh-size)
        init: function () {
          var i = this.$el.querySelector('input[name="size"]'), k = this.$el.querySelector('input[name="sku"]');
          this.size = i ? (i.getAttribute('value') || '') : '';
          this.sku = k ? (k.getAttribute('value') || '') : '';
        },
        get formVisible() { return this.status !== 'ok'; },
        get submitLabel() { return this.busy ? 'Sending' : 'Send price match request'; },
        // Tyres: detail.label. Wheels: detail.pm (size and finish) and detail.sku, which follow the finish too.
        onSize: function (e) { var d = e.detail || {}; this.size = d.pm || d.label || ''; if (d.sku) { this.sku = d.sku; } },
        open: function () { var d = this.$refs.dlg; if (d && !d.open) { this.status = ''; d.showModal(); document.body.classList.add('overflow-hidden'); } },
        close: function () { var d = this.$refs.dlg; if (d && d.open) { d.close(); } },
        onClose: function () { document.body.classList.remove('overflow-hidden'); },
        submit: function (e) {
          var self = this, form = e.currentTarget;
          e.preventDefault();
          if (this.busy) { return; }
          this.busy = true;
          this.status = '';
          fetch(form.action, { method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(function (res) {
              if (!res.ok) { throw new Error('status ' + res.status); }
              self.status = 'ok';
              form.reset();
            })
            .catch(function () { self.status = 'error'; })
            .then(function () { self.busy = false; });
        }
      };
    });

    // Pay later dialog: native dialog with tabs for Afterpay, Zip and humm
    Alpine.data('ohPayLater', function () {
      return {
        tab: 'afterpay',
        open: function (t) {
          if (t && typeof t === 'string') { this.tab = t; }
          var d = this.$refs.dlg;
          if (d && !d.open) {
            d.showModal();
            document.body.classList.add('overflow-hidden');
          }
        },
        close: function () {
          var d = this.$refs.dlg || (this.$el ? this.$el.querySelector('dialog') : null);
          if (d && d.open) { d.close(); }
          document.body.classList.remove('overflow-hidden');
        },
        onClose: function () {
          document.body.classList.remove('overflow-hidden');
        },
        setTab: function (t) {
          this.tab = t;
        }
      };
    });

    // Wheel page: spec tables and the "How to read your wheel size" capsule follow the selected size and finish.
    // The tabs sit outside the buy box section, so this reads the default from data-sizes / data-finishes on the buy box and
    // listens for ohBuy's "oh-size" window event. Sizes carry d (diameter, inches), w (width, inches), pcd ("6x139.7"), off (offset, mm), sku.
    Alpine.data('ohWheelSpec', function () {
      function signed(n) { return (n < 0 ? '-' : '+') + Math.abs(n); }
      return {
        d: {},
        init: function () {
          var box = document.querySelector('[data-sizes]'), sizes = [], finishes = [], f, s, i;
          if (!box) { return; }
          try { sizes = JSON.parse(box.dataset.sizes || '[]'); finishes = JSON.parse(box.dataset.finishes || '[]'); } catch (e) { return; }
          for (i = 0; i < sizes.length; i++) { if (sizes[i].default) { s = sizes[i]; } }
          for (i = 0; i < finishes.length; i++) { if (finishes[i].default) { f = finishes[i]; } }
          s = s || sizes[0] || {};
          f = f || finishes[0];
          this.d = f ? Object.assign({}, s, { finish: f.label, sku: (s.sku || '') + (f.sfx || '') }) : s;
        },
        onSize: function (e) { this.d = e.detail || {}; },
        get sizeLabel() { return this.d.label || ''; },
        get finishLabel() { return this.d.finish || ''; },
        get skuLabel() { return this.d.sku || ''; },
        get diameter() { return this.d.d || ''; },
        get width() { return this.d.w || ''; },
        get diameterLabel() { return this.diameter + ' inches'; },
        get widthLabel() { return this.width + ' inches'; },
        get pcd() { return this.d.pcd || ''; },
        get studs() { return (this.pcd.split('x')[0]) || ''; },
        get circle() { return (this.pcd.split('x')[1]) || ''; },
        get offset() { return signed(this.d.off || 0); },
        get offsetLabel() { return this.offset + ' mm'; }
      };
    });

    // Review form: posts with fetch, shows the result inline. Without JS the native form post still works.
    Alpine.data('ohReview', function () {
      return {
        status: '', busy: false,
        get formVisible() { return this.status !== 'ok'; },
        get message() {
          if (this.status === 'ok') { return 'Thanks. Your review is with our team and appears here once approved.'; }
          if (this.status === 'error') { return 'Sorry, your review did not send. Check your connection and try again. Your answers are still here.'; }
          return '';
        },
        get msgCls() {
          if (this.status === 'ok') { return 'mb-3 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-800'; }
          if (this.status === 'error') { return 'mb-3 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-800'; }
          return '';
        },
        get submitLabel() { return this.busy ? 'Sending' : 'Submit review'; },
        submit: function (e) {
          var self = this, form = e.currentTarget;
          e.preventDefault();
          if (this.busy) { return; }
          this.busy = true;
          this.status = '';
          fetch(form.action, { method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(function (res) {
              if (!res.ok) { throw new Error('status ' + res.status); }
              self.status = 'ok';
              form.reset();
            })
            .catch(function () { self.status = 'error'; })
            .then(function () { self.busy = false; });
        }
      };
    });
  }

  function registerReviews() {
    // Review list: all reviews stay in the HTML (SEO). Each li has data-review, data-date (ISO) and data-rating.
    // Footer select "Show" (5, 10, 20, 50; default 5) sets how many are visible. Sort changes the rank of each review; rank drives CSS order and visibility.
    // Live site: reviews come from Magento. For more than 50 reviews load pages server-side instead and keep the first page in the HTML.
    Alpine.data('ohReviews', function () {
      var INITIAL = 3;
      var STEP = 3;
      var CMP = {
        recent: function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : a.i - b.i; },
        high: function (a, b) { return b.rating - a.rating || CMP.recent(a, b); },
        low: function (a, b) { return a.rating - b.rating || CMP.recent(a, b); }
      };
      return {
        items: [], shown: INITIAL, mode: 'recent',
        init: function () {
          var self = this;
          this.$el.querySelectorAll('[data-review]').forEach(function (li, i) {
            self.items.push({ i: i, date: li.dataset.date || '', rating: parseInt(li.dataset.rating, 10) || 0 });
          });
        },
        get total() { return this.items.length; },
        get hasMore() { return this.shown < this.total; },
        loadMore: function () {
          this.shown = Math.min(this.shown + STEP, this.total);
        },
        // rank per review index: { r0: 2, r1: 0, ... }
        get ranks() {
          var o = {};
          this.items.slice().sort(CMP[this.mode] || CMP.recent).forEach(function (it, k) { o['r' + it.i] = k; });
          return o;
        },
        get vis() {
          var n = this.shown, r = this.ranks, o = {};
          Object.keys(r).forEach(function (k) { o[k] = r[k] < n; });
          return o;
        },
        get ord() {
          var r = this.ranks, o = {};
          Object.keys(r).forEach(function (k) { o[k] = { order: r[k] }; });
          return o;
        },
        get countLabel() { return this.total + (this.total === 1 ? ' review' : ' reviews'); },
        sort: function (e) { this.mode = e.currentTarget.value; },
        setShown: function (e) { this.shown = parseInt(e.currentTarget.value, 10) || INITIAL; }
      };
    });

    // Promo card carousel (preview-promo-carousel.html). The track scrolls natively (scroll-snap, touch swipe works without JS);
    // buttons move one card, auto-advance runs every 5 s and loops. Paused on hover, focus and touch, and while the tab is hidden.
    // Not started with prefers-reduced-motion.
    Alpine.data('ohCarousel', function () {
      return {
        paused: false, timer: null, reduced: false,
        init: function () {
          var self = this;
          this.reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
          if (this.reduced) { return; }
          this.timer = window.setInterval(function () { if (!self.paused && !document.hidden) { self.next(); } }, 5000);
        },
        destroy: function () { if (this.timer) { window.clearInterval(this.timer); } },
        get step() {
          var t = this.$refs.track, c = t.firstElementChild;
          return c ? c.getBoundingClientRect().width + (parseFloat(window.getComputedStyle(t).columnGap) || 0) : t.clientWidth;
        },
        get behavior() { return this.reduced ? 'auto' : 'smooth'; },
        pause: function () { this.paused = true; },
        resume: function () { this.paused = false; },
        next: function () {
          var t = this.$refs.track;
          if (t.scrollLeft + t.clientWidth >= t.scrollWidth - 4) { t.scrollTo({ left: 0, behavior: this.behavior }); }
          else { t.scrollBy({ left: this.step, behavior: this.behavior }); }
        },
        prev: function () {
          var t = this.$refs.track;
          if (t.scrollLeft <= 4) { t.scrollTo({ left: t.scrollWidth, behavior: this.behavior }); }
          else { t.scrollBy({ left: -this.step, behavior: this.behavior }); }
        }
      };
    });
  }

  function registerAll() { register(); registerReviews(); }
  if (window.Alpine) { registerAll(); } else { document.addEventListener('alpine:init', registerAll); }
})();
