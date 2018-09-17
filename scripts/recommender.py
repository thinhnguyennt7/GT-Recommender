import datetime
import paramiko
import sys
import dataAnalysis
import logStatement
import sshConnection

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

	# Connect into Georgia Tech PACE Login
	def sshClientConnect(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.hostname, username=self.username, password=self.password)
		print("----------------------------")
		print("gathering queue statistic")
		print("executing qstat ...")
		print("----------------------------")

	# Return the current date with time
	def getCurrentDateTime(self):
		return datetime.datetime.now()

if __name__ == '__main__':
	username = input("Please enter your GT username: ")
	password = input("Please enter your password: ")
	execute = Recommender(username, password)
	print (execute.getSSHLink())





