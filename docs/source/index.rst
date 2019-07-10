Astronomical Trigger Filtering
===================================

This package provides algorithms for reducing the number of superfluous triggers that occur in matched template searches pipelines use in astronomy.

Installation
-------------

.. code-block:: python

   pip install astro-trigger-filter


Command line tool
--------------------

The `ambertf` command line tool process *Amber* formatter trigger files.
To combine and filter all trigger files matching `CB??.trigger` run::

   shell> ambertf -i CM??.trigger -o output.txt -v


.. figure:: _static/radio_pulse_template.png
    :align: center

.. figure:: _static/overlap_region.png
    :align: center

Requirements
------------

* Python 2.7, 3.5, 3.6 or 3.7

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ambertf
   examples
   modules
   license




