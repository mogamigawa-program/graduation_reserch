from app.app import app

if __name__ == "__main__":
    app.run(debug=True)

#host='0.0.0.0', port=5000, を追加するとローカルネットワークでアクセス可能
#ローカルアクセス用：http://127.0.0.1:5000
#ネットワーク内アクセス用（荒木）：http://192.168.0.4:5000
