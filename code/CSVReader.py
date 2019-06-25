from pandas import DataFrame, read_csv
import pandas as pd
import json
import os

os.system('mkdir ../Jasons/')

groupsPath = '../CSVs/groups.csv'
groupsCsv = pd.read_csv(groupsPath)
groupNames = groupsCsv['name'].tolist()
groupPoints = groupsCsv['point'].tolist()

problemsPath = '../CSVs/problems.csv'
problemsCsv = pd.read_csv(problemsPath)
problemNames = problemsCsv['name'].tolist()
problemsSolved = problemsCsv['solved'].tolist()

with open("../Jasons/GroupsJson.txt","w") as f :
    f.write(json.dumps(list(zip(*(reversed(sorted(zip(groupPoints, groupNames))))))))

with open("../Jasons/ProblemsJson.txt","w") as f :
    f.write(json.dumps([problemNames, problemsSolved]))