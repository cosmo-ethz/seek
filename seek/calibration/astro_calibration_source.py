# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 20, 2015

author: cchang

Models taken from: Baars 1997, Hafez 2008, Benz 2009
All numbers divided by 2 to account for the fact that our data is
single polarization.

'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

h = 6.626e-34
k = 1.38e-23
c = 3.0e8
SFU = 1e-22 # W/m^2/Hz = 1.0e26 Jy

def black_body(freq, T):
	"""
	Black body model spectra

	:param freq: frequency in Hz
	:param T: temperature of black body

	:return: model spectra
	"""
	return 2*h*freq**3/c**2*(1./(np.exp(h*freq/k/T)-1.))

def barrs77_power_law(freq, a, b, c):
	"""
	Power law model from Baars 1997.

	:param freq: frequency in Hz
	:param a: model parameter
	:param b: model parameter
	:param c: model parameter

	:return: model spectra
	"""
	return 10**(a + b*np.log10(freq/1.0e6) + c*np.log10(freq/1.0e6)**2)

def benz_sun(freq):
	"""
	Model of Solar spectra based on Benz 2009.

	:param freq: frequency in Hz

	:return: model spectra
	"""

	Sq = 0.845*(freq/1e6)**0.5617 # quiet sun
	Sv = 1.2*1e-5*(freq/1e6)**1.374 # active sun
	Z = 56   # check up sun spot number
	return (Sq + Sv*Z)*SFU/1.0e-26

def source(obj, freq):
	"""
	Given name of calibration source and frequency grid, give model spectrum.
	"""
	
	if obj=="Sun":
		return benz_sun(freq)/2 # Jansky

	elif obj=="CasA": 
		F = (0.68 - 0.15*np.log10(freq/1.0e9)*(2015-1970))*0.01
		return (1.0+F)*barrs77_power_law(freq, 5.88, -0.792, 0.0)/2

	elif obj=="CygA": 
		return barrs77_power_law(freq, 4.695, 0.085, -0.178)/2

	elif obj=="SagA": # to be updated
		return barrs77_power_law(freq, 5.88, -0.792, 0.0)/2

	elif obj=="TauA": 
		return barrs77_power_law(freq, 3.915, -0.299, 0.0)/2

	elif obj=="VirA": 
		return barrs77_power_law(freq, 5.023, -0.856, 0.0)/2

	else:
		print("Unknown calibration source.")
		return np.zeros(len(freq))
		

