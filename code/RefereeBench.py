import PySimpleGUI as sg      
import numpy as np
from os import _exit
import threading
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
measurer = np.vectorize(len)

groups = pd.read_csv("../CSVs/groups.csv", usecols=['name'])['name'].values.tolist()
problems = pd.read_csv("../CSVs/problems.csv", usecols=['id'])['id'].values.tolist()

sg.ChangeLookAndFeel('Black')

homeLayout = [
    [sg.Listbox(values=(groups), size=(15, 15), font=("Helvetica", 20), key='__groupname__'),
        sg.Listbox(values=(problems), size=(15, 15), font=("Helvetica", 20), key='__problemNumber__')],
    [sg.Exit(button_color=('white', 'purple')),
        sg.RButton('Accept!', button_color=('white', 'green'), size = (25, 1)),
        sg.RButton('Reject!', button_color=('white', 'red'), size = (25, 1))]
        
]

def solved(groupName, tag) :
    if groupName not in groups :
        return 'Wrong group name!'

    if tag not in problems :
        return 'This problem dosen\'t exist'

    groupsActivity = pd.read_csv("../db/groupsActivity.csv")
    thisGroupActivity = json.loads(groupsActivity[groupsActivity['name']==groupName]['problems'].values[0])
    if tag in  thisGroupActivity:
        return 'This problem is already solved for you!'
    
    thisGroupActivity.append(tag)
    groupsActivity['problems'][groupsActivity['name']==groupName] = json.dumps(thisGroupActivity)
    groupsActivity['point'][groupsActivity['name']==groupName] += 1
    groupsActivity.to_csv("../db/groupsActivity.csv",index=False)

    problemHistory = pd.read_csv("../db/problemHistory.csv")
    thisProblemHistory = json.loads(problemHistory[problemHistory['id']==tag]['solvers'].values[0])
    thisProblemHistory.append(groupName)
    problemHistory['solvers'][problemHistory['id']==tag] = json.dumps(thisProblemHistory)
    problemHistory['solved_no'][problemHistory['id']==tag] += 1
    problemHistory.to_csv("../db/problemHistory.csv",index=False)

    return 'Done'

def reject(groupName, tag):
    if groupName not in groups :
        return 'Wrong group name!'
    groupsActivity = pd.read_csv("../db/groupsActivity.csv")
    thisGroupActivity = json.loads(groupsActivity[groupsActivity['name']==groupName]['problems'].values[0])
    if tag not in problems :
        return 'This problem dosen\'t exist'
    if tag not in thisGroupActivity:
        return 'Invalid input'

    thisGroupActivity.remove(tag)
    groupsActivity['problems'][groupsActivity['name']==groupName] = json.dumps(thisGroupActivity)
    groupsActivity['point'][groupsActivity['name']==groupName] -= 1
    groupsActivity.to_csv("../db/groupsActivity.csv",index=False)

    problemHistory = pd.read_csv("../db/problemHistory.csv")
    thisProblemHistory = json.loads(problemHistory[problemHistory['id']==tag]['solvers'].values[0])
    thisProblemHistory.remove(groupName)
    problemHistory['solvers'][problemHistory['id']==tag] = json.dumps(thisProblemHistory)
    problemHistory['solved_no'][problemHistory['id']==tag] -= 1
    problemHistory.to_csv("../db/problemHistory.csv",index=False)

    return 'Done'


homeWindow = sg.Window('Home', background_color='black').Layout(homeLayout)

def refereeBench() :
    while True:
        event, values = homeWindow.Read(timeout=200)
        if event is None or event == 'Exit':
            homeWindow.Close()
            _exit(True)
            break

        elif event == 'Reject!':
            if(len(values['__groupname__']) != 0 and len(values['__problemNumber__']) != 0):
                sg.Popup(reject(values['__groupname__'][0], values['__problemNumber__'][0]), font=("Helvetica", 20))
            else:
                sg.Popup('Invalid input!', font=("Helvetica", 20))


        elif event == 'Accept!':
            if(len(values['__groupname__']) != 0 and len(values['__problemNumber__']) != 0):
                sg.Popup(solved(values['__groupname__'][0], values['__problemNumber__'][0]), font=("Helvetica", 20))
            else:
                sg.Popup('Invalid input!', font=("Helvetica", 20))
    homeWindow.Close()
refereeBench()