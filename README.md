Technology to parse data in CSV
======================================
Pandas - Pandas dataframe to process csv data has been used for following reasons
1. Pandas provide extremely streamlined form of data which helped to view data and build the code
2. Data processing/customization using pandas is simple and efficient e.g. removing column
3. Can efficiently handle large amounts of data if need be


Unit Testing
======================================
doctest - doctest framework has been used for Unit testing.
testfile() module has been called and UnitTest.txt is the file containing unit tests
To unit test the code run following command from cmd from path where Csv2Json.py has been placed
py -3 Csv2Json.py -v


Instructions
======================================
1. Place the .CSV file in the same path as .py file. In this case just pass the file name while calling the csv2json function
2. Alternatively provide the complete path along with file name in case file is placed at a different path 
3. Output of the function is a .JSON file which will be created at same path as .py file
4. Kindly refer call.py for command line invocation
5. It can be imported as an module using pip. All files are placed in module folder for the same
6. Two files data.csv and data_c.csv have been provided as both of them have different size and levels of data
7. data_e.csv is an erroneous file used for Unit Testing
8. Sample output file data.json is provided in output folder