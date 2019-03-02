import os.path
import dataAnalysis as da


# Helper method to write data into the txt file
def writeDataToTxtFile(path: str, data: str):
	folderPath = path[:path.index('/')]

	# Create folder if it not in there yet
	createNewFolder(folderPath)

	if data:
		openFile = open(path, 'w')
		openFile.write("Today is: " +  str(da.getCurrentDateTime()) + '\n\n')
		openFile.write(data)
		openFile.close()


# Helper method to read the lines from the txt file
def readDataFromTxtFile(path: str):
	openFile = open(path, 'r')
	lines = openFile.readlines()
	return lines


# Helper method to check if the file exist in the folder
def checkFileInPath(path) -> bool:
	return os.path.exists(path)

# Helper method to create new folder in directory
def createNewFolder(path):
	if not checkFileInPath(path):
		os.makedirs(path)