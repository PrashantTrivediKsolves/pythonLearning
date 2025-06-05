import csv

# csv.reader: Reading CSV as Lists

with open('csvdata.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)



# csv.DictReader: Reading CSV as Dictionaries ............................  .


# Each row is returned as an OrderedDict or regular dict where headers become keys.


with open('csvdata.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)



# 3 . csv.writer: Writing CSV

data = [
    ['name', 'age', 'city'],
    ['Charlie', 35, 'Chicago'],
    ['Diana', 28, 'Houston']
]

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# writer.writerow(row) → Writes a single row.

# writer.writerows(list_of_rows) → Writes multiple rows.



# 4 . csv.DictWriter: Writing CSV from dictionaries

# import csv

data = [
    {'name': 'Eve', 'age': 22, 'city': 'Boston'},
    {'name': 'Frank', 'age': 40, 'city': 'Seattle'}
]

with open('dict_output.csv', mode='w', newline='') as file:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()         # Write column names
    writer.writerows(data)       # Write rows as dictionaries


# Quick Recap
# Feature	Purpose
# csv.reader	Read CSV file as a list of lists
# csv.DictReader	Read CSV file as a list of dictionaries
# csv.writer	Write rows to CSV using lists
# csv.DictWriter	Write rows to CSV using dictionary




