import time, sys, getpass, datetime, paramiko
from os import path
sys.path.insert(0, './scripts/')
import recommenderClass as mainClass
import dataAnalysis as helper

##################
#### ANALYSIS ####
##################
class Analysis(mainClass.Recommender):

	# Instance Varibles
	queues_Data = {}
	sampleQueues = ['joeforce', 'iw-shared-6', 'joe']
	recommended_queue, timeRangeCheck = None, 10

	# Connect into Georgia Tech PACE Login
	def sshClientConnect(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.hostname, username=self.username, password=self.password)

			print("Collecting walltime for each queues...")

			if (helper.justExecuted(self.timeRangeCheck)):
				lines = helper.readDataFromTxtFile("lastExecution/Recently")
				previousOutput = ''.join(lines)
				print("----------------------------")
				print(previousOutput)

			else:
				walltime = helper.collectWallTimeQueue(ssh, self.sampleQueues)
				print("----------------------------")
				print("gathering queue statistic")
				print("executing qstat ...")
				print("----------------------------")
				self.recommendedQueue(self.queues_Data, ssh, walltime)

		except paramiko.AuthenticationException:
			print ("Wrong credentials.")
			exit(1)

	# Algorithmns to analyze data and compute the best to the worse queue (in order)
	def recommendedQueue(self, queues_Data, ssh, walltime):

		# HANDLE THE COMMAND EXECUTE
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('qstat -q')
		mainLinesOut = rawOutput = 'Requester ID: ' + self.getUserName() + '\n\n'

		# MAIN ALGORITHMNS
		for line in iter(ssh_stdout.readline, ""):
			data = line.split()
			if len(data) > 1 and data[0] in self.sampleQueues:
				mainLinesOut += data[0] + " is having " + data[6] + " watting" + "\n"
				queues_Data[data[0]] = int(data[6])
			rawOutput += line + '\n'

		for queue in queues_Data.keys():
			if self.recommended_queue is None:
				self.recommended_queue = queue
			else:
				if self.recommended_queue in walltime and queue in walltime:
					if queues_Data[self.recommended_queue] > queues_Data[queue] and helper.compare(walltime[queue], walltime[self.recommended_queue]):
						self.recommended_queue = queue
				else:
					if queues_Data[self.recommended_queue] > queues_Data[queue]:
						self.recommended_queue = queue

		# ANALYZE THE QUEUE DATA SET OF THE SERVER
		serverDetails = helper.taskSplitByNodeRequested(self.nodeRequested, self.recommended_queue, ssh)

		# Auto generate the new list by number of core nodes
		helper.taskNpsByCore(self.recommended_queue, ssh)

		# CONCATENATE THE FINAL RESULT
		if serverDetails[0] == '':
			self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'This queue does not contain nay Core or Hostname.'
		else:
			self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'The Hostname has least core and cpu is: [' + serverDetails[0] + ']' + '\n' + 'The tasks/np is: [' + serverDetails[1] + ']' + '\n' + 'The number of CPU: [' + serverDetails[2] + ']'

		# WRITE THE DATA INTO THE TXT FILE
		fileName = "QSTAT_Raw_Data/" + str(helper.getCurrentDateTime())
		helper.writeDataToTxtFile(fileName, rawOutput)

		mainLinesOut += '\n' + self.recommended_queue
		helper.writeDataToTxtFile("Queue_Analysis/NewestFetch", mainLinesOut)

		# UPDATE THE NEW PREVIOUS VALUE TO TXT FILE
		helper.writeDataToTxtFile("lastExecution/Recently", self.recommended_queue)

		# PRINT FINAL RESULT
		print(self.recommended_queue)

################
#### DRIVER ####
################
if __name__ == '__main__':
	print ("Welcome To Georgia Tech Recommender System...")
	time.sleep(1)
	username = input("Please enter your GT username: ")
	password = getpass.getpass("Please enter your GT password: ")

	# Verify make sure the number of node Requested input correct type
	while True:
		try:
			nodeRequested = int(input("Please entere the number of node request: "))
		except:
			print("The node number request must be an integer")
			continue
		else:
			break

	# Instantiate
	Recommender = Analysis(username, password, nodeRequested)
	Recommender.sshClientConnect()