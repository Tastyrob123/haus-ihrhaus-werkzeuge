#!/usr/bin/env python3
"""Die Marke von «Ihr Haus»: Zeichen, Wortmarke als Pfade aus der Schrift, Logo-Fassungen, Tapete, Farbkarten,
und das Markenbuch als Seite im Kleid des Hauses (marke/markenbuch.html, druckbar als PDF). Fakten aus haus.py.
Das Zeichen liegt in Fassungen vor (FASSUNGEN); gewählt wird über haus.MARKE['zeichen_nr']. Solange nichts gewählt ist,
zeigt das Markenbuch unten links ein Schild und wechselt die Fassung mit ← → in allen Stellen zugleich (Robert 02.11.2026:
«ich mag dieses Logo nicht»). Schreibt assets/marke/*.svg + marke/markenbuch.html.   python3 marke.py"""
import os, json, html, urllib.parse
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import haus as H
HIER = os.path.dirname(os.path.abspath(__file__))
MK = os.path.join(HIER, 'assets', 'marke'); os.makedirs(MK, exist_ok=True)
os.makedirs(os.path.join(HIER, 'marke'), exist_ok=True)
B = json.load(open(os.path.join(HIER, 'assets', 'img', 'bilder.json')))
e = html.escape
F = {n: c for n, c, _ in H.MARKE['farben']}
ZN = H.MARKE.get('zeichen_nr')   # None = noch nicht gewählt → Schild zum Durchklicken

# ------------------------------------------------------------------ Schrift → Pfade
_FONTS = {}
def font(name):
    if name not in _FONTS: _FONTS[name] = TTFont(os.path.join(HIER, 'assets', 'fonts', name))
    return _FONTS[name]
def text_pfad(schrift, text, groesse, sperrung=0.0):
    """Zeichenkette als SVG-Pfad (Buchstaben als Umrisse), Sperrung in em. Gibt Pfad, Breite, Höhe über und unter der Grundlinie."""
    f = font(schrift); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    s = groesse / f['head'].unitsPerEm; x = 0; teile = []; oben = 0; unten = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None: x += groesse * .28; continue
        pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, 0))); d = pen.getCommands()
        if d: teile.append(d)
        bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds: oben = max(oben, bp.bounds[3] * s); unten = min(unten, bp.bounds[1] * s)
        x += gs[g].width * s + sperrung * groesse
    return ' '.join(teile), x - sperrung * groesse, oben, unten
def svg_text(schrift, text, groesse, sperrung, name, rand=2):
    d, w, o, u = text_pfad(schrift, text, groesse, sperrung)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-rand} {-o - rand} {w + 2 * rand} {o - u + 2 * rand}" role="img" aria-label="{e(name)}">'
            f'<path fill="currentColor" d="{d}"/></svg>'), w, o, u
CG, IS = 'CormorantGaramond-500.woff2', 'InstrumentSans-normal-400_600.woff2'
def mitte(schrift, text, groesse, sperrung=0.0, cy=50):
    """Text als Pfad, in einem 100×100-Feld waagerecht und senkrecht mittig (auf die Versalhöhe bezogen)"""
    d, w, o, u = text_pfad(schrift, text, groesse, sperrung)
    return f'<path fill="currentColor" transform="translate({(100 - w) / 2:.2f} {cy + o / 2:.2f})" d="{d}"/>', w, o

# ------------------------------------------------------------------ Die Fassungen des Zeichens (alle im Feld 0 0 100 100, Farbe = currentColor, __D__ = Strichstärke)
L = 'fill="none" stroke="currentColor" stroke-width="__D__" stroke-linecap="round" stroke-linejoin="round"'
S = 'fill="currentColor"'
def P(*pts): return 'M' + ' L'.join(f'{x} {y}' for x, y in pts) + ' Z'
# Richtige Bildzeichen aus der Welt des Hauses (Robert 02.11.2026: «ein richtiges Logo, keine Buchstaben»), als Silhouetten gebaut
def f_kran():
    return (f'<path {S} d="M16 88h48v4H16z {P((22,88),(28,88),(36,52),(32,52))} {P((52,52),(48,52),(56,88),(62,88))} M26 42h32v12H26z {P((44,46),(91,9),(94,13),(50,50))} M16 44h12v4H16z"/>'
            f'<g {L}><path d="M89 15v22"/><path d="M89 37c0 6-8 6-8 1"/></g>')
def f_laterne():
    return (f'<path {S} fill-rule="evenodd" d="M34 24h32L50 11z M44 24h12v3H44z M36 27h28l-3 37H39z M50 37c7 9 7 15 0 20c-7-5-7-11 0-20z M33 64h34v5H33z M47 69h6v12h-6z M40 81h20v4H40z"/>'
            f'<circle cx="50" cy="8.5" r="2.4" {S}/>')
def f_poller():
    return (f'<path {S} d="M30 44a20 11 0 0 1 40 0v5H30z M36 49h28v8H36z {P((34,57),(66,57),(68,88),(32,88))}"/>'
            f'<g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><path d="M21 53c8-9 50-9 58 0"/><path d="M24 62c8 7 44 7 52 0"/></g>')
def f_haken():
    return (f'<g fill="none" stroke="currentColor" stroke-linecap="round"><path stroke-width="9" d="M50 18v24c0 24-30 24-30 4c0-9 7-14 13-14"/>'
            f'<circle cx="50" cy="11" r="6" stroke-width="5"/></g>')
