from DBbcss.dcb import DatasBases
check = DatasBases()

class DataBase:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print(check.set_uspass(username, password))
    def get_code(self):
    	print(check.get_code[username])
    def set_code(self, code):
        try:
        	self.code = code
        	check.set_code(code, username)
        	print("You have successfully registered your code.\n")
        except:
        	print("Error ...")