# -*- coding: utf-8 -*-
# author: Andrew Ellis <a.w.ellis@gmail.com>
# date: 02/12/2014

from __future__ import division
import csv
import os
from psychopy import gui
from random import shuffle, seed


experiment = 'egocentric-adaptation'

V = {'participant_name': 'FM',
     'participant_number': '501',
     # 'session': '01',
     # 'age': '99',
     # 'hand': ['right', 'left'],
     'gender': ['male', 'female'],
     # 'task': ['gravity', 'egocentric'],
     'side': ['left', 'right']}

dlg = gui.DlgFromDict(dictionary=V, title='Create conditions',
                      order=['participant_number', 'participant_name'])

"""
Setup output files
"""
if not os.path.isdir('participants'):
    os.makedirs('participants')

participant_dir = V['participant_number'] + '_' + V['participant_name']

if not os.path.isdir('participants' + os.sep + participant_dir):
    os.makedirs('participants' + os.sep + participant_dir)

filename = 'participants' + os.sep + participant_dir + os.sep + \
    '{0:s}_{1:s}_{2:s}'.format(str(V['participant_number']),
                               V['participant_name'], experiment)


positions = ['0', '5']
tasks = ['egocentric', 'gravity']
adaptations = ["left", "right"]
side = V['side']

conditions =[{'position': position, \
            'task': task, \
            'adaptation': adaptation, \
            'side': side} \
            for position in positions \
            for task in tasks \
            for adaptation in adaptations]


seed(1985834 * int(V['participant_number']))
shuffle(conditions)

column_headers = ['tilt_position', 'task', 'adaptation', 'side']
with open(filename + '.csv', 'wb') as conditions_file:
        writer = csv.writer(conditions_file, dialect='excel')
        writer.writerow(column_headers)
        for row in conditions:
            writer.writerow(row.values())

print("Created conditions file for participant {0}".format(participant_dir))

