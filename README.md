# Evolving Digital Ecologies

## Research-Grade Artificial-Life-Simulation fuer Evolution, Emergenz und komplexe Systeme

> Note: Fuer die Entwicklung, Strukturierung, Dokumentation und Erklaermaterialien wurden ChatGPT und NotebookLM als unterstuetzende Werkzeuge verwendet. Die Simulation, Konfigurationen, Auswertungen und Projektdateien liegen in diesem Repository nachvollziehbar vor.

Dieses Projekt ist eine Python-basierte Forschungsplattform fuer Artificial Life und Evolutionary Computation. Es simuliert eine Population autonomer digitaler Organismen in einer dynamischen 2D-Umwelt. Agenten bewegen sich lokal, suchen Ressourcen, verbrauchen Energie, altern, sterben, reproduzieren sich und vererben mutierbare Eigenschaften an ihre Nachkommen.

Die zentrale Forschungsfrage lautet:

> Wie koennen komplexe, emergente und kollektive Verhaltensmuster aus einfachen lokalen Regeln, Vererbung, Mutation, Selektionsdruck und Umweltbeschraenkungen entstehen?

Das System ist nicht als Spiel gedacht, sondern als wissenschaftlich auswertbare Simulationsumgebung fuer eine Masterarbeits-Implementierung in Artificial Life, Emergence, Complex Systems und Computational Intelligence.

## Kurzueberblick

- Kontinuierliche 2D-Welt mit Ressourcen, Umweltzonen, Gefahren und Klima-Schwankungen
- Evolvierende Agenten mit Energie, Alter, Gesundheit, Abstammung und vererbbaren Traits
- Reproduktion mit Mutation, Trait-Grenzen und optionalen grossen Mutationsereignissen
- Heuristisches Verhalten und optionaler neuroevolutionaerer Controller
- Metriken fuer Population, Ressourcen, Energie, Trait-Diversitaet, Linien-Dominanz und Clusterbildung
- Live-Visualisierung mit Pygame inklusive Dashboard und Verlaufskurven
- Sonifikation: Evolution wird im Live-Modus sichtbar und hoerbar gemacht
- Accessibility-Konzept fuer visuelle, akustische und textuelle Auswertung
- Baseline Distance Index fuer schleichende Drift vom Anfangszustand
- Automatische CSV/JSON-Exporte und wissenschaftliche Plots nach dem Lauf
- Parameter-Sweeps fuer Experimente
- Pytest-Testabdeckung fuer zentrale Simulationsinvarianten

## Demo Video

Ein kurzer Demonstrationslauf der Live-Simulation ist als MP4 enthalten:

[Demo-Video ansehen](media/demo.mp4)

## Projektstruktur

```text
alife_thesis_sim/
|-- src/
|   |-- core/              # Konfiguration, Geometrie, deterministische Zufallsquellen
|   |-- agents/            # Agenten, Traits, Genome
|   |-- world/             # Ressourcen, Zonen, Gefahren, Umweltmodell
|   |-- behavior/          # Heuristik- und Neural-Controller
|   |-- evolution/         # Mutation, Reproduktion, Lineage-Tracking
|   |-- neuroevolution/    # Kleine vererbbare neuronale Netze
|   |-- simulation/        # Simulationsengine
|   |-- analytics/         # Metriken und Exporte
|   |-- visualization/     # Live-Ansicht und Plot-Erzeugung
|   |-- experiments/       # Experiment-Runner und Parameter-Sweeps
|   `-- utils/             # Logging
|-- configs/               # YAML-Konfigurationen
|-- data/
|   |-- logs/
|   |-- runs/
|   |-- exports/
|   `-- plots/
|-- tests/                 # Pytest-Tests
|-- docs/                  # Wissenschaftliche Dokumentation und Vorstellungsnotizen
|-- media/                 # Demo-Video der Live-Simulation
|-- notebooks/             # Optional fuer spaetere Analyse
|-- main.py                # Haupteinstieg
|-- requirements.txt
|-- pyproject.toml
`-- README.md
```

## Installation

Empfohlen wird Python 3.11 oder 3.12. Python 3.14 kann bei `pygame` Probleme machen.

Im Projektordner:

```powershell
pip install -r requirements.txt
```

Falls `pygame` nicht installierbar ist, funktionieren Headless-Laeufe und Plot-Auswertungen auch ohne Live-Fenster, wenn mindestens diese Pakete installiert sind:

```powershell
pip install numpy pandas matplotlib PyYAML pytest
```

## Start in PyCharm

1. PyCharm oeffnen.
2. `File` -> `Open` -> Ordner auswaehlen:

```text
alife_thesis_sim
```

3. Run Configuration anlegen:

```text
Script path:
main.py

