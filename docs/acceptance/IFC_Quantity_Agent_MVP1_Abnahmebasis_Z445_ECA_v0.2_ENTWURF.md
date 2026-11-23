# IFC Quantity Agent – MVP-1-Abnahmebasis Z445 ECA v0.2 (ENTWURF)

> **Status: Prüfvorschlag, fachliche Freigabe durch Tom ausstehend.**
> Kein Wert in diesem Dokument ist als Sollwert freigegeben. Alle Zahlen sind lesend mit dem unveränderten Collector (`collect()`) und der unveränderten Regelengine (`run_regression.py`) am neuen Referenzmodell ermittelt. Es wurde weder eine neue Baseline-JSON angelegt noch wurden Regeln, Collector oder die Baseline v0.1 geändert. Die IFC-Datei ist nicht im Repository abgelegt.

## 1. Anlass

Das ursprüngliche Z445-Referenzmodell (SHA-256 `1b8e679b…`, Export 2026-10-05T16:39:23) ist nicht mehr auffindbar. Nutzerentscheidung: Die unten beschriebene IFC-Datei dient als neues Referenzmodell. Sie ist ein anderes, deutlich kleineres und fachlich überarbeitetes Modell; die Baseline v0.1 ist darauf nicht anwendbar (Abschnitt 11).

## 2. Dateiidentität

| Merkmal | Wert |
| --- | --- |
| Dateiname im Modell (FILE_NAME) | `Z445_799_ECA_BM-801-3D.ifc` |
| Dateiname im Referenzlauf | `Z445_799_ECA_BM_801_3D.ifc` (Kopie im Temp-Ordner, Unterstriche wie in Baseline v0.1, damit die Modelltyp-Ableitung ECA identisch greift) |
| Größe | 784.536 Byte |
| SHA-256 | `EA051785859FC96B918E53ADD7495E6C257B7EE6A559BEDCB77732C061C7C1BE` |
| Schema | IFC4 |
| ViewDefinition | ReferenceView_V1.2 |
| FILE_NAME-Zeitstempel | 2026-11-23T20:10:34 |
| Authoring-Anwendung | SketchUp 2026 |
| Exporter | IFC Manager for SketchUp 5.5.4-bdm-corefix02 |
| Modelltyp | ECA (abgeleitet aus Dateiname, Konfidenz medium, keine Property-Bestätigung) |
| Einheiten | Länge Millimeter, Fläche m², Volumen m³ |
| STEP-Entitäten | 5.363 |

## 3. Objektzahlen

| Kennzahl | Wert |
| --- | --- |
| IfcProduct | 89 (86 Bauelemente + IfcSite, IfcBuilding, IfcBuildingStorey) |
| IfcElement | 86 |
| Elemente mit Repräsentation | 86 |
| Elemente ohne Repräsentation | 0 |
| IfcRoot-Objekte mit GlobalId | 918 |
| Doppelte GlobalIds | 0 |
| Elemente mit genau einer räumlichen Zuordnung | 86 |
| Elemente ohne räumliche Zuordnung | 0 |
| IfcElementAssembly | 0 |
| IfcOpeningElement / IfcRelVoidsElement | 0 / 0 |
| IfcBuildingElementProxy | 0 |

Native IFC-Klassen (nicht durch `BIM_Core.IfcClass` überschrieben):

| IFC-Klasse | Anzahl |
| --- | ---: |
| IfcColumn | 38 |
| IfcWall | 16 |
| IfcBeam | 12 |
| IfcSlab | 11 |
| IfcFooting | 9 |
| **Summe** | **86** |

`PredefinedType` ist bei allen 86 Elementen leer.

## 4. Räumliche Struktur

```
IfcProject "default project"
└─ IfcSite "default site"
   └─ IfcBuilding "default building"
      └─ IfcBuildingStorey "default building storey"   (enthält alle 86 Elemente)
```

Keine IfcSpace (0). Keine Zyklen, keine nicht zugeordneten Elemente, 89 Relationen (3 × IfcRelAggregates, 86 Elemente über IfcRelContainedInSpatialStructure).

## 5. Materialien

Alle 86 Elemente haben genau ein Material: `Stahlbeton` (86). Keine weiteren Materialzuordnungen.

## 6. PSets und QTO-Quellen

