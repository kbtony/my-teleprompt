# importing csv module
import csv
# for command line arguments
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone

USAGE = f"usage: python {sys.argv[0]} filename datetime"

class CommandLine:
    def __init__(self):
        # More than two cmd arguments
        if len(sys.argv) > 3:
            print("error: at most two command line arguments")
            raise SystemExit(USAGE)
        # Two arguments: filename, datetime
        elif len(sys.argv) == 3:
            self.filename = sys.argv[1]
            self.query = sys.argv[2]
        # One argument: filename
        elif len(sys.argv) == 2:
            self.filename = sys.argv[1]
            self.query = str(datetime.now().astimezone())
        # No arguments
        else:
            print("error: the following arguments are required: filename")
            raise SystemExit(USAGE)

# Function to read the input csv file
def read_file(filename):
    fields = []
    rows = []
    try:
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            # extracting field names through first row
            fields = next(csvreader)
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
            return rows
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

# Generate a datetime object for query in UTC (zero UTC offset)
class Query(object):
    def __init__(self, query):
        # record the timezone (before or after UTC)
        self.early = True
        # record the UTC offset in seconds
        self.second = 0

        if query[len(query) - 1] == 'Z':
            self.date = datetime.fromisoformat(query[:-1])
        elif '+' in query:
            self.time = query.split("+")[1]
            self.second = utcoffset_to_seconds(self.time)
            self.date = datetime.fromisoformat(query.split("+")[0]) - timedelta(seconds=self.second)
        else:
            # be careful, there are more than one "-"
            self.time = query.split("-")[3]
            self.second = utcoffset_to_seconds(self.time)
            self.date = datetime.fromisoformat(query.split("+")[0]) + timedelta(seconds=self.second)
            self.early = False

        self.date = self.date.replace(tzinfo=None)
        self.check = "" + str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year)[2:]


def final_fnc(rows, date, check, second, early):
    for i in range(0, len(rows)):
        # parsing each column of a row
        if (rows[i][2] == check):
            year = int("20" + rows[i][2].split("/")[2])
            month = int(rows[i][2].split("/")[1])
            day = int(rows[i][2].split("/")[0])

            candidate_start = datetime(year, month, day, int(rows[i][3].split(":")[0]), int(rows[i][3].split(":")[1]))
            offset = timedelta(seconds=int(rows[i][4]))
            candidate_end = candidate_start + offset

            if (date >= candidate_start and date < candidate_end):
                if early:
                    endtime = str((candidate_end + timedelta(seconds=second)).time())
                else:
                    endtime = str((candidate_end - timedelta(seconds=second)).time())
                res = "[" + endtime[:5] + "]" + " That was " + rows[i][0] + ", up next is " + rows[i + 1][0]
                res = res + " which is rated " + rows[i + 1][1] + " and coming up later is " + rows[i + 2][0] + "."
                print(res)
                break

def main():
    user_input = CommandLine()
    program_list = read_file(user_input.filename)
    my_query = Query(user_input.query)
    final_fnc(program_list, my_query.date, my_query.check, my_query.second, my_query.early)

if __name__=="__main__":
    main()
