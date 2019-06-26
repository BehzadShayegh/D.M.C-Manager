from pandas import DataFrame, read_csv
import pandas as pd
import json

groupsPath = '../CSVs/groups.csv'
groupsCsv = pd.read_csv(groupsPath)
groupNames = groupsCsv['name'].tolist()
groupPoints = groupsCsv['point'].tolist()

problemsPath = '../CSVs/problems.csv'
problemsCsv = pd.read_csv(problemsPath)
problemNames = problemsCsv['name'].tolist()
problemsSolved = problemsCsv['solved'].tolist()

with open("../Jasons/GroupsJson.txt","r") as groupFile :
    groupPoints, groupNames = json.load(groupFile)

with open("../Jasons/ProblemsJson.txt","r") as problemFile :
    problemNames, problemsSolved = json.load(problemFile)

groupsInfo = {'id': range(1, len(groupPoints)+1),
        'name': groupNames,
        'point': groupPoints }

problemsInfo = {'id': range(1, len(problemsSolved)+1),
        'name': problemNames,
        'solved': problemsSolved }

export_csv = DataFrame(groupsInfo, columns= ['id', 'name', 'point'])\
            .to_csv(groupsPath, index = None, header=True)

export_csv = DataFrame(problemsInfo, columns= ['id', 'name', 'solved'])\
            .to_csv(problemsPath, index = None, header=True)