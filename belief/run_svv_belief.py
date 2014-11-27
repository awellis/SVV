# -*- coding: utf-8 -*-
# author: Andrew Ellis <a.w.ellis@gmail.com>
# date: 16/11/2014

from __future__ import division
from psychopy import core, data, event, sound, gui
# import pyglet
# pyglet.options['shadow_window'] = False
import numpy as np
import os
from sys import platform as _platform
"""
1) calibrate (yes/no)
2) once calibrated, we are in a given tilt position
3) do staircase or adjustment in order to roughly determine the SVV
4) given the estimated SVV, use this as midpoint when creating line orientations
"""

# GUI dialogue
exp_name = 'svv_belief'

V = {'participant_name': 'AE',
     'participant_number': '01',
     'session': '01',
     'age': '99',
     'hand': ['right', 'left'],
     'gender': ['male', 'female'],
     'xpos': 480,
     'tilt_position': ['0', '-5', '5'],
     'reps': 40,
     'side': ['left', 'right'],
     # 'belief_side': ['left', 'right'],
     # 'adaptation': ['yes', 'no'],
     'belief': ['upright', 'tilted'],
     'task': ['gravity', 'ego'],
     'estimation_method': ['adjustment'],
     # 'estimation_method': ['adjustment', 'staircase'],
     'display': ['oculus', 'laptop'],
     'Moog': ['yes', 'no'],
     'n_adjust': 1}


dlg = gui.DlgFromDict(dictionary=V, title=exp_name,
                      order=['participant_number', 'participant_name', 'age',
                      'hand', 'gender', 'xpos', 'session',
                      'side', 'tilt_position',
                      'belief', 'task', 'reps', 'Moog', 'display', 'n_adjust'])

if not dlg.OK:
    core.quit()

V['date'] = data.getDateStr()
V['exp_name'] = exp_name


"""
workaround for dropdown selection error:
https://groups.google.com/forum/#!topic/psychopy-users/jV8JBSwIUWk
"""
from psychopy import visual


# experiment parameters
valid_responses = ['f', 'j', 'escape']
audio_dir = 'audio'
RANGE = 3  # test orientations lie in the range [svv-RANGE, svv+RANGE]
# number of test orientations around estimate
N_ORI = 7
N_REPS = int(V['reps'])

ITI_DURATION = 60
LINE_DURATION = 30
MOVEMENT_DURATION = 40 # 40 seconds

# stimulus parameters
XPOS = V['xpos']

if V['display'] == "oculus":
    OPACITY = 0.1
else:
    OPACITY = 0.6

print("Line opacity: {0}". format(OPACITY))

FIX_SIZE = [20, 20]
LINE_SIZE = [15, 250]
NOISE_SIZE = [300, 300]

COLOR = {"blue": [-1, -1, 1],
            "red": [1, -1, -1],
            "yellow": [1, 1, -1],
            "green": [-1, 1, -1],
            "orange": [1, 0, -1],
            "black": [-1, -1, -1]}


"""
Setup output files (CSV and log files)
"""
if not os.path.isdir('data'):
    os.makedirs('data')

