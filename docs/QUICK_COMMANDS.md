# Schnellbefehle

## Demo mit Plot

```powershell
python main.py --config configs/quick_demo.yaml --plot
```

## Live-Analyse

```powershell
python main.py --config configs/long_live_analysis.yaml --live
```

## Langer Headless-Lauf

```powershell
python main.py --config configs/long_evolution.yaml --plot
```

## Ergebnisordner oeffnen

```powershell
explorer data\runs\long_live_analysis
```

## Tests

```powershell
python -m pytest
```
