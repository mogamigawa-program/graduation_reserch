mariaDBを入れる。基本的に安定しているバージョンならなんでも大丈夫。わからなければ卒論に書いてあるバージョンを使用してください。

pythonとflaskもインストールする。こちらは基本的にインストールするとき最新バージョンを入れる。

mariaDBのデータベースを用意する。

dataset：中野先輩の卒論を見て定義を確認してテーブルを作ってテーブル名に合う適当なデータを入れてください。usersは渡邉の卒論を確認して同様にテーブル作ってデータ入れてください。
user_info：渡邉の卒論見てテーブル作ってみてください。


mariaDB
root
pass:0734

how to using mariaDB(windowsで使う方法)

mysql client を開く
passを入力

databaseにinsertをしたい場合、MySQL.pyのmethodを使うのではなく
その場でmysql.connector.MySQLConnectionを定義してmethodを使っていく
commitしないとdatabaseに反映されない

run.pyをターミナル上で実行するとアプリが起動します。
コマンド上にURLが表示されるのでこのURLを実際にブラウザで入力するとアプリが触れます。