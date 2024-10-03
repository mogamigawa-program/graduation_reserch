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
            tables = ['users', 'employees', 'products', 'products_initialstate', 'discounts', 'customers', 'inventory']
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


#-------------------------------------------------------------------------#
#ここから！！！！！！！！！！！！！！！！！！
#-------------------------------------------------------------------------#

#update専用のバックアップテーブルと初期状態テーブル
def create_initial_state_and_backup(table_name):
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()

    # 初期状態テーブルの作成
    initial_state_table_name = f"{table_name}_initialstate"
    cursor.execute(f"DROP TABLE IF EXISTS {initial_state_table_name}")  # 初期状態テーブルを削除
    create_initial_sql = f"CREATE TABLE {initial_state_table_name} AS SELECT * FROM `{table_name}`"
    cursor.execute(create_initial_sql)

    # バックアップテーブルの作成・更新
    backup_table_name = f"{table_name}_backup"
    cursor.execute(f"DROP TABLE IF EXISTS {backup_table_name}")  # バックアップテーブルを削除
    create_backup_sql = f"CREATE TABLE {backup_table_name} AS SELECT * FROM `{table_name}`"
    cursor.execute(create_backup_sql)

    cursor.close()
    conn.commit()
    conn.close()

#update table chooseのページ
@app.route('/update_table_choose', methods=['GET', 'POST'])
def update_table_choose():
    if request.method == 'POST':
        update_table_name = request.form.get('table_name')
        session['update_table_name'] = update_table_name  # セッションに保存

        # 初期状態とバックアップの作成
        create_initial_state_and_backup(update_table_name)

        return redirect(url_for('update_table'))
    
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    users_table_call = "SHOW TABLES"
    cursor.execute(users_table_call)
    
    tables_original = cursor.fetchall()
    tables = [item[0] for item in tables_original]
    
    cursor.close()
    conn.commit()
    conn.close()
    
    return render_template('update_table_choose.html', tables=tables)

#update tableのページ
@app.route('/update_table', methods=['GET', 'POST'])
def update_table():
    try:
        update_table_name = session.get('update_table_name')
        if not update_table_name:
            raise ValueError("セッションからテーブル名が取得できませんでした。")

        if request.method == 'POST':
            set_clause = request.form.get('set_clause')
            condition = request.form.get('condition')

            try:
                # バックアップの更新
                create_backup(update_table_name)

                # データの更新
                update_data(update_table_name, set_clause, condition)

                message = "データが更新されました。"
                table_desc, table = fetch_table_data(update_table_name)
                return render_template('update_table.html', table_name=update_table_name, desc=table_desc, table=table, message=message)
            except Exception as e:
                error_message = str(e)
                table_desc, table = fetch_table_data(update_table_name)
                return render_template('update_table.html', table_name=update_table_name, desc=table_desc, table=table, error_message=error_message)

        # テーブルの定義とデータを取得
        table_desc, table = fetch_table_data(update_table_name)

        return render_template('update_table.html', table_name=update_table_name, desc=table_desc, table=table)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return render_template('error.html', error_message="テーブルの情報を取得できませんでした")

def update_data(table_name, set_clause, condition):
    update_sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {condition}"

    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    cursor.execute(update_sql)
    cursor.close()
    conn.commit()
    conn.close()

def create_backup(table_name):
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()

    # バックアップテーブルの作成・更新
    backup_table_name = f"{table_name}_backup"
    cursor.execute(f"DROP TABLE IF EXISTS {backup_table_name}")  # バックアップテーブルを削除
    create_backup_sql = f"CREATE TABLE {backup_table_name} AS SELECT * FROM `{table_name}`"
    cursor.execute(create_backup_sql)

    cursor.close()
    conn.commit()
    conn.close()

def fetch_table_data(table_name):
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # テーブルの定義を取得
        users_table_desc = f"DESC `{table_name}`"
        cursor.execute(users_table_desc)
        table_desc = cursor.fetchall()

        # テーブルのデータを取得
        selected_table = f"SELECT * FROM `{table_name}`"
        cursor.execute(selected_table)
        table = cursor.fetchall()

        cursor.close()
        conn.commit()
        conn.close()

        return table_desc, table
    except Exception as e:
        print(f"{table_name}のデータ取得に失敗しました: {e}")
        raise


