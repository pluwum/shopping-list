"""App Class
Thhe App class is the main application class
The class handles all actions of a user on the application by leveraging
other classes
the are
    - Registration/signup
    - Login
    - Share list
    - Create list
    - Delete list
"""


class ShoppingListApp():
    def __init__(self):
        self.users = {}
        self.list_items = {}
        self.shopping_lists = {}

    def registerUser(self, first_name, last_name, email, password):
        if email in self.users:
            raise Exception(
                "User already exists, Did you forget password?")

        user = User(first_name, last_name, email, password)
        self.users[email] = user
        return user

    def registerItem(self, name, description):

        if name in self.list_items:
            raise Exception(
                "User already exists, Please try again")

        item = ListItem(name, description)
        self.list_items[name] = item
        return item

    def createShoppingList(self, name, description, user_id):
        shopping_list = ShoppingList(name, description, user_id)
        self.shopping_lists[name] = shopping_list
        return shopping_list

    def deleteShoppingList(self, name):
        self.shopping_lists.pop(name, None)
        return True

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


"""The User class models the generic behaviour
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


"""The Shopping List class definition
This class represents each shopping list and the generic
attributes it has
"""


class ShoppingList():
    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.list_items = {}

    # Add item to shopping list
    def addListItem(self, list_item, quantity=None):
        if quantity is None:
            quantity = 1

        self.list_items[list_item] = quantity
        return True


"""This file contains the ListItem class
This class models the attirbutes and behaviours
 of an individual list item
"""


class ListItem():
    def __init__(self, name, description):
        self.name = name
        self.description = description
