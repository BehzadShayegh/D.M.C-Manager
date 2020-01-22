import PySimpleGUI as sg
import time
import numpy as np
import os
import json
from math import floor
import pandas as pd
measurer = np.vectorize(len)

TIME_LIMIT = 3*60*15
START_PROBLEM_ID = 1
SIZE = 5

groups = pd.read_csv("../db/groupsActivity.csv")
problems = pd.read_csv("../db/problemHistory.csv")
maximumGroupNameLenght = max(measurer(groups['name']))

# INTERFACE

sg.ChangeLookAndFeel('Dark')  

def rankColor(index) :
    if index == 0 :
        return 'gold'
    elif index == 1 :
        return 'silver'
    elif index == 2 :
        return 'darkorange'
    else : return 'white'

rightSide = [
    [sg.Text(str(index+1)+'. '+groups['name'][index], size=(floor(0.3*SIZE*maximumGroupNameLenght), 1), text_color=rankColor(index), background_color='black', font=("Helvetica", 3*SIZE), key='rank'+str(index)),
    sg.Text(groups['point'][index], justification='left', text_color=rankColor(index), background_color='black', key='point'+str(index), font=("Helvetica", 3*SIZE), size=(10, 1))]
    for index in range(15) ]
rightestSide = [
    [sg.Text(str(index+1)+'. '+groups['name'][index], size=(floor(0.3*SIZE*maximumGroupNameLenght), 1), text_color='white', background_color='black', key='rank'+str(index), font=("Helvetica", 2*SIZE)),
    sg.Text(groups['point'][index], justification='left', text_color='white', background_color='black', key='point'+str(index), font=("Helvetica", 2*SIZE), size=(10, 1))]
    for index in range(15, groups.shape[0])]

def problem(tag) :
    return [
        sg.Text('', size=(2*SIZE, 3), text_color='pink', font=("Helvetica", 4*SIZE), key=tag+'Name'),
        sg.Text('', size=(8, 1), text_color='orange', font=('Helvetica', 4*SIZE), justification='center', key=tag+'Time'),
        sg.Text('', size=(8, 1), text_color='lightgreen', font=('Helvetica', 3*SIZE), justification='center', key=tag+'Solved')]

leftSide = [
    [sg.Text('Problem name', size=(3*SIZE, 1), text_color='white', font=("Helvetica", 3*SIZE)),
    sg.Text('Remainder time', size=(3*SIZE, 1), text_color='white', font=("Helvetica", 3*SIZE), justification='center'),
    sg.Text('solve rate', text_color='white', font=("Helvetica", 2*SIZE), justification='center') ] ,
    [sg.Text('_'*12*SIZE)],
    problem('up'),
    [sg.Text('_'*12*SIZE)],
    problem('mid'),
    [sg.Text('_'*12*SIZE)],
    problem('down'),
    [sg.Text('_'*12*SIZE)],
    [sg.RButton('Freeze', button_color=('white', 'purple'))], 
    [sg.Exit(button_color=('white', 'purple'))]
    ]

scoreBoardLayout = [[sg.Column(leftSide),
        sg.Column(rightSide, background_color='black' , size=(52*SIZE, 105*SIZE)),
        sg.Column(rightestSide, background_color='black', size=(48*SIZE, 105*SIZE))]] 

# ------------------------------------------------------------------

def nextProblem(problemSet, startTimes) :
    problemSet['up'] = problemSet['mid']
    startTimes['up'] = startTimes['mid']
    problemSet['mid'] = problemSet['down']
    startTimes['mid'] = startTimes['down']
    problemSet['down'] += 1
    startTimes['down'] = int(round(time.time() * 100))

    os.system('mpg123 ../voices/QtimeFinish.mp3')


scoreBoardWindow = sg.Window('Score Board', scoreBoardLayout, no_titlebar=True, auto_size_buttons=False, grab_anywhere=True) # keep_on_top=True
problemSet = {'up': START_PROBLEM_ID-1, 'mid': START_PROBLEM_ID, 'down': START_PROBLEM_ID+1}

startTimes = {'up': int(round(time.time() * 100) - (100*TIME_LIMIT)/3),\
            'mid': int(round(time.time() * 100) + 0 ),\
            'down': int(round(time.time() * 100) + (100*TIME_LIMIT)/3)}

def setStartTimes(last_time) :
    problemSet['up'] = START_PROBLEM_ID-1 + (last_time // TIME_LIMIT)
    problemSet['mid'] = START_PROBLEM_ID + (last_time // TIME_LIMIT)
    problemSet['down'] = START_PROBLEM_ID+1 + (last_time // TIME_LIMIT)
    startTimes['up'] -= last_time
    startTimes['mid'] -= last_time
    startTimes['down'] -= last_time

def updateScoreBoard(last_time) :
    groups = pd.read_csv("../db/groupsActivity.csv")
    problems = pd.read_csv("../db/problemHistory.csv")

    groups.sort_values(by=['point'], ascending=False, inplace=True, kind='mergesort'    )
    groups.reset_index(inplace=True)

    for index in range(groups.shape[0]) :
        scoreBoardWindow.Element('rank'+str(index)).Update(str(index+1)+'. '+groups['name'][index])
        scoreBoardWindow.Element('point'+str(index)).Update(groups['point'][index])
    
    nextProblem = False
    for tag in problemSet :
        if problemSet[tag] >= problems.shape[0] :
            continue
        scoreBoardWindow.Element(tag+'Name').Update(str(problemSet[tag]+1)+'. ')
        scoreBoardWindow.Element(tag+'Solved').Update(str(problems['solved_no'][problemSet[tag]]))
        
        remainderTime = TIME_LIMIT - (int(round(time.time() * 100)) - startTimes[tag]) // 100
        scoreBoardWindow.Element(tag+'Time').Update('{:02d}:{:02d}'.format((remainderTime) // 60, (remainderTime) % 60))
        if remainderTime <= 0 : nextProblem = True
    
    return nextProblem
                
def clearBoard() :
    for tag in problemSet :
        scoreBoardWindow.Element(tag+'Name').Update('')
        scoreBoardWindow.Element(tag+'Solved').Update('')
        scoreBoardWindow.Element(tag+'Time').Update('')


def scoreBoard(last_time) :   
    start = int(round(time.time() * 100)) - last_time
    freeze = False
    freezeTime = 0
    setStartTimes(last_time)
    os.system('mpg123 ../voices/Cstart.mp3')

    while (True):
        event, values = scoreBoardWindow.Read(timeout=1000)
        
        if event == 'Exit' :
            os._exit(True)
        
        elif event == 'Freeze' :
            if not freeze :
                updateScoreBoard(last_time)

                freezeTime = int(round(time.time() * 100))
            else :
                for tag in startTimes :
                    startTimes[tag] += int(round(time.time() * 100)) - freezeTime 
            freeze = not freeze
        
        if freeze : continue

        clearBoard()
        if updateScoreBoard(last_time) :
            nextProblem(problemSet, startTimes)

        last_time = int(round(time.time() * 100)) - start
        pd.DataFrame({'time':[last_time]}).to_csv("../db/time.csv", index=False)

    scoreBoardWindow.Close()    

last_time = pd.read_csv("../db/time.csv")['time'].values[0]
scoreBoard(last_time)
