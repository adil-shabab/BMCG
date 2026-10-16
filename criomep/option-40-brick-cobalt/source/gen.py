"""Generate the Criomep Option 40 'Brick' recolour deck (15 slides) + logo kit."""
import os, re, random, sys

S = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(S, 'orig')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, 'out')
os.makedirs(os.path.join(OUT, 'logo'), exist_ok=True)

# ---------------------------------------------------------------- palette
C = '#2B4EFF'   # Blueprint Cobalt  (primary)
N = '#1A2B8F'   # Conduit Navy      (deep)
Y = '#FFB31F'   # Desert Saffron    (accent)
M = '#0D1530'   # Midnight Steel    (ink)
L = '#F4F1EA'   # Limestone         (tint)
G = '#5B6478'   # Slate             (supporting text)
P = '#8FA2FF'   # Periwinkle        (deep brick on dark)

POS = {'#B23A2E': C, '#8E2C22': N, '#D9774B': Y, '#2B2B2B': M, '#7A6A64': G, '#1E1A19': M}
DARK = {'#B23A2E': C, '#8E2C22': P, '#D9774B': Y, '#1E1A19': M}


def recolour(svg, cmap):
    return re.sub(r'#[0-9A-Fa-f]{6}', lambda m: cmap.get(m.group(0).upper(), m.group(0)), svg)


def mono(svg, col):
    return re.sub(r'fill="[^"]+"', f'fill="{col}"', svg)


def orig(name):
    return open(os.path.join(ORIG, f'criomep-{name}.svg')).read()


def inline(svg, cls='', style=''):
    svg = re.sub(r'\s(width|height)="[^"]*"', '', svg, count=2)
    return svg.replace('<svg ', f'<svg class="{cls}" style="{style}" ', 1)


# ---------------------------------------------------------------- geometry from the master files
BRICKS = []  # (x, y, role)  role: a=primary, b=deep, c=light
for x, y, f in re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="16" height="8" rx="1.6" fill="(#\w+)"',
                          orig('symbol')):
    BRICKS.append((float(x), float(y), {'#B23A2E': 'a', '#8E2C22': 'b', '#D9774B': 'c'}[f]))
paths = re.findall(r'd="([^"]+)"', orig('horizontal-tagline'))
D_CRIO, D_MEP, D_TAG = paths


def sym(a=C, b=N, c=Y, cls='', style='', stroke=None):
    col = {'a': a, 'b': b, 'c': c}
    r = ''
    for x, y, k in BRICKS:
        if stroke:
            r += f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="none" stroke="{stroke}" stroke-width=".5"/>'
        else:
            r += f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{col[k]}"/>'
    return f'<svg class="{cls}" style="{style}" viewBox="0 0 84 96" xmlns="http://www.w3.org/2000/svg">{r}</svg>'


def wm(c1=M, c2=C, cls='', style=''):
    return (f'<svg class="{cls}" style="{style}" viewBox="0 -51 209 53" xmlns="http://www.w3.org/2000/svg">'
            f'<path fill="{c1}" d="{D_CRIO}"/><path fill="{c2}" d="{D_MEP}"/></svg>')


