#!/usr/bin/env python3
"""Macht aus den gezeichneten Logo-Entwürfen (Tasty Studios Website/_quelle/haus/gen/logo/*.png, schwarz auf Papier) Vektoren:
Papier weg, Zeichnung beschneiden, potrace → Pfade, in ein 100×100-Feld gesetzt, Farbe currentColor.
Schreibt assets/marke/entwuerfe/<key>.svg und assets/marke/entwuerfe.json (für marke.py als Fassungen).   python3 logo_vektor.py"""
import os, re, json, subprocess, html
from PIL import Image, ImageOps
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__))
Q = os.path.expanduser('~/Desktop/Website-Projekte/Tasty Studios Website/_quelle/haus/gen/logo')
OUT = os.path.join(HIER, 'assets', 'marke', 'entwuerfe'); os.makedirs(OUT, exist_ok=True)
NAMEN = {'kran': 'Der Kran', 'speicher': 'Der Speicher', 'barkasse': 'Die Barkasse', 'laterne': 'Die Laterne', 'haken': 'Der Haken', 'poller': 'Der Poller'}
STIL = {'stich': 'als feiner Stich', 'linie': 'als klare Linie'}
SATZ = {'kran': 'Die Kräne stehen in jedem Fenster des Hauses.', 'speicher': 'Der Giebel des Speichers mit der Winde am First.', 'barkasse': 'Mit der Barkasse kommt man am Anleger an.',
        'laterne': 'Die Lampe am Eingang brennt, wenn Sie ankommen.', 'haken': 'Der Haken am Seil, der die Säcke in die Böden hob.', 'poller': 'Der Poller am Kai, an dem man festmacht.'}
AUS = {'barkasse-stich', 'speicher-stich', 'haken-stich', 'poller-linie'}   # Kreise, Siegel, Wappen und ein Knäuel: nach Roberts Regeln nicht zeigen
ent = []
for f in sorted(os.listdir(Q)):
    if not f.endswith('.png'): continue
    key = f[:-4]; motiv, stil = key.split('-')
    if key in AUS: continue
    im = Image.open(os.path.join(Q, f)).convert('L'); a = np.asarray(im).astype(int)
    # Tinte ist fast schwarz, Papier, Papierschatten und Tischgrund sind hell bis mittelgrau: Schwelle zwischen dunkelstem Wert und Papier
    papier = int(np.median(a)); dunkel = int(np.percentile(a, 0.2)); t = dunkel + int(.5 * (papier - dunkel))
    tinte = (a < t).astype(np.uint8)
    # nur die Zeichnung selbst: grösstes Stück plus alles, was in seiner Nähe liegt (kleine Siegel darunter fallen weg)
    import cv2
    n, lab, st, _ = cv2.connectedComponentsWithStats(tinte, 8)
    if n < 2: print('leer', key); continue
    gross = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x0, y0, w0, h0 = st[gross, :4]; box = [x0, y0, x0 + w0, y0 + h0]
    for _ in range(2):
        m = .08 * max(box[2] - box[0], box[3] - box[1]); drin = []
        for i in range(1, n):
            x, y, w, h, fl = st[i]
            if fl < 6: continue
            cx, cy = x + w / 2, y + h / 2
            if box[0] - m < cx < box[2] + m and box[1] - m < cy < box[3] + m: drin.append(i)
        box = [min(st[i, 0] for i in drin), min(st[i, 1] for i in drin), max(st[i, 0] + st[i, 2] for i in drin), max(st[i, 1] + st[i, 3] for i in drin)]
    halt = np.isin(lab, drin); tinte = tinte & halt
    x0, y0, x1, y1 = box; r = max(8, int(.04 * max(x1 - x0, y1 - y0)))
    box = (max(0, x0 - r), max(0, y0 - r), min(a.shape[1], x1 + r), min(a.shape[0], y1 + r))
    bw = Image.fromarray(np.where(tinte, 0, 255).astype(np.uint8)).crop(box)
    W, Hh = bw.size
    pbm = os.path.join(OUT, key + '.pbm'); bw.convert('1').save(pbm)
    svg = os.path.join(OUT, key + '.potrace.svg')
    subprocess.run(['potrace', '-s', '--turdsize', '12', '--alphamax', '1.0', '--opttolerance', '0.25', '-o', svg, pbm], check=True)
    s = open(svg).read()
    g = re.search(r'<g[^>]*transform="([^"]+)"[^>]*>(.*?)</g>', s, re.S)
    tr, paths = g.group(1), g.group(2)
    paths = re.sub(r'\s+', ' ', paths)
    k = 100 / max(W, Hh); tx = (100 - W * k) / 2; ty = (100 - Hh * k) / 2
    innen = f'<g fill="currentColor" stroke="none" transform="translate({tx:.2f} {ty:.2f}) scale({k:.6f})"><g transform="{tr}">{paths}</g></g>'
    open(os.path.join(OUT, key + '.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{innen}</svg>')
    os.remove(pbm); os.remove(svg)
    ent.append({'key': key, 'name': f'{NAMEN[motiv]} {STIL[stil]}', 'satz': SATZ[motiv], 'erkl': f'Gezeichnet {STIL[stil]}, als Vektor gesetzt. Steht allein auf Anhänger, Siegel und Serviette, neben der Wortmarke, wo Platz für beides ist.', 'innen': innen})
    print(key, f'{W}×{Hh}', len(innen) // 1000, 'kB')
json.dump(ent, open(os.path.join(HIER, 'assets', 'marke', 'entwuerfe.json'), 'w'), ensure_ascii=False)
print(len(ent), 'Entwürfe')
