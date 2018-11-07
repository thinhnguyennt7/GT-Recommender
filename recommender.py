import time, sys, getpass, datetime, paramiko
from os import path
sys.path.insert(0, './scripts/')
import recommenderClass as rC
import dataAnalysis as dA

##################
#### ANALYSIS ####
##################
class Analysis(rC.Recommender):

	# Instance Varibles
	queues_Data = {}
	sampleQueues = ['joeforce', 'joe-test', 'iw-shared-6', 'joe']
	recommended_queue = None

	# Connect into Georgia Tech PACE Login
	def sshClientConnect(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.hostname, username=self.username, password=self.password)

			print("Collecting walltime for each queues...")
			walltime = dA.collectWallTimeQueue(ssh, self.sampleQueues)

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
		# Generate a new file
		filePath = "qstat_Run_logs/" + str(dA.getCurrentDateTime())
		newFile = open(filePath, 'w')
		newFile.write("Today is: " +  str(dA.getCurrentDateTime()) + '\n')
		newFile.write('Current requester ID: ' + self.getUserName() + '\n')

		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('qstat -q')

		# Algorithmns
		for line in iter(ssh_stdout.readline, ""):
			data = line.split()
			if len(data) > 1 and data[0] in self.sampleQueues:
				print (data[0] + " is having " + data[6] + " watting")
				queues_Data[data[0]] = int(data[6]) # 6 mean jobs in queue, 0 mean name of queue
			newFile.write(line)

		for queue in queues_Data.keys():
			if self.recommended_queue is None:
				self.recommended_queue = queue
			else:
				if self.recommended_queue in walltime and queue in walltime:
					if queues_Data[self.recommended_queue] > queues_Data[queue] and dA.compare(walltime[queue], walltime[self.recommended_queue]):
						self.recommended_queue = queue
				else:
					if queues_Data[self.recommended_queue] > queues_Data[queue]:
						self.recommended_queue = queue
		arrData = dA.taskSplitRecommender(self.recommended_queue, ssh)
		dA.taskNpsByCore("joeforce", ssh)

		# Print result
		if arrData[0] == '':
			self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'This queue does not contain nay Core or Hostname.'
		else:
			self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']' + '\n' + 'The Hostname has least core and cpu is: [' + arrData[0] + ']' + '\n' + 'The tasks/np is: [' + arrData[1] + ']' + '\n' + 'The number of CPU: [' + arrData[2] + ']'

		print("----------------------------")
		print (self.recommended_queue)

		# Write file
		newFile.write(self.recommended_queue)
		newFile.close()

	# def queueSummaryDataRequire(self, recommended_queue):


################
#### DRIVER ####
################
if __name__ == '__main__':
	print ("Welcome To Georgia Tech Recommender System...")
	time.sleep(1)
	username = input("Please enter your GT username: ")
	password = getpass.getpass("Please enter your GT password: ")

	# Instantiate
	Recommender = Analysis(username, password)
	Recommender.sshClientConnect()