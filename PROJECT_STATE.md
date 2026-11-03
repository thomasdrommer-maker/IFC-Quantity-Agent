# IFC Quantity Agent – Projektstatus

**Stand:** 03.11.2026  
**Entwicklungskonzept:** [v1.12](docs/concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md)  
**Implementierungspaket:** v0.3.6  
**API-Vertrag:** v1.0.0  
**Regelpaket:** IQA-M1-Z445-ECA v0.1.0

## Fertiggestellt

- Z445-ECA-Inventur und prüfbare MVP-1-Abnahmebasis
- maschinenlesbare Referenzbaseline
- 32 stabile MVP-1-Regel-IDs
- deterministischer IFC-Collector auf Basis von IfcOpenShell
- CLI-Regressionslauf mit JSON- und JUnit-Ausgabe
- plattformneutraler Application Service
- REST-/OpenAPI-Adapter
- Projektübersicht, Regelresultate, Findings, Objektliste und Objekt-Drilldown als API
- Quellenabgrenzung für natives `NetVolume`
- 14 automatisierte Tests, davon ein vollständiger Z445-End-to-End-Test
- Ergebnis am Referenzmodell: 32/32 Regeln bestanden
- erste browserbasierte MVP-1-Oberfläche mit IFC-Upload
- Projektübersicht, filterbarer Prüfbericht, Objektliste und Objekt-Drilldown
- Mehrfachauswahl über GlobalIds mit vorbereitetem Selektionsereignis `iqa:select-objects`
- sichtbare Leerzustände für die weiteren Konzeptansichten
- Windows-Zielbetrieb mit Python 3.14 und IfcOpenShell 0.8.4.post1
- CI-Kompatibilitätsmatrix für Python 3.12 und 3.14
- vollständiger Z445-End-to-End-Lauf unter Python 3.14.8: 15/15 Tests und 32/32 Regeln bestanden
- UI v0.3.2: SHA-256-Identität und Referenzabweichungen explizit kennzeichnen; Regelquote als Referenzvergleich benennen
- UI v0.3.3: IFC-Schema und Export-/Erstellungszeitpunkt aus `FILE_NAME.TIME_STAMP` in der Projektübersicht anzeigen, ohne eine Zeitzone anzunehmen

## Bewusste MVP-Grenzen

- Analyseergebnisse werden noch im Arbeitsspeicher gehalten.
- Analyse läuft synchron.
- noch keine Datenbank, Authentifizierung oder Rollenverwaltung
- noch keine 3D-Geometrieausgabe
- noch keine integrierte 3D-Modellansicht; Selektion ist als GlobalId-Schnittstelle vorbereitet

## Nächster Schritt

MVP-1-UI anhand des Z445-Modells fachlich und visuell prüfen. Danach Mengenübersicht und 3D-Viewer-Adapter über die vorbereitete GlobalId-Selektion ergänzen.

## Referenzmodell

`Z445_799_ECA_BM_801_3D.ifc` wird nicht im Repository gespeichert. Für den lokalen End-to-End-Test wird der Pfad über `IFC_MVP1_REFERENCE_MODEL` gesetzt.


## UI v0.3.4 – Aktualisierung eindeutig erkennen

- Versionsnummer in der Seitenleiste, versionierte Asset-URLs
- Schema, IFC-Zeitstempel und Referenzstand direkt oberhalb der Kennzahlen
- Starter reserviert einen freien Port und öffnet den Browser erst nach Serverbereitschaft; keine Weiterleitung auf einen älteren Prozess


## Fachübergabe v0.2 / Auftrag v1.12 – 01.11.2026

