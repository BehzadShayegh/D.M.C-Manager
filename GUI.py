import PySimpleGUI as sg
from pandas import DataFrame, read_csv
import pandas as pd
import csv



groupsPath = './groups.csv'
groupsCsv = pd.read_csv(groupsPath)
groupNames = groupsCsv['name'].tolist()
groupMems = groupsCsv['members'].tolist()
groupPoints = groupsCsv['point'].tolist()
groupTickets = groupsCsv['ticket'].tolist()
groupDicLimit = groupsCsv['dicLimit'].tolist()
groupsNumber = len(groupPoints)

problemsPath = './problems.csv'
problemsCsv = pd.read_csv(problemsPath)
problemIds = problemsCsv['id'].tolist()
problemNames = problemsCsv['name'].tolist()
problemSubjects = problemsCsv['subject'].tolist()
problemLevels = problemsCsv['level'].tolist()
problemsNumber = len(problemIds)



homeLayout = [[sg.Text('Enter group ID:')],      
          [sg.Input()],
          [sg.Text('Enter question ID:')],      
          [sg.Input()],
          [sg.RButton('Get', button_color=('white', 'yellow')), sg.RButton('Solve', button_color=('white', 'green')), sg.RButton('Dissolve', button_color=('white', 'red'))],
          [sg.RButton('Status'), sg.Exit(button_color=('white', 'black'))]]      

getQuestionLayout = [[sg.Text('Enter question subject:')],      
          [sg.Input()],
          [sg.Text('Enter question level:')],      
          [sg.Input()],
          [sg.RButton('Apply'), sg.Exit(button_color=('white', 'black'))]]      



def findStatus(groupId, questionId) :
    if questionId not in problemIds :
        return 'undifined question'
    if groupId-1 not in range(groupsNumber) :
        return 'undifined group'

    statusPath = './statuses/'+str(groupId)+'.csv'
    statusCsv = pd.read_csv(statusPath)
    statuses = statusCsv['status'].tolist()
    return statuses[problemIds.index(questionId)]




def update() :
    groupsInfo = {'id': range(1, groupsNumber+1),
            'name': groupNames,
            'members': groupMems,
            'point': groupPoints,
            'ticket': groupTickets,
            'dicLimit': groupDicLimit
            }
    df = DataFrame(groupsInfo, columns= ['id', 'name', 'members', 'point', 'ticket', 'dicLimit'])
    export_csv = df.to_csv(groupsPath, index = None, header=True)




def updateStatus(groupId, problemIndex, newStatus) :
    statusPath = './statuses/'+str(groupId)+'.csv'
    statusCsv = pd.read_csv(statusPath)
    statuses = statusCsv['status'].tolist()
    statuses[problemIndex] = newStatus

    statusInfo = {'problemId': problemIds,
            'status': statuses,
            }
    df = DataFrame(statusInfo, columns= ['problemId', 'status'])
    export_csv = df.to_csv(statusPath, index = None, header=True)



def solve(groupId, questionId) :
    status = findStatus(groupId, questionId)
    if status != 'read' :
        return status
    
    problemIndex = problemIds.index(questionId)
    pointPlus = problemLevels[problemIndex]
    groupPoints[groupId-1] += pointPlus*pointPlus - pointPlus + 1
    groupTickets[groupId-1] += 1
    update()
    updateStatus(groupId, problemIndex, 'solved')
    return 'Done!'


def dissolve(groupId, questionId) :
    status = findStatus(groupId, questionId)
    if status != 'read' :
        return status
    if groupDicLimit[groupId-1] <= 0 :
        return 'Dissolve Limit Error!!!'

    problemIndex = problemIds.index(questionId)
    groupTickets[groupId-1] += 1
    groupDicLimit[groupId-1] -= 1
    update()
    updateStatus(groupId, problemIndex, 'dissolved')
    return 'Done!'

    

def getQuestion(groupId) :
    getQuestionWindow = sg.Window('Gqt Question').Layout(getQuestionLayout)  

    while True:
        try :
            event, values = getQuestionWindow.Read()  
            if event is None or event == 'Exit': 
                getQuestionWindow.Close()     
                return 'ok'
            
            if groupId-1 not in range(groupsNumber) :
                getQuestionWindow.Close()
                return 'undifined group'

            subject, level = values[0], int(values[1])
            if subject == '' : continue

            for index in range(problemsNumber) :
                if problemSubjects[index] == subject and problemLevels[index] == level\
                    and findStatus(groupId, problemIds[index]) == 'not read' :
                    
                    groupTickets[groupId-1] -= 1
                    update()
                    updateStatus(groupId, index+1, 'read')
                    getQuestionWindow.Close()
                    return 'Done!'

            return 'You cann\'t choose this type any more ...'
            
        except :
            pass





homeWindow = sg.Window('Home').Layout(homeLayout)

while True:

    try :
        event, values = homeWindow.Read()      
        if event is None or event == 'Exit':      
            break
        
        elif event == 'Get' :
            groupId = int(values[0])
            sg.Popup(getQuestion(groupId))

        elif event == 'Status' :
            groupId, questionId = int(values[0]), int(values[1])
            sg.Popup(findStatus(groupId, questionId))

        elif event == 'Solve' :
            groupId, questionId = int(values[0]), int(values[1])
            sg.Popup(solve(groupId, questionId))

        elif event == 'Dissolve' :
            groupId, questionId = int(values[0]), int(values[1])
            sg.Popup(dissolve(groupId, questionId))

    except :
        pass

homeWindow.Close()