# Report: EnergyPlus limitations for greenhouse modelling

**Context**: Cross-validation of GreenhousesJL (Julia) against EnergyPlus 25.1
on the Savona 5×5m bare greenhouse across 4 climates and 6 months.

---

## 1. The Ouazzani Chahidi / Fossa case (SamLab Albenga)

Ouazzani Chahidi et al. (2021) modelled the **SamLab greenhouse in Albenga** —
the same facility and geographic area as our Savona validation case — using
EnergyPlus. Key observations:

- They report **"fair agreement"** between EP and measured data for GCHP
  consumption and borehole heat transfer, but do not publish RMSE for
  air temperature.
- The paper does not specify whether they used `Material` (opaque) or
  `WindowMaterial:Glazing` for the glass cover — a critical choice that
  we showed changes the interior convection model from TARP to ISO 15099.
- Ground coupling details are not published — it is unclear whether they
  used `Site:GroundTemperature:BuildingSurface` (constant or Kusuda) or
  Foundation:Kiva.

**Incoherences we can identify from our benchmark**:

1. If they used `Material` for glass (as many greenhouse EP studies do),
   their model received **zero solar gain** through the cover — the same bug
   we found and fixed. Their "fair agreement" for heating energy may reflect
   error cancellation: no solar gain but also no proper sky radiation exchange.

2. If they used `WindowMaterial:Glazing`, their exterior h on glass was
   ISO 15099 (~50 W/(m²K)) — 7× higher than the Bot (1983) value of
   ~7 W/(m²K) that is standard in greenhouse science. This would cause
   the cover to overcool, increasing heating demand.

3. The "fair agreement" descriptor without published RMSE makes it difficult
   to assess the actual quality of the EP model for the SamLab greenhouse.

**Our contribution**: we show that for the same geographic area (Savona/Albenga),
the choice of EP glass material type and the uncontrollable fenestration exterior
convection create a **+0.5°C winter to +4.3°C summer bias** vs the greenhouse-
specific physics (Bot + Balemans). The Ouazzani study likely encountered similar
issues but may have absorbed them into calibration parameters.

---

## 2. Martin & Monfet (2024): convection algorithms are "ill-suited"

Martin & Monfet (2024) systematically compared EP's interior convection algorithms
against CFD for high-density controlled environment agriculture (CEA-HD):

**What they tested:**
- Simple, TARP, ASTMC1340, and Adaptive convection algorithms
- Reference: CFD-computed convective heat transfer coefficients (CHTC)

**What they found:**
- Simple, TARP, and ASTMC1340 are **"ill-suited to model CEA-HD production
  spaces"** compared to CFD reference values.
- The Adaptive algorithm produced **"aberrant values for ceiling CHTC"**
  due to modelled flow rate issues.
- They recommend **"caution when using BPS tools for energy modelling of
  CEA-HD spaces"** and validation against actual conditions.

**What they did NOT test:**
- **Fenestration surfaces** — they only tested opaque surfaces. The ISO 15099
  exterior convection on glass (our main finding) was not in scope.
- **Greenhouse-specific exterior convection** (Bot 1983) — not mentioned.

**Our contribution complements theirs**: Martin & Monfet showed interior h is
wrong; we show exterior h on glass is also wrong AND cannot be overridden.
Together, both interior and exterior convection on the dominant surface
(glass cover) use building-calibrated models that are inappropriate for
greenhouses.

---

## 3. Our results in context

### What we showed

| Finding | Impact | Status |
|---------|--------|--------|
| EP `Material` = zero solar through glass | Dominant error (+2.8°C RMSE) | Fixed (WindowMaterial:Glazing) |
| EP ground temp constant 3°C | +1.3°C bias | Fixed (Kusuda / Kiva) |
| Julia missing angular τ correction | +0.2-1.0°C in sunny climates | Fixed (Fresnel n=1.526) |
| Julia VF formula bug (A/B swap) | Row sums > 1 in radiosity | Fixed, validated analytically |
| EP interior h overridable (ISO 15099 → Balemans) | h_in matched via EMS ✓ | Confirmed working |
| **EP exterior h NOT overridable on glass** | **h=7 (Bot) vs h=50 (ISO 15099)** | **Irreducible** |
| EP exterior h drives seasonal bias | +0.5°C winter, +4.3°C summer | **Accepted** |

