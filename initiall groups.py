import csv

groupsPath = './groups.csv'

print('groups! format :')
print('group name')
print('first member/second member/...')
print('------------------------------')
groups = {}
while(True) :
    groupName = input()
    if groupName == '-' : break
    members = input()
    groups[groupName] = members

with open(groupsPath, 'w') as groupsCsv:
    groupsCsv.write("%s,%s,%s,%s,%s,%s\n"%('id','name','members','point','ticket','dicLimit'))
    id = 0
    for name, members in groups.items() :
        id += 1
        groupsCsv.write("%s,%s,%s,%d,%d,%d\n"%(id,name,members,0,3,10))
