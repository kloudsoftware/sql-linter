import unittest
from php_parser import parse_php_for_mysql_statements

class TestStringMethods(unittest.TestCase):

    def test_parser(self):
        fd = "test.php"

        matches = parse_php_for_mysql_statements(fd)
        self.assertEqual(10, len(matches))

if __name__ == '__main__':
    unittest.main()