def lockup(dark=False, tag=False, cls='', style='', monocol=None):
    """Horizontal lockup, built from the master geometry."""
    a, b, c = (C, P, Y) if dark else (C, N, Y)
    t1, t2, tg = ('#fff', Y, 'rgba(255,255,255,.7)') if dark else (M, C, G)
    if monocol:
        a = b = c = t1 = t2 = tg = monocol
    rects = ''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{ {"a": a, "b": b, "c": c}[k] }"/>'
                    for x, y, k in BRICKS)
    h = 110 if tag else 96
    t = f'<g transform="translate(126 100.5)"><path fill="{tg}" d="{D_TAG}"/></g>' if tag else ''
    return (f'<svg class="{cls}" style="{style}" viewBox="0 0 {360 if tag else 334} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'{rects}<g transform="translate(126 74.5)"><path fill="{t1}" d="{D_CRIO}"/><path fill="{t2}" d="{D_MEP}"/></g>{t}</svg>')


def wall(w, h, bw=48, bh=22, gap=6, cols=(N,), weights=None, seed=1, rx=3, holes=0.0, opacity=1):
    """Running-bond brick wall as an SVG string."""
    rnd = random.Random(seed)
    r = []
    y, row = 0, 0
    while y < h:
        x = -(bw + gap) / 2 if row % 2 else 0
        while x < w:
            if rnd.random() >= holes:
                col = rnd.choices(cols, weights=weights)[0]
                r.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" rx="{rx}" fill="{col}"/>')
            x += bw + gap
        y += bh + gap
        row += 1
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="opacity:{opacity}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(r)}</svg>')


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmyk(h):
    r, g, b = (v / 255 for v in rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    return tuple(round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


TOTAL = 15


def foot(n, dark=False):
    lg = lockup(dark=dark, cls='foot-logo')
    return f'<div class="foot {"dk" if dark else ""}">{lg}<span>Criomep · Option 40 · Brick</span><b>{n:02d}<i> / {TOTAL}</i></b></div>'


def head(eyebrow, title, dark=False):
    return f'<div class="head {"dk" if dark else ""}"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2></div>'


slides = []

# ---------------------------------------------------------------- 01 cover
cover_wall = wall(900, 900, bw=64, bh=28, gap=8, cols=('#131D40', '#16224C', '#1A2858', N, C, Y),
                  weights=(30, 30, 20, 8, 4, 1.5), seed=7, rx=4, holes=.18)
slides.append(f'''
<section class="slide" style="background:{M}">
  <div class="cover-wall">{cover_wall}</div>
  <div class="cover-glow"></div>
  {sym(cls="cover-sym", b=P)}
  <div class="cover-left">
    <div class="eyebrow light">Brand identity proposal · Option 40 · Colour refresh</div>
    {lockup(dark=True, tag=True, cls="cover-logo")}
    <h1>Built<br>brick by<br><span>brick.</span></h1>
    <p>The Brick mark, re-fired in <b>Blueprint Cobalt</b> &amp; <b>Desert Saffron</b>.</p>
  </div>
  <div class="cover-meta"><span>Criomep — formerly Mepclick</span><span>October 2026</span></div>
  <div class="loose b1"></div><div class="loose b2"></div><div class="loose b3"></div>
</section>''')

# ---------------------------------------------------------------- 02 colour story
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("The refresh", "Same wall. New colour story.")}
  <div class="story">
    <div class="story-card before">
      <div class="tag">Before</div>
      {inline(orig("symbol"), "story-sym")}
      <h3>Fired clay</h3>
      <div class="chips">{''.join(f'<i style="background:{x}"></i>' for x in ('#B23A2E', '#8E2C22', '#D9774B', '#2B2B2B'))}</div>
      <p>Warm, earthy and handmade — but close to every brick-maker and cement brand in the region.</p>
    </div>
    <div class="story-arrow">
      <svg viewBox="0 0 120 40"><path d="M0 20h108M96 6l16 14-16 14" fill="none" stroke="{C}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>
    <div class="story-card after">
      <div class="tag">After</div>
      {sym(cls="story-sym big", b=P)}
      <h3>Cobalt <span>×</span> Saffron</h3>
      <div class="chips">{''.join(f'<i style="background:{x}"></i>' for x in (C, P, Y, '#fff'))}</div>
      <p>Engineered and confident. Cobalt speaks of blueprints, precision and trust; saffron brings the desert sun and the high-vis energy of the jobsite.</p>
    </div>
  </div>
  <div class="story-why">
    <div><b>01</b><span>Stands apart from red-and-grey construction brands</span></div>
    <div><b>02</b><span>Reads as a tech platform, not a materials supplier</span></div>
    <div><b>03</b><span>Saffron accent is instantly visible on site and on screen</span></div>
  </div>
  {foot(2)}
</section>''')

# ---------------------------------------------------------------- 03 concept
slides.append(f'''
<section class="slide" style="background:{L}">
  {head("Concept", "Brick")}
  <div class="concept">
    <div class="concept-disc">{sym(cls="concept-sym")}</div>
    <div class="concept-text">
      <p class="quote">“Every brick is a product, a supplier, a delivery.”</p>
      <p>A <b>C</b> laid brick by brick in staggered courses, like a real wall. Criomep builds your project’s supply one solid piece at a time — and the refreshed palette makes that process feel precise, digital and dependable.</p>
      <div class="pills"><span>Construction</span><span>Precision</span><span>Step by step</span><span>Marketplace</span></div>
      <div class="traits">
        <div><i style="background:{C}"></i>Sturdy</div>
        <div><i style="background:{N}"></i>Precise</div>
        <div><i style="background:{Y}"></i>Optimistic</div>
        <div><i style="background:{M}"></i>Hard-working</div>
      </div>
    </div>
  </div>
  {foot(3)}
</section>''')

# ---------------------------------------------------------------- 04 meaning
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("What the logo means", "Every part tells the story")}
  <div class="anat">
    <div class="anat-art">
      {sym(cls="anat-sym")}
      <div class="pin p1">01</div><div class="pin p2">02</div><div class="pin p3">03</div><div class="pin p4">04</div>
    </div>
    <div class="anat-list">
      <div><b>01</b><h4>Each brick</h4><p>A product or a supplier, placed exactly where it belongs.</p></div>
      <div><b>02</b><h4>Staggered courses</h4><p>Built like a real wall — interlocked, strong, load-bearing.</p></div>
      <div><b>03</b><h4>The C</h4><p>The open wall curves into the C of Criomep — open for business.</p></div>
      <div><b>04</b><h4>Three tones</h4><p><span class="sw" style="background:{C}"></span>Cobalt = structure &nbsp; <span class="sw" style="background:{N}"></span>Navy = depth &nbsp; <span class="sw" style="background:{Y}"></span>Saffron = energy</p></div>
    </div>
  </div>
  {foot(4)}
</section>''')

# ---------------------------------------------------------------- 05 geometry (blueprint)
circ = ''.join(f'<circle cx="47" cy="48" r="{r}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".35" stroke-dasharray="1.2 1.2"/>' for r in (17, 46))
grid = ''.join(f'<line x1="{x}" y1="-6" x2="{x}" y2="102" stroke="#fff" stroke-opacity=".12" stroke-width=".25"/>' for x in range(-4, 100, 9)) + \
       ''.join(f'<line x1="-6" y1="{y}" x2="100" y2="{y}" stroke="#fff" stroke-opacity=".12" stroke-width=".25"/>' for y in range(4, 100, 10))
fills = ''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{ {"a": "#fff", "b": P, "c": Y}[k] }" fill-opacity=".92"/>' for x, y, k in BRICKS)
blue = (f'<svg class="bp-art" viewBox="-6 -6 106 108" xmlns="http://www.w3.org/2000/svg">{grid}{circ}{fills}'
        f'<line x1="47" y1="48" x2="90.2" y2="32.3" stroke="{Y}" stroke-width=".4"/><text x="86" y="29" fill="{Y}" font-size="3.2" font-family="Inter">R46</text>'
        f'<line x1="47" y1="48" x2="64" y2="48" stroke="{Y}" stroke-width=".4"/><text x="52" y="52" fill="{Y}" font-size="3.2" font-family="Inter">R17</text>'
        f'<line x1="2" y1="-2.5" x2="18" y2="-2.5" stroke="#fff" stroke-width=".3"/><text x="5.5" y="-3.6" fill="#fff" font-size="2.6" font-family="Inter">16</text>'
        f'<line x1="-2.5" y1="24" x2="-2.5" y2="32" stroke="#fff" stroke-width=".3"/><text x="-5.5" y="29.5" fill="#fff" font-size="2.6" font-family="Inter">8</text>'
        f'<circle cx="47" cy="48" r=".9" fill="{Y}"/></svg>')
slides.append(f'''
<section class="slide bp" style="background:{C}">
  {head("Construction", "Built on a blueprint", dark=True)}
  {blue}
  <div class="bp-spec">
    <div><span>Module</span><h4>16 × 8 brick</h4><p>Every brick shares one proportion, with 2-unit mortar joints.</p></div>
    <div><span>Bond</span><h4>Half-brick offset</h4><p>Every second course shifts by half a brick — a true running bond.</p></div>
    <div><span>Mask</span><h4>C between R17 &amp; R46</h4><p>Only bricks that fall inside the C-ring are laid.</p></div>
    <div><span>Corners</span><h4>1.6 radius</h4><p>Softened edges keep it friendly at small sizes.</p></div>
  </div>
  {foot(5, dark=True)}
</section>''')

# ---------------------------------------------------------------- 06 master lockup
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("Primary logo", "The master lockup")}
  <div class="master">{lockup(tag=True, cls="master-logo")}</div>
  <div class="master-notes">
    <span>Horizontal lockup with descriptor — first choice for all applications.</span>
    <span>Wordmark: Bebas Neue, outlined · “CRIO” in Midnight, “MEP” in Cobalt</span>
  </div>
  <div class="master-strip">{wall(1440, 60, bw=40, bh=16, gap=5, cols=(C, N, Y, '#E7EBFF'), weights=(30, 20, 8, 42), seed=3)}</div>
  {foot(6)}
