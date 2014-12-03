from __future__ import division
from psychopy import core, data, event, logging, sound, gui
import pyglet
pyglet.options['shadow_window'] = False
import numpy as np
import os
from sys import platform as _platform

# GUI dialogue
exp_name = 'calibration'

V = {'xpos': 480}

from psychopy import visual

# experiment parameters
valid_responses = ['f', 'j', 'escape']

# stimulus parameters
XPOS = 500
OPACITY = 0.15
FIX_SIZE = [20, 20]
blue = [-1, -1, 1]
red = [1, -1, -1]
yellow = [1, 1, -1]
green = [-1, 1, -1]
orange = [1, 0, -1]
black = [-1, -1, -1]

win = visual.Window(size=(1200, 800), fullscr=True,
                    units='pix', screen=1,
                    allowGUI=False, allowStencil=False,
                    monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
                    blendMode='avg', useFBO=True)

V['frame_rate'] = win.getActualFrameRate()
if V['frame_rate'] is not None:
    frame_dur = 1.0/round(V['frame_rate'])
else:
    frame_dur = 1.0/60.0


scaling_factor = round(V['frame_rate'])/60
print('Frame rate: {frame_rate}'.format(frame_rate=V['frame_rate']))
print('Scaling factor: {scaling_factor}'.format(scaling_factor=scaling_factor))

def create_stimuli(win, xpos):
    clock = core.Clock()

    fixation_left = visual.Polygon(win=win,
                                   name='fixation_left',
                                   edges=120,
                                   size=FIX_SIZE,
                                   ori=0,
                                   pos=[-xpos, 0],
                                   lineWidth=1,
                                   lineColor=[-1, -1, -1],
                                   lineColorSpace='rgb',
                                   fillColor=[-1, 1, -1],
                                   fillColorSpace='rgb',
                                   opacity=OPACITY,
                                   interpolate=True)

    fixation_right = visual.Polygon(win=win,
                                    name='fixation_right',
                                    edges=120,
                                    size=FIX_SIZE,
                                    ori=0,
                                    pos=[xpos, 0],
                                    lineWidth=1,
                                    lineColor=[-1, -1, -1],
                                    lineColorSpace='rgb',
                                    fillColor=[-1, 1, -1],
                                    fillColorSpace='rgb',
                                    opacity=OPACITY,
                                    interpolate=True)
    return(clock, fixation_left, fixation_right)

def draw_fixation(color):
    while 'space' not in event.getKeys():
        [s.setFillColor(color) for s in fixations]
        [s.draw() for s in fixations]
        win.flip()
        if event.getKeys(["escape"]):
            core.quit()
    event.clearEvents()
    win.flip()
    core.wait(0.5)

clock,  fixation_left, fixation_right = \
    create_stimuli(win=win, xpos=XPOS)

fixations = [fixation_left, fixation_right]



xpos = V['xpos']

[s.setFillColor(orange) for s in fixations]
done = False
while not done:
#        line_left.setPos([-xpos, 0])
#        line_right.setPos([xpos, 0])
#        [line.draw() for line in lines]
    fixation_left.setPos([-xpos, 0])
    fixation_right.setPos([xpos, 0])
    [s.draw() for s in fixations]

    if event.getKeys('f'):
        xpos -= 1
        print('X Position: {0}'.format(xpos))

    elif event.getKeys('j'):
        xpos += 1
        print('X Position: {0}'.format(xpos))

    if event.getKeys('space'):
        done = True
    win.flip()

V['xpos'] = xpos
print('Final X Position: {0}'.format(xpos))

with open("IPD.txt", "w") as text_file:
    text_file.write("Interpupillary distance: {0}".format(xpos))
core.quit()