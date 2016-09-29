================
RFI mitigation
================

SEEK's RFI mitigation follows the `Offringa et al. <http://arxiv.org/pdf/1002.1957v1.pdf>`_ `SumThreshold` algorithm. 
It's implemented in pure Python and JIT-compiled for speed with the `HOPE <https://github.com/cosmo-ethz/hope>`_ package.

It can easily be used without of the SEEK data processing pipeline::


	import numpy as np
	from seek.mitigation import sum_threshold
	
	rfi_mask = sum_threshold.get_rfi_mask(tod=np.ma.array(data), 
					chi_1=20, 
					sm_kwargs=sum_threshold.get_sm_kwargs(40, 20, 15, 7.5),
					di_kwargs=sum_threshold.get_di_kwrags(3, 7))
										  
The TOD has to be a Numpy masked array when passed to the `sum_threshold` algorithm. The other parameters are optional an give you the possiblity to tune the mitigation.
Crucial is the a good starting value of `chi_1`, best explored by trial and error. The keyword-arguments control the smoothing and dilation process. Further options can be found in the documentation of the module.

The resulting boolean mask looks something like that::

.. image:: https://raw.githubusercontent.com/cosmo-ethz/seek/master/docs/masked_realdata.jpg
   :alt: SumThresholds RFI mitigation.
   :align: center
