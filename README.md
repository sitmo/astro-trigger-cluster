# astro-trigger-filter
A Python package for filtering radio astronomical pulse matched template searches.


## Installation

```
pip install astro-trigger-filter
```

## Usage

First generate a set of random triggers, sorten on time:

```python
import random

N = 1000

# Generate random trigger data
start_times = [random.uniform(0.0, 1.0) for _ in range(N)]
widths = [random.uniform(0.00, 0.01) for _ in range(N)]
DMs = [random.uniform(0.0, 100.0) for _ in range(N)]
SNRs = [random.uniform(5.0, 10.0) for _ in range(N)]

# Reformat data into a list of tuples
triggers = [t for t in zip(start_times, widths,DMs, SNRs)]

# Make sure the list is sorted on start time
# aditional reverse sorting on DM improves the effiency
triggers.sort(key=lambda tup: (tup[0], -tup[2]))
```

Now filter the triggers:

```python
from astrotf.radio_pulse import RadioPulseFilterGen

freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8

# Itialize the filter generator
gen = RadioPulseFilterGen(freq_lo_mhz, freq_hi_mhz)

# Apply the filter to the list of triggers and print results
for filtered_trigger in gen(triggers):
    print(filtered_trigger)

print('Filtered {} triggers out of a set of {}'.format(gen.num_out, gen.num_in))
```

## Usage with Pandas

```python
import pandas as pd
import random
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

# Initialize the filter generator
gen = RadioPulseFilterGen(freq_lo_mhz, freq_hi_mhz)

# Print just the filtered triggers
for filtered_trigger in gen((e.t, e.w, e.DM, e.SNR) for e in triggers.itertuples()):
    print(filtered_trigger)

print('Filtered {} triggers out of a set of {}'.format(gen.num_out, gen.num_in))
```