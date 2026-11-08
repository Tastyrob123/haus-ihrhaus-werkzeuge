# Ihr Haus · die sieben Werkzeuge als Vorführung (Cloud-Bau, Robert 03.11.2026)

## Wozu
Tasty Studios verkauft Websites mit Werkzeugen für Hotels und Restaurants. Auf der Tasty-Studios-Seite gibt es den Bereich «Werkzeuge», ein Atelier: Ein möglicher Kunde sieht jedes Werkzeug, liest, was es tut, öffnet es und klickt sich darin herum. Diese sieben Werkzeuge werden hier gebaut, als **auslieferungsfertige Vorführung**. Das Beispielhaus ist «Ihr Haus», ein erfundenes Hotel in einem Speicher von 1888 am Sandtorkai in Hamburg (Website liegt in `Ihr Haus/`, alle Fakten in `Ihr Haus/haus.py`, Charakter in `Ihr Haus/CHARAKTER.md`).

Je Cloud-Sitzung genau **ein** Werkzeug. Welches, steht in deinem Auftrag und in `werkzeuge/<schlüssel>/AUFTRAG.md`.

## Die sieben Werkzeuge (Namen aus `haus.py` WERKZEUGE)
| Schlüssel (Ordner) | Name | Aufgabe | Vorlage in `Tastyrob123/haus-wildside` (`Walk on the Wild Side Hannover/_werkzeuge/…`) |
|---|---|---|---|
| `giebel` | Der Giebel | Zentrale: das Kontrollpanel, von dem aus man alle sechs anderen öffnet | `maison/` + `oberflaeche/` |
| `kontor` | Das Kontor | Website pflegen: Texte, Preise, Zeiten, Fotos | `bureau/` |
| `lagerbuch` | Das Lagerbuch | Karten: Tafel, Frühstück, Bar, Wochenmenü, als Karte und PDF | `carte/` |
| `winde` | Die Winde | Anfragen und Rezeption im Chat | `reception/` |
| `musterkammer` | Die Musterkammer | Marke: Bilder, Logo, Farben, Schriften, Markenbuch | `livre/` |
| `werkstatt` | Die Werkstatt | Drucksachen: Briefpapier, Tischkarten, Kofferetiketten, Aushänge, Feed | `imprimerie/` |
| `logbuch` | Das Logbuch | Besuche: wer die Website öffnet, woher, wie lange, was zur Buchung führt | `registre/` |

Die Vorlagen sind fertige, geprüfte Werkzeuge echter Häuser (`git clone --depth 1 https://github.com/Tastyrob123/haus-wildside /tmp/wild`). Aufbau, Wege und Funktionen von dort übernehmen, ins Kleid von Ihr Haus umziehen, mit Ihr-Haus-Inhalt füllen und zur reinen Vorführung umbauen (siehe unten). Vorgaben in `vorgaben/` (Werkzeug-Bau-Master: Abschnitte 4 Funktionen, 10 Tool-Datenbank, 10a Fehlerbuch Zeile für Zeile beachten).

