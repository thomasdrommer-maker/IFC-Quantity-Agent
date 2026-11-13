# Entwicklungsstand vom 13.11.2026

[ZIP direkt herunterladen](https://github.com/thomasdrommer-maker/IFC-Quantity-Agent/raw/refs/heads/main/downloads/2026-11-13/IFC_Quantity_Agent_MVP1_UI_v0.3.7_Python314.zip)

Vollständiger Quellstand von `main`, Commit `31cfe03000b02ae0384c917c4c879c474d97f97e`. UI v0.3.7, API v1.1.0, Zielumgebung Windows/Python 3.14. Die Datumsablage kennzeichnet den Verpackungsstand, keine neue Anwendungsversion.

## Inhalt und Start

60 versionierte Dateien einschließlich Quellcode, UI, Tests/CI, Baseline, Regeln, OpenAPI, Entwicklungsauftrag, Agentenregeln, Fachkonzept v1.12 und Stahl-/Betonbau-Übergaben. Zusätzlich START_HIER.txt. Keine IFC-Dateien, Zugangsdaten, Git-Historie oder installierten Abhängigkeiten.

ZIP vollständig entpacken und `START_IFC_QUANTITY_AGENT.cmd` starten. Python 3.14 erforderlich; erste Einrichtung benötigt Zugriff auf den Python-Paketserver. Danach eigene IFC-Datei laden.

## Prüfen und weiterentwickeln

`docs/acceptance/IFC_Quantity_Agent_MVP1_UI_v0.3.7_Testplan.md` abarbeiten: Start, native Struktur, Baugruppen, Filter und Objektdetails/Scrollen. Die vollständige MVP-1-Abnahme ist noch offen.

Entwicklungsgrundlagen im Paket: `docs/entwicklungsauftrag.md`, `AGENTS.md`, `PROJECT_STATE.md` und `docs/concept/IFC_Quantity_Agent_Entwicklungskonzept_v1.12.md`.

## Paketprüfung

Alle 60 versionierten Dateien bytegleich zum Quellcommit übernommen und ZIP-Integrität geprüft. In dieser Verpackungsänderung wurde kein Anwendungscode geändert; keine neuen Funktionstests ausgeführt.

SHA-256: `077fcf42500ed2537627826d9901fced7e41d79abd12b0ce0adb5641e4eb097c`
