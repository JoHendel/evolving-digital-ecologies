# Abgabe-Checkliste

## Projektstatus

- Vollstaendige Python-Projektstruktur vorhanden
- PyCharm-Einstieg ueber `main.py`
- YAML-Konfigurationen fuer Demo, Langzeitlauf, Live-Analyse und Experimente
- Live-Visualisierung mit Dashboard
- Sonifikation fuer hoerbare Evolution
- Baseline Distance Index fuer Drift vom Anfangszustand
- Accessibility-Konzept fuer visuelle, akustische und textuelle Erklaerung
- Automatischer Export nach Live- und Headless-Laeufen
- Wissenschaftliche Plots vorhanden
- Tests vorhanden und ausgefuehrt
- README fuer Installation, Start und wissenschaftliche Einordnung angepasst
- Beispielanalyse fuer `long_live_analysis` vorhanden

## Wichtige Startpunkte

```text
main.py
configs/quick_demo.yaml
configs/long_live_analysis.yaml
configs/long_evolution.yaml
configs/experiment_mutation_sweep.yaml
```

## Wichtige Ergebnisdateien

```text
data/runs/long_live_analysis/metrics.csv
data/runs/long_live_analysis/final_population.csv
data/runs/long_live_analysis/summary.json
data/runs/long_live_analysis/analysis_report.md
data/runs/long_live_analysis/accessible_summary.txt
data/runs/long_live_analysis/plots/
```

## Vor der Abgabe pruefen

1. Projekt in PyCharm oeffnen.
2. Interpreter auswaehlen.
3. `quick_demo` starten.
4. `plots/` im Ausgabeordner oeffnen.
5. README und `docs/PRESENTATION_SUMMARY.md` lesen.
