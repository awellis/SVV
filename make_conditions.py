# -*- coding: utf-8 -*-
# author: Andrew Ellis <a.w.ellis@gmail.com>
# date: 20/11/2014

from __future__ import division
import csv, os

task = 'gravity'

V = {'participant_name': 'AE',
     'participant_number': '01',
     'session': '01',
     'age': '99',
     'hand': ['right', 'left'],
     'gender': ['male', 'female'],
     # 'task': ['gravity', 'egocentric'],
     'side': ['left', 'right']}

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
                               V['participant_name'], task)


positions = ['0', 'right_6', 'left_6']
adaptations = ['yes', 'no']
beliefs = ['upright', 'tilted']
durations = [1]

conditions =[{'position': position, 'adaptation': adaptation, \
            'belief': belief, 'duration': duration} \
            for position in positions for adaptation in adaptations \
            for belief in beliefs for duration in durations]

for cond in conditions:
    if cond['adaptation'] == 'yes':
        cond['duration'] = 11
    else:
        cond['duration'] = 6

from random import shuffle, seed

seed(19834 * int(V['participant_number']))
shuffle(conditions)


column_headers = ['duration', 'tilt_position', 'adaptation', 'belief']
with open(filename + '.csv', 'wb') as conditions_file:
        writer = csv.writer(conditions_file, dialect='excel')
        writer.writerow(column_headers)
        for row in conditions:
            writer.writerow(row.values())

print("Created conditions file for participant {0}".format(participant_dir))

