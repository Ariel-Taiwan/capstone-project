import csv
import os


filename = input('Input the csv file name: ')
input_directory = os.path.abspath("./input") + '/urls/' + filename
domains = []

with open(input_directory) as file:
    rows = csv.reader(file)

    for row in rows:
        url = row[0].split("/")     # extract the domain
        domains.append(url[2])


output_directory = os.path.abspath("./input") + '/domains/' + (filename.split("."))[0] + '_domain.csv'

with open(output_directory, 'w') as output_file:
    writer = csv.writer(output_file)
    
    for domain in domains:
        writer.writerow([domain])

# output_directory = os.path.abspath('./output/') 

# if not os.path.isdir(output_directory):
#   os.makedirs(output_directory)

# output_filename = output_directory + "/" + str(interval) + '_' + filename
# output_report = output_directory + "/" + str(interval) + '_report.txt'

# report_file = open(output_report, 'a')