# Ihr Haus — Charakterblatt

**Geschichte in einem Satz:** Ein Speicher von 1888 am Sandtorkai, in dem früher Kaffee und Tabak lagerten und heute zwölf Gäste über dem Wasser schlafen; die Seite geht vom Kai durchs Haus hinauf und wieder hinaus ans Wasser.

**Register:** ruhig, warm, nachts. Backstein, Eiche, Messing, Leinen, Flaschengrün. Kein Glanz, kein Spielzeug.

**Marke:** Wortmarke «IHR HAUS / Am Hafen · Hamburg» in Cormorant Garamond, gesperrt. Grundton Nacht #10151d, Leinen #efe7da, Licht #e2ae68 (nur Linie und Knauf), Messing #a8844f, Flaschengrün #16221d (nur die Tafel). Lesetext Instrument Sans.

**Fakten (eine Wahrheit, gleich wie `Tasty Studios Website/_varianten/runde3/ihrhaus.py`):** Sandtorkai 7, 20457 Hamburg · seit 1888 · zwölf Zimmer auf fünf Böden · Speicherzimmer 22 m² ab 159 € · Zimmer zum Wasser 28 m² ab 189 € · Kranzimmer 34 m² ab 229 € · Dachsuite 48 m² ab 340 € · Die Tafel Donnerstag bis Samstag ab 19 Uhr, fünf Gänge.

**Je Abschnitt (Anordnung · tragende Bewegung):**
- Auftakt: Fassade vom Wasser, Kamerafahrt 3 s, Titel aus dem Schlitz, Buchungsleiste in Leinen.
- Empfang: Tür hoch, Theke breit, Satz neben der Halle · als Fläche gemeinsam hoch, Bilder setzen sich.
- Fenster 1 (Fensterbank) und Fenster 2 (Speicherstadt): Ausschnitt geht auf, Satz rollt.
- Zimmer auf Leinen: vier Zimmerarten als Reiter, grosses Bild + drei kleine zum Antippen · neues Bild steigt im Rahmen auf, Linie fliesst.
- Die Tafel auf Flaschengrün: Karte von heute Abend, der gewählte Gang zeigt seinen Teller · Gänge staffeln sich hoch.
- Anreise: die Fähre gross, drei Wege, Koffer und Räder · Wege staffeln sich.
- Schluss: der Speicher am Kanal bei Nacht, zwei Knöpfe.

**Bilder:** erzeugt (Robert 02.11.2026), `Tasty Studios Website/_quelle/haus/gen40.py` und `gen.py`. Webgrössen: `python3 bilder.py`, Seite: `python3 bau.py`, Prüfung: `node _qa/ansicht.js <ordner>`.

**Marke (02.11.2026):** `marke.py` baut Zeichen (Winde am Giebel, Linie), Wortmarke als Pfade aus Cormorant 500, Logo gestapelt und in der Zeile, Tapete Backstein im Verband, Farbkarten → `assets/marke/`; Markenbuch `marke/markenbuch.html` (12 Blätter, druckbar). Schriften liegen lokal in `assets/fonts/`.

**Unterseiten (02.11.2026):** `bau.py` baut jetzt index, zimmer, tafel, anreise, kontakt, impressum aus `haus.py`; Leiste und Fuss führen auf echte Seiten, Fuss mit dem Zeichen (Kran). Jede Unterseite: Kopfbild mit Kamerafahrt, eigene Komposition (Zimmer: Kapitel je Zimmerart mit wechselnden Seiten · Tafel: Karte der Woche als Bildreihe, Herkunft, Frühstück, Bar, Feiern · Anreise: fünf Wege im Wechsel, Umgebung, Regeln · Kontakt: Anfrage-Fenster mit vier Arten, noch ohne Server). Schriften lokal.
