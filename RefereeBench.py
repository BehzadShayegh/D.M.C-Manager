import PySimpleGUI as sg      
import numpy as np
from os import _exit
import threading
import json
measurer = np.vectorize(len)

with open("GroupsJson.txt","r") as groupFile :
    groupPoints, groupNames = json.load(groupFile)
groupsNumber = len(groupPoints)
maximumGroupNameLenght = max(measurer(groupNames))

with open("ProblemsJson.txt","r") as problemFile :
    problemNames, problemsSolved = json.load(problemFile)
problemsNumber = len(problemsSolved)
maximumProblemNameLenght = max(measurer(problemNames))

problemsHistory = {}
for pid in range(problemsNumber) :
    problemsHistory[pid] = []
with open("problemsHistory.txt","w") as phf :
    phf.write(json.dumps(problemsHistory))

# INTERFACE

sg.ChangeLookAndFeel('Black')

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
    problemSet = {}
    with open("ProblemSet.txt","r") as f :
        problemSet = json.load(f)

    if groupName not in groupNames :
        return 'Wrong group name!'

    if problemSet[tag] >= problemsNumber :
        return 'This problem dosen\'t exist anymore!'
    
    if tag != 'extra' :
        if groupName in problemsHistory[problemSet[tag]] :
            return 'This problem is already solved for you!'
    
    groupPoints[groupNames.index(groupName)] += 1
    with open("GroupsJson.txt","w") as groupFile :
        groupFile.write(json.dumps(list(zip(*(reversed(sorted(zip(groupPoints, groupNames))))))))
    
    if tag != 'extra' :
        problemsSolved[problemSet[tag]] += 1
        with open("ProblemsJson.txt","w") as problemFile :
            problemFile.write(json.dumps([problemNames, problemsSolved]))
        problemsHistory[problemSet[tag]].append(groupName)
    
    with open("problemsHistory.txt","w") as phf :
        phf.write(json.dumps(problemsHistory))

    return 'Done'


homeWindow = sg.Window('Home', background_color='black').Layout(homeLayout)

def refereeBench() :
    while True:
        # try :
            event, values = homeWindow.Read(timeout=200)
            if event is None or event == 'Exit':   
                _exit(True)   
                break

            elif len(event.split()) > 2 and event.split()[2] == 'solved!' :
                sg.Popup(solved(values[0], event.split()[0]), font=("Helvetica", 20))
            
        # except :
        #     pass

    homeWindow.Close()

refereeBench()