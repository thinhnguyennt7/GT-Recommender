import datetime
import recommenderClass as mainClass

# Helper method to check the time has the least
def compare(time1, time2):
    if len(time1) < len(time2):
        return 1
    elif len(time1) > len(time2):
        return -1
    else:
        timeOne = time1.split(":")
        timeTwo = time2.split(":")
        if (int(timeOne[0]) < int(timeTwo[0])):
            return 1
        elif (int(timeOne[0]) > int(timeTwo[0])):
            return -1
        else:
            return 0

# Estimate the total amount task should split out for each hostname
def taskSplitRecommender(recommenderQueue, ssh):
    hostname, nodes, maxData, lines = '', '', 100.0, ''
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-check-queue ' + recommenderQueue)

    # Get out the one has the least CPU and core number
    for line in iter(ssh_stdout.readline, ""):
        lines += line
        dataNode = line.split()
        if len(dataNode) >= 8 and dataNode[6] != 'No' and dataNode[2] not in ['Nodes', 'Memory', 'Cpu%']:
            # Calculate the one has the least cpu in use
            if float(dataNode[2]) < float(maxData):
                maxData = float(dataNode[2])
                hostname = dataNode[0]
                nodes = dataNode[1]

    # Write new data to logs
    filePath = 'HostServerDetail_Data/' + str(getCurrentDateTime())
    writeDataToTxtFile(filePath, lines)

    return [hostname, nodes, str(maxData)]

# Get out the list of queue summary
def taskNpsByCore(recommenderQueue, ssh):
    baseCounter, lines = 2, "" + recommenderQueue + " Queue summary:" + "\n"

    # Generate the summary logs file base on best recommender queue and base core number
    while baseCounter <= 64:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-check-queue ' + recommenderQueue)
        lines += "NUMBER OF TASK/NP REQUESTED: " + '[' + str(baseCounter) + ']' + '\n'
        for line in iter(ssh_stdout.readline, ""):
            lineData = line.split()
            if len(lineData) >= 8 and lineData[6] != 'No' and lineData[2] not in ['Nodes', 'Memory', 'Cpu%']:
                if numberOfCoreLeft(lineData[1]) >= baseCounter:
                    lines += line
        baseCounter *= 2
        lines += '\n'

    # Write new data to logs
    summaryPath = 'hostName_Core_Requested/' + str(getCurrentDateTime())
    writeDataToTxtFile(summaryPath, lines)

# Return the current date with time
def getCurrentDateTime():
    return datetime.datetime.now()

# Collect of the total of walltime of each queues
def collectWallTimeQueue(ssh, sampleQueues):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-whoami')
    walltime, lines = {}, ''

    for line in iter(ssh_stdout.readline, ""):
        lines += line
        queue_Node = line.split()
        if (len(queue_Node) != 0):
            if queue_Node[0] in sampleQueues:
                walltime[queue_Node[0]] = queue_Node[1]

    # Write new data to logs
    filePath = "paceWallTime_Data/" + str(getCurrentDateTime())
    writeDataToTxtFile(filePath, lines)

    return walltime

# Helper method to return the number of core cpu has left in the hostname
def numberOfCoreLeft(taskNp):
    left, right = taskNp.split('/')
    return int(right) - int(left)

# Helper method to write data into the txt file
def writeDataToTxtFile(path: str, data: str):
    if data:
        openFile = open(path, 'w')
        openFile.write("Today is: " +  str(getCurrentDateTime()) + '\n')
        openFile.write(data)
        openFile.close()

# Helper method to read the lines from the txt file
def readDataFromTxtFile(path: str):
    openFile = open(path, 'r')
    lines = openFile.readlines()
    return lines

def compareTimeRange(oldTime, newTime, time_range) -> bool:
    # Generate the old time range to real data value
    oldTimeRange = datetime.datetime(oldTime[0], oldTime[1], oldTime[2], oldTime[3], oldTime[4], oldTime[5])

    if oldTimeRange < getCurrentDateTime():
        diff_Year = newTime[0] - oldTime[0]
        diff_Month = newTime[1] - oldTime[1]
        diff_Date = newTime[2] - newTime[2]

        if diff_Year or diff_Month or diff_Date:
            return False

        diff_Hour = newTime[3] - oldTime[3]
        diff_Min =  newTime[4] - oldTime[4]

        if diff_Hour > 0:
            return False
        else:
            if diff_Min <= time_range:
                return True
            else:
                return False
    return True

# Determine if the last executed fall under 10 mins
def justExecuted(time_range: int) -> bool:
    # Last execution file
    previousExecutedDate = readDataFromTxtFile("lastExecution/recently")[0]

    # Get the last execution time
    dateExecuted = previousExecutedDate[10:20]
    timeExecuted = previousExecutedDate[21:29]
    oldYear, oldMonth, oldDay = dateExecuted.split("-")
    oldHour, oldMinutes, oldSecond = timeExecuted.split(":")
    oldTime = [int(oldYear), int(oldMonth), int(oldDay), int(oldHour), int(oldMinutes), int(oldSecond)]

    # Get the current time
    currentTime = str(getCurrentDateTime())
    date = currentTime[0:10]
    time = currentTime[11:19]
    year, month, day = date.split("-")
    hour, minutes, second = time.split(":")
    newTime = [int(year), int(month), int(day), int(hour), int(minutes), int(second)]

    return compareTimeRange(oldTime, newTime, time_range)