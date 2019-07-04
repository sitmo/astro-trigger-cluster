import sys
import pandas as pd
import matplotlib.pyplot as plt


# Import TriggerFilter class
sys.path.append("..") # Adds higher directory to python modules path.
from astrotf.radio_pulse import RadioPulseFilterGen


# General telescope specific settings and constants
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8
sample_rate = 8.192e-05
tol = 0.0001
fontsize = 18



data = pd.read_csv('triggers.txt', delim_whitespace=True)
data.sort_values(by=['time', 'DM', 'integration_step'], ascending=[True, False, False], inplace=True)
data['w'] = data.integration_step * 8.192e-05
data['t'] = data.time - data.time.values[0]

num_splits = [r for r in range(1, 33)]
num_triggers = []
num_triggers2 = []

print("splits,intermediate_triggers,final_triggers")
for split_count in num_splits:

	clean_triggers = []
	for subset_ndx in range(split_count):

		data_sub = data.iloc[subset_ndx::split_count]

		cleaner = RadioPulseFilterGen(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8, time_tol=tol)
		clean_gen = cleaner((e.t, e.w, e.DM, e.SNR) for e in data_sub.itertuples())
		clean_triggers.extend([e for e in clean_gen])

	# clean the merged set
	clean_triggers.sort(key=lambda tup: tup[0])
	cleaner = RadioPulseFilterGen(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8, time_tol=tol)
	clean_triggers2 = [ e for e in cleaner(clean_triggers)]

	# collect statistics
	trigger_count = len(clean_triggers)
	trigger_count2 = len(clean_triggers2)
	num_triggers.append(trigger_count)
	num_triggers2.append(trigger_count2)
	print('{},{},{}'.format(split_count, trigger_count, trigger_count2))


#
num_triggers_1 = [float(c)/num_triggers2[0] for c in num_triggers]
num_triggers2_1 = [float(c)/num_triggers2[0] for c in num_triggers2]

_, ax = plt.subplots(figsize=(6, 4))
ax.loglog(num_splits, num_triggers_1, 'k--*', label='intermediate')
ax.loglog(num_splits, num_triggers2_1, 'k-*', label='final')
ax.set_xlabel('number of parallel streams', fontsize=fontsize)
ax.set_ylabel('rel. num of triggers', fontsize=fontsize)
plt.title('Distributed hierarchical filtering')
plt.legend()
plt.grid(which='major', color='k', alpha=.5)
plt.grid(which='minor', color='k', alpha=.125)
plt.savefig('output/filter_parallel.png', dpi=300)






# Diagram

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