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
        """Test if that the methods to register user are wroking as expected
        """
        # Get the number of users before
        users_before = len(self.app.users)
        # Now add a new user
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')
        # The we get the number of users after
        users_after = len(self.app.users)

        """check that user object creates succesfully
        and number of users increased by users created"""
        self.assertEqual(users_after, users_before + 1)


class TestCreateList(TestCase):
    """ Handles test cases for create list methods"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_creates_list_successfully(self):
        """This method checks that the list is created as required"""
        # We get the number of lists stored before adding a new one
        lists_before = len(self.app.shopping_lists)
        # We attempt to add a list
        self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        # Then we get the number of lists stored after adding a new one
        lists_after = len(self.app.shopping_lists)

        """TO test the condition, we assert that number of items increased by
        items created
        """
        self.assertEqual(lists_after, lists_before + 1)

    def test_create_list_fails_if_user_doesnt_exist(self):
        """Test that adding a shopping list wont work if user doesnt exist"""
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
        """Test that items are added to a list correctly"""
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
        """Test that editing shopping list works correct"""
        # creates shopping list with id 0
        self.app.createShoppingList(
            'Back to school', 'school shopping list', 'luwyxx@gmail.com')
        list_id = len(self.app.shopping_lists) - 1
        # We edit the shopping list
        result = self.app.editShoppingList(list_id, 'luwyxx@gmail.com',
                                           'Back to Primary School')
        # We assert that the function returns True when edit is succesful
        self.assertTrue(result)


class TestUserLogsIn(TestCase):
    """ Handles test cases for user login functionality"""

    def setUp(self):
        self.app = ShoppingListApp()
        self.user = self.app.registerUser(
            'patrick', 'alvin', 'luwyxx@gmail.com', 'psw12345!')

    def test_user_login_successfully(self):
        """This method tests that the user login methods of the application
        function as required
        """
        # We attempt to create the user
        result = self.app.login('luwyxx@gmail.com', 'psw12345!')
        # To check the condition, we assert that the method returns True
        self.assertTrue(result)

    def test_user_login_fails_with_wrong_email(self):
        """This method tests if an exception is raised when a non user
        attempts to login
        """
        self.assertRaises(Exception, self.app.login,
                          'fakeUser@gmail.com', 'psw12345!')
