import pandas as pd
import random

import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from astrotf.radio import FilterEngine

N = 1000  # Number of random triggers

# Generate a Pandas Data Frame with random trigger data
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
    columns=['t', 'w', 'DM', 'SNR', 'counter']
)

# Initialize a filter egine
eng = FilterEngine(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8)

# Sort triggers
eng.sort(data, ['t', 'w', 'DM', 'b1'])

# Process triggers and print result
for filtered_trigger in eng.filter((e.t, e.w, e.DM, e.SNR, e.counter) for e in data.itertuples()):
    print(filtered_trigger)

print('Filtered {} triggers out of a set of {}'.format(eng.num_out, eng.num_in))
