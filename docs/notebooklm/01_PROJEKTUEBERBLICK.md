# Projektueberblick fuer NotebookLM

## Titel

Evolving Digital Ecologies: Eine Artificial-Life-Simulation zur Untersuchung von Evolution, Emergenz und Populationsdynamik.

## Kurzbeschreibung

Das Projekt ist eine wissenschaftliche Python-Simulation, in der digitale Organismen in einer dynamischen 2D-Welt leben. Die Agenten suchen Ressourcen, verbrauchen Energie, altern, sterben und reproduzieren sich. Ihre Eigenschaften werden vererbt und durch Mutation leicht veraendert. Dadurch entsteht ueber viele Simulationsschritte ein evolutionaerer Prozess.

## Zentrale Forschungsfrage

Wie koennen komplexe Populationsmuster aus einfachen lokalen Regeln, Ressourcenknappheit, Mutation, Vererbung und Selektionsdruck entstehen?

## Warum ist das Projekt interessant?

Das Projekt zeigt, wie Evolution und Emergenz in einem kontrollierten Computermodell untersucht werden koennen. Es gibt keine zentral gesteuerte Intelligenz und keine direkt programmierte globale Fitnessfunktion. Stattdessen entsteht Erfolg indirekt: Agenten, die laenger ueberleben und sich haeufiger reproduzieren, praegen die spaetere Population.

## Was wird simuliert?

- Eine kontinuierliche 2D-Welt
- Ressourcen, die aufgenommen und neu erzeugt werden
- Fruchtbare, arme und gefaehrliche Umweltzonen
- Agenten mit Energie, Alter, Gesundheit und Position
- Vererbbare Traits wie Geschwindigkeit, Wahrnehmung, Metabolismus, Aggression und Sozialverhalten
- Reproduktion mit Mutation
- Sterben durch Energiemangel, Alter, Schaden oder Umweltgefahren
- Messung von Population, Ressourcen, Energie, Diversitaet und Abstammungslinien

## Ziel der Software

Die Software dient als Forschungsplattform. Sie soll nicht nur eine Animation zeigen, sondern Daten erzeugen, die wissenschaftlich ausgewertet werden koennen. Deshalb werden CSV-Dateien, JSON-Zusammenfassungen und Plots gespeichert.

## Wichtigste Erkenntnis aus dem Beispielrun

Im Lauf `long_live_analysis` setzte sich eine schnelle, energiesparende und eher kompetitive Strategie durch. Am Ende blieb nur eine dominante Abstammungslinie uebrig. Das deutet auf einen evolutionaeren Sweep hin: Eine Linie hatte eine vorteilhafte Kombination von Eigenschaften und verdraengte die anderen.

