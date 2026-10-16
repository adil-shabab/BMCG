"""Criomep Option 40 'Brick' — detailed 25-page brand presentation in the original clay palette."""
import os, re, random, sys

S = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(S, '..', 'orig')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, 'out')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- original palette
R = '#B23A2E'   # Brick Red   (primary)
K = '#2B2B2B'   # Mortar      (secondary)
T = '#D9774B'   # Terracotta  (light)
F = '#8E2C22'   # Fired Clay  (deep)
P = '#FAF1EC'   # Plaster     (tint)
D = '#1E1A19'   # Kiln Black  (dark backgrounds)
G = '#7A6A64'   # Ash         (descriptor / supporting text)


def orig(name):
    return open(os.path.join(ORIG, f'criomep-{name}.svg')).read()


BRICKS = []
for x, y, f in re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="16" height="8" rx="1.6" fill="(#\w+)"', orig('symbol')):
    BRICKS.append((float(x), float(y), {'#B23A2E': 'a', '#8E2C22': 'b', '#D9774B': 'c'}[f]))
D_CRIO, D_MEP, D_TAG = re.findall(r'd="([^"]+)"', orig('horizontal-tagline'))


def rects(a=R, b=F, c=T, op=None):
    col = {'a': a, 'b': b, 'c': c}
    o = f' fill-opacity="{op}"' if op else ''
    return ''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{col[k]}"{o}/>' for x, y, k in BRICKS)


def sym(a=R, b=F, c=T, cls='', style=''):
    return f'<svg class="{cls}" style="{style}" viewBox="0 0 84 96" xmlns="http://www.w3.org/2000/svg">{rects(a, b, c)}</svg>'


def wm(c1=K, c2=R, cls='', style=''):
    return (f'<svg class="{cls}" style="{style}" viewBox="0 -51 209 53" xmlns="http://www.w3.org/2000/svg">'
            f'<path fill="{c1}" d="{D_CRIO}"/><path fill="{c2}" d="{D_MEP}"/></svg>')


def tag(col=G, cls='', style=''):
    return f'<svg class="{cls}" style="{style}" viewBox="0 -9 234 10" xmlns="http://www.w3.org/2000/svg"><path fill="{col}" d="{D_TAG}"/></svg>'


