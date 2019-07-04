import sys
import time
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


# Read the list of triggers from a text file
data = pd.read_csv('triggers.txt', delim_whitespace=True)

# sort time increasing, then DM descending, then width descending
data.sort_values(by=['time', 'DM', 'integration_step'], ascending=[True, False, False], inplace=True)

# Add a column with the pulse width -in seconds-.
data['w'] = data.integration_step * 8.192e-05

# Add a relative time column to nicer plot x-axis labels
data['t'] = data.time - data.time.values[0]


# Show what the data looks like
print('Read {} triggers from file.'.format(data.shape[0]))
print(data.head())

# -------------------------------------------------------
# Compute triggers
start = time.time()
# -------------------------------------------------------


# Configure the cleaner generator
gen = RadioPulseFilterGen(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8, time_tol=tol)


# Link the generator to source of events that need to be processed
clean_it = gen((e.t, e.w, e.DM, e.SNR) for e in data.itertuples())

# read out the the filtered triggers from the generator
clean_triggers = [e for e in clean_it]


# -------------------------------------------------------
end = time.time()
print('triggers in:                  {:8.0f}'.format(gen.num_in))
print('triggers out:                 {:8.0f}'.format(gen.num_out))
print('Trigger reduction:            {:2.4f}'.format(1.0 - (gen.num_out+1.0)/(gen.num_in+1.0)))
print('Trigger reduction factor:     {:2.2f}'.format( (gen.num_in + 1.0) / (gen.num_out + 1.0)))
print('clusting time elapsed:       ', end - start)
print('triggers / sec:               {:8.0f}'.format(gen.num_in / (end - start)))
# -------------------------------------------------------


# -------------------------------------------------------
# Plots
# -------------------------------------------------------
fontsize = 16

_, ax = plt.subplots(figsize=(6, 4))
ax.scatter(data.t, data.DM,  s=10, lw=0, c='k', alpha=0.1)
ax.set_xlabel('time (s)', fontsize=fontsize)
ax.set_ylabel('DM', fontsize=fontsize)
ax.set_yscale('log')
ax.set_ylim(0.05, 450)
plt.title('{:,} source triggers'.format(data.shape[0]))
plt.savefig('output/filter_all.png', dpi=300)


# split the list of tuples into separate lists
clean_t, clean_w, clean_dm, clean_snr = zip(*clean_triggers)

_, ax = plt.subplots(figsize=(6, 4))
ax.scatter(clean_t, clean_dm,  s=10, lw=0, c='k', alpha=1.0)
ax.set_xlabel('time (s)', fontsize=fontsize)
ax.set_ylabel('DM', fontsize=fontsize)
ax.set_yscale('log')
ax.set_ylim(0.05, 450)
plt.title('{:,} triggers after filtering'.format(len(clean_t)))
plt.savefig('output/filter_clean.png', dpi=300)
