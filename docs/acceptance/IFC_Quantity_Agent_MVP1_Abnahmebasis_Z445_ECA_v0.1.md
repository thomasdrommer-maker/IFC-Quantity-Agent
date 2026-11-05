# IFC Quantity Agent – MVP-1-Abnahmebasis

**Referenzmodell:** `Z445_799_ECA_BM_801_3D.ifc`  
**Dokumentversion:** 0.1  
**Stand:** 21.10.2026  
**Fachliche Grundlage:** Entwicklungskonzept v1.11  
**Zweck:** Prüffähige Sollbasis für Implementierung, Test und Abnahme von MVP 1

## 1. Abnahmeziel

MVP 1 ist abnahmefähig, wenn der IFC Quantity Agent das Referenzmodell reproduzierbar einliest, die unten definierten Modellfakten ohne stille Umdeutung ermittelt und sie in Projektübersicht, Modellstruktur, Befundliste und Objekt-Detailansicht nachvollziehbar darstellt.

Die Abnahme bewertet in MVP 1 noch **keine fachliche Freigabe von Mengen oder Kosten**. Sie bewertet die robuste Inventur, Transparenz, Rückverfolgbarkeit und korrekte Kennzeichnung von Auffälligkeiten.

## 2. Prüfgrundlagen

| Grundlage | Festlegung |
| --- | --- |
| Entwicklungskonzept | `01-IFC_Quantity_Agent_Entwicklungskonzept_v1.11-1-.md` |
| IFC-Referenzdatei | `Z445_799_ECA_BM_801_3D.ifc` |
| SHA-256 | `1b8e679b9a43691b0574a0de5fd675c679f42bc4a05320703c64bdc527d72523` |
| Dateigröße | 1.133.708 Byte |
| IFC-Schema | IFC4 |
| Export | IFC Manager for SketchUp 5.5.4 / SketchUp 2025 |
| ViewDefinition | ReferenceView_V1.2 |
| Exportzeitstempel | 2026-10-05T16:39:23 |

Der Hash ist vor jedem Wiederholungs- oder Regressionstest zu prüfen. Bei abweichendem Hash gelten die Zahlenwerte dieses Dokuments nicht automatisch als Sollwerte für die neue Datei.

## 3. Abgrenzung

### Bestandteil von MVP 1

- IFC-Datei öffnen und technische Metadaten anzeigen
- Einheiten und räumliche Struktur erfassen
- physische Elemente und Baugruppen inventarisieren
- GUID-Prüfung auf fehlende und doppelte Werte
- IFC-Klassen, Geometrie, Psets, QTOs und Materialien inventarisieren
- unklassifizierte bzw. prüfbedürftige Objekte sichtbar machen
- Befunde mit Objektbezug und Drilldown darstellen
- Ergebnisse reproduzierbar und ohne erfundene Ersatzwerte ausgeben

### Nicht Bestandteil von MVP 1

- Excel-Export oder Excel-ähnliche Tabellenbearbeitung
- regelbasierte automatische Umklassifizierung
- automatische Korrektur des IFC-Modells
- LV-Zuordnung oder Mengenfreigabe
- Preis-, Kosten- oder Abrechnungslogik
- verbindliche ECA-Fachprüfung über die reine Modellinventur hinaus

## 4. Verbindliche Referenzwerte

### 4.1 Modell- und Objektbestand

| Merkmal | Sollwert |
| --- | ---: |
| STEP-Entities | 6.966 |
| `IfcProduct` | 205 |
| `IfcElement` | 202 |
| Elemente mit Repräsentation | 166 |
| Elemente ohne Repräsentation | 36 |
| `IfcRoot` mit GlobalId | 1.465 |
| doppelte GlobalIds | 0 |
| Elemente mit genau einer räumlichen Zuordnung | 175 |
| Elemente ohne räumliche Zuordnung | 27 |

### 4.2 IFC-Klassen

| IFC-Klasse | Sollwert |
| --- | ---: |
| `IfcBuildingElementProxy` | 77 |
| `IfcElementAssembly` | 36 |
| `IfcColumn` | 30 |
| `IfcFooting` | 20 |
| `IfcWall` | 14 |
| `IfcBeam` | 11 |
| `IfcSlab` | 11 |
| `IfcOpeningElement` | 3 |
| **Summe `IfcElement`** | **202** |

### 4.3 Raumstruktur und Einheiten

| Merkmal | Sollwert |
| --- | --- |
| `IfcSite` | 1 – `default site` |
| `IfcBuilding` | 1 – `default building` |
| `IfcBuildingStorey` | 1 – `default building storey` |
| `IfcSpace` | 0 |
| Längeneinheit | Millimeter |
| Flächeneinheit | Quadratmeter |
| Volumeneinheit | Kubikmeter |

