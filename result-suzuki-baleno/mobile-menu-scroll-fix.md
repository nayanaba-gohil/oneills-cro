# Mobile menu scrolling fix

Target: the mobile main menu on `oneillstyres.com.au` (the `<dialog>` opened by the hamburger button).

## What is broken now

Reproduced on the live site at 375x812:

1. **The page behind the menu keeps scrolling.** With the menu open, `document.body` stays
   `overflow: visible` and `position: static`. Scrolling or swiping over the open menu moves the
   page underneath it. On close the user is dropped at a different scroll position than where
   they started.
2. **Scroll chaining.** The menu panel (`div.grow.relative.overflow-y-auto`) and the dialog both
   use `overscroll-behavior: auto`. When the menu list hits its end, the gesture continues into
   the page behind instead of stopping.
3. **No backdrop separation.** The dialog is 337px wide with no `::backdrop` dimming, so the
   scrolling page behind it stays fully visible and reads as part of the menu.
4. **Sticky CTAs sit on top of the open menu.** The `CALL NOW` / `BOOK ONLINE` bottom bar and the
   floating call pill stay above the dialog, which is the overlapping-sticky-buttons problem
   called out in the optimisation brief.
5. **Panel height is set from `%`.** On iOS Safari the dynamic URL bar makes `100%` taller than
   the visible area, so the last menu items sit under the browser chrome.

## CSS

```css
/* 1. Lock the page behind the menu. Applied to <body> while the dialog is open. */
.body-scroll-locked {
  position: fixed;
  left: 0;
  right: 0;
  width: 100%;
  overflow: hidden;
}

/* 2. Dialog fills the visible viewport, not the layout viewport. */
.m-menu {
  width: min(88vw, 340px);
  max-width: none;
  height: 100dvh;
  max-height: 100dvh;
  border: 0;
  padding: 0;
  margin: 0;
}

.m-menu::backdrop {
  background: rgba(11, 20, 32, 0.55);
}

/* 3. Head and foot fixed, only the link list scrolls, and it does not chain. */
.m-menu-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.m-menu-head,
.m-menu-foot {
  flex: 0 0 auto;
}

.m-menu-scroll {
  flex: 1 1 auto;
  min-height: 0;            /* without this a flex child refuses to shrink and never scrolls */
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

/* 4. Keep the last row clear of the iOS home indicator. */
.m-menu-foot {
  padding-bottom: calc(14px + env(safe-area-inset-bottom));
}

/* 5. Keep the sticky CTA bar and floating call button under the open menu. */
.oneills-mobile-bottom-bar,
.desktop-floating-call-btn {
  z-index: 30;
}
```

## JavaScript

```js
(function () {
  var dlg = document.getElementById('mobileMenu');
  var openBtn = document.getElementById('menuOpen');
  var closeBtn = document.getElementById('menuClose');
  if (!dlg || !openBtn) return;

  var scrollTop = 0;
  var lockClass = 'body-scroll-locked';

  function lock() {
    scrollTop = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.style.top = '-' + scrollTop + 'px';
    document.body.classList.add(lockClass);
  }

  function unlock() {
    document.body.classList.remove(lockClass);
    document.body.style.top = '';
    // html { scroll-behavior: smooth } would animate the restore and land short.
    var prev = document.documentElement.style.scrollBehavior;
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, scrollTop);
    document.documentElement.style.scrollBehavior = prev;
  }

  function openMenu() {
    if (dlg.open) return;               // a second open would throw and strand the lock
    lock();
    try {
      if (typeof dlg.showModal === 'function') { dlg.showModal(); }
      else { dlg.setAttribute('open', ''); }
    } catch (err) {
      unlock();
    }
  }

  function closeMenu() {
    if (dlg.open) {
      try { dlg.close(); } catch (err) { dlg.removeAttribute('open'); }
    }
    unlock();
  }

  openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  dlg.addEventListener('close', unlock);                              // backstop, idempotent
  dlg.addEventListener('cancel', function () { setTimeout(unlock, 0); }); // Esc
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg) closeMenu();                                // backdrop
  });
  Array.prototype.forEach.call(dlg.querySelectorAll('a'), function (a) {
    a.addEventListener('click', closeMenu);
  });
  window.addEventListener('resize', function () {
    if (dlg.open && window.innerWidth >= 1024) closeMenu();
  });
})();
```

### Why every close path calls `unlock()` directly

`dialog.close()` is specified to fire a `close` event, but it did not fire reliably during
testing. Hanging the unlock on that event alone leaves `<body>` stuck at `position: fixed` with
the page frozen and no way back. Each close path therefore calls `unlock()` itself, and the
`close` listener stays only as a harmless backstop. `unlock()` is idempotent, so running it
twice is safe.

## Verified behaviour

Tested in `vehicles.html` at 375x812, page scrolled to 2500px before opening the menu:

| Path | Dialog | `body` position | Scroll after close |
|---|---|---|---|
| Open | open | `fixed`, `top: -2500px` | page frozen |
| Close button | closed | `static` | 2500, exact |
| Menu link click | closed | `static` | 2500, exact |
| Backdrop click | closed | `static` | 2500, exact |
| Open called twice | open once | `fixed`, `top: -2500px` | no stranded lock |

Panel scrolls internally (`scrollHeight` 1019 vs `clientHeight` 658) with
`overscroll-behavior: contain`, so the gesture stops at the end of the list.
