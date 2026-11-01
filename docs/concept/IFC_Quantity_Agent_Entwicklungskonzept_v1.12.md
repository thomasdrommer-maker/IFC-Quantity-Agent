# IFC Quantity Agent – Entwicklungskonzept v1.12

**Zweck:** IFC-Modelle fachlich einlesen, klassifizieren, prüfen und daraus nachvollziehbare Mengen- und Massenübersichten erstellen. Der Agent soll Mengen nicht nur ausgeben, sondern Quelle, Berechnung, Qualität und offene Prüfungen transparent machen.

**Status:** Verbindlicher Entwicklungsauftrag / fachliches Zielbild. Version 1.12 übernimmt v1.11 und integriert die Stahlbau- und Betonbau-Übergabepakete v0.2 sowie benutzerdefinierte Kategorieprofile. Stand: 01.11.2026. Kategorien und Profilverwaltung sind spezifiziert, aber noch nicht in der MVP-1-Anwendung implementiert. UI-Ansichten werden vor dem Mengenbericht-Excel-Export umgesetzt.  
**Unterlagen:** [Übergabepakete und Pflegeablauf](../handover/README.md). v1.11 bleibt als historischer Stand erhalten.  
**Projektanschluss:** BCIP-Quantity-Modul, bestehende IFC-LV-Regeln, BASF_General und Modellcodes ESM/ESS/ESO/ESC/ESK.  
**UI-Leitbild:** modellzentrierte HTML-Oberfläche mit Projektbaum, Analyseansichten und objektbezogenem Detailbereich; Fachlogik bleibt unabhängig von der Oberfläche.

## 1. Ziel und Arbeitsprinzipien

Der Agent unterstützt die modellbasierte Mengenermittlung für Gründung, Beton- und Stahlbau. Er liest IFC-Klassen, Beziehungen, PSets, QTOs, Materialien, Geschosse und Geometrie aus. Daraus erzeugt er prüfbare Mengenlisten, Summen und Qualitätsberichte.

Verbindliche Grundsätze:

1. **Jeder Wert bleibt rückverfolgbar:** IFC-Datei/Revision, GlobalId, Modell, IFC-Klasse, PSet/QTO, Property, Regel-ID und Regelversion werden mitgeführt.
2. **Mengen werden objektbezogen ermittelt:** keine pauschale globale Methode, wenn Bauteile unterschiedliche Quellen oder Geometrien haben.
3. **Doppelzählungen werden vermieden:** Assemblies und ihre Bestandteile dürfen nicht gleichzeitig als Menge summiert werden, außer eine definierte Auswertung verlangt ausdrücklich beides.
4. **Keine stille Umklassifizierung:** Mehrdeutige Fälle werden als Reviewfälle ausgegeben. Die Regel darf eine Klassifikation vorschlagen, aber eine nicht belegte Änderung nicht still durchführen.
5. **Einheiten werden normalisiert und angezeigt:** intern mit SI-Einheiten rechnen; in Berichten die fachlich gewünschte Einheit (z. B. kg/to, m², m³, lfm, Stk) ausgeben.
6. **Schätzungen sind keine Modellmengen:** geometrische Näherungen und Kennwerte erhalten eine Qualitätsklasse und eine sichtbare Kennzeichnung.
7. **Exportierte Summen sind reproduzierbar:** gleiche IFC-Datei plus gleiche Regelversion ergibt gleiche Ergebnisse.

## 2. Geplanter Ablauf

1. **Modell einlesen:** IFC-Schema, Projekt-/Gebäudestruktur, Einheiten, Modelle, Geschosse, GUIDs und Datei-Metadaten erfassen.
2. **Inventar bilden:** physische IFC-Elemente, Assemblies/Container, Verteilung nach IFC-Klasse und Geschoss zählen; fehlende oder doppelte GUIDs melden.
3. **Datenbestand analysieren:** PSets, QTOs, Materialzuweisungen, Klassifizierungen und relevante Namens-/Beschreibungstexte erkennen.
4. **Modelltyp bestimmen:** Modellcode und weitere Indizien auswerten; Erkennung mit Konfidenz und Begründung ausgeben.
5. **Mengenquellen auswählen:** je Mengengröße und Objekt passende Quelle gemäß Regelpaket verwenden.
6. **Validieren:** Einheiten, fehlende Werte, Geometrie, Ausreißer, Widersprüche, Doppelzählungen und Zuordnungsunsicherheit prüfen.
7. **Ergebnisse darstellen:** Managementübersicht, Mengenmatrix, Detailtabelle, Prüfbericht und geeignete Ansichten bereitstellen.
8. **Exportieren:** Excel als erster Ziel-Export; zusätzlich maschinenlesbarer JSON/CSV-Datensatz für die spätere BCIP-Anbindung.

## 3. Modell- und Objektinventar

### 3.1 Basiskennzahlen

- IFC-Elemente insgesamt, eindeutig nach GlobalId
- Elemente je IFC-Klasse, Modellcode und Geschoss
- Assemblies/Container separat
- physische Blattelemente separat
- Objekte ohne verwertbare IFC-Klassifizierung
- Objekte ohne GlobalId, mit leerer oder mehrfach vorkommender GlobalId
- Objekte ohne Material, ohne relevantes PSet oder ohne auswertbare Menge
- Verteilung nach IfcMaterial/Materialschicht, sofern vorhanden

**Zählregel:** `IfcElementAssembly` ist standardmäßig ein Container und wird nicht zusätzlich zu seinen physischen Bestandteilen als Bauteilmenge gezählt. Eine separate Montage-/Positionssicht darf Assemblies ausweisen, muss sie aber klar von der Stückzahl der Blattobjekte trennen. Deduplizierung erfolgt vorrangig über GlobalId.

### 3.2 IFC-Klassifizierung

Der Agent unterscheidet mindestens:

- gültige IFC-Klasse vorhanden und fachlich plausibel
- IFC-Klasse fehlt/ist nicht lesbar
- IFC-Klasse vorhanden, aber fachlich verdächtig
- erwartete Klasse weicht von der tatsächlichen Klasse ab
- Container-/Assembly-Objekt

Die fachliche Plausibilisierung nutzt IFC-Klasse, PredefinedType, ObjectType, Typzuordnung und IFC-Beziehungen, Modellcode, PSets, Material, Namen/Beschreibungen, räumliche Lage und – sofern verfügbar – Geometrie. Die tatsächliche Klasse wird in der Rohdatenansicht nie überschrieben. KI-gestützte Klassifizierungshinweise sind in Abschnitt 8.1 geregelt.

### 3.3 Model Quality Checker – Klassifizierungs- und Plausibilitätsprüfung

Der Model Quality Checker ergänzt die Mengenauswertung um eine eigene Prüfebene für IFC-Kernattribute. Er untersucht, ob IFC-Klasse und zugehörige Attribute fachlich zum modellierten Bauteil passen. Beispiele sind eine Stütze als `IfcColumn` statt `IfcBeam`, ein Aussteifungsverband als `IfcMember` oder eine Stützenverankerung als `IfcMechanicalFastener` statt `IfcElementProxy`. Diese Beispiele sind nicht abschließend; die Prüftaxonomie muss erweiterbar sein.

Die Prüfung berücksichtigt – abhängig von Verfügbarkeit und Regel – IFC-Klasse, `PredefinedType`, `IfcObjectType`, Typobjekt und Beziehungen, Geometrie, Lage/Orientierung, räumliche Nachbarschaft, Material, `IfcName`, `IfcDescription`, PSets, QTOs und Klassifikationen. Fehlende Daten werden als Evidenzlücke ausgewiesen.

Die KI darf auffällige Fälle erkennen, Evidenz zusammenfassen und alternative Klassifizierungen vorschlagen. Jeder Vorschlag enthält tatsächliche Werte, vorgeschlagene Klasse/Attribute, Begründung, berücksichtigte Evidenz, Konfidenz und Reviewstatus. KI-Ausgaben sind Hinweise und keine Konformitätsentscheidung. Sie ändern weder IFC-Daten noch verbindliche Mengenregeln oder Summen. Bis zur fachlichen Bestätigung rechnet die Quantity Engine mit den tatsächlich gelieferten IFC-Angaben und kennzeichnet eine mögliche Mengenauswirkung. Bestätigte Fälle können als versionierte Regeln und Referenztests aufgenommen werden.

