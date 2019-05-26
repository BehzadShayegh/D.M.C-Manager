import csv

problemsPath = './problems.csv'

problems = []
print('problems! format:')
print('id/name/subject/level')
print('------------------------------')
while(True) :
    problem = input().split('/')
    if problem[0] == '-' : break
    problems.append(problem)

with open(problemsPath, 'w') as problemsCsv:
    problemsCsv.write("%s,%s,%s,%s\n"%('id','name','subject','level'))
    for id,name,subject,level in problems :
        problemsCsv.write("%s,%s,%s,%s\n"%(id,name,subject,level))
