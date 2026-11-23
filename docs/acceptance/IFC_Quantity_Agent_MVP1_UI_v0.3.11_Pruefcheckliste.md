# Prüfcheckliste Nutzerabnahme UI v0.3.8 bis v0.3.11

Nur Prüfliste; keine Änderung an Code, Regeln oder Baseline. Keine IFC-Dateien oder sensiblen Daten im Repo ablegen.
Legende: ☐ offen · ☑ passt · ✗ Abweichung · n/a nicht prüfbar.

Prüfer/Datum: ______ · IFC (nur Name): ______ · Python: ______

## 0. Vorbereitung je Version
- ☐ ZIP in neuen Ordner entpacken, SHA-256 mit `downloads/2026-11-16/README.md` vergleichen.
- ☐ `START_IFC_QUANTITY_AGENT.cmd`: keine DLL-Fehler, Umgebung unter `%LOCALAPPDATA%\IQA`.
- ☐ Richtige Version links oben (ab v0.3.10 auch im Konsolenbanner).

## 1. v0.3.8 – Auffindbarkeit
| # | Schritt | Erwartet | ☐ |
|---|---|---|---|
| 1.1 | Projektübersicht „Modellstruktur öffnen →“ | Struktur direkt offen, erste Baumebene sichtbar | ☐ |
| 1.2 | Buttons IFC-Struktur / Baugruppen / LV-Ident-Gruppen | Aktive Ansicht markiert, Wechsel ohne Dropdown | ☐ |
| 1.3 | Baugruppen bei Modell ohne Baugruppen | „Keine Baugruppen im Modell vorhanden.“ (nur Leerzustand) | ☐ |
| 1.4 | Suche (Name/GlobalId/STEP-ID), leeren | Treffer korrekt, danach voller Baum | ☐ |
| 1.5 | Klassen-/Materialfilter anwenden, zurücksetzen | Filter wirken und lassen sich zurücksetzen | ☐ |
| 1.6 | LV-Ident-Gruppen | Werte und leere Felder getrennt, keine Auto-Klassifizierung | ☐ |
| 1.7 | Objekt anklicken | Richtige Details, PSets/Mengen; Liste/Details getrennt scrollbar | ☐ |

## 2. v0.3.9 – Zuklappen
| # | Schritt | Erwartet | ☐ |
|---|---|---|---|
| 2.1 | Mehrere Untergruppen aufklappen | Zweige offen | ☐ |
| 2.2 | „Untergruppen zuklappen“ bei einer Gruppe | Gruppe bleibt offen, Untergruppen schließen, andere Zweige unverändert | ☐ |
| 2.3 | „Alle Gruppen zuklappen“ | Alle Gruppen der Ansicht schließen | ☐ |
| 2.4 | Wieder öffnen, Objekt anklicken | Baum und Details korrekt | ☐ |
| 2.5 | Wiederholen in LV-Ident-/Baugruppenansicht, mit Suche/Filter | Gleiches Verhalten | ☐ |

## 3. v0.3.10 – Einstieg und IFC-Identität
| # | Schritt | Erwartet | ☐ |
|---|---|---|---|
| 3.1 | Einstieg vor Upload | „IFC-Modell öffnen und prüfen“, kein Z445-Bezug | ☐ |
| 3.2 | Bekanntes Objekt suchen | IfcClass, IfcName, IfcDescription, IfcObjectType = Originalmodell | ☐ |
| 3.3 | Leeres Attribut | „Nicht angegeben“, nichts ergänzt | ☐ |
| 3.4 | „IfcDescription / IfcObjectType anzeigen“ aus/an | Kompakt bzw. beide Felder wieder da | ☐ |
| 3.5 | Suche nach Description-/ObjectType-Text (auch ausgeblendet) | Objekt gefunden | ☐ |
| 3.6 | Zuklappen, Drilldown | Unverändert | ☐ |

## 4. v0.3.11 – BIM_Core-Quellen
Beispiel: Objekt „Konsole“ (STEP-ID 365).
| # | Schritt | Erwartet | ☐ |
|---|---|---|---|
| 4.1 | Objekt suchen | Gefunden | ☐ |
| 4.2 | Description/ObjectType | „Betonunterzug_b30“ / „Stahlbetonunterzug“ mit Quelle BIM_Core und Hinweis auf leeres natives Attribut | ☐ |
| 4.3 | Name | Nativ „Konsole“ und BIM_Core „Unterzug_b30“ getrennt, nicht gleichgesetzt | ☐ |
| 4.4 | Klasse | Native IfcClass nicht durch BIM_Core.IfcClass überschrieben; Abweichung daneben ausgewiesen | ☐ |
| 4.5 | Objekt mit abweichenden Werten | Beide Werte sichtbar (Konflikt), keine Umklassifizierung | ☐ |
| 4.6 | Suche „Stahlbetonunterzug“ | Objekt auffindbar | ☐ |
| 4.7 | Zusatzangaben aus/an, Zuklappen, Drilldown | Funktioniert, Quelle erkennbar | ☐ |

## 5. Offene Altpunkte
| # | Punkt | Erwartet / Stand | ☐ |
|---|---|---|---|
| 5.1 | v0.3.7 Punkt 3: Baugruppen | **Modell fehlt.** Bekannte Assembly aufklappen, mit Modellansicht vergleichen; Zahl nicht addieren; wiederholte Verweise keine neuen Objekte; keine Mengensummen; Doppelzählung prüfen | ☐ |
| 5.2 | v0.3.7 Punkt 4: Fehlende Zuordnungen/Filter | „Ohne direkte räumliche Zuordnung“ (kann Einzelteile enthalten), Suche, Filter, LV-Ident | ☐ |
| 5.3 | v0.3.7 Punkt 5: Objektdetails | Name, Klasse, STEP-ID, PSets, QTOs; Hinweis bei fehlender/doppelter GlobalId; getrenntes Scrollen | ☐ |
| 5.4 | Z445-Referenzlauf | Original-IFC in freigegebener Umgebung, unveränderter Dateiname; erwartet 32/32, keine übersprungenen Referenzprüfungen | ☐ |
| 5.5 | `python -m unittest discover -s tests -v` (Python 3.14; CI 3.12) | Grün; ohne Original-IFC 2 Referenzprüfungen übersprungen | ☐ |
| 5.6 | Gesamt-MVP-1-Abnahme | Erst nach 5.1–5.5 | ☐ |

## 6. Rückmeldungen / Befunde
| Nr. | Version | Schritt | Objekt / STEP-ID | Erwartet | Beobachtet |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

Gesamturteil: v0.3.8 ☐ passt ☐ Abweichung · v0.3.9 ☐ · v0.3.10 ☐ · v0.3.11 ☐

Freitext:
