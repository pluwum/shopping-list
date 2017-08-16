from classes.user import User
class App():
    def __init__(self):
        self.users = {}

    def registerUser(self, first_name, last_name, email, password):
        user = User(first_name, last_name, email, password)
        self.users[email] = {'first_name':first_name, 'last_name':last_name, 'email':email, 'password':password}
        return True
