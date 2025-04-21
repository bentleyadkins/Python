""" 
Bentley Adkins
Started on 2/27/2025 
Last Modified 2/28/2025

Data Validation Script - 

To check off the first task on the bigger Validation Script project.

Task:
Please write one .py file.

Params:
That function would take two csvs as input. The one file will be named "SpecSheet", and the other file can be named anything. There will be only two files in the input folder.

The input file, (the one that is not named " SpecSheet") let us call it File A, will be the dataset itself.

Convert all time / dates in format "MM/DD/YYYY"
Make sure all columns in File A are 'strings', if not, convert them. 
Save the file as a .csv, let us call this Modified File A

The other input file, let us call it File B, will list all the columns in the File A; and it will have a corresponding max length for each of those columns. This file will be a csv with two columns named "Columns in Input File" and "Column Length"

Take Modified File A, make sure it complies with specifications in File B. 
If Modified File A is compliant, create a simple .txt file called "Output" and print "Input file is compliant", else print "File doesn't comply"
"""

# Library for reading csv files
import pandas as pd

# Using this library to give extra functionality for changing the data. Pandas to_datetime won't be enough for this since we need to read strings,
# needs to be pulled so that we can convert dates with strings "Tuesday, January 16, 2024" to proper format such as "MM/DD/YYYY"
from dateutil.parser import parse

class ModifyFileA:
    # Function written to check if the file exists in the directory and then print all files found with .xlsx or .csv
    # If csv Exists then file is read by pandas
    def readFileintoPandas(fileReadA):
        if fileReadA.endswith('.csv'):  # looks to see if string/filename ends with csv 
            try:
                fileRead_Updated = pd.read_csv(fileReadA) 
                return fileRead_Updated
            except Exception as e:
                print(f"Error reading file {fileReadA}: {e}")
                return None
        else:
            print("File must be a CSV.")
            return None

    # Sets object columns as type string
    def columnToString(fileReadA):
        for column in fileReadA.columns: # iterates through each of the columns
            if fileReadA[column].dtype != 'object': # if datatype is not an object the converts to string, pandas 
                fileReadA[column] = fileReadA[column].astype(str)  # converts columns to strings
        return fileReadA

    def is_date(stringChecked):    
        if isinstance(stringChecked, (int, float)): # if value is an integer or floating number then pass
            return False
        try:
            if parse(stringChecked, fuzzy=True):  # fuzzy = True means that it searches for an approximate match
                return True
        except (ValueError, TypeError):  # Returns False if you have a conversion of int to string or if you add an int to a string
            return False

    # Function takes care of converting the specific column to the accurate date format
    def dateConversion(fileReadA, dateformat="%m/%d/%Y"):
        for column in fileReadA.columns: # iterates through each of the columns
            try:
                if fileReadA[column].dtype == 'object':                   
                    fileReadA[column] = fileReadA[column].apply(lambda x:    # lambda is mapping each column that is a date with the proper format
                        parse(x, fuzzy=True).strftime(dateformat) if ModifyFileA.is_date(x) else x)
            except Exception as e:
                print(f"Error converting date column {column}: {e}")
        return fileReadA


class CompareFileB:

    # Function to compare compliance of columns between File A and File B
    def ColumnComparisonCompliancy(fileA, fileB, column_name): 

        # Converts each column to a string and gets the max length of each converted string
        fileA_maxLength = fileA[column_name].astype(str).str.len().max()
        fileB_maxLength = fileB.loc[fileB['Columns in Input File'] == column_name, 'Column Length'].values  # Get max length from File B

        if fileB_maxLength.size > 0:  # If there's a match
            fileB_maxLength = int(fileB_maxLength[0])
            return fileA_maxLength <= fileB_maxLength  # Check if File A complies with the max length in File B
        else:
            print(f"Column '{column_name}' not found in File B.")
            return False


# Written to check if file is in Directory, mostly for testing purposes and to make sure files existed
fileA = ModifyFileA.readFileintoPandas("Validation_Test_1.csv")
print()
print("File A has been read into pandas.")
print("File A before modification.")
print()
print(fileA.head())
print()

# Calls to function to convert date and time into proper format
fileA = ModifyFileA.dateConversion(fileA)

print("Date has been updated and formatted in MM/DD/YYYY.")
print()
print(fileA.head()) # Overview of Modified data, returns first 5 records
print()

# Converts all columns into strings
fileA = ModifyFileA.columnToString(fileA)

print("Columns have been converted to Strings.")
print()
print(fileA.head())
print()

print("New CSV will be written with modifications.")
fileA.to_csv("ModifiedFileA.csv", index=False)      # index = False basically keeps the csv from having each row labels with an index and ,
print()



#Commented out for later modification
'''
fileB = ModifyFileA.readFileintoPandas("SpecSheet.csv")
print()
print("File B has been read into pandas.")
print("File B before modification.")
print()
print(fileB.head())
print()

 CompareFileB.ColumnComparisonCompliancy(fileA, fileB, 'Adkins_Column')

 New compliance check after modification of fileA

fileB = ModifyFileA.readFileintoPandas("SpecSheet.csv")
if fileA is None or fileB is None:
    print("One of the files is not loaded properly. Exiting.")
else:
    # Check compliance for each column listed in File B
    compliant = True
    for column in fileB['Columns in Input File']:
        if not CompareFileB.ColumnComparisonCompliancy(fileA, fileB, column):
            compliant = False
            break
    
    # Write the output to a text file based on compliance check
    with open('Output.txt', 'w') as output_file:
        if compliant:
            output_file.write("Input file is compliant")
        else:
            output_file.write("File doesn't comply")

    print("Compliance check complete. Output written to 'Output.txt'.")
'''