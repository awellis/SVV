# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 14:56:34 2014

@author: Andrew Ellis <a.w.ellis@gmail.com>
"""

# TODO:
def make_win(full_screen=False):
    win = visual.Window(size=(1200, 800), fullscr=full_screen,
                        units = 'pix', screen=0,
                        allowGUI=False, allowStencil=False,
                        monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
                        blendMode='avg', useFBO=True)
    return(win)



def gen_trial_list(conditions):
    trial_list = data.createFactorialTrialList(conditions)
    for item in trialList:
        if item['orientation'] > 0:
            item['correct_key'] = expInfo['right_key']
        elif item['orientation'] < 0:
            item['correct_key'] = expInfo['left_key']
    return trial_list


def draw_fixation(color):
    stim_list = [fixation_left, fixation_right]
    while 'space' not in event.getKeys():
        [s.setFillColor(color) for s in stim_list]
        [s.draw() for s in stim_list]
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
        no_response = True
        while no_response:
            frame_n += 1
            if frame_n >= 0:
                if frame_n < 30:
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

class csvWriter(object):
    def __init__(self, saveFilePrefix='', saveFolder=''):
        """
        Creates a csv file and appends single rows to it using the csvWriter.write() function.
        Use this function to save trials. Writing is very fast. Around a microsecond.

        :saveFilePrefix: a string to prefix the file with
        :saveFolder: (string/False) if False, uses same directory as the py file

        So you'd do this::
                # In the beginning of your script
                writer = ppc.csvWriter('subject 1', 'dataFolder')

                # In the trial-loop
                trial = {'condition': 'fun', 'answer': 'left', 'rt': 0.224}  # your trial
                writer.write(trial)
        """
        import csv, time

        # Create folder if it doesn't exist
        if saveFolder:
            import os
            saveFolder += '/'
            if not os.path.isdir(saveFolder):
                os.makedirs(saveFolder)

        # Generate self.saveFile and self.writer
        self.saveFile = saveFolder + str(saveFilePrefix) + ' (' + time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()) +').csv'  # Filename for csv. E.g. "myFolder/subj1_cond2 (2013-12-28 09-53-04).csv"
        self.writer = csv.writer(open(self.saveFile, 'wb'), delimiter=';').writerow  # The writer function to csv. It appends a single row to file
        self.headerWritten = False

    def write(self, trial):
        """:trial: a dictionary"""
        if not self.headerWritten:
            self.headerWritten = True
            self.writer(trial.keys())
        self.writer(trial.values())



def getActualFrameRate(frames=1000):
    """
    Measures the actual framerate of your monitor. It's not always as clean as
    you'd think. Prints various useful information.
        :frames: number of frames to do test on.
    """
    from psychopy import visual, core

    # Set stimuli up
    durations = []
    clock = core.Clock()
    win = visual.Window(color='pink')

    # Show a brief instruction / warning
    visual.TextStim(win, text='Now wait and \ndon\'t do anything', color='black').draw()
    win.flip()
    core.wait(1.5)

    # blank screen and synchronize clock to vertical blanks
    win.flip()
    clock.reset()

    # Run the test!
    for i in range(frames):
        win.flip()
        durations += [clock.getTime()]
        clock.reset()

    win.close()

    # Print summary
    import numpy as np
    print 'average frame duration was', round(np.average(durations) * 1000, 3), 'ms (SD', round(np.std(durations), 5), ') ms'
    print 'corresponding to a framerate of', round(1 / np.average(durations), 3), 'Hz'
    print '60 frames on your monitor takes', round(np.average(durations) * 60 * 1000, 3), 'ms'
    print 'shortest duration was ', round(min(durations) * 1000, 3), 'ms and longest duration was ', round(max(durations) * 1000, 3), 'ms'
