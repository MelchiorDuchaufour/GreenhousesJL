#!/usr/bin/env python3
"""Generate PV cross-section: two-panel figure (overview + zoomed detail)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8),
                                gridspec_kw={"width_ratios": [1, 1.3]})

# ── Colours ──────────────────────────────────────────
C_GLASS  = "#2196F3"
C_FLUSH  = "#0D47A1"
C_TILT   = "#BF360C"
C_GROUND = "#D7CCC8"
C_INT    = "#FFF8E1"
C_SKY    = "#E3F2FD"
C_ANN    = "#FF6F00"   # annotation orange
C_GAP    = "#7B1FA2"   # gap cavity purple

# ═══════════════════════════════════════════════════════
# LEFT PANEL — greenhouse cross-section
# ═══════════════════════════════════════════════════════
ax1.set_xlim(-2.5, 6.5)
ax1.set_ylim(-0.5, 6.5)
ax1.set_aspect("equal")
ax1.set_xlabel("south  →  north  (m)", fontsize=11)
ax1.set_ylabel("height (m)", fontsize=11)
ax1.set_title("Savona 5×5 m cross-section", fontsize=13, fontweight="bold")

# Ground
ax1.fill_between([-2.5, 6.5], -0.5, 0, color=C_GROUND, alpha=0.6)
ax1.axhline(0, color="#8D6E63", lw=1.5)

# Interior fill
gh_x = [0, 0, 2.5, 5, 5, 0]
gh_y = [0, 2, 4.165, 2, 0, 0]
ax1.fill(gh_x, gh_y, color=C_INT, alpha=0.4)

# Glass envelope
ax1.plot([0, 0], [0, 2], color=C_GLASS, lw=2)          # south wall
ax1.plot([5, 5], [0, 2], color=C_GLASS, lw=2)          # north wall
ax1.plot([0, 2.5], [2, 4.165], color=C_GLASS, lw=2.5)  # south roof
ax1.plot([2.5, 5], [4.165, 2], color=C_GLASS, lw=2.5)  # north roof

# Floor
ax1.plot([0, 5], [0, 0], color="#5D4037", lw=3)

# Labels
ax1.text(2.5, 1.0, "interior ($T_{air}$)", ha="center", fontsize=11,
         color="#795548", style="italic")
ax1.text(0, -0.15, "south\ngutter", ha="center", va="top", fontsize=8, color="#555")
ax1.text(5, -0.15, "north\ngutter", ha="center", va="top", fontsize=8, color="#555")
ax1.text(2.5, 4.35, "ridge", ha="center", va="bottom", fontsize=9, color="#555")

# ── PV panels (flush) ──
# Position flush panel on south roof lower half
p1_s = np.array([0.6, 2 + 0.6*2.165/2.5])
p1_e = np.array([1.4, 2 + 1.4*2.165/2.5])
ax1.plot([p1_s[0], p1_e[0]], [p1_s[1], p1_e[1]],
         color=C_FLUSH, lw=8, solid_capstyle="round")

# ── PV panel (tilted) ──
# Position tilted panel on south roof upper half
p2_s = np.array([1.7, 2 + 1.7*2.165/2.5])
# Tilt: add 15° to the 37° roof slope → 52° from horizontal
tilt_total = np.radians(52)
panel_len = 0.8
p2_e = p2_s + panel_len * np.array([np.cos(tilt_total), np.sin(tilt_total)])
ax1.plot([p2_s[0], p2_e[0]], [p2_s[1], p2_e[1]],
         color=C_TILT, lw=8, solid_capstyle="round")

# ── Dashed zoom box around PV region ──
zx0, zy0 = 0.3, 2.15
zx1, zy1 = 2.5, 4.5
rect = mpatches.FancyBboxPatch((zx0, zy0), zx1-zx0, zy1-zy0,
                                boxstyle="round,pad=0.1",
                                fill=False, edgecolor="#888", lw=1.5,
                                linestyle="--")
ax1.add_patch(rect)
ax1.text(zx1+0.15, (zy0+zy1)/2, "detail →", fontsize=10, color="#888",
         va="center", ha="left", style="italic")

# Roof angle arc
arc_center = (0, 2)
arc = Arc(arc_center, 2.0, 2.0, angle=0, theta1=0, theta2=40.8,
          color=C_GLASS, lw=1.5, linestyle="--")
ax1.add_patch(arc)
ax1.text(1.3, 2.25, "37°", fontsize=12, color=C_GLASS, fontweight="bold")

# Legend
from matplotlib.lines import Line2D
leg_items = [
    Line2D([0],[0], color=C_GLASS, lw=2.5, label="glass roof (37°)"),
    Line2D([0],[0], color=C_FLUSH, lw=6, label="flush panel (37°)"),
    Line2D([0],[0], color=C_TILT,  lw=6, label="tilted panel (+15° extra)"),
]
ax1.legend(handles=leg_items, loc="upper left", fontsize=9, framealpha=0.9)


# ═══════════════════════════════════════════════════════
# RIGHT PANEL — zoomed PV stack detail (layered schematic)
# ═══════════════════════════════════════════════════════
ax2.set_xlim(-1, 10)
ax2.set_ylim(-2.5, 10.5)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("PV panel thermal stack", fontsize=14, fontweight="bold", pad=12)

# Draw a clean, nearly-horizontal layered schematic
# Layers from bottom to top: interior | glass | gap | PV panel | exterior

layer_len = 7.0  # horizontal extent
y_glass = 0.0
y_gap_bot = 0.8
y_gap_top = 2.8
y_panel = y_gap_top
y_tilt_base = y_gap_top  # tilted panel starts here too

# ── Interior zone (below glass) ──
ax2.fill_between([0, layer_len], -2.0, y_glass, color=C_INT, alpha=0.5)
ax2.text(layer_len/2, -1.0, "interior ($T_{air}$)", fontsize=12,
         ha="center", va="center", color="#795548", style="italic")

# ── Glass cover ──
ax2.fill_between([0, layer_len], y_glass, y_gap_bot,
                 color=C_GLASS, alpha=0.25)
ax2.plot([0, layer_len], [y_glass, y_glass], color=C_GLASS, lw=3)
ax2.plot([0, layer_len], [y_gap_bot, y_gap_bot], color=C_GLASS, lw=3)
ax2.text(-0.3, (y_glass + y_gap_bot)/2, "glass\ncover",
         fontsize=11, ha="right", va="center", color=C_GLASS, fontweight="bold")

# ── Air gap cavity ──
ax2.fill_between([0, layer_len], y_gap_bot, y_gap_top,
                 color=C_GAP, alpha=0.08)
# Gap arrows
for xpos in [1.5, 3.5, 5.5]:
    ax2.annotate("", xy=(xpos, y_gap_top - 0.15), xytext=(xpos, y_gap_bot + 0.15),
                 arrowprops=dict(arrowstyle="<->", color=C_GAP, lw=1.5))
# Gap label — right side, clear space
ax2.text(layer_len + 0.4, (y_gap_bot + y_gap_top)/2,
         "air gap\nHollands (1976)\ncavity convection",
         fontsize=11, color=C_GAP, fontweight="bold",
         ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                   edgecolor=C_GAP, alpha=0.95))

# ── Flush PV panel ──
flush_x0, flush_x1 = 0.3, 3.2
ax2.fill_between([flush_x0, flush_x1], y_panel, y_panel + 0.4,
                 color=C_FLUSH, alpha=0.9)
ax2.text((flush_x0 + flush_x1)/2, y_panel + 0.7,
         "flush PV panel", fontsize=11, color=C_FLUSH,
         ha="center", va="bottom", fontweight="bold")

# ── Tilted PV panel ──
tilt_x0 = 4.0
tilt_extra_deg = 15
tilt_rad = np.radians(tilt_extra_deg)
tilt_len = 2.8
tilt_x1 = tilt_x0 + tilt_len * np.cos(tilt_rad)
tilt_y1 = y_panel + tilt_len * np.sin(tilt_rad)
# Draw panel as thick line
ax2.plot([tilt_x0, tilt_x1], [y_panel, tilt_y1],
         color=C_TILT, lw=10, solid_capstyle="round")

# Ghost horizontal (roof surface reference)
ax2.plot([tilt_x0, tilt_x0 + tilt_len], [y_panel, y_panel],
         color="#bbb", lw=1.5, linestyle="--")

# +15° arc — large and clear
arc_r = 1.8
arc3 = Arc((tilt_x0, y_panel), arc_r*2, arc_r*2,
           angle=0, theta1=0, theta2=tilt_extra_deg,
           color=C_TILT, lw=2.5)
ax2.add_patch(arc3)
# +15° label
alx = tilt_x0 + (arc_r + 0.4) * np.cos(tilt_rad/2)
aly = y_panel + (arc_r + 0.4) * np.sin(tilt_rad/2)
ax2.text(alx, aly, "+15°", fontsize=16, color=C_TILT, fontweight="bold",
         ha="left", va="center")

# Tilted panel label
tmx = (tilt_x0 + tilt_x1)/2 - 0.3
tmy = (y_panel + tilt_y1)/2 + 0.6
ax2.text(tmx, tmy, "tilted PV panel", fontsize=11, color=C_TILT,
         ha="center", va="bottom", fontweight="bold",
         rotation=np.degrees(tilt_rad))

# ── Convection annotation: h_top (exterior, above panels) ──
ax2.text(layer_len/2, y_panel + 3.5,
         "$h_{top}$: wind + natural convection\n"
         "Sharples (1998) + Bot (1983)",
         fontsize=11, color=C_ANN, fontweight="bold",
         ha="center", va="bottom",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                   edgecolor=C_ANN, alpha=0.95))
# Arrows pointing down to panels
for xpos in [1.7, 5.5]:
    ax2.annotate("", xy=(xpos, y_panel + 0.5),
                 xytext=(xpos, y_panel + 3.4),
                 arrowprops=dict(arrowstyle="->", color=C_ANN, lw=1.5))

# Exterior side label
ax2.text(layer_len/2, y_panel + 5.2,
         "exterior side (sky + wind)", fontsize=11, color="#555",
         ha="center", va="bottom", style="italic")

# ── Convection annotation: h_bottom (sheltered, glass-panel gap) ──
ax2.text(-0.5, (y_gap_bot + y_gap_top)/2,
         "$h_{bottom}$ (sheltered)",
         fontsize=10, color="#555", fontweight="bold",
         ha="right", va="center",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                   edgecolor="#999", alpha=0.9))
ax2.annotate("", xy=(0.1, (y_gap_bot + y_gap_top)/2),
             xytext=(-0.4, (y_gap_bot + y_gap_top)/2),
             arrowprops=dict(arrowstyle="->", color="#999", lw=1.2))

# ── Cell temperature: Faiman ──
ax2.text(tilt_x1 + 0.5, tilt_y1 + 0.3,
         "$T_{cell}$: Faiman (2008)",
         fontsize=11, color=C_TILT,
         ha="left", va="bottom",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                   edgecolor=C_TILT, alpha=0.95))
ax2.annotate("", xy=(tilt_x1, tilt_y1),
             xytext=(tilt_x1 + 0.4, tilt_y1 + 0.25),
             arrowprops=dict(arrowstyle="->", color=C_TILT, lw=1.2))

plt.tight_layout(pad=1.5)
plt.savefig("/home/duchaufm/doctorat/fresh/GreenhousesJL/presentation/assets/pv_panels_3d.png",
            dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("OK: pv_panels_3d.png saved")
