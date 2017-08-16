"""Test cases for the shopping list application

This file contains test cases used to build the 
shopping list app
"""
from unittest import TestCase
from classes.app import App


class TestRegisterUser(TestCase):

    """Handles Test cases for user sign up features"""

    def setUp(self):
        self.app = App()

    def test_register_successfully(self):
        usersBefore = len(self.app.users)
        result = self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')
        usersAfter = len(self.app.users)

        """check that user object creates succesfully 
        and number of users increased by users created"""
        self.assertListEqual([True, usersAfter], [result, usersBefore + 1])


class TestCreateItem(TestCase):
    """ Handles test cases for create new item"""

    def setUp(self):
        self.app = App()

    def test_creates_item_successfully(self):
        itemsBefore = len(self.app.listItems)
        result = self.app.registerItem(
            'sugar', 'sweet substance that kills people')
        itemsAfter = len(self.app.listItems)

        """check that user object creates succesfully 
        and number of items increased by items created"""
        self.assertListEqual([True, itemsAfter], [result, itemsBefore + 1])


class TestCreateList(TestCase):
    """ Handles test cases for create list feature"""

    def setUp(self):
        self.app = App()

    def test_creates_list_successfully(self):
        listsBefore = len(self.app.shoppingLists)
        result = self.app.createShoppingList(
            'Back to school', 'school shopping list')
        listsAfter = len(self.app.shoppingLists)

        """check that user object creates succesfully 
        and number of items increased by items created"""
        self.assertListEqual([True, listsAfter], [result, listsBefore + 1])
