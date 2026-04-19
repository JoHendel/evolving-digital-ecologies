# Simulationsablauf fuer NotebookLM

## Ablauf eines Simulationsschritts

Die Simulation laeuft in diskreten Zeitschritten. In jedem Schritt werden Welt, Agenten und Metriken aktualisiert.

## Schritt 1: Welt aktualisieren

Die Welt erzeugt neue Ressourcen. Die Menge haengt von der Konfiguration, den Umweltzonen und einem Klimafaktor ab. Dadurch entsteht eine dynamische Umwelt, in der Ressourcen knapp oder reichlich sein koennen.

## Schritt 2: Agenten nehmen ihre Umgebung wahr

Jeder Agent erhaelt lokale Informationen:

- Wo ist die naechste Ressource?
- Wie viele andere Agenten sind in der Naehe?
- Wie hoch ist die eigene Energie?
- Befindet sich der Agent in einer Gefahrzone?
- Wie alt ist der Agent?

Die Agenten haben keine globale Sicht auf die Welt. Sie handeln lokal.

## Schritt 3: Verhalten auswaehlen

Der Controller entscheidet eine Aktion:

- Richtung aendern
- bewegen
- reproduzieren
- optional angreifen
- Signal aussenden

Im Basismodell ist das Verhalten heuristisch. Optional kann ein kleines neuronales Netz als Controller verwendet werden, dessen Gewichte evolutionaer vererbt und mutiert werden.

## Schritt 4: Bewegung und Energie

Agenten bewegen sich entsprechend ihrer Geschwindigkeit und Aktion. Bewegung, Wahrnehmung und Metabolismus kosten Energie. Gefahrenzonen koennen zusaetzlich Schaden verursachen.

## Schritt 5: Ressourcenaufnahme

Wenn ein Agent eine Ressource erreicht, nimmt er deren Energie auf. Die Ressource verschwindet danach aus der Welt.

## Schritt 6: Reproduktion

Wenn ein Agent genug Energie besitzt, kann er ein Kind erzeugen. Das Kind erbt die Traits des Elternteils, aber mit Mutation. So entsteht Variation.

## Schritt 7: Tod

Agenten sterben, wenn:

- ihre Energie aufgebraucht ist
- sie zu alt werden
- ihre Gesundheit zu stark sinkt

## Schritt 8: Metriken speichern

In regelmaessigen Abstaenden werden Metriken gespeichert:

- Populationsgroesse
- Ressourcenanzahl
- Geburten und Tode
- mittlere Energie
- Trait-Diversitaet
- Clusterindex
- Anzahl lebender Abstammungslinien

Diese Daten ermoeglichen spaeter eine wissenschaftliche Auswertung.

