#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,request,session,flash

from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_bcrypt import Bcrypt

import mysql.connector

from DataStore.MySQL import MySQL
dns = {
    'user': 'root',
    'host': 'localhost',
    'password': '0734',
    'database': 'dataset',
    'auth_plugin': 'mysql_native_password'
}
user_dns = {
    'user': 'root',
    'host': 'localhost',
    'password': '0734',
    'database': 'user_info',
    'auth_plugin': 'mysql_native_password'
}
this_users_dns = {
    'user': 'root',
    'host': 'localhost',
    'password': '0734',
    'auth_plugin': 'mysql_native_password',
    'database': None 
}

db = MySQL(**dns)
user_db = MySQL(**user_dns)
this_users_db = MySQL(**this_users_dns)

#Flaskオブジェクトの生成
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt(app)

# ログインが必要なページ
protected_pages = ['/index', '/users', '/multiple_users', '/primary_school', '/multiple_primary_school', '/sisya',
                   '/multiple_sisya', '/choose', '/join', '/cross_join', '/inner_join', '/left_join', '/create_table']

# before_request フィルタでログインの確認を行う
@app.before_request
def check_login():
    # ログインが必要なページにアクセスする場合、ログインしているか確認
    if request.path in protected_pages and 'user_id' not in session:
        return redirect(url_for('login'))

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/index")
def main():
    props = {'title': 'データベースアプリ', 'msg': 'データベース学習用ページへようこそ'}
    html = render_template('index.html', props=props)
    return html
    
#「/hello」へアクセスがあった場合に、「hello.html」を返す
@app.route('/hello')
def hello():
    props = {'title': 'Step-by-Step Flask - hello', 'msg': 'Hello World.'}
    html = render_template('hello.html', props=props)
    return html

#条件を１つのみ入力前画面。(cities)
@app.route('/users')
def users():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_cities'
    users = db.query(stmt)
    html = render_template('users.html', props=props, users=users)
    return html

#条件を１つのみ入力後画面。(cities)   
@app.route('/users',methods=["post"], endpoint='/users')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    
    if stmt1 == 'cities':
        users = 'select id, name, population, true from cities where ' + stmt2
        users_select = db.query(users)
        All = 'select cities.id, cities.name, cities.population, result_cities.id from cities left join (select id, true from cities where ' + stmt2 +') as result_cities on result_cities.id=cities.id order by cities.id asc'
        All_select = db.query(All)
        html = render_template('dif_result.html', props=props, All_select=All_select, users_select=users_select)
        return html
        
    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html


#条件が複数ある場合の入力前画面。(cities)
@app.route('/multiple_users')
def multiple_users():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_cities'
    users = db.query(stmt)
    html = render_template('multiple_select_users.html', props=props, users=users)
    return html


#条件が複数ある場合の入力後画面。(cities)
@app.route('/multiple_users',methods=["post"],endpoint='/multiple_users')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    
    if stmt1 == 'cities':
        if stmt3!=None and stmt4!=None:
            users = 'select id, name, population, true from cities where ' + stmt2 + ' ' + stmt3 + ' ' + stmt4
            users_select = db.query(users)
            All = 'select cities.id, cities.name, cities.population, result_cities.id from cities left join (select id, true from cities where ' + stmt2 + ' ' + stmt3 + ' ' + stmt4 + ') as result_cities on result_cities.id=cities.id order by cities.id asc'
            All_select = db.query(All)
            html = render_template('multiple_users.html', props=props, All_select=All_select, users_select=users_select)
            return html
        
        elif stmt3==None and stmt4==None:
            users = 'select id, name, population, true from cities where ' + stmt2
            users_select = db.query(users)
            All = 'select cities.id, cities.name, cities.population, result_cities.id from cities left join (select id, true from cities where ' + stmt2 + ') as result_cities on result_cities.id=cities.id order by cities.id asc'
            All_select = db.query(All)
            html = render_template('multiple_users.html', props=props, All_select=All_select, users_select=users_select)
            return html

        else:
            stmt = 'SELECT * FROM result_cities'
            users = db.query(stmt)
            html = render_template('multiple_users.html', props=props, users=users)
            return html

    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html



#条件を１つのみ入力前画面。(pschool)
@app.route('/primary_school')
def primary_school():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_pschool'
    users = db.query(stmt)
    html = render_template('primary_school.html', props=props, users=users)
    return html


#条件を１つのみ入力後画面。(pschool)
@app.route('/primary_school',methods=["post"], endpoint='/primary_school')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    
    if stmt1 =='pschool':
        users = 'select id, category, name, true from pschool where ' + stmt2
        users_select = db.query(users)
        All = 'select pschool.id, pschool.category, pschool.name, result_pschool.id from pschool left join (select id, true from pschool where '+ stmt2 +') as result_pschool on result_pschool.id=pschool.id order by pschool.id asc'
        All_select = db.query(All)
        html = render_template('result_primary_school.html', props=props, All_select=All_select, users_select=users_select)
        return html

    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html


