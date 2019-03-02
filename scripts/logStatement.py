import os.path
import dataAnalysis as da

# Helper method to write data into the txt file
def writeDataToTxtFile(path: str, data: str):
    if data:
        openFile = open(path, 'w')
        openFile.write("Today is: " +  str(da.getCurrentDateTime()) + '\n')
        openFile.write(data)
        openFile.close()

# Helper method to read the lines from the txt file
def readDataFromTxtFile(path: str):
    openFile = open(path, 'r')
    lines = openFile.readlines()
    return lines

# Helper method to check if the file exist in the folder
def checkFileInPath(path):
	return os.path.exists(path)