def f_barkasse():
    return (f'<path {S} fill-rule="evenodd" d="M10 68h80l-8 16H18z M30 52a2 2 0 0 1 2-2h36a2 2 0 0 1 2 2v16H30z M36 55h8v7h-8z M46 55h8v7h-8z M56 55h8v7h-8z M49 30h3v20h-3z M44 36h13v2H44z M62 40h6v10h-6z"/>'
            f'<g {L}><path d="M14 91h72"/></g>')
def f_giebel():
    return (f'<path {S} fill-rule="evenodd" d="M18 92V48L50 16l32 32v44z M44 92V64a6 6 0 0 1 12 0v28z M30 58h7v9h-7z M63 58h7v9h-7z M46 40h8v9h-8z"/>'
            f'<g {L}><path d="M50 16h42"/><circle cx="92" cy="16" r="3"/><path d="M92 19v41"/><path d="M92 60c0 5-7 5-7 1"/></g>')
def f_ladebalken():
    return (f'<path {S} d="M24 14h6v74h-6z M24 14h56v6H24z {P((30,52),(30,60),(70,20),(64,20))}"/>'
            f'<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><circle cx="80" cy="17" r="6"/><path d="M80 23v39"/><path d="M80 62c0 8-10 8-10 1c0-4 3-6 5-6"/></g>')
def f_luke():
    return f'<path {S} fill-rule="evenodd" d="M28 14h44v72H28z M40 86V38a10 10 0 0 1 20 0v48z M34 22h32v4H34z"/>'

FASSUNGEN = [
 ('Der Kran', 'Der Hafenkran, als Silhouette.', 'Die Kräne stehen in jedem Fenster des Hauses. Portal, Kanzel, Ausleger und ein Haken am Seil, aus einer Form geschnitten. Trägt in 18 px wie auf dem Aushang.', f_kran),
 ('Die Laterne', 'Die Lampe am Eingang, mit der Flamme als Aussparung.', '«Die Lampe am Eingang brennt, wenn Sie ankommen.» Das Zeichen ist dieser Satz: die Laterne an der Tür, die Flamme bleibt frei.', f_laterne),
 ('Der Poller', 'Der Poller am Kai, mit dem Tau.', 'Das Ding, an dem man festmacht. Steht vor dem Haus am Anleger. Schwer, ruhig, zwei Schläge Tau darum.', f_poller),
 ('Der Haken', 'Der Kranhaken, allein.', 'Das Werkzeug des Speichers: der Haken am Seil, der die Säcke in die Böden hob. Eine Form, kein Beiwerk.', f_haken),
 ('Die Barkasse', 'Das Hafenschiff, mit der Wasserlinie.', 'Mit der Barkasse kommt man am Anleger an. Rumpf, Kajüte, Mast, darunter eine Linie Wasser.', f_barkasse),
 ('Der Speicher', 'Der Giebel als Silhouette, mit der Winde.', 'Das Haus selbst, als Stempel: der Giebel, die Luke, drei Fenster, am First die Winde mit Seil und Haken.', f_giebel),
 ('Der Ladebalken', 'Die Winde ohne das Haus.', 'Der Balken an der Wand, die Strebe, die Rolle, das Seil, der Haken. Das Stück des Speichers, das nie abgebaut wurde.', f_ladebalken),
 ('Die Luke', 'Die Ladeluke, als Aussparung im Stein.', 'Ein Stein, darin der Bogen der Ladeluke. Das Zeichen für eine Tür, die zum Wasser aufgeht.', f_luke),
]
# Gezeichnete Entwürfe (logo_vektor.py) ersetzen die Handformen, sobald sie vorliegen
_E = os.path.join(MK, 'entwuerfe.json')
if os.path.exists(_E):
    FASSUNGEN = [(x['name'], x['satz'], x['erkl'], (lambda i=x['innen']: i)) for x in json.load(open(_E))]
def innen(nr, dicke):
    return FASSUNGEN[nr][3]().replace('__D__', str(dicke))
def zeichen_svg(dicke=2.4, cls='', nr=None):
    nr = ZN if nr is None else nr
    if nr is None: nr = 0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{e(FASSUNGEN[nr][0])}"'
            f'{" class=" + chr(34) + cls + chr(34) if cls else ""}>{innen(nr, dicke)}</svg>')
def slot(dicke=2.4, cls='', wrap='span'):
    """Zeichen an dieser Stelle, mit Strichstärke, damit das Schild es austauschen kann"""
    return f'<{wrap} class="zslot{(" " + cls) if cls else ""}" data-d="{dicke}">{zeichen_svg(dicke)}</{wrap}>'

# ------------------------------------------------------------------ Wortmarke und Unterzeile
WM, wm_w, wm_o, wm_u = svg_text(CG, 'IHR HAUS', 100, .3, 'Ihr Haus')
UZ, uz_w, uz_o, uz_u = svg_text(IS, 'AM HAFEN · HAMBURG', 100, .34, 'Am Hafen, Hamburg')
open(os.path.join(MK, 'wortmarke.svg'), 'w').write(WM)
open(os.path.join(MK, 'unterzeile.svg'), 'w').write(UZ)

