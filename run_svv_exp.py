# -*- coding: utf-8 -*-
# @author: Andrew Ellis <a.w.ellis@gmail.com>

from __future__ import division
from psychopy import visual, core, data, event, logging, sound, gui
import pyglet
pyglet.options['shadow_window'] = False
import numpy as np
import os

"""
1) calibrate (yes/no)
2) once calibrated, we are in a given tilt position
3) do staircase or adjustment in order to roughly determine the SVV
4) given the estimated SVV, use this as midpoint when creating line orientations
"""

# experiment parameters
valid_responses = ['f', 'j', 'escape']
audio_dir = 'audio'
RANGE = 3  # test orientations lie in the range [est-RANGE, est+RANGE]
# number of test orientations around estimate
N_ORI = 9
N_REPS = 10
ITI_DURATION = 60
LINE_DURATION = 30

# stimulus parameters
XPOS = 500
OPACITY = 0.15
FIX_SIZE = [20, 20]
LINE_SIZE = [15, 300]
NOISE_SIZE = [300, 300]
blue = [-1, -1, 1]
red = [1, -1, -1]
yellow = [1, 1, -1]
green = [-1, 1, -1]
orange = [1, 0, -1]

# GUI dialogue
exp_name = 'svv'

V = {'participant': 'AE',
     'session': '01',
     'age': '99',
     'gender': ['male', 'female'],
     'xpos': 480,
     'tilt_position': ['0', '4', '6', '16'],
     'side': ['left', 'right'],
     'belief': ['upright', 'tilted'],
     'task': ['ego', 'gravity'],
     'estimation_method': ['adjustment', 'staircase'],
     'display': ['laptop', 'oculus']}


dlg = gui.DlgFromDict(dictionary=V, title=exp_name)

if not dlg.OK:
    core.quit()

V['date'] = data.getDateStr()
V['exp_name'] = exp_name

"""
Setup output files (CSV and log files)
"""
if not os.path.isdir('data'):
    os.makedirs('data')

filename = 'data' + os.sep + '{0:s}_{1:s}_{2:s}_{3:s}_{4:s}_{5:s}'.format(
    V['participant'], V['task'],
    V['tilt_position'], V['belief'], V['session'],
    V['date'])


# logFile = logging.LogFile(filename+'.log', level=logging.EXP)
# logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file


"""
Experiment handler
"""
experiment = data.ExperimentHandler(name=exp_name,
                                    version='',
                                    extraInfo=V,
                                    runtimeInfo=None,
                                    originPath=None,
                                    savePickle=True,
                                    saveWideText=True,
                                    dataFileName=filename)


if V['display'] == 'oculus':
    full_screen = True
else:
    full_screen = False

win = visual.Window(size=(1200, 800), fullscr=full_screen,
                    units='pix', screen=0,
                    allowGUI=False, allowStencil=False,
                    monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
                    blendMode='avg', useFBO=True)

V['frame_rate'] = win.getActualFrameRate()
if V['frame_rate'] is not None:
    frame_dur = 1.0/round(V['frame_rate'])
else:
    frame_dur = 1.0/60.0

if V['display'] == 'oculus':
    scaling_factor = round(V['frame_rate'])/60
    ITI_DURATION = 60*scaling_factor
    LINE_DURATION = 30*scaling_factor
    print('Frame rate: {0}'.format(V['frame_rate']))

"""
functions
"""

def create_stimuli(win, xpos):
    clock = core.Clock()
    voice = sound.Sound('A', secs=3)

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

    line_left = visual.GratingStim(win=win,
                                   name='line_left',
                                   tex='sin',
                                   mask='gauss',
                                   ori=0,
                                   pos=[-xpos, 0],
                                   size=LINE_SIZE,
                                   sf=None,
                                   phase=0.0,
                                   color=[1, 1, 1],
                                   colorSpace='rgb',
                                   opacity=OPACITY,
                                   texRes=512,
                                   interpolate=True,
                                   depth=-1.0)

    line_right = visual.GratingStim(win=win,
                                    name='line_right',
                                    tex='sin',
                                    mask='gauss',
                                    ori=0,
                                    pos=[xpos, 0],
                                    size=LINE_SIZE,
                                    sf=None,
                                    phase=0.0,
                                    color=[1, 1, 1],
                                    colorSpace='rgb',
                                    opacity=OPACITY,
                                    texRes=512,
                                    interpolate=True,
                                    depth=-1.0)

    noise_left = visual.GratingStim(win=win,
                               name='noise_left',
                               tex=np.random.random((512, 512))*2-1,
                               mask='gauss',
                               ori=0,
                               pos=[-xpos, 0],
                               size=NOISE_SIZE,
                               sf=None,
                               phase=0.0,
                               color=[1,1,1],
                               colorSpace='rgb',
                               opacity=0.6,
                               texRes=512,
                               interpolate=True,
                               depth=-1.0)

    noise_right = visual.GratingStim(win=win,
                               name='noise_right',
                               tex=np.random.random((512, 512))*2-1,
                               mask='gauss',
                               ori=0,
                               pos=[xpos, 0],
                               size=NOISE_SIZE,
                               sf=None,
                               phase=0.0,
                               color=[1,1,1],
                               colorSpace='rgb',
                               opacity=0.6,
                               texRes=512,
                               interpolate=True,
                               depth=-1.0)

    return(clock, voice, fixation_left, fixation_right, line_left, line_right, noise_left, noise_right)


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

