import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt

import time
import random

import viz
import viztask

import vizmatplot

viz.go()

#determine size of arrays (number of samples)
MAX_SIZE_OF_ARRAY = 1000

#create arrays
array_x, array_y = [],[]

#fill array with zeros 
for i in range(0,MAX_SIZE_OF_ARRAY):
	array_x.append(0)
	array_y.append(0)
	
###---matplotlib codes---###
fig = plt.figure()	#instantiate pyplot figure
ax = fig.add_subplot(111)	#create axes
ax.axis([0,MAX_SIZE_OF_ARRAY,0,1])	#determine axis limits
line, = ax.plot(array_x,array_y)	#instantiate plot 
matplot = vizmatplot.Show(fig)
matplot.showDrawRate(viz.ON)

def plotter():
	""" task that randomly creates y data while incrementing x data"""
	while True:
		#yield None
		for i in range (0,MAX_SIZE_OF_ARRAY):
			array_x[i] = (i)	
			array_y[i] = (random.random())
			ax.axis([0,MAX_SIZE_OF_ARRAY,0,1])	#make sure the axis limits don't change
			line.set_data(array_x,array_y)	#set the data points
		
			yield None	#wait at least a frame before setting new data points
		#	yield viztask.waitTime(matplot.rate) #or wait draw rate length calculated in module
		
		for b in range(0,MAX_SIZE_OF_ARRAY):	#clear out the arrays 
			array_x[b] = 0
			array_y[b] = 0
			line.set_data(array_x,array_y)	#clear graph by setting all data points to [0,0]
			
	
viztask.schedule( plotter() )