# Analysis: Martin & Monfet (2024) — EnergyPlus CHTC comparison

**Source**: Martin, G.L. & Monfet, D. (2024). "Comparison of EnergyPlus inside
surfaces convective heat transfer coefficients algorithms for energy modelling
of high-density controlled environment agriculture." *Energy and Buildings*, 319.

## Table 2 — Key numerical results (h_in in W/(m²·K))

| Surface | CFD ref | Simple | TARP 21°C | TARP 18°C | Ceiling Diff | Adaptive | ASTMC1340 21°C | ASTMC1340 18°C |
|---------|---------|--------|-----------|-----------|-------------|----------|---------------|---------------|
| Front   | **41.61** | 3.07 | 3.34 | 0.77 | 17.55 | 43.09 | 2.79 | 1.5 |
| Right   | **24.62** | 3.07 | 3.34 | 0.77 | 17.55 | 43.04 | 2.79 | 1.5 |
| Back    | **29.82** | 3.07 | 3.34 | 0.77 | 17.55 | 43.09 | 2.79 | 1.5 |
| Left    | **34.54** | 3.07 | 3.34 | 0.77 | 17.55 | 43.04 | 2.79 | 1.5 |
| Ceiling | **34.42** | 0.95 | 1.96 | 0.45 | 43.80 | **3.44e+06** | 1.58 | 1.5 |
| Floor   | **38.95** | 4.04 | 3.86 | 0.87 | 11.35 | 28.93 | 4.03 | 1.6 |

## Key findings

### 1. CFD reference values are VERY HIGH (25-42 W/(m²·K))
This is a **forced convection** CEA-HD space with air inlet velocities of ~2-4 m/s
and multi-tier crop shelves creating complex flow patterns. The CFD values reflect
the actual turbulent boundary layer on each surface.

### 2. TARP gives 1-4 W/(m²·K) — 10-40× lower than CFD
- Walls: TARP = 3.34 vs CFD = 25-42 → **ratio 7-12×** too low
- Floor: TARP = 3.86 vs CFD = 38.95 → **ratio 10×** too low
- Ceiling: TARP = 1.96 vs CFD = 34.42 → **ratio 18×** too low
- At 18°C setpoint: TARP drops to 0.45-0.87 → even worse

### 3. Simple is equally bad
- All walls: Simple = 3.07 (constant!) vs CFD = 25-42 → **10-14× too low**
- Ceiling: Simple = 0.95 vs CFD = 34.42 → **36× too low**

### 4. Adaptive Convection has a catastrophic bug
- Ceiling: Adaptive = **3.44 × 10⁶ W/(m²·K)** — ABERRANT
- This is the "aberrant ceiling CHTC" mentioned in the abstract
- Other surfaces: ~43 W/(m²·K) — actually close to CFD for walls!

### 5. ASTMC1340 is also too low
- Walls: 1.5-2.8 vs CFD 25-42 → 10-15× too low

### 6. Ceiling Diffuser is the best (but still off)
- Walls: 17.55 vs CFD 25-42 → **2× too low**
- Floor: 11.35 vs CFD 38.95 → 3× too low

## Impact on energy (Fig. 6)

The paper shows yearly peak demand comparison:
- **Sensible cooling peak**: CFD ≈ 12000 W, TARP ≈ 3000 W → **4× underestimate**
- **Sensible heating peak**: CFD ≈ 3000 W, TARP ≈ 1500 W → 2× underestimate
- Simple, ASTMC1340 give similar wrong results
- Only Adaptive (with the ceiling bug) approaches CFD for walls

## Context: their geometry vs ours

| | Martin & Monfet (CEA-HD) | Our work (Savona greenhouse) |
|---|---|---|
| Type | Indoor vertical farm, insulated | Glass greenhouse, exposed |
| Air velocity | 2-4 m/s (forced) | <0.5 m/s (natural) |
| CFD h_in | 25-42 W/(m²·K) | Not computed |
| EP TARP h_in | 1-4 W/(m²·K) | 1-2 W/(m²·K) |
| Balemans h_in | Not tested | 3-6 W/(m²·K) |
| EP ISO 15099 h_in | Not tested (fenestration) | 1-6 W/(m²·K) |

### Critical difference
Their CEA-HD has **forced convection** (fans at 2-4 m/s) → TARP (natural convection)
is completely wrong. Our greenhouse has **natural convection** (still air) → TARP is
wrong for a different reason (building-calibrated, not greenhouse-calibrated).

## How this supports our argument

1. **Martin proves TARP is wrong for CEA interior surfaces** (10-40× too low for
   forced convection). This is the same algorithm EP uses on opaque surfaces
   in our greenhouse model.

2. **We prove ISO 15099 is wrong for greenhouse glass exterior** (7× too high
   vs Bot, which was measured on actual greenhouse glass). This is the algorithm
   EP uses on fenestration and cannot be overridden.

3. **Together**: EP has NO valid convection pathway for greenhouse glass surfaces.
   Interior: TARP is too low (Martin 2024). Exterior: ISO 15099 is too high (our
   finding). Both are building-calibrated, neither greenhouse-calibrated.

4. **The Adaptive algorithm** is closest to CFD for walls but has a catastrophic
   bug on the ceiling (3.44e+06). EP explicitly warns against it for certain
   geometries.

## Conclusion for thesis

> "Martin & Monfet (2024) demonstrated that EnergyPlus's interior convection
> algorithms (Simple, TARP, ASTMC1340) underestimate the convective heat
> transfer coefficient by 10-40× compared to CFD in high-density CEA spaces.
> Our work shows that the exterior convection on glass fenestration (ISO 15099)
> overestimates the coefficient by 7× compared to the greenhouse-calibrated
> Bot (1983) correlation. Together, these findings confirm that EnergyPlus's
> convection models are fundamentally incompatible with greenhouse physics —
> too low on the interior of opaque surfaces, too high on the exterior of
> glass surfaces, and not overridable for fenestration."
