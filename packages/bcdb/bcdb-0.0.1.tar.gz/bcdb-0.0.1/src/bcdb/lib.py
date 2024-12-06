uspass = {}
codes = {}
class BCDB:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        if username in uspass:
        	if uspass[username] == password:
        		print("You have successfully logged in.\n")
        	else:
        		print("The password or username is wrong.\n")
        else:
        	print("You have successfully registered.\n")
        	uspass[username] = password

    def get_code(self):
    	try:
    		return codes[self.username]
    	except:
    		print("You don't have a code, use the set_code() method to register your code.\n")
    def set_code(self, code):
    	self.code = code
    	codes[self.username] = code
    	print("You have successfully registered your code.\n")