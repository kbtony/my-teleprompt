# My-teleprompt
My-teleprompt will list the TV shows that match the DateTime entered by the user according to the program schedule. The displayed information includes the current program and its ending time, followed by the two upcoming shows.
## Technologies
Project is created with:
* Python 3.9.1

Testing with:
* Pytest 6.2.2
## Launch
To run this project,  

Put **run.py** and the **CSV file** containing the program schedule data in the same directory.  

Our program supplies two command-line arguments. The first argument is required, it contains the file name of the CSV file. The second one, which stores the DateTime, is optional.  

If you want to assign a specified DateTime (in ISO 8601 format including the UTC offset) for querying, run with:  
> $ python3 run.py file_name.csv datetime  

