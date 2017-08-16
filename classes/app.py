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
        self.list_items = {}
        self.shopping_lists = {}

    def registerUser(self, first_name, last_name, email, password):
        if email in self.users:
            return "User already exists"

        user = User(first_name, last_name, email, password)
        self.users[email] = user
        return user

    def registerItem(self, name, description):

        if name in self.list_items:
            return "Item already exists"

        item = ListItem(name, description)
        self.list_items[name] = item
        return item

    def createShoppingList(self, name, description, user_id):
        shopping_list = ShoppingList(name, description, user_id)
        self.shopping_lists[name] = shopping_list
        return shopping_list

    def userAddItemToList(self, shopping_list, list_item, quantity=None):
        shopping_list.addListItem(list_item.name, quantity)
        return shopping_list

    def login(self, email, password):

        if email not in self.users:
            raise Exception("User doesnt exists, Please add")
        user = self.users[email]

        if user.verifyCredentials(email, password) is False:
            raise Exception(
                "Authentication Failed, Please check email and password")
        return True
