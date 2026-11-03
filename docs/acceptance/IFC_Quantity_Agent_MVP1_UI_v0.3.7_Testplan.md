# Testplan UI v0.3.7

Stand: 03.11.2026 · Autor: OpenAI Codex · Status: Nutzerprüfung offen

## 1. Start und Umgebung

ZIP in einen neuen Ordner entpacken und `START_IFC_QUANTITY_AGENT.cmd` starten. Die Konsole soll einen kurzen Umgebungspfad unter `%LOCALAPPDATA%\IQA` zeigen; keine DLL-Fehlermeldung. Links oben muss **UI v0.3.7** stehen. Die erste Einrichtung benötigt Zugriff auf den konfigurierten Python-Paketserver; beim zweiten Start keine erneute Paketinstallation. Alte `.venv314` nicht kopieren oder löschen.

## 2. Native Modellstruktur

Aktuelle Z445-IFC laden und **Modellstruktur → IFC-Struktur** wählen. Projekt/Standort/Bauwerk/Geschoss soweit im Modell vorhanden aufklappen. Erwartet: Namen und Klassen entsprechen den tatsächlich exportierten IFC-Objekten. Fehlende Ebenen werden nicht erfunden. Beziehungen tragen IFC-Beziehungstyp und STEP-ID.

## 3. Baugruppen und Zählung

**Baugruppen** wählen und eine bekannte Assembly aufklappen. Enthaltene Objekte mit unabhängiger Modellansicht vergleichen. Die Zahl der Assemblies ist bereits in den IFC-Elementen enthalten; Zahlen nicht addieren. Wiederholte Verweise auf dasselbe Objekt sind keine zusätzlichen Objekte. Die Modellstruktur summiert keine Mengen.

## 4. Fehlende Zuordnungen und Filter

**Ohne direkte räumliche Zuordnung** prüfen: Hier können auch Einzelteile erscheinen, deren Baugruppe räumlich zugeordnet ist. Suche nach bekanntem Namen/GlobalId/STEP-ID testen, dann Suche leeren. IFC-Klassen- und Materialfilter einzeln anwenden und zurücksetzen. **LV-Ident-Gruppen** zeigt vorhandene Werte und leere Felder getrennt; es gibt keine neue automatische Klassifizierung.

## 5. Objektdetails und bisherige Bedienung

Einen Objektnamen im Baum anklicken. Erwartet: korrekter Name, Klasse, STEP-ID, PSets und QTOs im Objekt-Drilldown. Bei fehlender oder doppelter GlobalId steht ein Hinweis; Finding-Zuordnung bleibt dann bewusst offen. Zur Modellstruktur zurückwechseln. Objektliste und Details weiter getrennt scrollbar, Filter und Tabellenköpfe bleiben sichtbar.

## Rückmeldung

Punkte 1–5 jeweils mit „passt“ oder konkreter Abweichung melden. Bei einer Strukturabweichung Objektname, STEP-ID, erwartete Beziehung und Screenshot angeben. Die ursprüngliche eingefrorene Z445-Referenzdatei wird weiterhin separat für Software-Regression benötigt; der aktuelle Export ersetzt die Baseline nicht automatisch.

## Abschluss

Nach Nutzerprüfung Ergebnisse dokumentieren, verbleibende Abweichungen korrigieren und die vollständige MVP-1-Abnahme vornehmen. Danach PR/Tests prüfen und den abgenommenen Stand konsolidieren. Gemeinsamer Regel-/Profilkern folgt anschließend; GCC-Mapping bleibt nachrangig.