filename = 'data' + os.sep + '{0:s}_{1:s}_{2:s}_{3:s}_{4:s}_{5:s}_{6:s}'.format(
    V['participant_number'], V['participant_name'], V['exp_name'],
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
    if _platform == "win32":
        screen_n = 1
    else:
        screen_n = 0
else:
    full_screen = False
    screen_n = 0

win = visual.Window(size=(1200, 800), fullscr=full_screen,
                    units='pix', screen=screen_n,
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
    print('Frame rate: {frame_rate}'.format(frame_rate=V['frame_rate']))
    print('Scaling factor: {scaling_factor}'.format(scaling_factor=scaling_factor))


"""
define functions
"""
def make_noise(size=512):
    return np.random.random((size, size))*2-1

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

                                    tex=make_noise(),
                                    mask='gauss',
                                    ori=0,
                                    pos=[-xpos, 0],
                                    size=NOISE_SIZE,
                                    sf=None,
                                    phase=0.0,
                                    color=[1, 1, 1],
                                    colorSpace='rgb',
                                    opacity=0.6,
                                    texRes=512,
                                    interpolate=True,
                                    depth=-1.0)

    noise_right = visual.GratingStim(win=win,
                                     name='noise_right',
                                     # tex=np.random.random((512, 512))*2-1,
                                     tex=make_noise(),
                                     mask='gauss',
                                     ori=0,
                                     pos=[xpos, 0],
                                     size=NOISE_SIZE,
                                     sf=None,
                                     phase=0.0,
                                     color=[1, 1, 1],
                                     colorSpace='rgb',
                                     opacity=0.6,
                                     texRes=512,
                                     interpolate=True,
                                     depth=-1.0)

    return(clock, voice, fixation_left, fixation_right, line_left, line_right, noise_left, noise_right)


def print_message(what, message):
    print('{what}: {message}'.format(what=what, message=message))


def draw_fixation(color):
    """args: color should be a string
    """
    print_message("Color", color)
    print("Press 'space' to continue")
    while 'space' not in event.getKeys():
        [s.setFillColor(COLOR[color]) for s in fixations]
        [s.draw() for s in fixations]
        win.flip()
        if event.getKeys(["escape"]):
            core.quit()
    event.clearEvents()
    win.flip()
    core.wait(0.5)


def draw_lines(lines, trials):
    print("Starting 2AFC task now")
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


def play_voice(V, voice, dur=4):
    if V['belief'] == 'upright':
        message = os.path.join(audio_dir, 'aufrecht.wav')
        print("Message: aufrecht")

    elif V['belief'] == 'tilted':
        # this_tilt_pos = float(V['tilt_position'])
        if V['side'] == "right":
            message = os.path.join(audio_dir, 'rechts_geneigt.wav')
            print("Message: rechts geneigt")
        elif V['side'] == "left":
            message = os.path.join(audio_dir, 'links_geneigt.wav')
            print("Message: links geneigt")

    voice.setSound(message)
    voice.play()
    win.flip()
    core.wait(dur)


def ask_calibrate():
    done = False
    print("Press 'space' to continue or 'c' for calibration")
    while not done:
        [s.setFillColor(COLOR['yellow']) for s in fixations]
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


def wait_quit():
    print("Press 'q' to end experiment")
    done = False
    while not done:
        [s.setFillColor(COLOR['black']) for s in fixations]
        [s.draw() for s in fixations]
        win.flip()
        if event.getKeys(["q"]):
            done = True
            # core.quit()
    event.clearEvents()
    win.flip()
    core.wait(0.5)


def deg2rad(deg):
    import math
    rad = (math.pi/180) * deg
    return(rad)


def rad2deg(rad):
    import math
    deg = (180/math.pi) * rad
    return(deg)


def transform(ori):
    if ori < 0:
        sign = -1
    elif ori >= 0:
        sign = 1
    ori = ori % (sign * 360)
    return(ori)


def flip_coin(boolean=True):
    import numpy as np
    if boolean:
        return(np.random.choice([True, False]))
    else:
        return(np.random.binomial(n=1, p=0.5, size=1))


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


# ------------------------------------------------------------------------------
# EXPERIMENT STARTS HERE
# ------------------------------------------------------------------------------

calibrate = ask_calibrate()

if calibrate:
    print('Calibration: {0}'.format(calibrate))
    xpos = V['xpos']

    [s.setFillColor(COLOR['orange']) for s in fixations]
    done = False

    while not done:
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
# print("Press 'space' to continue")
draw_fixation(color='green')

print("Playing instructions:")
play_voice(V, voice, dur=4)

if V['Moog'] == 'yes':
    print("Running experiment on MOOG")
else:
    print("Running experiment on laptop")


if V['Moog'] == 'yes':
    print("Waiting for Moog to finish...")
    countdown = MOVEMENT_DURATION * ITI_DURATION
    while countdown >= 0:
        if countdown % 60 == 0:
            print("Countdown: {0}".format(countdown))
        win.flip()
        countdown -= 1
else:
    core.wait(0.5)


# wait for another 10 seconds

print("Waiting for another 5 seconds...")
core.wait(5)

print("Waiting for adjustment task to start")
draw_fixation(color='green')


"""
2) obtain rough SVV estimate
    a) adjustment
    b) staircase (not yet implemented)
provides estimated SVV (default 0 deg)
"""

tilt = float(V['tilt_position'])
if V['side'] == 'left':
    ori = round(np.random.uniform(-tilt-2, tilt))
elif V['side'] == 'right':
    ori = round(np.random.uniform(-tilt, tilt+2))

# tilt = side * float(V['tilt_position'])
# ori = round(np.random.uniform(tilt-2, tilt+2), 2)


# start adjustment task
print("Adjustment task started...")
done = False
while not done:
    [line.setOri(ori) for line in lines]
    [line.draw() for line in lines]

    if event.getKeys('f'):
        ori -= 1
        print('current SVV: {svv}'.format(svv=ori))
    elif event.getKeys('j'):
        ori += 1
        print('current SVV: {svv}'.format(svv=ori))

    if event.getKeys('escape'):
        core.quit()

    if event.getKeys('space'):
        done = True
    win.flip()

# TODO: transform ori so that it always lies in interval [-90, 90]

V['SVV'] = transform(ori)


# this is the rough estimate of the SVV
svv = V['SVV']
print("Final SVV estimate: {0}".format(svv))

core.wait(0.5)


# spin line and then draw some noise to get rid of adjust line
frame_n = -1
degrees = 360/30

print("Rotate line and draw some noise")

if flip_coin():
    op = '+'
else:
    op = '-'

while frame_n < 5 * ITI_DURATION:
    frame_n += 1
    if frame_n % 1 == 0:
        ori = ori
        [line.setOri(degrees, op) for line in lines]
        [line.draw() for line in lines]
        win.flip()

frame_n = -1
noise_left.setPos([-xpos, 0])
noise_right.setPos([xpos, 0])

while frame_n < 5 * ITI_DURATION:
    frame_n += 1
    if frame_n % 2 == 0:
        noise_texture = np.random.random((512, 512))*2-1
        [i.setTex(noise_texture) for i in noise]
    [i.draw() for i in noise]
    win.flip()


"""
3) line orientation judgment trials
    using the rough SVV estimate as centre for line orientations
"""

# GO signal for line orientation discrimination trials
print("Waiting for 2AFC task to start\n")
draw_fixation(color='green')


sequence = list(np.linspace(start=svv-RANGE, stop=svv+RANGE, num=N_ORI))

conditions = {'orientation': sequence}
trial_list = data.createFactorialTrialList(conditions)
trials = data.TrialHandler(trialList=trial_list, nReps=N_REPS, method='random')
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
draw_fixation(color='yellow')
print("2AFC task done")

wait_quit()

"""
end experiment
"""
win.close()
core.quit()
