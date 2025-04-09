import unittest
import mysql.connector
from DataStore.MySQL import MySQL
class MySQLTest(unittest.TestCase):

    def setUp(self):
        self.dns = {
            'host': 'localhost',
            'user': 'root',
            'password': '0734',
            'database': 'dataset'
        }
        self.db = MySQL(**self.dns)

    def tearDown(self):
        self.db._close()

    def test_query_without_prepared_statement(self):
        stmt = 'SELECT * FROM users'
        data = self.db.query(stmt)
        self.assertEqual(len(data), 2)

    def test_query_with_prepared_statement(self):
        stmt = 'SELECT * FROM users WHERE email = %s'
        email = 'webmaster@python.org'
        data = self.db.query(stmt, prepared=True, email=email)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], email)

if __name__ == '__main__':
    unittest.main()