| PSet / QTO | Elemente |
| --- | ---: |
| BASF_General | 86 |
| QTO (benutzerdefiniert) | 86 |
| PropertySets | 86 |
| Classifications | 86 |
| BASF_General_GUID | 76 |
| BASF_GCC (GCC-Code A222) | 43 |
| Qto_ColumnBaseQuantities | 38 |
| Qto_WallBaseQuantities | 16 |
| Qto_BeamBaseQuantities | 12 |
| Qto_SlabBaseQuantities | 11 |
| Pset_QuantityTakeOff | 31 |
| QuantityTakeOff | 3 |
| BIM_Core | 0 |

Native `Qto_*BaseQuantities` fehlen bei allen 9 IfcFooting.

## 7. BIM_Core-Angaben

Das PSet `BIM_Core` ist im Modell nicht vorhanden (`BIM_Core.IfcClass` 0 von 86; auch IfcName/IfcDescription/IfcObjectType leer an allen 90 Knoten). Es entsteht daher kein Abgleich zwischen nativer Klasse und `BIM_Core.IfcClass`; es wird nichts ergänzt.

## 8. LV-Ident-Gruppen (`BASF_General.540_LV_Ident`)

84 von 86 befüllt, 2 leer. Das Vokabular unterscheidet sich vollständig von Baseline v0.1 (Präfix `Stb_`, neue Gruppen Sockel und Fertigteil).

| LV-Ident | Objekte | IFC-Klassen |
| --- | ---: | --- |
| Stb_Fertigteil_Stuetze | 20 | IfcColumn |
| Stb_Stuetze | 18 | IfcColumn |
| Stb_Fertigteil_Wand | 13 | IfcWall |
| Stb_Unterzug | 10 | IfcBeam |
| Stb_Decke | 6 | IfcSlab |
| Stb_Einzelfundament | 5 | IfcFooting |
| Stb_Streifenfundament | 4 | IfcFooting |
| Stb_Sockel | 4 | IfcSlab |
| Stb_Wand | 3 | IfcWall |
| Stb_Bodenplatte | 1 | IfcSlab |
| *(leer)* | 2 | IfcBeam |

Die zwei leeren Objekte sind IfcBeam „Konsole“ (GlobalId `0pNU2ahuTEBw2NB97WRsBz`, Tag TR-101; `3t7s7o4zP6TfTdn$fqFcjr`, Tag TR-126), ObjectType `UNTERZUG`, Description `Unterzug_Kragarm`. Es erfolgt keine automatische Zuordnung; ein Textattribut-Fallback wäre nur als gekennzeichneter Vorschlag zulässig. Offen: fachliche Zuordnung durch Tom.

## 9. Mengenquellen

Getrennt gehalten: Brutto `BASF_General.701_Bruttovolumen`, benutzerdefiniert `QTO.QTO.01_Bruttovolumen_m3`, Netto `Qto_*BaseQuantities.NetVolume` (nur native Quelle).

| Quelle | Objekte |
| --- | ---: |
| BASF_General.701_Bruttovolumen | 86 |
| QTO.QTO.01_Bruttovolumen_m3 | 86 |
| Qto_ColumnBaseQuantities.NetVolume | 38 |
| Qto_WallBaseQuantities.NetVolume | 16 |
| Qto_BeamBaseQuantities.NetVolume | 12 |
| Qto_SlabBaseQuantities.NetVolume | 11 |
| NetVolume nicht vorhanden | 9 (alle IfcFooting) |

701 stimmt bei allen Objekten mit dem benutzerdefinierten QTO überein (keine Abweichung).

Summen (m³, Collector-Ist, Prüfvorschlag):

| Kennzahl | Wert |
| --- | ---: |
| Objekte mit Brutto 701 und NetVolume | 77 |
| Brutto 701 (alle 86 Objekte, Summe der Klassenwerte) | 538,66 |
| Brutto 701 der 77 Objekte | 529,40 |
| NetVolume der 77 Objekte | 529,3064097829563 |
| Differenz Brutto − Netto | 0,09359021704370529 |

Hinweis: Die Collector-Summe 529,40 bezieht sich auf die 77 Objekte mit beiden Werten; die 9 IfcFooting (Brutto 9,26 m³) haben kein NetVolume.

Je IFC-Klasse:

| Klasse | Objekte | Brutto 701 (m³) | Objekte mit NetVolume | NetVolume (m³) |
| --- | ---: | ---: | ---: | ---: |
| IfcBeam | 12 | 29,29 | 12 | 29,2622 |
| IfcColumn | 38 | 28,10 | 38 | 28,0125 |
| IfcFooting | 9 | 9,26 | 0 | – |
| IfcSlab | 11 | 319,17 | 11 | 319,1727 |
| IfcWall | 16 | 152,84 | 16 | 152,859 |

