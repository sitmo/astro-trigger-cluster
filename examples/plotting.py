import sys, random
import matplotlib.pyplot as plt
import shapely.geometry as sg
import descartes
from graphviz import Graph

# Import TriggerFilter class
sys.path.append("..") # Adds higher directory to python modules path.
from astrotf.radio_pulse import radio_pulse_polygon


# ----------------------------------------------------------------------------------------------------
# General settings
# ----------------------------------------------------------------------------------------------------

# General telescope specific settings and constants
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8
sample_rate = 8.192e-05
tol = 0.0001

# A list of triggers: t0, width, DM
triggers = [
    (0.02, 0.015, 370),
    (0.07, 0.015, 20),
    (0.12, 0.015, 320),
    (0.17, 0.015, 60),
    (0.22, 0.015, 60),
    (0.25, 0.015, 200)
]

# Make sure the list is sorted on arrival time
triggers.sort(key=lambda tup: tup[0])

# ----------------------------------------------------------------------------------------------------
# Plot curves and their intersections
# ----------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)

# Plot the templates
for num, trigger in enumerate(triggers, start=1):
    p = sg.Polygon(radio_pulse_polygon(*trigger))
    ax.add_patch(descartes.PolygonPatch(p, fc='w', ec='k'))
    ax.annotate(str(num), xy=(trigger[0] + trigger[1]/2, freq_hi_mhz + 10), fontsize=16, ha="center")

# Plot the overlapping regions
for i in range(len(triggers)):
    p_i = sg.Polygon(radio_pulse_polygon(*triggers[i]))
    for j in range(i+1, len(triggers)):
        p_j = sg.Polygon(radio_pulse_polygon(*triggers[j]))
        if p_i.intersects(p_j):
            p_ij = p_i.intersection(p_j)
            ax.add_patch(descartes.PolygonPatch(p_ij, fc='k', ec='k'))

# Styling the plot
ax.autoscale_view()
plt.xlabel('Time (s)')
plt.ylabel('frequency (MHz)')
plt.tight_layout()
plt.savefig('output/trigger_templates.png', dpi=300)


# ----------------------------------------------------------------------------------------------------
# Plot the intersection graph
# ----------------------------------------------------------------------------------------------------
dot = Graph('G', format='png', filename='output/intersection_graph.gv', engine='dot')

#  Plot the nodes
for i in range(len(triggers)):
    dot.node('t{}'.format(i+1), str(i+1))

#  Plot the edges
gen = RadioPulseIntersectionGen(freq_lo_mhz, freq_hi_mhz)
for i,j in gen(triggers):
    dot.edge('t{}'.format(i + 1), 't{}'.format(j + 1))

dot.render('output/intersection_graph', view=False)
with open('output/intersection_graph.dot', 'w') as f:
    f.write(dot.source)