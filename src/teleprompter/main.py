# importing csv module
import csv
from datetime import datetime
from datetime import timedelta
from datetime import timezone

# for command line arguments
import sys
if len(sys.argv) == 3:
    filename = sys.argv[1]
    query = sys.argv[2]
    # print(sys.argv[1])
# no input argument
else:
    filename = sys.argv[1]
    query =str(datetime.now().astimezone())

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("file", type=str, help="filepath")
# parser.add_argument("-d", "--datetime", required=False, type="str", default=str(datetime.now().astimezone()), help="the datetime")
# args = parser.parse_args()
# filename = args.file

print("query: ", query)

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
try:
    with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        # extracting field names through first row
        fields = next(csvreader)
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
except IOError:
    print("Error: can\'t find file or read data")

# Function to convert utcoffset into seconds
def utcoffset_to_seconds(time):
    hours = int(time[:2])
    if len(time) == 5:
        minutes = int(time.split(":")[1])
    elif len(time) == 4:
        minutes = int(time[2:])
    else:
        minutes = 0
    return hours*3600 + minutes*60


# compute start date of query in UTC (zero UTC offset)
second = 0
early = True

if query[len(query)-1] == 'Z':
    date = datetime.fromisoformat(query[:-1])
elif '+' in query:
    time = query.split("+")[1]
    second = utcoffset_to_seconds(time)
    date = datetime.fromisoformat(query.split("+")[0]) - timedelta(seconds=second)
else:
    # be careful, there are more than one "-"
    time = query.split("-")[3]
    second = utcoffset_to_seconds(time)
    date = datetime.fromisoformat(query.split("+")[0]) + timedelta(seconds=second)
    early = False

#date = date.replace(tzinfo=timezone.utc)
date = date.replace(tzinfo=None)
print("date: ", date)

check = "" + str(date.day) + "/" + str(date.month) + "/" + str(date.year)[2:]
print("check: ", check)

for i in range(0, len(rows)):
    # parsing each column of a row
    # print("row: ", rows[i])
    if (rows[i][2] == check):
        # print("rows[i][2]: ", rows[i][2])
        year = int("20"+rows[i][2].split("/")[2])
        month = int(rows[i][2].split("/")[1])
        day = int(rows[i][2].split("/")[0])

        candidate_start = datetime(year, month, day, int(rows[i][3].split(":")[0]), int(rows[i][3].split(":")[1]))
        offset = timedelta(seconds=int(rows[i][4]))
        candidate_end = candidate_start + offset

        # print("start: ", candidate_start)
        # print("end: ",candidate_end)
        if (date >= candidate_start and date < candidate_end):
            if early:
                endtime = str((candidate_end + timedelta(seconds=second)).time())
            else:
                endtime = str((candidate_end - timedelta(seconds=second)).time())
            res = "[" + endtime[:5] + "]" + " That was " + rows[i][0] + ", up next is " + rows[i + 1][0]
            res = res + " which is rated " + rows[i + 1][1] + " and coming up later is " + rows[i + 2][0] + "."
            print(res)
            break