import unittest
from unittest.mock import patch
from io import StringIO

from insta360_gfpt.main import main

class TestMain(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_hello_command(self, mock_stdout):
        with patch('sys.argv', ['mycli', 'hello', '--option', 'World']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

    @patch('sys.stdout', new_callable=StringIO)
    def test_info_command(self, mock_stdout):
        with patch('sys.argv', ['mycli', 'info', '--option', 'Some info']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Info: Some info")

if __name__ == "__main__":
    unittest.main()