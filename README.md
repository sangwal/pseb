# Analyse Matric and Sr. Sec. results downloaded from PSEB (pseb.ac.in)

This repository is about analysing the school results of matric and senior secondary 
classes of the Punjab School Education Board (pseb.ac.in).

NOTICE: This may not be suitable for other Boards. Modify the script in case of other Boards.


## Setup the environment

1. Install python 3.xx from the python.org site for your operating system.
2. Install requisite modules by issuing the following command in the command terminal:
    ```
        pip install pandas
    ```
    (You may need to prefix the above command with sudo in Linux.)

Upon successful installed of the packages, the following steps should work.

# Download required scripts

Point your browser to ```https://github.com/sangwal/pseb``` site and download par.py and pnb2unicode.py.
Move these files to a folder of your choice, maybe PSEB-results in Documents folder.

## Download the result from the PSEB site

Download the result for class 10 or 12 and save it to a file, say, Result-2025.xlsx.
Copy/Move this file to the folder (PSEB-results) containing par.py file.

## Add a column named "Section" to Result-2025.xlsx

Add a column named "Section" before the name of the students in the downloaded
result file and enter section for each student.

## Add a new sheet "MM" to Result-2025.xlsx

Add a new sheet named "MM" to the downloaded result file, Result-2025.xlsx.
In the A1 and B1 cells of this MM sheet, write "Subject" and "MM", respectively.
In the following rows, type in the names of the subjects (as abbreviated in the 
"detailres" column of the downloaded result file, Result-2025.xlsx) in the A column
and maximum marks for that subject in the B column in the corresponding row.

Once the above data is entered correctly, save the file by pressing Ctrl+S and close the file.

# Run the script to get statistics

Open the command terminal and issue the command:

```
    python par.py Result-2025.xlsx
```

A successful run of the above command creates two more sheets "processed" and "performance" in the file Result-2025.xlsx.

The "processed" sheet contains the marks properly arranged along with Punjabi names for students.
The "performace" sheet has the required statistics to be filled in the ACRs of the teachers.

