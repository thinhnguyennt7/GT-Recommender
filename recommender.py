import time, sys, getpass, datetime, paramiko
from os import path
sys.path.insert(0, './scripts/')
import recommenderClass as mainClass
import dataAnalysis as da
import logStatement as lg

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

			# If the program just executed and the data inside still valid then
			if (da.justExecuted(self.timeRangeCheck) and da.verifyData(self.nodeRequested)):
				lines = lg.readDataFromTxtFile("lastExecution/Recently")
				previousOutput = ''.join(lines)
				print("----------------------------")
				print(previousOutput)

			else:
				walltime = da.collectWallTimeQueue(ssh, self.sampleQueues)
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
		mainLinesOut = rawOutput = 'Requester ID: ' + self.getUserName() + '\n'

		# MAIN ALGORITHMNS
		for line in iter(ssh_stdout.readline, ""):
			data = line.split()
			if len(data) > 1 and data[0] in self.sampleQueues:
				mainLinesOut += data[0] + " is having " + data[6] + " watting" + "\n"
				queues_Data[data[0]] = int(data[6])
			rawOutput += line + '\n'

		# Sort the number of node waiting by acending order
		queues_Data = {k: v for k, v in sorted(queues_Data.items(), key=lambda x: x[1])}

		# Compute the best queue with less jobs waiting and less walltime
		for queue in queues_Data.keys():
			if self.recommended_queue is None:
				self.recommended_queue = queue
			else:
				if self.recommended_queue in walltime and queue in walltime:
					if queues_Data[self.recommended_queue] > queues_Data[queue] and da.compare(walltime[queue], walltime[self.recommended_queue]):
						self.recommended_queue = queue
				else:
					if queues_Data[self.recommended_queue] > queues_Data[queue]:
						self.recommended_queue = queue

		# Find server, node, hostname of the recommended queue
		index, foundServer = 0, False
		for queue_name in queues_Data.keys():
			# Assume the second to n is recommender queue if the old recommended queue can not find any server
			if index > 0:
				self.recommended_queue = queue_name

			# Analyze the queue data set of the server and generate list of server name
			serverDetails = da.taskSplitByNodeRequested(self.getUserName(), self.nodeRequested, self.recommended_queue, ssh)

			# Concatenate the final result
			if serverDetails[0] == '':
				index += 1
				continue
			else:
				foundServer = True
				self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'The Hostname is: [' + serverDetails[0] + ']' + '\n' + 'The tasks/np is (used/total): [' + serverDetails[1] + ']' + '\n' + 'The number of CPU remain: [' + serverDetails[2] + ']'
				break

		# In case if no server, hostname found
		if not foundServer:
			self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'There are no server have enough number of node requested as you want or all servers have down already!'

		# WRITE THE DATA INTO THE TXT FILE
		fileName = "QSTAT_Raw_Data/" + str(da.getCurrentDateTime())
		lg.writeDataToTxtFile(fileName, rawOutput)

		mainLinesOut += '\n' + self.recommended_queue
		lg.writeDataToTxtFile("Queue_Analysis/NewestFetch", mainLinesOut)

		# UPDATE THE NEW PREVIOUS VALUE TO TXT FILE
		lg.writeDataToTxtFile("lastExecution/Recently", self.recommended_queue)

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
			if (nodeRequested <= 0):
				print("The node number request must positive integer")
				continue
			elif (nodeRequested > 64):
				print("The PACE system take up to 64 bits")
				continue
		except:
			print("The node number request must be an integer")
			continue
		else:
			break

	# Instantiate
	Recommender = Analysis(username, password, nodeRequested)
	Recommender.sshClientConnect()