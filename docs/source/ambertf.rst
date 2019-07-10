ambertf
===============

Command line tool for filtering Amber trigger files.

Usage::

    usage: ambertf [-h] [-i [INPUT]] [-o [OUTPUT]] [-p [PLOT]] [-fh [FREQ_HI_MHZ]]
                   [-fl [FREQ_LO_MHZ]] [-dt [SAMPLE_TIME]] [-v]

    Process Amber trigger files.

    optional arguments:
      -h, --help            show this help message and exit
      -i [INPUT], --input [INPUT]
                            input filename(s). Wildcards are allowed.
      -o [OUTPUT], --output [OUTPUT]
                            output filename. Writes to stdout when omitted.
      -p [PLOT], --plot [PLOT]
                            Optional plot filename.
      -fh [FREQ_HI_MHZ], --freq_hi_mhz [FREQ_HI_MHZ]
                            Highest observation frequency (MHz)
      -fl [FREQ_LO_MHZ], --freq_lo_mhz [FREQ_LO_MHZ]
                            Lowest observation frequency (MHz)
      -dt [SAMPLE_TIME], --sample_time [SAMPLE_TIME]
                            Sampling time (seconds)
      -v, --verbose         modify output verbosity