#条件が複数ある場合の入力前画面。(pschool)
@app.route('/multiple_primary_school')
def multiple_primary_school():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_pschool'
    users = db.query(stmt)
    html = render_template('multiple_select_primary_school.html', props=props, users=users)
    return html


#条件が複数ある場合の入力後画面。(pschool)
@app.route('/multiple_primary_school',methods=["post"], endpoint='/multiple_primary_school')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    if stmt1 =='pschool':
        if stmt3!=None and stmt4!=None:
            users = 'select id, category, name, true from pschool where ' + stmt2 + ' ' + stmt3 + ' ' + stmt4
            users_select = db.query(users)
            All = 'select pschool.id, pschool.category, pschool.name, result_pschool.id from pschool left join (select id, true from pschool where '+ stmt2 + ' ' + stmt3 + ' ' + stmt4 + ') as result_pschool on result_pschool.id=pschool.id order by pschool.id asc'
            All_select = db.query(All)
            html = render_template('multiple_primary_school.html', props=props, All_select=All_select, users_select=users_select)
            return html
                
        elif stmt3==None and stmt4==None:
            users = 'select id, category, name, true from pschool where ' + stmt2
            users_select = db.query(users)
            All = 'select pschool.id, pschool.category, pschool.name, result_pschool.id from pschool left join (select id, true from pschool where '+ stmt2 +') as result_pschool on result_pschool.id=pschool.id order by pschool.id asc'
            All_select = db.query(All)
            html = render_template('multiple_primary_school.html', props=props, All_select=All_select, users_select=users_select)
            return html

        else:
            stmt = 'SELECT * FROM result_pschool'
            users = db.query(stmt)
            html = render_template('primary_school.html', props=props, users=users)
            return html

    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html



#条件を１つのみ入力前画面。(sisya)
@app.route('/sisya')
def sisya():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_sisya'
    users = db.query(stmt)
    html = render_template('sisya.html', props=props, users=users)
    return html


#条件を１つのみ入力後画面。(sisya)
@app.route('/sisya',methods=["post"], endpoint='/sisya')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    if stmt1 == 'sisya':
        users = 'select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2
        users_select = db.query(users)
        All = 'select sisya.id, sisya.year, sisya.all_died, sisya.child_died, sisya.old_died, result_sisya.id from sisya left join (select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2 + ') as result_sisya on result_sisya.id = sisya.id order by sisya.id asc'
        All_select = db.query(All)
        html = render_template('result_sisya.html', props=props, All_select=All_select, users_select=users_select)
        return html

    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html


#条件が複数ある場合の入力前画面。(sisya)
@app.route('/multiple_sisya')
def multiple_sisya():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    stmt = 'SELECT * FROM result_sisya'
    users = db.query(stmt)
    html = render_template('multiple_select_sisya.html', props=props, users=users)
    return html


#条件が複数ある場合の入力後画面。(sisya)
@app.route('/multiple_sisya',methods=["post"], endpoint='/multiple_sisya')
def post():
    props = {'title': '検索結果表示', 'msg': '検索結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    if stmt1 == 'sisya':
        if stmt3!=None and stmt4!=None:
            users = 'select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2 + ' ' + stmt3 + ' ' + stmt4
            users_select = db.query(users)
            All = 'select sisya.id, sisya.year, sisya.all_died, sisya.child_died, sisya.old_died, result_sisya.id from sisya left join (select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2 + ' ' + stmt3 + ' ' + stmt4 + ') as result_sisya on result_sisya.id = sisya.id order by sisya.id asc'
            All_select = db.query(All)
            html = render_template('multiple_sisya.html', props=props, All_select=All_select, users_select=users_select)
            return html

        elif stmt3==None and stmt4==None:
            users = 'select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2
            users_select = db.query(users)
            All = 'select sisya.id, sisya.year, sisya.all_died, sisya.child_died, sisya.old_died, result_sisya.id from sisya left join (select id, year, all_died, child_died, old_died, true from sisya where ' + stmt2 + ') as result_sisya on result_sisya.id = sisya.id order by sisya.id asc'
            All_select = db.query(All)
            html = render_template('multiple__sisya.html', props=props, All_select=All_select, users_select=users_select)
            return html
            
        else:
            stmt = 'SELECT * FROM result_sisya'
            users = db.query(stmt)
            html = render_template('sisya.html', props=props, users=users)
            return html

    else:
        props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
        html = render_template('choose.html', props=props)
        return html



