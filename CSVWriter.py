from pandas import DataFrame, read_csv
import pandas as pd
import json

groupsPath = './groups.csv'
groupsCsv = pd.read_csv(groupsPath)
groupNames = groupsCsv['name'].tolist()
groupPoints = groupsCsv['point'].tolist()

problemsPath = './problems.csv'
problemsCsv = pd.read_csv(problemsPath)
problemIds = problemsCsv['id'].tolist()
problemNames = problemsCsv['name'].tolist()
problemsSolved = problemsCsv['solved'].tolist()

with open("GroupsJson.txt","r") as groupFile :
    groupPoints, groupNames = json.load(groupFile)

with open("ProblemsJson.txt","r") as problemFile :
    problemIds, problemNames, problemsSolved = json.load(problemFile)

groupsInfo = {'id': range(1, len(groupPoints)+1),
        'name': groupNames,
        'point': groupPoints }

problemsInfo = {'id': problemIds,
        'name': problemNames,
        'solved': problemsSolved }

export_csv = DataFrame(groupsInfo, columns= ['id', 'name', 'point'])\
            .to_csv(groupsPath, index = None, header=True)

export_csv = DataFrame(problemsInfo, columns= ['id', 'name', 'solved'])\
            .to_csv(problemsPath, index = None, header=True)