# 「初期状態に戻す」または「1つ前の状態に戻す」ボタンの処理
@app.route('/rollback_table', methods=['POST'])
def rollback_table():
    try:
        rollback_type = request.form.get('rollback_type')  # ボタンの種類（initialstate または backup）
        update_table_name = session.get('update_table_name')
        if not update_table_name:
            raise ValueError("セッションからテーブル名が取得できませんでした。")

        if rollback_type == 'initial':
            source_table = f"{update_table_name}_initialstate"
        elif rollback_type == 'backup':
            source_table = f"{update_table_name}_backup"
        else:
            raise ValueError("不正なロールバックタイプが指定されました。")

        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # 元のテーブルを空にする
        cursor.execute(f"DELETE FROM `{update_table_name}`")

        # バックアップからデータを復元する
        cursor.execute(f"INSERT INTO `{update_table_name}` SELECT * FROM `{source_table}`")

        cursor.close()
        conn.commit()
        conn.close()

        flash(f"{rollback_type} 状態に復元しました。")
        return redirect(url_for('update_table'))

    except Exception as e:
        print(f"ロールバック中にエラーが発生しました: {e}")
        return render_template('error.html', error_message="テーブルの復元に失敗しました。")





# GROUP BY テーブル選択ページ (groupby_table_choose)
@app.route('/groupby_table_choose', methods=['GET', 'POST'])
def groupby_table_choose():
    if request.method == 'POST':
        groupby_table_name = request.form.get('table_name')
        session['groupby_table_name'] = groupby_table_name  # セッションに保存
        return redirect(url_for('groupby_table'))
    
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
    
    return render_template('groupby_table_choose.html', tables=tables)

# GROUP BY 実行ページ (groupby_table)
@app.route('/groupby_table', methods=['GET', 'POST'])
def groupby_table():
    try:
        groupby_table_name = session.get('groupby_table_name')
        if groupby_table_name:
            if request.method == 'POST':
                select_clause = request.form.get('select_clause')
                groupby_clause = request.form.get('groupby_clause')
                print(select_clause, groupby_clause)
                try:
                    # Execute GROUP BY query
                    result, table_desc, table = execute_groupby_query(groupby_table_name, select_clause, groupby_clause)
                    return render_template('groupby_table.html', table_name=groupby_table_name, desc=table_desc, table=table, result=result)
                except Exception as e:
                    error_message = str(e)
                    table_desc, table = fetch_table_data(groupby_table_name)
                    return render_template('groupby_table.html', table_name=groupby_table_name, desc=table_desc, table=table, error_message=error_message)

            # Fetch table description and data
            table_desc, table = fetch_table_data(groupby_table_name)

            return render_template('groupby_table.html', table_name=groupby_table_name, desc=table_desc, table=table)

        else:
            print("テーブルが選択されていません")
            return render_template('error.html', error_message="テーブルが選択されていません")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return render_template('error.html', error_message="テーブルの情報を取得できませんでした")

def execute_groupby_query(table_name, select_clause, groupby_clause):
    groupby_sql = f"SELECT {select_clause} FROM {table_name} GROUP BY {groupby_clause}"

    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    cursor.execute(groupby_sql)
    result = cursor.fetchall()

    users_table_desc = f"DESC {table_name}"
    cursor.execute(users_table_desc)
    table_desc = cursor.fetchall()

    selected_table = f"SELECT * FROM {table_name}"
    cursor.execute(selected_table)
    table = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return result, table_desc, table

