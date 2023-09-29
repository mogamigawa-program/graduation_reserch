#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,request

from DataStore.MySQL import MySQL
dns = {
    'user': 'root',
    'host': 'localhost',
    'password': '',
    'database': 'dataset'
}
db = MySQL(**dns)


#Flaskオブジェクトの生成
app = Flask(__name__)



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



@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))
                                

#おまじない
if __name__ == "__main__":
    app.run(debug=True)
                                    

