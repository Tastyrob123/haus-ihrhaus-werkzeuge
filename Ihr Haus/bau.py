#!/usr/bin/env python3
"""Baut die Startseite von «Ihr Haus», dem Beispielhaus von Tasty Studios (Robert 02.11.2026):
ein Hotel in einem Speicher von 1888 am Sandtorkai. Geschichte: vom Kai durchs Haus hinauf und wieder hinaus ans Wasser.
Fakten (einmal hier, gleich wie in Tasty Studios Website/_varianten/runde3/ihrhaus.py): zwölf Zimmer, Tafel Donnerstag bis Samstag ab 19 Uhr.
python3 bau.py → index.html"""
import os, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HIER, 'assets', 'img', 'bilder.json')))
V = str(int(os.path.getmtime(os.path.join(HIER, 'ihrhaus.css')) + os.path.getmtime(os.path.join(HIER, 'ihrhaus.js'))))
e = html.escape
import haus as H
ZEICHEN = open(os.path.join(HIER, 'assets', 'marke', 'zeichen.svg')).read().replace('<svg ', '<svg class="zeichen" ', 1)

def img(n, sizes='100vw', alt='', eager=False, pos=None, cls=''):
    d = B[n]; br = d['b']
    srcset = ', '.join(f'assets/img/{n}-{b}.webp {b}w' for b in br)
    st = f' style="object-position:{pos}"' if pos else ''
    c = f' class="{cls}"' if cls else ''
    lade = ' fetchpriority="high" decoding="sync"' if eager else ' loading="lazy" decoding="async"'
    return f'<img{c} src="assets/img/{n}-{br[min(1, len(br) - 1)]}.webp" srcset="{srcset}" sizes="{sizes}" width="{d["w"]}" height="{d["h"]}" alt="{e(alt)}"{st}{lade}>'

def zeilen(text, cls='t1', tag='h2', start=0):
    """Titel steigt Zeile für Zeile aus dem Schlitz"""
    z = ''.join(f'<span class="sl"><span style="--i:{start + i}">{e(x)}</span></span>' for i, x in enumerate(text.split('|')))
    return f'<{tag} class="{cls}">{z}</{tag}>'

PFEIL = '<i class="kn__k"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></i>'
def knopf(text, href, art='hell'):
    return f'<a class="kn kn--{art}" href="{href}"><span>{e(text)}</span>{PFEIL}</a>'

LOGO = '<a class="logo" href="index.html" aria-label="Ihr Haus, zur Startseite"><b>Ihr Haus</b><small>Am Hafen · Hamburg</small></a>'

# ------------------------------------------------------------------ Abschnitte
import re as _re
def _marke(datei, cls):
    s = open(os.path.join(HIER, 'assets', 'marke', datei)).read()
    s = _re.sub(r'\srole="img"', '', s); s = _re.sub(r'\saria-label="[^"]*"', '', s)
    return s.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1)
# Logo der Leiste (Robert 03.11.2026, Leiste Fassung 9): Kran, Wortmarke, Unterzeile gestapelt in der Mitte, Seiten mit feinen Trennern
LOGO_STAPEL = f'<a class="llogo llogo--stapel" href="index.html" aria-label="Ihr Haus, zur Startseite">{_marke("zeichen.svg", "lz")}{_marke("wortmarke.svg", "lw")}{_marke("unterzeile.svg", "lu")}</a>'

def leiste():
    return f'''<header class="leiste lv9 fest" data-leiste>
  <nav class="leiste__l lv9__t"><a href="zimmer.html">Zimmer</a><a href="tafel.html">Die Tafel</a></nav>
  {LOGO_STAPEL}
  <nav class="leiste__r lv9__t"><a href="anreise.html">Anreise</a><a href="kontakt.html">Kontakt</a></nav>
  <a class="lv9__b" href="kontakt.html#anfrage">Buchen</a>
</header>'''

