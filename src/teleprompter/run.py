import csv
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone

USAGE = f"usage: python {sys.argv[0]} file_name.csv datetime"

class CommandLine:
    def __init__(self, argv):
        # More than two cmd arguments
        if len(argv) > 3:
            print("error: at most two command line arguments")
            raise SystemExit(USAGE)
        # Two cmd arguments: filename, datetime
        elif len(argv) == 3:
            self.filename = argv[1]
            self.query = argv[2]
        # One cmd argument: filename
        elif len(argv) == 2:
            self.filename = argv[1]
            self.query = str(datetime.now().astimezone())
        # No cmd arguments
        else:
            print("error: the following arguments are required: filename")
            raise SystemExit(USAGE)

# Read the input csv file
def read_file(filename: str):
    rows = []
    try:
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
            # Creating a csv reader object
            csvreader = csv.reader(csvfile)
            # Skip first row (field names)
            next(csvreader, None)
            # Extracting each data row one by one
            for row in csvreader:
                rows.append(row)
            return rows
    except IOError:
        print("Error: can't find file or read data")

# Convert utcoffset into seconds
def utcoffset_to_seconds(time: str):
    hours = int(time[:2])
    if len(time) == 5:
        minutes = int(time.split(":")[1])
    elif len(time) == 4:
        minutes = int(time[2:])
    else:
        minutes = 0
    return hours*3600 + minutes*60

# Generate a datetime object in UTC (zero UTC offset)
class Query:
    def __init__(self, query: str):
        # Record the timezone (before or after UTC)
        self.early = True
        # Record the UTC offset in seconds
        self.second = 0

        if query[len(query) - 1] == 'Z':
            self.date = datetime.fromisoformat(query[:-1])
        elif '+' in query:
            self.time = query.split("+")[1]
            self.second = utcoffset_to_seconds(self.time)
            self.date = datetime.fromisoformat(query.split("+")[0]) - timedelta(seconds=self.second)
        else:
            # Offset is right after the third "-"
            self.time = query.split("-")[3]
            self.second = utcoffset_to_seconds(self.time)
            self.date = datetime.fromisoformat(query.split("+")[0]) + timedelta(seconds=self.second)
            self.early = False

        self.date = self.date.replace(tzinfo=None)
        self.check = "" + str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year)[2:]

# Retrive information from program list
def lookup(program_list, query_date, check, second, early):
    for i in range(0, len(program_list)):
        programs = ""
        # Matching the UTC start date
        if (program_list[i][2] == check):
            # For each programs with correct start date
            # Create two datetime object, one for start time, one for end time
            year = int("20" + program_list[i][2].split("/")[2])
            month = int(program_list[i][2].split("/")[1])
            day = int(program_list[i][2].split("/")[0])
            hour = int(program_list[i][3].split(":")[0])
            minute = int(program_list[i][3].split(":")[1])

            candidate_start = datetime(year, month, day, hour, minute)
            offset = timedelta(seconds=int(program_list[i][4]))
            candidate_end = candidate_start + offset

            # Check whether the query_date is within the playing time of a certain program
            if (query_date >= candidate_start and query_date < candidate_end):
                if early:
                    endtime = str((candidate_end + timedelta(seconds=second)).time())
                else:
                    endtime = str((candidate_end - timedelta(seconds=second)).time())
                programs = "[{}] That was {}, up next is {} which is rated {} and coming up later is {}."\
                    .format(endtime[:5],program_list[i][0] ,program_list[i + 1][0], program_list[i + 1][1], program_list[i + 2][0])
                return programs
                break

def main():
    user_input = CommandLine(sys.argv)
    program_list = read_file(user_input.filename)
    my_query = Query(user_input.query)
    result = lookup(program_list, my_query.date, my_query.check, my_query.second, my_query.early)
    print(result)

if __name__=="__main__":
    main()
