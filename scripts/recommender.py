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
			# self.fileGenerator('error')
			print ("Wrong credentials.")
			exit(1)

	# Algorithmns to analyze data and compute the best to the worse queue (in order)
	def recommendedQueue(self, queues_Data, ssh):

		# Generate a new file
		# newFile = open(str(self.getCurrentDateTime()), 'w')
		# noteMessage = "Today is: " +  str(self.getCurrentDateTime()) + '\n'
		# currentRequester = 'Current requester ID: ' + self.getUserName()
		# newFile.write(noteMessage)
		# newFile.write(currentRequester)
		# Generate logs (errors, rawData) to txt file
		def fileGenerator(self, option):
			newFile = open(str(self.getCurrentDateTime()), 'w')
			if (option == 'rawData'):
				noteMessage = "Today is: " +  str(self.getCurrentDateTime()) + '\n'
				currentRequester = 'Current requester ID: ' + self.getUserName()
				newFile.write(noteMessage)
				newFile.write(currentRequester)
			elif (option == 'error'):
				newFile.write('Wrong credentials... Please double check your username or password')
		# self.fileGenerator('rawData')

		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('qstat -q') # View all the list

		# Algorithmns
		for line in iter(ssh_stdout.readline, ""):
			spl = line.split()
			if len(spl) > 1 and (spl[0]== 'joe' or spl[0] == 'joeforce'):
				print (spl[0] + " is having " + spl[6] + " watting")
				queues_Data[spl[0]] = int(spl[6])
			newFile.write(line)

		for queue in queues_Data:
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

	# Send the txt file (raw data) including recommended result to user's request
	def sendResultToUser(self):
		currentUserEmail = self.username + '@gatech.edu'
		print ("Email is sending ... Please wait")
		time.sleep(3)
		print ("Email has been sent to [ " + self.username + " ]")


################
#### DRIVER ####
################
if __name__ == '__main__':
	print ("Welcome To Georgia Tech Recommender System...")
	time.sleep(1) # Time out for 1 sec
	username = input("Please enter your GT username: ")
	password = getpass.getpass("Please enter your GT password: ")

	# Instanciate
	Recommender = Analysis(username, password)
	Recommender.sshClientConnect()