Je LV-Gruppe (Collector-Ist):

| LV-Ident | Objekte | Brutto 701 (m³) | Objekte NetVolume | NetVolume (m³) |
| --- | ---: | ---: | ---: | ---: |
| Stb_Unterzug | 10 | 28,17 | 10 | 28,146150998241428 |
| Stb_Fertigteil_Stuetze | 20 | 5,78 | 20 | 5,73749999999989 |
| Stb_Stuetze | 18 | 22,32 | 18 | 22,275000000006262 |
| Stb_Streifenfundament | 4 | 8,79 | 0 | – |
| Stb_Einzelfundament | 5 | 0,47 | 0 | – |
| Stb_Bodenplatte | 1 | 212,96 | 1 | 212,9582500000008 |
| Stb_Sockel | 4 | 0,06 | 4 | 0,06280624674098553 |
| Stb_Decke | 6 | 106,15 | 6 | 106,15165622559488 |
| Stb_Wand | 3 | 57,45 | 3 | 57,44547570281943 |
| Stb_Fertigteil_Wand | 13 | 95,39 | 13 | 95,41357060955272 |

Doppelzählung Baugruppen/Einzelteile: nicht prüfbar, keine IfcElementAssembly im Modell. Bei IfcWall kann NetVolume leicht über Brutto liegen (z. B. Stb_Fertigteil_Wand); das ist als Quellenabweichung zu betrachten, nicht zu korrigieren.

## 10. Auffälligkeiten

| Nr. | Befund | Umfang |
| --- | --- | --- |
| A1 | Fehlende GlobalIds an IfcRoot-Elementen | 0 |
| A2 | Doppelte GlobalIds | 0 |
| A3 | Elemente ohne räumliche Zuordnung | 0 |
| A4 | `540_LV_Ident` leer | 2 (IfcBeam „Konsole“) |
| A5 | Kein natives NetVolume (keine Qto_*BaseQuantities) | 9 IfcFooting; 4 davon mit Pset_QuantityTakeOff, aber ohne nativen Qto |
| A6 | `504_Planungsstand` leer | 16 (12 IfcWall, 3 IfcBeam, 1 IfcSlab) |
| A7 | `550_Baunummer` leer | 86 von 86 |
| A8 | `604_Bruttogewicht` leer | 86 von 86 |
| A9 | `BIM_Core` nicht vorhanden | 86 von 86 |
| A10 | BASF_GCC fehlt | 43 von 86 |
| A11 | BASF_General_GUID fehlt | 10 von 86 |
| A12 | Auffälliger ObjectType `Êinzelfundament` (Sonderzeichen Ê) | 1 |
| A13 | Uneinheitliche ObjectType-Schreibweise (z. B. `AUSSENWAND`/`Stahlbetonwand`) | mehrere |
| A14 | Natives Name/Description/ObjectType/Tag: leer | 0 (alle befüllt, Tags eindeutig) |
| A15 | IfcSlab-Elemente mit LV `Stb_Sockel` (Name „Sockel_Stütze“) | 4; Zuordnung fachlich zu bestätigen |
| A16 | Einzelfundament-Elemente „Einzelfundament_Treppe“ | 2; Brutto sehr klein, fachlich prüfen |

## 11. Vergleich mit Baseline v0.1

Alle Werte stammen aus `baseline/IFC_Quantity_Agent_MVP1_Referenzwerte_Z445_ECA_v0.1.json` (Soll v0.1) und dem Lauf am neuen Modell (Ist). Nichts davon ist freigegebener Sollwert für das neue Modell.

