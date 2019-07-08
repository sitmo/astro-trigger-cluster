import pandas as pd
import random

import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from astrotf.radio_pulse import RadioPulseFilterGen, dm_one_delay

N = 1000  # Number of random triggers
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8

# Generate a Pandas Data Frame with random trigger data
# ..or read triggers from a file:
# data = pd.read_csv('triggers.txt', delim_whitespace=True)

data = pd.DataFrame(
    [
        [
            random.uniform(0.0, 1.0),
            random.uniform(0.0, 0.01),
            random.uniform(0.0, 100.0),
            random.uniform(5.0, 10.0),
            i
        ]
        for i in range(N)
    ],
    columns=['t', 'w', 'DM', 'SNR', 'ndx']
)

# Add a column with the pulse timing information.
dm1 = dm_one_delay(freq_lo_mhz, freq_hi_mhz)
data['b0'] = data.t + data.DM * dm1  # The timestamp of the start of the pulse at the bottom frequency
data['b1'] = data.b0 + data.w  # The timestamp of the end of the pulse at the bottom frequency
data.sort_values(by=['t', 'b1'], ascending=[True, False], inplace=True)  # sort triggers

# Itialize the filter generator
gen = RadioPulseFilterGen(freq_lo_mhz, freq_hi_mhz)

# Process triggers and print result
for filtered_trigger in gen((e.t, e.w, e.DM, e.SNR, e.ndx) for e in data.itertuples()):
    print(filtered_trigger)

print('Filtered {} triggers out of a set of {}'.format(gen.num_out, gen.num_in))
