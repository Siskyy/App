import unittest
from unittest.mock import patch
import functions


class TestDatabaseFunctions(unittest.TestCase):
    @patch('my_database.Database')
    def test_add_item(self, mock_db):
        # Mock the database so that we can control its behavior in the test
        mock_cursor = mock_db.return_value.cursor.return_value
        mock_cursor.lastrowid = 1

        # Call the add_item function with a mock item
        mock_item = {'name': 'Test Item', 'description': 'This is a test item'}
        result = add_item(mock_item)

        # Check that the item was added to the database
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            ('Test Item', 'This is a test item')
        )

    @patch('my_database.Database')
    def test_delete_item(self, mock_db):
        # Mock the database so that we can control its behavior in the test
        mock_cursor = mock_db.return_value.cursor.return_value

        # Call the delete_item function with a mock item ID
        result = delete_item(1)

        # Check that the item was deleted from the database
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM items WHERE id = ?",
            (1,)
        )
