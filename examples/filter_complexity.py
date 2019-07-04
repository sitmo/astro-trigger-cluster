import sys
import time
import pandas as pd
import matplotlib.pyplot as plt

# Import TriggerFilter class
sys.path.append("..")  # Adds higher directory to python modules path.
from astrotf.radio_pulse import RadioPulseFilterGen


# General telescope specific settings and constants
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8
sample_rate = 8.192e-05
tol = 0.0001
fontsize = 18

# Read the list of triggers from a text file
data = pd.read_csv('triggers.txt', delim_whitespace=True)
data.sort_values(by=['time', 'DM', 'integration_step'], ascending=[True, False, False], inplace=True)
data['w'] = data.integration_step * 8.192e-05
data['t'] = data.time - data.time.values[0]


# Configure the cleaner generator
chunk_size = 1000
num_chunks = int((data.shape[0] + 1) / chunk_size)

memory_series = []
timing_series = []

for bz in [0,25]:

	gen = RadioPulseFilterGen(
		freq_lo_mhz=1249.8,
		freq_hi_mhz=1549.8,
		time_tol=tol,
		buffersize=bz,
		autoflush=False
	)
	memory = []
	timing = []

	for i in range(num_chunks):

		start = time.time()

		clean_it = gen((e.t, e.w, e.DM, e.SNR) for e in data.iloc[i*chunk_size:(i+1)*chunk_size].itertuples())
		clean_triggers = [e for e in clean_it]

		end = time.time()

		timing.append(end - start)
		memory.append(len(gen.active_set))

	memory_series.append(memory)
	timing_series.append(timing)

x = [i+1 for i in range(num_chunks)]


_, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)
ax.plot(x, memory_series[0], 'k--', label='memory use')
ax.set_ylabel('buffer size', fontsize=fontsize)
ax2 = ax.twinx()
ax2.plot(x, timing_series[0], 'k-', label='cpu time')
ax2.set_ylabel('time / 1k triggers', fontsize=fontsize)
plt.title('Unbound buffer size', fontsize=fontsize)

# ask matplotlib for the plotted objects and their labels
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

ax.set_ylim(0, 800)
ax2.set_ylim(0, 0.25)
plt.tight_layout()
plt.savefig('output/complexity_unbound.png', dpi=300)



_, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)
ax.plot(x, memory_series[1], 'k--', label='memory use')
ax.set_ylabel('buffer size', fontsize=fontsize)
ax2 = ax.twinx()
ax2.plot(x, timing_series[1], 'k-', label='cpu time')
ax2.set_ylabel('time / 1k triggers', fontsize=fontsize)
plt.title('Bound buffer of size 25', fontsize=fontsize)

# ask matplotlib for the plotted objects and their labels
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)
ax.set_ylim(0, 800)
ax2.set_ylim(0, 0.25)
plt.tight_layout()
plt.savefig('output/complexity_bound_25.png', dpi=300)



buffer_sizes = [1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000]
trigger_count = []
timing = []

for bz in buffer_sizes:
	print(bz)
	gen = RadioPulseFilterGen(
		freq_lo_mhz=1249.8,
		freq_hi_mhz=1549.8,
		time_tol=tol,
		buffersize=bz,
		autoflush=True
	)


	start = time.time()

	clean_it = gen((e.t, e.w, e.DM, e.SNR) for e in data.itertuples())
	clean_triggers = [e for e in clean_it]

	end = time.time()

	timing.append(end - start)
	trigger_count.append(gen.num_out)



trigger_count_1 = [float(c)/trigger_count[-1] for c in trigger_count]
_, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)
ax.semilogx(buffer_sizes, trigger_count_1, 'k-', label='trigger count')
ax.set_xlabel('buffer size', fontsize=fontsize)
ax.set_ylabel('rel. num of triggers', fontsize=fontsize)
plt.title('Number of triggers vs. buffer size', fontsize=fontsize)
plt.tight_layout()
plt.grid(which='major', color='k', alpha=.5)
plt.grid(which='minor', color='k', alpha=.125)
plt.savefig('output/complexity_triggers.png', dpi=300)

timing_1 =[ timing[-1]/float(c) for c in timing]
_, ax = plt.subplots(1, 1, figsize=(6,4), sharex=True, sharey=True)
ax.semilogx(buffer_sizes, timing_1, 'k-', label='run time')
ax.set_xlabel('buffer size', fontsize=fontsize)
ax.set_ylabel('rel. speed-up', fontsize=fontsize)
plt.title('Runtime vs. buffer size', fontsize=fontsize)
plt.tight_layout()
plt.grid(which='major', color='k', alpha=.5)
plt.grid(which='minor', color='k', alpha=.125)
plt.savefig('output/complexity_runtime.png', dpi=300)