def auftakt():
    return f'''<section class="auftakt" id="oben">
  <picture class="auftakt__b"><source media="(max-width:700px)" srcset="assets/img/hero-m-600.webp 600w, assets/img/hero-m-1000.webp 1000w" sizes="100vw">{img('hero', '100vw', 'Der Speicher von Ihr Haus am Sandtorkai in der Dämmerung, vom Wasser aus', eager=True, pos='60% 50%')}</picture>
  <div class="auftakt__t">
    {zeilen('Ein Speicher|am Hafen.', 'auftakt__h', 'h1')}
    <p class="auftakt__p">Zwölf Zimmer hinter Backstein, eine lange Tafel und das Wasser vor der Tür. Seit 1888 am Sandtorkai.</p>
    <form class="buchen" id="buchen" onsubmit="return false">
      <label><small>Anreise</small><span>Fr, 13. November</span></label>
      <label><small>Abreise</small><span>So, 15. November</span></label>
      <label><small>Gäste</small><span>2 Erwachsene</span></label>
      <a class="kn kn--nacht" href="zimmer.html"><span>Zimmer finden</span>{PFEIL}</a>
    </form>
  </div>
</section>'''

def empfang():
    return f'''<section class="empfang" aria-labelledby="h-empfang">
  <div class="empfang__w">
    <div class="empfang__links">
      <figure class="rahmen empfang__tuer sw">{img('s-eingang', '(max-width:900px) 100vw, 34vw', 'Die Eichentür von Ihr Haus mit brennender Laterne')}</figure>
      <figure class="rahmen empfang__brett sw" style="--i:1">{img('s-schluesselbrett', '(max-width:900px) 100vw, 34vw', 'Das Schlüsselbrett hinter dem Empfang')}</figure>
    </div>
    <figure class="rahmen empfang__theke sw">{img('empfang', '(max-width:900px) 100vw, 60vw', 'Die Theke am Empfang, ein Schlüssel liegt bereit')}</figure>
    <div class="empfang__t sw" id="h-empfang">
      {zeilen('Unten wird empfangen,|oben wird geschlafen.', 't1')}
      <p>Wo früher Kaffee und Tabak lagerten, steht heute eine lange Theke aus Eiche. Ihr Schlüssel liegt bereit, und wer mag, setzt sich mit dem ersten Glas in die Halle ans Fenster.</p>
    </div>
    <figure class="rahmen empfang__halle sw">{img('s-lobby', '(max-width:900px) 100vw, 30vw', 'Die Halle mit Ledersofas und Blick auf den Hafen')}</figure>
  </div>
</section>'''

def fenster(bild, satz, alt, pos='50% 50%', cls=''):
    return f'''<section class="fenster sw-feld{(' ' + cls) if cls else ''}" aria-label="{e(satz.replace('|', ' '))}">
  <div class="fenster__a"><div class="fenster__i">{img(bild, '100vw', alt, pos=pos)}</div></div>
  <div class="fenster__t">{zeilen(satz, 'fenster__s', 'p')}</div>
</section>'''

import haus as H
ZIMMER = [(z['id'], z['name'], f"{z['qm']} m² · {z['lage']} · Bett {z['bett']}", str(z['preis']['neben']), z['satz'], z['bilder']) for z in H.ZIMMER]

def zimmer():
    reiter = ''.join(f'<button type="button" class="zi-r{" an" if i == 0 else ""}" data-zimmer="{k}">{e(n)}</button>' for i, (k, n, *_r) in enumerate(ZIMMER))
    daten = {k: {'name': n, 'fakten': f, 'preis': p, 'satz': s, 'bilder': [[b, a] for b, a in bs]} for k, n, f, p, s, bs in ZIMMER}
    k, n, f, p, s, bs = ZIMMER[0]
    daumen = ''.join(f'<button type="button" class="zi-d{" an" if i == 0 else ""}" data-i="{i}" aria-label="{e(a)}">{img(b, "220px", a)}</button>' for i, (b, a) in enumerate(bs))
    return f'''<section class="zimmer" id="zimmer" aria-labelledby="h-zimmer">
  <div class="zimmer__kopf sw">
    {zeilen('Vier Arten, über|dem Wasser zu schlafen.', 't1 t1--dunkel')}
    <div class="zi-reiter" role="tablist">{reiter}<i class="zi-linie" aria-hidden="true"></i></div>
  </div>
  <div class="zimmer__w">
    <div class="zimmer__links sw">
      <figure class="rahmen zi-buehne" data-buehne>{img(bs[0][0], '(max-width:900px) 100vw, 62vw', bs[0][1])}</figure>
      <div class="zi-daumen">{daumen}</div>
    </div>
    <div class="zimmer__info sw" aria-live="polite">
      <h3 class="zi-name"><span class="sl"><span>{e(n)}</span></span></h3>
      <p class="zi-satz">{e(s)}</p>
      <p class="zi-fakten">{e(f)}</p>
      <p class="zi-preis">ab <b>{p} €</b> die Nacht, mit Frühstück</p>
      {knopf('Dieses Zimmer anfragen', 'kontakt.html#anfrage', 'nacht')}
      <p class="zi-rest">Zwölf Zimmer auf fünf Böden. Jedes ist ein bisschen anders, weil der Speicher es auch ist.</p>
    </div>
  </div>
  <script type="application/json" id="zimmer-daten">{json.dumps(daten, ensure_ascii=False)}</script>
</section>'''

