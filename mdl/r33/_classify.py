#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
| @purpose: Classification of eyetracking data for mdl.r33.procesing.   
| @date: Created on Sat May 1 15:12:38 2019   
| @author: Semeon Risom   
| @email: semeon.risom@gmail.com   
| @url: https://semeon.io/d/R33-analysis  
"""

# available functions
__all__ = ['Classify']

# required external library
__required__ = ['numpy','pandas','nslr']

from pdb import set_trace as breakpoint
import numpy as np
import pandas as pd

# local libraries
if __name__ == "__main__":
	from .. import settings

class Classify():
	"""Analysis methods for mdl.processing.preprocesing."""
	def __init__(self, isLibrary=False):
		"""
		Initiate the mdl.r33.Classify module.

		Parameters
		----------
		isLibrary : :obj:`bool`
			Check if required libraries are available. Default `False`.
		"""
		#check libraries
		if isLibrary:
			settings.library(__required__)

	def VisualAngle(self ,g_x, g_y, config):
		"""
		Convert pixel eye-coordinates to visual angle.

		Parameters
		----------
		g_x,g_y : :class:`numpy.ndarray`
			List of gaze coordinates.
		drift : :obj:`dict`
			Counter of drift correct runs.
		config : :class:`dict`
			Configuration data for data analysis. i.e. trial number, location.

		Notes
		-----
		* Stimulus positions (g_x,g_y) are defined in x and y pixel units, with the origin (0,0) being at the **center** of 
		  the display, as to match the PsychoPy pix unit coord type.  
		* The pix2deg method is vectorized, meaning that is will perform the pixel to angle calculations on all elements 
		  of the provided pixel position numpy arrays in one numpy call.  
		* The convertion process can use either a fixed eye to calibration plane distance, or a numpy array of eye distances 
		  passed as eye_distance_mm. In this case the eye distance array must be the same length as g_x, g_y arrays.  
		"""

		d_x=config['monitor.cm'][0]
		d_y=config['monitor.cm'][1]
		r_x=config['resolution.px'][0]
		r_y=config['resolution.px'][1]
		dist=config['distance']
		mmpp_x = d_x/r_x
		mmpp_y = d_y/r_y

		x_mm = mmpp_x * g_x
		y_mm = mmpp_y * g_y

		breakpoint() #TODO!

		Ah = np.arctan2(x_mm, np.hypot(dist, y_mm))
		Av = np.arctan2(y_mm, np.hypot(dist, x_mm))

		return np.rad2deg(Ah), np.rad2deg(Av)   

	def Velocity(self, time, config, d_x, d_y=None):
		"""
		Calculate the instantaneous velocity (degrees / second) for data points in d_x and (optionally) d_y, using the 
		time numpy array for time delta information.

		Parameters
		----------
		time : :class:`numpy.ndarray`
			Timestamp of each coordinate.
		d_x,d_y : :class:`numpy.ndarray`
			List of gaze coordinates.
		config : :class:`dict`
			Configuration data for data analysis. i.e. trial number, location.

		Notes
		-----
		Numpy arrays time, d_x, and d_y must all be 1D arrays of the same length. If both d_x and d_y are provided, then
		the euclidian distance between each set of points is calculated and used in the velocity calculation. Time must be
		in seconds.msec units, while d_x and d_y are expected to be in visual degrees. If the position traces
		are in pixel coordinate space, use the VisualAngleCalc class to convert the data into degrees.
		"""
		if d_y is None:
			data=d_x
		else:
			data=np.sqrt(d_x*d_x+d_y*d_y)

		velocity_between = (data[1:]-data[:-1])/(time[1:]-time[:-1])
		velocity = (velocity_between[1:]+velocity_between[:-1])/2.0
		return velocity

	def Acceleration(self, time, data_x, data_y=None):
		"""
		Calculate the acceleration (deg/sec/sec) for data points in d_x and (optionally) d_y, using the time numpy array for
		time delta information.

		Parameters
		----------
		time : :class:`numpy.ndarray`
			Timestamp of each coordinate.
		d_x,d_y : :class:`numpy.ndarray`
			List of gaze coordinates.
		config : :class:`dict`
			Configuration data for data analysis. i.e. trial number, location.

		"""
		velocity=Velocity(time,data_x,data_y)
		accel = Velocity(time[1:-1],velocity)
		return accel

	def savitzky_golay(self, y, window_size, order, deriv=0, rate=1):
		"""
		Smooth (and optionally differentiate) data with a Savitzky-Golay filter.

		The Savitzky-Golay filter removes high frequency noise from data. It has the advantage of preserving the original
		shape and features of the signal better than other types of filtering approaches, such as moving averages techniques.

		Parameters
		----------
		y : :class:`numpy.ndarray`, shape (N,)
			the values of the time history of the signal.
		window_size : :obj:`int`
			the length of the window. Must be an odd integer number.
		order : :obj:`int`
			the order of the polynomial used in the filtering.
			Must be less then `window_size` - 1.
		deriv : :obj:`int`
			the order of the derivative to compute (default = 0 means only smoothing)

		Returns
		-------
		ys : :class:`numpy.ndarray`, shape (N)
			the smoothed signal (or it's n-th derivative).

		Notes
		-----
		The Savitzky-Golay is a type of low-pass filter, particularly suited for smoothing noisy data. The main idea behind this
		approach is to make for each point a least-square fit with a polynomial of high order over a odd-sized window centered at
		the point. For more information, see: http://wiki.scipy.org/Cookbook/SavitzkyGolay.

		Examples
		--------
		>>> t = np.linspace(-4, 4, 500)
		>>> y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
		>>> ysg = savitzky_golay(y, window_size=31, order=4)
		>>> import matplotlib.pyplot as plt
		>>> plt.plot(t, y, label='Noisy signal')
		>>> plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
		>>> plt.plot(t, ysg, 'r', label='Filtered signal')
		>>> plt.legend()
		>>> plt.show()

		References
		----------
		.. [1] A. Savitzky, Golay, M. (1964). Smoothing and Differentiation of Data by Simplified Least Squares Procedures. 
			Analytical Chemistry. 36(8), pp 1627-1639.

		.. [2] S.A. Teukolsky, W.T. Vetterling, B.P. Flannery Numerical Recipes 3rd Edition: The Art of Scientific 
			Computing. W.H. Press,Cambridge University Press ISBN-13: 9780521880688.
		"""
		import numpy as np
		from math import factorial

		try:
			window_size = np.abs(np.int(window_size))
			order = np.abs(np.int(order))
		except ValueError:
			raise ValueError("window_size and order have to be of type int")
		if window_size % 2 != 1 or window_size < 1:
			raise TypeError("window_size size must be a positive odd number")
		if window_size < order + 2:
			raise TypeError("window_size is too small for the polynomials order")
		order_range = range(order+1)
		half_window = (window_size -1) // 2
		# precompute coefficients
		b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
		m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
		# pad the signal at the extremes with
		# values taken from the signal itself
		firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
		#breakpoint() #TODO!
		if isinstance(y, pd.core.series.Series):
			y_m1 = y.iloc[-1]
		else:
			y_m1 = y[-1]
		lastvals = y_m1 + np.abs(y[-half_window-1:-1][::-1] - y_m1)
		y = np.concatenate((firstvals, y, lastvals))
		return np.convolve( m[::-1], y, mode='valid')

	def ivt(self,data, v_threshold, config):
		"""
		Identification with Velocity Threshold.

		In the I-VT model, the velocity value is computed for every eye position sample.  The velocity value is then compared 
		to the threshold. If the sampled velocity is less than the threshold, the corresponding eye-position sample is 
		marked as part of a fixation, otherwise it is marked as a part of a saccade.

		Parameters
		----------
		data : :class:`numpy.ndarray`, shape (N,)
			the smoothed signal (or it's n-th derivative).
		v_threshold : :obj:`str`
			Velocity threshold in pix/sec.
		config : :class:`dict`
			Configuration data for data analysis. i.e. trial number, location.

		Returns
		-------
		ys : :class:`numpy.ndarray`, shape (N,)
			the smoothed signal (or it's n-th derivative).

		Notes
		-----
		From https://github.com/ecekt/eyegaze. Formula from: https://dl.acm.org/citation.cfm?id=355028

		"""
		l_time = data['timestamp']

		ts = []

		for t in l_time:
			ts.append(float(t)/1000.0)

		Xs = data['x']
		Ys = data['y']

		difX = []
		difY = []
		tdif = []


		for i in range(len(data) - 1):
			difX.append(float(Xs[i+1]) - float(Xs[i]))
			difY.append(float(Ys[i+1]) - float(Ys[i]))
			tdif.append(float(l_time[i+1]) - float(l_time[i]))

		dif = np.sqrt(np.power(difX,2) + np.power(difY,2)) #in pix
		#print (dif)

		velocity = dif / tdif
		#print velocity in pix/sec
		#print tdif

		mvmts = [] #length is len(data)-1

		for v in velocity:
			if (v < v_threshold):
				#fixation
				mvmts.append(1)
				#print v, v_threshold
			else:
				mvmts.append(0)

		fixations = []
		fs = []


		for m in range(len(mvmts)):
			if(mvmts[m] == 0):
				if(len(fs) > 0):
					fixations.append(fs)
					fs = []
			else:
				fs.append(m)

		if(len(fs) > 0):
			fixations.append(fs)

		#print fixations
		centroidsX = []
		centroidsY = []
		time0 = []
		time1 = []

		for f in fixations:
			cX = 0
			cY = 0

			if(len(f) == 1):
				i = f[0]
				cX = (float(data['x'][i]) + float(data['x'][i+1]))/2.0
				cY = (float(data['y'][i]) + float(data['y'][i+1]))/2.0
				t0 = float(data['timestamp'][i])
				t1 = float(data['timestamp'][i+1])

			else:
				t0 = float(data['timestamp'][f[0]])
				t1 = float(data['timestamp'][f[len(f)-1]+1])

				for e in range(len(f)):

					cX += float(data['x'][f[e]]) 
					cY += float(data['y'][f[e]])

				cX += float(data['x'][f[len(f)-1]+1]) 
				cY += float(data['y'][f[len(f)-1]+1]) 

				cX = cX / float(len(f)+1)
				cY = cY / float(len(f)+1)

			centroidsX.append(cX)
			centroidsY.append(cY)
			time0.append(t0)
			time1.append(t1)

		#create dataframe
		cxy_df = pd.DataFrame(np.column_stack([centroidsX, centroidsY, time0, time1]), 
					 columns=['cx', 'cy', 'start','end'])

		return cxy_df

	def hmm(self, data, filter_type, config):
		"""
		Hidden Makov Model, adapted from https://gitlab.com/nslr/nslr-hmm.

		Parameters
		----------
		data : :class:`pandas.DataFrame`
			Pandas dataframe of x,y and timestamp positions.
		filter_type : :class:`dict`
			Types of filters to use.
		config : :class:`dict`
			Configuration data for data analysis. i.e. trial number, location.

		Attributes
		----------
		data : :class:`numpy.ndarray`
			The smoothed signal (or it's n-th derivative).
		dr_th : :obj:`str`
			Data threshold.

		Notes
		-----
		**Definitions**
			* **Saccade**: The saccade is a ballistic movement, meaning it is pre-programmed and does not change once it
			  has started. Saccades of amplitude 40° peak at velocities of 300–600°/s and last for 80–150 ms.
			* **Fixation**: The point between any two saccades, during which the eyes are relatively stationary and
			  virtually all visual input occurs. Regular eye movement alternates between saccades and visual fixations, the
			  notable exception being in smooth pursuit.
			* **Smooth pursuit**: Smooth pursuit movements are much slower tracking movements of the eyes designed to
			  keep a moving stimulus on the fovea. Such movements are under voluntary control in the sense that the observer
			  can choose whether or not to track a moving stimulus. (Neuroscience 2nd edition).

		References
		----------
		.. [1] Pekkanen, J., & Lappi, O. (2017). A new and general approach to signal denoising and eye movement
			classification based on segmented linear regression. Scientific Reports, 7(1). doi:10.1038/s41598-017-17983-x.
		"""

		from . import nslr_hmm

		t = data['timestamp'].values
		x = data['x']
		y = data['y']

		#class_df (list of fixations), c_sample (list of samples with associated classification)
		class_df, c_sample = nslr_hmm.classify_gaze(t, np.vstack((x, y)).T)

		#keep fixation events only
		class_df = class_df[(class_df['class'] == 1)]

		#if trial has at least one fixation
		if class_df.shape[0]>=1:
			###split cxy0 tuple into cx0 and cy0
			class_df[['cx0', 'cy0']] = class_df['cxy0'].apply(pd.Series) 
			###split cxy0 tuple into cx1 and cy1 
			class_df[['cx1', 'cy1']] = class_df['cxy1'].apply(pd.Series)

			###drop column
			class_df = class_df.drop(['cxy0','cxy1'], axis=1)

			###merge c_sample
			data['%s_class'%(filter_type)] = c_sample

		return data, class_df

	def idt(self,data, dis_threshold, dur_threshold):
		"""
		Identification with Dispersion Threshold.

		Parameters
		----------
		data : :class:`numpy.ndarray`
			The smoothed signal (or it's n-th derivative).
		dr_th : :obj:`str`
			Fixation duration threshold in pix/msec
		di_th : :obj:`str`
			Dispersion threshold in pixels

		Returns
		-------
		ys : :class:`numpy.ndarray`
			The smoothed signal (or it's n-th derivative).

		Notes
		-----
		The I-DT algorithm has two parameters: a dispersion threshold and the length of a time window in which the dispersion 
		is calculated. The length of the time window is often set to the minimum duration of a fixation, which is around
		100-200 ms.

		"""

		current = 0 #pointer to represent the current beginning point of the window
		last = 0
		#final lists for fixation info
		centroidsX = []
		centroidsY = []
		time0 = []
		time1 = []

		while (current < len(data)):

			t0 = float(data['timestamp'][current]) #beginning time
			t1 = t0 + float(dur_threshold)     #time after a min. fix. threshold has been observed

			for r in range(current, len(data)): 
				if(float(data['timestamp'][r])>= t0 and float(data['timestamp'][r])<= t1):
					#print "if",r
					last = r #this will find the last index still in the duration threshold


			#now check the dispersion in this window
			#print "window", current, last
			points = data[current:last+1]
			dispersion = 0

			argxmin = np.min(points.loc[:,'x'].astype(np.float))
			argxmax = np.max(points.loc[:,'x'].astype(np.float))

			argymin = np.min(points.loc[:,'y'].astype(np.float))
			argymax = np.max(points.loc[:,'y'].astype(np.float))

			dispersion = ((argxmax - argxmin) + (argymax - argymin))/2

			if (dispersion <= dis_threshold):

				#add new points
				while(dispersion <= dis_threshold and last + 1 < len(data)):

					last += 1

					points = data[current:last+1]
					dispersion = 0

					argxmin = np.min(points.loc[:,'x'].astype(np.float))
					argxmax = np.max(points.loc[:,'x'].astype(np.float))

					argymin = np.min(points.loc[:,'y'].astype(np.float))
					argymax = np.max(points.loc[:,'y'].astype(np.float))

					dispersion = ((argxmax - argxmin) + (argymax - argymin))/2

				#dispersion threshold is exceeded
				#fixation at the centroid [current,last]

				cX = 0
				cY = 0

				for f in range(current, last + 1):
					cX += float(data['x'][f])
					cY += float(data['y'][f])

				cX = cX / float(last - current + 1)
				cY = cY / float(last - current + 1)

				t0 = float(data['timestamp'][current])
				t1 = float(data['timestamp'][last])

				centroidsX.append(cX)
				centroidsY.append(cY)
				time0.append(t0)
				time1.append(t1)

				current = last + 1 #this will move the pointer to a novel window

			else:
				current += 1 #this will remove the first point
				last = current #this is not necessary

		#create dataframe
		cxy_df = pd.DataFrame(np.column_stack([centroidsX, centroidsY, time0, time1]), 
					 columns=['cx', 'cy', 'start','end'])

		return cxy_df

	def simple(self,df, missing, maxdist, mindur):
		"""Detects fixations, defined as consecutive samples with an inter-sample distance of less than a set amount of 
		pixels (disregarding missing data).
   
		Parameters
		----------
		df : :class:`pandas.DataFrame`
			Pandas dataframe of x,y and timestamp positions
		missing : :obj:`str`
			Value to be used for missing data (default = 0.0)
		maxdist : :obj:`str`
			Maximal inter-sample distance in pixels (default = 25)
		mindur : :obj:`str`
			Minimal duration of a fixation in milliseconds; detected fixation cadidates will be 
			disregarded if they are below this duration (default = 100).

		Returns
		-------
		Sfix : :class:`numpy.ndarray` shape (N)
			list of lists, each containing [starttime]
		Efix : :class:`numpy.ndarray` shape (N)
			list of lists, each containing [starttime, endtime, duration, endx, endy]

		Notes
		-----
		From https://github.com/esdalmaijer/PyGazeAnalyser/blob/master/pygazeanalyser/detectors.py

		"""
		x = df['x']
		y = df['y']
		time = df['timestamp']
		# empty list to contain data
		Sfix = []
		Efix = []

		# loop through all coordinates
		si = 0
		fixstart = False
		for i in range(1,len(x)):
			# calculate Euclidean distance from the current fixation coordinate
			# to the next coordinate
			dist = ((x[si]-x[i])**2 + (y[si]-y[i])**2)**0.5
			# check if the next coordinate is below maximal distance
			if dist <= maxdist and not fixstart:
				# start a new fixation
				si = 0 + i
				fixstart = True
				Sfix.append([time[i]])
			elif dist > maxdist and fixstart:
				# end the current fixation
				fixstart = False
				# only store the fixation if the duration is ok
				if time[i-1]-Sfix[-1][0] >= mindur:
					Efix.append([Sfix[-1][0], time[i-1], time[i-1]-Sfix[-1][0], x[si], y[si]])
				# delete the last fixation start if it was too short
				else:
					Sfix.pop(-1)
				si = 0 + i
			elif not fixstart:
				si += 1


		#return Sfix, Efix
		return Sfix, Efix
