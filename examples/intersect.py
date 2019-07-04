import sys
import time
import pandas as pd
import matplotlib.pyplot as plt

# Import TriggerFilter class
sys.path.append("..") # Adds higher directory to python modules path.
from astrotf.radio_pulse import RadioPulseIntersectionGen


# General telescope specific settings and constants
freq_lo_mhz = 1249.8
freq_hi_mhz = 1549.8
sample_rate = 8.192e-05
tol = 0.0


# Read the list of triggers from a text file
data = pd.read_csv('triggers.txt', delim_whitespace=True)
data.sort_values('time', inplace=True)
data = data.iloc[:10000]

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
gen = RadioPulseIntersectionGen(freq_lo_mhz=1249.8, freq_hi_mhz=1549.8, time_tol=tol)


# Link the generator to source of events that need to be processed
intersections_it = gen((e.t, e.w, e.DM) for e in data.itertuples())

# read out the the filtered triggers from the generator
intersections = [e for e in intersections_it]


# -------------------------------------------------------
end = time.time()
print('triggers in:                  {:8.0f}'.format(gen.num_in))
print('intersection out:             {:8.0f}'.format(gen.num_out))
print('avg number of intersection:   {:8.0f}'.format(gen.num_out / gen.num_in))
print('computingtime elapsed:        ', end - start)
print('triggers / sec:               {:8.0f}'.format(gen.num_in / (end - start)))
# -------------------------------------------------------