#テーブル選択ページ
@app.route('/choose')
def choose():
    props = {'title': 'テーブル選択ページ', 'msg': 'テーブルを選択してください。'}
    html = render_template('choose.html', props=props)
    return html


#テーブル選択ページのセレクトボックスの処理
@app.route('/choose', methods=["post"])
def post():
    props = {'title': '検索前', 'msg': '条件を追加して検索しよう'}
    name = request.form.get('table')
    
    if name == "cities":
        stmt = 'SELECT * FROM result_cities'
        users = db.query(stmt)
        html_cities = render_template('users.html', props=props, users=users)
        return html_cities
        
    elif name == "primary school":
        stmt = 'SELECT * FROM result_pschool'
        users = db.query(stmt)
        html_pschool = render_template('primary_school.html', props=props, users=users)
        return html_pschool
        
    else:
        stmt = 'SELECT * FROM result_sisya'
        users = db.query(stmt)
        html = render_template('sisya.html', props=props, users=users)
        return html



#結合前の最初のページ
@app.route('/join')
def join():
    props = {'title': '結合ページ', 'msg': 'テーブルの結合の様子を見てみよう'}
    stmt1 = 'SELECT * FROM team'
    stmt2 = 'SELECT * FROM user'
    team = db.query(stmt1)
    user = db.query(stmt2)
    html = render_template('join.html', props=props, team=team, user=user)
    return html


@app.route('/join',methods=["post"],endpoint='/join')
def post():
    props = {'title': '結合結果表示', 'msg': '結合結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    stmt5 = request.form.get('name5')

    columns = request.form.get('name6')
    result = columns.split(',')
    length = len(result)

    db_team = 'SELECT * FROM team'
    db_user = 'SELECT * FROM user'
    team = db.query(db_team)
    user = db.query(db_user)

    if (stmt1 == 'team' and stmt3 == 'user') or (stmt1 == 'user' and stmt3 == 'team'):
        if stmt2 == 'cross join':
            if stmt4 == '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            elif stmt4 == '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' WHERE ' + stmt5
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            elif stmt4 != '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            
        elif stmt2 == 'inner join':
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html
                
            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' where ' + stmt5
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html


        else:
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html

            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' where ' + stmt5
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html
                
            
    else:
        props = {'title': '結合ページ', 'msg': 'テーブルの結合の様子を見てみよう'}
        stmt1 = 'SELECT * FROM team'
        stmt2 = 'SELECT * FROM user'
        team = db.query(stmt1)
        user = db.query(stmt2)
        html = render_template('join.html', props=props, team=team, user=user)
        return html


#cross joinのページ
@app.route('/cross_join')
def cross_join():
    props = {'title': 'クロス結合ページ', 'msg': 'クロス結合の結果を見てみよう'}
    stmt1 = 'SELECT * FROM team'
    stmt2 = 'SELECT * FROM user'
    team = db.query(stmt1)
    user = db.query(stmt2)
    stmt3 = 'SELECT * FROM team CROSS JOIN user'
    cross_join = db.query(stmt3)
    html = render_template('cross_join.html', props=props, team=team, user=user, cross_join=cross_join)
    return html




@app.route('/cross_join',methods=["post"],endpoint='/cross_join')
def post():
    props = {'title': '結合結果表示', 'msg': '結合結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    stmt5 = request.form.get('name5')

    columns = request.form.get('name6')
    result = columns.split(",")
    length = len(result)

    db_team = 'SELECT * FROM team'
    db_user = 'SELECT * FROM user'
    team = db.query(db_team)
    user = db.query(db_user)

    if (stmt1 == 'team' and stmt3 == 'user') or (stmt1 == 'user' and stmt3 == 'team'):
        if stmt2 == 'cross join':
            if stmt4 == '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 == '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' WHERE ' + stmt5 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            elif stmt4 != '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            
        elif stmt2 == 'inner join':
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html
                
            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' where ' + stmt5
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html


        else:
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html

            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' where ' + stmt5
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result =result, length=length)
                return html

    else:
        props = {'title': '結合ページ', 'msg': 'テーブルの結合の様子を見てみよう'}
        stmt1 = 'SELECT * FROM team'
        stmt2 = 'SELECT * FROM user'
        team = db.query(stmt1)
        user = db.query(stmt2)
        html = render_template('join.html', props=props, team=team, user=user)
        return html



#inner joinのページ
@app.route('/inner_join')
def inner_join():
    props = {'title': '内部結合ページ', 'msg': '内部結合の結果を見てみよう'}
    stmt1 = 'SELECT * FROM team'
    stmt2 = 'SELECT * FROM user'
    team = db.query(stmt1)
    user = db.query(stmt2)
    stmt3 = 'SELECT * FROM team INNER JOIN user ON team.team_id = user.team_id'
    inner_join = db.query(stmt3)
    html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join)
    return html