| Merkmal | Baseline v0.1 | Neues Modell |
| --- | --- | --- |
| SHA-256 | `1b8e679b…2523` | `ea051785…c1be` |
| Größe (Byte) | 1.133.708 | 784.536 |
| Schema / ViewDefinition | IFC4 / ReferenceView_V1.2 | gleich |
| Autoring / Exporter | SketchUp 2025 / 5.5.4 | SketchUp 2026 / 5.5.4-bdm-corefix02 |
| Exportzeitstempel | 2026-10-05T16:39:23 | 2026-11-23T20:10:34 |
| Einheiten, ECA-Typ, Spatial-Struktur | mm/m²/m³, ECA, je 1 Site/Building/Storey | gleich |
| STEP-Entitäten | 6.966 | 5.363 |
| IfcProduct | 205 | 89 |
| IfcElement | 202 | 86 |
| Mit / ohne Repräsentation | 166 / 36 | 86 / 0 |
| IfcRoot mit GlobalId | 1.465 | 918 |
| Doppelte GlobalIds | 0 | 0 |
| Elemente mit / ohne Raumzuordnung | 175 / 27 | 86 / 0 |
| IfcBuildingElementProxy | 77 | 0 |
| IfcElementAssembly | 36 | 0 |
| IfcColumn | 30 | 38 |
| IfcFooting | 20 | 9 |
| IfcWall | 14 | 16 |
| IfcBeam | 11 | 12 |
| IfcSlab | 11 | 11 |
| IfcOpeningElement | 3 | 0 |
| Materialien | 10 Materialien (Stahlbeton 113, …) | nur Stahlbeton (86) |
| PSet BIM_Core | 59 | 0 |
| PSet Classifications | – | 86 |
| BASF_General / QTO / PropertySets | 87 / 84 / 66 | 86 / 86 / 86 |
| BASF_General_GUID / BASF_GCC | 59 / 45 | 76 / 43 |
| Qto Column / Wall / Beam / Slab | 30 / 14 / 11 / 11 | 38 / 16 / 12 / 11 |
| Pset_QuantityTakeOff / QuantityTakeOff | 29 / 3 | 31 / 3 |
| LV-Ident befüllt / leer | 81 / 121 | 84 / 2 |
| LV-Vokabular | Stütze, Einzelfundament, Unterzug, Außenwand, Decke, Streifenfundament, Innenwand, Bodenplatte | Stb_* (10 Gruppen, Abschnitt 8) |
| 701 Bruttovolumen vorhanden | 81 | 86 |
| 504 Planungsstand | 86 In_Planung / 116 leer | 70 In_Planung / 16 leer |
| 604 / 550 leer | 202 / 202 | 86 / 86 |
| BIM_Core.IfcClass | 59 | 0 |
| native Description / ObjectType leer | 202 / 202 | 0 / 0 |
| native Tag leer | 77 | 0 |
| Baugruppen | 36 (27 Kinder referenziert) | 0 |
| Objekte mit Brutto 701 und NetVolume | 66 | 77 |
| Brutto 701 Summe (m³) | 392,64 | 529,40 |
| NetVolume Summe (m³) | 347,3087 | 529,3064 |
| Brutto − Netto (m³) | 45,3313 | 0,0936 |
| 701 = benutzerdefiniertes QTO | ja | ja |
| Reviewbefunde | proxies 77, uncontained 27, Öffnungen ohne Void 3, Sockel mit LV Einzelfundament 3, Einzelfundament ohne Brutto 3, Baunummer 202, Bruttogewicht 202 | nur Baunummer 86, Bruttogewicht 86 |

Die LV-Gruppenmengen sind wegen des neuen LV-Vokabulars nicht 1:1 vergleichbar (v0.1: Außenwand 11/122,13, Bodenplatte 1/3,19, Decke 7/164,72, Einzelfundament 14/0,13, Innenwand 3/57,64, Streifenfundament 4/9,41, Stütze 30/9,85, Unterzug 11/35,06 – Objekte/Brutto m³).

## 12. Referenzlauf (`run_regression.py`)

Aufruf in einem temporären Ordner außerhalb des Repos (Python 3.14.6, IfcOpenShell 0.8.4.post1), Regelpaket `IQA-M1-Z445-ECA` 0.1.0, Baseline v0.1 unverändert:

```
python run_regression.py --ifc <temp>\Z445_799_ECA_BM_801_3D.ifc --output-dir <temp>\out
MVP-1 Regression: 7/32 bestanden, 25 fehlgeschlagen, 0 Fehler
```

Berichte (JSON/JUnit) liegen nur im Temp-Ordner und nicht im Repo.

Bestanden (7): FILE-003, FILE-004, FILE-006, UNIT-001, SPAT-001, GUID-002, QTY-005.

### Fehlschlagende Regeln und Ursache

