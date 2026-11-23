# UI v0.3.9 – Gruppen zuklappen

1. In neuen Ordner entpacken, Starter öffnen und UI v0.3.9 prüfen.
2. IFC laden, Modellstruktur öffnen und mehrere Untergruppen aufklappen.
3. Bei einer Gruppe „Untergruppen zuklappen“ wählen. Erwartet: diese Gruppe bleibt offen, ihre Untergruppen schließen; andere Zweige bleiben unverändert.
4. „Alle Gruppen zuklappen“ wählen. Erwartet: alle Gruppen der aktuellen Ansicht schließen.
5. Gruppen erneut öffnen und ein Objekt anklicken. Erwartet: Baum und richtige Objektdetails weiterhin verfügbar.
6. LV-Ident-Gruppen, Suche und Filter prüfen und Zuklappen wiederholen.

Bestätigt: Nutzerabnahme von v0.3.8 (Version, Einstieg, Ansichtsbuttons).
Noch offen: Nutzerabnahme v0.3.9, Baugruppenprüfung mit geeignetem IFC und vollständige MVP-1-Abnahme.

Automatisiert: 19 Python-Tests erfolgreich, 2 Referenzprüfungen mangels Original-IFC übersprungen. Struktur- und Scrollbrowserprüfung erfolgreich.
