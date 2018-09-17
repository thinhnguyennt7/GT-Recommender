import datetime
import paramiko
import time
import sys

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
	recommended_queue = ''

	# Connect into Georgia Tech PACE Login
	def sshClientConnect(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.hostname, username=self.username, password=self.password)
		print("----------------------------")
		print("gathering queue statistic")
		print("executing qstat ...")
		print("----------------------------")

	# Generate logs (errors, data, output) to txt file
	def logsGenerator(self, option):
		# In case of error (ssh, execute command line)
			# Write to the txt file
			# exit the code exit(1)

		# In case no error, able to access data
			# Save the result to the text file include date and time
		return

	# Algorithmns to analyze data and compute the best to the worse queue (in order)
	def recommendedQueue(self, queues_Data):
		# TODO
		return

	# Return the best queue to recommend user to run
	def getRecommendedQueue(self):
		print("----------------------------")
		# Get the best queue from queue
		# recommended_queue = queues_Data[0]
		return recommended_queue if recommended_queue != '' else 'Please run recommendedQueue function to receive the best queue.'

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
	password = input("Please enter your GT password: ")
	test = Analysis(username, password)





