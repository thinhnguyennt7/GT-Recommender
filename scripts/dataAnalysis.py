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
    for line in iter(ssh_stdout.readline, ""):
        newFile.write(line)
        dataNode = line.split()
        if len(dataNode) >= 8 and dataNode[6] != 'No' and dataNode[2] not in ['Nodes', 'Memory', 'Cpu%']:
            if float(dataNode[2]) < float(maxData):
                maxData = float(dataNode[2])
                hostname = dataNode[0]
                nodes = dataNode[1]
    arrData.append(hostname)
    arrData.append(nodes)
    arrData.append(str(maxData))
    newFile.close()
    return arrData

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