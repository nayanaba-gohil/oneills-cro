/**
 * O'Neills homepage Alpine components.
 * Written for Hyvä's Alpine CSP build: templates only reference properties, getters and
 * argument-free methods, so no inline expressions are needed.
 * In Hyvä, place this inside the homepage .phtml and register it with $hyvaCsp->registerInlineScript().
 */
(function () {
  'use strict';

  // Store data used by JS (store finder status and nearest store).
  // Hours are minutes from midnight, Australia/Sydney time. Public holidays are not handled.
  // lat/lng are approximate suburb positions; replace with exact Google Business Profile coordinates.
  var STORES = {
    broadmeadow: { name: 'Broadmeadow',    week: [450, 1020], sat: [480, 720], lat: -32.924, lng: 151.735 },
    beresfield:  { name: 'Beresfield TME', week: [420, 1020], sat: [450, 690], lat: -32.800, lng: 151.656 },
    gateshead:   { name: 'Gateshead',      week: [450, 1020], sat: [480, 690], lat: -32.983, lng: 151.689 },
    warnersBay:  { name: 'Warners Bay',    week: [450, 1020], sat: [480, 690], lat: -32.969, lng: 151.646 },
    belmont:     { name: 'Belmont',        week: [450, 1020], sat: [480, 690], lat: -33.034, lng: 151.660 },
    morisset:    { name: 'Morisset',       week: [450, 1020], sat: [480, 690], lat: -33.108, lng: 151.488 },
    kurriKurri:  { name: 'Kurri Kurri',    week: [450, 1020], sat: [480, 690], lat: -32.819, lng: 151.480 },
    cessnock:    { name: 'Cessnock',       week: [450, 1020], sat: [480, 690], lat: -32.834, lng: 151.356 }
  };
  var STORE_KEYS = Object.keys(STORES);

  // Endpoints and params used by the live site's finder forms. Keep in sync with them.
  var CONFIG = {
    vehicleApi: '/tyres/api/vehicle',        // ?type=makes|years|models|series&make=&year=&model=
    tyreVehicleResult: '/tyres/result',      // confirm param names against the live vehicleFinder()
    wheelVehicleResult: '/wheels/result',    // TODO dev: confirm or build a wheels-by-vehicle result route
    searchResult: '/catalogsearch/result/'   // tyre size: width, profile, rim_diameter. Wheels: q=wheels, diameter, wheel_width, pcd, stud_pattern, offset
  };

  function opts(list) { return list.map(function (v) { return { val: v, label: v }; }); }

  // Static fallbacks. On the live site, tyre sizes come from data-combinations (attribute option IDs + labels).
  var TYRE_WIDTHS = opts(['155', '165', '175', '185', '195', '205', '215', '225', '235', '245', '255', '265', '275', '285', '295', '305', '315', '325', '31', '33', '35', '37']);
  var TYRE_PROFILES = opts(['30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '9.5', '10.5', '11.5', '12.5', '13.5']);
  var TYRE_RIMS = opts(['13', '14', '15', '16', '17', '18', '19', '20', '21', '22']);

  // Wheel options mirror the live wheel form (junk PCD values without an "x" removed).
  var DIAMETERS = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'].map(function (v) { return { val: v + '"', label: v + '"' }; });
  var WHEEL_WIDTHS = opts(['5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '12']);
  var PCDS = opts(['4x100', '4x114.3', '5x100', '5x108', '5x112', '5x114.3', '5x120', '5x139.7', '5x150', '6x114.3', '6x130', '6x135', '6x139.7']);
  var OFFSETS = opts(['-44', '-25', '-20', '-12', '-10', '0', '+10', '+12', '+15', '+20', '+25', '+30', '+35', '+38', '+40', '+45']);

  function uniqueBy(rows, valKey, labelKey) {
    var seen = {}, out = [];
    rows.forEach(function (r) {
      if (!seen[r[valKey]]) { seen[r[valKey]] = true; out.push({ val: r[valKey], label: r[labelKey] }); }
    });
    return out.sort(function (a, b) { return parseFloat(a.label) - parseFloat(b.label); });
  }

  function labelOf(list, val) {
    for (var i = 0; i < list.length; i++) { if (String(list[i].val) === String(val)) return list[i].label; }
    return val;
  }

  function sydneyNow() {
    var parts = new Intl.DateTimeFormat('en-AU', {
      timeZone: 'Australia/Sydney', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date());
    var out = {};
    parts.forEach(function (p) { out[p.type] = p.value; });
    return { day: out.weekday, minutes: parseInt(out.hour, 10) * 60 + parseInt(out.minute, 10) };
  }

  function fmt(mins) {
    var h = Math.floor(mins / 60), m = mins % 60, suffix = h >= 12 ? 'pm' : 'am';
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + (m ? ':' + String(m).padStart(2, '0') : '') + suffix;
  }

  function register() {
    // Header drawer
    Alpine.data('ohHeader', function () {
      return {
        drawerOpen: false,
        toggleDrawer: function () { this.drawerOpen = !this.drawerOpen; },
        closeDrawer: function () { this.drawerOpen = false; },
        openCall: function () { this.drawerOpen = false; this.$dispatch('oh-open-call'); }
      };
    });

    // Promotions bar under the navigation: slides marked data-promo rotate every data-interval ms (default 5000).
    // Pauses while hovered or focused, with the pause button, and when the tab is hidden; reduced motion starts paused.
    Alpine.data('ohPromo', function () {
      var timer = null;
      return {
        index: 0, count: 0, playing: true, held: false, ms: 5000,
        init: function () {
          this.count = this.$el.querySelectorAll('[data-promo]').length;
          this.ms = parseInt(this.$el.dataset.interval, 10) || 5000;
          if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { this.playing = false; }
          this.restart();
        },
        restart: function () {
          var self = this;
          if (timer) { clearInterval(timer); }
          timer = setInterval(function () {
            if (self.playing && !self.held && self.count > 1 && document.visibilityState === 'visible') {
              self.index = (self.index + 1) % self.count;
            }
          }, this.ms);
        },
        map: function (on, off) {
          var c = this.index, o = {};
          for (var i = 0; i < this.count; i++) { o['s' + i] = i === c ? on : off; }
          return o;
        },
        get shown() { return this.map(true, false); },
        get current() { return this.map('true', null); },
        get dotCls() { return this.map('bg-navy-900', 'bg-slate-400'); },
        get paused() { return !this.playing; },
        get toggleLabel() { return this.playing ? 'Pause offers' : 'Play offers'; },
        go: function (e) { this.index = parseInt(e.currentTarget.dataset.slide, 10) || 0; this.restart(); },
        toggle: function () { this.playing = !this.playing; this.restart(); },
        hold: function () { this.held = true; },
        release: function () { this.held = false; }
      };
    });

    // Hero finder: Buy Tyres / Buy Wheels, each by size or by vehicle
    Alpine.data('ohFinder', function () {
      return {
        product: 'tyres', by: 'size',
        combos: [],
        width: '', profile: '', rim: '', staggered: false, rearWidth: '', rearProfile: '', rearRim: '',
        diameters: DIAMETERS, wheelWidths: WHEEL_WIDTHS, pcds: PCDS, offsets: OFFSETS,
        diameter: '', wheelWidth: '', pcd: '', offset: '',
        makes: [], years: [], models: [], seriesList: [],
        make: '', year: '', model: '', series: '',
        loading: false,

        init: function () {
          var raw = this.$el.dataset.combinations;
          if (raw) { try { this.combos = JSON.parse(raw) || []; } catch (e) { this.combos = []; } }
        },

        // Tabs and toggles
        get isTyres() { return this.product === 'tyres'; },
        get isWheels() { return this.product === 'wheels'; },
        get isSize() { return this.by === 'size'; },
        get isVehicle() { return this.by === 'vehicle'; },
        get isTyreSize() { return this.isTyres && this.isSize; },
        get isWheelSize() { return this.isWheels && this.isSize; },
        get panelLabel() { return this.isTyres ? 'tab-tyres' : 'tab-wheels'; },
        get tyresTabClass() { return this.isTyres ? 'border-brand-600 text-brand-700' : 'border-transparent text-slate-500 hover:text-navy-900'; },
        get wheelsTabClass() { return this.isWheels ? 'border-brand-600 text-brand-700' : 'border-transparent text-slate-500 hover:text-navy-900'; },
        get sizeBtnClass() { return this.isSize ? 'bg-white text-navy-900 shadow' : 'text-slate-600'; },
        get vehicleBtnClass() { return this.isVehicle ? 'bg-white text-navy-900 shadow' : 'text-slate-600'; },
        get vehicleCta() { return this.isTyres ? 'Find Tyres' : 'Find Wheels'; },
        showTyres: function () { this.product = 'tyres'; },
        showWheels: function () { this.product = 'wheels'; },
        showSize: function () { this.by = 'size'; },
        showVehicle: function () {
          this.by = 'vehicle';
          if (!this.makes.length) { this.load('makes', {}, 'makes'); }
        },

        // Tyre size options: dependent when live combinations are present, static otherwise
        get hasCombos() { return this.combos.length > 0; },
        get widthOptions() { return this.hasCombos ? uniqueBy(this.combos, 'width_val', 'width_label') : TYRE_WIDTHS; },
        profilesFor: function (w) {
          if (!this.hasCombos) return TYRE_PROFILES;
          return uniqueBy(this.combos.filter(function (c) { return String(c.width_val) === String(w); }), 'profile_val', 'profile_label');
        },
        rimsFor: function (w, p) {
          if (!this.hasCombos) return TYRE_RIMS;
          return uniqueBy(this.combos.filter(function (c) { return String(c.width_val) === String(w) && String(c.profile_val) === String(p); }), 'rim_val', 'rim_label');
        },
        get profileOptions() { return this.width ? this.profilesFor(this.width) : []; },
        get rimOptions() { return this.profile ? this.rimsFor(this.width, this.profile) : []; },
        get rearProfileOptions() { return this.rearWidth ? this.profilesFor(this.rearWidth) : []; },
        get rearRimOptions() { return this.rearProfile ? this.rimsFor(this.rearWidth, this.rearProfile) : []; },
        get noWidth() { return !this.width; },
        get noProfile() { return !this.profile; },
        get noRearWidth() { return !this.rearWidth; },
        get noRearProfile() { return !this.rearProfile; },
        onWidth: function () { this.profile = ''; this.rim = ''; },
        onProfile: function () { this.rim = ''; },
        onRearWidth: function () { this.rearProfile = ''; this.rearRim = ''; },
        onRearProfile: function () { this.rearRim = ''; },
        get cannotSearchTyreSize() {
          if (!this.width || !this.profile || !this.rim) return true;
          return this.staggered && (!this.rearWidth || !this.rearProfile || !this.rearRim);
        },
        searchTyreSize: function () {
          if (this.cannotSearchTyreSize) return;
          var w = labelOf(this.widthOptions, this.width), p = labelOf(this.profileOptions, this.profile), r = labelOf(this.rimOptions, this.rim);
          var params = new URLSearchParams({ q: w + '/' + p + 'R' + r, width: this.width, profile: this.profile, rim_diameter: this.rim });
          if (this.staggered) {
            params.set('staggered', '1');
            params.set('rear_width', this.rearWidth);
            params.set('rear_profile', this.rearProfile);
            params.set('rear_rim_diameter', this.rearRim);
          }
          window.location.href = CONFIG.searchResult + '?' + params.toString();
        },

        // Wheel size
        get cannotSearchWheelSize() { return !this.diameter || !this.pcd; },
        searchWheelSize: function () {
          if (this.cannotSearchWheelSize) return;
          var params = new URLSearchParams({ q: 'wheels', diameter: this.diameter, pcd: this.pcd, stud_pattern: this.pcd.split('x')[0] + ' Stud' });
          if (this.wheelWidth) { params.set('wheel_width', this.wheelWidth); }
          if (this.offset) { params.set('offset', this.offset); }
          window.location.href = CONFIG.searchResult + '?' + params.toString();
        },

        // Vehicle (shared by tyres and wheels)
        get noMake() { return !this.make; },
        get noYear() { return !this.year; },
        get noModel() { return !this.model; },
        get cannotSearchVehicle() { return !this.make || !this.year || !this.model; },
        load: function (type, params, target) {
          var self = this;
          var query = new URLSearchParams(Object.assign({ type: type }, params));
          self.loading = true;
          return fetch(CONFIG.vehicleApi + '?' + query.toString(), { headers: { Accept: 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (json) {
              if (!json.success) { throw new Error(json.message || 'failed'); }
              self[target] = json.data || [];
            })
            .catch(function () { self[target] = []; })
            .finally(function () { self.loading = false; });
        },
        onMake: function () {
          this.year = ''; this.model = ''; this.series = ''; this.years = []; this.models = []; this.seriesList = [];
          if (this.make) { this.load('years', { make: this.make }, 'years'); }
        },
        onYear: function () {
          this.model = ''; this.series = ''; this.models = []; this.seriesList = [];
          if (this.year) { this.load('models', { make: this.make, year: this.year }, 'models'); }
        },
        onModel: function () {
          this.series = ''; this.seriesList = [];
          if (this.model) { this.load('series', { make: this.make, year: this.year, model: this.model }, 'seriesList'); }
        },
        // Vehicle hint fallback: opens the "Call your nearest store" sheet (footer.html, below lg)
        openCall: function () { this.$dispatch('oh-open-call'); },
        searchVehicle: function () {
          if (this.cannotSearchVehicle) return;
          var params = new URLSearchParams({ make: this.make, year: this.year, model: this.model });
          if (this.series) { params.set('series', this.series); }
          var base = this.isTyres ? CONFIG.tyreVehicleResult : CONFIG.wheelVehicleResult;
          window.location.href = base + '?' + params.toString();
        }
      };
    });

    // Store finder: one panel at a time, open/closed status, nearest store
    Alpine.data('ohStores', function () {
      function map(fn) { var o = {}; STORE_KEYS.forEach(function (k) { o[k] = fn(k); }); return o; }
      function openNow(k) {
        var s = STORES[k], now = sydneyNow();
        var hours = now.day === 'Sun' ? null : (now.day === 'Sat' ? s.sat : s.week);
        return hours && now.minutes >= hours[0] && now.minutes < hours[1] ? hours : null;
      }
      function km(lat1, lng1, lat2, lng2) {
        var r = Math.PI / 180, dLat = (lat2 - lat1) * r, dLng = (lng2 - lng1) * r;
        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1 * r) * Math.cos(lat2 * r) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
        return 12742 * Math.asin(Math.sqrt(a));
      }
      return {
        selected: 'broadmeadow', ready: false, tick: 0, locating: false, locMsg: '',
        init: function () {
          var self = this;
          this.ready = true;
          setInterval(function () { self.tick++; }, 60000); // refresh open/closed each minute
        },
        get show() { var c = this.selected; return map(function (k) { return k === c; }); },
        get current() { var c = this.selected; return map(function (k) { return k === c ? 'true' : null; }); },
        get tabCls() {
          var c = this.selected;
          return map(function (k) { return k === c ? 'bg-navy-900 text-white ring-navy-900' : 'bg-white text-navy-900 ring-slate-200 hover:ring-brand-500'; });
        },
        get status() {
          this.tick;
          return map(function (k) { var h = openNow(k); return h ? 'Open until ' + fmt(h[1]) : 'Closed now'; });
        },
        get statusCls() {
          this.tick;
          return map(function (k) { return openNow(k) ? 'bg-emerald-400 text-navy-900' : 'bg-white/15 text-white'; });
        },
        get dotCls() {
          this.tick;
          return map(function (k) { return openNow(k) ? 'bg-emerald-500' : 'bg-slate-300'; });
        },
        get locateLabel() { return this.locating ? 'Finding your location...' : 'Find my nearest store'; },
        get hasLocMsg() { return this.locMsg !== ''; },
        select: function (e) {
          var k = e.currentTarget.dataset.store;
          if (STORES[k]) { this.selected = k; }
        },
        locate: function () {
          var self = this;
          if (!navigator.geolocation) { self.locMsg = 'Your browser cannot share its location. Choose a store from the list.'; return; }
          self.locating = true; self.locMsg = '';
          navigator.geolocation.getCurrentPosition(function (pos) {
            var best = null, bestKm = Infinity;
            STORE_KEYS.forEach(function (k) {
              var d = km(pos.coords.latitude, pos.coords.longitude, STORES[k].lat, STORES[k].lng);
              if (d < bestKm) { bestKm = d; best = k; }
            });
            self.selected = best;
            self.locating = false;
            self.locMsg = 'Your nearest store is ' + STORES[best].name + ', about ' + Math.round(bestKm) + ' km away.';
          }, function () {
            self.locating = false;
            self.locMsg = 'We could not get your location. Choose a store from the list.';
          }, { timeout: 8000, maximumAge: 600000 });
        }
      };
    });

    // How buying tyres online works: the step crossing the middle of the screen drives the pinned tyre print
    // (number, rotation), the active step's border and the convoy's position.
    Alpine.data('ohSteps', function () {
      var KEYS = ['s1', 's2', 's3', 's4'];
      function map(step, on, off) { var o = {}; KEYS.forEach(function (k, i) { o[k] = i + 1 === step ? on : off; }); return o; }
      return {
        step: 1,
        init: function () {
          // On scroll and resize (once per frame), pick the last step whose top has passed the middle of the screen.
          // Works for jumps too (anchor links, reload mid-page), which an IntersectionObserver alone can miss.
          var self = this, items = this.$el.querySelectorAll('[data-step]'), ticking = false;
          function update() {
            var mid = window.innerHeight * 0.5, s = 1;
            items.forEach(function (el, i) { if (el.getBoundingClientRect().top <= mid) { s = i + 1; } });
            self.step = s; ticking = false;
          }
          function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
          window.addEventListener('scroll', onScroll, { passive: true });
          window.addEventListener('resize', onScroll, { passive: true });
          update();
        },
        get num() { return map(this.step, true, false); },
        get stepCls() { return map(this.step, 'lg:border-amber-400', 'lg:border-white/20'); },
        get spinStyle() { return 'transform: rotate(' + (this.step - 1) * 90 + 'deg)'; },
        get driveStyle() { return 'transform: translateX(' + (this.step - 1) * 48 + 'px)'; }
      };
    });

    // Shop tyres by vehicle make: A to Z letter bar, one panel per letter.
    // data-letters lists the letters that have makes; data-default is the letter shown first.
    Alpine.data('ohMakes', function () {
      var LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
      function map(fn) { var o = {}; LETTERS.forEach(function (l) { o[l] = fn(l); }); return o; }
      return {
        letter: '', available: [],
        init: function () {
          this.available = (this.$el.dataset.letters || '').split('');
          this.letter = this.$el.dataset.default || this.available[0] || '';
        },
        get shown() { var c = this.letter; return map(function (l) { return l === c; }); },
        get selected() { var c = this.letter; return map(function (l) { return l === c; }); },
        get tabIndex() { var c = this.letter; return map(function (l) { return l === c ? '0' : '-1'; }); },
        get letterCls() {
          var c = this.letter;
          return map(function (l) { return l === c ? 'bg-slate-100 font-semibold text-navy-900' : 'text-slate-600 hover:bg-slate-50 hover:text-navy-900'; });
        },
        get atStart() { return this.available.indexOf(this.letter) <= 0; },
        get atEnd() { return this.available.indexOf(this.letter) >= this.available.length - 1; },
        pick: function (e) { this.go(e.currentTarget.dataset.letter, false); },
        prev: function () { this.step(-1, false); },
        next: function () { this.step(1, false); },
        prevKey: function () { this.step(-1, true); },
        nextKey: function () { this.step(1, true); },
        step: function (dir, focus) {
          var i = this.available.indexOf(this.letter) + dir;
          if (i >= 0 && i < this.available.length) { this.go(this.available[i], focus); }
        },
        go: function (l, focus) {
          if (this.available.indexOf(l) < 0) return;
          this.letter = l;
          var strip = this.$refs.strip, btn = strip ? strip.querySelector('[data-letter="' + l + '"]') : null;
          if (!btn) return;
          // keep the chosen letter in view on narrow screens, without scrolling the page
          strip.scrollTo({ left: btn.offsetLeft - (strip.clientWidth - btn.offsetWidth) / 2, behavior: 'smooth' });
          if (focus) { btn.focus({ preventScroll: true }); }
        }
      };
    });

    // Google reviews: one capsule per store (data-store, data-name, data-pid, data-count on each), the first selected.
    // Feed: data-json (inline JSON element id) or data-endpoint (URL), same shape either way.
    // data-endpoint returns real Google reviews keyed by store, e.g. {"broadmeadow": [{id, author, authorUrl, photo, rating, text, when}]}.
    // With no endpoint (or no reviews for a store) the cards stay hidden and only the Google links show.
    Alpine.data('ohReviews', function () {
      var REVIEWS = 'https://search.google.com/local/reviews?placeid=';
      var WRITE = 'https://search.google.com/local/writereview?placeid=';
      return {
        stores: {}, keys: [], selectedKey: '', feed: {},
        init: function () {
          var self = this;
          this.$el.querySelectorAll('[data-store]').forEach(function (b) {
            var d = b.dataset;
            self.stores[d.store] = { name: d.name, pid: d.pid, count: parseInt(d.count, 10) || 0 };
            self.keys.push(d.store);
          });
          this.selectedKey = this.keys[0] || '';
          // Reviews either rendered into the page (data-json = id of a <script type="application/json">, e.g. cached
          // server-side from the Places API) or fetched from data-endpoint.
          var inline = this.$el.dataset.json && document.getElementById(this.$el.dataset.json);
          if (inline) { try { this.feed = JSON.parse(inline.textContent) || {}; } catch (e) { this.feed = {}; } return; }
          var url = this.$el.dataset.endpoint;
          if (!url) return;
          fetch(url, { headers: { Accept: 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (json) { self.feed = json || {}; })
            .catch(function () { self.feed = {}; });
        },
        map: function (on, off) {
          var c = this.selectedKey, o = {};
          this.keys.forEach(function (k) { o[k] = k === c ? on : off; });
          return o;
        },
        get selected() { return this.map(true, false); },
        get tabIndex() { return this.map('0', '-1'); },
        get pillCls() { return this.map('border-navy-900 bg-navy-900 text-white', 'border-slate-200 bg-white text-navy-900 hover:border-brand-400'); },
        get store() { return this.stores[this.selectedKey] || { name: '', pid: '', count: 0 }; },
        get readUrl() { return REVIEWS + this.store.pid; },
        get writeUrl() { return WRITE + this.store.pid; },
        get readLabel() { return 'Read all ' + this.store.count.toLocaleString('en-AU') + ' reviews'; },
        get storeSr() { return " for O'Neills " + this.store.name + ' on Google (opens in a new tab)'; },
        get cards() {
          var name = this.store.name;
          return (this.feed[this.selectedKey] || []).slice(0, 3).map(function (r, i) {
            var rating = Math.max(0, Math.min(5, Number(r.rating) || 0));
            return {
              id: r.id || String(i), author: r.author || 'Google user', authorUrl: r.authorUrl || null,
              photo: r.photo || '', hasPhoto: !!r.photo, noPhoto: !r.photo,
              initial: (r.author || 'G').trim().charAt(0).toUpperCase(),
              text: r.text || '', when: r.when ? '· ' + r.when : '', store: name + ' store',
              ratingLabel: rating + ' out of 5 stars', starStyle: 'width:' + (rating / 5 * 100) + '%'
            };
          });
        },
        get hasCards() { return this.cards.length > 0; },
        pick: function (e) { this.go(e.currentTarget.dataset.store, false); },
        prevKey: function () { this.step(-1); },
        nextKey: function () { this.step(1); },
        step: function (dir) {
          var i = this.keys.indexOf(this.selectedKey) + dir;
          if (i >= 0 && i < this.keys.length) { this.go(this.keys[i], true); }
        },
        go: function (key, focus) {
          if (!this.stores[key]) return;
          this.selectedKey = key;
          // looked up by id: inside a click handler $el is the clicked pill, not the section
          var btn = document.querySelector('#reviews [data-store="' + key + '"]'), panel = document.getElementById('rv-panel');
          if (panel && btn) { panel.setAttribute('aria-labelledby', btn.id); }
          if (btn && focus) { btn.focus({ preventScroll: true }); }
          if (btn && btn.scrollIntoView && btn.parentElement.scrollWidth > btn.parentElement.clientWidth) {
            btn.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
          }
        }
      };
    });

    // Mobile sticky bar call sheet
    Alpine.data('ohSticky', function () {
      return {
        sheetOpen: false, barShown: false,
        init: function () {
          var self = this, ticking = false;
          function check() { self.barShown = window.scrollY > window.innerHeight * 0.85; ticking = false; }
          window.addEventListener('scroll', function () { if (!ticking) { ticking = true; window.requestAnimationFrame(check); } }, { passive: true });
          check();
        },
        openSheet: function () { this.sheetOpen = true; },
        closeSheet: function () { this.sheetOpen = false; }
      };
    });
  }

  if (window.Alpine) { register(); } else { document.addEventListener('alpine:init', register); }
})();
