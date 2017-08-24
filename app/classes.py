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
        # Tracks items in the system
        self.users = {}
        # Tracks items created
        self.list_items = {}
        # Tracks shopping lists created
        self.shopping_lists = {}
        # Tracks login sessions
        self.sessions = []

    def registerUser(self, first_name, last_name, email, password):
        if email in self.users:
            raise Exception(
                "User already exists, Did you forget your password?")

        user = User(first_name, last_name, email, password)
        self.users[email] = user
        return user

    def getUserShoppingLists(self, email):
        if email in self.shopping_lists:
            return self.shopping_lists[email]
        return []

    def getUserDetail(self, email):
        if email in self.users:
            return self.users[email]
        # When user not found, raise error
        raise Exception(
                "This user doesn't exist, Please login or register")

    def registerItem(self, name, description):

        if name in self.list_items:
            raise Exception(
                "Item already exists, Please try again")

        item = ListItem(name, description)
        self.list_items[name] = item
        return item

    def createShoppingList(self, name, description, user_email):
        """This method creates a shopping list for a user"""
        if name is None or description is None or user_email is None:
            raise Exception("Missing Field:Please provide name & Description")
        if user_email not in self.users:
            raise Exception(
                "Non Existent users are not allowed to created lists:Please"
                "register or log in"
            )
        # Create list Object
        shopping_list = ShoppingList(name, description, user_email)
        # Add list to user list tracker
        # Check if user already has a list
        if user_email in self.shopping_lists:
            users_lists = self.shopping_lists[user_email]

            for user_list in users_lists:
                if user_list.name.lower() == name.lower():
                    raise Exception(
                        "You already have a list with the same name: "\
                        "Please perform action again using new list name"
                        )
            users_lists.append(shopping_list)
        else:
            # Create a new list if this is the user's first shopping List
            self.shopping_lists[user_email] = [shopping_list]
        return shopping_list

    def editShoppingList(self, id, user_email, name=None, description=None):
        """This method edits the shopping list at index id and email"""
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        if id is not None:
            user_lists = self.shopping_lists[user_email]
            list_to_edit = user_lists[id]
            # Update name
            if name is not None:
                list_to_edit.setName(name)
            # Update Description
            if description is not None:
                list_to_edit.setDescription(description)
            # Update the object stored in our list tracker
            self.shopping_lists[user_email][id] = list_to_edit
            return True
        return False

    def viewShoppingList(self, id, user_email):
        """This method returns a shopping list given its ID and creator's
        email
        """
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        if id is not None:
            user_lists = self.shopping_lists[user_email]
            return user_lists[id]

        raise Exception("Oops! List ID field was not received with request")

    def deleteShoppingList(self, id, user_email):
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        # Make sure the index is not out of bounds
        if len(self.shopping_lists[user_email]) > id:
            self.shopping_lists[user_email].pop(id)
            return True
        raise Exception("Oops! List does not exist")

    def userAddItemToList(self, shopping_list, item_name, description,
                          quantity=None):
        # Lets check that everything we need is available
        if all(param is not None for param in [shopping_list, item_name,
                                               description]):
            list_item = ListItem(item_name, description, quantity)
            item_id = shopping_list.addListItem(list_item, quantity)
            return item_id

        raise Exception(
            "Oops! Some parameters seem to be missing, please review")

    def userUpdateItemInList(self, shopping_list, list_item, item_name,
                             description, quantity=None):
        shopping_list.updateItem(list_item, item_name, description)

    def userRemoveItemFromList(self, shopping_list, list_item, quantity=None):
        shopping_list.removeListItem(list_item, quantity)
        return True

    def login(self, email, password):
        # Lets find out if user exists
        if email not in self.users:
            raise Exception("User doesnt exists, Please add")
        # User exists, so lets get their data
        user = self.users[email]

        # Check if received password and email combinations match up
        if user.verifyCredentials(email, password) is False:
            raise Exception(
                "Authentication Failed, Please check email and password")

        return True

    def logout(self, email):
        if email in self.sessions:
            self.sessions.remove(email)
        else:
            raise Exception(
                "User login session could not be found")

    def isLoggedIn(self):
        # Check if user is in list of logged in users
        if email in self.sessions:
            return True
        # User not logged in so we return false
        return False


"""The User class models the generic behaviour
and attributes of a user in the system
"""


class User():
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def getEmail():
        return self.email

    def verifyCredentials(self, email, password):
        if email == self.email and password == self.password:
            return True

        return False


class ShoppingList():
    """The Shopping List class definition
    This class represents each shopping list and the generic attributes it has
    """
    def __init__(self, name, description, user_id):
        self.id = None
        self.name = name
        self.description = description
        self.user_id = user_id
        self.list_items = []

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def getListItems(self):
        return self.list_items

    def getListItem(self, id):
        if len(self.list_items) > id:
            return self.list_items[id]

    # Add item to shopping list
    def addListItem(self, list_item, quantity=None):
        # Check if similar item already in list
        for item in self.list_items:
            if list_item.name.lower() == item.name.lower():
                raise Exception("Error:Sorry, Item already exists in your"\
                                "list, please choose another name")

        # When nothing is found, add item to list
        self.list_items.append(list_item)
        # Lets return the item's index to use as an ID
        return len(self.list_items) - 1

    # Remove item to shopping list
    def removeListItem(self, list_item, quantity=None):
        if quantity is None:
            quantity = 1
        # Check that ID exists as index
        if len(self.list_items) > list_item:
            if quantity >= self.list_items[list_item].quantity:
                self.list_items.pop(list_item)
                return True
            else:
                self.list_items[list_item].quantity -= quantity
                return True

        # ID given didnt not exist as index so we return false
        return False

    def updateItem(self, list_item, name=None, description=None):
        # Check that ID exists as index in our list
        if len(self.list_items) > list_item:
            # Update name if new name provided
            if name is not None:
                self.list_items[list_item].setName(name)
            # Update description if new description provided
            if description is not None:
                self.list_items[list_item].setDescription(description)

        # ID given didnt not exist as index so we return false
        return False


class ListItem():
    """This file contains the ListItem class This class models the attirbutes
     and behaviours of an individual list item
    """
    def __init__(self, name, description, quantity=None):
        self.name = name
        self.description = description
        if quantity is None:
            quantity = 1
        self.quantity = quantity

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description