</section>''')

# ---------------------------------------------------------------- 07 suite + clear space
stacked = (f'<div class="stack">{sym(cls="st-sym")}{wm(cls="st-wm")}'
           f'<svg class="st-tag" viewBox="0 -9 234 10"><path fill="{G}" d="{D_TAG}"/></svg></div>')
slides.append(f'''
<section class="slide" style="background:{L}">
  {head("Logo suite", "One system, every format")}
  <div class="suite">
    <div class="card s-h">{lockup(cls="lg")}<label>Horizontal</label></div>
    <div class="card s-st">{stacked}<label>Stacked</label></div>
    <div class="card s-sy">{sym(cls="sm")}<label>Symbol</label></div>
    <div class="card s-wm">{wm(cls="wmk")}<label>Wordmark</label></div>
    <div class="card s-cs">
      <div class="cs-box">{lockup(cls="cs-logo")}<i class="x x1">x</i><i class="x x2">x</i><i class="x x3">x</i><i class="x x4">x</i></div>
      <label>Clear space = x (½ symbol height) · Min. 120 px / 30 mm · Symbol 24 px</label>
    </div>
  </div>
  {foot(7)}
</section>''')

# ---------------------------------------------------------------- 08 palette
pal = [('Primary', 'Blueprint Cobalt', C, '#fff', 44), ('Ink', 'Midnight Steel', M, '#fff', 22),
       ('Accent', 'Desert Saffron', Y, M, 12), ('Deep', 'Conduit Navy', N, '#fff', 12), ('Tint', 'Limestone', L, M, 10)]
bar = ''.join(f'<i style="flex:{p};background:{h}"></i>' for _, _, h, _, p in pal)
cards = ''
for role, name, h, tc, p in pal:
    r, g, b = rgb(h)
    cc = cmyk(h)
    cards += (f'<div class="sw-card" style="background:{h};color:{tc}"><div class="sw-top"><span>{role}</span><b>{p}%</b></div>'
              f'<div class="sw-bot"><h4>{name}</h4><p>HEX {h}<br>RGB {r} {g} {b}<br>CMYK {cc[0]} {cc[1]} {cc[2]} {cc[3]}</p></div></div>')
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("Colour palette", "Colours with purpose")}
  <div class="pal-bar">{bar}</div>
  <div class="pal">{cards}</div>
  <div class="pal-note"><span class="sw" style="background:{P}"></span><b>Periwinkle {P}</b> replaces Conduit Navy in the symbol whenever it sits on a dark background, so every brick stays visible.</div>
  {foot(8)}
</section>''')