BILD_JE_GANG = ['r-brot', 'r-krabben', 'r-zander', 'r-lamm', 'r-gruetze']
GAENGE = [(b, n, t) for b, (n, t) in zip(BILD_JE_GANG, H.TAFEL['karte'])]

def tafel():
    gaenge = ''.join(f'<li><button type="button" class="ga{" an" if i == 2 else ""}" data-bild="{b}" style="--i:{i}"><b>{e(n)}</b><span>{e(t)}</span></button></li>'
                     for i, (b, n, t) in enumerate(GAENGE))
    return f'''<section class="tafel" id="tafel" aria-labelledby="h-tafel">
  <div class="tafel__kopf sw">
    {zeilen('Die Tafel.', 't1')}
    <p>{e(H.TAFEL['tage'])} ab {e(H.TAFEL['ab'])}. Gekocht wird, was der Hafenmarkt am Morgen hatte, in fünf Gängen und von Hand angerichtet.</p>
  </div>
  <div class="tafel__w">
    <figure class="rahmen ta-buehne sw" data-teller>{img('r-zander', '(max-width:900px) 100vw, 58vw', 'Zander mit Lauch und Beurre blanc')}</figure>
    <div class="ta-karte sw">
      <div class="ta-karte__kopf"><b>Heute Abend</b><span>Fünf Gänge</span></div>
      <ol class="ta-gaenge">{gaenge}</ol>
      {knopf('Tisch reservieren', 'kontakt.html#tisch', 'nacht')}
    </div>
  </div>
  <div class="tafel__band sw">
    <figure class="rahmen">{img('r-gastraum', '(max-width:900px) 100vw, 64vw', 'Der Gastraum vor dem Service, die Kerzen brennen')}</figure>
    <figure class="rahmen">{img('r-weinkeller', '(max-width:900px) 100vw, 32vw', 'Der Weinkeller im Gewölbe')}</figure>
  </div>
  <div class="vorlad" aria-hidden="true">{''.join(img(b, '(max-width:900px) 100vw, 58vw') for b, *_ in GAENGE if b != 'r-zander')}</div>
</section>'''

def anreise():
    wege = [(t, x) for t, x in H.ANREISE if t in ('Mit der Bahn', 'Mit dem Schiff', 'Mit dem Rad')]
    w = ''.join(f'<div class="weg" style="--i:{i}"><h3>{e(t)}</h3><p>{e(s)}</p></div>' for i, (t, s) in enumerate(wege))
    return f'''<section class="anreise" id="anreise" aria-labelledby="h-anreise">
  <div class="anreise__w">
    <figure class="rahmen an-faehre sw">{img('a-faehre', '(max-width:900px) 100vw, 56vw', 'Die Hafenfähre auf der Elbe in der Dämmerung')}</figure>
    <div class="an-t sw">
      {zeilen('Ankommen|am Sandtorkai.', 't1')}
      <div class="wege">{w}</div>
      <p class="an-adresse">Ihr Haus · Sandtorkai 7 · 20457 Hamburg</p>
    </div>
    <figure class="rahmen an-koffer sw">{img('a-koffer', '(max-width:900px) 100vw, 28vw', 'Ein Koffer vor der offenen Eingangstür')}</figure>
    <figure class="rahmen an-raeder sw">{img('a-raeder', '(max-width:900px) 100vw, 28vw', 'Zwei Hotelräder an der Backsteinwand')}</figure>
  </div>
</section>'''

