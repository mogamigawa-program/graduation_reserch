import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",          # MariaDBサーバーのホスト
            user="root",          # ユーザー名（rootも可）
            password="0734",  # パスワード
            database="user_info"   # データベース名
        )

        if conn.is_connected():
            print("✅ MariaDB に接続成功！")

            cursor = conn.cursor()
            cursor.execute("SELECT NOW();")  # 現在時刻を取得
            result = cursor.fetchone()
            print("サーバー時刻:", result[0])

            cursor.close()
            conn.close()
        else:
            print("❌ 接続できませんでした")

    except Error as e:
        print("接続エラー:", e)

if __name__ == "__main__":
    test_connection()