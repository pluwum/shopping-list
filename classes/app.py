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
        user = User(first_name, last_name, email, password)
        self.users[email] = {'first_name': first_name,
                             'last_name': last_name, 'email': email,
                             'password': password}
        return user

    def registerItem(self, name, description):
        item = ListItem(name, description)
        self.list_items[name] = {'name': name, 'description': description}
        return item

    def createShoppingList(self, name, description, user_id):
        shopping_list = ShoppingList(name, description, user_id)
        self.shopping_lists[name] = {
            'name': name, 'user': user_id, 'description': description}
        return shopping_list

    def userAddItemToList(self, list_item, shopping_list):
        shopping_list.addListItem(list_item.name)
        return shopping_list