# ---------------------------------------------------------------- 09 colour versions
slides.append(f'''
<section class="slide" style="background:{L}">
  {head("Colour versions", "Positive, reversed &amp; mono")}
  <div class="vers">
    <div class="v" style="background:#fff">{lockup(cls="vl")}<label>Primary · on white</label></div>
    <div class="v" style="background:{M}">{lockup(dark=True, cls="vl")}<label class="lt">Reversed · on midnight</label></div>
    <div class="v" style="background:{C}">{lockup(monocol="#fff", cls="vl")}<label class="lt">Mono white · on cobalt</label></div>
    <div class="v" style="background:{Y}">{lockup(monocol=M, cls="vl")}<label>Mono midnight · on saffron</label></div>
  </div>
  {foot(9)}
</section>''')

# ---------------------------------------------------------------- 10 typography
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("Typography", "Inter Display &amp; Inter")}
  <div class="type">
    <div class="type-hero">
      <div class="aa">Aa</div>
      <div class="glyphs">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 &amp; @ # % → ✓</div>
    </div>
    <div class="type-scale">
      <div class="ts"><span>Display · Inter Display Black · 72</span><p class="t1">MEP procurement, <em>simplified.</em></p></div>
      <div class="ts"><span>Heading · Inter Display Bold · 32</span><p class="t2">Compare suppliers in minutes</p></div>
      <div class="ts"><span>Body · Inter Regular · 16</span><p class="t3">Send your BOQ, compare supplier options and move project requirements toward procurement — one workflow, from quote to delivery.</p></div>
      <div class="ts row"><span>Logo wordmark</span>{wm(cls="ts-wm")}<p class="t4">Bebas Neue, outlined — used in the logo only, never retyped.</p></div>
    </div>
  </div>
  {foot(10)}
