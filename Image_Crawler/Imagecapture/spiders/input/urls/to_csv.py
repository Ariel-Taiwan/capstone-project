import csv
import json
  
employee_info = ['_id', 'category', 'layer', 'indomain', 'urls']
  
#new_dict = [

#]

student_id = []
fo = open('cat8_insert.csv','r')
#line = fo.read()
for line in fo.readlines():                          #依次读取每行  
    js = json.loads(line)
    line = line.strip()
    student_id.append(js)

#print(student_id)
#print(type(fo))
#line = '[' + line + ']'

with open('cat8.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = employee_info)
    #print(type(line))
    #print(line)
    writer.writeheader()
    writer.writerows(student_id)

fo.close()
