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