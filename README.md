# My-teleprompt
My-teleprompt will list the TV shows that match the DateTime entered by the user according to the program schedule. The displayed information includes the current program and its ending time, followed by the two upcoming shows.
## Technologies
Project is created with:
* Python 3.9.1

Testing with:
* Pytest 6.2.2
## Launch
To run this project, put **run.py** and the **CSV file** containing the program schedule data in the same directory.  

Our program supplies **two command-line arguments**. The first argument is required, it contains the file name of the CSV file. The second one, which stores the DateTime, is optional.  

If you want to assign a specified DateTime (in **ISO 8601 format** including the UTC offset) for querying, run with:  
```
$ python3 run.py file_name.csv datetime  
```
If not, run with: 
```
$ python3 run.py file_name.csv 
```
Hint: In this way, our program will take the local datetime and time offset of your machine for querying
## Sample Outputs
```
$> python run.py example.csv 2021-06-19T15:27:30+10:00

[15:30] That was M.A.S.H, up next is The Simpsons which is rated PG and coming up later is Futurama.  
```
## Design and Assumptions
### Design
We put most code into a function or class and call them from main().  
```
def main():
    user_input = CommandLine(sys.argv)
    program_list = read_file(user_input.filename)
    my_query = Query(user_input.query)
    result = lookup(program_list, my_query.date, my_query.check, my_query.second, my_query.early)
    print(result)
```
First, we store the information entered by the user in the CommandLine class and read the *.csv* file with the CSV module.  

We then generate a DateTime object in UTC (zero UTC offset), and a check string (contains the start date information) based on user input or the machine's local DateTime.  

Finally, while traversing the program schedule, we use this check string to compare with the data in the *utc_start_data* field. Once the start date of a program is matched, we create two DateTime objects concerning this show, one for start time, one for the end time. We check whether the DateTime of the query is within the playing time of a certain program and output the results.
### Assumptions
We assume that the data in the CSV file is sorted in ascending order according to *utc_start_date* and *utc_start_time*.  

We assume that the format of *utc_start_date* is 19/6/21 (as presented in example.csv) rather than 19/06/2021 (as shown in readme.pdf). Otherwise, our check string will never match.
