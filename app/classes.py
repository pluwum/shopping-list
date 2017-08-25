"""This file contains the ShoppingListApp, User, ShoppingList and ListItem
classes. Together, they provide the logic for a simple shopping list
application.
The App class is the main application class
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
    """This is the overall application class. It leverages all other classes
    to achieve the functionalities required of the shopping list app
    """

    def __init__(self):
        # User's database: Tracks users in the system
        self.users = {}

        # Item database: Tracks items created
        self.list_items = {}

        # List Database: Tracks shopping lists created
        self.shopping_lists = {}

    def register_user(self, first_name, last_name, email, password):
        """Adds user to the application's user pool"""
        # Lets make sure the user is not registered already
        if email in self.users:
            raise Exception(
                "User already exists, Did you forget your password?")
        # We create a user object and store it in our user database
        user = User(first_name, last_name, email, password)
        self.users[email] = user
        return user

    def register_item(self, name, description):
        """Creates a new list item object"""
        if name in self.list_items:
            raise Exception(
                "Item already exists, Please try again")

        item = ListItem(name, description)
        self.list_items[name] = item
        return item

    def get_user_shopping_lists(self, email):
        """Given a user's email address, this method returns their shopping
        lists
        """
        # Check if user has shopping lists and then return what is found
        if email in self.shopping_lists:
            return self.shopping_lists[email]

        # We return an empty list when we find no lists
        return []

    def get_user_detail(self, email):
        """This gets the user object with details of the user specified by
         email
         """
        # First check that the user exists then return their details
        if email in self.users:
            return self.users[email]

        # When user not found, raise error
        raise Exception(
            "This user doesn't exist, Please login or register")

    def create_shopping_list(self, name, description, user_email):
        """This method creates a shopping list for a user"""
        # Check if required input parameter is missing
        if name is None or description is None or user_email is None:
            raise Exception("Missing Field:Please provide name & Description")

        # Check if this user really exists
        if user_email not in self.users:
            raise Exception(
                "Guest users are not allowed to create lists:Please "
                "register or log in"
            )

        # Create list Object
        shopping_list = ShoppingList(name, description, user_email)
        # Add list to user list tracker
        # Check if user already has a list
        if user_email in self.shopping_lists:
            users_lists = self.shopping_lists[user_email]

            # Check that the user does not have a list with the same name
            for user_list in users_lists:
                if user_list.name.lower() == name.lower():
                    raise Exception(
                        "You already have a list with the same name: "
                        "Please perform action again using new list name"
                    )
            # Add the new list to the users record
            users_lists.append(shopping_list)
        else:
            # Create a new list if this is the user's first shopping List
            self.shopping_lists[user_email] = [shopping_list]

        return shopping_list

    def edit_shopping_list(self, id, user_email, name=None, description=None):
        """This method edits the shopping list at index id and email"""
        # Make sure the list we are editing exists
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        if id is not None:
            # Find the list object we want to edit
            user_lists = self.shopping_lists[user_email]
            list_to_edit = user_lists[id]

            # Update name
            if name is not None:
                list_to_edit.set_name(name)

            # Update Description
            if description is not None:
                list_to_edit.set_description(description)

            # Update the object stored in our list tracker
            self.shopping_lists[user_email][id] = list_to_edit
            return True

        return False

    def get_shopping_list(self, id, user_email):
        """This method returns a shopping list given its ID and creator's
        email
        """
        # Check that user has shopping lists
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        if id is not None:
            # Get the shopping list we want to return
            user_lists = self.shopping_lists[user_email]
            return user_lists[id]

        raise Exception("Oops! List ID field was not received with request")

    def delete_shopping_list(self, id, user_email):
        """This method deletes shopping list with id and belong to user with
        email provided
        """
        # Make sure this user has lists to begin with
        if user_email not in self.shopping_lists:
            raise Exception("Oops! List does not exist in User's records")

        # Make sure the index is not out of bounds
        if len(self.shopping_lists[user_email]) > id:
            self.shopping_lists[user_email].pop(id)
            return True
        # Cause alarm if we dont find a list
        raise Exception("Oops! List does not exist")

    def user_add_item_to_list(self, shopping_list, item_name, description,
                              quantity=None):
        """This method adds an item to a shopping list"""
        # Lets check that everything we need is available
        if all(param is not None for param in [shopping_list, item_name,
                                               description]):
            # We create a new ListItem object and store it in the list
            list_item = ListItem(item_name, description, quantity)
            item_id = shopping_list.add_list_item(list_item, quantity)
            return item_id

        raise Exception(
            "Oops! Some parameters seem to be missing, please review")

    def user_update_item_in_list(self, shopping_list, list_item, item_name,
                                 description, quantity=None):
        """Updates the item in a list with name and desceiption"""
        shopping_list.update_item(list_item, item_name, description)

    def user_remove_item_from_list(self, shopping_list, list_item,
                                   quantity=None):
        """Removes a  single item from a given shopping list"""
        shopping_list.remove_list_item(list_item, quantity)
        return True

    def login(self, email, password):
        """This method authenticated use email and password against the database
        and returns true if they match"""
        # Lets find out if user exists
        if email not in self.users:
            raise Exception("User doesnt exists, Please add")
        # User exists, so lets get their data
        user = self.users[email]

        # Check if received password and email combinations match up
        if user.verify_credentials(email, password) is False:
            raise Exception(
                "Authentication Failed, Please check email and password")

        return True


