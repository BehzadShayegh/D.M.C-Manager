from pandas import DataFrame, read_csv
import pandas as pd
import csv

problemsPath = './problems.csv'
groupsPath = './groups.csv'

groupsCsv = pd.read_csv(groupsPath)
groupIds = groupsCsv['id']
problemsCsv = pd.read_csv(problemsPath)
problemIds = problemsCsv['id']

for groupId in groupIds :
    statusPath = './statuses/'+str(groupId)+'.csv'
    with open(statusPath, 'w') as statusCsv :
        statusCsv.write("%s,%s\n"%('problemId','status'))
        for problemId in problemIds :
            statusCsv.write("%s,%s\n"%(problemId,'not read'))