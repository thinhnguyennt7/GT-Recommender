import datetime
import recommenderClass as rC

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
    hostname, nodes, maxData, arrData = '', '', 100.0, []
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-check-queue ' + recommenderQueue)
    filePath = 'recommendQueue_summary_logs/' + str(getCurrentDateTime())
    newFile = open(filePath, 'w')
    newFile.write("Today is: " +  str(getCurrentDateTime()) + '\n')

    # Get out the one has the least CPU and core number
    for line in iter(ssh_stdout.readline, ""):
        newFile.write(line)
        dataNode = line.split()
        if len(dataNode) >= 8 and dataNode[6] != 'No' and dataNode[2] not in ['Nodes', 'Memory', 'Cpu%']:
            # Calculate the one has the least cpu in use
            if float(dataNode[2]) < float(maxData):
                maxData = float(dataNode[2])
                hostname = dataNode[0]
                nodes = dataNode[1]
    arrData.append(hostname)
    arrData.append(nodes)
    arrData.append(str(maxData))
    newFile.close()
    return arrData

# Get out the list of queue summary
def taskNpsByCore(recommenderQueue, ssh):
    summaryPath = 'hostName_Core_Requested_logs/' + str(getCurrentDateTime()) + '\n'
    summaryFile = open(summaryPath, 'w')
    summaryFile.write("Today is: " +  str(getCurrentDateTime()) + '\n')
    summaryFile.write("" + recommenderQueue + " Queue summary:" + "\n")
    baseCounter = 2

    # Generate the summary logs file base on best recommender queue and base core number
    while baseCounter <= 64:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-check-queue ' + recommenderQueue)
        summaryFile.write("NUMBER OF TASK/NP REQUESTED: " + '[' + str(baseCounter) + ']' + '\n')
        for line in iter(ssh_stdout.readline, ""):
            lineData = line.split()
            if len(lineData) >= 8 and lineData[6] != 'No' and lineData[2] not in ['Nodes', 'Memory', 'Cpu%']:
                if numberOfCoreLeft(lineData[1]) >= baseCounter:
                    summaryFile.write(line)
        baseCounter *= 2
        summaryFile.write("\n")
    summaryFile.close()

# Return the current date with time
def getCurrentDateTime():
    return datetime.datetime.now()

# Collect of the total of walltime of each queues
def collectWallTimeQueue(ssh, sampleQueues):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pace-whoami')
    walltime = {}
    filePath = "paceWallTime_logs/" + str(getCurrentDateTime())
    newFile = open(filePath, 'w')
    newFile.write("Today is: " +  str(getCurrentDateTime()) + '\n')
    for line in iter(ssh_stdout.readline, ""):
        queue_Node = line.split()
        newFile.write(line)
        if (len(queue_Node) != 0):
            if queue_Node[0] in sampleQueues:
                walltime[queue_Node[0]] = queue_Node[1]
    newFile.close()
    return walltime

# Helper method to return the number of core cpu has left in the hostname
def numberOfCoreLeft(taskNp):
    left, right = taskNp.split('/')
    return int(right) - int(left)

# Return the last execution
def lastExecution() -> str:
    pass

# Determine if the last executed fall under 10 mins
def justExecuted() -> bool:
    # Last execution file
    filePath = "lastExecution/recently"
    currentFile = open(filePath, 'r')
    line = currentFile.readline()

    # Get the last execution time
    dateExecuted = line[10:20]
    timeExecuted = line[21:29]

    oldYear, oldMonth, oldDay = dateExecuted.split("-")
    oldHour, oldMinutes, oldSecond = timeExecuted.split(":")

    # Get the current time
    currentTime = str(getCurrentDateTime())
    date = currentTime[0:10]
    time = currentTime[11:19]

    year, month, day = date.split("-")
    hour, minutes, second = time.split(":")

    oldTime = datetime.datetime(int(oldYear), int(oldMonth), int(oldDay), int(oldHour), int(oldMinutes), int(oldSecond))

    if oldTime < datetime.datetime.now():
        diff_Year = int(year) - oldYear
        diff_Month = int(month) - oldMonth
        diff_Date = int(date) - oldDay

        if diff_Year or diff_Month or diff_Date:
            return False

        diff_Hour = int(hour) - oldHour
        diff_Min = int(minutes) - oldMinutes

        if diff_Hour > 0:
            return False
        else:
            if diff_Min <= 10:
                return True
            else:
                return False
    return True