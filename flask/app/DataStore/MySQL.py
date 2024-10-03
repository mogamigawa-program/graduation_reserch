import mysql.connector

class MySQL:
    def __init__(self, **dns):
        self.dns = dns
        self.dbh = None

    def _open(self):
        self.dbh = mysql.connector.MySQLConnection(**self.dns)

    def _close(self):
        if self.dbh:
            self.dbh.close()

    def query(self, stmt, *args, **kwargs):
        try:
            self._open()
            if kwargs.get('prepared', False):
                cursor = self.dbh.cursor(prepared=True)
                cursor.execute(stmt, args)
            else:
                cursor = self.dbh.cursor()
                cursor.execute(stmt)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            # エラーハンドリング: エラーが発生した場合の処理を記述
            print(f"Error: {e}")
        finally:
            self._close()