@app.route('/inner_join',methods=["post"],endpoint='/inner_join')
def post():
    props = {'title': '結合結果表示', 'msg': '結合結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    stmt5 = request.form.get('name5')

    columns = request.form.get('name6')
    result = columns.split(",")
    length = len(result)

    db_team = 'SELECT * FROM team'
    db_user = 'SELECT * FROM user'
    team = db.query(db_team)
    user = db.query(db_user)

    if (stmt1 == 'team' and stmt3 == 'user') or (stmt1 == 'user' and stmt3 == 'team'):
        if stmt2 == 'cross join':
            if stmt4 == '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            elif stmt4 == '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' WHERE ' + stmt5 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
            
        elif stmt2 == 'inner join':
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html

            else: 
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html

        else:
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html

                
            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html   
            
    else:
        props = {'title': '結合ページ', 'msg': 'テーブルの結合の様子を見てみよう'}
        stmt1 = 'SELECT * FROM team'
        stmt2 = 'SELECT * FROM user'
        team = db.query(stmt1)
        user = db.query(stmt2)
        html = render_template('join.html', props=props, team=team, user=user)
        return html



#left joinのページ
@app.route('/left_join')
def left_join():
    props = {'title': 'left joinページ', 'msg': 'left joinの結果を見てみよう'}
    stmt1 = 'SELECT * FROM team'
    stmt2 = 'SELECT * FROM user'
    team = db.query(stmt1)
    user = db.query(stmt2)
    stmt3 = 'SELECT * FROM team LEFT JOIN user ON team.team_id = user.team_id'
    left_join = db.query(stmt3)
    html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join)
    return html


@app.route('/left_join',methods=["post"],endpoint='/left_join')
def post():
    props = {'title': '結合結果表示', 'msg': '結合結果！'}
    stmt1 = request.form.get('name1')
    stmt2 = request.form.get('name2')
    stmt3 = request.form.get('name3')
    stmt4 = request.form.get('name4')
    stmt5 = request.form.get('name5')

    columns = request.form.get('name6')
    result = columns.split(",")
    length = len(result)

    db_team = 'SELECT * FROM team'
    db_user = 'SELECT * FROM user'
    team = db.query(db_team)
    user = db.query(db_user)

    if (stmt1 == 'team' and stmt3 == 'user') or (stmt1 == 'user' and stmt3 == 'team'):
        if stmt2 == 'cross join':
            if stmt4 == '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
                
            elif stmt4 == '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' WHERE ' + stmt5 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html

            elif stmt4 != '' and stmt5 != '':
                join = 'SELECT ' + columns + ' FROM ' +  stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                cross_join = db.query(join)
                html = render_template('cross_join.html', props=props, team=team, user=user, cross_join = cross_join, result=result, length=length)
                return html
            
        elif stmt2 == 'inner join':
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html

            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' +  stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                inner_join = db.query(join)
                html = render_template('inner_join.html', props=props, team=team, user=user, inner_join=inner_join, result=result, length=length)
                return html

        else:
            if stmt5 == '':
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html

            else:
                join = 'SELECT ' + columns + ' FROM ' + stmt1 + ' ' + stmt2 + ' ' + stmt3 + ' ON ' + stmt4 + ' WHERE ' + stmt5
                left_join = db.query(join)
                html = render_template('left_join.html', props=props, team=team, user=user, left_join=left_join, result=result, length=length)
                return html   
            
    else:
        props = {'title': '結合ページ', 'msg': 'テーブルの結合の様子を見てみよう'}
        stmt1 = 'SELECT * FROM team'
        stmt2 = 'SELECT * FROM user'
        team = db.query(stmt1)
        user = db.query(stmt2)
        html = render_template('join.html', props=props, team=team, user=user)
        return html


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if 'submit_button' in request.form:
        button_val = request.form['submit_button']
        insert_table_name = "users"
        #結果を表示する
        if button_val == 'result_btn':    
            columns = request.form.getlist('columns[]')
            values = request.form.getlist('values[]')

            # columns と values の中身を確認
            print("Columns:", columns)
            print("Values:", values)
            
            # 送られた情報をもとにインサートを実行する
            try:
                insert_data(insert_table_name, columns, values)
                table_desc, table = fetch_table_data(insert_table_name)
                
                message = "テーブルを更新しました。"
                
                return render_template('insert.html', table_name=insert_table_name, desc=table_desc, table=table, message=message)
            
            except Exception as e:
                # エラーが発生した場合の処理 エラーをinsert.htmlに表示するようにする。
                table_show = "SELECT * FROM " + insert_table_name
                users_table_desc = "desc " + insert_table_name
                
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(users_table_desc)
                table_desc = cursor.fetchall()
                cursor.execute(table_show)
                changed_table = cursor.fetchall()
                cursor.close()
                conn.commit()
                conn.close()
                
                return render_template('insert.html', table_name=insert_table_name, desc=table_desc, table=changed_table, error_message=str(e))
        #テーブルを初期化する    
        elif button_val == 'table_init_btn':
            try:
                user_db = this_users_dns['database']
                drop_table = f"drop table if exists users"
                
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                try:
                    cursor.execute(drop_table)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                cursor.close()
                conn.commit()
                conn.close()
                
                # ユーザーのデータベースにdataset内にあるusersをコピーする
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                copy_table_query = f"CREATE TABLE {user_db}.users AS SELECT * FROM dataset.users"
                try:
                    cursor.execute(copy_table_query)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                alter_table_query = f"ALTER TABLE {user_db}.users ADD PRIMARY KEY (id)"
                try:
                    cursor.execute(alter_table_query)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                cursor.close()
                conn.commit()
                conn.close()
                
                print("success")
                
                table_show = "SELECT * FROM " + insert_table_name
                users_table_desc = "desc " + insert_table_name
                
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(users_table_desc)
                table_desc = cursor.fetchall()
                cursor.execute(table_show)
                changed_table = cursor.fetchall()
                cursor.close()
                conn.commit()
                conn.close()
                
                message = "テーブルを初期化しました。"
            except Exception as e:
                message = "テーブルを初期化できませんでした。"
                
                table_show = "SELECT * FROM " + insert_table_name
                users_table_desc = "desc " + insert_table_name
                
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(users_table_desc)
                table_desc = cursor.fetchall()
                cursor.execute(table_show)
                changed_table = cursor.fetchall()
                cursor.close()
                conn.commit()
                conn.close()
            
            return render_template('insert.html', table_name=insert_table_name, desc=table_desc, table=changed_table, message=message)
    
    try:
        insert_table_name = "users"
        print(f"選択されたテーブル: {insert_table_name}")
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()
        users_table_desc = "desc " + insert_table_name
        cursor.execute(users_table_desc)
        
        table_desc = cursor.fetchall()
        print(table_desc)
        
        selected_table = "select * from " + insert_table_name
        cursor.execute(selected_table)
        
        table = cursor.fetchall()
        print(table)
        
        cursor.close()
        conn.commit()
        conn.close()
        
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"Error fetching tables: {e}")
        error_message = "An error occurred while fetching tables."
        return render_template('error.html', error_message=error_message)
    
    return render_template('insert.html', table_name=insert_table_name, desc=table_desc, table=table)