</section>''')

# ---------------------------------------------------------------- 11 brand graphics
steps = [('BOQ received', 4), ('Quotes compared', 8), ('Order placed', 12), ('Delivered', 16)]
prog = ''
for i, (lbl, n) in enumerate(steps):
    bricks = ''.join(f'<i class="{"on" if j < n else ""} {"y" if (j < n and i == 3) else ""}"></i>' for j in range(16))
    prog += f'<div class="pg"><div class="pg-b">{bricks}</div><span>{lbl}</span></div>'
slides.append(f'''
<section class="slide" style="background:{M}">
  {head("Brand graphics", "A pattern you can build with", dark=True)}
  <div class="gfx">
    <div class="g g1">{wall(420, 470, bw=46, bh=20, gap=6, cols=(C, N, '#3A5CFF', Y), weights=(40, 40, 15, 5), seed=11)}<label>Running bond — backgrounds &amp; hoardings</label></div>
    <div class="g g2">{wall(420, 470, bw=46, bh=20, gap=6, cols=(Y, '#FFC552', '#F5A100', '#fff'), weights=(45, 25, 25, 5), seed=4, holes=.55)}<label>Loose bricks — energy, launches, promos</label></div>
    <div class="g g3"><div class="prog">{prog}</div><label>Brick progress — order tracking in the product</label></div>
  </div>
  {foot(11, dark=True)}
</section>''')

# ---------------------------------------------------------------- 12 app & mobile
icon = lambda bg, a, b, c, cls='': f'<div class="ic {cls}" style="background:{bg}">{sym(a=a, b=b, c=c)}</div>'
slides.append(f'''
<section class="slide" style="background:{L}">
  {head("Digital", "App icon &amp; mobile")}
  <div class="app">
    <div class="icons">
      <div class="ic-row">{icon(M, C, P, Y, "xl")}{icon(C, "#fff", P, Y, "xl")}{icon(Y, M, N, "#fff", "xl")}</div>
      <div class="ic-labels"><span>Primary</span><span>Cobalt</span><span>Saffron (promo)</span></div>
      <div class="ic-sizes">{icon(M, C, P, Y, "s1")}{icon(M, C, P, Y, "s2")}{icon(M, C, P, Y, "s3")}{icon(M, C, P, Y, "s4")}<span>180 · 96 · 48 · 24 px</span></div>
      <p>The symbol works as a standalone app icon, favicon and social avatar — legible down to 24 px.</p>
    </div>
    <div class="phone ph1"><div class="scr" style="background:{M}">
      <div class="splash">{sym(b=P, cls="sp-sym")}{wm(c1="#fff", c2=Y, cls="sp-wm")}<div class="sp-t">MEP procurement, simplified</div></div>
    </div></div>
    <div class="phone ph2"><div class="scr" style="background:#fff">
      <div class="m-top">{lockup(cls="m-logo")}<i></i></div>
      <div class="m-hero"><small>Your project</small><b>Al Noor Tower — Phase 2</b>
        <div class="pg-b mini">{''.join(f'<i class="{"on" if j < 11 else ""}"></i>' for j in range(16))}</div><span>11 of 16 packages sourced</span></div>
      <div class="m-list">
        <div><i style="background:{C}"></i><b>HVAC ducting</b><em>3 quotes</em></div>
        <div><i style="background:{Y}"></i><b>LV cables</b><em>Ordered</em></div>
        <div><i style="background:{N}"></i><b>PPR pipes</b><em>Delivered</em></div>
      </div>
      <div class="m-btn">Upload BOQ</div>
    </div></div>
  </div>
  {foot(12)}
