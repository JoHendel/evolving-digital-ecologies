# Architektur und Module fuer NotebookLM

## Gesamtarchitektur

Das Projekt ist modular aufgebaut. Jede Komponente hat eine klare Aufgabe. Dadurch ist die Simulation erweiterbar und nachvollziehbar.

## Zentrale Module

### `src/core`

Dieses Modul enthaelt Grundfunktionen:

- Konfigurationen aus YAML-Dateien
- Vektor-Geometrie fuer Positionen und Bewegungen
- deterministische Zufallsquellen fuer reproduzierbare Experimente

### `src/world`

Dieses Modul beschreibt die Umwelt:

- Groesse der 2D-Welt
- Ressourcen
- Umweltzonen
- Gefahrenbereiche
- Ressourcen-Spawning
- Klima- oder Umweltveraenderungen ueber die Zeit

### `src/agents`

Dieses Modul beschreibt die digitalen Organismen:

- eindeutige ID
- Position
- Energie
- Alter
- Gesundheit
- Abstammungslinie
- Genome und vererbbare Traits

### `src/behavior`

Dieses Modul entscheidet, was Agenten tun:

- Ressourcen suchen
- ausweichen
- explorieren
- reproduzieren
- optional angreifen

Es gibt einen heuristischen Controller und einen optionalen Neural-Controller.

### `src/evolution`

Dieses Modul enthaelt den evolutionaeren Kern:

- Mutation
- Reproduktion
- Vererbung
- Linienverfolgung
- Populationsinitialisierung

### `src/simulation`

Dieses Modul verbindet alles:

- Welt aktualisieren
- Agenten wahrnehmen lassen
- Aktionen ausfuehren
- Energie und Tod berechnen
- Reproduktion ausloesen
- Metriken sammeln

### `src/analytics`

Dieses Modul erzeugt wissenschaftlich auswertbare Daten:

- `metrics.csv`
- `final_population.csv`
- `summary.json`
- Metriken zu Population, Ressourcen, Energie, Diversitaet und Linien

### `src/visualization`

Dieses Modul erzeugt:

- Live-Bild mit Pygame
- Dashboard im Live-Fenster
- Plots nach dem Lauf

### `src/experiments`

Dieses Modul erlaubt Parameter-Sweeps, zum Beispiel:

- verschiedene Mutationsraten
- verschiedene Ressourcenmengen
- Hazard-Vergleiche
- Heuristik vs. Neuroevolution

## Warum diese Architektur sinnvoll ist

Die klare Trennung macht das Projekt wissenschaftlich nutzbar. Man kann eine Komponente veraendern, ohne alles neu zu schreiben. Zum Beispiel kann man spaeter Predator-Prey-Systeme, Kommunikation oder neue Metriken ergaenzen.