### 4.4 Property- und QTO-Abdeckung

| PropertySet / QuantitySet | Elemente mit Set |
| --- | ---: |
| `BASF_General` | 87 |
| `QTO` | 84 |
| `PropertySets` | 66 |
| `BASF_General_GUID` | 59 |
| `BIM_Core` | 59 |
| `BASF_GCC` | 45 |
| `Qto_ColumnBaseQuantities` | 30 |
| `Pset_QuantityTakeOff` | 29 |
| `Qto_WallBaseQuantities` | 14 |
| `Qto_BeamBaseQuantities` | 11 |
| `Qto_SlabBaseQuantities` | 11 |
| `QuantityTakeOff` | 3 |

### 4.5 LV-Kennzeichnung

Für `BASF_General.540_LV_Ident` gelten **81 befüllte** und **121 leere/fehlende** Werte.

| Wert | Anzahl |
| --- | ---: |
| Stütze | 30 |
| Einzelfundament | 14 |
| Unterzug | 11 |
| Außenwand | 11 |
| Decke | 7 |
| Streifenfundament | 4 |
| Innenwand | 3 |
| Bodenplatte | 1 |
| leer/fehlend | 121 |

Hinweis zur Datenbereinigung der Analyse: Die Summe der befüllten Werte beträgt 81. Eine frühere Arbeitsnotiz mit 78 war ein Additionsfehler und ist nicht als Sollwert zu verwenden.

### 4.6 Weitere Schlüsselfelder

| Feld | Sollbefund |
| --- | --- |
| `BASF_General.701_Bruttovolumen` | 81 vorhanden, 121 fehlend |
| `BASF_General.604_Bruttogewicht` | bei allen 202 Elementen fehlend |
| `BASF_General.550_Baunummer` | bei allen 202 Elementen fehlend |
| `BASF_General.504_Planungsstand` | 86 × `In_Planung`, 116 fehlend |
| `BIM_Core.IfcClass` | 59 vorhanden, 143 fehlend |
| natives `Name` | bei allen 202 Elementen vorhanden |
| natives `Description` | bei allen 202 Elementen fehlend |
| natives `ObjectType` | bei allen 202 Elementen fehlend |
| natives `Tag` | 125 vorhanden, 77 fehlend |

Das Property `BIM_Core.IfcClass` ist als Zusatzinformation anzuzeigen. Es darf die native IFC-Klasse nicht überschreiben.

### 4.7 Materialien

| Materialbezeichnung | Anzahl Zuordnungen |
| --- | ---: |
| Stahlbeton | 113 |
| HAUFF_WDF | 16 |
| WDF | 8 |
| `#1E90FF` | 8 |
| Stahl_EBT | 7 |
| RC0-32 | 3 |
| Stahlbeton_Sauberkeitsschicht | 3 |
| Default | 2 |
| Pumpensupf | 2 |
| Farbe D07 | 1 |

### 4.8 Baugruppen und Öffnungen

| Merkmal | Sollwert |
| --- | ---: |
| `IfcElementAssembly` | 36 |
| Assemblies mit eigener Repräsentation | 0 |
| Assembly-Elternbeziehungen | 5 |
| darin referenzierte Kinder | 27 |
| `IfcOpeningElement` | 3 |
| `IfcRelVoidsElement` | 0 |

Die drei Öffnungsobjekte heißen `KÄLTE_WDF`, besitzen aber keine `IfcRelVoidsElement`-Verknüpfung. Das ist als Prüfhinweis darzustellen, nicht automatisch zu reparieren.

## 5. Mengenbezogene Referenzbefunde

### 5.1 Abdeckung und Summen

- 66 Objekte besitzen sowohl `BASF_General.701_Bruttovolumen` als auch ein natives `NetVolume`.
- Summe Bruttovolumen dieser 66 Objekte: **392,64 m³**.
- Summe Netto-Volumen dieser 66 Objekte: **347,3087246361 m³**.
- Differenz: **45,3312753639 m³**.
- Wo sowohl `BASF_General.701_Bruttovolumen` als auch `QTO.01_Bruttovolumen_m3` vorhanden sind, stimmen die Werte überein.

Die Differenz zwischen Brutto- und Netto-Volumen ist allein kein Fehler. MVP 1 muss unterschiedliche Bedeutungen und Quellen getrennt halten und darf keine Quelle stillschweigend zur „richtigen“ Menge erklären.

### 5.2 LV-Gruppen