## 4. Erkennung der Modelltypen

Bekannte Teilfachmodell-Codes und Kategorien gemäß der vorliegenden Projektübersicht:

| Code | Kategorie | Hauptauswertung |
|---|---|---|
| EFD | Deep Foundation (Tiefgründung) | Gründung – Tiefgründung |
| EFF | Flat Foundation (Flachgründung) | Gründung – Flachgründung |
| EFB | Baseplate (Bodenplatte) | Gründung – Bodenplatte |
| EFI | Embed Parts (Einbauteile) | Gründung – Einbauteile |
| EFP | Subseg. Pedestal (nachträglicher Sockel) | Gründung – nachträglicher Sockel |
| ECS | Load Bearing Structures (tragende Konstruktion) | Stahlbetonbau – aufgehende Bauteile |
| ECI | Embed Parts (Einbauteile) | Stahlbetonbau – Einbauteile |
| ECP | Subseq. Pedestal (nachträglicher Sockel) | Stahlbetonbau – nachträglicher Sockel |
| ECL | Floor Structures (Bodenaufbauten) | Stahlbetonbau – Bodenaufbauten |
| ESM | Main Steel Structure (Hauptstahlbau) | Stahlbau |
| ESS | Secondary Steel Structure (Sekundärstahlbau, keine Sonderkonstruktionen) | Stahlbau |
| ESO | Others (Geländer, Treppen, Steigleiter) | Stahlbau – sonstige Bauteile |
| ESC | Covers (Bühnenbeläge) | Stahlbau – Bühnenbeläge |
| ESK | Special Support (Sonderkonstruktionen) | Stahlbau – Sonderkonstruktionen |
| ESP | Piperacks | Stahlbau – Piperacks |
| ECA | Stahlbeton / Massivbau | kombiniertes Teilfachmodell; Projektcode, nicht in der vorliegenden Codeübersicht aufgeführt |
| ESA | Stahlbau | kombiniertes Stahlbau-Teilfachmodell; Projektcode, nicht in der vorliegenden Codeübersicht aufgeführt |

Modelltypbestimmung erfolgt regelbasiert aus mehreren Signalen: Dateiname/Modellkennung, BASF-Properties, IfcProject/IfcBuilding-Information, Objektverteilung und charakteristische Objekt-/Materialmerkmale. Der Modellcode allein darf die Auswertung nicht erzwingen, wenn Inhalt und Code deutlich widersprechen.

Ausgabe pro Datei: erkannter Modelltyp, verwendete Indizien, Konfidenz (hoch/mittel/niedrig), widersprechende Hinweise und manuell zu prüfende Zuordnungen.

### 4.1 Führende Zuordnungsquelle und Fallbacks

Die fachliche Zuordnung von Objekten zu Modell-/Mengen-/LV-Gruppen wird vorrangig aus der UDA `BASF_General.540_LV_Ident` abgeleitet. `IfcName`, `IfcObjectType` und `IfcDescription` sind Fallback-Indizien, wenn `540_LV_Ident` fehlt oder leer ist.

- Ein vorhandener, regelkonformer `540_LV_Ident` ist führend. Abweichende Hinweise in IFC-Textattributen überschreiben ihn nicht; der Widerspruch wird als Finding mit betroffenen Attributwerten angezeigt.
- Fehlt `540_LV_Ident`, dürfen die drei IFC-Attribute über versionierte Zuordnungsregeln eine vorläufige Gruppe bestimmen. Die Zuordnung wird als Fallback gekennzeichnet und erhält Begründung sowie Konfidenz.
- Widersprüchliche oder mehrdeutige Fallback-Treffer werden nicht automatisch entschieden, sondern zur fachlichen Prüfung gestellt.
- Rohwerte, verwendetes Attribut, angewendete Regel-ID/-Version und Zuordnungsergebnis bleiben im Detailbereich sichtbar. Es erfolgt keine Rückschreibung in das IFC-Modell.

**Schemaabgleich vor Implementierung:** Dieses Konzept verwendet `540_LV_Ident` wie aktuell vorgegeben. Falls bestehende Regeldateien noch `504_LV_Ident` enthalten, müssen die Property-Pfade zwischen BASF_General-Sollschema und den Quantity-Agent-Regeln abgeglichen und versioniert werden.

### 4.2 Offene und erweiterbare Objektgruppen-Taxonomie

Die Zuordnungslogik gilt für alle fachlichen Objektgruppen des Modells und ist ausdrücklich nicht auf die aktuell bekannten Beispiele beschränkt. Geländer, Steigleitern, Sicherungstüren und Bühnenbeläge sind erste Beispiele; weitere Kategorien können projekt- und modellabhängig hinzukommen.

Die Taxonomie wird als versioniertes Regelpaket gepflegt, nicht als feste Liste oder `if/else`-Kette im Programmcode. Für jede neue Objektgruppe lassen sich mindestens hinterlegen:

- eindeutige Gruppen-ID und Bezeichnung sowie übergeordnete Gruppe,
- gültige Werte in `BASF_General.540_LV_Ident`,
- Fallback-Muster und Synonyme für `IfcName`, `IfcObjectType` und `IfcDescription`,
- relevante Modellcodes und IFC-Klassen,
- zugehöriges Mengenprofil und Gruppierungs-/Roll-up-Regeln,
- Ausschlüsse, Mehrdeutigkeitsregeln, Konfidenzgrenzen und Regressionstestfälle.

Die UI erzeugt ihre Filter und Gruppenansichten aus diesem Regelpaket. Neue Gruppen sollen ohne Änderung am UI-Code ergänzt werden können. Für noch nicht bekannte Objekte zeigt der Agent die Rohattribute und schlägt keine unbelegte Kategorie vor; der Nutzer kann den Fall prüfen und eine bestätigte Regel für spätere Modelle freigeben.

Ein Objekt kann eine führende fachliche Gruppe und ergänzende Merkmale (z. B. Material oder Baugruppe) erhalten. Mengenaggregation und übergeordnete Summen müssen je Regel ausdrücklich festlegen, welche Gruppen additiv sind, damit ein Objekt nicht zugleich in einer Untergruppe und einer überlappenden Hauptgruppe doppelt summiert wird.

## 5. PSet-, QTO- und Materialanalyse

Der Agent soll PSets nicht nur listen, sondern semantisch auswerten:

- Property-Namen und Werte je Objekt sowie Häufigkeit/Abdeckung im Modell
- bekannte BASF_General- und BASF_GCC-Felder erkennen
- QTO-PropertySets und Basismengen erkennen
- Zahlenwerte samt IFC-Einheit, Umrechnung und Plausibilitätsstatus ausgeben
- fehlende, leere, widersprüchliche oder mehrfach belegte Properties markieren
- unbekannte PSets unverändert als Rohdaten zugänglich halten
- Materialzuweisungen auf Objekt-, Schicht- oder Komponentenebene auswerten; Materialnamen normalisieren, Originalwert erhalten

Für Mengen ist immer zwischen **Wert**, **Einheit**, **Quelle**, **Methode** und **Qualität** zu unterscheiden.

### 5.1 Mengenquellen und Priorität

Die Quelle wird je Mengengröße durch das Regelpaket festgelegt. Vorgeschlagene Standardlogik:

- **Stahlgewicht:** `BASF_General.604_Bruttogewicht` ist im BASF-Stahlworkflow primär; danach Tekla Quantity/Weight bzw. explizit konfigurierte Tekla-Gewichtsproperty; danach `BaseQuantities.NetWeight`. Propertypfad und Regelversion im Ergebnis festhalten.
- **Übrige Mengen:** gültige, semantisch passende IFC-QTO-/BaseQuantity vor PSet-Werten; danach projektspezifische PSet-/Tekla-Werte; zuletzt geometrische Berechnung, sofern die Geometrie dafür geeignet ist.
- Ein nicht plausibler oder widersprüchlicher Wert wird nicht automatisch durch eine nachrangige Quelle ersetzt. Der Agent zeigt den Konflikt und kann eine Ersatzquelle als Vorschlag mit Qualitätsabstufung ausweisen.
- Geometrische Fallbacks erhalten eindeutige Kennzeichnung, z. B. `FallbackVolume` oder `FallbackLength`.

