"""This file contains the User classThisclassmodels the generic behaviour
and attributes of a user in the system
"""


class User():
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def verifyCredentials(self, email, password):
        if email == self.email and password == self.password:
            return True

        return False