Working directory:
alife_thesis_sim

Parameters:
--config configs/quick_demo.yaml --plot
```

4. Mit dem gruenen Play-Button starten.

## Wichtige Terminalbefehle

Kurzer Testlauf mit Plot-Auswertung:

```powershell
python main.py --config configs/quick_demo.yaml --plot
```

Live-Lauf mit spaeterer automatischer Auswertung:

```powershell
python main.py --config configs/long_live_analysis.yaml --live
```

Im Live-Modus sind Abstammungslinien farblich markiert. Die dominante Linie wird hell umrandet. Wenn Audio aktiviert ist, wird Evolution zusaetzlich hoerbar:

- mittlere Generation beeinflusst die Tonhoehe
- dominante Linie beeinflusst Lautstaerke und Klangklarheit
- Trait-Diversitaet erzeugt ein komplexeres Klangbild
- wenn eine Linie dominiert, wird der Klang stabiler
- Baseline Distance verschiebt den Klang, wenn der Anfangszustand verloren geht

Accessibility-Gedanke:
Das Projekt ist bewusst multimodal angelegt. Taube Menschen koennen Linien, Dominanz und Trends ueber Farben, Umrandungen, Dashboard und Plots verfolgen. Blinde Menschen koennen Dominanz, Diversitaet und Generationen ueber die Sonifikation wahrnehmen und nach dem Lauf die Datei `accessible_summary.txt` mit einem Screenreader lesen.

Falls `pygame` fehlt:

```powershell
python -m pip install pygame
```

Langer Headless-Lauf:

```powershell
python main.py --config configs/long_evolution.yaml --plot
```

Experiment mit Mutationsraten:

```powershell
python main.py --experiment configs/experiment_mutation_sweep.yaml
```

Tests:

```powershell
python -m pytest
```

## Output-Dateien

Jeder Lauf schreibt Ergebnisse nach:

```text
data/runs/<run_name>/
```

Wichtige Dateien:

- `metrics.csv`: Zeitreihe aller wissenschaftlichen Metriken
- `final_population.csv`: finale Agentenpopulation mit Traits, Positionen und Linien
- `summary.json`: kompakte Zusammenfassung des Laufs
- `accessible_summary.txt`: einfache Textzusammenfassung fuer Screenreader und schnelle Interpretation
- `config_snapshot.yaml`: exakte Konfiguration des Laufs
- `plots/`: automatisch erzeugte Diagramme

Wichtige Plots:

- `population_resources.png`: Populations- und Ressourcenverlauf
- `energy_diversity.png`: Energie und Trait-Diversitaet
- `trait_evolution.png`: Entwicklung zentraler Eigenschaften
- `spatial_lineage.png`: Clusterbildung und Anzahl lebender Linien
- `population_energy_phase.png`: Beziehung zwischen Populationsgroesse und Energie
- `baseline_distance.png`: Drift vom urspruenglichen Zustand, getrennt nach Trait, Sound und Visual
- `final_spatial_traits.png`: finale raeumliche Verteilung der Agenten
- `final_trait_histograms.png`: finale Trait-Verteilungen

## Modellbeschreibung

Die Simulation verwendet diskrete Zeitschritte in einer kontinuierlichen 2D-Welt. Pro Schritt:

1. Die Umwelt aktualisiert Ressourcen und Klimafaktor.
2. Jeder Agent nimmt lokale Signale wahr: Ressourcen, Nachbarn, Gefahren, interne Energie.
3. Ein Controller waehlt Aktion: Bewegung, Reproduktion, Angriff, Signal.
4. Die Engine aktualisiert Bewegung, Energieverbrauch, Ressourcenkonsum, Interaktionen und Tod.
5. Erfolgreiche Agenten reproduzieren sich und vererben mutierte Traits.
6. Metriken werden gespeichert.

Selektion entsteht indirekt: Es gibt keine globale Fitnessfunktion. Agenten, die unter den gegebenen Umweltbedingungen besser ueberleben und reproduzieren, dominieren spaetere Generationen.

## Heritable Traits

Agenten besitzen unter anderem:

- Geschwindigkeit
- Wahrnehmungsreichweite
- Drehneigung
- Metabolismus
- Reproduktionsschwelle
- Reproduktionskosten
- Aggression
- Sozialtendenz
- Explorationstendenz
- Risikosensitivitaet
- Kommunikationstendenz

Alle Traits sind begrenzt, damit die Simulation numerisch stabil bleibt.

## Forschungsfragen

Das Framework erlaubt unter anderem folgende Untersuchungen:

1. Unter welchen Umweltbedingungen entsteht stabiles Populationswachstum?
2. Welche Selektionsdruecke beguenstigen Konkurrenz, Kooperation oder Clusterbildung?
3. Wie beeinflusst Mutation die Anpassung, Diversitaet und Kollapswahrscheinlichkeit?
4. Fuehren lokale Regeln zu hoehergeordneten raeumlichen Mustern?
5. Kann Neuroevolution adaptiver sein als ein transparenter Heuristik-Controller?
6. Wann entfernt sich ein System so weit von seiner Ausgangsbasis, dass der neue Zustand als normal erscheint?

## Baseline Distance Index

Der Baseline Distance Index misst, wie weit sich die aktuelle Population vom Anfangszustand entfernt hat. Dieser Index operationalisiert den Gedanken schleichender Normalisierung: Kleine Veraenderungen wirken einzeln harmlos, koennen aber ueber viele Schritte eine neue Normalitaet erzeugen.

Der Index besteht aus drei Teilen:

- `trait_baseline_distance`: Abstand der aktuellen Trait-Mittelwerte vom Anfangszustand
- `sound_baseline_distance`: akustische Drift ueber Generation, Diversitaet und Dominanz
- `visual_baseline_distance`: visuelle Drift ueber raeumliche Verteilung, Spread und Linienverlust

Der Gesamtwert `baseline_distance` ist der Mittelwert dieser drei Perspektiven. Damit wird messbar, ob sich das System graduell so stark veraendert, dass Anfangsbild und Grundton nicht mehr intuitiv praesent sind.

## Wissenschaftliche Leitidee der finalen Version

Die finale Version verbindet drei Ebenen:

1. Evolution im Modell: Agenten veraendern sich durch Mutation, Vererbung und Selektion.
2. Wahrnehmung der Veraenderung: Bild und Ton zeigen, wie sich Dominanz, Diversitaet und Generationen veraendern.
3. Schleichende Normalisierung: Der Baseline Distance Index misst, wie weit sich das System vom Anfang entfernt hat.

Damit untersucht das Projekt nicht nur, ob sich Populationen evolutionaer veraendern, sondern auch, wie graduelle Veraenderungen als neuer Normalzustand wahrgenommen werden koennen.

## Beispielbefund aus `long_live_analysis`

Ein ausgewerteter Langzeitlauf zeigte:

- 15.000 Simulationsschritte
- finale Population: 187 Agenten
- maximale Population: 366 Agenten
- 9.834 Geburten und 9.727 Tode
- am Ende nur noch eine lebende Abstammungslinie
- sinkende Ressourcen und sinkende mittlere Energie
- Selektion hin zu schneller, sparsamer und eher kompetitiver Strategie

Interpretation: In dieser Konfiguration wurde keine kooperative Schwarmstruktur selektiert, sondern eine ressourceneffiziente Konkurrenzstrategie. Das ist ein verwertbares Ergebnis: Die Umweltbedingungen beguenstigen in diesem Modell eher kompetitive Ausbeutung knapper Ressourcen als soziale Aggregation.

Zusatzinterpretation mit Baseline Distance:
Wenn die Baseline Distance im Verlauf steigt, entfernt sich die Population sichtbar, hoerbar und trait-basiert vom Anfangszustand. Das macht den Prozess der schleichenden Verschiebung messbar: Der neue Zustand wirkt irgendwann stabil, obwohl er deutlich vom Ursprung abweicht.

Der Bericht liegt unter:

```text
data/runs/long_live_analysis/analysis_report.md
```

## Tests und Qualitaetssicherung

Die Tests pruefen:

- Reproduktion und Abstammung
- Mutation innerhalb erlaubter Grenzen
- Ressourcenverbrauch
- Welt-Update und Resource-Spawning
- deterministische Seeds
- eindeutige Agenten-IDs
- Metrikberechnung
- Experiment-Runner

Aktueller Stand der Verifikation:

```text
8 passed
```

## Grenzen des Modells

Das Modell programmiert keine Zivilisation, Sprache oder Kooperation hart ein. Genau das ist Absicht: Emergenz soll aus lokalen Regeln entstehen. Der aktuelle Nachbarschaftsscan ist einfach und lesbar, aber fuer sehr grosse Populationen waere eine raeumliche Beschleunigungsstruktur sinnvoll.

## Moegliche Erweiterungen

- Predator-Prey-Koevolution
- echte Kommunikationssysteme
- Paarungswahl und sexuelle Selektion
- Territorialitaet
- Speicher und Lernen innerhalb der Lebenszeit
- Multi-Species-Oekosysteme
- systematische Kollapsanalyse
- statistische Mehrfachlaeufe mit Signifikanztests