## 6. Auswertungsmatrix nach Bauteilgruppe

Die folgende Matrix ist der fachliche Umfang des MVP. Mengenregeln sollen konfigurierbar sein und nicht fest im Programmcode stecken.

| Bauteilgruppe | Modelltyp | Zielmengen | Wesentliche Zuordnung / Prüfpunkte |
|---|---|---|---|
| Stahlbau allgemein | ESM, ESS | kg, to | Gewicht nach BASF_General/604_Bruttogewicht, dann freigegebene Tekla-/BaseQuantities-Fallbacks; Material; IfcBeam/Column/Member/Plate und definierte weitere Klassen |
| Geländer | ESO | kg, to, lfm | IfcRailing sowie projektdefinierte Komponenten/Assemblies; laufende Länge gemäß freigegebener Regel, z. B. Achs-/Abschnittslänge; Anschlussbleche separat behandelbar |
| Steigleiter | ESO | kg, to, lfm, Stk | IfcBeam/Column/Member/Plate und IfcName/ObjectType wie „Steigleiter“/„Leitersprosse“ gemäß Regeln; Assembly nicht als zusätzliches Element zählen |
| Treppen | ESO | Stk, kg/to, ergänzend lfm | eigene Regelgruppe für Treppe, Lauf, Stufen und Geländer; Stufen nicht mit Treppenassembly doppelt zählen |
| Bühnenbelag | ESC | m² Oberfläche | IfcPlate/IfcCovering und Merkmale wie Gitterrost/Tränenblech; Netto-/Bruttofläche klar trennen |
| Gitterroststufen | ESO/ESC gemäß Projektregel | Stk | Breite, Länge und Dicke primär aus der Geometrie ableiten; PSets/QTOs als unterstützende oder geprüfte alternative Quellen verwenden; IfcName/IfcDescription/IfcObjectType nur als Hinweise bzw. Fallback, wenn eindeutig interpretierbar. Exakte Gruppierung nach Breite × Länge × Dicke; keine Toleranzklassen |
| Sonderkonstruktionen | ESK | Stk, kg, to | Objekt-/Positionsregeln, Montageeinheiten und Komponenten getrennt darstellen; keine pauschale Klasse ohne Regelbeleg |
| Tiefgründung (Pfähle) | EFD | Stk, lfm, m³ | Gesamtmengen plus getrennte Kategorien nach Durchmesser; Pfahltyp, Durchmesser, Länge und Volumen je Objekt nachvollziehbar |
| Fundamente | EFF | m³ | Gesamtvolumen plus getrennte Typen Streifenfundament und Einzelfundament; Typ und Betonmaterial je Objekt prüfen |
| Bodenplatte | EFB | m³, m² Oberfläche | Volumen und relevante Oberflächen getrennt; Öffnungen/Aussparungen und Pumpensümpfe gemäß Regelwerk behandeln |
| Aufkantungen | ECS | m³, lfm | Volumen und Länge getrennt; lfm entlang der Bauteil-Längsachse; eindeutige Objekt-/Geometrieklassifikation und Abgrenzung zur Bodenplatte dokumentieren |
| Wände | ECS | m³, optional m² | Volumen; bei Bedarf Oberfläche getrennt nach Seite; Öffnungen berücksichtigen, wenn QTO/Geometrie dies trägt |
| Stützen | ECS | m³ | Volumen je Stütze; Bauteilklasse und Material prüfen |
| Unterzüge | ECS | m³ | Volumen je Unterzug; Trennung von Decken und Trägern nachvollziehbar halten |
| Decken | ECS | m³, m² Oberfläche | Volumen plus definierte Oberfläche; Ober-/Unterseite und Brutto-/Nettofläche getrennt ausweisen |

**Erweiterung:** ESP/Piperacks, Bewehrungsmengen und LV-Positionszuordnung können nach dem MVP als eigene Regelpakete ergänzt werden.

### 6.1 Bauwerksbuch als Quelle für GFA und BSV

GFA (`GrossFloorArea`) und BSV (`BuildingStructureVolume`) werden als UDAs im PSet `BASF_General` an `IfcSpace`-Objekten des separaten Teilfachmodells **Bauwerksbuch** bereitgestellt. Die Funktionen der Spaces sind getrennt:

- **GFA:** genau ein eigenes `IfcSpace`-Objekt je Ebene; dessen `BASF_General.GrossFloorArea` liefert die Geschossfläche in m². Der Einzelwert wird für die Ebenenauswertung gezeigt; die Werte aller Ebenen werden zusätzlich zum Bauwerks-GFA addiert. Die Ebenenzuordnung erfolgt über das PSet `Hierachy`: Aus `AvevaZONE` wird der Zonenpfad gelesen und daraus die Ebene abgeleitet (Beispiel `D708/STL/-06.00M` → Ebene `-06.00M`). Im Teilfachmodell Bauwerksbuch (OBB) wird die Bauwerkszuordnung über die UDA `BASF_General.550_Baunummer` geführt. Für AVEVA-Modelle enthält `AvevaSITE` im Beispiel `V102/D708/STL` die Baunummer als zweiten Pfadbestandteil (`D708`); im OBB ist jedoch die separate Baunummer-UDA maßgeblich.
- **BSV:** je nach Projekt entweder ein gemeinsames Volumenobjekt oder ein `IfcSpace` je Ebene; jedes Objekt trägt `BASF_General.BuildingStructureVolume` in m³. Ein gemeinsames Objekt liefert den Bauwerksgesamtwert. Bei mehreren Ebenenobjekten werden Werte je Geschoss ausgewiesen und zum Bauwerksgesamtvolumen addiert. Es wird nicht automatisch aus den GFA-Spaces oder aus `GrossVolume` abgeleitet.

Die verbindlichen Propertypfade lauten `BASF_General.GrossFloorArea` beziehungsweise `BASF_General.BuildingStructureVolume`. Werte werden nicht still durch IFC-QTOs oder Geometrie-Fallbacks ersetzt. Die Beziehung zwischen BSV-IfcSpace und Bauwerk/Geschoss ist entsprechend der gelieferten Modellstruktur auszuwerten.

Der Agent liest und prüft die Originalwerte, ordnet sie den Geschossen zu und zeigt sie auf Raum-, Geschoss- und Bauwerksebene an. Je Wert werden Quellmodell, IfcSpace-GlobalId, Space-Name/Reference, Geschoss, Originalwert, Datentyp, Einheit, Propertypfad und Prüfstatus mitgeführt. Fehlende UDAs, falsche Datentypen, unplausible Einheiten, doppelte/mehrdeutige Zuordnungen und leere Werte werden als Findings gemeldet.

Die projektspezifische BSV-Struktur wird erkannt: ein gemeinsames Objekt gilt als Bauwerksgesamtwert; mehrere Objekte mit Ebenenzuordnung werden als Geschosswerte gezeigt und summiert. Doppelte Gesamtwerte oder eine Mischung aus Gesamt- und Teilwerten sind als Konflikt zu melden, nicht zusätzlich zu addieren. Die Ebenenzuordnung wird aus `Hierachy.AvevaZONE` abgeleitet. Für OBB-Bauwerkszuordnung ist die UDA `BASF_General.550_Baunummer` maßgeblich. Erwartete Einheiten sind GFA m² und BSV m³. Werte an `IfcBuilding` oder `IfcBuildingStorey` werden als Kontrollwerte angezeigt, aber nicht zusätzlich zu den summierten IfcSpace-Werten addiert. Ein geometrischer Vergleich bleibt eine getrennte Kontrollgröße und ersetzt die UDA nicht.