#DELETE文の学習ページ
@app.route('/delete/<type>', methods=['GET', 'POST'])
def delete(type):
    table_name = "employees"
    if type == 'single':
        url = 'delete.html'
    elif type == 'multiple':
        url = 'delete_mul.html'
    else:
        print(f"ページが存在しません。delete/<type>でtypeの部分をsingleかmultipleでもう一度確かめてみてください。")
        error_message = "ページが存在しません。delete/<type>でtypeの部分をsingleかmultipleでもう一度確かめてみてください。"
        return render_template('error.html', error_message=error_message)
    
    if request.method == "POST":
        if 'submit_button' in request.form:
            button_val = request.form['submit_button']
            desc, table = fetch_table_data(table_name)
            #削除をする場合
            if button_val == 'result_btn':
                try:
                    if type == 'single':
                        condition_1 = request.form['condition_1']
                        delete_sql = f'DELETE FROM {table_name} WHERE {condition_1}'
                        exec_sql(delete_sql)
                    elif type == 'multiple':
                        condition_1 = request.form['condition_1']
                        and_or = request.form['and_or']
                        condition_2 = request.form['condition_2']
                        delete_sql = f'DELETE FROM {table_name} WHERE {condition_1} {and_or} {condition_2}'
                        exec_sql(delete_sql)
                    else:
                        error_message = '条件が取得できませんでした。'
                        return render_template(url, table_name=table_name, desc=desc, table=table, error_message=error_message)
                    message = '正常に削除できました。'
                    desc, table = fetch_table_data(table_name)
                    return render_template(url, table_name=table_name, desc=desc, table=table, message=message)
                except Exception as e:
                    error_message = f'削除に失敗しました。:{e}'
                    print(e)
                    return render_template(url, table_name=table_name, desc=desc, table=table, error_message=error_message)
            #テーブルを初期化する場合
            elif button_val == 'table_init_btn':
                try:
                    user_db = this_users_dns['database']
                    drop_table = f"DROP TABLE IF EXISTS {table_name}"

                    # テーブルの削除
                    conn = mysql.connector.MySQLConnection(**this_users_dns)
                    cursor = conn.cursor()
                    try:
                        cursor.execute(drop_table)
                        conn.commit()
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                    finally:
                        cursor.close()
                        conn.close()

                    # テーブルのコピー
                    conn = mysql.connector.MySQLConnection(**this_users_dns)
                    cursor = conn.cursor()
                    copy_table_query = f"CREATE TABLE {user_db}.{table_name} LIKE dataset.{table_name}"
                    try:
                        cursor.execute(copy_table_query)
                        conn.commit()
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                    finally:
                        cursor.close()
                        conn.close()

                    # データの挿入
                    conn = mysql.connector.MySQLConnection(**this_users_dns)
                    cursor = conn.cursor()
                    insert_table_query = f"INSERT INTO {user_db}.{table_name} SELECT * FROM dataset.{table_name}"
                    try:
                        cursor.execute(insert_table_query)
                        conn.commit()
                        print("success")
                        message = 'テーブルを初期化しました。'
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                    finally:
                        cursor.close()
                        conn.close()

                    # テーブルのデータを取得してレンダリング
                    desc, table = fetch_table_data(table_name)
                    return render_template(url, table_name=table_name, desc=desc, table=table, message=message)
                except Exception as e:
                    error_message = f'初期化に失敗しました。:{e}'
                    print(e)
                    return render_template(url, table_name=table_name, desc=desc, table=table, error_message=error_message)
            else:
                error_message = 'テーブルを初期化、または、レコードの削除に失敗しました。'
                return render_template(url, table_name=table_name, desc=desc, table=table, error_message=error_message)
        else:
            error_message = '不明な操作が指定されました。'
            desc, table = fetch_table_data(table_name)
            return render_template(url, table_name=table_name, desc=desc, table=table, error_message=error_message)
    try:
        desc, table = fetch_table_data(table_name)
        return render_template(url, table_name=table_name, desc=desc, table=table)
    except Exception as e:
        print(f"Error fetching tables: {e}")
        error_message = "An error occurred while fetching tables."
        return render_template('error.html', error_message=error_message)


