import unittest
from unittest.mock import MagicMock, patch
from unittest import TestCase
import functions


mock_db = MagicMock()

mock_db.query.return_value = [(1, 'Item 1'), (2, 'Item 2')]


class TestApp(TestCase):

    @patch('my_module.sqlite3.connect', return_value=mock_db)
    def test_add_skill(mock_connect):
        items = functions.get_all_users()
        assert items == True




unittest.main()
