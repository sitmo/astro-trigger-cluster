import sys
import matplotlib.pyplot as plt
import shapely.geometry as sg
import descartes

# Import TriggerFilter class
sys.path.append("..") # Adds higher directory to python modules path.
from astrotf.radio import FilterEngine

# A list of triggers: t0, width, DM
triggers = [
    (0.02, 0.060, 370),
    (0.07, 0.015, 20),
    (0.12, 0.015, 320),
    (0.17, 0.005, 60),
    (0.22, 0.015, 60),
    (0.25, 0.015, 200)
]

eng = FilterEngine(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8)

# ----------------------------------------------------------------------------------------------------
# Plot curves and their intersections
# ----------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)

# Plot the templates
for trigger in triggers:
    p = sg.Polygon(eng.polygon(*trigger))
    ax.add_patch(descartes.PolygonPatch(p, fc='w', ec='k'))

# Plot the overlapping regions
for i in range(len(triggers)):
    p_i = sg.Polygon(eng.polygon(*triggers[i]))
    for j in range(i+1, len(triggers)):
        p_j = sg.Polygon(eng.polygon(*triggers[j]))

        if p_i.intersects(p_j):
            p_ij = p_i.intersection(p_j)
            ax.add_patch(descartes.PolygonPatch(p_ij, fc='r', ec='k'))

# Styling the plot
ax.autoscale_view()
plt.xlabel('Time (s)')
plt.ylabel('frequency (MHz)')
plt.tight_layout()
plt.savefig('output/example_plotting.png', dpi=300)
