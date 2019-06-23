import PySimpleGUI as sg      
from pandas import DataFrame, read_csv
import pandas as pd
import time
import numpy as np
from os import _exit
import threading
measurer = np.vectorize(len)

TIME_LIMIT = 3*10

groupsPath = './groups.csv'
groupsCsv = pd.read_csv(groupsPath)
groupNames = groupsCsv['name'].tolist()
groupPoints = groupsCsv['point'].tolist()
groupsNumber = len(groupPoints)
maximumGroupNameLenght = max(measurer(groupNames))

problemsPath = './problems.csv'
problemsCsv = pd.read_csv(problemsPath)
problemIds = problemsCsv['id'].tolist()
problemNames = problemsCsv['name'].tolist()
problemsSolved = problemsCsv['solved'].tolist()
problemsNumber = len(problemIds)
maximumProblemNameLenght = max(measurer(problemNames))

sg.ChangeLookAndFeel('Dark')      

# SCORE BOARD ......................

rightSide = [
    [sg.Text(str(index+1)+'. '+groupNames[index], size=(2*maximumGroupNameLenght, 1), text_color='white', background_color='black', font=("Helvetica", 37), key='rank'+str(index)),
    sg.Text(groupPoints[index], justification='right', text_color='white', background_color='black', font=("Helvetica", 37), key='point'+str(index))]
    for index in range(15) ]
rightestSide = [
    [sg.Text(str(index+1)+'. '+groupNames[index], size=(2*maximumGroupNameLenght, 1), text_color='white', background_color='black', key='rank'+str(index)),
    sg.Text(groupPoints[index], justification='right', text_color='white', background_color='black', key='point'+str(index))]
    for index in range(15, groupsNumber) ]

def problem(tag) :
    return [
        sg.Text('', size=(2*maximumProblemNameLenght, 3), text_color='pink', font=("Helvetica", 50), key=tag+'Name'),
        sg.Text('', size=(8, 1), text_color='orange', font=('Helvetica', 60), justification='center', key=tag+'Time'),
        sg.Text('', size=(8, 1), text_color='lightgreen', font=('Helvetica', 40), justification='center', key=tag+'Solved')]

leftSide = [
    [sg.Text('     Problem name', size=(20, 1), text_color='white', font=("Helvetica", 30)),
    sg.Text('Remainder time', size=(20, 1), text_color='white', font=("Helvetica", 30), justification='center'),
    sg.Text('solve rate', text_color='white', font=("Helvetica", 20), justification='center') ] ,
    [sg.Text('_'*150)],
    problem('easy'),
    [sg.Text('_'*150)],
    problem('normal'),
    [sg.Text('_'*150)],
    problem('hard'),
    [sg.Text('_'*150)],
    [sg.RButton('Freeze', button_color=('white', 'purple')), 
    sg.Text('Programmed by B.Shayegh. Github : https://github.com/BehzadShayegh/DMC')],
    [sg.Exit(button_color=('white', 'purple'))]
    ]

scoreBoardLayout = [[sg.Column(leftSide),
        sg.Column(rightSide, background_color='black'),
        sg.Column(rightestSide, background_color='black')]]  

def nextProblem(problemSet, startTimes) :
    problemSet['easy'] = problemSet['normal']
    startTimes['easy'] = startTimes['normal']
    problemSet['normal'] = problemSet['hard']
    startTimes['normal'] = startTimes['hard']
    problemSet['hard'] += 1
    startTimes['hard'] = int(round(time.time() * 100))




scoreBoardWindow = sg.Window('Score Board', scoreBoardLayout, no_titlebar=True, auto_size_buttons=False, grab_anywhere=True) # keep_on_top=True
problemSet = {'easy': 0, 'normal': 1, 'hard': 2}

def scoreBoard() :
    startTimes = {'easy': int(round(time.time() * 100) - (100*TIME_LIMIT)/3),\
                'normal': int(round(time.time() * 100) + 0 ),\
                'hard': int(round(time.time() * 100) + (100*TIME_LIMIT)/3)}
    
    freeze = False
    freezeTime = 0

    while (True):
        try :
            event, values = scoreBoardWindow.Read(timeout=200)
            
            if event == 'Exit' :
                _exit(True)
                break
            
            elif event == 'Freeze' :
                if not freeze :
                    updateScoreBoard(groupPoints, groupNames)

                    freezeTime = int(round(time.time() * 100))
                else :
                    for tag in startTimes :
                        startTimes[tag] += int(round(time.time() * 100)) - freezeTime 
                freeze = not freeze
            
            if freeze : continue

            needNextProblem = False

            for tag in problemSet :
                if problemSet[tag] >= problemsNumber :
                    scoreBoardWindow.Element(tag+'Name').Update('')
                    scoreBoardWindow.Element(tag+'Solved').Update('')
                    scoreBoardWindow.Element(tag+'Time').Update('')
                    continue

                scoreBoardWindow.Element(tag+'Name').Update(str(problemSet[tag]+1)+'. '+problemNames[problemSet[tag]])

                remainderTime = TIME_LIMIT - (int(round(time.time() * 100)) - startTimes[tag]) // 100
                scoreBoardWindow.Element(tag+'Time').Update('{:02d}:{:02d}'.format((remainderTime) // 60, (remainderTime) % 60))
                if remainderTime <= 0 : needNextProblem = True

                scoreBoardWindow.Element(tag+'Solved').Update(str(problemsSolved[problemSet[tag]]))

            if needNextProblem : nextProblem(problemSet, startTimes)
        except :
            pass
    scoreBoardWindow.Close()    

def updateScoreBoard(groupPoints, groupNames, scoreBoardWindow=scoreBoardWindow) :
    groupPoints, groupNames = list(zip(*( reversed(sorted(zip(groupPoints, groupNames))) )))
    for index in range(groupsNumber) :
        scoreBoardWindow.Element('rank'+str(index)).Update(groupNames[index])
        scoreBoardWindow.Element('point'+str(index)).Update(groupPoints[index])
    
# REFEREE BENCH .................................... 

homeLayout = [
    [sg.Text('Enter group name:', text_color='white', background_color='black', font=("Helvetica", 15)),
    sg.Input(background_color='purple', font=("Helvetica", 15), size=(2*maximumGroupNameLenght,1))],
    [sg.Text('_'*35, background_color='black')],    
    [sg.RButton('easy problem solved!', button_color=('white', 'darkgreen'), size = (30, 1))],
    [sg.RButton('normal problem solved!', button_color=('white', 'darkgreen'), size = (30, 1))],
    [sg.RButton('hard problem solved!', button_color=('white', 'darkgreen'), size = (30, 1))],
    [sg.RButton('extra problem solved!', button_color=('white', 'darkblue'), size = (30, 1))],
    [sg.Exit(button_color=('white', 'black'))]
    ]

def solved(groupName, tag) :
    if groupName not in groupNames :
        return False
    
    groupPoints[groupNames.index(groupName)] += 1
    if tag != 'extra' :
        problemsSolved[problemSet[tag]] += 1
    
    updateScoreBoard(groupPoints, groupNames)

    return True



homeWindow = sg.Window('Home', background_color='black').Layout(homeLayout)

def refereeBench() :
    while True:
        try :
            event, values = homeWindow.Read(timeout=200)
            if event is None or event == 'Exit':   
                _exit(True)   
                break

            elif len(event.split()) > 2 and event.split()[2] == 'solved!' :
                solved(values[0], event.split()[0])
            
        except :
            pass

    homeWindow.Close()
# ................................................................

threading.Thread(target=refereeBench).start()
time.sleep(1)
threading.Thread(target=scoreBoard).start()