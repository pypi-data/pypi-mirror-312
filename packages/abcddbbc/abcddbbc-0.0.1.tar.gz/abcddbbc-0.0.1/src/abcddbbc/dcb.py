uspass = {}
codes = {}

class DatasBases:
	def __init__(self):
		pass
	def set_code(self, code, username):
		self.code = code
		self.username = username
		codes[username] = code
	def get_code(self):
		try:
			return codes
		except:
            print("You don't have a code, use the set_code() method to register your code.\n")
	def set_uspass(self, username, password):
		self.username = usernane
		self.password = password
		if username in uspass:
			if uspass[username] == password:
				return "You have successfully logged in.\n"
			else:
				return "The password or username is wrong.\n"
		else:
			uspass[username] = password
			return "You have successfully registered.\n"