class User():
    """The User class models the generic behaviour
and attributes of a user in the system
"""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_email():
        """Returns email address"""
        return self.email

    def verify_credentials(self, email, password):
        """Checks that email and password combination matches records"""
        if email == self.email and password == self.password:
            return True

        return False


class ShoppingList():
    """The Shopping List class definition
    This class represents each shopping list and the generic attributes it has
    """

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.list_items = []

    def set_name(self, name):
        """Updates name"""
        self.name = name

    def set_description(self, description):
        """Updates description"""
        self.description = description

    def get_list_items(self):
        """Returns all list items in shopping list"""
        return self.list_items

    def get_list_item(self, id):
        """Returns single list item"""
        if len(self.list_items) > id:
            return self.list_items[id]

    def add_list_item(self, list_item, quantity=None):
        """Adds Item to the shopping list"""
        # Check if similar item already in list
        for item in self.list_items:
            if list_item.name.lower() == item.name.lower():
                raise Exception("Error:Sorry, Item already exists in your"
                                "list, please choose another name")

        # When nothing is found, add item to list
        self.list_items.append(list_item)
        # Lets return the item's index to use as an ID
        return len(self.list_items) - 1

    def remove_list_item(self, list_item, quantity=None):
        """Removes item from shopping list"""
        if quantity is None:
            quantity = 1
        # Check that ID exists as index
        if len(self.list_items) > list_item:
            # Remove item if the quantity removed is greater to quantity stored
            if quantity >= self.list_items[list_item].quantity:
                self.list_items.pop(list_item)
                return True
            else:
                # Update quantity if quantity is less than stored quantitiy
                self.list_items[list_item].quantity -= quantity
                return True

        # ID given didnt not exist as index so we return false
        return False

    def update_item(self, list_item, name=None, description=None):
        """Updates a single item"""
        # Check that ID exists as index in our list
        if len(self.list_items) > list_item:
            # Update name if new name provided
            if name is not None:
                self.list_items[list_item].set_name(name)
            # Update description if new description provided
            if description is not None:
                self.list_items[list_item].set_description(description)

        # ID given didnt not exist as index so we return false
        return False


class ListItem():
    """This file contains the ListItem class This class models the attirbutes
     and behaviours of an individual list item
    """

    def __init__(self, name, description, quantity=None):
        self.name = name
        self.description = description
        # Default quantity to 1 if not passed on initialisation
        if quantity is None:
            quantity = 1
        self.quantity = quantity

    def set_name(self, name):
        """Updates item name"""
        self.name = name

    def set_description(self, description):
        """updates item descrption"""
        self.description = description
