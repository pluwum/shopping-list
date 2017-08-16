"""User related Actions
This class contains all actions on the application
the are 
    - Registration/signup
    - Login
    - Share list
    - Create list
    - Delete list
    - View list
"""


class User():
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        