#CREATE文の演習ページ
@app.route('/create_table', methods=['GET', 'POST'])
def create_table():
    if request.method == "POST":
        try:
            table_name = request.form.get('table_name')
            columns = request.form.getlist('columns[]')
            datatypes = request.form.getlist('data_types[]')
            constraints = request.form.getlist('constraints[]')
            print(constraints)
            print(columns)
            print(datatypes)

            # テーブル作成
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()
            column = columns[0] + " " + datatypes[0]

            # カラムが複数ある場合の処理
            if len(columns) > 1:
                for i in range(1, len(columns)):
                    # データ型が存在する場合のみカンマを追加
                    if datatypes[i]:
                        column += f", {columns[i]} {datatypes[i]}"

            # 制約が存在する場合の処理
            if constraints and constraints[0]:  # 制約が存在し、かつ空文字列でない場合のみ追加
                for i in range(len(constraints)):
                    column += f", {constraints[i]}"

            create_table_query = f"CREATE TABLE {table_name} ({column})"
            print(create_table_query)
            cursor.execute(create_table_query)
            cursor.close()
            conn.commit()
            conn.close()
            return redirect(url_for('create_table', tables=get_tables()))
        except Exception as e:
            # エラーが発生した場合の処理
            print(f"Error fetching tables: {e}")
            error_message = "テーブル作成を失敗しました。"
            return render_template('error.html', error_message=error_message)
        
    try:
        tables = get_tables()
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"Error fetching tables: {e}")
        error_message = "テーブルが取得できませんでした。"
        return render_template('error.html', error_message=error_message)
            
    return render_template('create_table.html', tables=tables)

#insert tableの前段階でテーブルを選ばせる
@app.route('/insert_table_choose', methods=['GET', 'POST'])
def insert_table_choose():
    if request.method == 'POST':
        insert_table_name = request.form.get('table_name')
        session['insert_table_name'] = insert_table_name  # セッションに保存
        return redirect(url_for('insert_table'))
    
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    users_table_call = "SHOW TABLES"
    cursor.execute(users_table_call)
    
    tables_original = cursor.fetchall()
    tables = [item[0] for item in tables_original]
    print(tables)
    
    cursor.close()
    conn.commit()
    conn.close()
    
    return render_template('insert_table_choose.html', tables=tables)

