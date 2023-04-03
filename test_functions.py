import unittest
from unittest import TestCase
import functions
from unittest import mock
import sqlite3

def check_query(query: str, commit: bool):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        response = cur.execute(f"{query}")
        if commit: con.commit()
    return response
        
class TestApp(TestCase):

    @classmethod
    def setUpClass(cls):
        check_query("INSERT INTO levels ('user_id', 'technology', 'level', 'experience', 'favourite') VALUES (20, 'test', 10, 'none', 'False')", True)

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
        response = functions.search_users("python")
        self.assertTrue(len(response) > 0)

    def test_search_unknown_technology(self):
        response = functions.search_users("bar")
        self.assertFalse(response)

    def test_search_all_users(self):
        response = functions.get_all_users()
        self.assertEqual(len(response), 21)

    def test_add_skill(self):
        response = functions.add_skill(20, "test", 10, None, False)

        self.assertEqual(response, 200)
    
    def test_delete_skill(self):
        response = functions.delete_skill_db(20, "test")
        self.assertEqual(response, 200)

    def test_update_skill(self):
        mock_response = functions.add_skill(20, "test", 10, None, False)
        self.assertEqual(mock_response, 200)
        
        response = functions.update_skill_db(20, "test", 5, None, True)
        self.assertEqual(response, 200)

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            response = cur.execute(f"SELECT level, favourite FROM levels WHERE user_id = '20' AND technology = 'test'").fetchall()

        self.assertEqual(response, [(5, 'True')])


    @classmethod
    def tearDownClass(cls):
        check_query("DELETE FROM levels WHERE technology = 'test'", True)

unittest.main()