def schluss():
    return f'''<section class="schluss sw-feld" aria-labelledby="h-schluss">
  <div class="schluss__b">{img('schluss', '100vw', 'Der Speicher am Kanal bei Nacht, zwei Fenster brennen', pos='62% 50%')}</div>
  <div class="schluss__t">
    {zeilen('Die Lampe am Eingang|brennt, wenn Sie ankommen.', 't1 schluss__h')}
    <p>Zwölf Zimmer, eine Tafel und das Wasser vor der Tür. Wir freuen uns auf Sie.</p>
    <div class="knoepfe">{knopf('Zimmer finden', 'zimmer.html', 'hell')}{knopf('Tisch reservieren', 'kontakt.html#tisch', 'nacht')}</div>
  </div>
</section>'''

def fuss():
    return f'''<footer class="fuss">
  <div class="fuss__w">
    <div class="fuss__m">{ZEICHEN}{LOGO}</div>
    <p>{e(H.HAUS['adresse']['strasse'])} · {e(H.HAUS['adresse']['plz'])} {e(H.HAUS['adresse']['ort'])}<br>{e(H.HAUS['telefon'])} · {e(H.HAUS['mail'])}</p>
    <nav><a href="zimmer.html">Zimmer</a><a href="tafel.html">Die Tafel</a><a href="anreise.html">Anreise</a><a href="kontakt.html">Kontakt</a><a href="impressum.html">Impressum</a></nav>
  </div>
  <p class="fuss__klein">Ein Beispielhaus von Tasty Studios. Das Haus ist erfunden, die Bilder sind erzeugt.</p>
</footer>'''

def seite(datei, titel, beschr, inhalt, preload=None, cls=''):
    pre = f'<link rel="preload" as="image" href="assets/img/{preload}-1400.webp" imagesrcset="assets/img/{preload}-800.webp 800w, assets/img/{preload}-1400.webp 1400w, assets/img/{preload}-2400.webp 2400w" imagesizes="100vw" fetchpriority="high">' if preload else ''
    return f'''<!doctype html>
<html lang="de" class="warte">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschr)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#10151d">
<link rel="preload" href="assets/fonts/CormorantGaramond-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="ihrhaus.css?v={V}">
<script>setTimeout(function(){{document.documentElement.classList.remove('warte');document.documentElement.classList.add('los')}},3500)</script>
</head>
<body class="{cls}">
{leiste()}
<main>
{inhalt}
</main>
{fuss()}
<script>window.IH_B={json.dumps({k: v['b'] for k, v in B.items()})};</script>
<script src="ihrhaus.js?v={V}"></script>
</body>
</html>'''

def schreibe(datei, text):
    open(os.path.join(HIER, datei), 'w', encoding='utf-8').write(text); print(datei, 'gebaut')

# ------------------------------------------------------------------ Unterseiten
def kopfbild(bild, titel, satz, alt, pos='50% 50%', hoch=False):
    """Auftakt einer Unterseite: ein grosses Bild, Titel aus dem Schlitz, ein Satz; kleiner als die Startseite, derselbe Schwung"""
    return f'''<section class="kopfbild{" kopfbild--hoch" if hoch else ""}" id="oben">
  <div class="kopfbild__b">{img(bild, '100vw', alt, eager=True, pos=pos)}</div>
  <div class="kopfbild__t">{zeilen(titel, 'kopfbild__h', 'h1')}<p class="kopfbild__p">{e(satz)}</p></div>
</section>'''

