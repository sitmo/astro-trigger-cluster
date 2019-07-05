# astro-trigger-filter
A Python package for filtering radio astronomical pulse matched template searches.


## Installation

```
pip install astro-trigger-filter
```

## Basic Usage

Generate a set of random triggers:

```python
import random

N = 1000

start_times = [random.uniform(0.0, 1.0) for _ in range(N)]
widths = [random.uniform(0.00, 0.01) for _ in range(N)]
DMs = [random.uniform(0.0, 100.0) for _ in range(N)]
SNRs = [random.uniform(5.0, 10.0) for _ in range(N)]

triggers = [t for t in zip(start_times, widths,DMs, SNRs)]
```

Make sure the list is sorted on start time. Aditional reverse sorting on DM will improve the effiency.

```
triggers.sort(key=lambda tup: (tup[0], -tup[2]))
```

Now filter the triggers:

```python
from astrotf.radio_pulse import RadioPulseFilterGen

gen = RadioPulseFilterGen(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8)

for filtered_trigger in gen(triggers):
    print(filtered_trigger)
```

Print statistics:

```
print('Reduced the number of triggers from  {} to {}'.format(
	gen.num_in, 
	gen.num_out
))
```

# Processing Pandas Dataframes

Generate a pandas dataframe with random triggers:

```python
import pandas as pd
import random

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
```

..or read a csv file from disk:


```python
triggers = pd.read_csv('triggers.txt', delim_whitespace=True)
```

Sort time increasing, then DM descending, then pulse-width descending:


```python
triggers.sort_values(
	by=['t', 'DM', 'w'], 
	ascending=[True, False, False], 
	inplace=True
)
```

Filter and print the triggers:

```python
gen = RadioPulseFilterGen(freq_lo_mhz, freq_hi_mhz)

for filtered_trigger in gen(
		(e.t, e.w, e.DM, e.SNR) 
		for e in triggers.itertuples()
	):
    print(filtered_trigger)
```

# Storing extra data along each trigger

You can add extra data for each trigger, as long as the first 4 elements remain *[`time, width, dispersion measure, signal-to-noise ratio`]*. In the example below we have added a `beam_id` and `sample_id`. These extra columns will show up again in the filtered output.

```python
for filtered_trigger in gen(
        (
            e.time, 
            e.w, 
            e.DM, 
            e.SNR, 
            e.beam_id, 
            e.sample_id
        ) 
        for e in triggers.itertuples()
    ):
    print(filtered_trigger)
```

# More settings

`buffersize=0`
: Limit the buffer size. The default setting is 0 which means an unlimited buffer size. A buffer size of 25 speeds up filtering while only generating marginally more false triggers.


`autoflush=True`
: Automatically flush the internal buffer when finished processing the input trigger. Set this to `false` if you want to process triggers in chunks and not flush the buffers between each chunk.


