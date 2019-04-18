#####################
#### RECOMMENDER ####
#####################

class Recommender:
	# Class Attribute
	hostname = "login-s.pace.gatech.edu"

	'''
		Default Recommender Constructor
		@param username: Take in GT username
		@param nodeRequested: Take in numnber of node requested
	'''
	def __init__(self, nodeRequested : int, username: str, password: str):
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

	# Change the number of node requested
	def setNewNodeRequest(self, numberOfNodes: int):
		self.nodeRequested = numberOfNodes

	# Return the current GT hostName
	def getHost(self) -> str:
		return self.hostname

	# Change to the new GT hostname address
	def setHost(self, newHostName : str):
		self.hostname = newHostName