### 6.2 Weitere fachliche Mengenregeln

- Betonmengen werden als Brutto ohne Öffnungsabzug und als Netto nach Abzug aller im IFC-Modell erfassten Öffnungen ausgewiesen. Öffnungen werden je Menge höchstens einmal abgezogen; die Herkunft der Öffnungsgeometrie und der Abzug bleiben nachvollziehbar. Bei Bodenplatten und Decken werden Oberfläche (Oberseite) und Unterseite jeweils separat ausgewiesen, mit Brutto- und Nettowerten.
- Definition lfm bei Geländer/Leiter: geometrische Achslänge, modellierte Teilsegmente oder freigegebene PSet-Länge.
- Rundung und Toleranz je Mengeneinheit sowie Materialnormalisierung und Materialgruppen.
- Pfahldurchmesser wird primär aus Geometrie gelesen; unterstützend werden PSets/QTOs sowie `IfcName`, `IfcDescription` und `IfcObjectType` geprüft. Die Gruppierung erfolgt nach dem tatsächlichen Durchmesser.

### 6.3 Gruppierung und Materialausgabe

Alle Mengenübersichten lassen sich nach Modell/Teilfachmodell, Bauteilgruppe und Material filtern und aggregieren. Rohmaterialname und normalisierte Materialgruppe bleiben parallel sichtbar. Mengen unterschiedlicher Dimensionen und Materialgruppen werden nicht in eine fachlich irreführende Gesamtsumme verdichtet. Für kategorisierte Mengen (Pfahldurchmesser, Fundamenttyp, Stufenmaße) sind Einzelkategorien und Gesamtsumme gemeinsam darzustellen.

## 7. UI vor Excel-Export

Die Oberfläche wird vor dem Excel-Export als professioneller, modellzentrierter Arbeitsbereich aufgebaut. Sie soll nicht wie eine klassische Eingabemaske wirken. Links steht die Projekt-/Teilmodellnavigation, zentral die gewählte Analyseansicht, rechts der Detail- und Herkunftsbereich. Gemeinsame Filter für Modell, Modellcode, Gewerk, Geschoss, Material und Prüfstatus wirken über die Ansichten hinweg. Tabellen erhalten Sortierung, Spaltenfilter, Suche, Summenzeilen, sichtbare Einheiten und klar markierte Warnungen. Ein Doppelklick auf eine Tabellenzeile öffnet die Objekt- bzw. Mengenherkunft mit GlobalId, IFC-Klasse, Name, PSet/QTO, Wert, Regel und Prüfhinweisen. Ladefortschritt und Teilmodellstatus bleiben sichtbar.

### 7.1 Navigationsansichten

1. **Projektübersicht:** eingelesene Dateien/Teilmodelle, IFC-Schema, erkannte Codes, Geschosse, Elementzahlen, Datenabdeckung und offene Findings.
2. **Modellstruktur:** Projektbaum aus Bauwerk, Teilmodell, Geschoss und Objektgruppen; Filter nach ESM/ESS/ESO/ESC/ESK/ESP sowie Material.
3. **Mengenübersicht:** Summen nach Gewerk/Bauteilgruppe, Material und Einheit; Auswahl einer Zeile führt in die enthaltenen Objekte.
4. **Bauwerksbuch / Räume:** `IfcSpace`-Liste mit GFA und BSV, Quellwert und Einheit, Space-Identität, Geschosszuordnung und Quellmodell. Summen je Ebene und Gesamtbauwerk.
5. **Objekt- und Mengendetails:** alle Mengen eines gewählten Objekts mit Rohquelle, normalisiertem Wert, Methode, Regelversion und Qualitäts-/Prüfstatus.
6. **Datenqualität / Findings:** fehlende Klassifizierungen, GUID-Probleme, nicht zugeordnete Spaces, PSet-/QTO-Lücken, Material- und Einheitenkonflikte sowie mögliche Doppelzählungen.
7. **Materialanalyse:** Mengen nach Originalmaterial und normalisierter Materialgruppe, mit Drill-down auf Objekte.
8. **Model Quality Checker:** getrennte Arbeitsbereiche für KI-gestützte IFC-Klassifizierungs- und Plausibilitätshinweise sowie deterministische EIR-/AIA-Anforderungsprüfungen.

Der Excel-Export folgt erst nach der UI-Prüfung: Die aktuell gefilterte Ansicht und eine vollständige Detail-/Rohdatenansicht müssen in der Oberfläche nachvollziehbar sein, bevor ein Export ausgelöst wird. Der Export wird anschließend aus denselben Ergebnisdaten erzeugt, die in der UI angezeigt werden. Alle Navigationsansichten werden bereits im UI-Grundgerüst sichtbar angelegt. Solange eine Datenquelle oder Auswertungsregel noch nicht implementiert ist, zeigt die Ansicht einen erklärenden Leerzustand und keine erfundenen Beispielmengen.

### 7.2 Model Quality Checker

Die UI erhält eine eigene Hauptansicht **Model Quality Checker** mit zwei getrennten Bereichen:

1. **IFC-Klassifizierungs- und Plausibilitätsprüfung:** KI-gestützte Reviewvorschläge mit Filter nach Klasse, Modell, Bauteilgruppe, Konfidenz und Status. Drill-down zeigt Objekt, Evidenz, tatsächliche und vorgeschlagene Werte sowie mögliche Auswirkungen auf Mengen.
2. **EIR-/AIA-Anforderungsprüfung:** deterministische Prüfung des IFC-Modells gegen ein ausgewähltes, freigegebenes Anforderungsprofil. Anforderungen können aus EIR/AIA-Projektdokumenten über einen KI-unterstützten Regelentwurf vorbereitet werden; ein Entwurf wird erst nach fachlicher Prüfung und Freigabe verbindlich.

Befunde sind nach Schweregrad, Anforderung/Regel-ID, Objekt, Prüflauf und Bearbeitungsstatus filterbar. KI-Vorschläge und verbindliche Regelverletzungen müssen optisch und begrifflich klar getrennt bleiben.

## 8. Bericht und optimale Ansichten

Der Bericht soll zuerst die entscheidungsrelevanten Summen zeigen und anschließend bis zum IFC-Objekt auflösbar sein.

### Ansicht A – Projektübersicht

- Dateiname, IFC-Schema, Modell-/Projektkennung, Erstellungsdatum, erkannter Modelltyp
- Anzahl Modelle, Geschosse, physische IFC-Elemente und Assemblies
- Klassifizierungsquote, GUID-Qualität, Mengenabdeckung
- Gesamtmengen nach Material und Bauteilgruppe
- offene Prüfungen und Datenqualitätsklasse

### Ansicht B – Mengenmatrix

Zeilen: Bauteilgruppe und Untergruppe.  
Spalten: Material, Anzahl, kg, to, lfm, m², m³, Qualitätsklasse, Datenabdeckung.  
Nicht anwendbare Einheiten leer lassen, nicht mit Null verwechseln.

### Ansicht C – Geschoss / Bauwerksbuch

- Bauwerksbuch-Properties und Datenvollständigkeit
- GFA m² je Ebene aus `GrossFloorArea` der `IfcSpace`-Objekte im Teilfachmodell Bauwerksbuch
- BSV m³ als eigener Bauwerkswert aus dem separaten `IfcSpace`-Volumenobjekt
- Space-Einzelnachweis; GFA-Summen je Ebene und Gesamtbauwerk; BSV-Einzelnachweis als Bauwerkswert
- je Ebene: Objektanzahl, Beton-/Stahlmengen, relevante Flächen

### Ansicht D – Material- und Modellvergleich

- Mengen nach Materialname/normalisierter Materialgruppe
- ESM/ESS/ESO/ESC/ESK als getrennte Filter oder Tabellenblätter
- Material unbekannt/mehrdeutig in eigener Gruppe

### Ansicht E – Objekt- und Herkunftsnachweis

GlobalId, Modell, IfcClass, Name, ObjectType, Geschoss, Material, Mengenwert, Einheit, Quelle, Property/QTO, Methode, Qualitätsklasse, Regel-ID/Version, Warnungen.

