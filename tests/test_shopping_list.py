"""Test cases for the shopping list application

This file contains test cases used to build the
shopping list app
"""
from unittest import TestCase
from app.classes import ShoppingListApp


class TestRegisterUser(TestCase):
    """Handles Test cases for user sign up features"""

    def setUp(self):
        self.app = ShoppingListApp()

    def test_register_successfully(self):
        users_before = len(self.app.users)
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')
        users_after = len(self.app.users)

        """check that user object creates succesfully
        and number of users increased by users created"""
        self.assertEqual(users_after, users_before + 1)


class TestCreateList(TestCase):
    """ Handles test cases for create list feature"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_creates_list_successfully(self):
        lists_before = len(self.app.shopping_lists)
        self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        lists_after = len(self.app.shopping_lists)

        """check that user object creates succesfully
        and number of items increased by items created"""
        self.assertEqual(lists_after, lists_before + 1)

    def test_create_list_fails_if_user_doesnt_exist(self):
        self.assertRaises(Exception, self.app.createShoppingList,
                          'Back to school', 'school shopping list',
                          'fakeUser@gmail.com')


class TestAddItemToList(TestCase):
    """ Handles test case for adding items to shopping list"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

        # Lets create a sample list
        self.shopping_list = self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        # Then we create a list item object
        self.list_item = self.app.registerItem(
            'sugar', 'sweet substance that kills people')

    def test_adds_item_successfully(self):
        # we count number of items before
        items_before = len(self.shopping_list.list_items)
        # Then add an item
        self.app.userAddItemToList(self.shopping_list, self.list_item, 1)
        # And count the items after adding a new one
        items_after = len(self.shopping_list.list_items)

        """check that that item created succesfully by assering that
        the number of items increased by number of items created"""
        self.assertEqual(items_after, items_before + 1)


class TestEditList(TestCase):
    """ Handles test cases for edit list feature"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_edit_shoppinglist_successfully(self):
        # creates shopping list with id 0
        self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        list_id = len(self.app.shopping_lists) - 1

        result = self.app.editShoppingList(list_id, 'luwyxx@gmail.com',
                                           'Back to Primary School')
        self.assertTrue(result)


class TestUserLogsIn(TestCase):
    """ Handles test cases for user login functionality"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.user = self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_user_login_successfully(self):
        result = self.app.login('luwyxx@gmail.com', 'psw12345!')
        self.assertTrue(result)

    def test_user_login_fails_with_wrong_email(self):
        self.assertRaises(Exception, self.app.login,
                          'fakeUser@gmail.com', 'psw12345!')
