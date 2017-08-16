"""This file contains the Shopping List class definition
This class represents each shopping list and the generic
attributes it has
"""


class ShoppingList():
    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.list_items = {}

    def addListItem(self, list_item, quantity=None):
        if quantity is None:
            quantity = 1

        self.list_items[list_item] = quantity
        return True
