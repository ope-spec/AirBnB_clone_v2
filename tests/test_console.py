#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from unittest import TestCase
from io import StringIO
import os
import sys
sys.path.append("..")
from console import HBNBCommand
from io import StringIO
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """
    Test cases for the HBNBCommand class.
    """

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.console = HBNBCommand()

    def setUp(self):
        """
        Set up the test environment by creating an instance of HBNBCommand and
        redirecting stdout to a StringIO object for capturing output.
        """
        self.console = HBNBCommand()
        self.saved_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out

    @classmethod
    def tearDownClass(cls):
        """Cleanup after the test"""
        del cls.console

    def tearDown(self):
        """
        Restore the original stdout after each test case.
        """
        sys.stdout = self.saved_stdout

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """
        Test the quit command to ensure that the program exits properly.
        """
        with self.assertRaises(SystemExit):
            self.console.onecmd("quit")
        self.assertEqual(self.out.getvalue(), "")

    def test_create_missing_class_name(self):
        """
        Test create command with missing class name.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

    def test_create_nonexistent_class(self):
        """
        Test create command with nonexistent class name.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_show_missing_class_name(self):
        """Test show command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

    def test_show_nonexistent_class(self):
        """Test show command with nonexistent class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_show_missing_instance_id(self):
        """Test show command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

    def test_show_nonexistent_instance(self):
        """Test show command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy_missing_class_name(self):
        """Test destroy command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

    def test_destroy_nonexistent_class(self):
        """Test destroy command with nonexistent class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_destroy_missing_instance_id(self):
        """Test destroy command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

    def test_destroy_nonexistent_instance(self):
        """Test destroy command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all_nonexistent_class(self):
        """Test all command with nonexistent class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_all_empty_class(self):
        """Test all command with empty class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update_missing_class_name(self):
        """Test update command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

    def test_update_nonexistent_class(self):
        """Test update command with nonexistent class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_update_missing_instance_id(self):
        """Test update command with missing instance id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

    def test_update_nonexistent_instance(self):
        """Test update command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update_missing_attribute_name(self):
        """Test update command with missing attribute name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())

    def test_update_missing_value(self):
        """Test update command with missing value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

if __name__ == "__main__":
    unittest.main()
