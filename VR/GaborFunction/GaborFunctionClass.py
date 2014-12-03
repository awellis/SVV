import matplotlib, sys
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab, math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import random, viz, vizmatplot, vizact

viz.go()

# Load DirectInput plug-in
#dinput = viz.add('DirectInput.dle')
# Add first available joystick
#joy = dinput.addJoystick()

class GaborPatch():
	""" http://www.science-emergence.com/ImageProcessing/ImageProcessingPython/PlotGaborFilterMatplotlib/
	one can think of a Gabor function as the image produced when looking at a sine or cosine wave 
	through a Gaussian window"""
	
	###pylab.clf()
	
	def __init__(self):
		self.F = 0.0
		self.ANGLE = 30
		self.theta = math.radians(self.ANGLE) # Converts angle x from degrees to radians.
		self.sigma_x = 1.0
		self.sigma_y = 30.0
		self.radius = 100
		
		self.M = np.zeros((self.radius*2, self.radius*2))
		# viz.ON or viz.OFF

	def onSensorDown(self, key):
		#if e.button == 6:.
		if key == viz.KEY_RIGHT:
			self.ANGLE += 10
			print(self.ANGLE)
			pylab.clf()
			self.Gabor()
		#if e.button == 7:
		if key == viz.KEY_LEFT:
			self.ANGLE -= 10
			print(self.ANGLE)
			pylab.clf()
			self.Gabor()
			
	def ChangeBase(self, x, y, theta):
		self.x_theta = x * math.cos(self.theta) + y * math.sin(self.theta)
		self.y_theta = y * math.cos(self.theta) - x * math.sin(self.theta)
		return self.x_theta, self.y_theta

	def GaborFunction(self, x, y, theta, f, sigma_x, sigma_y):
		r1 = self.ChangeBase(x, y, theta)[0] / sigma_x
		r2 = self.ChangeBase(x, y, theta)[1] / sigma_y
		arg = - 0.5 * (r1**2 + r2**2)
		return math.exp(arg) * math.cos(2*math.pi*f*self.ChangeBase(x, y, theta)[0])

	def Gabor(self):
		self.theta = math.radians(self.ANGLE)
		x = -float(self.radius)
		for i in range(self.radius*2):
			y = -float(self.radius)
			for j in range(self.radius*2):
				self.M[i, j] = self.GaborFunction(x, y, self.theta, self.F, self.sigma_x, self.sigma_y)
				y = y + 1
			x = x + 1
		# Normalization from 0 to 255
		self.M[:, :] = ((self.M[:, :] - self.M.min()) * 255) / (self.M.max() - self.M.min())
		
		self.Plot()
				
	def Plot(self):
		# Create a figure with size 8 x 8 inches, resolution 80 dots per inch and 
		# set color of drawing background to black = 'k' 
		self.fig = pylab.figure(figsize=[8, 8], dpi=100, facecolor='k')
		# gca stands for 'get current axis'
		self.ax = self.fig.gca()
		self.ax.axis('off')
		plt.imshow(self.M, cmap=cm.Greys_r)
		plt.hold(False)
		#enable rendering of plot by passing the pyplot figure to vizmatplot
		plt.grid()
		#enable display of draw rate
		#self.matplot.showDrawRate(viz.OFF)

def main():
	patch = GaborPatch()
	patch.Gabor()
	#viz.callback(viz.SENSOR_DOWN_EVENT, patch.onSensorDown)
	viz.callback(viz.KEYDOWN_EVENT, patch.onSensorDown)
main()



