import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


_, ax = plt.subplots(figsize=(6, 4))
plt.axis('off')
plt.xlim(0,150)
plt.ylim(0,100)

N = 4
dy = 16
x = 10
dx = 26

mx = 58
for i in range(N):
    y = 100*(2*i+1) / (2*N)
    ax.add_patch(Rectangle((x, y - dy/2), dx, dy, fill=None, alpha=1))
    ax.annotate("filter", xy=(x+5,y), fontsize=18, ha="left", va='center')
    ax.arrow(0, y, x - 3, 0, head_width=3, head_length=3, fc='k', ec='k', length_includes_head=True)
    ax.arrow(x + dx + 3, y, 20*0.8, (50-y)*0.8, head_width=3, head_length=3, fc='k', ec='k', length_includes_head=True)

ax.add_patch(Rectangle((mx, 50 - dy/2), 35, dy, fill=None, alpha=1))
ax.annotate("merge", xy=(mx + 5, 50), fontsize=18, ha="left", va='center')

fx = 106
ax.add_patch(Rectangle((fx, 50 - dy/2), dx, dy, fill=None, alpha=1))
ax.annotate("filter", xy=(fx + 5, 50), fontsize=18, ha="left", va='center')
ax.arrow(fx-x, 50, x - 3, 0, head_width=3, head_length=3, fc='k', ec='k', length_includes_head=True)
plt.tight_layout()

ax.arrow(fx+ dx + 4, 50, x - 3, 0, head_width=3, head_length=3, fc='k', ec='k', length_includes_head=True)

plt.savefig('output/filter_parallel_diagram.png', dpi=300)