## Die harte Grenze: alles ist Vorführung (Robert, wörtlich sinngemäss)
Der Kunde soll sich «ein bisschen klicken und probieren können, aber darf auf keinen Fall irgendwas an Daten, Informationen, Strukturen ändern, anpassen, speichern und nachhaltig verändern».
- **Reine statische Seiten.** Kein Server, kein Python zur Laufzeit, kein `/api`. Jedes Werkzeug ist `werkzeuge/<schlüssel>/index.html` mit eigenen CSS/JS-Dateien im eigenen Ordner und läuft mit jedem einfachen Dateiserver (`python3 -m http.server` im Ordner `werkzeuge/`).
- **Als erstes Skript im `<head>`:** `<script src="../_kleid/demo.js"></script>`. Es sperrt Netz, Speicher, Cookies, Downloads, Drucken, neue Fenster, mailto/tel und Formular-Versand. Nicht umgehen, nicht abschwächen.
- Dann `../_kleid/werkzeug.css` (Kleid) und `../_kleid/haus.js` (`window.HAUS`, alle Fakten). Bilder, Schriften, Logo nur aus `../_haus/` (`img/<name>-800.webp|-1400.webp`, Register `img/bilder.json`; `marke/zeichen.svg`, `wortmarke.svg`, `logo.svg` …).
- Änderungen des Kunden leben **nur im Arbeitsspeicher**. Neu laden = alles wieder wie vorher. Ein Knopf «Zurücksetzen» stellt den Anfangsstand auch ohne Neuladen her.
- **Die Website wird nie geöffnet.** Kein Knopf «Website ansehen», kein Link auf `Ihr Haus/…`, keine externe Adresse. Wo das echte Werkzeug die Website zeigen würde (Vorschau einer geänderten Seite, Karte auf der Website), zeigt das Werkzeug eine **eingebaute Vorschau** im eigenen Fenster: nachgebauter Ausschnitt mit Bildern aus `../_haus/`, als Bild oder Nachbau, nicht als iframe auf die Website.
- «Veröffentlichen», «Senden», «PDF herunterladen», «Drucken»: Die Handlung läuft sichtbar durch (Ladebalken, Häkchen, Vorschau, «So erscheint es auf Website, Karte, Chat»), dann `DEMO.hinweis('…')` mit einem ruhigen Satz. Es entsteht keine Datei und es geht nichts raus.
- KI-Antworten (Chat, Briefe, Texte) sind **vorgeschrieben** und werden abgespielt, als würden sie gerade geschrieben. Keine echte KI, keine Schlüssel.
- Das Logbuch zeigt erfundene, plausible Besuchszahlen. Sie sind als Beispiel gemeint und müssen nicht belegt sein; alles andere über das Haus kommt aus `haus.py`, nie erfunden.

## Umfang: reich, aber nicht überladen
Robert: «Die Werkzeuge müssen nicht überbordend sein mit 100 Vorlagen, sondern es reichen zu Demozwecken 10–15 verschiedene pro Kategorie.» Je Kategorie also **10 bis 15 verschiedene, voll ausgearbeitete Stücke** (Gerichte, Karten, Anfragen, Chatfragen, Drucksachen, Fotos, Tage …). Jede Kategorie, jeder Reiter, jedes Fenster ist gefüllt. Kein Platzhalter, kein Lorem, kein TODO, keine leere Kachel.

## Fertig heisst «auslieferungsfertig an die Tasty-Studios-Seite»
Das Werkzeug wird später auf der Tasty-Studios-Seite im Atelier geöffnet (eigenes Fenster bzw. iframe, 1440 bis 390 Pixel breit). Dafür liegt am Ende im eigenen Ordner:
1. `index.html` + eigene Dateien, alles funktioniert, alle vier Breiten 1440/1280/1000/390 sauber (Handy eigener Aufbau, nichts abgeschnitten, nichts quer scrollend).
2. `STECKBRIEF.md`: Name, eine Zeile «was es tut» in Kundensprache, 4 bis 6 Fähigkeiten als kurze Sätze (je höchstens 12 Wörter), die drei eindrucksvollsten Handgriffe für einen Rundgang.
3. `ZUSTAENDE.md` + Sprungadressen: Jeder wichtige Zustand ist per `index.html#<zustand>` direkt aufrufbar (z. B. `#karte-tafel`, `#chat`). Die Datei listet 4 bis 6 Zustände, die als Bild im Atelier gut aussehen, und je ein Bildschirmfoto `bilder/<zustand>-1440.png` und `-390.png`.
4. Im Giebel steht das Werkzeug als Kachel und öffnet sich über `../<schlüssel>/index.html`.

## Gestaltung
- Kleid von Ihr Haus, nicht die Vorlage umgefärbt: Nacht `#10151d`, Leinen `#efe7da`, Licht `#e2ae68` nur als Linie und Knauf, Messing `#a8844f` für kleine Schrift und Linien, Backstein `#8c4b34` sparsam, Flaschengrün `#16221d` nur für die Tafel. Titel Cormorant Garamond 500 (nie fett, nie kursiv), Text Instrument Sans. Nur Variablen aus `werkzeug.css` für Flächen.
- Knöpfe mit Tiefe und rundem Pfeil-Knauf (`.kn`). Keine Einkerbungen, keine Punkt-Etiketten über Überschriften, keine Pillen-Reihen als Schmuck, keine grauen Kachel-Raster, keine Emojis.
- Nichts der Vorlage darf sichtbar bleiben: `grep -rIn -i "wild side\|wildside\|culinarium\|momo\|derya\|prata\|hanken\|linden\|F0323F\|D8B264" werkzeuge/<schlüssel>` muss leer sein.
- Texte: Deutsch, ruhig, Wertigkeit (Sorgfalt, der einzelne Gast). Nie nach Masse, Abfertigung, Fliessband klingen. Keine Marketing-Floskeln.
- Beim Öffnen sind Schrift und alle sichtbaren Bilder gleichzeitig da (Seite bleibt unsichtbar, bis die Bilder im ersten Bild geladen sind, Bilder dort mit `decoding="sync"`, CSS-Rückfall nach 3 s). Bewegung nur über `transform`/`opacity`.