| Regel | Schwere | Soll v0.1 → Ist | Ursache |
| --- | --- | --- | --- |
| IQA-M1-FILE-001 | blocker | SHA `1b8e679b…` → `ea051785…` | anderes Modell |
| IQA-M1-FILE-002 | error | 1.133.708 → 784.536 Byte | anderes Modell |
| IQA-M1-FILE-005 | warning | 2026-10-05T16:39:23 → 2026-11-23T20:10:34 | neuer Export |
| IQA-M1-ELEM-001 | blocker | 205 → 89 | weniger Produkte |
| IQA-M1-ELEM-002 | blocker | 202 → 86 | weniger Elemente |
| IQA-M1-ELEM-003 | error | 6.966 → 5.363 | kleineres Modell |
| IQA-M1-ELEM-004 | error | 166 → 86 | weniger Elemente mit Geometrie |
| IQA-M1-ELEM-005 | error | 36 → 0 | keine Baugruppen ohne Geometrie mehr |
| IQA-M1-ELEM-006 | blocker | Proxy 77, Assembly 36, Column 30, Footing 20, Wall 14, Beam 11, Slab 11, Opening 3 → Column 38, Wall 16, Beam 12, Slab 11, Footing 9 | Proxies, Assemblies, Openings entfallen; übrige Zahlen geändert |
| IQA-M1-GUID-001 | error | 1.465 → 918 | kleineres Modell |
| IQA-M1-SPAT-002 | error | 175 → 86 | alle Elemente zugeordnet, weniger Elemente |
| IQA-M1-SPAT-003 | error | 27 → 0 | alle Elemente räumlich zugeordnet |
| IQA-M1-PSET-001 | error | siehe Abschnitt 6/11 | BIM_Core entfällt, Classifications neu, Zahlen geändert |
| IQA-M1-FIELD-001 | blocker | 81 befüllt, 8 Werte → 84 befüllt, 10 `Stb_*`-Werte | neues LV-Vokabular, fast vollständig befüllt |
| IQA-M1-FIELD-002 | error | siehe Abschnitt 11 | Feldabdeckung geändert (Description/ObjectType/Tag befüllt, 701 vollständig, BIM_Core 0) |
| IQA-M1-FIELD-003 | blocker | BIM_Core.IfcClass 6 Klassen → leer | `BIM_Core` fehlt im Modell |
| IQA-M1-MAT-001 | error | 10 Materialien → nur Stahlbeton 86 | Materialien reduziert |
| IQA-M1-ASM-001 | blocker | 36 Baugruppen → 0 | keine IfcElementAssembly (Regel dadurch an diesem Modell nicht prüfbar) |
| IQA-M1-OPEN-001 | error | 3 Öffnungen → 0 | keine IfcOpeningElement |
| IQA-M1-QTY-001 | blocker | 66 → 77 | geänderte Mengenlage |
| IQA-M1-QTY-002 | blocker | 392,64 → 529,40 m³ | anderes Modell |
| IQA-M1-QTY-003 | blocker | 347,3087 → 529,3064 m³ | anderes Modell |
| IQA-M1-QTY-004 | error | 45,3313 → 0,0936 m³ | anderes Modell |
| IQA-M1-QTY-006 | blocker | 8 LV-Gruppen → 10 `Stb_*`-Gruppen | neues LV-Vokabular, andere Mengen |
| IQA-M1-REVIEW-001 | error | 7 erwartete Befunde → nur Baunummer 86, Bruttogewicht 86 | Proxies, Opening, uncontained, Sockel-/Fundament-Befunde entfallen; Baunummer/Bruttogewicht 202 → 86 |

Fazit: Alle Fehlschläge sind erwartbare Soll-/Ist-Abweichungen zwischen dem alten und dem neuen Modell; es gibt keine Laufzeitfehler (0 Error). Die Baseline v0.1 ist am neuen Modell nicht anwendbar.

## 13. Offene Fachfragen / Freigabe

1. Freigabe des neuen Modells als Referenz und der daraus abzuleitenden Sollwerte durch Tom (ausstehend).
2. Einordnung der zwei leeren LV-Idents (IfcBeam „Konsole“).
3. Umgang mit fehlendem nativem NetVolume der 9 IfcFooting.
4. Fehlendes `BIM_Core` und leere Baunummer/Bruttogewicht: erwartet oder zu liefern?
5. ASM-001 und OPEN-001 bleiben mit diesem Modell ungeprüft; Referenzmodell mit Baugruppen/Öffnungen nötig.
6. Neues LV-Vokabular `Stb_*` und seine Gruppenmengen fachlich bestätigen.
7. Auswirkung auf Regelversion/Baseline nach Freigabe als eigener Schritt (neue Baseline-JSON, Regelversion, Tests).
