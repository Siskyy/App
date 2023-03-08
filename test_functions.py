import unittest
from unittest import TestCase
import functions
from unittest import mock
import sqlite3

class TestApp(TestCase):

    @classmethod
    def setUpClass(cls):
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                f"INSERT INTO levels ('user_id', 'technology', 'level', 'experience', 'favourite') VALUES (15, 'test', 10, 'none', 'False')"
                )
            con.commit()


    def test_login_valid(self):
        response = functions.check_credentials("marcbert", "password")
        self.assertEqual(response[0], True)

    def test_login_invalid_username(self):
        response = functions.check_credentials("foo", "password")
        self.assertEqual(response, [False, "User 'foo' does not exist!"])

    def test_login_invalid_password(self):
        response = functions.check_credentials("marcbert", "foo")
        self.assertEqual(response, [False, "Password Incorrect! Try again"])

    def test_search_by_technology(self):
        response = functions.search_users("test")
        self.assertEqual(response[0][0], "joshader")

    def test_search_unknown_technology(self):
        response = functions.search_users("bar")
        self.assertFalse(response)

    def test_search_all_users(self):
        response = functions.get_all_users()
        self.assertEqual(len(response), 21)

    def test_add_skill(self):
        response = functions.add_skill(20, "foo", 10, None, False)

        self.assertEqual(response, 200)
        self.assertTrue(True)
    
    def test_delete_skill(self):
        response = functions.delete_skill_db(20, "foo")
        self.assertEqual(response, 200)

    @classmethod
    def tearDownClass(cls):
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM levels WHERE technology = 'test'")
            con.commit()

unittest.main()