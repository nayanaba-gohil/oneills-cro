"""Generates two decorative SVG symbols for the icon sprite (src/icons.html), between the
<!-- graphics:start --> and <!-- graphics:end --> markers. Run from the homepage folder:
    python3 tools/graphics.py
  g-tread-swirl  tyre tracks spiralling inwards (section 4 step graphic). Uses currentColor.
  g-convoy       one row of side-on line-art vehicles, 730 x 54 (section 4 convoy). Uses currentColor.
"""
import math, pathlib

f = lambda v: f'{v:.1f}'.rstrip('0').rstrip('.')

# ---------- Tyre tracks: two staggered tread bands plus thin edges, fading in from the tail ----------
CX = CY = 100
def spiral(t0, sweep, r0, r1, step=15):
    """Clockwise spiral as arc segments: returns [(path_d, start_fraction)] split in 6 pieces for the fade."""
    pieces, n = [], 6
    for k in range(n):
        a0, a1 = t0 + sweep * k / n, t0 + sweep * (k + 1) / n
        r = lambda a: r0 + (r1 - r0) * (a - t0) / sweep
        pt = lambda a, rr: (CX + rr * math.cos(math.radians(a)), CY + rr * math.sin(math.radians(a)))
        def d(off, a0=a0, a1=a1, r=r, pt=pt):  # bind loop values now, not when called
            x, y = pt(a0, r(a0) + off); out = f'M{f(x)} {f(y)}'
            a = a0
            while a < a1 - 1e-6:
                b = min(a + step, a1); x, y = pt(b, r(b) + off); rr = (r(a) + r(b)) / 2 + off
                out += f'A{f(rr)} {f(rr)} 0 0 1 {f(x)} {f(y)}'; a = b
            return out
        pieces.append((d, (k + 1) / n))
    return pieces

def track(t0, sweep, r0, r1, peak):
    """Tyre print: two staggered tread bands (no edge lines, which read as rails), fine shoulder sipes,
    and a faint offset second pass for a rough, printed edge. Fades in from the tail."""
    out = []
    for d, frac in spiral(t0, sweep, r0, r1):
        op = f(peak * (0.35 + 0.65 * frac))
        out.append(f'<g opacity="{op}">'
                   f'<path d="{d(-3.4)}" stroke-width="6" stroke-dasharray="2.6 1.5"/>'
                   f'<path d="{d(3.4)}" stroke-width="6" stroke-dasharray="2.6 1.5" stroke-dashoffset="2"/>'
                   f'<path d="{d(-7.6)}" stroke-width="1.6" stroke-dasharray=".8 2.6"/>'
                   f'<path d="{d(7.6)}" stroke-width="1.6" stroke-dasharray=".8 2.6" stroke-dashoffset="1.6"/>'
                   f'<path d="{d(.9)}" stroke-width="13" stroke-dasharray="1.2 6.4" stroke-dashoffset="3" opacity=".35"/></g>')
    return ''.join(out)

swirl = ('<symbol id="g-tread-swirl" viewBox="0 0 200 200" fill="none" stroke="currentColor">'
         + track(-100, 520, 93, 66, 1) + track(70, 430, 82, 57, .55) + '</symbol>')

# ---------- Convoy: body outline with wheel arches, windows, wheels. Ground at y=50, wheel centre y=43 ----------
def body(x0, profile, wheels, arch=9, base=42):
    """profile: points from front-bottom round to rear-bottom (local x). Bottom edge is drawn with arches."""
    xs = sorted(wheels); front = profile[0][0]; rear = profile[-1][0]
    d = f'M{f(x0 + rear)} {base}'
    for w in xs:
        d += f'H{f(x0 + w - arch)}A{arch} {arch} 0 0 1 {f(x0 + w + arch)} {base}'
    d += f'H{f(x0 + front)}' + ''.join(f'L{f(x0 + x)} {f(y)}' for x, y in profile[1:]) + 'Z'
    return f'<path d="{d}"/>'
def poly(x0, pts, close=True):
    return f'<path d="M' + 'L'.join(f'{f(x0 + x)} {f(y)}' for x, y in pts) + ('Z' if close else '') + '"/>'
def wheel(x, cy=43, r=7):
    return f'<circle cx="{f(x)}" cy="{cy}" r="{r}"/><circle cx="{f(x)}" cy="{cy}" r="{f(r * .36)}"/>'