### Ansicht F – Prüfbericht

- fehlende IFC-Klassen, GUIDs, PSets, QTOs und Materialien
- mehrdeutige Modell-/Bauteilzuordnung
- doppelte/konfligierende Mengenquellen
- negative, nullwertige oder auffällige Werte
- wahrscheinliche Doppelzählungen, Assembly-/Leaf-Konflikte
- Geometrie-/Einheitenfehler und nicht unterstützte IFC-Entitäten

## 8. Qualitätsklassen und Findings

Vorgeschlagene Mengenqualität aus dem BCIP-Zielbild:

| Klasse | Bedeutung |
|---|---|
| A | direkte, geprüfte IFC-QTO-/Propertymenge mit passender Einheit und plausibler Zuordnung |
| B | exakt aus belastbarer Geometrie abgeleitete Menge |
| C | vereinfachte Geometrieberechnung mit dokumentierter Annahme |
| D | Kennwert oder Schätzung; keine direkte Modellmenge |
| E | fehlend, widersprüchlich oder nicht belastbar |

Jedes Finding enthält Schweregrad, betroffene GlobalIds, Regel-ID, Befund, Auswirkung, Vorschlag und Status (offen/akzeptiert/behoben). Ein Finding ändert die IFC-Daten nicht.

### 8.1 Prüfbereich A – KI-gestützte IFC-Klassifizierungsprüfung

Die KI analysiert Modellobjekte anhand der in Abschnitt 3.3 aufgeführten Merkmale und liefert begründete Reviewvorschläge. Die Prüfung ist unterstützend und darf keine Modelländerung auslösen. Jeder Befund dokumentiert mindestens GlobalId, Modellrevision, tatsächliche IFC-Klasse und Kernattribute, vorgeschlagene Alternative (falls vorhanden), Evidenz/Quellen, Begründung, Konfidenz, Regelversion sowie Status (neu, geprüft, bestätigt, verworfen). Unsicherheit oder fehlende Evidenz muss sichtbar sein.

Fachlich bestätigte Entscheidungen werden versioniert in das Regelpaket und in Regressionstests überführt. Nicht bestätigte Vorschläge bleiben Vorschläge. Die Mengenengine nutzt weiterhin die tatsächliche Modellklassifizierung; ein Reviewbefund kann mögliche Folgen erläutern, aber keine Ergebnisse still verändern.

### 8.2 Prüfbereich B – EIR-/AIA-Reviewer

Der EIR-/AIA-Reviewer prüft den gelieferten IFC-Datenstand deterministisch gegen ein ausgewähltes und freigegebenes Projektanforderungsprofil. Der Sollzustand kann Anforderungen aus EIR/AIA sowie freigegebene BASF_General-Definitionen aus dem BASF Rulebook enthalten. Der BASF_General Editor bildet den Sollzustand und dessen Propertydefinitionen ab; der Ifc PSet Explorer steht für die Analyse des tatsächlich gelieferten IFC-Zustands. Der Reviewer verbindet beide Seiten, ohne ihre Rollen zu vermischen.

Je Anforderung prüft der Reviewer mindestens:

- Anwendbarkeit auf Modell, IFC-Klasse/Objektgruppe, Projektphase und Planungsstand;
- Vorhandensein von PSet und Property sowie Befüllungsstatus;
- erwarteten Datentyp und zulässige Werte;
- freigegebene Auswahllisten oder Freitextvorgaben einschließlich definierter Format-/Validierungsregeln;
- bedingte Anforderungen, darunter die im BASF-Regelwerk definierte Abhängigkeit vom `504_Planungsstand`;
- Herkunft, Regel-ID/-Version und Prüfresultat je betroffenem Objekt.

Wenn Anforderungen nur als Dokumenttext vorliegen, kann KI daraus einen **Regelentwurf** mit Zuordnung zu betroffenen Objekten, Propertypfaden, Pflichtstatus, Datentypen, Auswahllisten und Bedingungen erstellen. Der Entwurf ist nicht ausführbar als verbindliche Prüfung, bis ein fachlich Verantwortlicher ihn geprüft und freigegeben hat. Die freigegebene Prüfung selbst läuft deterministisch und reproduzierbar. Unklare oder widersprüchliche Anforderungen werden als Klärfall ausgewiesen, nicht von der KI verbindlich ausgelegt.

Jeder EIR-/AIA-Befund enthält mindestens Objektbezug (GlobalId), Anforderung, tatsächlichen Wert/Pfad, erwartete Regel, Prüfergebnis, Schweregrad, Regelprofil/-version und Status. Ein Reviewer-Befund verändert das IFC-Modell nicht.

## 9. Regelpakete und Konfiguration

Mengen-, Klassifikations- und EIR-/AIA-Anforderungsregeln werden als versionierte Knowledge Packages verwaltet. Eine Regel bzw. Anforderung enthält – soweit zutreffend – Quelle, Geltungsbereich, Propertypfad, erwarteten Datentyp/Wertebereich, Pflichtstatus, Bedingungen und Freigabestatus. KI-generierte EIR-/AIA-Regelentwürfe bleiben bis zur fachlichen Freigabe unverbindlich. Geeignete Tabellen/Dateien sind YAML/JSON für Laufzeitregeln sowie Excel für fachliche Pflege und Prüfung. Eine Regel enthält mindestens:

- Regel-ID, Titel, Version, Gültigkeit und Modelltyp
- IFC-Klassen, Modellcodes, Name/ObjectType/Description-Filter
- PSet/QTO/Property-Pfade und Prioritäten
- Mengendimension, Ziel-Einheit und Umrechnungsfaktor
- Filter-/Ausschlussbedingungen und Assembly-Strategie
- Material-/Geschoss-/Positionsgruppierung
- Fallbackmethode, Qualitätsklasse und Toleranz
- Testfälle und erwartetes Ergebnis

Regeln sollen fachlich versioniert und gegen bekannte IFC-Beispiele regressionsgeprüft werden. Eine aktualisierte Regel darf alte Ergebnisse reproduzierbar lassen.

### 9.1 Verbindliche Fachpakete Stahlbau und Betonbau v0.2

Die [Stahlbauübergabe](../handover/stahlbau/v0.2/IFC_Quantity_Agent_Stahlbau_Konzept_v0.2.md) und die [Betonbauübergabe EFx/ECx](../handover/betonbau/v0.2/IFC_Quantity_Agent_Betonbau_Konzept_v0.2.md) konkretisieren diesen Auftrag. Zugehörige Excel-/JSON-Dateien, Prüfvermerke und Original-ZIPs sind im [Paketindex](../handover/README.md) verlinkt. Sie sind noch keine aktiv geladenen Laufzeitregeln. Keine Kategoriegrenzen im Programmcode fest einbauen. Die bereitgestellten Grenzen sind anpassbare Projektvorschläge, keine allgemein normativen Klassen.

| Bereich | Verbindlicher Umfang |
|---|---|
| Stahlbau | Profilfamilie, Profilreihe, genaue Profilbezeichnung, Herstellungsart und Werkstoff getrennt; Einzelmassen- und Profilmetergewichtskategorien; Einzelteil, Fertigungsbaugruppe und Montageeinheit getrennt |
| Stahlbleche | Benutzerprofile für Dicke, Länge, Breite, Fläche und Einzelmasse; tatsächliche Dicke aus bestätigter Quelle/lokaler Geometrie; gedrehte und gekantete Bleche nicht über globale Außenabmessungen klassieren |
| Betonbau EFx/ECx einschließlich ECA | Vollständige Bauteiltaxonomie aus dem Paket, 41 Bauteilarten plus ungeklärte Objekte; Flach-/Tiefgründung, Platten, Wände, Stützen, Balken, Treppen und Sonderbauteile |
| Betonstützen | Breite/Höhe mit lokalen Achsen, Runddurchmesser, Querschnittsfläche, Stützenhöhe und Einzelvolumen; Rechteck und Rund getrennt |
| Betonwände | Dicke normal zur Bezugsfläche, Höhe, Achslänge, Wandansichtsfläche und Einzelvolumen; Ansichtsfläche und Schalungsfläche getrennt |
| Mengenbasis | Brutto, Netto und Vertragsmenge getrennt; Betonvolumen, Schalung und Bewehrung eigenständig; Öffnungen nur einmal abziehen; Materialabdeckung und Überschneidungen nachweisen |