# update_joinページ (update_join.html) JOIN句あり 
@app.route('/update_join', methods=['GET', 'POST'])
def update_join():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # テーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("SELECT * FROM discounts")
        discounts_data = cursor.fetchall()

        cursor.execute("SELECT * FROM inventory")
        inventory_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.execute("DESC discounts")
        discounts_desc = cursor.fetchall()

        cursor.execute("DESC inventory")
        inventory_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('multiple_table_join_study.html', error_message=error_message)

    if 'submit_button' in request.form:
        button_val = request.form['submit_button']
        updatetable_name = request.form.get('table_name', "products")
        
        # 実行する ボタンを押した場合
        if button_val == 'result_btn':    
            # フォームからのデータを取得
            in_out = request.form.get('inner_outer') 
            join_table = request.form.get('from_table')  
            join_condition = request.form['join_condition']  
            set_clause = request.form['set_clause']
            where_clause = request.form.get('where_clause', '')  

            # SQL文の組み立て
            update_query = (
                f"UPDATE {updatetable_name} "
            )

            if join_condition:
                update_query += (
                    f"{in_out} JOIN {join_table} ON {join_condition} " 
                )
            
            update_query += (
                f"SET {set_clause} "
            )

            if where_clause:
                update_query += (
                f"WHERE {where_clause};"
            )
            else:
                update_query += ";"

            try:
                # UPDATE前にproducts_backupを作成
                create_backup_table('products')

                # UPDATE文の実行
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()

                # テーブルの状態を取得
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                message = "テーブルを更新しました。"
                
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, message=message,
                                        products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)
            
            except Exception as e:
                # エラーが発生した場合の処理
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, error_message=str(e), 
                                        products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

        # テーブルを初期状態に戻すボタンを押した場合
        elif button_val == 'table_init_btn':
            try:
                # productsテーブルの中身を削除
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                # products_backupからproductsテーブルにデータをコピー
                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_initialstate
                """
                cursor.execute(insert_from_backup_query)

                conn.commit()
                cursor.close()
                conn.close()

                # 初期化後のテーブル内容を取得して表示
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                message = "テーブルを初期化しました。"
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, message=message,
                                        products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

            except Exception as e:
                message = "テーブルを初期化できませんでした。"
                print(f"Error: {e}")
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, message=message,
                                        products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

        # 1つ前の状態に戻す ボタンを押した場合
        elif button_val == 'restore_backup_btn':
            try:
                # productsテーブルの中身を削除
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                # products_initialstateからproductsテーブルにデータをコピー
                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_backup
                """
                cursor.execute(insert_from_backup_query)

                conn.commit()
                cursor.close()
                conn.close()

                # 復元後のテーブル内容を取得して表示
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                message = "1つ前の状態に戻しました。"
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, message=message, products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

            except Exception as e:
                message = "状態を復元できませんでした。"
                print(f"Error: {e}")
                table_desc, table = fetch_table_data(updatetable_name)
                products_desc, products_data = fetch_table_data(updatetable_name)
                return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, message=message, products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

    # GETリクエスト時、テーブルの情報を表示
    try:
        updatetable_name = "products"
        table_desc, table = fetch_table_data(updatetable_name)
        products_desc, products_data = fetch_table_data(updatetable_name)
        return render_template('update_join.html', table_name=updatetable_name, desc=table_desc, table=table, products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)

    except Exception as e:
        print(f"Error fetching tables: {e}")
        error_message = "An error occurred while fetching tables."
        return render_template('error.html', error_message=error_message, products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data)



#JOIN 学習ページ
@app.route('/join_select', methods=['GET', 'POST'])
def join_select():
    return render_template('join_select.html')