- Beide vollständigen Originalpakete in [docs/handover](docs/handover/README.md) übernommen; zehn Dateien mit SHA-256-Manifest und bytegleichen ZIP-Inhalten.
- Gesamtauftrag auf v1.12 fortgeschrieben; Stahl-/Betonkategorien sowie PR01–PR20 für eigene Profile verbindlich eingeordnet.
- Schwerpunkt: Stützenquerschnitte/-höhen, Wanddicken/-höhen und Blechdicken/-flächen/-massen; exakte Maße parallel zu Intervallen.
- Profilengine, API-/UI-Verwaltung und Excel-/JSON-Konfigurationsaustausch sind noch offen. Je Paket 32 fachliche und 20 Profil-Sollfälle sind noch als Integrationstests umzusetzen.
- Keine Änderung an Collector, Baseline, aktiven MVP-1-Regeln, Anwendungsversion oder OpenAPI. Fachpakete nicht automatisch aktiv laden.
- Nach MVP-1-Abnahme gemeinsamen Profilkern entwickeln; Integration in Stahlbau MVP 3 und Betonbau MVP 4. Modellcode-Mapping und Mengenquellen des Gesamtauftrags bleiben maßgebend.

## UI-Abnahmefeedback und v0.3.5 – 02.11.2026

- Nutzer bestätigt v0.3.4, Metadaten/Referenzanzeige und unabhängige Element-/Assemblyzahlen. Objektbezug und tatsächliche PSets/QTOs vorläufig bestätigt.
- Beanstandung: JSON-Blöcke zu klein und schlecht lesbar. v0.3.5 zeigt PSet-Gruppen als aufklappbare Tabellen und Mengen mit Einheit, Quelle sowie exaktem Rohwert. Roh-JSON bleibt optional. Anzeige rundet nur Zahlenformat auf maximal 6 Dezimalstellen; Collector/Regeln/Baseline unverändert.
- Lesbarkeitsabnahme v0.3.5 und Modellstruktur weiterhin offen; keine vollständige MVP-1-Freigabe.

## UI v0.3.6 – Scrollbereiche der Objektansicht

- Nutzer bestätigt PSet-Tabellen, Mengenanzeige und aufklappbare Rohwerte in v0.3.5.
- Korrektur: Objektansicht auf Fensterhöhe begrenzen; Filterleiste außerhalb der scrollenden Tabelle, gesamter Tabellenkopf bleibt sichtbar. Objektdetails scrollen unabhängig, Objekttitel bleibt stehen.
- Für kleine Fenster werden Liste und Details als zwei begrenzte Bereiche übereinander angezeigt. Beim Wechsel der Ansicht wird das normale Seitenlayout wiederhergestellt.
- Keine Änderungen an API, Collector oder Mengen-/Referenzregeln. Vollständige MVP-1-Abnahme weiterhin offen (Modellstruktur).

- Browser-Regression v0.3.6 lokal bestanden: 1500×900, 1280×720, 1280×600, 1024×768, 390×844; 600 Objekte und 20 aufgeklappte PSet-Gruppen. Listenende, Detailende, feststehende Filter/Spaltenköpfe und Rückkehr zur Projektübersicht geprüft. Neuer CI-Job `object-layout`.
- Die PSet-Gruppen bilden zusätzlich den Positionierungsrahmen für unsichtbare Tabellenbeschriftungen. Ohne diesen Rahmen können lange Detailinhalte eine unsichtbare zusätzliche Seitenhöhe erzeugen; der Browsertest prüft deshalb auch die Dokumenthöhe.

## Nutzerabnahme Scrollkorrektur – 03.11.2026

- Tom bestätigt: „Scrollprüfung von v0.3.6 funktioniert“. Scrollkorrektur der Objektansicht damit nutzerseitig bestätigt.
- Keine vollständige MVP-1-Freigabe: Modellstrukturansicht und abschließender Gesamtcheck weiterhin offen.
- Zusätzlich offen: Starter gegen lange Windows-Installationspfade absichern (DLL-Ladefehler im langen, doppelt verschachtelten Paketpfad).
- Nächster Funktionsschritt: reale räumliche IFC-Struktur und Assembly-Beziehungen darstellen; fehlende Zuordnungen sichtbar halten und Objekte zum Drilldown verknüpfen. Danach MVP-1-Abnahme und Konsolidierung.
