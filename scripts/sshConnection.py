import paramiko

# Helper method to connect into the PACE server
def connectToServer(hostname: str, username: str, password: str):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username, password=password)