# 以下は各JOINページ
#CROSS JOIN 学習ページ
@app.route('/cross_join_study', methods=['GET', 'POST'])
def cross_join_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsとcustomersテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('cross_join_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            columns = request.form['columns']
            table1_name = request.form['table1_name']
            table2_name = request.form['table2_name']
            where_condition = None
            if 'use_where' in request.form and request.form['where_condition']:
                where_condition = f"WHERE {request.form['where_condition']}"

            # CROSS JOINを実行するクエリ
            cross_join_query = f"SELECT {columns} FROM {table1_name} CROSS JOIN {table2_name} "
            if where_condition:
                cross_join_query += where_condition

            cross_join_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # CROSS JOINの結果を取得
            cursor.execute(cross_join_query)
            cross_join_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('cross_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                                   products_data=products_data, customers_data=customers_data,
                                   cross_join_result=cross_join_result, table1_name=table1_name, table2_name=table2_name, columns=columns, cross_join_query=cross_join_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('cross_join_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('cross_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                           products_data=products_data, customers_data=customers_data)

# CROSS JOINの実行例ページ
@app.route('/cross_join_study_example', methods=['GET'])
def cross_join_study_example():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsとcustomersテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        # CROSS JOINのクエリを実行
        cross_join_query = """
        SELECT products.product_id, products.product_name, customers.customer_id, customers.order_date
        FROM products
        CROSS JOIN customers;
        """
        cursor.execute(cross_join_query)
        cross_join_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('cross_join_study_example.html', error_message=error_message)
    
    # カラム情報の設定
    columns = "products.product_id, products.product_name, customers.customer_id, customers.order_date"

    return render_template('cross_join_study_example.html',  products_desc=products_desc, customers_desc=customers_desc, products_data=products_data, customers_data=customers_data,
                           cross_join_result=cross_join_result, columns=columns)

#INNER JOIN 学習ページ
@app.route('/inner_join_study', methods=['GET', 'POST'])
def inner_join_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsとcustomersテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('inner_join_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            columns = request.form['columns']
            table1_name = request.form['table1_name']
            table2_name = request.form['table2_name']
            on_clause = request.form['on_clause']
            where_condition = ""
            if 'use_where' in request.form and request.form['where_condition']:
                where_condition = f" WHERE {request.form['where_condition']}"

            # INNER JOINを実行するクエリ
            inner_join_query = f"SELECT {columns} FROM {table1_name} INNER JOIN {table2_name} ON {on_clause}"
            if where_condition:
                inner_join_query += where_condition

            inner_join_query += ";"
            
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # INNER JOINの結果を取得
            cursor.execute(inner_join_query)
            inner_join_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('inner_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                                   products_data=products_data, customers_data=customers_data,
                                   inner_join_result=inner_join_result, table1_name=table1_name, table2_name=table2_name, columns=columns, inner_join_query=inner_join_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('inner_join_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('inner_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                           products_data=products_data, customers_data=customers_data)


#LEFT OUTER JOIN 学習ページ
@app.route('/left_outer_join_study', methods=['GET', 'POST'])
def left_outer_join_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsとcustomersテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('left_outer_join_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            columns = request.form['columns'] 
            table1_name = request.form['table1_name']
            table2_name = request.form['table2_name']
            on_clause = request.form['on_clause']
            where_condition = ""
            if 'use_where' in request.form and request.form['where_condition']:
                where_condition = f" WHERE {request.form['where_condition']}"

            # LEFT OUTER JOINを実行するクエリ
            left_outer_join_query = f"SELECT {columns} FROM {table1_name} LEFT OUTER JOIN {table2_name} ON {on_clause}"
            if where_condition:
                left_outer_join_query += where_condition

            left_outer_join_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # LEFT OUTER JOINの結果を取得
            cursor.execute(left_outer_join_query)
            left_outer_join_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('left_outer_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                                   products_data=products_data, customers_data=customers_data,
                                   left_outer_join_result=left_outer_join_result, table1_name=table1_name, table2_name=table2_name, columns=columns, left_outer_join_query=left_outer_join_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('left_outer_join_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('left_outer_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                           products_data=products_data, customers_data=customers_data)

#RIGHT OUTER JOIN 学習ページ
@app.route('/right_outer_join_study', methods=['GET', 'POST'])
def right_outer_join_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsとcustomersテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('right_outer_join_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            columns = request.form['columns']
            table1_name = request.form['table1_name']
            table2_name = request.form['table2_name']
            on_clause = request.form['on_clause']
            where_condition = ""
            if 'use_where' in request.form and request.form['where_condition']:
                where_condition = f" WHERE {request.form['where_condition']}"

            # RIGHT OUTER JOINを実行するクエリ
            right_outer_join_query = f"SELECT {columns} FROM {table1_name} RIGHT OUTER JOIN {table2_name} ON {on_clause}"
            if where_condition:
                right_outer_join_query += where_condition

            right_outer_join_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # RIGHT OUTER JOINの結果を取得
            cursor.execute(right_outer_join_query)
            right_outer_join_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('right_outer_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                                   products_data=products_data, customers_data=customers_data,
                                   right_outer_join_result=right_outer_join_result, table1_name=table1_name, table2_name=table2_name, columns=columns, right_outer_join_query=right_outer_join_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('right_outer_join_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('right_outer_join_study.html', products_desc=products_desc, customers_desc=customers_desc,
                           products_data=products_data, customers_data=customers_data)


#複数のテーブルJOIN 学習ページ
@app.route('/multiple_table_join_study', methods=['GET', 'POST'])
def multiple_table_join_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # テーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("SELECT * FROM discounts")
        discounts_data = cursor.fetchall()

        cursor.execute("SELECT * FROM inventory")
        inventory_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.execute("DESC discounts")
        discounts_desc = cursor.fetchall()

        cursor.execute("DESC inventory")
        inventory_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('multiple_table_join_study.html', error_message=error_message)

    if request.method == 'POST':
        try:
            select_columns = request.form['select_columns']
            from_table = request.form['from_table']

            # JOINの組み立て
            joins = []
            join_types = request.form.getlist('join_type')
            join_tables = request.form.getlist('join_table')
            on_clauses = request.form.getlist('on_clause')

            for i in range(len(join_types)):
                join_type = join_types[i]
                join_table = join_tables[i]
                if join_type == 'CROSS JOIN':
                    joins.append(f"{join_type} {join_table}")
                else:
                    on_clause = on_clauses[i]
                    joins.append(f"{join_type} {join_table} ON {on_clause}")

            # WHERE句の処理
            where_condition = ""
            if 'use_where' in request.form and request.form['where_condition']:
                where_condition = f" WHERE {request.form['where_condition']}"

            # 最終的なクエリを構築
            join_query = f"SELECT {select_columns} FROM {from_table} " + " ".join(joins) + where_condition + ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # JOINの結果を取得
            cursor.execute(join_query)
            join_result = cursor.fetchall()


            # カラム名を取得
            columns = [desc[0] for desc in cursor.description]

            cursor.close()
            conn.close()

            return render_template('multiple_table_join_study.html', products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                                   products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data,
                                   join_result=join_result, columns=columns, join_query=join_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('multiple_table_join_study.html', error_message=error_message)

    # GET時のページ表示
    return render_template('multiple_table_join_study.html', products_desc=products_desc, customers_desc=customers_desc, discounts_desc=discounts_desc, inventory_desc=inventory_desc,
                           products_data=products_data, customers_data=customers_data, discounts_data=discounts_data, inventory_data=inventory_data,)


#以下はUPDATE!
#UPDATE 学習ページ
@app.route('/update_select', methods=['GET', 'POST'])
def update_select():
    return render_template('update_select.html')

#1つのカラムに1つの条件でUPDATEを行う(update_single_study)
@app.route('/update_single_study', methods=['GET', 'POST'])
def update_single_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルのデータとカラム情報を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('update_single_study.html', error_message=error_message)

    if request.method == 'POST':
        button_val = request.form.get('button_val')

        # レコード更新の処理
        if button_val == 'update_record_btn':
            try:
                column_to_update = request.form.get('column_to_update')
                new_value = request.form.get('new_value')
                condition_column = request.form.get('condition_column')
                condition_value = request.form.get('condition_value')

                # UPDATE文の作成（パラメータ化されたクエリを使用してSQLインジェクションを防止）
                update_query = f"UPDATE products SET {column_to_update} = %s WHERE {condition_column} = %s"

                # UPDATE前にproducts_backupを作成
                create_backup_table('products')

                # UPDATE文の実行
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(update_query, (new_value, condition_value))
                conn.commit()

                # 更新後のデータを再取得
                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "レコードを更新しました。"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

        # テーブルをす初期状態に戻す処理
        elif button_val == 'table_init_btn':
            try:
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_initialstate
                """
                cursor.execute(insert_from_backup_query)
                conn.commit()

                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "テーブルを初期化しました。"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"テーブルを初期化できませんでした: {str(e)}"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

        # 1つ前の状態に戻す処理
        elif button_val == 'restore_backup_btn':
            try:
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_backup
                """
                cursor.execute(insert_from_backup_query)
                conn.commit()

                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "1つ前の状態に戻しました。"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"状態を復元できませんでした: {str(e)}"
                return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

    # GETリクエスト時の処理
    return render_template('update_single_study.html', products_desc=products_desc, products_data=products_data)


#1つ以上のカラムに1つ以上の条件でUPDATEを行う(update_multiple_study)
@app.route('/update_multiple_study', methods=['GET', 'POST'])
def update_multiple_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルのデータとカラム情報を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('update_multiple_study.html', error_message=error_message)

    if request.method == 'POST':
        button_val = request.form.get('button_val')

        # レコード更新の処理
        if button_val == 'update_record_btn':
            try:
                # 更新するカラムと値を収集
                columns_to_update = []
                values_to_update = []
                for key in request.form:
                    if key.startswith('column_to_update_'):
                        index = key.split('_')[-1]
                        column = request.form[key]
                        value = request.form.get(f'new_value_{index}')
                        columns_to_update.append(f"{column} = %s")
                        values_to_update.append(value)

                # 条件を収集
                conditions = []
                condition_values = []
                for key in request.form:
                    if key.startswith('condition_column_'):
                        index = key.split('_')[-1]
                        condition_column = request.form[key]
                        condition_value = request.form.get(f'condition_value_{index}')
                        conditions.append(f"{condition_column} = %s")
                        condition_values.append(condition_value)

                # UPDATEクエリの構築
                update_query = f"UPDATE products SET {', '.join(columns_to_update)} WHERE {' AND '.join(conditions)}"

                # UPDATE前にproducts_backupを作成
                create_backup_table('products')

                # UPDATE文の実行
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(update_query, values_to_update + condition_values)
                conn.commit()

                # 更新後のデータを再取得
                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "レコードを更新しました。"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)
            
        # テーブルを初期状態に戻す処理
        elif button_val == 'table_init_btn':
            try:
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_initialstate
                """
                cursor.execute(insert_from_backup_query)
                conn.commit()

                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "テーブルを初期化しました。"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"テーブルを初期化できませんでした: {str(e)}"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

        # 1つ前の状態に戻す処理
        elif button_val == 'restore_backup_btn':
            try:
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_backup
                """
                cursor.execute(insert_from_backup_query)
                conn.commit()

                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "1つ前の状態に戻しました。"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"状態を復元できませんでした: {str(e)}"
                return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

    # GETリクエスト時の処理
    return render_template('update_multiple_study.html', products_desc=products_desc, products_data=products_data)


# 全レコードUPDATE (update_all_column_study)
@app.route('/update_all_column_study', methods=['GET', 'POST'])
def update_all_column_study():
    try:
        # productsテーブルのデータとカラム情報を取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('update_all_column_study.html', error_message=error_message)

    if request.method == 'POST':
        button_val = request.form.get('button_val')

        # 全レコード更新の処理
        if button_val == 'update_all_records_btn':
            try:
                # ユーザーが入力したSET句を取得
                columns_to_update = []
                values_to_update = []
                for key in request.form:
                    if key.startswith('column_to_update_'):
                        index = key.split('_')[-1]
                        column = request.form[key]
                        new_value = request.form.get(f'new_value_{index}')
                        columns_to_update.append(f"{column} = %s")
                        values_to_update.append(new_value)

                # クエリ作成
                update_query = f"UPDATE products SET {', '.join(columns_to_update)}"

                # 全レコード更新前にproducts_backupを作成
                create_backup_table('products')

                # UPDATE文の実行
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(update_query, tuple(values_to_update))
                conn.commit()

                # 更新後のデータを再取得
                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "全てのレコードが更新されました。WHERE句がないため、全レコードが更新されています。"
                return render_template('update_all_column_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                return render_template('update_all_column_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)
            
        # テーブルを初期状態に戻す処理
        elif button_val == 'table_init_btn':
            try:
                # テーブルを初期状態に戻す
                truncate_table_query = "TRUNCATE TABLE products"
                conn = mysql.connector.MySQLConnection(**this_users_dns)
                cursor = conn.cursor()
                cursor.execute(truncate_table_query)

                # 初期状態に戻す
                insert_from_backup_query = """
                INSERT INTO products (product_id, product_name, price, stock_quantity, status)
                SELECT product_id, product_name, price, stock_quantity, status
                FROM products_initialstate
                """
                cursor.execute(insert_from_backup_query)
                conn.commit()

                # 更新後のデータを再取得
                cursor.execute("SELECT * FROM products")
                products_data = cursor.fetchall()

                cursor.close()
                conn.close()

                message = "テーブルを初期化しました。"
                return render_template('update_all_column_study.html', products_desc=products_desc, products_data=products_data, message=message)

            except Exception as e:
                error_message = f"テーブルを初期化できませんでした: {str(e)}"
                return render_template('update_all_column_study.html', products_desc=products_desc, products_data=products_data, error_message=error_message)

    # GETリクエスト時の処理
    return render_template('update_all_column_study.html', products_desc=products_desc, products_data=products_data)




#-------------------------------------------------------------------------#
#ここまで！！！！！！！！！！！！！
#-------------------------------------------------------------------------#


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

#あらきが追加した関数
# {table_name}_backupテーブルを作成
def create_backup_table(table_name):
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # 古い {table_name}_backup を削除
        drop_backup_query = f"DROP TABLE IF EXISTS {table_name}_backup"  # f-string を使用
        cursor.execute(drop_backup_query)

        # {table_name} テーブルをバックアップ
        create_backup_query = f"""
        CREATE TABLE {table_name}_backup AS 
        SELECT * FROM {table_name}
        """  # f-string を使用
        cursor.execute(create_backup_query)

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"General Error: {e}")