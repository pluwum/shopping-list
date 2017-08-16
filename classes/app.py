"""App Class
This file contains the App class c which is the main application class
The class handles all actions of a user on the application by leveraging 
other classes
the are 
    - Registration/signup
    - Login
    - Share list
    - Create list
    - Delete list
    - View list
"""
from classes.user import User
from classes.list_item import ListItem
from classes.shopping_list import ShoppingList


class App():
    def __init__(self):
        self.users = {}
        self.listItems = {}
        self.shoppingLists = {}

    def registerUser(self, first_name, last_name, email, password):
        user = User(first_name, last_name, email, password)
        self.users[email] = {'first_name': first_name,
                             'last_name': last_name, 'email': email, 'password': password}
        return True

    def registerItem(self, name, description):
        item = ListItem(name, description)
        self.listItems[name] = {'name': name, 'description': description}
        return True

    def createShoppingList(self, name, description):
        shoppingList = ShoppingList(name, description)
        self.shoppingLists[name] = {'name': name, 'description': description}
        return True
