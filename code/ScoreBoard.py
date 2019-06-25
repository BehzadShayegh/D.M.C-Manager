import PySimpleGUI as sg
import time
import numpy as np
import os
import json
measurer = np.vectorize(len)

TIME_LIMIT = 3*10
START_PROBLEM_ID = 1

with open("../Jasons/GroupsJson.txt","r") as groupFile :
    groupPoints, groupNames = json.load(groupFile)
groupsNumber = len(groupPoints)
maximumGroupNameLenght = max(measurer(groupNames))

with open("../Jasons/ProblemsJson.txt","r") as problemFile :
    problemNames, problemsSolved = json.load(problemFile)
problemsNumber = len(problemsSolved)
maximumProblemNameLenght = max(measurer(problemNames))

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
    [sg.Text(str(index+1)+'. '+groupNames[index], size=(2*maximumGroupNameLenght, 1), text_color=rankColor(index), background_color='black', font=("Helvetica", 37), key='rank'+str(index)),
    sg.Text(groupPoints[index], justification='right', text_color=rankColor(index), background_color='black', font=("Helvetica", 37), key='point'+str(index))]
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

# ------------------------------------------------------------------

def nextProblem(problemSet, startTimes) :
    problemSet['easy'] = problemSet['normal']
    startTimes['easy'] = startTimes['normal']
    problemSet['normal'] = problemSet['hard']
    startTimes['normal'] = startTimes['hard']
    problemSet['hard'] += 1
    startTimes['hard'] = int(round(time.time() * 100))
    
    with open("../Jasons/ProblemSet.txt","w") as f :
        f.write(json.dumps(problemSet))

    os.system('mpg123 ../voices/QtimeFinish.mp3')


scoreBoardWindow = sg.Window('Score Board', scoreBoardLayout, no_titlebar=True, auto_size_buttons=False, grab_anywhere=True) # keep_on_top=True
problemSet = {'easy': START_PROBLEM_ID-1, 'normal': START_PROBLEM_ID, 'hard': START_PROBLEM_ID+1}

startTimes = {'easy': int(round(time.time() * 100) - (100*TIME_LIMIT)/3),\
            'normal': int(round(time.time() * 100) + 0 ),\
            'hard': int(round(time.time() * 100) + (100*TIME_LIMIT)/3)}

with open("../Jasons/ProblemSet.txt","w") as f :
    f.write(json.dumps(problemSet))

def updateScoreBoard() :
    with open("../Jasons/GroupsJson.txt","r") as groupFile :
        groupPoints, groupNames = json.load(groupFile)
    with open("../Jasons/ProblemsJson.txt","r") as problemFile :
        problemNames, problemsSolved = json.load(problemFile)

    for index in range(groupsNumber) :
        scoreBoardWindow.Element('rank'+str(index)).Update(str(index+1)+'. '+groupNames[index])
        scoreBoardWindow.Element('point'+str(index)).Update(groupPoints[index])
    
    nextProblem = False
    for tag in problemSet :
        if problemSet[tag] >= problemsNumber :
            continue
        scoreBoardWindow.Element(tag+'Name').Update(str(problemSet[tag]+1)+'. '+problemNames[problemSet[tag]])
        scoreBoardWindow.Element(tag+'Solved').Update(str(problemsSolved[problemSet[tag]]))
        
        remainderTime = TIME_LIMIT - (int(round(time.time() * 100)) - startTimes[tag]) // 100
        scoreBoardWindow.Element(tag+'Time').Update('{:02d}:{:02d}'.format((remainderTime) // 60, (remainderTime) % 60))
        if remainderTime <= 0 : nextProblem = True
    
    return nextProblem
                
def clearBoard() :
    for tag in problemSet :
        scoreBoardWindow.Element(tag+'Name').Update('')
        scoreBoardWindow.Element(tag+'Solved').Update('')
        scoreBoardWindow.Element(tag+'Time').Update('')


def scoreBoard() :    
    freeze = False
    freezeTime = 0
    timer = 1

    os.system('mpg123 ../voices/Cstart.mp3')

    while (True):
        # try :
            event, values = scoreBoardWindow.Read(timeout=1000)
            
            if event == 'Exit' :
                os._exit(True)

            if not os.path.exists('../Jasons/ProblemSet.txt') :
                continue
            
            elif event == 'Freeze' :
                if not freeze :
                    updateScoreBoard()

                    freezeTime = int(round(time.time() * 100))
                else :
                    for tag in startTimes :
                        startTimes[tag] += int(round(time.time() * 100)) - freezeTime 
                freeze = not freeze
            
            if freeze : continue

            clearBoard()
            if updateScoreBoard() :
                nextProblem(problemSet, startTimes)

        # except :
        #     pass
    scoreBoardWindow.Close()    

scoreBoard()