## Arbeitsweise in der Cloud
- Modell Opus. Keine Fragen an Robert, er schläft oder ist unterwegs. Offenes in die Schlussmeldung.
- **Nur im eigenen Ordner `werkzeuge/<schlüssel>/` schreiben.** `_kleid/`, `_haus/`, `Ihr Haus/` nur lesen. Braucht dein Werkzeug etwas Gemeinsames, löse es im eigenen Ordner. Ausnahme: der Giebel darf `_kleid/werkzeug.css` ergänzen (nur ergänzen, nichts umbenennen).
- Prüfen selbst, headless: `cd werkzeuge && python3 -m http.server 8800 &`, dann mit Playwright/Chromium jeden Navigationspunkt, jeden Reiter, jedes Fenster in 1440/1280/1000/390 aufnehmen und mindestens 20 Bilder mit dem Read-Werkzeug ansehen. Konsole ohne Fehler (abgesehen von den gewollten «Vorführung»-Sperren). Zusätzlich prüfen: nach Änderungen und Neuladen ist alles wie vorher; kein Element führt aus dem Werkzeug heraus.
- Eigene Prozesse per PID beenden, nie `pkill`/`killall`.
- Commit und Push auf deinen eigenen Zweig, oft, mit kurzer deutscher Nachricht («Lagerbuch: Karten fertig»). Kein Force, nichts in andere Ordner. Am Ende: letzte Nachricht `<Name>: fertig` und eine kurze Schlussmeldung in der Sitzung: fertig/nicht fertig, Zweig, was offen ist. Keine Begründungen.
- Nichts verschicken, nichts veröffentlichen, nichts online stellen, nichts bezahlen.

## Limit und Übergabe (Robert 04.11.2026, gilt für jeden Chat in jedem Profil)
- Jeder Chat in diesem Repo hält `UEBERGABE-LIMIT.md` im Stamm **laufend** aktuell: nach jedem fertigen Schritt nachführen, committen, pushen. Inhalt: Auftrag, was fertig ist (mit Links), was offen ist in Reihenfolge, der nächste genaue Schritt, Zweige, Prüfstand, Stolpersteine. Ein Chat in einem anderen Profil macht allein mit dieser Datei nahtlos weiter.
- `.claude/limit/` meldet sich von selbst, wenn das 5-Stunden- oder Wochenlimit fast erreicht ist (ab 95 % / 97 %, letzte Warnung ab 98 % / 99 %). Dann sofort die Übergabe vollständig schreiben und pushen, erst danach weiter.
- **Weitermachen in einem anderen Profil:** neue Cloud-Sitzung auf diesem Repo, erster Satz: «Lies UEBERGABE-LIMIT.md und mach dort weiter.» Der neue Chat liest zuerst diese Datei, dann CLAUDE.md, und setzt beim «nächsten genauen Schritt» an.

## Lebenszeichen und nicht aufhören (Robert 09.11.2026)
- `.claude/limit/lebenszeichen.sh` pusht höchstens alle 10 Minuten `LEBENSZEICHEN`, solange gearbeitet wird. Bleibt es 20 Minuten aus, startet die Wache am Mac eine Folgesitzung («Lies UEBERGABE-LIMIT.md und mach dort weiter»). Nie abschalten.
- Nie aufhören, solange der Auftrag offen ist: Unteragenten abwarten, weiterbauen. Erst wenn alles fertig und geprüft ist, beginnt `UEBERGABE-LIMIT.md` mit «Fertig. …» (oder «Nicht fertig. …» mit Grund). Der Stop-Hook `.claude/limit/nicht-aufhoeren.sh` hält die Sitzung sonst an der Arbeit.