def lockup(dark=False, tagline=False, cls='', style='', mono=None):
    t1, t2, tg = ('#fff', T, 'rgba(255,255,255,.72)') if dark else (K, R, G)
    a, b, c = R, F, T
    if mono:
        a = b = c = t1 = t2 = tg = mono
    h = 110 if tagline else 96
    tl = f'<g transform="translate(126 100.5)"><path fill="{tg}" d="{D_TAG}"/></g>' if tagline else ''
    return (f'<svg class="{cls}" style="{style}" viewBox="0 0 {360 if tagline else 334} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'{rects(a, b, c)}<g transform="translate(126 74.5)"><path fill="{t1}" d="{D_CRIO}"/><path fill="{t2}" d="{D_MEP}"/></g>{tl}</svg>')


def stacked(dark=False, cls='', style=''):
    t1, t2, tg = ('#fff', T, 'rgba(255,255,255,.72)') if dark else (K, R, G)
    return (f'<svg class="{cls}" style="{style}" viewBox="0 0 234 220" xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate(75 0)">{rects()}</g>'
            f'<g transform="translate(12.5 172)"><path fill="{t1}" d="{D_CRIO}"/><path fill="{t2}" d="{D_MEP}"/></g>'
            f'<g transform="translate(0 205) scale(1)"><path fill="{tg}" d="{D_TAG}"/></g></svg>')


def wall(w, h, bw=48, bh=22, gap=6, cols=(F,), weights=None, seed=1, rx=3, holes=0.0, cls='', style=''):
    rnd = random.Random(seed)
    r, y, row = [], 0, 0
    while y < h:
        x = -(bw + gap) / 2 if row % 2 else 0
        while x < w:
            if rnd.random() >= holes:
                r.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="{bh}" rx="{rx}" fill="{rnd.choices(cols, weights=weights)[0]}"/>')
            x += bw + gap
        y += bh + gap
        row += 1
    return f'<svg class="{cls}" style="{style}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{"".join(r)}</svg>'


def rgb(h):
    return tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


TOTAL = 25


def foot(n, dark=False):
    return (f'<div class="foot {"dk" if dark else ""}">{lockup(dark=dark, cls="fl")}'
            f'<span>Brand identity · Option 40 · Brick</span><b>{n:02d}<i> / {TOTAL}</i></b></div>')


def head(eyebrow, title, dark=False, sub=''):
    s = f'<p class="sub">{sub}</p>' if sub else ''
    return f'<div class="head {"dk" if dark else ""}"><div class="eb">{eyebrow}</div><h2>{title}</h2>{s}</div>'


def slide(n, body, bg='#fff', dark=False, cls='', footer=True):
    return f'<section class="slide {cls}" style="background:{bg}">{body}{foot(n, dark) if footer else ""}</section>'


SL = []

# 01 ------------------------------------------------------------ cover
SL.append(slide(1, f'''
  <div class="cv-wall">{wall(820, 900, bw=70, bh=30, gap=9, cols=('#2A2422', '#2F2826', '#352C29', F, R, T), weights=(30, 30, 25, 6, 4, 3), seed=40, rx=5, holes=.22)}</div>
  <div class="cv-shade"></div>
  <div class="cv-in">
    <div class="eb lt">Brand identity proposal · Option 40</div>
    {sym(cls="cv-sym")}
    {wm(c1="#fff", c2=T, cls="cv-wm")}
    {tag("rgba(255,255,255,.7)", cls="cv-tag")}
  </div>
  <div class="cv-title"><h1>Brick</h1><p>Built brick by brick.</p></div>
  <div class="cv-meta"><span>Criomep — formerly Mepclick</span><span>Brand guidelines &amp; applications</span><span>October 2026</span></div>
''', bg=D, footer=False))

# 02 ------------------------------------------------------------ contents
chap = [('01', 'The story', [('The rebrand', 3), ('Brand essence', 4), ('Concept', 5), ('What the logo means', 6)]),
        ('02', 'The logo', [('Geometry', 7), ('How it is built', 8), ('Master lockup', 9), ('Logo suite', 10), ('Clear space', 11)]),
        ('03', 'Colour, type &amp; usage', [('Colour palette', 12), ('Colour versions', 13), ('Logo misuse', 14), ('Typography', 15), ('Pattern', 16), ('Iconography', 17)]),
        ('04', 'Applications', [('Letterhead', 18), ('Business cards', 19), ('ID card', 20), ('App &amp; mobile', 21), ('Website', 22), ('Signage', 23), ('Fleet, merch &amp; social', 24)])]
cont = ''
for no, name, items in chap:
    li = ''.join(f'<li><span>{it}</span><b>{n:02d}</b></li>' for it, n in items)
    cont += f'<div class="ch"><div class="ch-no">{no}</div><h3>{name}</h3><ul>{li}</ul></div>'
SL.append(slide(2, f'''
  {head("Contents", "What's inside")}
  <div class="toc">{cont}</div>
  <div class="toc-strip">{wall(1440, 34, bw=46, bh=14, gap=6, cols=(R, F, T, '#F1E2D9'), weights=(20, 20, 15, 45), seed=2)}</div>
'''))

# 03 ------------------------------------------------------------ rebrand
SL.append(slide(3, f'''
  {head("The rebrand", "From Mepclick to Criomep")}
  <div class="rb">
    <div class="rb-old">mepclick</div>
    <svg class="rb-arr" viewBox="0 0 120 40"><path d="M0 20h108M94 6l16 14-16 14" fill="none" stroke="{R}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    {lockup(cls="rb-new")}
  </div>
  <div class="rb-cards">
    <div><h4>Crio</h4><p>The platform’s core identity — short, ownable and ready to grow beyond a single product.</p></div>
    <div><h4>MEP</h4><p>Mechanical, Electrical &amp; Plumbing — says exactly what the marketplace sources, at a glance.</p></div>
    <div class="dk"><h4>Criomep</h4><p>MEP procurement, simplified — for contractors, facilities teams, developers and procurement professionals.</p></div>
  </div>
''', bg='#fff'))

# 04 ------------------------------------------------------------ brand essence
SL.append(slide(4, f'''
  {head("Brand essence", "What Criomep stands for")}
  <div class="ess">
    <div class="ess-mission"><span>Mission</span><p>Make MEP procurement in Saudi Arabia <em>simple, transparent and fast</em> — from BOQ to delivery, in one workflow.</p>
      {wall(560, 120, bw=54, bh=22, gap=7, cols=(R, F, T, '#3A3230'), weights=(30, 25, 20, 25), seed=8, cls="ess-wall")}</div>
    <div class="ess-col">
      <div class="ess-box"><span>Who we serve</span><ul><li>Contractors &amp; sub-contractors</li><li>Facilities &amp; maintenance teams</li><li>Developers &amp; project owners</li><li>Procurement professionals</li></ul></div>
      <div class="ess-box"><span>Promise</span><h4>Every product, placed exactly where it belongs.</h4></div>
    </div>
    <div class="ess-col">
      <div class="ess-box pers"><span>Personality</span>
        <div class="bar"><b>Sturdy</b><i style="--w:90%"></i></div>
        <div class="bar"><b>Honest</b><i style="--w:84%"></i></div>
        <div class="bar"><b>Hard-working</b><i style="--w:95%"></i></div>
        <div class="bar"><b>Warm</b><i style="--w:72%"></i></div>
        <div class="bar"><b>Modern</b><i style="--w:66%"></i></div>
      </div>
    </div>
  </div>
''', bg=P))

# 05 ------------------------------------------------------------ concept
SL.append(slide(5, f'''
  {head("Concept", "Brick")}
  <div class="cc">
    <div class="cc-disc">{sym(cls="cc-sym")}</div>
    <div class="cc-txt">
      <p class="q">Built brick by brick.</p>
      <p>A <b>C</b> laid brick by brick in staggered courses, like a real wall. Every brick is a product, a supplier, a delivery — Criomep builds your project’s supply one solid piece at a time. Warm clay reds make it honest, sturdy and rooted in construction.</p>
      <div class="pills"><span>Construction</span><span>Solid</span><span>Step by step</span></div>
      <div class="traits"><div><i style="background:{R}"></i>Sturdy</div><div><i style="background:{K}"></i>Honest</div><div><i style="background:{T}"></i>Hard-working</div><div><i style="background:{F}"></i>Warm</div></div>
    </div>
  </div>
''', bg=P))

# 06 ------------------------------------------------------------ meaning
SL.append(slide(6, f'''
  {head("What the logo means", "Every part tells the story")}
  <div class="an">
    <div class="an-art">{sym(cls="an-sym")}<div class="pin pn1">01</div><div class="pin pn2">02</div><div class="pin pn3">03</div><div class="pin pn4">04</div></div>
    <div class="an-list">
      <div><b>01</b><h4>Each brick</h4><p>A product or supplier, placed exactly where it belongs.</p></div>
      <div><b>02</b><h4>Staggered courses</h4><p>Built like a real wall — strong and interlocked.</p></div>
      <div><b>03</b><h4>The C</h4><p>The wall curves into the C of Criomep.</p></div>
      <div><b>04</b><h4>Clay tones</h4><p>Three shades of fired clay for warmth and texture.</p></div>
    </div>
  </div>
  <div class="an-chips"><span>✓ Unmistakably construction</span><span>✓ Rich, crafted texture</span><span>✓ Strong on signage and site hoardings</span></div>
''', bg='#fff'))

# 07 ------------------------------------------------------------ geometry
grid = ''.join(f'<line x1="{x}" y1="-4" x2="{x}" y2="100" stroke="#fff" stroke-opacity=".08" stroke-width=".3"/>' for x in range(-4, 96, 9)) + \
       ''.join(f'<line x1="-6" y1="{y}" x2="96" y2="{y}" stroke="#fff" stroke-opacity=".08" stroke-width=".3"/>' for y in range(4, 100, 10))
circ = ''.join(f'<circle cx="47" cy="48" r="{r}" fill="none" stroke="{T}" stroke-opacity=".7" stroke-width=".35" stroke-dasharray="1.2 1.2"/>' for r in (17, 46))
geo = (f'<svg class="geo-art" viewBox="-8 -8 106 110">{grid}{circ}{rects()}'
       f'<line x1="47" y1="48" x2="90.2" y2="32.3" stroke="#fff" stroke-width=".35"/><text x="84" y="29" fill="#fff" font-size="3.4" font-family="Manrope">R46</text>'
       f'<line x1="47" y1="48" x2="64" y2="48" stroke="#fff" stroke-width=".35"/><text x="54" y="52.5" fill="#fff" font-size="3.4" font-family="Manrope">R17</text>'
       f'<circle cx="47" cy="48" r=".9" fill="#fff"/>'
       f'<line x1="2" y1="-3" x2="18" y2="-3" stroke="#fff" stroke-width=".3"/><text x="7" y="-4.3" fill="#fff" font-size="2.8" font-family="Manrope">16</text>'
       f'<line x1="-3" y1="24" x2="-3" y2="32" stroke="#fff" stroke-width=".3"/><text x="-6.5" y="29.5" fill="#fff" font-size="2.8" font-family="Manrope">8</text>'
       f'<text x="-6" y="101" fill="#fff" fill-opacity=".5" font-size="2.6" font-family="Manrope" letter-spacing=".4">COURSES ×9 · MORTAR 2 · OFFSET ½</text></svg>')
SL.append(slide(7, f'''
  {head("Construction", "Built on geometry", dark=True)}
  {geo}
  <div class="geo-spec">
    <div><span>01 · Bricks</span><h4>16 × 8 units</h4><p>Every brick shares one proportion, with 2-unit mortar joints.</p></div>
    <div><span>02 · Courses</span><h4>Half-brick offset</h4><p>Every second course shifts by half a brick — a true running bond.</p></div>
    <div><span>03 · C mask</span><h4>Radii 17 &amp; 46</h4><p>Only the bricks that fall inside the C-ring are laid.</p></div>
    <div><span>04 · Corners</span><h4>1.6 radius</h4><p>Softened corners keep the mark crisp yet friendly at small sizes.</p></div>
  </div>
''', bg=D, dark=True))

# 08 ------------------------------------------------------------ build process
full = [(x, y) for y in range(4, 94, 10) for x in ([2, 20, 38, 56] if (y // 10) % 2 == 0 else [11, 29, 47, 65])]
inset = {(x, y) for x, y, _ in BRICKS}
st1 = ''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="#E9D9D0"/>' for x, y in full)
st2 = ''.join(f'<rect x="{x}" y="{y}" width="16" height="8" rx="1.6" fill="{K if (x, y) in inset else "#EFE3DC"}"/>' for x, y in full) + \
      ''.join(f'<circle cx="47" cy="48" r="{r}" fill="none" stroke="{R}" stroke-width=".5" stroke-dasharray="1.4 1.2"/>' for r in (17, 46))
steps = [('Lay the wall', 'A full running-bond wall of identical 16 × 8 bricks.', st1),
         ('Mask the C', 'A C-ring between radii 17 and 46 selects the bricks to keep.', st2),
         ('Fire the clay', 'The remaining bricks take three clay tones — the mark is built.', rects())]
proc = ''.join(f'<div class="pr"><div class="pr-art"><svg viewBox="-6 -2 96 100">{s}</svg></div><b>Step {i + 1:02d}</b><h4>{t}</h4><p>{d}</p></div>'
               + ('<div class="pr-arr">→</div>' if i < 2 else '') for i, (t, d, s) in enumerate(steps))
SL.append(slide(8, f'''
  {head("Process", "How the mark is built")}
  <div class="proc">{proc}</div>
''', bg='#fff'))

# 09 ------------------------------------------------------------ master lockup
SL.append(slide(9, f'''
  {head("Primary logo", "The master lockup")}
  <div class="ms">{lockup(tagline=True, cls="ms-logo")}</div>
  <div class="ms-notes"><span>Horizontal lockup with descriptor — first choice for all applications.</span><span>Wordmark: Bebas Neue, outlined · “CRIO” in Mortar, “MEP” in Brick Red</span></div>
''', bg='#fff'))

# 10 ------------------------------------------------------------ suite
SL.append(slide(10, f'''
  {head("Logo suite", "One system, every format")}
  <div class="su">
    <div class="cd a">{lockup(cls="su-h")}<label>Horizontal</label></div>
    <div class="cd b">{stacked(cls="su-st")}<label>Stacked</label></div>
    <div class="cd c">{sym(cls="su-sy")}<label>Symbol</label></div>
    <div class="cd d">{wm(cls="su-wm")}<label>Wordmark</label></div>
    <div class="cd e" style="background:{D}">{lockup(dark=True, tagline=True, cls="su-ht")}<label class="lt">Horizontal + descriptor</label></div>
  </div>
''', bg=P))

# 11 ------------------------------------------------------------ clear space
SL.append(slide(11, f'''
  {head("Usage", "Clear space &amp; minimum size")}
  <div class="cs">
    <div class="cs-area"><div class="cs-box">{lockup(cls="cs-logo")}<i class="x x1">x</i><i class="x x2">x</i><i class="x x3">x</i><i class="x x4">x</i></div></div>
    <div class="cs-txt">
      <p>Keep a clear zone of <b>x</b> around the logo, where <b>x</b> equals half the symbol height. No text, images or edges may enter this space.</p>
      <div class="cs-min"><span>Minimum size</span>
        <div class="mins">
          <div>{lockup(cls="m1")}<em>Logo · 120 px / 30 mm</em></div>
          <div>{sym(cls="m2")}<em>Symbol · 24 px / 6 mm</em></div>
        </div>
      </div>
      <div class="cs-min"><span>Placement</span><p>Top-left or bottom-left is preferred. Centre the stacked logo on covers, signage and merchandise.</p></div>
    </div>
  </div>
''', bg='#fff'))

# 12 ------------------------------------------------------------ palette
pal = [('Primary', 'Brick Red', R, '#fff', 'CMYK 0 67 74 30', 40), ('Secondary', 'Mortar', K, '#fff', 'CMYK 0 0 0 83', 25),
       ('Light', 'Terracotta', T, '#fff', 'CMYK 0 45 65 15', 15), ('Deep', 'Fired Clay', F, '#fff', 'CMYK 0 69 76 44', 10),
       ('Tint', 'Plaster', P, K, 'CMYK 0 4 6 2', 10)]
cards = ''.join(f'<div class="pc" style="background:{h};color:{tc}"><div class="pc-t"><span>{role}</span><b>{pct}%</b></div>'
                f'<div><h4>{n}</h4><p>HEX {h}<br>RGB {" ".join(map(str, rgb(h)))}<br>{cm}</p></div></div>' for role, n, h, tc, cm, pct in pal)
SL.append(slide(12, f'''
  {head("Colour palette", "Colours with purpose")}
  <div class="pal">{cards}</div>
  <div class="pal-bar">{''.join(f'<i style="flex:{p};background:{h}"></i>' for _, _, h, _, _, p in pal)}</div>
  <div class="pal-note">Recommended proportion of use across all brand communication. Kiln Black <b>{D}</b> is used for dark backgrounds.</div>
''', bg='#fff'))

# 13 ------------------------------------------------------------ versions
SL.append(slide(13, f'''
  {head("Colour versions", "Positive, reversed &amp; mono")}
  <div class="vs">
    <div style="background:#fff" class="w">{lockup(cls="vl")}<label>Primary · on white</label></div>
    <div style="background:{D}">{lockup(dark=True, cls="vl")}<label class="lt">Reversed · on dark</label></div>
    <div style="background:{R}">{lockup(mono="#fff", cls="vl")}<label class="lt">Mono white · on brand colour</label></div>
    <div style="background:#EEEDEB">{lockup(mono="#000", cls="vl")}<label>Mono black</label></div>
  </div>
''', bg=P))

# 14 ------------------------------------------------------------ misuse
mis = [('Don\'t stretch', f'<div style="transform:scaleX(1.45)">{lockup(cls="ml")}</div>'),
       ('Don\'t recolour', lockup(cls="ml", style="filter:hue-rotate(110deg)")),
       ('Don\'t rotate', f'<div style="transform:rotate(-14deg)">{lockup(cls="ml")}</div>'),
       ('Don\'t add effects', lockup(cls="ml", style="filter:drop-shadow(4px 4px 0 #9ad) drop-shadow(0 0 6px #f0f)")),
       ('Don\'t rearrange', f'<div class="rearr">{wm(cls="ml-w")}{sym(cls="ml-s")}</div>'),
       ('Don\'t use low contrast', f'<div style="background:{T};padding:22px 18px;border-radius:8px">{lockup(cls="ml")}</div>')]
SL.append(slide(14, f'''
  {head("Usage", "Logo misuse")}
  <div class="mis">{''.join(f'<div class="mi"><div class="mi-a">{a}</div><span><i>×</i>{t}</span></div>' for t, a in mis)}</div>
''', bg='#fff'))

# 15 ------------------------------------------------------------ typography
SL.append(slide(15, f'''
  {head("Typography", "Bebas Neue &amp; Manrope")}
  <div class="ty">
    <div class="ty-card dk"><span>Headline</span><div class="ty-aa bebas">Aa</div><h4 class="bebas">Bebas Neue</h4>
      <p class="bebas gl">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0123456789 &amp; @ # %</p></div>
    <div class="ty-card"><span>Body</span><div class="ty-aa man">Aa</div><h4 class="man">Manrope</h4>
      <p class="man gl">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 &amp; @ # %</p></div>
    <div class="ty-scale">
      <div><span>H1 · Bebas Neue · 72 pt</span><p class="s1">MEP procurement, <em>simplified.</em></p></div>
      <div><span>H2 · Manrope Bold · 26 pt</span><p class="s2">Compare suppliers in minutes</p></div>
      <div><span>Body · Manrope Regular · 14 pt</span><p class="s3">Send your BOQ, compare supplier options and move project requirements toward procurement — one workflow.</p></div>
      <div><span>Label · Manrope Bold · 10 pt · tracked</span><p class="s4">ELECTRICAL · PLUMBING · HVAC · MECHANICAL</p></div>
    </div>
  </div>
''', bg=P))

# 16 ------------------------------------------------------------ pattern
SL.append(slide(16, f'''
  {head("Graphic language", "A wall you can build with", dark=True)}
  <div class="pt">
    <div class="pt1">{wall(560, 520, bw=56, bh=24, gap=7, cols=(R, F, T), weights=(40, 35, 25), seed=16)}<label>Full bond · hoardings, covers</label></div>
    <div class="pt2">{wall(330, 520, bw=40, bh=17, gap=6, cols=(F, R, T, '#3A3230'), weights=(20, 15, 10, 55), seed=5, holes=.15)}<label>Tonal bond · backgrounds</label></div>
    <div class="pt3">
      <div class="pt3a">{wall(330, 250, bw=40, bh=17, gap=6, cols=(R, T), weights=(60, 40), seed=9, holes=.6)}<label>Loose bricks · promos</label></div>
      <div class="pt3b"><div class="prog">{''.join(f'<i class="{"on" if j < 11 else ""}"></i>' for j in range(16))}</div><p>11 of 16 packages sourced</p><label>Brick progress · product UI</label></div>
    </div>
  </div>
''', bg=D, dark=True))

# 17 ------------------------------------------------------------ icons
icons = [('Electrical', '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
         ('Plumbing', '<path d="M12 3s-7 8-7 12a7 7 0 0 0 14 0c0-4-7-12-7-12z"/><path d="M9 15a3 3 0 0 0 3 3"/>'),
         ('HVAC', '<circle cx="12" cy="12" r="2"/>' + ''.join(f'<path transform="rotate({a} 12 12)" d="M12 10c0-5 3-7 5-6s1 5-3 7"/>' for a in (0, 120, 240))),
         ('Mechanical', '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7.5" stroke-dasharray="3 2.9" stroke-width="3.2"/>'),
         ('Fire safety', '<rect x="8" y="9" width="8" height="12" rx="2"/><path d="M12 9V6h4M10 6h2M16 6l2 2"/>'),
         ('Upload BOQ', '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>'),
         ('Delivery', '<path d="M2 7h12v9H2zM14 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>'),
         ('Verified supplier', '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>')]
ic = ''.join(f'<div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="{K}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
             f'<i></i><span>{n}</span></div>' for n, p in icons)
SL.append(slide(17, f'''
  {head("Iconography", "Simple lines, one clay accent")}
  <div class="icg">{ic}</div>
  <div class="ic-rule"><span>1.6 pt stroke</span><span>Rounded caps &amp; joins</span><span>24 px grid</span><span>One terracotta brick as accent</span></div>
''', bg='#fff'))

# 18 ------------------------------------------------------------ letterhead
letter = f'''
<div class="a4">
  <div class="a4-top">{lockup(tagline=True, cls="a4-logo")}<div class="a4-ct">criomep.com<br>info@criomep.com<br>+966 11 XXX XXXX</div></div>
  <div class="a4-meta"><span>Riyadh, 16 October 2026</span><span>Ref: CRM/PRC/2026/0142</span></div>
  <div class="a4-to">Eng. Name Surname<br>Projects Director<br>Client Company<br>Riyadh, Kingdom of Saudi Arabia</div>
  <div class="a4-sub">Subject: Quotation summary — MEP package, Tower Project Phase 2</div>
  <div class="a4-body">
    <p>Dear Eng. Name,</p>
    <p>Thank you for sharing your bill of quantities with Criomep. We have compared offers from verified suppliers across the electrical, plumbing and HVAC packages and attached a side-by-side summary for your review.</p>
    <p>All quotations include delivery to site in Riyadh and are valid for 30 days. Our procurement team is available to arrange samples, technical submittals and staged deliveries to match your programme.</p>
    <p>We look forward to building this project with you — brick by brick.</p>
    <p class="sig">Sincerely,<br><b>Name Surname</b><br>Procurement Manager</p>
  </div>
  <div class="a4-foot"><span>Criomep · Riyadh, Kingdom of Saudi Arabia</span><span>CR No. XXXXXXXXXX · VAT No. XXXXXXXXXXXXXXX</span></div>
  <div class="a4-strip">{wall(420, 12, bw=26, bh=5, gap=2, cols=(R, F, T), seed=3, rx=1)}</div>
</div>'''
env = f'''<div class="env"><div class="env-flap"></div>{lockup(cls="env-logo")}<div class="env-addr">Eng. Name Surname<br>Client Company<br>Riyadh, KSA</div><div class="env-strip"></div></div>'''
SL.append(slide(18, f'''
  {head("Stationery · Mockup 01", "Letterhead", sub="A4 · 210 × 297 mm · with DL envelope")}
  <div class="lh-stage">
    <div class="lh-back"></div>
    {letter}
    {env}
    <div class="pen"></div>
  </div>
  <div class="lh-spec">
    <div><span>Logo</span>Horizontal + descriptor, 48 mm wide, 15 mm from top and left edge.</div>
    <div><span>Type</span>Manrope Regular 9.5 / 15 pt body, Manrope Bold for subject lines.</div>
    <div><span>Footer</span>Legal details in Ash, finished with a three-tone brick course.</div>
  </div>
''', bg=P))

# 19 ------------------------------------------------------------ business cards
SL.append(slide(19, f'''
  {head("Stationery · Mockup 02", "Business cards", sub="85 × 55 mm · 400 gsm uncoated, double-sided", dark=True)}
  <div class="bc-stage">
    <div class="bcd bc-f1" style="background:{R}">{wall(340, 220, bw=34, bh=14, gap=4, cols=(F, '#A33428', R), weights=(40, 30, 30), seed=12, cls="bc-tex")}{lockup(mono="#fff", cls="bc-lg")}</div>
    <div class="bcd bc-b1"><div class="bc-sy">{sym()}</div><div class="bc-n"><b>Name Surname</b><span>Procurement Manager</span></div>
      <div class="bc-c"><span><i></i>+966 5X XXX XXXX</span><span><i></i>name@criomep.com</span><span><i></i>criomep.com</span><span><i></i>Riyadh, Saudi Arabia</span></div><div class="bc-edge"></div></div>
    <div class="bcd bc-f2" style="background:{D}">{lockup(dark=True, tagline=True, cls="bc-lg2")}</div>
    <div class="bcd bc-b2" style="background:{P}">{sym(cls="bc-big")}</div>
  </div>
''', bg='#2A2422', dark=True))

# 20 ------------------------------------------------------------ ID card
qr_r = random.Random(4)
qr = ''
for yy in range(21):
    for xx in range(21):
        fin = any(x0 <= xx < x0 + 7 and y0 <= yy < y0 + 7 for x0, y0 in ((0, 0), (14, 0), (0, 14)))
        if fin:
            lx, ly = (xx % 7 if xx < 7 else (xx - 14) % 7), (yy % 7 if yy < 7 else (yy - 14) % 7)
            on = lx in (0, 6) or ly in (0, 6) or (2 <= lx <= 4 and 2 <= ly <= 4)
        else:
            on = qr_r.random() < .45
        if on:
            qr += f'<rect x="{xx}" y="{yy}" width="1" height="1" fill="{K}"/>'
bars = ''.join(f'<rect x="{x}" y="0" width="{w}" height="20" fill="{K}"/>' for x, w in
               [(i * 3 + random.Random(i).choice([0, .5]), random.Random(i * 7).choice([1, 1.5, .6])) for i in range(46)])
lan = f'''<svg class="lanyard" viewBox="0 0 300 260" preserveAspectRatio="none"><defs><pattern id="lt" width="70" height="26" patternUnits="userSpaceOnUse">
  <rect width="70" height="26" fill="{R}"/><g transform="translate(8 18) scale(.24)"><path fill="#fff" d="{D_CRIO}"/><path fill="#FFD9C9" d="{D_MEP}"/></g></pattern></defs>
  <path d="M20 0 L120 230 L150 230 L60 0Z" fill="url(#lt)"/><path d="M280 0 L180 230 L150 230 L240 0Z" fill="url(#lt)"/>
  <path d="M20 0 L120 230 L150 230 L60 0Z M280 0 L180 230 L150 230 L240 0Z" fill="#000" opacity=".12"/></svg>'''
idf = f'''<div class="idc front">
  <div class="id-top">{wall(300, 140, bw=36, bh=14, gap=4, cols=(F, '#A33428', R, T), weights=(35, 25, 30, 10), seed=20, cls="id-tex")}<div class="slot"></div>{lockup(mono="#fff", cls="id-lg")}</div>
  <div class="id-photo"><svg viewBox="0 0 100 100"><rect width="100" height="100" fill="#EADBD2"/><circle cx="50" cy="40" r="18" fill="#C9AFA3"/><path d="M14 100c4-24 20-34 36-34s32 10 36 34z" fill="#C9AFA3"/></svg></div>
  <div class="id-name">Name Surname</div><div class="id-role">Procurement Manager</div>
  <div class="id-row"><div><span>ID No.</span><b>CRM-0142</b></div><div><span>Dept.</span><b>Procurement</b></div><div><span>Valid</span><b>12 / 2027</b></div></div>
  <div class="id-bot"><svg viewBox="0 0 140 20" preserveAspectRatio="none">{bars}</svg></div>
</div>'''
idb = f'''<div class="idc back">
  <div class="slot dk"></div>
  {sym(cls="idb-sym")}
  <div class="idb-qr"><svg viewBox="-1 -1 23 23"><rect x="-1" y="-1" width="23" height="23" fill="#fff"/>{qr}</svg></div>
  <p>This card is the property of Criomep and must be worn visibly on all project sites and offices.</p>
  <p class="ret">If found, please return to:<br><b>Criomep · Riyadh, Kingdom of Saudi Arabia</b><br>+966 11 XXX XXXX · criomep.com</p>
  <div class="idb-strip">{wall(300, 16, bw=30, bh=6, gap=3, cols=(R, F, T), seed=7, rx=1)}</div>
</div>'''
SL.append(slide(20, f'''
  {head("Identity · Mockup 03", "Employee ID card", sub="CR80 · 54 × 86 mm portrait · PVC with lanyard")}
  <div class="id-stage">
    <div class="id-wrap w1">{lan}<div class="clip"></div>{idf}</div>
    <div class="id-wrap w2"><div class="clip"></div>{idb}</div>
    <div class="id-notes">
      <div><span>Front</span>Brick-textured header with reversed logo, photo, name, role and ID details.</div>
      <div><span>Back</span>Symbol, verification QR code, site-safety note and return address.</div>
      <div><span>Lanyard</span>20 mm Brick Red strap with repeating CRIOMEP wordmark.</div>
      <div><span>Visitor &amp; contractor</span>Same layout; header switches to Mortar or Terracotta for quick recognition on site.</div>
    </div>
  </div>
''', bg=P))

# 21 ------------------------------------------------------------ app & mobile
SL.append(slide(21, f'''
  {head("Digital · Mockup 04", "App icon &amp; mobile")}
  <div class="ap">
    <div class="ap-ic">
      <div class="aic big" style="background:{D}">{sym()}</div>
      <div class="aic-row"><div class="aic m" style="background:{R}">{sym(a="#fff", b="#FFD9C9", c="#F4A98A")}</div><div class="aic m" style="background:{P}">{sym()}</div><div class="aic s" style="background:{D}">{sym()}</div><div class="aic xs" style="background:{D}">{sym()}</div></div>
      <p>The symbol works as a standalone app icon, favicon and social avatar — legible down to 24 px.</p>
    </div>
    <div class="ph p1"><div class="scr" style="background:{D}"><div class="spl">{sym(cls="spl-s")}{wm(c1="#fff", c2=T, cls="spl-w")}{tag("rgba(255,255,255,.6)", cls="spl-t")}</div></div></div>
    <div class="ph p2"><div class="scr" style="background:#fff">
      <div class="mt">{lockup(cls="mt-l")}<i></i></div>
      <div class="mh"><small>Active project</small><b>Tower Project — Phase 2</b><div class="prog sm">{''.join(f'<i class="{"on" if j < 11 else ""}"></i>' for j in range(16))}</div><span>11 of 16 packages sourced</span></div>
      <div class="mc"><div><b>14</b><span>Quotes</span></div><div><b>6</b><span>Orders</span></div><div><b>3</b><span>Deliveries</span></div></div>
      <div class="ml2"><div><i style="background:{R}"></i><b>HVAC ducting</b><em>3 quotes</em></div><div><i style="background:{T}"></i><b>LV cables</b><em>Ordered</em></div><div><i style="background:{F}"></i><b>PPR pipes</b><em>Delivered</em></div></div>
      <div class="mb">Upload BOQ</div>
    </div></div>
  </div>
''', bg=P))

# 22 ------------------------------------------------------------ website
SL.append(slide(22, f'''
  {head("Digital · Mockup 05", "Website")}
  <div class="br">
    <div class="br-bar"><i></i><i></i><i></i><span>criomep.com</span></div>
    <div class="br-nav">{lockup(cls="br-lg")}<div class="br-links"><span>Categories</span><span>How it works</span><span>Suppliers</span><span>Projects</span></div><b>Upload BOQ</b></div>
    <div class="br-hero">
      <div class="br-wall">{wall(700, 440, bw=58, bh=24, gap=8, cols=('#2A2422', '#2F2826', F, R, T), weights=(34, 34, 14, 10, 8), seed=22, holes=.18)}</div>
      <div class="br-txt"><div class="kick">Saudi Arabia · MEP marketplace</div><h3>MEP procurement,<br><em>simplified.</em></h3>
        <p>Send your BOQ, compare supplier options and procure electrical, plumbing, HVAC and mechanical products.</p>
        <div class="ctas"><b>Send your requirement</b><span>Explore categories</span></div></div>
      {sym(cls="br-sym")}
    </div>
    <div class="br-cats">{''.join(f'<div><svg viewBox="0 0 24 24" fill="none" stroke="{K}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{p}</svg>{n}</div>' for n, p in icons[:5])}</div>
  </div>
''', bg='#fff'))

# 23 ------------------------------------------------------------ signage
SL.append(slide(23, f'''
  {head("Environment · Mockup 06", "Signage &amp; site hoarding", dark=True)}
  <div class="sg">
    <div class="sg-fac">
      <div class="fac-wall"></div>
      <div class="fac-sign">{lockup(dark=True, cls="fac-lg")}</div>
      <div class="fac-glass"><i></i><i></i><i></i><i></i></div>
      <div class="fac-door"></div>
      <div class="fac-ground"></div>
      <label>Office façade · back-lit fascia sign</label>
    </div>
    <div class="sg-tot">
      <div class="tot-sky"></div>
      <div class="totem"><div class="tot-top">{sym(cls="tot-sym")}</div>{wm(c1="#fff", c2=T, cls="tot-wm")}<div class="tot-dir"><span>Reception →</span><span>Warehouse ↑</span><span>Deliveries ←</span></div></div>
      <div class="tot-ground"></div>
      <label>Wayfinding totem</label>
    </div>
    <div class="sg-hd">
      {wall(1300, 200, bw=60, bh=26, gap=8, cols=(R, F, T), weights=(40, 35, 25), seed=23, cls="hd-wall")}
      <div class="hd-panel">{lockup(tagline=True, cls="hd-lg")}<div class="hd-msg"><b>Building Saudi Arabia, brick by brick.</b><span>All MEP materials for this site supplied via criomep.com</span></div></div>
      <label>Construction-site hoarding · 2.4 m high</label>
    </div>
  </div>
''', bg=D, dark=True))

# 24 ------------------------------------------------------------ fleet, merch, social
van = f'''<svg class="van" viewBox="0 0 640 300">
  <ellipse cx="320" cy="282" rx="300" ry="12" fill="#000" opacity=".2"/>
  <path d="M30 56 Q30 36 52 36 H430 Q450 36 455 56 L470 250 H30 Z" fill="#fff"/>
  <path d="M455 66 H528 Q560 66 576 98 L610 170 Q618 186 618 205 V250 H470 Z" fill="#fff"/>
  <path d="M478 84 H524 Q546 84 556 104 L582 158 H478 Z" fill="{D}" opacity=".88"/>
  <g clip-path="url(#vc)"><clipPath id="vc"><path d="M30 196 H618 V250 H30Z"/></clipPath>
  <g transform="translate(30 196)">{''.join(f'<rect x="{x * 30 - (15 if r % 2 else 0)}" y="{r * 14}" width="27" height="11" rx="2" fill="{(R, F, T)[(x + r) % 3]}"/>' for r in range(4) for x in range(21))}</g></g>
  <g transform="translate(64 70) scale(1.05)">{rects()}</g>
  <g transform="translate(176 156) scale(.95)"><path fill="{K}" d="{D_CRIO}"/><path fill="{R}" d="{D_MEP}"/></g>
  <text x="178" y="182" font-family="Manrope" font-weight="700" font-size="13" fill="{G}" letter-spacing="2.4">MEP PROCUREMENT, SIMPLIFIED · CRIOMEP.COM</text>
  <circle cx="130" cy="252" r="34" fill="#151211"/><circle cx="130" cy="252" r="14" fill="#BDB3AE"/>
  <circle cx="520" cy="252" r="34" fill="#151211"/><circle cx="520" cy="252" r="14" fill="#BDB3AE"/>
  <rect x="604" y="196" width="16" height="10" rx="3" fill="{T}"/></svg>'''
hat = f'''<svg class="hat" viewBox="0 0 320 220"><defs><radialGradient id="hg" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#ECE6E2"/><stop offset="1" stop-color="#CFC4BE"/></radialGradient></defs>
  <ellipse cx="160" cy="196" rx="140" ry="14" fill="#000" opacity=".18"/>
  <path d="M30 170 Q160 205 290 170 L292 182 Q160 214 28 182Z" fill="#E2DAD5"/>
  <path d="M58 172 Q58 52 160 44 Q262 52 262 172 Q160 192 58 172Z" fill="url(#hg)"/>
  <path d="M146 46 Q160 42 174 46 L176 176 Q160 178 144 176Z" fill="#E4DCD7"/>
  <g transform="translate(92 92) scale(.62)">{rects()}</g></svg>'''
mug = f'''<svg class="mug" viewBox="0 0 220 220"><ellipse cx="100" cy="206" rx="80" ry="9" fill="#000" opacity=".18"/>
  <path d="M168 80 q40 0 40 36 t-40 36" fill="none" stroke="{F}" stroke-width="14"/>
  <path d="M30 40 V184 Q30 204 100 204 Q170 204 170 184 V40Z" fill="{R}"/>
  <path d="M30 40 V184 Q30 204 100 204 Q170 204 170 184 V40Z" fill="url(#mg)"/>
  <defs><linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".25"/><stop offset=".35" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient></defs>
  <ellipse cx="100" cy="40" rx="70" ry="13" fill="#9C3227"/><ellipse cx="100" cy="42" rx="62" ry="9" fill="#3A1A14"/>
  <g transform="translate(70 80) scale(.72)">{rects("#fff", "#FFD9C9", "#F4A98A")}</g></svg>'''
SL.append(slide(24, f'''
  {head("Brand in the world · Mockup 07", "Fleet, merchandise &amp; social")}
  <div class="bt">
    <div class="bt-van">{van}<label>Delivery fleet</label></div>
    <div class="bt-hat">{hat}<label>Site hard hat</label></div>
    <div class="bt-mug">{mug}<label>Mug</label></div>
    <div class="bt-soc">
      <div class="ig"><div class="ig-h"><div class="av">{sym()}</div><b>criomep</b><span>MEP procurement, simplified</span></div>
        <div class="ig-g">
          <div style="background:{R}">{sym(a="#fff", b="#FFD9C9", c="#F4A98A", cls="ig-s")}</div>
          <div style="background:{P}"><b>BOQ in.<br><em>Quotes out.</em></b></div>
          <div style="background:{D}">{wall(160, 160, bw=26, bh=11, gap=3, cols=('#2F2826', F, R, T), weights=(50, 20, 20, 10), seed=6)}<span>500+<br>suppliers</span></div>
        </div></div>
      <label>Social media</label>
    </div>
  </div>
''', bg=P))

# 25 ------------------------------------------------------------ closing
SL.append(slide(25, f'''
  <div class="end-wall">{wall(1440, 810, bw=70, bh=30, gap=9, cols=('#262120', '#2A2422', '#2E2725'), weights=(1, 1, 1), seed=99, rx=5, holes=.06)}</div>
  <div class="end-in">
    {sym(cls="end-sym")}
    {wm(c1="#fff", c2=T, cls="end-wm")}
    {tag("rgba(255,255,255,.72)", cls="end-tag")}
    <div class="end-meta">Option 40 · Brick</div>
    <p>The most construction-rooted option — it looks built, not drawn.</p>
    <div class="end-thx">Thank you</div>
  </div>
  <div class="end-dots">{''.join(f'<i style="background:{x}"></i>' for x in (R, K, T, F, P))}</div>
''', bg=D, footer=False, cls='end'))

assert len(SL) == TOTAL, len(SL)
css = open(os.path.join(S, 'deck2.css')).read()
open(os.path.join(OUT, 'deck.html'), 'w').write(
    f'<!doctype html><html><head><meta charset="utf-8"><title>Criomep — Option 40 Brick · Brand Presentation</title>'
    f'<style>{css}</style></head><body>{"".join(SL)}</body></html>')
print('ok', len(SL))
