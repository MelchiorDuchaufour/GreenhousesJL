# Case C: Savona 5×5 m, PI-heated to 18 °C (Genoa Dec)

## Scenario
- Julia scenario: `savona_walls` from `scripts/benchmark.jl`
- EP IDF: `/home/duchaufm/doctorat/fresh/Greenhouses-Library-master/energyplus/results_savona`
- Period: 7-day TMY starting 2024-12-10
- Julia data: `scripts/results_julia.csv` (169 hourly rows)
- EP data: ESO converted to hourly (168 hours)

## Metrics (Julia vs EnergyPlus, T_air)
| Metric | Value |
|---|---|
| RMSE | 0.05 °C |
| Bias | +0.00 °C |
| R² | 0.781 |
| Julia T_air range | [5.0, 18.6] °C |
| EP T_air range | [17.6, 18.5] °C |

## Plot
![Case C: Savona 5×5 m, PI-heated to 18 °C (Genoa Dec)](assets/benchmark/case_c_savona.png)

## How to regenerate
```bash
# 1. Run Julia benchmark (if results_julia.csv is stale)
cd /home/duchaufm/doctorat/fresh/GreenhousesJL && julia scripts/benchmark.jl

# 2. Regenerate plots
python3 /tmp/generate_comparison_plots.py
```