def logo_svg(art='gestapelt', nr=None):
    """gestapelt: Zeichen über Wortmarke über Unterzeile · zeile: Zeichen links, Wortmarke und Unterzeile rechts"""
    nr = (ZN if nr is None else nr); nr = 0 if nr is None else nr
    wm_d, w1, o1, u1 = text_pfad(CG, 'IHR HAUS', 100, .3)
    uz_d, w2, o2, u2 = text_pfad(IS, 'AM HAFEN · HAMBURG', 34, .34)
    z = '__Z__' if nr == '__V__' else innen(nr, 2.4)
    if art == 'gestapelt':
        W = max(w1, w2) + 40
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 290" role="img" aria-label="Ihr Haus, am Hafen, Hamburg">'
                f'<g transform="translate({(W - 100) / 2:.1f} 0)">{z}</g>'
                f'<path fill="currentColor" transform="translate({(W - w1) / 2:.1f} 195)" d="{wm_d}"/>'
                f'<path fill="currentColor" transform="translate({(W - w2) / 2:.1f} 250)" d="{uz_d}"/></svg>')
    W = 120 + max(w1, w2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 110" role="img" aria-label="Ihr Haus, am Hafen, Hamburg">'
            f'<g transform="translate(0 5)">{z}</g>'
            f'<path fill="currentColor" transform="translate(120 62)" d="{wm_d}"/>'
            f'<path fill="currentColor" transform="translate(120 100)" d="{uz_d}"/></svg>')
def lslot(art, cls=''):
    return f'<span class="lslot{(" " + cls) if cls else ""}" data-art="{art}">{logo_svg(art)}</span>'

# ------------------------------------------------------------------ Tapete: Backstein im Läuferverband, Ton in Ton, in jeder vierten Reihe das Zeichen
def tapete_svg(nr, grund=F['Nacht'], linie='#ffffff', deck=.05, zeichen=.09):
    r = []
    for i in range(8):
        y = i * 30; off = 60 if i % 2 else 0
        r.append(f'<path d="M0 {y}h480" stroke="{linie}" stroke-opacity="{deck}"/>')
        for x in range(off - 120, 481, 120): r.append(f'<path d="M{x} {y}v30" stroke="{linie}" stroke-opacity="{deck}"/>')
    r.append(f'<g transform="translate(190 60) scale(.5)" color="{linie}" opacity="{zeichen}">{'__Z__' if nr == '__V__' else innen(nr, 2.4)}</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 240" width="480" height="240"><rect width="480" height="240" fill="{grund}"/>{"".join(r)}</svg>'
def daten_url(svg): return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe="/:=,-.' ") + '")'

# ------------------------------------------------------------------ Dateien für die gewählte Fassung
n0 = 0 if ZN is None else ZN
open(os.path.join(MK, 'zeichen.svg'), 'w').write(zeichen_svg(2.4, nr=n0))
open(os.path.join(MK, 'logo.svg'), 'w').write(logo_svg('gestapelt', n0))
open(os.path.join(MK, 'logo-zeile.svg'), 'w').write(logo_svg('zeile', n0))
open(os.path.join(MK, 'tapete-nacht.svg'), 'w').write(tapete_svg(n0))
open(os.path.join(MK, 'tapete-leinen.svg'), 'w').write(tapete_svg(n0, F['Leinen'], '#1c2029', .07, .12))

# ------------------------------------------------------------------ Farbkarten
GEMESSEN = {'Nacht': ('#0c1720', 's-aussen-wasser', 'das Wasser vor dem Haus'), 'Leinen': ('#cccac3', 'z-bettdetail', 'das Kissen im Schatten'),
            'Licht': ('#fcb876', 's-aussen-wasser', 'die Fenster am Abend'), 'Messing': ('#b27435', 's-schluesselbrett', 'die Lampe am Schlüsselbrett'),
            'Backstein': ('#9b5c34', 'm-backstein', 'die Fassade im Abendlicht'), 'Flaschengrün': ('#0c2117', 'z-bad', 'die Fliesen im Bad')}
