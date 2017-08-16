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
        result = self.app.registerUser('patrick','alvin','luwyxx@gmail.com','psw12345!')
        usersAfter = len(self.app.users)
        
        """check that user object creates succesfully 
        and number of users increased by users created"""
        self.assertListEqual([True, usersAfter], [result, usersBefore+1])