def draw_lines(lines, trials):
    for trial in trials:
        t = 0
        frame_n = 0

        [line.setOri(trial['orientation']) for line in lines]

        event.clearEvents()
        clock.reset()
        # win.callOnFlip(clock.reset)

        no_response = True
        while no_response:
            frame_n += 1
            if frame_n >= 0:
                if frame_n < LINE_DURATION:
                    [line.draw() for line in lines]

            if frame_n >= 0:
                keys = event.getKeys(keyList=valid_responses, timeStamped=clock)

                if len(keys) > 0:
                    no_response = False

            win.flip()

        if 'escape' in keys[-1][0]:
            core.quit()
        else:
            # Take only the last key press
            response = keys[-1][0]
            rt = keys[-1][1]

        trials.addData('response', response)
        trials.addData('rt', rt)

        # inter-trial interval
        frameN = -1
        while frameN < ITI_DURATION:
            frameN += 1
            win.flip()

        experiment.nextEntry()

def play_voice(V, voice):
    # TODO: check logic here...
    if V['belief'] == 'upright':
        message = os.path.join(audio_dir, 'aufrecht.wav')
    elif V['belief'] == 'tilted':
        if V['side'] == 'left':
            side = -1
        elif V['side'] == 'right':
            side = 1
        this_tilt_pos = side * float(V['tilt_position'])
        if this_tilt_pos > 6:
            message = os.path.join(audio_dir, 'rechts_stark.wav')
        elif (this_tilt_pos > 0) or (this_tilt_pos == 0 and V['side'] == 'left'):
            message = os.path.join(audio_dir, 'rechts_leicht.wav')
        elif this_tilt_pos < -6:
            message = os.path.join(audio_dir, 'links_stark.wav')
        elif (this_tilt_pos < 0) or (this_tilt_pos == 0 and V['side'] == 'right'):
            message = os.path.join(audio_dir, 'links_leicht.wav')

    voice.setSound(message)
    voice.play()
    win.flip()

    core.wait(4)

def ask_calibrate():
    done = False
    while not done:
        [s.setFillColor(red) for s in fixations]
        [s.draw() for s in fixations]
        win.flip()
        if event.getKeys(["escape"]):
            core.quit()
        if event.getKeys(['c']):
            calibrate = True
            done = True
        if event.getKeys(['space']):
            calibrate = False
            done = True

    event.clearEvents()
    win.flip()
    core.wait(0.5)
    return calibrate


"""
create stimuli
"""""
clock, voice, fixation_left, fixation_right, line_left, line_right, noise_left, noise_right = \
    create_stimuli(win=win, xpos=XPOS)

fixations = [fixation_left, fixation_right]
lines = [line_left, line_right]
noise = [noise_left, noise_right]
left_stims = [fixation_left, line_left]
right_stims = [fixation_right, line_right]


#------------------------------------------------------------------------------
# EXPERIMENT STARTS HERE
#------------------------------------------------------------------------------

calibrate = ask_calibrate()

if calibrate:
    print('Calibration: {0}'.format(calibrate))
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

        if event.getKeys('escape'):
            core.quit()

        if event.getKeys('space'):
            done = True
        win.flip()

    V['xpos'] = xpos
else:
    xpos = V['xpos']

[s.setPos([-xpos, 0]) for s in left_stims]
[s.setPos([xpos, 0]) for s in right_stims]


core.wait(1)

"""
INSTRUCTIONS
"""
draw_fixation(color=green)
play_voice(V, voice)
draw_fixation(color=green)

core.wait(0.5)

"""
2) obtain rough SVV estimate
    a) adjustment
    b) staircase
provides estimated SVV (default 0 deg)
"""

tilt = float(V['tilt_position'])
if V['side'] == 'left':
    ori = round(np.random.uniform(-tilt, 6))
elif V['side'] == 'right':
    ori = round(np.random.uniform(-6, tilt))

#tilt = side * float(V['tilt_position'])
#ori = round(np.random.uniform(tilt-2, tilt+2), 2)


if V['estimation_method'] == 'adjustment':
    done = False
    while not done:
        [line.setOri(ori) for line in lines]
        [line.draw() for line in lines]

        if event.getKeys('f'):
            ori -= 1
            print('SVV: {svv}'.format(svv=ori))
        elif event.getKeys('j'):
            ori += 1
            print('SVV: {svv}'.format(svv=ori))

        if event.getKeys('escape'):
            core.quit()

        if event.getKeys('space'):
            done = True
        win.flip()

    V['SVV'] = ori

elif V['estimation_method'] == 'staircase':
    # do some other stuff...
    V['SVV'] = 0


# this is the rough estimate of the SVV
svv = V['SVV']

core.wait(0.5)


# draw some noise to get rid of adjuste line
frame_n = -1
noise_left.setPos([-xpos, 0])
noise_right.setPos([xpos, 0])

while frame_n < ITI_DURATION:
    frame_n += 1
    if frame_n%2 == 0:
        noise_texture = np.random.random((512, 512))*2-1
        [i.setTex(noise_texture) for i in noise]
    [i.draw() for i in noise]
    win.flip()




"""
3) line orientation judgment trials
    using the rough SVV estimate as centre for line orientations
"""

# GO signal for line orientation discrimination trials
draw_fixation(color=green)
sequence = list(np.linspace(start=svv-RANGE, stop=svv+RANGE, num=N_ORI))

conditions = {'orientation': sequence}
trial_list = data.createFactorialTrialList(conditions)
trials = data.TrialHandler(trialList=trial_list, nReps = N_REPS, method='random')
experiment.addLoop(trials)


"""
start trial loop
"""

# initial interval
frame_n = 0
while frame_n < ITI_DURATION:
    frame_n += 1
    win.flip()


# start trial
draw_lines(lines, trials)



# draw yellow circle to indicate end of trials
draw_fixation(color=yellow)



"""
end experiment
"""
win.close()
core.quit()
