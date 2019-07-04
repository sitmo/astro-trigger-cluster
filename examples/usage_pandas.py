import pandas as pd
import random

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from astrotf.radio_pulse import RadioPulseFilterGen

N = 1000 # Number of random triggers
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8

# Generate a Pandas Data Frame with random trigger data
# ..or read triggers from a file:
# triggers = pd.read_csv('triggers.txt', delim_whitespace=True)

triggers = pd.DataFrame(
	[
		[
			random.uniform(0.0, 1.0),
			random.uniform(0.0, 0.01),
			random.uniform(0.0, 100.0),
			random.uniform(5.0, 10.0)
		]
		for _ in range(N)
	],
	columns=['t', 'w', 'DM', 'SNR']
)

# sort time increasing, then DM descending, then width descending
triggers.sort_values(by=['t', 'DM', 'w'], ascending=[True, False, False], inplace=True)

# Itialize the filter generator
gen = RadioPulseFilterGen(freq_lo_mhz, freq_hi_mhz)

for filtered_trigger in gen((e.t, e.w, e.DM, e.SNR) for e in triggers.itertuples()):
    print(filtered_trigger)

print('Filtered {} triggers out of a set of {}'.format(gen.num_out, gen.num_in))