Das Modellcode-Mapping aus Abschnitt 4 und `540_LV_Ident` bleiben führend. Unbekannte oder widersprüchliche LV-Werte erzeugen einen Klärfall; keine frei erfundene Zuordnung. `Qto_BeamBaseQuantities` ist kein vollständiger Baugruppenmassennachweis einschließlich Anbauteilen. Die vorhandene MVP-1-Definition von nativem `NetVolume` bleibt erhalten; spätere Geometrieableitungen erhalten eine eigene Methode/Quelle und überschreiben keinen nativen QTO-Wert.

### 9.2 Benutzerdefinierte Kategorieprofile – gemeinsame Kernfunktion

PR01–PR20 in beiden Fachkonzepten sind gemeinsam verbindlich. Dieselbe Fachlogik dient API und Oberfläche; keine getrennten Klassierer pro Gewerkeoberfläche.

1. Schreibgeschützte Standardprofile als eigenes Profil kopieren; zusätzlich anlegen, benennen, bearbeiten, duplizieren, auswählen und archivieren. Persönliche und projektbezogene Profile getrennt speichern; Freigabe an Kollegen mit Berechtigungen vorsehen.
2. `profile_id`, Version, Ursprung, Änderungszeit und Inhalts-Fingerprint speichern. Fachliche Änderung erzeugt eine neue Version; bestehende Berichte referenzieren unverändert ihren alten Profilstand.
3. Messgröße, Dimension, Anzeigeeinheit, strukturierter Scope, Mengenbasis und Auswertungsebene explizit festlegen. Leerer/ungültiger Scope bedeutet nicht automatisch alle Objekte. Unbekannte Messalgorithmen müssen vor Verwendung fachlich registriert werden.
4. Originalwert, Quelle und Einheit erhalten; kanonisch m, m², m³, kg beziehungsweise kg/m verwenden. Exakte Maßgruppen und Intervalle parallel anbieten. Pfahl-Ø und Standardquerschnitte bleiben exakt verfügbar; keine unbeauftragte Rundung/Toleranz oder Ersatzdurchmesser.
5. Untergrenze exklusiv, Obergrenze inklusive; keine Rundung vor Zuordnung. Offene letzte Obergrenze als JSON `null` beziehungsweise Excel-Leerwert. Überlappende Bänder und doppelte Codes pro Profil ablehnen. `complete` verlangt lückenlose positive Abdeckung, `partial` erlaubt bewusste Lücken mit `out_of_range`.
6. `unknown`, `invalid`, `variable`, `not_applicable`, `out_of_range` und `conflict` sichtbar ausweisen. Variable Wand-/Blechdicken und Stützenquerschnitte nicht ungefragt über Mittel-/Maximalwerte klassieren. Null und negative Größen bleiben prüfbare Rohwerte, erhalten aber keine gültige Größenklasse.
7. Vorschau zeigt Objektzahlen je Band und Sonderstatus mit Drilldown. Erst validierte und ausgewählte Profile anwenden; mitgelieferte Entwurfsvorlagen bleiben deaktiviert. Kombinierte Filter bilden Schnittmengen, ein Profilwechsel verändert keine Rohmengen und erzeugt keine zusätzliche Materialsumme.
8. Excel-/JSON-Import vollständig validieren und atomar übernehmen. Bei Fehlern bleibt die letzte gültige Konfiguration erhalten. Identische ID/Version mit anderem Inhalt ablehnen. Excel-/JSON-Konsistenz ist vor Freigabe nachzuweisen; die gelieferte Übergabe besitzt noch keine automatische Synchronisation.
9. Je Zuordnung mindestens `profile_id`, `profile_version`, `profile_fingerprint`, `metric`, `category_code`, `classification_status`, `canonical_value`, `quantity_basis`, `evaluation_level` und Objekt-/Modellbezug ausgeben. Berichte speichern Modell-Inhaltshash und Profilversionen; derselbe Dateiname beweist keinen identischen Modellstand.

Blechnet-/Bruttofläche, Mittelfläche, Oberfläche und bestätigte Abwicklung sind verschiedene Metriken. Ebenso bleiben Wandansichtsfläche, Öffnungsabzug und tatsächliche Schalungskontaktfläche eigenständig. Die Profilfunktion verändert weder IFC-Daten noch Modellverschachtelungen.

## 10. Plattformneutrale Zielarchitektur

Der Agent muss als eigenständiges, plattformneutrales Fachsystem funktionieren. Copilot, ChatGPT oder eine andere Oberfläche dürfen die IFC-Auswertung verwenden, aber weder die fachliche Logik noch die Ergebnisdaten besitzen oder ersetzen.

### 10.1 Komponenten

1. **Domain Model und Core Services:** gemeinsame Datenmodelle und Dienste für Projekte, Teilmodelle, Construction Objects, Mengen, Findings, Regelpakete und Audit. Fachlogik ohne Bindung an eine KI oder GUI.
2. **IFC-/Geometrie-Adapter:** IFC-Modellöffnung, Einheiten, Beziehungen, PSets/QTOs, Material, Geometrie, GUID-Deduplizierung und räumliche Zuordnung. IFC-Schema- und Bibliotheksversionen werden gekapselt und getestet.
3. **Quantity- und Rule-Engine:** deterministische Mengenquellen, Assembly-Handling, Berechnungen, Validierung und Qualitätsbewertung.
4. **Model Quality Services:** KI-gestützte, evidenzbasierte Klassifizierungsvorschläge sowie ein deterministischer EIR-/AIA-Regelprüfer. KI-Vorschläge und Regelentwürfe werden getrennt von freigegebenen Regeln gespeichert und ändern keine IFC-Daten oder verbindlichen Mengen.
5. **API-Schicht:** versionierte REST-API mit OpenAPI-Vertrag für Import, Analyse, Status, Ergebnisse, Findings und Detailnachweise. JSON-Schemata definieren die plattformunabhängigen Ein- und Ausgaben. MCP kann als zusätzlicher Adapter bereitgestellt werden, sofern ein Host es unterstützt.
6. **UI:** responsive, modellzentrierte HTML-Oberfläche. Sie arbeitet direkt mit der API und bleibt auch ohne Copilot benutzbar.
7. **Host-Adapter:** getrennte Integrationen für Copilot und weitere Assistenten. Sie übersetzen Host-Aktionen in API-Aufrufe und geben die Core-Ergebnisse unverändert zurück. Kein Host-spezifischer Code in der Mengenlogik.
8. **Export und Persistenz:** Excel/CSV/JSON-Ausgabe und revisionsbezogene Speicherung aus denselben geprüften Ergebnisdatensätzen.

### 10.2 Microsoft Copilot-Kompatibilität

Die Architektur muss eine Anbindung an Microsoft 365 Copilot ermöglichen, zum Beispiel über einen deklarativen Agenten mit REST-/OpenAPI-Plugin oder – falls vom Zieltenant unterstützt – MCP-Plugin. Copilot Studio kann als separate Low-Code-Option für Agentenaufbau und Veröffentlichung geprüft werden. Copilot ruft dabei Funktionen des IFC Quantity Agent auf; IFC-Parsing, Mengenberechnung, Regeln, Prüfstatus und Ergebnis-Herkunft verbleiben in den Core Services.

Die technische Kompatibilität ist unabhängig von der KI-Plattform. Ob eine konkrete Copilot-Integration mit dem vorhandenen „Copilot Premium“-Abonnement nutzbar ist, muss vor der Bereitstellung anhand des genauen Lizenzprodukts, Tenant-Setups und der Administrationsrichtlinien geprüft werden. Microsoft beschreibt API- und MCP-Plugins für deklarative Agents; Verfügbarkeit und Lizenzierung können je nach Host variieren.

