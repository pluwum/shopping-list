from classes.user import User
from classes.list_item import ListItem
class App():
    def __init__(self):
        self.users = {}
        self.listItems = {}
        self.shoppingLists = {}

    def registerUser(self, first_name, last_name, email, password):
        user = User(first_name, last_name, email, password)
        self.users[email] = {'first_name':first_name, 'last_name':last_name, 'email':email, 'password':password}
        return True

    def registerItem(self, name, description):
        item = ListItem(name, description)
        self.listItems[name] = {'name':name, 'description':description}
        return True