### The argument

**EnergyPlus is not designed for greenhouses because:**

1. **Glass must be modelled as fenestration** (WindowMaterial:Glazing) for solar
   transmission, but this forces ISO 15099 exterior convection (~50 W/(m²K))
   instead of greenhouse-calibrated Bot (~7 W/(m²K)). There is no way to use
   transparent glass with greenhouse convection in EP.

2. **Interior convection CAN be overridden** via EMS (we validated this), but
   **exterior convection on fenestration CANNOT**. EP's window heat balance
   solver ignores the EMS actuator for the exterior face.

3. **This is not a calibration issue** — it is an architectural limitation.
   The window module in EP was designed for building windows in urban
   environments (ISO 15099) and there is no mechanism to substitute
   greenhouse-specific physics.

4. **Martin & Monfet (2024) confirmed** that EP's interior convection algorithms
   are also "ill-suited" for CEA/greenhouse spaces, even on opaque surfaces.

5. **The Ouazzani/Fossa study** on the SamLab (our geographic reference) reports
   only "fair agreement" without publishing temperature RMSE, suggesting
   awareness of systematic discrepancies.

### What greenhouse-specific models provide

| Model | Exterior h | Interior h | Solar | Status |
|-------|-----------|-----------|-------|--------|
| **GreenhousesJL** | Bot (1983) | Balemans (1989) | Fresnel + PAR/NIR | This work |
| **GreenLight** | Bot | Balemans | De Jong angular | Katzin 2020 |
| **KASPRO** | Bot | Balemans | Fresnel + multi-layer | de Zwart 1996 |
| **Vanthoor** | Bot | Balemans | Constant τ per band | Vanthoor 2011 |
| **EnergyPlus** | ISO 15099 (glass) | ISO 15099 (glass) | Fresnel polynomial | Not greenhouse-calibrated |

All greenhouse-specific models use Bot + Balemans. EP uses building-calibrated
ISO 15099. This is the fundamental reason for the cross-validation gap.

---

## References

- Ouazzani Chahidi, L., Fossa, M., Priarone, A., & Mechaqrane, A. (2021).
  Greenhouse cultivation in Mediterranean climate: Dynamic energy analysis and
  experimental validation. *Thermal Science and Engineering Progress*, 26.

- Martin, G.L. & Monfet, D. (2024). Comparison of EnergyPlus inside surfaces
  convective heat transfer coefficients algorithms for energy modelling of
  high-density controlled environment agriculture. *Energy and Buildings*, 319.

- Martin, G.L. & Monfet, D. (2025). Toward integrated crop and building
  simulation for controlled environment agriculture using EnergyPlus.
  *ScienceDirect*.

- Katzin, D., van Henten, E.J., & van Mourik, S. (2022). Process-based
  greenhouse climate models: Genealogy, current status, and future directions.
  *Agricultural Systems*, 198.

- Choudhary, R. et al. (2021). Co-simulating a greenhouse in a building to
  quantify co-benefits of different coupled configurations. *Journal of Building
  Performance Simulation*, 14(3).

- Bot, G.P.A. (1983). *Greenhouse climate: from physical processes to a
  dynamic model*. PhD thesis, Wageningen University.

- Balemans, L. (1989). *Assessment of criteria for energetic effectiveness
  of greenhouse screens*. PhD thesis, Agricultural University, Ghent.

- Vanthoor, B.H.E. et al. (2011). A methodology for model-based greenhouse
  design. *Biosystems Engineering*, 110(4), 363-377.

- Katzin, D. et al. (2020). GreenLight — An open source model for greenhouses
  with supplemental lighting. *Biosystems Engineering*, 194, 61-81.

- de Zwart, H.F. (1996). *Analysing energy-saving options in greenhouse
  cultivation using a simulation model*. PhD thesis, Wageningen University.