#insert tableのページ
@app.route('/insert_table', methods=['GET', 'POST'])
def insert_table():
    try:
        insert_table_name = session.get('insert_table_name')
        if insert_table_name:
            if request.method == 'POST':
                columns = request.form.getlist('columns[]')
                values = request.form.getlist('values[]')
                print(columns, values)
                try:
                    # Insert data into the table
                    insert_data(insert_table_name, columns, values)
                    message = "テーブルを更新しました。"
                    table_desc, table = fetch_table_data(insert_table_name)
                    return render_template('insert_table.html', table_name=insert_table_name, desc=table_desc, table=table, message=message)
                except Exception as e:
                    error_message = str(e)
                    table_desc, table = fetch_table_data(insert_table_name)
                    return render_template('insert_table.html', table_name=insert_table_name, desc=table_desc, table=table, error_message=error_message)

            # Fetch table description and data
            table_desc, table = fetch_table_data(insert_table_name)

            return render_template('insert_table.html', table_name=insert_table_name, desc=table_desc, table=table)

        else:
            print("テーブルが選択されていません")
            return render_template('error.html', error_message="テーブルが選択されていません")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return render_template('error.html', error_message="テーブルの情報を取得できませんでした")


#delete tableの前段階でテーブルを選ばせる
@app.route('/delete_table_choose', methods=['GET', 'POST'])
def delete_table_choose():
    if request.method == 'POST':
        delete_table_name = request.form.get('table_name')
        session['delete_table_name'] = delete_table_name  # セッションに保存
        return redirect(url_for('delete_from_table'))
    
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    users_table_call = "SHOW TABLES"
    cursor.execute(users_table_call)
    
    tables_original = cursor.fetchall()
    tables = [item[0] for item in tables_original]
    print(tables)
    
    cursor.close()
    conn.commit()
    conn.close()
    
    return render_template('delete_table_choose.html', tables=tables)

#delete from tableのページ
@app.route('/delete_from_table', methods=['GET', 'POST'])
def delete_from_table():
    if request.method == 'POST':
        condition = request.form.get('condition')
        delete_table_name = session.get('delete_table_name', None)
        print(condition)
        try:
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()
            
            delete_sql = f"DELETE FROM {delete_table_name} WHERE {condition}"
            cursor.execute(delete_sql)
            
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            # エラーが発生した場合の処理
            print(f"Error fetching tables: {e}")
            error_message = "An error occurred while fetching tables."
            return render_template('error.html', error_message=error_message)
        
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()
        
        users_table_desc = "desc " + delete_table_name
        cursor.execute(users_table_desc)
        table_desc = cursor.fetchall()
        print(table_desc)
        
        selected_table = "select * from " + delete_table_name
        cursor.execute(selected_table)
        table = cursor.fetchall()
        print(table)
        
        cursor.close()
        conn.commit()
        conn.close()
        
        return render_template('delete_from_table.html', table_name=delete_table_name, desc=table_desc, table=table)
    
    try:
        delete_table_name = session.get('delete_table_name', None)
        if delete_table_name is not None:
            print(f"選択されたテーブル: {delete_table_name}")
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()
            
            users_table_desc = "desc " + delete_table_name
            cursor.execute(users_table_desc)
            table_desc = cursor.fetchall()
            print(table_desc)
            
            selected_table = "select * from " + delete_table_name
            cursor.execute(selected_table)
            table = cursor.fetchall()
            print(table)
            
            cursor.close()
            conn.commit()
            conn.close()
            
        else:
            # セッションに insert_table_name がない場合の処理
            print("テーブルが選択されていません")
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"Error fetching tables: {e}")
        error_message = "An error occurred while fetching tables."
        return render_template('error.html', error_message=error_message)
    return render_template('delete_from_table.html', table_name=delete_table_name, desc=table_desc, table=table)

