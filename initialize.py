import pandas as pd
import json

groupsActivity = pd.read_csv("./CSVs/groups.csv")
problemHistory = pd.read_csv("./CSVs/problems.csv")

groupsActivity['problems'] = json.dumps([]*groupsActivity.shape[0])
problemHistory['solvers'] = json.dumps([]*problemHistory.shape[0])
groupsActivity['point'] = 0
problemHistory['solved_no'] = 0

groupsActivity.to_csv("./db/groupsActivity.csv", index=False)
problemHistory.to_csv("./db/problemHistory.csv", index=False)
pd.DataFrame({'time':[0]}).to_csv("./db/time.csv", index=False)