### 10.3 Bedienbarkeit, Sicherheit und Erweiterbarkeit

- Kernablauf mit wenigen Schritten: Teilmodelle wählen → Analyse starten → Ergebnisse prüfen → optional exportieren.
- Verständliche deutsche Fachbegriffe, Tooltips und kontextbezogene Hilfe; technische IFC-Begriffe bleiben in Objekt- und Quellen-Details sichtbar.
- Ladefortschritt, Abbruchmöglichkeit, klare Fehlermeldungen und Wiederaufnahme bei großen Modellen.
- Rollen- und Berechtigungskonzept sowie nachvollziehbares Audit; sensible IFC-Dateien werden nur an freigegebene Dienste übergeben. Daten werden nicht ohne ausdrückliche Konfiguration an ein KI-Modell gesendet. Für KI-Prüfungen werden nur freigegebene, erforderliche Modellmerkmale übertragen; vollständige Geometrie ist nicht standardmäßig an ein KI-Modell zu senden.
- UI, API und Agent-Host sind separat versioniert und testbar. Ein Wechsel von Copilot zu einem anderen Host darf keine Änderung an Berechnungsergebnissen verursachen.
- Abnahmetests prüfen dieselben Eingaben und Ergebnisse über UI, API und Host-Adapter.

Jeder `QuantityResult` führt mindestens Modell-ID, GlobalId(s), Mengentyp, Wert, Einheit, Quelle, Methode, Qualitäts-/Prüfstatus, Regel-ID/-Version, Annahmen und Warnungen. Projektergebnisse müssen aus Regelversion und IFC-Revision reproduzierbar sein.

**Microsoft-Referenzen:** [MCP- und API-Plugins für deklarative Agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-plugins), [Declarative Agents für Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-declarative-agent), [Copilot Studio – Agentenübersicht](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-overview).

## 11. MVP-Umfang und Ausbaureihenfolge

### MVP 1 – Einlesen, Qualität und UI-Grundgerüst

IFC öffnen, Modellmetadaten und Einheiten erkennen, physische Elemente/Assemblies zählen, fehlende/duplizierte GUIDs und unklassifizierte Objekte berichten, PSets/QTOs/Materialien inventarisieren. Dazu das UI-Grundgerüst mit Projektübersicht, Modellstruktur, Prüfbericht und Objekt-Drill-down bauen. Noch kein Excel-Export.

### MVP 2 – Model Quality Checker

EIR-/AIA-Anforderungsprofile und BASF-Regeln deterministisch gegen IFC-Objekte prüfen; Befunde mit Regelherkunft und Drill-down darstellen. KI-gestützte Klassifizierungshinweise zunächst als klar gekennzeichnete Reviewvorschläge mit Evidenz, Konfidenz und Status bereitstellen. Regelentwürfe aus EIR/AIA-Dokumenten bleiben bis zur fachlichen Freigabe unverbindlich.

### MVP 3 – Erste Objektgruppen und Stahlmodelle

ESM/ESS/ESO/ESC/ESK erkennen; Stahlgewicht mit BASF-Gewichtspriorität; erste freigegebene Regeln beispielsweise für Geländer, Steigleiter, Sicherungstüren und Bühnenbelag; Material- und Modellübersichten; Assembly-Doppelzählung verhindern. Die Liste bleibt offen und wird über versionierte Regelpakete erweitert, ohne neue Kategorien fest in den Programmcode einzubauen.

Für MVP 3 gilt zusätzlich das Stahlbaupaket v0.2 nach Abschnitt 9.1. Die gemeinsame Profilfunktion nach Abschnitt 9.2 ist mit der ersten Kategorienauswertung bereitzustellen, insbesondere für Bleche.

### MVP 4 – Beton und Gründung

Fundamente, Bodenplatte, Tiefgründung, Aufkantungen, Wände, Stützen, Unterzüge und Decken. IFC-QTOs zuerst dort, wo semantisch passend; sonst freigegebene Geometrie-/PSet-Regeln.

Für MVP 4 gilt zusätzlich das Betonbaupaket v0.2, insbesondere benutzerdefinierte Stützen- und Wandprofile sowie exakte Pfahl-/Querschnittsgruppen. Dieselbe Profilengine aus MVP 3 wird wiederverwendet.

### MVP 5 – Bauwerksbuch und IfcSpace-Ansicht

Teilfachmodell Bauwerksbuch erkennen und die getrennten GFA-Ebenen-IfcSpaces sowie das eigenständige BSV-Volumen-IfcSpace auswerten. GFA je Ebene und als Gesamtwert aggregieren; BSV als einzelnes Volumenobjekt führen. Mehrfachobjekte, fehlende Zuordnung oder unklare Additivität als Findings zeigen. UI-Ansicht und Herkunftsnachweis fertigstellen.

### MVP 6 – Excel-Export

Excel-Export erst nach UI-Prüfung ergänzen. Die Exportblätter werden aus denselben gefilterten und geprüften Ergebnisdaten aufgebaut, die der Nutzer in der Oberfläche kontrolliert.

Der Excel-/JSON-Austausch von Kategorieprofilen gehört zur Konfigurationsverwaltung in MVP 3/4 und ist unabhängig vom Mengenbericht-Export in MVP 6.

### MVP 7 – Plattformadapter und BCIP-Anbindung

Versionierte REST-/OpenAPI-Schnittstelle und Host-Adapter bereitstellen. Microsoft 365 Copilot als erster Integrationsadapter wird anhand der verfügbaren Lizenz- und Tenant-Bedingungen geprüft. Danach Projekt-/Modellverwaltung, revisionsbezogene Speicherung, Multi-IFC, Knowledge Packages und Model-to-LV-Verknüpfung ausbauen.

## 12. Abnahmekriterien

- Modell- und Elementzahlen stimmen mit einer unabhängigen Referenzzählung überein; Assemblies werden nach dokumentierter Zählregel behandelt.
- Jedes ausgegebene Ergebnis ist bis zum Objekt und zur Mengenquelle zurückverfolgbar.
- `BASF_General.540_LV_Ident` steuert die Zuordnung aller Objektgruppen; IFC-Textattribute dienen nur bei fehlendem oder leerem UDA-Wert als gekennzeichnete Fallbacks. Regeln sind erweiterbar, Konflikte und Mehrdeutigkeiten werden sichtbar und nicht still verworfen oder umklassifiziert.
- Summen nach Modelltyp, Bauteilgruppe und Material sind konsistent mit der Detailtabelle.
- Einheitenumrechnung, Rundung und Null-/Fehlwertbehandlung sind getestet.
- Stahlgewicht folgt der konfigurierten BASF-/Tekla-/BaseQuantities-Priorität.
- GFA, BSV und Oberflächen verwenden dokumentierte Definitionen.
- Ergebnisse sind mit IFC-Datei, Regelpaketversion und Exportdatum reproduzierbar.
- Prüfberichte enthalten alle Abweichungen, die Summen oder fachliche Zuordnung beeinflussen.
- Model Quality Checker unterscheidet KI-Hinweise nachvollziehbar von deterministischen Regelverletzungen. KI-Befunde enthalten Evidenz, Konfidenz und Status und verändern weder IFC-Daten noch Mengen.
- EIR-/AIA-Prüfungen sind aus freigegebenen, versionierten Anforderungen reproduzierbar; Dokument-basierte KI-Regelentwürfe können vor Freigabe keine verbindlichen Befunde erzeugen.

### 12.1 Zusätzliche Abnahme der Fachpakete und Profile