| LV-Ident | Objekte | Bruttovolumen 701 | NetVolume |
| --- | ---: | ---: | ---: |
| Außenwand | 11 | 122,13 m³ | 92,7828626901 m³ |
| Bodenplatte | 1 | 3,19 m³ | 3,1875 m³ |
| Decke | 7 | 164,72 m³ | 153,5891736895 m³ |
| Einzelfundament | 14 | 0,13 m³ auf 11 Objekten | 0,0430396086 m³ auf 3 Objekten |
| Innenwand | 3 | 57,64 m³ | 56,8652407208 m³ |
| Streifenfundament | 4 | 9,41 m³ | nicht vorhanden |
| Stütze | 30 | 9,85 m³ | 9,5875069289 m³ |
| Unterzug | 11 | 35,06 m³ | 31,2534009982 m³ |

Bei `Einzelfundament` fehlen für drei Objekte sowohl das 701-Bruttovolumen als auch das benutzerdefinierte QTO-Bruttovolumen. Zwei Objekte heißen `Einzelfundament`, eines `Fundament_Treppenantritt`.

## 6. Abnahmetestfälle

| ID | Prüfschritt | Erwartetes Ergebnis | Abnahmekriterium |
| --- | --- | --- | --- |
| M1-FILE-001 | Referenzdatei laden | IFC4, Metadaten und Dateiname werden angezeigt | Laden ohne Abbruch; Hash und Headerdaten nachvollziehbar |
| M1-UNIT-001 | Projekteingaben öffnen | mm, m² und m³ werden korrekt erkannt | keine implizite oder falsche Einheitenumrechnung |
| M1-SPAT-001 | Modellstruktur öffnen | Site 1, Building 1, Storey 1, Space 0 | Namen und Zählwerte entsprechen Abschnitt 4.3 |
| M1-ELEM-001 | Inventur ausführen | 205 Products und 202 Elements | exakte Übereinstimmung |
| M1-CLASS-001 | Klassenverteilung prüfen | acht Klassen gemäß Abschnitt 4.2 | Summe 202; keine doppelte Zählung |
| M1-GEOM-001 | Geometrieabdeckung prüfen | 166 mit, 36 ohne Repräsentation | Assemblies nicht fälschlich als defekte Geometrie zählen |
| M1-GUID-001 | GUID-Prüfung ausführen | 1.465 GlobalIds, 0 Duplikate | keine falschen Dublettenmeldungen |
| M1-CONT-001 | räumliche Zuordnung prüfen | 175 mit genau einer, 27 ohne Zuordnung | unzugeordnete Objekte filter- und öffnbar |
| M1-ASM-001 | Baugruppen prüfen | 36 Assemblies; 5 Elternbeziehungen; 27 Kinder | verschachtelte Assemblies bleiben nachvollziehbar |
| M1-PSET-001 | Set-Inventur öffnen | Zählwerte aus Abschnitt 4.4 | Set- und Feldebene unterscheidbar |
| M1-LV-001 | LV-Ident prüfen | 81 befüllt, 121 leer/fehlend | leere Werte explizit filter- und zählbar |
| M1-FIELD-001 | Pflicht-/Schlüsselfelder prüfen | Abdeckung aus Abschnitt 4.6 | „fehlend“ und „leer“ werden nicht als erfundener Wert ausgegeben |
| M1-MAT-001 | Materialinventur öffnen | Verteilung aus Abschnitt 4.7 | Originalbezeichnungen bleiben erhalten |
| M1-OPEN-001 | Öffnungen prüfen | 3 OpeningElements, 0 Voids-Beziehungen | als Prüfhinweis, nicht als automatische Reparatur |
| M1-QTY-001 | Mengenquellen vergleichen | Werte aus Abschnitt 5.1 | Brutto und Netto getrennt, Quelle am Wert sichtbar |
| M1-FND-001 | Einzelfundamente prüfen | drei Objekte ohne Bruttovolumen | konkrete Objekte in Befundliste und Drilldown erreichbar |
| M1-REVIEW-001 | Klassifizierungsbefunde öffnen | 77 Proxies als Prüfkandidaten | keine automatische Reklassifizierung |
| M1-REVIEW-002 | Sockel-Stützen prüfen | 3 `IfcSlab` mit Name `Sockel_Stütze` und LV-Ident `Einzelfundament` | als fachlicher Prüfhinweis sichtbar |
| M1-ECA-001 | Modellart anzeigen | ECA aus Dateiname ableitbar; inhaltliche Bestätigung fehlt | Herleitung und Konfidenz transparent; keine harte Fachbehauptung |
| M1-UI-001 | Projektübersicht prüfen | Datei, Schema, Einheiten, Zählwerte, Befundstatus | alle Werte ohne Entwicklerwerkzeug erreichbar |
| M1-UI-002 | Objekt-Drilldown prüfen | GUID, native Klasse, Name, räumliche Lage, Psets/QTOs, Material und Befunde | Rücksprung und Objektbezug funktionieren |
| M1-TRACE-001 | Befundquelle prüfen | jeder Befund enthält Regel, Objektbezug und Quelldaten | keine nicht nachvollziehbaren Warnungen |