V = []
def hatch(x):
    V.append(body(x, [(66, 42), (66, 33), (60, 29), (48, 27), (40, 18), (18, 18), (8, 27), (2, 30), (0, 34), (0, 42)], [14, 52])
             + poly(x, [(12, 26), (19, 21), (28, 21), (28, 26)]) + poly(x, [(31, 26), (31, 21), (39, 21), (44, 26)]) + wheel(x + 14) + wheel(x + 52)); return 66
def prime_mover(x):
    V.append(body(x, [(90, 42), (90, 29), (87, 27), (85, 14), (82, 10), (62, 10), (62, 34), (0, 34), (0, 42)], [14, 30, 76])
             + poly(x, [(66, 14), (81, 14), (83, 24), (66, 24)]) + poly(x, [(59, 34), (59, 9), (57, 2)], close=False)
             + poly(x, [(18, 34), (18, 30), (34, 30), (34, 34)], close=False) + wheel(x + 14) + wheel(x + 30) + wheel(x + 76)); return 90
def wagon(x):
    V.append(body(x, [(72, 42), (72, 30), (69, 27), (58, 26), (53, 12), (6, 12), (2, 14), (0, 18), (0, 42)], [15, 57])
             + poly(x, [(8, 16), (22, 16), (22, 24), (8, 24)]) + poly(x, [(25, 16), (38, 16), (38, 24), (25, 24)])
             + poly(x, [(41, 16), (51, 16), (54, 24), (41, 24)]) + poly(x, [(10, 12), (10, 8), (48, 8), (48, 12)], close=False)
             + wheel(x + 15) + wheel(x + 57)); return 72
def van(x):
    V.append(body(x, [(78, 42), (78, 30), (74, 25), (61, 23), (55, 10), (4, 10), (0, 13), (0, 42)], [15, 62])
             + poly(x, [(52, 13), (55, 13), (59, 22), (52, 22)]) + poly(x, [(40, 12), (40, 40)], close=False) + wheel(x + 15) + wheel(x + 62)); return 78
def ute(x):
    V.append(body(x, [(82, 42), (82, 31), (78, 28), (64, 27), (57, 16), (33, 16), (31, 28), (0, 28), (0, 42)], [16, 64])
             + poly(x, [(36, 19), (46, 19), (46, 26), (35, 26)]) + poly(x, [(49, 19), (55, 19), (60, 26), (49, 26)]) + wheel(x + 16) + wheel(x + 64)); return 82
def box_truck(x):
    V.append(body(x, [(96, 42), (96, 28), (93, 26), (91, 14), (87, 10), (74, 10), (74, 38), (0, 38), (0, 42)], [16, 32, 82])
             + poly(x, [(0, 6), (70, 6), (70, 38), (0, 38)]) + poly(x, [(77, 13), (86, 13), (88, 23), (77, 23)])
             + wheel(x + 16) + wheel(x + 32) + wheel(x + 82)); return 96
def sedan(x):
    V.append(body(x, [(74, 42), (74, 34), (70, 31), (56, 29), (46, 19), (26, 19), (16, 28), (4, 30), (0, 33), (0, 42)], [15, 59])
             + poly(x, [(19, 28), (27, 22), (35, 22), (35, 28)]) + poly(x, [(38, 28), (38, 22), (45, 22), (51, 28)]) + wheel(x + 15) + wheel(x + 59)); return 74
def tractor(x):
    V.append(poly(x, [(29, 36), (43, 36)], close=False) + poly(x, [(28, 24), (54, 24), (58, 28), (58, 37)], close=False)
             + poly(x, [(6, 24), (6, 6), (27, 6), (27, 24)]) + poly(x, [(10, 10), (23, 10), (23, 20), (10, 20)]) + poly(x, [(48, 24), (48, 12)], close=False)
             + wheel(x + 16, cy=37, r=13) + wheel(x + 50)); return 60

x = 4
for draw in (hatch, prime_mover, wagon, van, ute, box_truck, sedan, tractor):
    x += draw(x) + 14
convoy = ('<symbol id="g-convoy" viewBox="0 0 730 54" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
          + ''.join(V) + '<path d="M0 50.5H730"/></symbol>')
assert x - 4 == 730, x  # repeat period: the next copy starts 14 units after the tractor

p = pathlib.Path('src/icons.html'); t = p.read_text()
a = t.index('<!-- graphics:start -->'); b = t.index('<!-- graphics:end -->')
p.write_text(t[:a] + '<!-- graphics:start --> <!-- generated by tools/graphics.py -->\n    ' + swirl + '\n    ' + convoy + '\n    ' + t[b:])
print('graphics written; convoy width', x, '; swirl', len(swirl), 'bytes; convoy', len(convoy), 'bytes')
