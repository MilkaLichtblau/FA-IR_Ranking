import csv
import sys

inFile = sys.argv[1]
outFile = sys.argv[2]
query_id = int(sys.argv[3])

with open(inFile, 'r') as fin, open(outFile, 'w', newline='') as fout:

    # define reader and writer objects
    reader = csv.reader(fin, skipinitialspace=True)
    writer = csv.writer(fout, delimiter=',')

    # iterate and write rows based on condition
    for i in reader:
        if int(i[0]) == query_id:
            writer.writerow(i)
