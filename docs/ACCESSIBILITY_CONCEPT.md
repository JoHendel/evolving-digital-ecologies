# Accessibility-Konzept: Evolution sichtbar und hoerbar machen

## Grundidee

Das Projekt soll evolutionaere Dynamik nicht nur als abstrakte Datenreihe darstellen, sondern fuer unterschiedliche Wahrnehmungsformen zugaenglich machen. Deshalb kombiniert die Simulation visuelle Darstellung, akustische Sonifikation und textuelle Zusammenfassungen.

## Fuer taube oder schwerhoerige Menschen

Die Simulation bietet starke visuelle Signale:

- Agenten sind sichtbar in der 2D-Welt.
- Abstammungslinien werden durch Farben unterschieden.
- Die dominante Linie wird hell umrandet.
- Ein Dashboard zeigt Population, Ressourcen, Trait-Diversitaet, dominante Linie und mittlere Generation.
- Nach dem Lauf werden Plots erzeugt, die Trends visuell erklaeren.

Dadurch kann evolutionaere Dominanz ohne Ton verstanden werden.

## Fuer blinde oder sehbehinderte Menschen

Die Simulation erzeugt eine Sonifikation:

- Die mittlere Generation beeinflusst die Tonhoehe.
- Dominanz einer Linie beeinflusst Lautstaerke und Klangklarheit.
- Trait-Diversitaet erzeugt ein komplexeres Klangbild.
- Wenn sich eine Linie durchsetzt, wird der Klang stabiler.

Zusaetzlich wird nach dem Lauf eine einfache Textdatei `accessible_summary.txt` erzeugt. Diese kann mit Screenreadern gelesen werden und beschreibt die wichtigsten Ergebnisse in Alltagssprache.

## Wissenschaftlicher Mehrwert

Die Sonifikation ist nicht nur ein Effekt, sondern eine alternative Datenkodierung. Sie macht Divergenz, Konvergenz, Dominanz und Stabilisierung wahrnehmbar. Wenn eine Population divers ist, klingt das System komplexer. Wenn eine Linie dominant wird, stabilisiert sich der Klang.

## Praesentationssatz

Das Projekt macht Evolution multimodal erfahrbar: Hoerende Personen koennen Dominanz und Diversitaet akustisch verfolgen, sehende Personen koennen Linien und Muster visuell erkennen, und Screenreader-Nutzer koennen die Ergebnisse ueber eine automatisch erzeugte Textzusammenfassung nachvollziehen.

