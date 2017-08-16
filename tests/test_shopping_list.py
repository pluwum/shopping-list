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
        users_before = len(self.app.users)
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')
        users_after = len(self.app.users)

        """check that user object creates succesfully
        and number of users increased by users created"""
        self.assertEqual(users_after, users_before + 1)


class TestCreateItem(TestCase):
    """ Handles test cases for create new item"""

    def setUp(self):
        self.app = App()

    def test_creates_item_successfully(self):
        items_before = len(self.app.list_items)
        self.app.registerItem(
            'sugar', 'sweet substance that kills people')
        items_after = len(self.app.list_items)

        """check that user object creates succesfully
        and number of items increased by items created"""
        self.assertEqual(items_after, items_before + 1)


class TestCreateList(TestCase):
    """ Handles test cases for create list feature"""

    def setUp(self):
        self.app = App()

    def test_creates_list_successfully(self):
        lists_before = len(self.app.shopping_lists)
        self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        lists_after = len(self.app.shopping_lists)

        """check that user object creates succesfully
        and number of items increased by items created"""
        self.assertEqual(lists_after, lists_before + 1)


class TestAddItemToList(TestCase):
    """ Handles test case for adding items to shopping list"""

    def setUp(self):
        self.app = App()
        self.shopping_list = self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')

        self.list_item = self.app.registerItem(
            'sugar', 'sweet substance that kills people')

    def test_adds_item_successfully(self):
        items_before = len(self.shopping_list.list_items)
        self.app.userAddItemToList(self.shopping_list, self.list_item, 1)
        items_after = len(self.shopping_list.list_items)

        """check that user object creates succesfully
        and number of items increased by items created"""
        self.assertEqual(items_after, items_before + 1)


class TestUserLogsIn(TestCase):
    """ Handles test cases for user login functionality"""

    def setUp(self):
        self.app = App()
        self.user = self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_user_login_successfully(self):
        result = self.app.login('luwyxx@gmail.com', 'psw12345!')
        self.assertTrue(result)

    def test_user_login_fails_with_wrong_email(self):
        self.assertRaises(Exception, self.app.login,
                          'luwy@gmail.com', 'psw12345!')
