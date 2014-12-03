import matplotlib, sys
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab, math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import random
import viz, vizact
import vizmatplot

viz.go()

#ground = viz.add('tut_ground.wrl', pos = [0,0,25])

f = 0.0
angle = 60
theta = math.radians(angle) # Converts angle x from degrees to radians.
sigma_x = 1.0
sigma_y = 30.0
radius = 100

M = np.zeros((radius*2, radius*2))

def onSensorDown(e):
	if e.button == 6:
		print('pressed plus')
		angle += 1
		main()
	if e.button == 7:
		pressed('pressed minus')
		angle-=1
		main()
viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)
		
def ChangeBase(x, y, theta):
	x_theta = x * math.cos(theta) + y * math.sin(theta)
	y_theta = y * math.cos(theta) - x * math.sin(theta)
	return x_theta, y_theta

def GaborFunction(x, y, theta, f, sigma_x, sigma_y):
	r1 = ChangeBase(x, y, theta)[0] / sigma_x
	r2 = ChangeBase(x, y, theta)[1] / sigma_y
	arg = - 0.5 * (r1**2 + r2**2)
	return math.exp(arg) * math.cos(2*math.pi*f*ChangeBase(x, y, theta)[0])

def main():
	x = -float(radius)
	for i in range(radius*2):
		y = -float(radius)
		for j in range(radius*2):
			M[i, j] = GaborFunction(x, y, theta, f, sigma_x, sigma_y)
			y = y + 1
		x = x + 1

	# Normalization from 0 to 255
	M[:, :] = ((M[:, :] - M.min()) * 255) / (M.max() - M.min())

	matrix = np.round(np.random.random((8,8,4))* 255)
	fig = pylab.figure(figsize=[8, 8], facecolor='k')
	ax = fig.gca()
	plt.imshow(M, cmap=cm.Greys_r)#ax.imshow(gaborValues, cmap=mp.cm.Greys_r)
	ax.axis('off')
	
	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	plt.grid()
	
	matplot = vizmatplot.Show(fig)
	#enable display of draw rate
	matplot.showDrawRate(viz.OFF) # viz.ON or viz.OFF

main()
