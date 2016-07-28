=============================
SEEK: Signal Extraction and Emission Kartographer
=============================

.. image:: https://travis-ci.org/cosmo-ethz/seek.png?branch=master
        :target: https://travis-ci.org/cosmo-ethz/seek
        
.. image:: https://coveralls.io/repos/cosmo-ethz/seek/badge.svg
  		:target: https://coveralls.io/r/cosmo-ethz/seek

.. image:: https://readthedocs.org/projects/seek/badge/?version=latest
		:target: http://seek.readthedocs.io/en/latest/?badge=latest
		:alt: Documentation Status
		
.. image:: http://img.shields.io/badge/arXiv-1607.07443-orange.svg?style=flat
        :target: http://arxiv.org/abs/1607.07443

**SEEK** is a flexible and easy-to-extend data processing pipeline for single dish radio telescopes. It takes the observed (or simulated) TOD in the time-frequency domain as an input and processes it into *healpix*maps while applying calibration and automatically masking RFI. The data processing is parallelized using *ivy's* parallelization scheme.

.. image:: https://raw.githubusercontent.com/cosmo-ethz/seek/master/docs/forecast_map.png
   :alt: Forecasted healpix map with **SEEK**.
   :align: center

The **SEEK** package has been developed at ETH Zurich in the `Software Lab of the Cosmology Research Group <http://www.cosmology.ethz.ch/research/software-lab.html>`_ of the `ETH Institute of Astronomy <http://www.astro.ethz.ch>`_. 

The development is coordinated on `GitHub <http://github.com/cosmo-ethz/seek>`_ and contributions are welcome. The documentation of **SEEK** is available at `readthedocs.org <http://seek.readthedocs.io/>`_ .