## 7. Bewertungs- und Statuslogik

| Status | Bedeutung |
| --- | --- |
| Bestanden | Sollwert und Darstellung stimmen; Objekt- und Quellenbezug sind nachvollziehbar |
| Bestanden mit Hinweis | Ergebnis stimmt, aber es besteht eine dokumentierte, nicht blockierende Darstellungsabweichung |
| Nicht bestanden | falscher Zählwert, verlorener Objektbezug, erfundener Wert, stille Umdeutung oder Funktionsabbruch |
| Nicht prüfbar | Testumgebung oder benötigte Ansicht fehlt; gilt nicht als bestanden |

### Blockierende Abweichungen

MVP 1 kann nicht abgenommen werden, wenn mindestens einer der folgenden Punkte auftritt:

- IFC-Datei kann nicht vollständig geladen werden.
- Objektzahlen oder Klassenverteilung weichen ohne dokumentierten Grund ab.
- GUID-, Mengen- oder Propertywerte werden verändert oder synthetisch ergänzt.
- native IFC-Klasse und `BIM_Core.IfcClass` werden vermischt.
- Befunde sind nicht auf die betroffenen Objekte zurückführbar.
- leere oder fehlende Werte werden aus Filtern oder Zählungen ausgeschlossen.
- Brutto- und Netto-Mengen werden ohne sichtbare Quellkennzeichnung zusammengeführt.

## 8. Mindestanforderung an die Oberfläche

### Projektübersicht

Anzeige von Datei, Hash, Schema, Exportmetadaten, Einheiten, Objektzahlen und Anzahl der Befunde nach Schweregrad.

### Modellstruktur

Hierarchische Darstellung von Site, Building, Storey, Assemblies und Elementen. Objekte ohne räumliche Zuordnung müssen separat zugänglich sein.

### Befundliste

Mindestens filterbar nach Regel, Schweregrad, IFC-Klasse, LV-Ident und Status „leer/fehlend“. Auswahl eines Befunds öffnet das betroffene Objekt.

### Objekt-Detailansicht

Anzeige von GlobalId, nativer Klasse, Name, Tag, räumlicher Zuordnung, Repräsentation, Material, Psets, QTOs, Mengenquellen und zugehörigen Befunden.

## 9. Bekannte fachliche Prüfhinweise des Referenzmodells

Diese Punkte sind erwartete Ergebnisse der Inventur, keine vom Agenten automatisch zu korrigierenden Fehler:

1. 77 `IfcBuildingElementProxy` enthalten teilweise fachlich erkennbare Bezeichnungen und sind Reklassifizierungs-Kandidaten.
2. 36 Assemblies besitzen keine eigene geometrische Repräsentation; das ist bei aggregierten Baugruppen plausibel.
3. 27 Elemente besitzen keine räumliche Zuordnung.
4. Drei Öffnungselemente haben keine `IfcRelVoidsElement`-Beziehung.
5. Drei als `Einzelfundament` gekennzeichnete `IfcSlab` heißen `Sockel_Stütze`.
6. Für drei Einzelfundament-Objekte fehlt das Bruttovolumen.
7. `604_Bruttogewicht` und `550_Baunummer` fehlen vollständig.
8. Die Ebenenlogik ist auf einen Default-Storey reduziert; Hierarchy-/AVEVA-Strukturfelder fehlen.
9. Die Modellart ECA ist im Dateinamen erkennbar, aber nicht durch die untersuchten Eigenschaften eindeutig bestätigt.

## 10. Abnahmeprotokoll

| Feld | Eintrag |
| --- | --- |
| geprüfte Softwareversion |  |
| Testdatum |  |
| Prüfer/in |  |
| Hash der IFC-Datei |  |
| bestandene Testfälle |  |
| nicht bestandene Testfälle |  |
| nicht prüfbare Testfälle |  |
| Restpunkte / Tickets |  |
| Entscheidung | ☐ abgenommen ☐ mit Auflagen ☐ nicht abgenommen |

## 11. Folgearbeit nach Freigabe dieser Basis

1. Referenzwerte als automatisierte Regressionstests anbinden.
2. Befundregeln mit stabilen Regel-IDs implementieren.
3. UI-Testfälle für Projektübersicht, Modellstruktur, Befundliste und Objekt-Drilldown ergänzen.
4. Erst danach fachliche Mengenregeln und spätere Exportfunktionen schrittweise hinzufügen.

