#!/usr/bin/env python3
"""Die Hausakte zum Lesen: baut konzept.html aus haus.py (eine Wahrheit, zwei Ansichten).   python3 konzept.py"""
import os, html
import haus as H
HIER = os.path.dirname(os.path.abspath(__file__))
e = html.escape

def bild(n, alt=''):
    import json
    B = json.load(open(os.path.join(HIER, 'assets', 'img', 'bilder.json')))
    if n not in B: return ''
    br = B[n]['b']; return f'<img src="assets/img/{n}-{br[min(1, len(br)-1)]}.webp" srcset="{", ".join(f"assets/img/{n}-{b}.webp {b}w" for b in br)}" sizes="(max-width:900px) 100vw, 520px" alt="{e(alt)}" loading="lazy" decoding="async">'

def kap(nr, titel, inhalt, foto=None):
    f = f'<figure class="k-foto">{bild(*foto)}</figure>' if foto else ''
    return f'<section class="kap"><div class="k-kopf"><small>{nr}</small><h2>{e(titel)}</h2></div><div class="k-inhalt">{inhalt}</div>{f}</section>'

def dl(paare):
    return '<dl>' + ''.join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in paare) + '</dl>'

h, f, t = H.HAUS, H.FIRMA, H.TAFEL
teile = []
teile.append(kap('01', 'Das Haus in einem Satz',
    f'<p class="gross">{e(h["kurz"])}</p><p>{e(h["adresse"]["strasse"])}, {e(h["adresse"]["plz"])} {e(h["adresse"]["ort"])} · gebaut {h["baujahr"]}, Hotel seit {h["eroeffnet"]} · {h["boeden"]} Böden, {h["zimmer_zahl"]} Zimmer · {e(h["telefon"])} · {e(h["mail"])}</p>',
    ('s-aussen-wasser', 'Der Speicher vom Wasser aus')))
teile.append(kap('02', 'Geschichte', '<ol class="zeit">' + ''.join(f'<li><b>{e(j)}</b><span>{e(s)}</span></li>' for j, s in H.GESCHICHTE) + '</ol>', ('m-backstein', 'Backstein im Abendlicht')))
teile.append(kap('03', 'Die Firma und die Menschen',
    dl([('Firma', f['name']), ('Sitz', f['sitz']), ('Register', f['register']), ('USt-IdNr.', f['ustid']), ('Geschäftsführung', f['geschaeftsfuehrung']), ('Gesellschafter', f['gesellschafter']), ('Team', f'{f["team"]} Menschen und ein Hund')])
    + '<div class="team">' + ''.join(f'<div class="person"><small>{e(r)}</small><b>{e(n)}</b><p>{e(s)}</p></div>' for r, n, s in f['struktur']) + f'<div class="person"><small>Hund</small><b>{e(f["hund"]["name"])}</b><p>{e(f["hund"]["satz"])}</p></div></div>',
    ('s-hundeplatz', 'Lottes Platz neben dem Empfang')))
zi = ''.join(f'''<div class="zimmer"><div class="zi-k"><b>{e(z["name"])}</b><span>{z["anzahl"]} × · {z["qm"]} m² · {e(z["lage"])} · {e(z["boden"])}</span></div>
<p>{e(z["satz"])}</p><p class="preis">Nebensaison {z["preis"]["neben"]} € · Hauptsaison {z["preis"]["haupt"]} €</p><ul>{"".join(f"<li>{e(a)}</li>" for a in z["ausstattung"])}</ul></div>''' for z in H.ZIMMER)
teile.append(kap('04', f'Die {h["zimmer_zahl"]} Zimmer', zi + f'<p class="klein">Nebensaison {e(H.SAISON["neben"])}, Hauptsaison {e(H.SAISON["haupt"])}. {e(H.SAISON["hinweis"])}</p>', ('z-kranzimmer', 'Das Kranzimmer')))
karte = lambda k: '<ol class="karte">' + ''.join(f'<li><b>{e(n)}</b><span>{e(s)}</span></li>' for n, s in k) + '</ol>'
teile.append(kap('05', 'Die Tafel',
    f'<p class="gross">{e(t["tage"])} ab {e(t["ab"])}, Einlass {e(t["einlass"])}. {t["plaetze"]} Plätze. {t["gaenge"]} Gänge {t["preis"]} €, Weinbegleitung {t["wein"]} €.</p><p>{e(t["satz"])}</p>'
    + '<div class="zwei"><div><small>Die Karte der Woche</small>' + karte(t['karte']) + '</div><div><small>Vegetarisch</small>' + karte(t['vegetarisch_karte']) + '</div></div>'
    + '<small>Woher es kommt</small>' + dl(t['lieferanten']) + '<small>Regeln</small><ul>' + ''.join(f'<li>{e(r)}</li>' for r in t['regeln']) + '</ul>',
    ('r-gastraum', 'Der Gastraum vor dem Service')))
