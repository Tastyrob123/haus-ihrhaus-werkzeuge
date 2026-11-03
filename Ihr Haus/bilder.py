#!/usr/bin/env python3
"""Rechnet die Bilder von «Ihr Haus» aus der Bildwelt der Tasty-Studios-Seite (_quelle/haus/gen) in Webgrössen:
assets/img/<name>-<breite>.webp (800 / 1400 / 2400, nie grösser als das Original) + assets/img/bilder.json (Breiten, Seitenverhältnis).
python3 bilder.py"""
import os, json
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.expanduser('~/Desktop/Website-Projekte/Tasty Studios Website/_quelle/haus/gen')
OUT = os.path.join(HIER, 'assets', 'img'); os.makedirs(OUT, exist_ok=True)
NAMEN = ['s-aussen-wasser', 'empfang', 's-eingang', 's-lobby', 's-schluesselbrett', 's-fensterplatz',
         'z-speicherzimmer', 'd-bett', 'z-leseecke', 'zimmer', 'z-schreibtisch', 'z-bettdetail', 'z-kranzimmer', 'z-wanne', 'z-morgen',
         'z-dachsuite', 'z-bad', 'z-minibar', 'r-gastraum', 'r-brot', 'r-krabben', 'r-zander', 'r-lamm', 'r-gruetze', 'r-pass', 'r-weinkeller',
         'r-tisch-fenster', 'm-schluessel', 'm-papier', 'm-seife', 'm-nebel', 'm-material', 's-hundeplatz', 's-dachboden', 's-bibliothek', 'bar', 'r-zutaten', 'r-franzbroetchen', 'a-speicherstadt', 'a-faehre', 'a-koffer', 'a-raeder', 'a-anleger', 'aussen', 'm-backstein']
J = {}
for n in NAMEN:
    im = Image.open(os.path.join(GEN, n + '.png')).convert('RGB'); w, h = im.size
    br = [b for b in (800, 1400, 2400) if b < w] + ([w] if w < 2400 else [])
    br = sorted(set(min(b, w) for b in br))
    for b in br:
        z = os.path.join(OUT, f'{n}-{b}.webp')
        if not os.path.exists(z):
            im.resize((b, round(h * b / w)), Image.LANCZOS).save(z, 'WEBP', quality=82, method=6)
    J[n] = {'w': w, 'h': h, 'b': br}
json.dump(J, open(os.path.join(OUT, 'bilder.json'), 'w'), indent=1)
print(len(J), 'Bilder', round(sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e6, 1), 'MB')

# Auftakt und Schluss mit weicher Abdunklung im Bild selbst (nie als Fläche über dem bewegten Foto, Regel 55d)
from PIL import ImageDraw, ImageFilter
def dunkel(n, ziel, links=.62, unten=.55):
    im = Image.open(os.path.join(GEN, n + '.png')).convert('RGB'); w, h = im.size
    m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    d.ellipse((-w * .45, h * .18, w * links, h * 1.45), fill=int(255 * unten))
    m = m.filter(ImageFilter.GaussianBlur(w * .09))
    schwarz = Image.new('RGB', (w, h), (8, 10, 16))
    out = Image.composite(schwarz, im, m)
    br = [800, 1400, 2400] if w >= 2400 else [800, 1400, w]
    for b in br:
        out.resize((b, round(h * b / w)), Image.LANCZOS).save(os.path.join(OUT, f'{ziel}-{b}.webp'), 'WEBP', quality=84, method=6)
    J[ziel] = {'w': w, 'h': h, 'b': br}
dunkel('s-aussen-wasser', 'hero')
dunkel('aussen', 'schluss', links=.7, unten=.6)
json.dump(J, open(os.path.join(OUT, 'bilder.json'), 'w'), indent=1)
print('Auftakt und Schluss gerechnet')

# Handy-Auftakt: Hochformat aus derselben Aufnahme, unten kräftiger abgedunkelt, damit Titel und Satz frei stehen
def hoch(n, ziel, mitte=.42):
    im = Image.open(os.path.join(GEN, n + '.png')).convert('RGB'); w, h = im.size
    cw = int(h * .72); x = max(0, min(w - cw, int(w * mitte - cw / 2)))
    im = im.crop((x, 0, x + cw, h)); w, h = im.size
    m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    for y in range(h):
        t = max(0, (y / h - .3) / .7); d.line([(0, y), (w, y)], fill=int(255 * min(.9, t ** .85 * 1.05)))
    out = Image.composite(Image.new('RGB', (w, h), (8, 10, 16)), im, m)
    for b in (600, 1000):
        out.resize((b, round(h * b / w)), Image.LANCZOS).save(os.path.join(OUT, f'{ziel}-{b}.webp'), 'WEBP', quality=84, method=6)
    J[ziel] = {'w': w, 'h': h, 'b': [600, 1000]}
hoch('s-aussen-wasser', 'hero-m')
json.dump(J, open(os.path.join(OUT, 'bilder.json'), 'w'), indent=1)
print('Handy-Auftakt gerechnet')
