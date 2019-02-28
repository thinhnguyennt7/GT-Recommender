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
		@param nodeRequested: Take in numnber of node requested
	'''
	def __init__(self, username: str, password : str, nodeRequested : int):
		self.username = username
		self.password = password
		self.nodeRequested = nodeRequested

	# Return the full ssh address with username and hostname
	def getSSHLink(self) -> str:
		return "ssh " + self.username + '@' + self.hostname

	# Return the current GT username
	def getUserName(self) -> str:
		return self.username

	# Return the number of node requested
	def getNodeRequested(self) -> int:
		return self.nodeRequested

	# Change to the new GT username
	def setUserName(self, newUserName: str):
		self.username = newUserName

	# Change to the new GT password
	def setPassword(self, newPassword: str):
		self.password = newPassword

	# Change the number of node requested
	def setNewNodeRequest(self, numberOfNodes: int):
		self.nodeRequested = numberOfNodes

	# Return the current GT hostName
	def getHost(self) -> str:
		return self.hostname

	# Change to the new GT hostname address
	def setHost(self, newHostName : str):
		self.hostname = newHostName