teile.append(kap('06', 'Frühstück und Bar',
    f'<p class="gross">Frühstück {e(H.FRUEHSTUECK["zeit"])}, sonntags {e(H.FRUEHSTUECK["sonntag"])}.</p><p>{e(H.FRUEHSTUECK["satz"])} Für Gäste von aussen {H.FRUEHSTUECK["preis_extern"]} €.</p>'
    + f'<p class="gross">{e(H.BAR["name"])}: {e(H.BAR["zeit"])}, {H.BAR["plaetze"]} Plätze.</p><p>{e(H.BAR["satz"])}</p><ol class="karte">' + ''.join(f'<li><b>{e(n)}</b><span>{e(s)}</span><i>{p} €</i></li>' for n, s, p in H.BAR['karte']) + '</ol>',
    ('r-franzbroetchen', 'Franzbrötchen am Morgen')))
teile.append(kap('07', 'Feiern', f'<p>{e(H.FEIERN["satz"])}</p>' + dl(H.FEIERN['orte']), ('s-dachboden', 'Der Dachboden unter dem Dachstuhl')))
teile.append(kap('08', 'Hausregeln', dl(H.REGELN), ('s-schluesselbrett', 'Das Schlüsselbrett')))
teile.append(kap('09', 'Anreise und Umgebung', dl(H.ANREISE) + '<small>Entfernungen</small>' + dl(H.UMGEBUNG), ('a-faehre', 'Die Hafenfähre')))
m = H.MARKE
teile.append(kap('10', 'Die Marke',
    f'<p class="gross">{e(m["wortmarke"])} <span class="u">{e(m["unterzeile"])}</span></p><p><b>Zeichen:</b> {e(m["zeichen"])}</p><p><b>Ton:</b> {e(m["ton"])}</p>'
    + '<div class="farben">' + ''.join(f'<div class="farbe"><i style="background:{c}"></i><b>{e(n)}</b><span>{c}</span><p>{e(s)}</p></div>' for n, c, s in m['farben']) + '</div>'
    + dl(m['schriften']), ('m-material', 'Die Materialien des Hauses')))
w = '<div class="wz">' + ''.join(f'<div class="person"><small>{e(a)}</small><b>{e(n)}</b><p>{e(s)}</p></div>' for n, a, s in H.WERKZEUGE) + '</div>'
w += '<p class="klein">Die Namen kommen aus der Speicherstadt und gehören nur diesem Haus. Jede Hausart bekommt ihren eigenen Satz aus ihrer Welt: ein Berghotel andere Wörter als ein Speicher, ein Landgasthof wieder andere.</p>'
teile.append(kap('11', 'Hinter dem Haus: die sieben Werkzeuge', w, ('z-schreibtisch', 'Der Schreibtisch am Fenster')))

