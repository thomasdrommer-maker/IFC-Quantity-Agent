# UI v0.3.11 – Native IFC-Attribute und BIM_Core

1. ZIP neu entpacken, Starter öffnen, UI v0.3.11 kontrollieren und IFC erneut laden.
2. Modellstruktur öffnen, Objekt Konsole (bisher STEP-ID 365) suchen.
3. Erwartet bei unverändertem Export: Description „Betonunterzug_b30“, ObjectType „Stahlbetonunterzug“, jeweils mit Quelle BIM_Core und Hinweis auf leeres natives Attribut.
4. Native IfcName „Konsole“ und BIM_Core.IfcName „Unterzug_b30“ bleiben getrennt sichtbar. Keine stillschweigende Gleichsetzung der Namen.
5. Nach „Stahlbetonunterzug“ suchen. Erwartet: Objekt auffindbar.
6. Zusatzangaben aus-/einblenden, Gruppen zuklappen/wieder öffnen und Objekt-Drilldown testen.

Automatische Prüfungen erfolgreich, 2 fachliche Referenzprüfungen ohne Original-IFC übersprungen.
Nächste Schritte: Abgleich mit Nutzerdatei, dann verbleibende MVP-1-Abnahme einschließlich Baugruppen an geeignetem Modell.