</section>''')

# ---------------------------------------------------------------- 13 website
slides.append(f'''
<section class="slide" style="background:#fff">
  {head("Digital", "Website")}
  <div class="browser">
    <div class="bar"><i></i><i></i><i></i><span>criomep.com</span></div>
    <div class="nav">{lockup(cls="nav-logo")}<div class="links"><span>Categories</span><span>How it works</span><span>Suppliers</span><span>Projects</span></div><b>Upload BOQ</b></div>
    <div class="hero" style="background:{M}">
      <div class="hero-wall">{wall(640, 420, bw=52, bh=22, gap=7, cols=('#141E44', '#18245A', N, C, Y), weights=(35, 30, 18, 12, 4), seed=21, holes=.2)}</div>
      <div class="hero-txt">
        <div class="kick">Saudi Arabia · MEP marketplace</div>
        <h3>MEP procurement,<br><em>simplified.</em></h3>
        <p>Send your BOQ, compare supplier options and procure electrical, plumbing, HVAC and mechanical products.</p>
        <div class="ctas"><b>Send your requirement</b><span>Explore categories</span></div>
      </div>
      {sym(b=P, cls="hero-sym")}
    </div>
    <div class="cats"><div><i style="background:{C}"></i>Electrical</div><div><i style="background:{Y}"></i>Plumbing</div><div><i style="background:{P}"></i>HVAC</div><div><i style="background:{N}"></i>Mechanical</div><div><i style="background:{M}"></i>Fire &amp; safety</div></div>
  </div>
  {foot(13)}