seite = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ihr Haus · Hausakte</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Instrument+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--nacht:#10151d;--leinen:#efe7da;--tinte:#1c2029;--licht:#e2ae68;--messing:#a8844f;--serif:'Cormorant Garamond',serif;--sans:'Instrument Sans',system-ui,sans-serif}}
*{{box-sizing:border-box;margin:0}}
body{{background:var(--leinen);color:var(--tinte);font:400 16.5px/1.6 var(--sans);-webkit-font-smoothing:antialiased}}
header{{background:var(--nacht);color:var(--leinen);padding:clamp(60px,9vw,120px) clamp(20px,5vw,80px) clamp(50px,6vw,80px)}}
header small{{font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--licht)}}
header h1{{font:500 clamp(56px,8vw,120px)/1 var(--serif);margin:14px 0 18px}}
header p{{max-width:60ch;font-size:19px;color:rgba(239,231,218,.86)}}
header nav{{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:34px;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase}}
header nav a{{color:var(--leinen);text-decoration:none;opacity:.8}}header nav a:hover{{opacity:1;color:var(--licht)}}
main{{padding:0 clamp(20px,5vw,80px) 100px}}
.kap{{display:grid;grid-template-columns:150px minmax(0,1fr) 420px;gap:40px;padding:56px 0;border-top:1px solid rgba(168,132,79,.4)}}
.k-kopf small{{display:block;font:500 48px/1 var(--serif);color:var(--messing)}}
.k-kopf h2{{font:500 26px/1.15 var(--serif);margin-top:10px}}
.k-inhalt>*+*{{margin-top:18px}}
.k-inhalt small{{display:block;margin-top:28px;font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--messing)}}
.gross{{font:500 clamp(22px,2vw,28px)/1.3 var(--serif)}}
.gross .u{{font:500 12px/1 var(--sans);letter-spacing:.3em;color:var(--messing);margin-left:10px;vertical-align:middle}}
.klein{{font-size:14px;color:rgba(28,32,41,.7)}}
dl{{display:grid;grid-template-columns:max-content 1fr;gap:8px 24px;margin-top:10px}}dt{{font-weight:500}}dd{{color:rgba(28,32,41,.85)}}
.zeit{{list-style:none;padding:0}}.zeit li{{display:grid;grid-template-columns:70px 1fr;gap:18px;padding:10px 0;border-bottom:1px solid rgba(168,132,79,.25)}}.zeit b{{font:500 24px/1.2 var(--serif);color:var(--messing)}}
.team,.wz{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;margin-top:22px}}
.person{{background:#fff;border-radius:6px;padding:18px 20px}}.person small{{margin:0 0 4px;font-size:10.5px}}.person b{{display:block;font:500 21px/1.2 var(--serif)}}.person p{{margin-top:6px;font-size:14.5px;color:rgba(28,32,41,.8)}}
.zimmer{{background:#fff;border-radius:6px;padding:22px 24px}}.zi-k b{{font:500 24px/1.2 var(--serif)}}.zi-k span{{display:block;font-size:13.5px;color:var(--messing);margin-top:2px}}
.zimmer p{{margin-top:10px}}.preis{{font-weight:500}}.zimmer ul{{columns:2;margin-top:10px;padding-left:18px;font-size:14.5px;color:rgba(28,32,41,.8)}}
.zwei{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}.zwei small{{margin-top:0}}
.karte{{list-style:none;padding:0;margin-top:8px}}.karte li{{display:grid;grid-template-columns:1fr auto;padding:10px 0;border-bottom:1px solid rgba(168,132,79,.25)}}.karte b{{font:500 20px/1.2 var(--serif);grid-column:1}}.karte span{{grid-column:1;font-size:14px;color:rgba(28,32,41,.7)}}.karte i{{grid-column:2;grid-row:1/3;font-style:normal;font:500 20px/1.2 var(--serif)}}
.k-inhalt ul{{padding-left:20px}}
.farben{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.farbe i{{display:block;height:64px;border-radius:5px;border:1px solid rgba(0,0,0,.08)}}.farbe b{{display:block;margin-top:8px;font:500 18px/1.2 var(--serif)}}.farbe span{{font-size:12.5px;letter-spacing:.08em;color:var(--messing)}}.farbe p{{font-size:13.5px;color:rgba(28,32,41,.75);margin-top:2px}}
.namen{{width:100%;border-collapse:collapse;margin-top:10px;font-size:15px}}.namen th{{text-align:left;font:500 12px/1.3 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--messing);padding:8px 10px 10px 0;border-bottom:1px solid rgba(168,132,79,.4)}}.namen td{{padding:9px 10px 9px 0;border-bottom:1px solid rgba(168,132,79,.2)}}.namen td:first-child{{color:rgba(28,32,41,.6)}}
.k-foto{{position:sticky;top:30px;align-self:start}}.k-foto img{{width:100%;height:auto;border-radius:6px;display:block}}
@media (max-width:1100px){{.kap{{grid-template-columns:1fr}}.k-foto{{position:static;max-width:520px}}.farben{{grid-template-columns:1fr 1fr}}.zwei{{grid-template-columns:1fr}}.zimmer ul{{columns:1}}}}
</style></head><body>
<header><small>Beispielhaus · Tasty Studios · Hausakte</small><h1>Ihr Haus</h1><p>{e(h["kurz"])} Alle Fakten des Hauses stehen hier einmal; Website, Karten, Chat, Marke und Werkzeuge lesen davon.</p>
<nav>{"".join(f'<a href="#k{i+1}">{i+1:02d} {e(t)}</a>' for i, t in enumerate(["Das Haus","Geschichte","Firma","Zimmer","Tafel","Frühstück und Bar","Feiern","Regeln","Anreise","Marke","Werkzeuge"]))}</nav></header>
<main>{"".join(x.replace('<section class="kap">', f'<section class="kap" id="k{i+1}">', 1) for i, x in enumerate(teile))}</main>
</body></html>'''
open(os.path.join(HIER, 'konzept.html'), 'w', encoding='utf-8').write(seite)
print('konzept.html gebaut')
