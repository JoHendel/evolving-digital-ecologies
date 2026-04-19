# Kurze Vorstellungszusammenfassung

## Elevator Pitch

Ich habe eine Artificial-Life-Simulation entwickelt, in der einfache digitale Organismen in einer dynamischen 2D-Umwelt leben. Sie suchen Ressourcen, verbrauchen Energie, sterben, reproduzieren sich und vererben mutierbare Eigenschaften. Dadurch entsteht Evolution nicht durch eine vorgegebene Fitnessfunktion, sondern durch Ueberleben und Fortpflanzung innerhalb der simulierten Umwelt.

In der finalen Version wird diese Evolution nicht nur berechnet, sondern multimodal erfahrbar gemacht: Man kann sie sehen, hoeren und nach dem Lauf als Text und Diagramm auswerten.

## Forschungsfrage

Die zentrale Frage lautet: Wie koennen aus einfachen lokalen Regeln, Mutation, Vererbung, Ressourcenknappheit und Umweltgefahren emergente Populationsmuster entstehen?

## Was wird simuliert?

- Eine 2D-Welt mit Ressourcen, fruchtbaren Zonen, armen Zonen und Gefahrenbereichen
- Agenten mit Energie, Alter, Gesundheit, Position und Abstammung
- Vererbbare Traits wie Geschwindigkeit, Wahrnehmung, Metabolismus, Aggression und Sozialtendenz
- Reproduktion mit Mutation
- Selektion ueber Ueberleben und erfolgreiche Fortpflanzung

## Warum ist das wissenschaftlich interessant?

Das System zeigt, wie kollektive Muster entstehen koennen, ohne dass diese direkt programmiert werden. Wenn Agenten clustern, aussterben, dominante Linien bilden oder bestimmte Traits bevorzugt ueberleben, dann ergibt sich das aus lokalen Interaktionen und Umweltbedingungen.

## Technischer Aufbau

Das Projekt ist modular aufgebaut:

- `world`: Umwelt, Ressourcen und Gefahren
- `agents`: digitale Organismen und Traits
- `behavior`: Entscheidungslogik
- `evolution`: Mutation, Reproduktion, Lineage
- `simulation`: Simulationsengine
- `analytics`: Metriken und Datenexport
- `visualization`: Live-Bild und Plots
- `experiments`: Parameter-Sweeps

## Wichtiges Ergebnis aus dem Beispielrun

Im Lauf `long_live_analysis` lief die Simulation 15.000 Schritte. Die Population ueberlebte, erreichte maximal 366 Agenten und endete mit 187 Agenten. Besonders interessant war, dass am Ende nur noch eine Abstammungslinie uebrig blieb.

Das deutet auf einen evolutionaeren Sweep hin: Eine Linie hatte eine besonders erfolgreiche Trait-Kombination und hat die anderen Linien verdraengt.

Zusaetzlich misst der Baseline Distance Index, wie weit sich das System vom Anfangszustand entfernt hat. Damit wird schleichende Normalisierung sichtbar: Viele kleine Veraenderungen fuehren irgendwann zu einem neuen Zustand, der stabil wirkt, obwohl er weit vom Ursprung entfernt ist.

## Interpretation

Die erfolgreiche Strategie war schnell, energiesparend, wenig sozial und relativ kompetitiv. Daraus folgt: In dieser konkreten Umwelt wurden keine kooperativen Schwarmmuster selektiert, sondern effiziente Konkurrenz um knappe Ressourcen.

## Was kann man daraus lernen?

Die Simulation zeigt, dass Umweltbedingungen stark bestimmen, welche Verhaltensformen entstehen. Wenn Ressourcen knapp sind und Konkurrenzdruck hoch ist, kann Selektion zu aggressiveren und sparsameren Strategien fuehren. Andere Konfigurationen koennten dagegen Kooperation oder Clusterbildung beguenstigen.

## Gute Saetze fuer die Vorstellung

- "Die Fitness ist nicht explizit programmiert, sondern entsteht indirekt durch Ueberleben und Reproduktion."
- "Emergenz bedeutet hier, dass Populationsmuster aus lokalen Agentenentscheidungen entstehen."
- "Der wichtigste beobachtete Effekt ist eine Linien-Dominanz: Aus vielen Anfangslinien bleibt eine erfolgreiche Abstammung uebrig."
- "Der Baseline Distance Index macht messbar, wie stark sich das System vom Anfangszustand entfernt hat."
- "Die Simulation macht Evolution sichtbar, hoerbar und textuell auswertbar."
- "Die Ergebnisse sind nicht als endgueltige biologische Aussage zu verstehen, sondern als computergestuetztes Modell zur Untersuchung von Selektionsdruck."
- "Der naechste wissenschaftliche Schritt waeren Mehrfachlaeufe mit verschiedenen Seeds und statistischer Auswertung."

## Wenn gefragt wird: Was ist die Haupterkenntnis?

In der getesteten Umwelt beguenstigt die Simulation keine soziale Kooperation, sondern eine schnelle, energieeffiziente und kompetitive Strategie. Das zeigt, dass einfache lokale Regeln zusammen mit Ressourcenknappheit ausreichen koennen, um klare evolutionaere Dominanzmuster zu erzeugen.
