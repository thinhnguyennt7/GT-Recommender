import datetime
import paramiko
import time
import sys
import getpass

#####################
#### RECOMMENDER ####
#####################
class Recommender:

	# Class Attribute
	hostname = "login-s.pace.gatech.edu"

	'''
		Default Recommender Constructor
		@param username: Take in GT username
		@param password: Take in GT password
	'''
	def __init__(self, username, password):
		self.username = username
		self.password = password

	# Return the full ssh address with username and hostname
	def getSSHLink(self):
		return "ssh " + self.username + '@' + self.hostname

	# Return the current GT username
	def getUserName(self):
		return self.username

	# Change to the new GT username
	def setUserName(self, newUserName):
		self.username = newUserName

	# Change to the new GT password
	def setPassword(self, newPassword):
		self.password = newPassword

	# Return the current GT hostName
	def getHost(self):
		return self.hostname

	# Change to the new GT hostname address
	def setHost(self, newHostName):
		self.hostname = newHostName

	# Return the current date with time
	def getCurrentDateTime(self):
		return datetime.datetime.now()


##################
#### ANALYSIS ####
##################
class Analysis(Recommender):

	# Instance Varibles
	queues_Data = {}
	recommended_queue = None

	# Connect into Georgia Tech PACE Login
	def sshClientConnect(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.hostname, username=self.username, password=self.password)

			print("----------------------------")
			print("gathering queue statistic")
			print("executing qstat ...")
			print("----------------------------")

			self.recommendedQueue(self.queues_Data, ssh)

		except paramiko.AuthenticationException:
			print ("Wrong credentials.")
			exit(1)

	# Algorithmns to analyze data and compute the best to the worse queue (in order)
	def recommendedQueue(self, queues_Data, ssh):
		# List queue available to use
		queues = ['joeforce', 'joe-test', 'iw-shared-6', 'joe']

		# Generate a new file
		newFile = open(str(self.getCurrentDateTime()), 'w')
		newFile.write("Today is: " +  str(self.getCurrentDateTime()) + '\n')
		newFile.write('Current requester ID: ' + self.getUserName())

		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('qstat -q')

		# Algorithmns
		for line in iter(ssh_stdout.readline, ""):
			data = line.split()
			if len(data) > 1 and data[0] in queues:
				print (data[0] + " is having " + data[6] + " watting")
				queues_Data[data[0]] = int(data[6]) # 6 mean jobs in queue, 0 mean name of queue
			newFile.write(line)

		for queue in queues_Data.keys():
			if self.recommended_queue is None:
				self.recommended_queue = queue
			else:
				if queues_Data[self.recommended_queue] > queues_Data[queue]:
					self.recommended_queue = queue
		self.recommended_queue = 'The Recommended queue is: [' + self.recommended_queue + ']'

		print("----------------------------")
		print (self.recommended_queue)
		newFile.write(self.recommended_queue)

		# Close file
		newFile.close()


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





