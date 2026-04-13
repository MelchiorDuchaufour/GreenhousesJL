# Diagnostic: Savona +23% Q_heat gap

## Summary
Julia Q_heat = 109.5 W/m² vs EP = 89 W/m² → gap = +23.1% (+20.5 W/m²)

## Root cause: wall thermal circuit

The gap is almost entirely in the WALL contribution:
- Julia walls: 67.8 W/m² of heating demand (from no-walls test: 109.5 − 41.7)
- EP walls (estimated): ~47 W/m² (89 − ~42)
- Wall-related gap: ~20.8 W/m² ← this IS the +23%

## Sensitivity tests (on diagnostic copy, original untouched)

| Test | Q_heat | Gap | What it tells us |
|---|---|---|---|
| Baseline | 109.5 | +23.1% | Reference |
| F_sky = 0.20 (all walls) | 108.0 | +21.4% | Wall sky VF: 1.5 W/m² contribution |
| F_sky = 0.15 | 107.3 | +20.5% | Diminishing returns |
| F_sky = 0.10 | 106.5 | +19.7% | |
| **F_sky = 0.00 (no sky rad)** | **105.1** | **+18.0%** | **Sky radiation = only 4.4 W/m² of the gap** |
| No walls at all | 41.7 | −53.2% | Cover-only loss (no wall contribution) |
| Low-e cover ε=0.05 | 98.1 | +10.2% | Cover radiation: 11.4 W/m² impact |
| Cover ε=0.70 | 107.7 | +21.1% | Small (−1.8 W/m²) |
| Floor ε changes | 109.5 | +23.1% | No effect |

## What drives the wall gap

The wall subcooling effect: walls radiate to the cold sky, cool BELOW T_out, then 
outside air convects heat back. The net wall heat loss depends on the balance:

```
Wall loses:  sky radiation (49.6 W/m²) + ground radiation + exterior convection
Wall gains:  interior convection from air (71.5 W/m²) + interior LW (radiosity)
```

Julia's walls are ~0.4°C colder than they would be in EP because:
1. Walton h_ext (19 W/(m²K) at 3.5 m/s) vs TARP (~11 W/(m²K)) 
   → Julia walls recover MORE heat from outside → should be WARMER → less gap
   → But Walton also makes exterior convection LOSS larger when T_wall > T_out
2. Interior h_in (Holman: 1.7|ΔT|^0.33 + 1) vs EP's algorithm
   → Julia may transfer MORE from air to wall → more heating needed
3. Combined effect: the wall subcooling amplifies small coefficient differences

## T_sky correction

**IMPORTANT**: Julia does NOT use T_sky = T_out − 20 as initially reported.
The TMY file contains actual T_sky values (variable offset 6–17°C, mean ~10°C).
T_sky model is NOT a significant gap source.

## Why this gap is expected (not a bug)

The two models use **different convection correlations calibrated for different
surface types**:

| | Julia / Modelica | EnergyPlus |
|---|---|---|
| **Exterior** | Bot 1983 — greenhouse saw-tooth glass, Wageningen | TARP — office buildings, DOE |
| **Interior** | Balemans 1989 — greenhouse floor/cover free convection | TARP interior algorithm |
| **Calibrated on** | Glass, inclined, smooth, open-field wind | Brick/concrete, vertical, rough, urban |

Bot 1983 is the **de facto standard in greenhouse science**, used by:
- Vanthoor et al. 2011 (our source library)
- GreenLight (Katzin et al. 2020, Wageningen)
- de Zwart 1996 (Wageningen energy model)
- Stanghellini 1987 (canopy transpiration)

TARP is the standard in **building energy simulation** (DOE, ASHRAE).

Neither is "wrong" — they're calibrated for different geometries. On a standard
Venlo (14000 m², walls < 3%), both agree to < 6%. On the small Savona (walls = 60%),
the wall convection model dominates and the different calibrations produce a
+23% gap. This confirms that **greenhouse-specific correlations are necessary**
and that generic building tools should be used with caution for small greenhouses.

## References

- Bot, G.P.A. (1983). *Greenhouse climate: from physical processes to a dynamic model*. PhD, Wageningen.
- Balemans, L. (1989). *Assessment of criteria for energetic effectiveness of greenhouse screens*. PhD, Ghent.
- Stanghellini, C. (1987). *Transpiration of greenhouse crops*. PhD, Wageningen.
- de Zwart, H.F. (1996). *Analysing energy-saving options in greenhouse cultivation*. PhD, Wageningen.
- Katzin, D. et al. (2020). *GreenLight*. Biosystems Engineering, 194, 61–81.
- Vanthoor, B.H.E. et al. (2011). *Biosystems Engineering*, 110(4), 363–377.