</section>''')

# ---------------------------------------------------------------- 14 brand in the world
van = f'''<svg class="van" viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="320" cy="282" rx="300" ry="12" fill="#000" opacity=".18"/>
  <path d="M30 60 Q30 40 50 40 H430 Q450 40 455 60 L470 250 H30 Z" fill="#fff"/>
  <path d="M455 70 H530 Q560 70 575 100 L610 170 Q618 186 618 205 V250 H470 Z" fill="#fff"/>
  <path d="M478 86 H526 Q546 86 556 106 L582 160 H478 Z" fill="{M}" opacity=".85"/>
  <rect x="30" y="206" width="588" height="44" fill="{C}"/>
  <rect x="30" y="200" width="588" height="6" fill="{Y}"/>
  <g transform="translate(70 70) scale(1.05)">{''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{ {"a": C, "b": N, "c": Y}[k] }"/>' for x, y, k in BRICKS)}</g>
  <g transform="translate(180 158) scale(.95)"><path fill="{M}" d="{D_CRIO}"/><path fill="{C}" d="{D_MEP}"/></g>
  <text x="182" y="186" font-family="Inter" font-weight="600" font-size="14" fill="{G}" letter-spacing="2">MEP PROCUREMENT, SIMPLIFIED · CRIOMEP.COM</text>
  <circle cx="130" cy="252" r="34" fill="{M}"/><circle cx="130" cy="252" r="14" fill="#C9CEDC"/>
  <circle cx="520" cy="252" r="34" fill="{M}"/><circle cx="520" cy="252" r="14" fill="#C9CEDC"/>
  <rect x="604" y="196" width="16" height="10" rx="3" fill="{Y}"/>
</svg>'''
slides.append(f'''
<section class="slide" style="background:{L}">
  {head("Brand in the world", "Stationery, fleet &amp; social")}
  <div class="world">
    <div class="stat">
      <div class="letter">{lockup(cls="lt-logo")}<div class="lt-lines"><i></i><i></i><i class="s"></i><i></i><i></i><i class="s"></i><i></i><i class="s"></i></div><div class="lt-foot"><span>criomep.com</span><span>Riyadh, Saudi Arabia</span></div><div class="lt-strip"></div></div>
      <div class="bc bc-front" style="background:{C}">{lockup(monocol="#fff", cls="bc-logo")}<div class="bc-y"></div></div>
      <div class="bc bc-back">{sym(cls="bc-sym")}<div class="bc-txt"><b>Name Surname</b><span>Procurement Manager</span><span>+966 5X XXX XXXX</span><span>name@criomep.com</span></div></div>
    </div>
    <div class="right">
      <div class="fleet" style="background:linear-gradient(180deg,#DDE3F5,#C6CEE6)">{van}<label>Delivery fleet</label></div>
      <div class="social">
        <div class="post" style="background:{C}"><div class="po-in">{sym(a="#fff", b=P, c=Y)}</div></div>
        <div class="post" style="background:{Y}"><b>BOQ in.<br>Quotes out.</b></div>
        <div class="post" style="background:{M}">{wall(200, 200, bw=30, bh=12, gap=4, cols=(N, C, Y, '#18245A'), weights=(30, 30, 6, 34), seed=5)}<span>500+ suppliers</span></div>
      </div>
    </div>
  </div>
  {foot(14)}
</section>''')

# ---------------------------------------------------------------- 15 closing
end_wall = wall(1440, 810, bw=64, bh=28, gap=8, cols=('#121C3E', '#15204A', '#192654'), weights=(1, 1, 1), seed=99, rx=4, holes=.08)
slides.append(f'''
<section class="slide end" style="background:{M}">
  <div class="end-wall">{end_wall}</div>
  <div class="end-in">
    {sym(b=P, cls="end-sym")}
    {wm(c1="#fff", c2=Y, cls="end-wm")}
    <svg class="end-tag" viewBox="0 -9 234 10"><path fill="rgba(255,255,255,.7)" d="{D_TAG}"/></svg>
    <div class="end-meta">Option 40 · Brick · Cobalt edition</div>
    <p>The most construction-rooted option — now engineered for a digital marketplace.<br>It looks built, not drawn.</p>
  </div>
  <div class="end-dots">{''.join(f'<i style="background:{x}"></i>' for x in (C, P, Y, L))}</div>
</section>''')

assert len(slides) == TOTAL, len(slides)

CSS = open(os.path.join(S, 'deck.css')).read()
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Criomep Option 40 — Brick (Cobalt edition)</title>
<style>{CSS}</style></head><body>{''.join(slides)}</body></html>'''
open(os.path.join(OUT, 'deck.html'), 'w').write(html)

# ---------------------------------------------------------------- logo kit
kit = {
    'horizontal': recolour(orig('horizontal'), POS),
    'horizontal-tagline': recolour(orig('horizontal-tagline'), POS),
    'horizontal-white': recolour(orig('horizontal-white'), DARK),
    'horizontal-black': orig('horizontal-black'),
    'stacked': recolour(orig('stacked'), POS),
    'stacked-white': recolour(orig('stacked-white'), DARK),
    'symbol': recolour(orig('symbol'), POS),
    'symbol-white': recolour(orig('symbol-white'), DARK),
    'wordmark': recolour(orig('wordmark'), POS),
    'app-icon': recolour(orig('app-icon'), DARK),
    'horizontal-mono-white': mono(orig('horizontal'), '#FFFFFF'),
}
for k, v in kit.items():
    open(os.path.join(OUT, 'logo', f'criomep-{k}.svg'), 'w').write(v)
print('ok', OUT)