def seite_zimmer():
    kap = []
    for i, z in enumerate(H.ZIMMER):
        b = z['bilder']; links = i % 2 == 0
        gross = f'<figure class="rahmen zk-gross sw">{img(b[0][0], "(max-width:900px) 100vw, 58vw", b[0][1])}</figure>'
        klein = ''.join(f'<figure class="rahmen zk-klein sw" style="--i:{j + 1}">{img(bb, "(max-width:900px) 50vw, 29vw", aa)}</figure>' for j, (bb, aa) in enumerate(b[1:]))
        aus = ''.join(f'<li>{e(a)}</li>' for a in z['ausstattung'])
        text = f'''<div class="zk-t sw" style="--i:1">
      <small class="zk-boden">{e(z['boden'])} · {z['anzahl']} × im Haus</small>
      {zeilen(z['name'], 't1 t1--dunkel zk-name', 'h2')}
      <p class="zk-satz">{e(z['satz'])}</p>
      <p class="zk-fakten">{z['qm']} m² · {e(z['lage'])} · Bett {e(z['bett'])}</p>
      <ul class="zk-aus">{aus}</ul>
      <div class="zk-preise"><div><small>{e(H.SAISON['neben'])}</small><b>{z['preis']['neben']} €</b></div><div><small>{e(H.SAISON['haupt'])}</small><b>{z['preis']['haupt']} €</b></div><p>je Nacht für zwei, mit Frühstück</p></div>
      {knopf('Dieses Zimmer anfragen', f'kontakt.html#anfrage?zimmer={z["id"]}', 'nacht')}
    </div>'''
        kap.append(f'<section class="zk{" zk--rechts" if not links else ""}" id="{z["id"]}"><div class="zk__w">{gross}{text}<div class="zk-reihe">{klein}</div></div></section>')
    regeln = ''.join(f'<div class="regel sw" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(H.REGELN) if a in ('Anreise', 'Abreise', 'Hunde', 'Kinder', 'Stornierung', 'Barrierefreiheit'))
    inhalt = (kopfbild('z-kranzimmer', 'Zwölf Zimmer|auf fünf Böden.', 'Vier Arten, über dem Wasser zu schlafen. Jedes Zimmer ist ein bisschen anders, weil der Speicher es auch ist.', 'Das Kranzimmer mit zwei Fenstern zum Hafen', '50% 55%')
              + ''.join(kap)
              + fenster('z-morgen', 'Morgens kommt das Frühstück|aufs Zimmer, wenn Sie mögen.', 'Frühstück im Bett, grau Licht vom Hafen', '50% 50%')
              + f'''<section class="gut" id="gut"><div class="gut__w"><div class="kopf sw">{zeilen('Gut zu wissen.', 't1')}<p>{e(H.SAISON['hinweis'])}</p></div><div class="regeln">{regeln}</div></div></section>'''
              + schluss())
    return seite('zimmer.html', 'Die Zimmer · Ihr Haus · Hamburg', 'Zwölf Zimmer in vier Arten im Speicher am Sandtorkai: Speicherzimmer, Zimmer zum Wasser, Kranzimmer, Dachsuite.', inhalt, 'z-kranzimmer', 'u-zimmer')

def seite_tafel():
    t = H.TAFEL
    gaenge = ''.join(f'<figure class="gang sw" style="--i:{i}"><div class="rahmen">{img(b, "(max-width:900px) 100vw, 20vw", n)}</div><figcaption><b>{e(n)}</b><span>{e(x)}</span></figcaption></figure>' for i, (b, (n, x)) in enumerate(zip(BILD_JE_GANG, t['karte'])))
    veg = ''.join(f'<li><b>{e(n)}</b><span>{e(x)}</span></li>' for n, x in t['vegetarisch_karte'])
    lief = ''.join(f'<div class="lief sw" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(t['lieferanten']))
    bar = ''.join(f'<li><b>{e(n)}</b><span>{e(x)}</span><i>{p} €</i></li>' for n, x, p in H.BAR['karte'])
    feiern = ''.join(f'<div class="feier sw" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(H.FEIERN['orte']))
    inhalt = (kopfbild('r-gastraum', 'Die Tafel.', f'{t["tage"]} ab {t["ab"]}, Einlass {t["einlass"]}. {t["plaetze"]} Plätze, fünf Gänge, eine Karte für alle.', 'Der Gastraum vor dem Service', '50% 50%')
              + f'''<section class="woche"><div class="woche__w">
  <div class="kopf sw">{zeilen('Die Karte|dieser Woche.', 't1')}<p>{e(t['satz'])}</p></div>
  <div class="gaenge">{gaenge}</div>
  <div class="woche__u">
    <div class="veg sw"><small>Vegetarisch, immer</small><ol class="ta-liste">{veg}</ol></div>
    <div class="preis-karte sw" style="--i:1"><div><small>Fünf Gänge</small><b>{t['preis']} €</b></div><div><small>Weinbegleitung</small><b>{t['wein']} €</b></div><p>{e(t['regeln'][0])}. {e(t['regeln'][1])}.</p>{knopf('Tisch reservieren', 'kontakt.html#tisch', 'hell')}</div>
  </div>
</div></section>'''
              + f'''<section class="herkunft"><div class="herkunft__w">
  <figure class="rahmen hk-b1 sw">{img('r-zutaten', '(max-width:900px) 100vw, 50vw', 'Fisch auf Eis, junge Möhren und Lauch in der Küche')}</figure>
  <div class="hk-t sw" style="--i:1">{zeilen('Woher|es kommt.', 't1 t1--dunkel')}<div class="liefs">{lief}</div></div>
  <figure class="rahmen hk-b2 sw" style="--i:2">{img('r-pass', '(max-width:900px) 100vw, 50vw', 'Der Pass vor dem Service')}</figure>
</div></section>'''
              + fenster('r-tisch-fenster', 'Ein Tisch für zwei|am Fenster zum Hafen.', 'Ein gedeckter Tisch am Fenster, draussen die Kräne')
              + f'''<section class="morgen-bar"><div class="mb__w">
  <div class="mb mb--morgen"><figure class="rahmen sw">{img('r-franzbroetchen', '(max-width:900px) 100vw, 46vw', 'Franzbrötchen und Kaffee am Morgen')}</figure><div class="mb-t sw" style="--i:1">{zeilen('Das Frühstück.', 't2')}<p class="mb-zeit">{e(H.FRUEHSTUECK['zeit'])}, sonntags {e(H.FRUEHSTUECK['sonntag'])}</p><p>{e(H.FRUEHSTUECK['satz'])} Für Gäste von aussen {H.FRUEHSTUECK['preis_extern']} €.</p></div></div>
  <div class="mb mb--bar"><div class="mb-t sw">{zeilen('Die Bar.', 't2')}<p class="mb-zeit">{e(H.BAR['zeit'])}</p><p>{e(H.BAR['satz'])}</p><ol class="bar-karte">{bar}</ol></div><figure class="rahmen sw" style="--i:1">{img('bar', '(max-width:900px) 100vw, 46vw', 'Die Bar vor dem Öffnen, Gläser auf Messing')}</figure></div>
</div></section>'''
              + f'''<section class="feiern"><div class="feiern__w">
  <figure class="rahmen fe-b sw">{img('s-dachboden', '(max-width:900px) 100vw, 60vw', 'Der Dachboden mit langer Tafel unter dem Dachstuhl')}</figure>
  <div class="fe-t sw" style="--i:1">{zeilen('Feiern|unter dem Dach.', 't1')}<p>{e(H.FEIERN['satz'])}</p><div class="feiers">{feiern}</div>{knopf('Feier anfragen', 'kontakt.html#feier', 'hell')}</div>
</div></section>'''
              + schluss())
    return seite('tafel.html', 'Die Tafel · Ihr Haus · Hamburg', f'Die Tafel im Speicher am Sandtorkai: {t["tage"]} ab {t["ab"]}, fünf Gänge, dazu Frühstück, Bar und Feiern unter dem Dach.', inhalt, 'r-gastraum', 'u-tafel')

def seite_anreise():
    bild = {'Mit der Bahn': 'a-speicherstadt', 'Mit dem Schiff': 'a-faehre', 'Mit dem Auto': 'a-koffer', 'Vom Flughafen': 'm-nebel', 'Mit dem Rad': 'a-raeder'}
    wege = ''.join(f'''<div class="wg{" wg--rechts" if i % 2 else ""}"><figure class="rahmen sw">{img(bild[t], "(max-width:900px) 100vw, 50vw", t)}</figure><div class="wg-t sw" style="--i:1">{zeilen(t, 't2', 'h2')}<p>{e(x)}</p></div></div>''' for i, (t, x) in enumerate(H.ANREISE))
    umg = ''.join(f'<li class="sw" style="--i:{i}"><b>{e(a)}</b><span>{e(b)}</span></li>' for i, (a, b) in enumerate(H.UMGEBUNG))
    regeln = ''.join(f'<div class="regel sw" style="--i:{i}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(H.REGELN) if a in ('Anreise', 'Abreise', 'Parken', 'Räder', 'Barrierefreiheit', 'Zahlung'))
    ad = H.HAUS['adresse']
    inhalt = (kopfbild('a-anleger', 'Ankommen|am Sandtorkai.', f'{ad["strasse"]}, {ad["plz"]} {ad["ort"]}. Zu Fuss vom Wasser, mit der Bahn, der Fähre oder dem Rad.', 'Der Anleger vor dem Haus in der Dämmerung', '50% 45%')
              + f'<section class="wege-s"><div class="wege-s__w">{wege}</div></section>'
              + fenster('m-nebel', 'Manchmal kommt der Hafen|erst gegen Mittag aus dem Nebel.', 'Der Hafen im Morgennebel')
              + f'''<section class="umgebung"><div class="umg__w"><div class="kopf sw">{zeilen('Von hier aus.', 't1 t1--dunkel')}</div><ul class="umg">{umg}</ul></div></section>'''
              + f'''<section class="gut gut--nacht"><div class="gut__w"><div class="kopf sw">{zeilen('Gut zu wissen.', 't1')}</div><div class="regeln">{regeln}</div></div></section>'''
              + schluss())
    return seite('anreise.html', 'Anreise · Ihr Haus · Hamburg', 'So kommen Sie zum Speicher am Sandtorkai: mit der Bahn, dem Schiff, dem Auto, vom Flughafen oder mit dem Rad.', inhalt, 'a-anleger', 'u-anreise')

def seite_kontakt():
    arten = [('zimmer', 'Zimmer'), ('tisch', 'Tisch an der Tafel'), ('feier', 'Feier'), ('nachricht', 'Nachricht')]
    opt = ''.join(f'<button type="button" class="art{" an" if i == 0 else ""}" data-art="{k}">{e(n)}</button>' for i, (k, n) in enumerate(arten))
    zi = ''.join(f'<option value="{z["id"]}">{e(z["name"])}</option>' for z in H.ZIMMER)
    f = H.FIRMA
    inhalt = (kopfbild('empfang', 'Schreiben|Sie uns.', 'Zimmer, Tisch, Feier oder eine Frage: Wir antworten am selben Tag, persönlich, in Ihrer Sprache.', 'Die Theke am Empfang mit Messinglampe', '50% 50%')
              + f'''<section class="anfrage" id="anfrage"><div class="anfrage__w">
  <form class="af sw" id="af" novalidate>
    <div class="af-arten" role="tablist">{opt}</div>
    <div class="af-feld af-feld--zimmer" data-nur="zimmer"><label>Zimmer<select name="zimmer"><option value="">Egal, Hauptsache am Wasser</option>{zi}</select></label></div>
    <div class="af-zwei"><label>Name<input name="name" type="text" required autocomplete="name"></label><label>E-Mail oder Telefon<input name="kontakt" type="text" required autocomplete="email"></label></div>
    <div class="af-zwei"><label><span data-tag="zimmer">Anreise</span><span data-tag="tisch feier">Datum</span><span data-tag="nachricht">Datum, falls es eines gibt</span><input name="datum" type="date"></label><label><span data-tag="zimmer">Abreise</span><span data-tag="tisch feier nachricht">Personen</span><input name="datum2" type="text" inputmode="numeric"></label></div>
    <label>Ihr Anliegen<textarea name="text" rows="5" maxlength="1200" placeholder="Was wir wissen sollten: Wünsche, Unverträglichkeiten, ein Hund, ein Anlass."></textarea></label>
    <input type="text" name="website" class="af-falle" tabindex="-1" autocomplete="off">
    <div class="af-fuss"><button type="submit" class="kn kn--nacht"><span>Anfrage senden</span>{PFEIL}</button><p>Es geht nichts an ein Portal. Ihre Anfrage landet am Empfang, bei {e(f['struktur'][3][1])}.</p></div>
    <div class="af-danke" hidden><b>Vielen Dank.</b><p>Ihre Anfrage ist am Empfang angekommen. Sie hören heute noch von uns.</p></div>
  </form>
  <aside class="af-seite sw" style="--i:1">
    <figure class="rahmen">{img('s-hundeplatz', '(max-width:900px) 100vw, 36vw', 'Lottes Platz neben dem Empfang')}</figure>
    <p class="af-lotte">{e(H.FIRMA['hund']['satz'])}</p>
    <dl><dt>Empfang</dt><dd>täglich 7 bis 23 Uhr</dd><dt>Telefon</dt><dd>{e(H.HAUS['telefon'])}</dd><dt>E-Mail</dt><dd>{e(H.HAUS['mail'])}</dd><dt>Adresse</dt><dd>{e(H.HAUS['adresse']['strasse'])}, {e(H.HAUS['adresse']['plz'])} {e(H.HAUS['adresse']['ort'])}</dd></dl>
    <p class="af-satz">Am Tresen: {e(f['struktur'][3][1])}. Für Feiern: {e(f['struktur'][0][1])}.</p>
  </aside>
</div></section>'''
              + schluss())
    return seite('kontakt.html', 'Kontakt · Ihr Haus · Hamburg', 'Zimmer anfragen, Tisch reservieren, Feier planen oder eine Frage stellen: Der Empfang antwortet am selben Tag.', inhalt, 'empfang', 'u-kontakt')

def seite_impressum():
    f = H.FIRMA
    inhalt = f'''<section class="recht"><div class="recht__w">
  <div class="kopf sw">{zeilen('Impressum.', 't1 t1--dunkel')}</div>
  <div class="recht__t sw">
    <p><b>{e(f['name'])}</b><br>{e(f['sitz'])}<br>{e(H.HAUS['telefon'])} · {e(H.HAUS['mail'])}</p>
    <p>Geschäftsführung: {e(f['geschaeftsfuehrung'])}<br>Registergericht: {e(f['register'])}<br>Umsatzsteuer-Identifikationsnummer: {e(f['ustid'])}</p>
    <p>Verantwortlich für den Inhalt: {e(f['geschaeftsfuehrung'])}, Anschrift wie oben.</p>
    <h2 class="t2">Datenschutz.</h2>
    <p>Diese Seite setzt keine Cookies und lädt nichts von fremden Servern. Was Sie über das Anfrage-Fenster schicken, lesen nur die Menschen am Empfang; es wird zur Bearbeitung Ihrer Anfrage gespeichert und auf Wunsch gelöscht. Besuche zählen wir ohne Namen und ohne Adresse, nur als Zahl. Fragen dazu an {e(H.HAUS['mail'])}.</p>
    <h2 class="t2">Bilder.</h2>
    <p>Ihr Haus ist ein Beispielhaus von Tasty Studios. Das Haus, die Menschen und die Zahlen sind erfunden, die Bilder wurden erzeugt. Gestaltung und Technik: Tasty Studios, Hamburg.</p>
  </div>
</div></section>'''
    return seite('impressum.html', 'Impressum · Ihr Haus · Hamburg', 'Impressum und Datenschutz von Ihr Haus, Sandtorkai 7, Hamburg.', inhalt, None, 'u-recht')

if __name__ == '__main__':
    schreibe('index.html', seite('index.html', 'Ihr Haus · Ein Speicher am Hafen · Hamburg', 'Zwölf Zimmer in einem Speicher von 1888 am Sandtorkai, eine Tafel von Donnerstag bis Samstag, das Wasser vor der Tür.',
             auftakt() + empfang() + fenster('s-fensterplatz', 'Jedes Zimmer hat ein Fenster zum Wasser.|Manche haben eine Bank darin.', 'Eine Fensterbank mit Kissen, Buch und Tee, draussen die Kräne', cls='fenster--hell')
             + zimmer() + tafel() + fenster('a-speicherstadt', 'Die Speicherstadt beginnt|hinter der nächsten Brücke.', 'Ein Fleet in der Speicherstadt zur blauen Stunde') + anreise() + schluss(), 'hero'))
    schreibe('zimmer.html', seite_zimmer()); schreibe('tafel.html', seite_tafel()); schreibe('anreise.html', seite_anreise()); schreibe('kontakt.html', seite_kontakt()); schreibe('impressum.html', seite_impressum())
