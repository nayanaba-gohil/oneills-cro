"""Builds the promotions bar banners from the client artwork in src/. Run from the homepage folder:
    python3 tools/promo_images.py

The bar uses ONE ratio and the artwork is shown whole, so the bar's height always equals the image's height
and no filler band can appear at any width. Supply every banner at the same ratio as BAR_W:BAR_H below.
Current artwork is 2172 x 724 (3:1); it is resized to 1920 and 960 wide for delivery (the bar caps at 1920).

To swap an offer: drop the artwork in src/, update JOBS, run this, then tools/build.py.
"""
import pathlib
from PIL import Image

P = pathlib.Path(__file__).resolve().parent.parent
OUT = P / 'assets' / 'promos'
BAR_W, BAR_H = 1920, 640          # 3:1 — must match aspect-[1920/640] in src/header.html (768px and up)
PHONE_W, PHONE_H = 1080, 720      # 1.5:1 — must match aspect-[1080/720] in src/header.html (below 768px)

# A 3:1 strip is short on a narrow screen: at 390px wide it is only 130px tall, about 15% of a phone screen,
# against 53% on a 1440x900 desktop. The phone version is a squarer crop of the left of the artwork (the message
# block), which roughly doubles that to 31%. It drops the product photo; for a mobile banner that keeps the
# product too, supply purpose-made artwork at 1080 x 720 (or taller) with the elements stacked.

# (source file in src/, output name)
# (source file in src/, output name, optional dedicated phone artwork in src/)
JOBS = [
    ('Toyo Tires Buy Three, Get One Free.png', 'toyo-buy3-get1', None),
    ('Yokohama Buy Three, Get One Free (1).png', 'yokohama-buy3-get1', None),
]

OUT.mkdir(parents=True, exist_ok=True)
for src, name, phone_src in JOBS:
    im = Image.open(P / 'src' / src).convert('RGB')
    got = im.width / im.height
    want = BAR_W / BAR_H
    if abs(got - want) > 0.01:
        print(f'  WARNING {src}: ratio {got:.3f} but the bar is {want:.3f}. '
              f'It will be cropped. Re-export at {BAR_W} x {BAR_H} or a multiple.')
    for w in (BAR_W, BAR_W // 2):
        out = im.resize((w, round(w * BAR_H / BAR_W)), Image.LANCZOS)
        f = OUT / f'{name}-{w}.webp'
        out.save(f, 'WEBP', quality=84, method=6)
        print(f'{f.name}: {out.width}x{out.height}, {f.stat().st_size // 1024} KB')

    # phone version: dedicated artwork if supplied, otherwise crop the message block from the left of the banner
    if phone_src:
        ph = Image.open(P / 'src' / phone_src).convert('RGB')
    else:
        ph = im.crop((0, 0, min(round(im.height * PHONE_W / PHONE_H), im.width), im.height))
    ph = ph.resize((PHONE_W, PHONE_H), Image.LANCZOS)
    f = OUT / f'{name}-phone.webp'
    ph.save(f, 'WEBP', quality=84, method=6)
    print(f'{f.name}: {ph.width}x{ph.height}, {f.stat().st_size // 1024} KB'
          + ('' if phone_src else '  (cropped from the banner; supply dedicated phone artwork for a better result)'))