- Je Fachpaket die 32 ursprünglichen fachlichen Sollfälle und 20 Profil-Sollfälle als automatisierte Prüfungen umsetzen. Gemeinsame Profilfälle dürfen parametrisiert sein; die Abdeckung beider Kataloge ist nachzuweisen.
- Grenzwerte, Einheitenwechsel, vollständige/partielle Intervalle, Überschneidungen, ungültige Scopes, Importabbruch, Versionskonflikte und Reproduzierbarkeit prüfen.
- Runde/rechteckige/variable Stützen, variable Wände sowie gedrehte, gelochte und gekantete Bleche mit passenden Quellen und Sonderstatus nachweisen.
- Profilwechsel erhält Rohmengen und Gesamtsummen; Assembly-/Einzelteilsicht sowie unterschiedliche Profile erzeugen keine Doppelzählung.
- Vorschau, API-Zuordnung, UI-Filter und späterer Export liefern dieselben Core-Ergebnisse. Reale IFC4-/IFC4.3-Adaptertests kommen zu den Katalogprüfungen hinzu.
- Die mitgelieferten Prüfvermerke bestätigen Katalogkonsistenz, keine bereits erfolgreiche Agentenintegration. Baseline und bestehende MVP-1-Regeln bleiben unverändert.

## 13. Versionsänderung in v1.9

v1.9 übernimmt alle fachlichen Festlegungen aus v1.8 unverändert und erweitert das Zielbild um den Model Quality Checker. Neu sind (1) ein KI-gestützter IFC-Klassifizierungs- und Plausibilitätsprüfer, der Evidenz und Konfidenz ausweist und ausschließlich Reviewvorschläge erstellt, sowie (2) ein deterministischer EIR-/AIA-Reviewer gegen freigegebene Projektanforderungen und BASF-Regeln. KI kann aus EIR/AIA-Dokumenten Regelentwürfe vorbereiten; erst nach fachlicher Freigabe werden diese ausführbar. UI, Regelpakete, MVP-Reihenfolge, Sicherheit und Abnahmekriterien sind entsprechend erweitert.

## 14. Abgleich mit der erweiterten Anforderung (Stand v1.8)

Die Anforderungsliste wurde mit dem bestehenden Konzept abgeglichen. Bereits abgedeckt sind IFC-Einlesen, getrennte Zählung von Elementen und Assemblies, unklassifizierte Objekte, semantische PSet-/QTO-/Materialanalyse, offene Objektgruppentaxonomie, UI-Ansichten, Material-/Modellfilter und nachvollziehbare Mengenquellen. Bestätigt bzw. ergänzt wurden: Gründung und Stahlbetonbau sind getrennte Teilmodelle mit den Codes EFD/EFF/EFB/EFI/EFP beziehungsweise ECS/ECI/ECP/ECL. Zusätzlich sind ECA als kombinierte Projektvariante Stahlbeton/Massivbau und ESA als kombinierte Projektvariante Stahlbau vereinbart. Beide Codes sind als Projektcodes zu behandeln, da sie in den vorliegenden Codeübersichten nicht aufgeführt sind. Es gibt genau einen GFA-IfcSpace je Ebene; Einzelwerte dienen der Ebenenauswertung und werden zusätzlich zum Gesamt-GFA addiert. Die Ebenenzuordnung erfolgt über `Hierachy.AvevaZONE`; die OBB-Bauwerkszuordnung erfolgt über `BASF_General.550_Baunummer`. BSV kann als gemeinsamer Bauwerks-IfcSpace oder als je Ebene getrennter IfcSpace geliefert werden; bei Ebenenobjekten sind Geschosssummen und Bauwerksgesamtwert auszugeben. Aufkantungs-lfm folgt der Bauteil-Längsachse. Gitterroststufenmaße sollen primär geometrisch abgeleitet und durch PSet/QTO/Textmerkmale unterstützt werden.

**Noch fachlich zu bestätigen:** Für Geländer/Leitern bleibt die lfm-Regel offen. Das PSet `Hierachy` mit `AvevaSITE`, `AvevaZONE`, `AvevaSTRU` und `AvevaFRMW` ist anhand des Beispiels verstanden; die Ebene wird aus `AvevaZONE` abgeleitet. GFA-/BSV-Logik, Brutto-/Netto-Behandlung aller modellierten Öffnungen, getrennte Ober-/Unterseiten bei Bodenplatten/Decken, exakte Gitterroststufen-Maße, tatsächliche Pfahldurchmesser-Gruppierung und doppelte Materialausgabe sind fachlich festgelegt. Offene Werte werden sichtbar gekennzeichnet und nicht stillschweigend angenommen.

## 15. Nächster Umsetzungsschritt

Stand 01.11.2026: MVP-1-Collector, API und UI v0.3.4 liegen auf `feature/mvp1-api-ui` in der offenen Draft-PR #1; `main` enthält bisher nur die initiale README. Die Kategoriepakete sind mit diesem Auftrag im Entwicklungsbranch eingeordnet, aber noch nicht funktional integriert. Aktueller Implementierungsstand: [PROJECT_STATE.md](../../PROJECT_STATE.md).

1. Bestehende MVP-1-UI fachlich/visuell am Referenzmodell abnehmen; Modell-Inhaltshash, IFC-Schema, Exportzeitpunkt und abweichenden Referenzstand prüfen. Bestehende Regression beibehalten.
2. Gemeinsamen Import-/Validierungsvertrag der beiden v0.2-Pakete und die Profilengine nach 9.1/9.2 implementieren. Vor produktiver Zuordnung BASF-Rulebook und LV-Mapping abgleichen; Vorschlagsprofile nicht automatisch freigeben.
3. Fachmodule gemäß MVP-Reihenfolge anbinden: Stahlbau einschließlich Blechen in MVP 3, Beton/Gründung einschließlich Stützen/Wänden in MVP 4. UI/API-Vorschau, Drilldown und versionsbezogene Auswahl gehören zur jeweiligen Integration.
4. Die Fach- und Profil-Sollfälle automatisieren, reale IFC4-/IFC4.3-Modelle prüfen und Integration separat dokumentieren. Die bestehende 3D-Viewer-Anbindung über GlobalIds bleibt ein eigener Umsetzungsschritt.

Model Quality Checker und Copilot-Adapter folgen weiterhin den Abschnitten 8 und 10/11. Keine Mengen- oder Regeländerung durch einen KI-Vorschlag. **Offene fachliche Klärpunkte:** Geländer-/Leiter-lfm-Regel, freigegebene `540_LV_Ident`-Mappings und Geometrie-/Toleranzkonventionen. Fehlende Festlegungen sichtbar lassen.

## 16. Versionsänderung in v1.10

v1.10 übernimmt das Zielbild und die Festlegungen aus v1.9. Die in der Projektübersicht nachgereichten Teilfachmodell-Codes wurden ergänzt: EFD/EFF/EFB/EFI/EFP für Gründung, ECS/ECI/ECP/ECL für Stahlbetonbau sowie ESM/ESS/ESO/ESC/ESK/ESP für Stahlbau. Die kombinierte Variante ECA wurde als Projektkonvention dokumentiert. Damit entfielen die zuvor offenen EF-/EC-Codefamilien; die Geländer-/Leiter-lfm-Regel blieb offen.

## 17. Versionsänderung in v1.11

v1.11 übernimmt v1.10 und präzisiert die kombinierten Projektvarianten: ECA steht für ein kombiniertes Teilfachmodell Stahlbeton/Massivbau; ESA steht für ein kombiniertes Teilfachmodell Stahlbau. Beide Codes sind Projektcodes und waren in den vorgelegten Codeübersichten nicht enthalten. Die übrigen Codes und fachlichen Festlegungen bleiben unverändert.


## 18. Versionsänderung in v1.12 – 01.11.2026

Übernahme beider unveränderter Übergabepakete v0.2 in `docs/handover/`, mit Fachkonzept, Excel, JSON, Prüfvermerk und Original-ZIP je Gewerk. Neue verbindliche Abschnitte 9.1/9.2 integrieren Stahl-/Betonkategorien und benutzerdefinierte Profile, insbesondere für Stützen, Wände und Bleche. MVP-Zuordnung, Abnahme, Import-/Exportregeln und Ergebnisvertrag sind ergänzt. AGENTS.md, README und Projektstatus verweisen auf v1.12. v1.11 bleibt historische Grundlage. Die Profil- und Kategorienfunktionen sind weiterhin als ausstehende Implementierung gekennzeichnet.