#delete from table multipleのページ
@app.route('/delete_from_table_multiple', methods=['GET', 'POST'])
def delete_from_table_multiple():
    if request.method == 'POST':
        conditions = request.form.getlist('conditions[]')
        and_or = request.form.get('and_or')
        delete_table_name = session.get('delete_table_name', None)
        print(conditions)
        print(and_or)
        try:
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()
            
            delete_sql = f"DELETE FROM {delete_table_name} WHERE {conditions[0]} {and_or} {conditions[1]}"
            cursor.execute(delete_sql)
            
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            # エラーが発生した場合の処理
            print(f"Error fetching tables: {e}")
            error_message = "An error occurred while fetching tables."
            return render_template('error.html', error_message=error_message)
        
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()
        
        users_table_desc = "desc " + delete_table_name
        cursor.execute(users_table_desc)
        table_desc = cursor.fetchall()
        print(table_desc)
        
        selected_table = "select * from " + delete_table_name
        cursor.execute(selected_table)
        table = cursor.fetchall()
        print(table)
        
        cursor.close()
        conn.commit()
        conn.close()
        
        return render_template('delete_from_table_multiple.html', table_name=delete_table_name, desc=table_desc, table=table)
    
    try:
        delete_table_name = session.get('delete_table_name', None)
        if delete_table_name is not None:
            print(f"選択されたテーブル: {delete_table_name}")
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()
            
            users_table_desc = "desc " + delete_table_name
            cursor.execute(users_table_desc)
            table_desc = cursor.fetchall()
            print(table_desc)
            
            selected_table = "select * from " + delete_table_name
            cursor.execute(selected_table)
            table = cursor.fetchall()
            print(table)
            
            cursor.close()
            conn.commit()
            conn.close()
            
        else:
            # セッションに insert_table_name がない場合の処理
            print("テーブルが選択されていません")
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"Error fetching tables: {e}")
        error_message = "An error occurred while fetching tables."
        return render_template('error.html', error_message=error_message)
    return render_template('delete_from_table_multiple.html', table_name=delete_table_name, desc=table_desc, table=table)




@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))

#サインアップ
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ユーザー名の重複を確認
        check_user_query = f"SELECT * FROM users WHERE username = '{username}'"
        existing_user = user_db.query(check_user_query)


        if existing_user:
            flash('ユーザー名は既に存在します。別のユーザー名を選択してください。', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # ユーザー情報をユーザーテーブルに挿入
            conn = mysql.connector.MySQLConnection(**user_dns)
            cursor = conn.cursor()
            insert_user_query = f"INSERT INTO `users` (`username`, `password`) VALUES ('{username}', '{hashed_password}')"
            cursor.execute(insert_user_query)
            #ユーザー専用のdatabaseを作成
            create_user_db = f"CREATE DATABASE `{username}_db`"
            cursor.execute(create_user_db)
            cursor.close()
            conn.commit()
            conn.close()
            
            # ユーザーのデータベースにdataset内にある、テーブルをいくつかコピーする
            tables = ['users', 'employees']
            for table in tables:
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                
                # テーブル構造の複製
                copy_table_query = f"CREATE TABLE {username}_db.{table} LIKE dataset.{table}"
                cursor.execute(copy_table_query)
                
                # データの挿入
                insert_table_query = f"INSERT INTO {username}_db.{table} SELECT * FROM dataset.{table}"
                cursor.execute(insert_table_query)
                
                cursor.close()
                conn.commit()
                conn.close()
            
            #ユーザーの持つデータベースの情報をuser_databasesに紐づけて格納
            check_user_id = f"SELECT id from users where username = '{username}'"
            user_id = user_db.query(check_user_id)
            print(user_id)
            conn = mysql.connector.MySQLConnection(**user_dns)
            cursor = conn.cursor()
            insert_user_db = f"INSERT INTO `user_databases` (`user_id`, `database_name`) VALUES ('{user_id[0][0]}', '{username}_db')"
            cursor.execute(insert_user_db)
            cursor.close()
            conn.commit()
            conn.close()
            
            print('ユーザー登録が完了しました。')
            return redirect(url_for('login'))

    return render_template('signup.html')

#ログイン機能
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ユーザーテーブルからユーザー情報を取得
        select_user_query = "SELECT * FROM users WHERE username = '" + username + "'"
        users = user_db.query(select_user_query)
        print(users)
        try:
            if users and bcrypt.check_password_hash(users[0][2], password):
                session['user_id'] = users[0][0]
                
                # ユーザー専用のデータベース名を生成して追加
                user_db_name = f"{username}_db"
                this_users_dns['database'] = user_db_name

                
                return redirect(url_for('main'))
        except Exception as e:
            print(f"Login Error: {e}")

    return render_template('login.html')

#ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    this_users_dns['database'] = None
    return redirect(url_for('login'))


#おまじない
if __name__ == "__main__":
    app.run(debug=True)


#汎用関数
def get_tables():
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    get_tables_sql = "show tables"
    cursor.execute(get_tables_sql)
    tables = cursor.fetchall()
    return tables

def insert_data(table_name, columns, values):
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES "
    values_str = ', '.join(['(' + ', '.join(map(str, values[i:i+len(columns)])) + ')' for i in range(0, len(values), len(columns))])
    insert_sql += values_str

    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    cursor.execute(insert_sql)
    cursor.close()
    conn.commit()
    conn.close()

def fetch_table_data(table_name):
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()

    users_table_desc = f"DESC {table_name}"
    cursor.execute(users_table_desc)
    table_desc = cursor.fetchall()

    selected_table = f"SELECT * FROM {table_name}"
    cursor.execute(selected_table)
    table = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return table_desc, table

def exec_sql(sql):
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()