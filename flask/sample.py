import mysql.connector

dns = {
    'host': 'localhost',
    'user': 'root',
    'password': '0734',
    'database': 'dataset'
}

# 接続を作成して、1 つのレコードを読み込む
connection = mysql.connector.MySQLConnection(**dns)
cursor = connection.cursor()
cursor.execute('SELECT * FROM users WHERE email = %s', ('webmaster@python.org',))
result = cursor.fetchone()
print(result)

# 接続を再利用して、すべてのレコードを読み込む
cursor.fetchall()
cursor.execute('SELECT * FROM users')
results = cursor.fetchall()
print(results)