ANTEIL = {'Nacht': 56, 'Leinen': 26, 'Flaschengrün': 10, 'Messing': 5, 'Licht': 2, 'Backstein': 1}
def farben_svg():
    k = []
    for i, (n, c, s) in enumerate(H.MARKE['farben']):
        x = i * 150; hell = n in ('Leinen', 'Licht'); t = '#1c2029' if hell else '#efe7da'
        k.append(f'<rect x="{x}" y="0" width="140" height="140" rx="6" fill="{c}"/><text x="{x + 12}" y="112" font-family="Georgia,serif" font-size="18" fill="{t}">{e(n)}</text>'
                 f'<text x="{x + 12}" y="128" font-family="Helvetica,Arial,sans-serif" font-size="10" letter-spacing="1" fill="{t}" opacity=".8">{c.upper()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 890 140" width="890" height="140">{"".join(k)}</svg>'
open(os.path.join(MK, 'farben.svg'), 'w').write(farben_svg())
open(os.path.join(MK, 'farben.txt'), 'w').write('\n'.join(f'{n}\t{c}\t{s}' for n, c, s in H.MARKE['farben']) + '\n')

# ------------------------------------------------------------------ Das Markenbuch
def img(n, sizes='50vw', alt='', pos=None):
    d = B[n]; br = d['b']; st = f' style="object-position:{pos}"' if pos else ''
    return (f'<img src="../assets/img/{n}-{br[min(1, len(br) - 1)]}.webp" srcset="{", ".join(f"../assets/img/{n}-{b}.webp {b}w" for b in br)}" sizes="{sizes}" '
            f'width="{d["w"]}" height="{d["h"]}" alt="{e(alt)}"{st} loading="lazy" decoding="async">')
def zl(text, cls='t1', tag='h2'):
    return f'<{tag} class="{cls}">' + ''.join(f'<span class="sl"><span style="--i:{i}">{e(x)}</span></span>' for i, x in enumerate(text.split('|'))) + f'</{tag}>'
PFEIL = '<i class="kn__k"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></i>'
def kn(t, href, art='hell', extra=''):
    return f'<a class="kn kn--{art}" href="{href}"{extra}><span>{e(t)}</span>{PFEIL}</a>'
def blatt(nr, kicker, titel, inhalt, grund='nacht', cls=''):
    return f'<section class="blatt blatt--{grund} {cls}" id="b{nr}"><div class="blatt__in"><div class="kopf sw"><small>{nr:02d} · {e(kicker)}</small>{zl(titel)}</div>{inhalt}</div></section>'

m = H.MARKE; fz = FASSUNGEN[n0]
T = []
T.append(f'''<section class="titel" id="oben">
  <div class="titel__in">
    <p class="kicker sw" style="--i:0">Das Markenbuch · November 2026</p>
    <div class="titel__z sw" style="--i:1">{slot(1.6)}</div>
    <h1 class="titel__w sw" style="--i:2">{WM}</h1>
    <p class="titel__u sw" style="--i:3">{UZ}</p>
    <p class="titel__s sw" style="--i:4">Alles, was Ihr Haus erkennbar macht, an einem Ort: das Zeichen, die Wortmarke, die Farben und woher sie kommen, die Schrift, die Tapete, die Bilder und die Bausteine der Website. Damit jedes neue Stück, ob Tischkarte, Aushang oder Seite, aussieht wie aus einem Guss.</p>
    <div class="knoepfe sw" style="--i:5">{kn('Lesen', '#b1', 'hell')}{kn('Als PDF sichern', '#', 'nacht', ' data-druck')}</div>
  </div>
</section>''')
T.append(f'''<section class="fenster sw-feld"><div class="fenster__a"><div class="fenster__i">{img('s-aussen-wasser', '100vw', 'Der Speicher vom Wasser aus', '60% 50%')}</div></div>
<div class="fenster__t">{zl('Ein Speicher|am Hafen.', 'fenster__s', 'p')}<p class="fenster__u">Der erste Satz des Hauses. Er steht auf der Website, auf dem Briefpapier und am Anleger.</p></div></section>''')
T.append(blatt(1, 'Das Zeichen', 'Was das Haus|zeichnet.', f'''
<div class="zwei">
  <div class="text sw"><p class="gross" data-ztext="satz">{e(fz[1])}</p>
  <p data-ztext="erkl">{e(fz[2])}</p>
  <p>Das Zeichen steht immer in der Farbe, die um es herum steht, nie gefüllt, nie mit Schatten. Allein auf dem Schlüsselanhänger, im Siegel, auf der Serviette und als kleines Bild im Browser. Neben der Wortmarke nur, wo Platz für beides ist.</p></div>
  <div class="zeichen-gross sw" style="--i:1">{slot(1.8)}</div>
</div>
<div class="reihe sw" style="--i:2">
  <figure class="probe probe--nacht"><div class="z z--96">{slot(2.4)}</div><figcaption>96 px</figcaption></figure>
  <figure class="probe probe--leinen"><div class="z z--48">{slot(2.8)}</div><figcaption>48 px</figcaption></figure>
  <figure class="probe probe--gruen"><div class="z z--24">{slot(3.6)}</div><figcaption>24 px</figcaption></figure>
  <figure class="probe probe--messing"><div class="z z--18">{slot(4.2)}</div><figcaption>18 px, die kleinste Grösse</figcaption></figure>
</div>
<div class="bild-band sw" style="--i:3"><figure class="rahmen">{img('m-schluessel', '(max-width:900px) 100vw, 33vw', 'Der Zimmerschlüssel mit Lederanhänger')}</figure><figure class="rahmen">{img('m-papier', '(max-width:900px) 100vw, 33vw', 'Briefpapier mit Siegel')}</figure><figure class="rahmen">{img('s-eingang', '(max-width:900px) 100vw, 33vw', 'Der Eingang')}</figure></div>
<p class="unterschrift sw">Wo das Zeichen hinkommt: in den Anhänger geprägt, ins Siegel gedrückt, über die Tür gesetzt.</p>'''))
T.append(blatt(2, 'Die Wortmarke', 'Zwei Wörter,|gesperrt gesetzt.', f'''
<div class="zwei">
  <div class="text sw"><p class="gross">IHR HAUS in Cormorant Garamond, Versalien, um drei Zehntel gesperrt. Darunter in Instrument Sans: AM HAFEN · HAMBURG.</p>
  <p>Die Wortmarke wird nie neu gesetzt, sondern als Datei eingesetzt. Sie steht in Leinen auf Nacht, in Tinte auf Leinen, in Leinen auf Flaschengrün. Nie in Licht, nie in Backstein, nie fett, nie kursiv.</p>
  <p>Die Unterzeile gehört dazu, wo die Wortmarke gross steht: auf der Website, dem Briefpapier, dem Aushang. Auf kleinen Stücken fällt sie weg.</p></div>
  <div class="lockups sw" style="--i:1">
    <figure class="lock lock--nacht"><div class="lock__l">{lslot('gestapelt')}</div><figcaption>Gestapelt: die Hauptfassung</figcaption></figure>
    <figure class="lock lock--leinen"><div class="lock__l lock__l--zeile">{lslot('zeile')}</div><figcaption>In der Zeile: Leiste, Briefkopf</figcaption></figure>
    <figure class="lock lock--gruen"><div class="lock__l lock__l--wm">{WM}</div><figcaption>Nur die Wortmarke: Leiste der Website</figcaption></figure>
    <figure class="lock lock--leinen"><div class="lock__l lock__l--z">{slot(2.4)}</div><figcaption>Nur das Zeichen: Siegel, Anhänger, Serviette</figcaption></figure>
  </div>
</div>
<div class="schutz sw" style="--i:2"><div class="schutz__r"><div class="schutz__l">{lslot('gestapelt')}</div></div><p>Schutzraum: ringsum mindestens die Höhe des Zeichens. Kleinste Grösse: 90 px Breite am Bildschirm, 22 mm im Druck.</p></div>'''))
karten = ''.join(f'''<div class="farbe sw" style="--i:{i}"><div class="farbe__f" style="background:{c}"></div><div class="farbe__t"><b>{e(n)}</b><span>{c.upper()}</span><p>{e(s)}</p></div></div>''' for i, (n, c, s) in enumerate(m['farben']))
balken = ''.join(f'<i style="flex:{ANTEIL[n]};background:{F[n]}" title="{e(n)} {ANTEIL[n]} %"></i>' for n in ANTEIL)
legende = ''.join(f'<span><i style="background:{F[n]}"></i>{e(n)} {ANTEIL[n]} %</span>' for n in ANTEIL)
T.append(blatt(3, 'Die Farben', 'Sechs Töne,|einer trägt.', f'''
<div class="farben">{karten}</div>
<div class="anteil sw"><div class="anteil__b">{balken}</div><div class="anteil__l">{legende}</div>
<p>So verteilen sich die Farben auf einer Seite: Nacht trägt, Leinen antwortet, Flaschengrün gehört nur der Tafel. Licht und Messing sind Linien, Knäufe, kleine Schrift. Backstein kommt aus den Fotos, nie aus der Dose.</p></div>''', 'leinen'))
fund = ''.join(f'''<figure class="fund sw" style="--i:{i}"><div class="rahmen">{img(b, '(max-width:900px) 100vw, 33vw', s)}</div>
<div class="fund__s"><i style="background:{g}"></i><i style="background:{F[n]}"></i></div><figcaption><b>{e(n)}</b> · {e(s)}<br>gemessen {g.upper()}, gesetzt {F[n].upper()}</figcaption></figure>''' for i, (n, (g, b, s)) in enumerate(GEMESSEN.items()))
T.append(blatt(4, 'Woher die Farben kommen', 'Aus den Fotos|gemessen.', f'''
<p class="gross sw">Jede Farbe hat eine Stelle im Haus. Gemessen in den Fotos, dann für den Bildschirm gesetzt: Nacht etwas tiefer als das Wasser, Leinen heller als das Kissen im Schatten, Licht gedämpft, damit es als Linie trägt.</p>
<div class="funde">{fund}</div>'''))
T.append(blatt(5, 'Die Schrift', 'Eine Serife|für den Namen.', f'''
<div class="zwei">
  <div class="text sw"><p class="gross">Cormorant Garamond trägt alles, was gross ist: Wortmarke, Titel, Preise, die Namen der Gänge. Instrument Sans trägt alles, was gelesen wird: Lauftext, Leiste, Knöpfe, Etiketten.</p>
  <p>Beide Schriften liegen als Datei im Haus und werden vom eigenen Server geladen. Lizenz: SIL Open Font License, frei für Web und Druck.</p>
  <dl class="skala"><dt>Titel der Startseite</dt><dd>Cormorant 500 · 150 px am Rechner, 64 px am Handy · Zeilenabstand 0,94</dd>
  <dt>Kapiteltitel</dt><dd>Cormorant 500 · 86 bis 42 px · 1,02</dd><dt>Name eines Zimmers, eines Gangs</dt><dd>Cormorant 500 · 54 bis 23 px</dd>
  <dt>Lauftext</dt><dd>Instrument Sans 400 · 17 px · 1,62</dd><dt>Etikett, Leiste, Knopf</dt><dd>Instrument Sans 500 · 11 bis 14 px · Versalien · gesperrt 0,14 bis 0,3 em</dd></dl></div>
  <div class="specimen sw" style="--i:1">
    <p class="sp-titel">Ein Speicher<br>am Hafen.</p>
    <p class="sp-name">Kranzimmer <span>ab 229 €</span></p>
    <p class="sp-lauf">Zwei hohe Fenster, davor die Kräne, und eine Wanne, von der aus man sie sieht. Unten wird empfangen, oben wird geschlafen.</p>
    <p class="sp-etikett">Anreise · Abreise · Gäste · Zimmer finden</p>
    <p class="sp-nie">Nie fett. <em>Nie kursiv.</em> <u>Nie unterstrichen.</u> NIE ALS LAUFTEXT IN VERSALIEN.</p>
  </div>
</div>''', 'leinen'))
T.append(blatt(6, 'Tapete und Flächen', 'Backstein|im Verband.', f'''
<div class="zwei">
  <div class="text sw"><p class="gross">Die Tapete ist der Läuferverband der Fassade, als feine Fuge, Ton in Ton. In jeder vierten Reihe sitzt klein das Zeichen.</p>
  <p>Sie liegt hinter Flächen ohne Foto: dem Fuss, dem Briefpapier, der Rückseite der Tischkarte, dem Kopf der Werkzeuge. Nie hinter Lauftext, nie hinter einem Foto, nie lauter als fünf Prozent.</p>
  <p>Die Seiten wechseln in diesem Rhythmus: Nacht für Auftakt, Empfang und Anreise, Leinen für die Zimmer, Flaschengrün nur für die Tafel. Eine helle Fläche folgt nie auf eine helle.</p></div>
  <div class="tapeten sw" style="--i:1">
    <div class="tap tap--nacht"><span>Nacht</span></div>
    <div class="tap tap--leinen"><span>Leinen</span></div>
    <div class="tap tap--gruen"><span>Flaschengrün, ohne Tapete</span></div>
  </div>
</div>'''))
bilder = [('s-lobby', 'Die Halle'), ('z-wanne', 'Die Wanne vor dem Fenster'), ('r-pass', 'Der Pass vor dem Service'), ('a-speicherstadt', 'Die Speicherstadt'), ('r-krabben', 'Nordseekrabben'), ('s-hundeplatz', 'Lottes Platz')]
wand = ''.join(f'<figure class="rahmen sw" style="--i:{i}">{img(b, "(max-width:900px) 50vw, 33vw", a)}</figure>' for i, (b, a) in enumerate(bilder))
T.append(blatt(7, 'Die Bilder', 'Die Stunde|vor dem ersten Gast.', f'''
<p class="gross sw">Alle Bilder des Hauses zeigen denselben Moment: Es ist vorbereitet, das Licht ist an, und noch ist niemand da. Film statt Hochglanz, warmes Licht im Dunkeln, der Ort als Held.</p>
<div class="wand">{wand}</div>
<div class="zwei zwei--eng sw">
  <div class="text"><small>So sind die Bilder</small><ul><li>Blaue Stunde oder Abend, eine Lichtquelle mit Richtung</li><li>Korn wie auf Film, echte Schatten, nichts geglättet</li><li>Niemand im Bild; der Gast kann sich hineinsetzen</li><li>Backstein, Eiche, Messing, Leinen, immer das Wasser in der Nähe</li><li>Ein Farbpunkt je Bild: die Kerze, das Fenster, das Glas Wein</li></ul></div>
  <div class="text"><small>So nie</small><ul><li>Kein Mittagslicht, kein Blitz, keine weisse Decke</li><li>Keine Menschen, die in die Kamera schauen</li><li>Keine Requisiten als Hauptmotiv, keine Collagen</li><li>Kein Bild, das nach Katalog oder Rechner aussieht</li><li>Nichts, was nicht im Haus steht</li></ul></div>
</div>'''))
T.append(blatt(8, 'Die Bausteine', 'Knopf, Leiste,|Karte, Fenster.', f'''
<div class="bausteine">
  <div class="bs sw"><small>Knöpfe mit Tiefe und rundem Knauf</small><div class="bs__f bs__f--nacht">{kn('Zimmer finden', '#', 'hell')}{kn('Tisch reservieren', '#', 'nacht')}</div><p>Hell ist der Hauptweg, Nacht der Nebenweg. Der Knauf trägt den Pfeil in Licht. Unter der Maus hebt sich der Knopf zwei Pixel, langsam.</p></div>
  <div class="bs sw" style="--i:1"><small>Die Buchungsleiste</small><div class="bs__f bs__f--nacht"><div class="buchen"><label><small>Anreise</small><span>Fr, 13. November</span></label><label><small>Abreise</small><span>So, 15. November</span></label><label><small>Gäste</small><span>2 Erwachsene</span></label>{kn('Zimmer finden', '#', 'nacht')}</div></div><p>Leinen auf Nacht, Etiketten in Messing, ein Knopf. Sie steht im Auftakt und sonst nirgends.</p></div>
  <div class="bs sw" style="--i:2"><small>Die Karte</small><div class="bs__f bs__f--gruen"><div class="karte"><div class="karte__k"><b>Heute Abend</b><span>Fünf Gänge</span></div><ol><li class="an"><b>Zander</b><span>auf der Haut gebraten, junger Lauch, Beurre blanc</span></li><li><b>Salzwiesenlamm</b><span>glasierte Möhren, Jus, wilde Kräuter</span></li></ol></div></div><p>Leinen auf Flaschengrün. Der gewählte Gang trägt links eine Linie in Messing. Dieselbe Karte wird zur PDF.</p></div>
  <div class="bs sw" style="--i:3"><small>Das Fenster</small><div class="bs__f bs__f--foto">{img('s-fensterplatz', '50vw', 'Die Fensterbank', '50% 40%')}<p class="bs__satz">Jedes Zimmer hat ein Fenster zum Wasser.</p></div><p>Ein stehendes Bild, ein Satz, der Ausschnitt geht beim Scrollen auf. Zwei je Seite, an den Wendepunkten.</p></div>
</div>''', 'leinen'))
T.append(blatt(9, 'Richtig und falsch', 'Eingesetzt,|nie verändert.', f'''
<div class="rf">
  <figure class="rf__k rf__k--ja sw"><div class="rf__f rf__f--nacht">{lslot('gestapelt')}</div><figcaption>Leinen auf Nacht</figcaption></figure>
  <figure class="rf__k rf__k--ja sw" style="--i:1"><div class="rf__f rf__f--leinen">{lslot('gestapelt')}</div><figcaption>Tinte auf Leinen</figcaption></figure>
  <figure class="rf__k rf__k--ja sw" style="--i:2"><div class="rf__f rf__f--foto">{img('a-anleger', '30vw', '', '70% 10%')}<div class="rf__ueber">{lslot('gestapelt')}</div></div><figcaption>Auf einem ruhigen Bildteil, mit weichem Hof</figcaption></figure>
  <figure class="rf__k rf__k--nein sw" style="--i:3"><div class="rf__f rf__f--nacht rf__f--breit">{lslot('gestapelt')}</div><figcaption>Nicht verzerren</figcaption></figure>
  <figure class="rf__k rf__k--nein sw" style="--i:4"><div class="rf__f rf__f--nacht rf__f--licht">{lslot('gestapelt')}</div><figcaption>Nicht in Licht oder Backstein</figcaption></figure>
  <figure class="rf__k rf__k--nein sw" style="--i:5"><div class="rf__f rf__f--nacht rf__f--schatten">{lslot('gestapelt')}</div><figcaption>Kein Schatten, kein Verlauf, kein Rahmen</figcaption></figure>
  <figure class="rf__k rf__k--nein sw" style="--i:6"><div class="rf__f rf__f--nacht rf__f--dreh">{lslot('gestapelt')}</div><figcaption>Nicht drehen, nicht kippen</figcaption></figure>
  <figure class="rf__k rf__k--nein sw" style="--i:7"><div class="rf__f rf__f--nacht"><p class="rf__falsch">Ihr Haus</p></div><figcaption>Nicht neu setzen, nicht fett, nicht kursiv</figcaption></figure>
</div>'''))
T.append(blatt(10, 'Der Ton', 'Sagen,|was ist.', f'''
<div class="zwei">
  <div class="text sw"><p class="gross">{e(m["ton"])}</p>
  <p>Ein Satz sagt eine Sache. Er beginnt mit dem Haus, nicht mit dem Gast («Zwölf Zimmer hinter Backstein», nicht «Erleben Sie»). Zahlen stehen, wo sie etwas erklären, und nie als Werbung.</p>
  <dl class="worte"><dt>Wörter des Hauses</dt><dd>Speicher, Boden, Kai, Anleger, Winde, Tafel, Theke, Fleet, Kräne, das Wasser, die Stunde vor dem Öffnen</dd>
  <dt>Wörter, die wir nicht benutzen</dt><dd>Luxus, einzigartig, Erlebnis, Oase, Wohlfühl-, Highlight, exklusiv, Traum-, Genuss, herzlich willkommen, Ausrufezeichen</dd></dl></div>
  <div class="saetze sw" style="--i:1">
    <p class="satz satz--ja">Unten wird empfangen, oben wird geschlafen.</p>
    <p class="satz satz--ja">Die Lampe am Eingang brennt, wenn Sie ankommen.</p>
    <p class="satz satz--ja">Gekocht wird, was der Hafenmarkt am Morgen hatte.</p>
    <p class="satz satz--nein">Erleben Sie einzigartigen Luxus in historischem Ambiente!</p>
    <p class="satz satz--nein">Ihre Wohlfühl-Oase mitten in der pulsierenden HafenCity.</p>
  </div>
</div>''', 'leinen'))
eig = [('m-schluessel', 'Der Schlüssel', 'Messing, schwer, mit Lederanhänger und geprägtem Zeichen. Kein Kartenschloss.'),
       ('s-hundeplatz', 'Lotte', 'Liegt neben dem Empfang. Hundegäste bekommen Decke, Napf und Handtuch.'),
       ('z-minibar', 'Hafenbonbons', 'Im Schrank jedes Zimmers: Gläser, zwei Flaschen ohne Etikett, ein Glas Bonbons aus der Speicherstadt.'),
       ('r-franzbroetchen', 'Franzbrötchen', 'Jeden Morgen aus dem Ofen. Das Hamburger Gebäck, das kein Gast kennt und jeder mitnehmen will.'),
       ('s-dachboden', 'Der Dachboden', 'Unter dem Dachstuhl von 1888, für Feiern an einer langen Tafel.'),
       ('a-raeder', 'Die Räder', 'Zwei dunkelgrüne Räder mit Korb und Wolldecke, am Empfang eintragen und losfahren.')]
eigk = ''.join(f'<figure class="eig sw" style="--i:{i}"><div class="rahmen">{img(b, "(max-width:900px) 100vw, 33vw", t)}</div><figcaption><b>{e(t)}</b><p>{e(s)}</p></figcaption></figure>' for i, (b, t, s) in enumerate(eig))
T.append(blatt(11, 'Was nur Ihr Haus ist', 'Die Dinge,|die bleiben.', f'<div class="eigen">{eigk}</div>'))
T.append(f'''<section class="schluss" id="b12"><div class="blatt__in">
  <div class="kopf sw"><small>12 · Die Dateien</small>{zl('Alles zum|Herunterladen.')}</div>
  <div class="dateien">
    <a class="datei sw" href="../assets/marke/zeichen.svg" download><b>Zeichen</b><span>zeichen.svg · in jeder Farbe</span></a>
    <a class="datei sw" style="--i:1" href="../assets/marke/wortmarke.svg" download><b>Wortmarke</b><span>wortmarke.svg · als Pfade</span></a>
    <a class="datei sw" style="--i:2" href="../assets/marke/logo.svg" download><b>Logo gestapelt</b><span>logo.svg</span></a>
    <a class="datei sw" style="--i:3" href="../assets/marke/logo-zeile.svg" download><b>Logo in der Zeile</b><span>logo-zeile.svg</span></a>
    <a class="datei sw" style="--i:4" href="../assets/marke/tapete-nacht.svg" download><b>Tapete Nacht</b><span>tapete-nacht.svg · Kachel 480 × 240</span></a>
    <a class="datei sw" style="--i:5" href="../assets/marke/tapete-leinen.svg" download><b>Tapete Leinen</b><span>tapete-leinen.svg</span></a>
    <a class="datei sw" style="--i:6" href="../assets/marke/farben.svg" download><b>Farbkarten</b><span>farben.svg · farben.txt</span></a>
    <a class="datei sw" style="--i:7" href="../assets/fonts/CormorantGaramond-500.woff2" download><b>Cormorant Garamond</b><span>500 · woff2 · OFL</span></a>
    <a class="datei sw" style="--i:8" href="../assets/fonts/InstrumentSans-normal-400_600.woff2" download><b>Instrument Sans</b><span>400 bis 600 · woff2 · OFL</span></a>
  </div>
  <div class="schluss__u sw"><div class="titel__z">{slot(1.8)}</div><p>Ihr Haus · Sandtorkai 7 · 20457 Hamburg<br>Markenbuch, Stand November 2026. Gebaut von Tasty Studios.</p>{kn('Zur Website', '../index.html', 'hell')}</div>
</div></section>''')

# Schild und Wechsel der Fassung (nur solange keine gewählt ist)
FD = [{'name': n, 'satz': s_, 'erkl': k, 'innen': fn()} for i, (n, s_, k, fn) in enumerate(FASSUNGEN)]
VORL = {'gest': logo_svg('gestapelt', '__V__'), 'zeile': logo_svg('zeile', '__V__'), 'tn': tapete_svg('__V__'), 'tl': tapete_svg('__V__', F['Leinen'], '#1c2029', .07, .12)}
schild = '' if ZN is not None else f'''
<div class="vschild"><button type="button" class="vschild__p" data-vor="-1" aria-label="vorige Fassung">‹</button><b data-vnr>00</b><span>/ {len(FASSUNGEN) - 1:02d}</span><em data-vname>{e(FASSUNGEN[0][0])}</em><button type="button" class="vschild__p" data-vor="1" aria-label="nächste Fassung">›</button><i>← →</i></div>
<script>window.FASSUNGEN={json.dumps(FD, ensure_ascii=False)};window.VORLAGEN={json.dumps(VORL, ensure_ascii=False)};</script>
<script>
(function(){{
  var F=window.FASSUNGEN,n=0,m=location.hash.match(/z=(\\d+)/);if(m)n=Math.min(F.length-1,+m[1]);
  function setze(k){{n=(k+F.length)%F.length;var f=F[n];
    document.querySelectorAll('.zslot').forEach(function(s){{var d=s.getAttribute('data-d');s.innerHTML='<svg viewBox="0 0 100 100" role="img" aria-label="'+f.name+'">'+f.innen.split('__D__').join(d)+'</svg>'}});
    var V=window.VORLAGEN;document.querySelectorAll('.lslot').forEach(function(s){{s.innerHTML=(s.getAttribute('data-art')==='zeile'?V.zeile:V.gest).replace('__Z__',f.innen.split('__D__').join('2.4'))}});
    document.querySelectorAll('[data-ztext="satz"]').forEach(function(p){{p.textContent=f.satz}});document.querySelectorAll('[data-ztext="erkl"]').forEach(function(p){{p.textContent=f.erkl}});
    var du=function(t){{return 'url("data:image/svg+xml,'+encodeURIComponent(t.replace('__Z__',f.innen.split('__D__').join('2.4')))+'")'}};document.documentElement.style.setProperty('--tn',du(V.tn));document.documentElement.style.setProperty('--tl',du(V.tl));
    document.querySelector('[data-vnr]').textContent=(n<10?'0':'')+n;document.querySelector('[data-vname]').textContent=f.name;
    history.replaceState(null,'','#z='+n)}}
  document.querySelectorAll('[data-vor]').forEach(function(b){{b.addEventListener('click',function(){{setze(n+ +b.getAttribute('data-vor'))}})}});
  window.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight')setze(n+1);if(ev.key==='ArrowLeft')setze(n-1)}});
  setze(n);
}})();
</script>'''

nav = ''.join(f'<a href="#b{i}">{i:02d}</a>' for i in range(1, 13))
seite = f'''<!doctype html>
<html lang="de" class="warte">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ihr Haus · Das Markenbuch</title><meta name="robots" content="noindex"><meta name="theme-color" content="{F['Nacht']}">
<link rel="preload" href="../assets/fonts/CormorantGaramond-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="markenbuch.css?v={int(os.path.getmtime(os.path.join(HIER, 'marke', 'markenbuch.css')))}">
<script>setTimeout(function(){{document.documentElement.classList.remove('warte');document.documentElement.classList.add('los')}},3500)</script>
</head>
<body>
<header class="leiste"><a class="leiste__m" href="#oben"><span class="leiste__z">{slot(3)}</span><span class="leiste__w">{WM}</span></a><nav class="leiste__n">{nav}</nav><button type="button" class="leiste__pdf" data-druck>Als PDF sichern</button></header>
<main>{"".join(T)}</main>
<script>
(function(){{
  var doc=document.documentElement;
  function zeigen(){{doc.classList.remove('warte');void doc.offsetWidth;setTimeout(function(){{doc.classList.add('los')}},20)}}
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(zeigen);else zeigen();
  var z=document.querySelectorAll('.sw,.sw-feld');
  if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('da');io.unobserve(x.target)}}}})}},{{rootMargin:'0px 0px -4% 0px'}});z.forEach(function(e){{io.observe(e)}})}}else z.forEach(function(e){{e.classList.add('da')}});
  document.querySelectorAll('[data-druck]').forEach(function(b){{b.addEventListener('click',function(ev){{ev.preventDefault();document.querySelectorAll('.sw,.sw-feld').forEach(function(e){{e.classList.add('da')}});setTimeout(function(){{window.print()}},150)}})}});
  var l=document.querySelector('.leiste'),letzt=0;window.addEventListener('scroll',function(){{var y=scrollY;l.classList.toggle('fest',y>80);l.classList.toggle('weg',y>innerHeight&&y>letzt+4);if(y<letzt-4)l.classList.remove('weg');letzt=y}},{{passive:true}});
}})();
</script>{schild}
</body></html>'''
open(os.path.join(HIER, 'marke', 'markenbuch.html'), 'w', encoding='utf-8').write(seite)
print('Markenbuch gebaut:', len(T), 'Blätter ·', len(FASSUNGEN), 'Zeichen-Fassungen ·', 'gewählt' if ZN is not None else 'Schild zum Wählen')
