#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,request,session,flash

from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_bcrypt import Bcrypt

import mysql.connector

from .config import Config
from DataStore.MySQL import MySQL

import re

#Flaskオブジェクトの生成
app = Flask(__name__)

app.config.from_object(Config)

dns = {
    'user': app.config['MYSQL_DATABASE_USER'],
    'host': app.config['MYSQL_DATABASE_HOST'],
    'password': app.config['MYSQL_DATABASE_PASSWORD'],
    'database': 'dataset',
    'auth_plugin': 'mysql_native_password'
}
user_dns = {
    'user': app.config['MYSQL_DATABASE_USER'],
    'host': app.config['MYSQL_DATABASE_HOST'],
    'password': app.config['MYSQL_DATABASE_PASSWORD'],
    'database': 'user_info',
    'auth_plugin': 'mysql_native_password'
}
this_users_dns = {
    'user': app.config['MYSQL_DATABASE_USER'],
    'host': app.config['MYSQL_DATABASE_HOST'],
    'password': app.config['MYSQL_DATABASE_PASSWORD'],
    'auth_plugin': 'mysql_native_password',
    'database': None 
}

db = MySQL(**dns)
user_db = MySQL(**user_dns)
this_users_db = MySQL(**this_users_dns)


app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt(app)

# ログイン不要ページのリスト（ホワイトリスト）
public_pages = ['/login', '/signup']

@app.before_request
def check_login():
    if request.path.startswith('/static') or request.path in public_pages:
        return

    # ログインしていない場合、ログインページへリダイレクト
    if 'user_id' not in session:
        return redirect(url_for('login'))


#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/index")
def main():
    index_item = [
        "データベースの基礎",
        "データベースの要素",
        "基本操作",
        "高度な検索",
        "集約と分析",
        "集合演算",
        "テーブル制約と管理",
        "トランザクション"
    ]
    
    return render_template('index_main.html', title="SQL学習の森", index_item=index_item)


@app.route("/index/<item>")
def index_item(item):
    flag = request.args.get('flag')
    try:
        if flag == "normal":
            normal_index_item = {
                "データベースの基礎": ["データベースとは", "関係データベースとは"],
                "データベースの要素": ["キー", "テーブルの定義", "テーブルの作成"],
                "基本操作": ["select", "join", "insert", "update", "upsert", "delete"],
                "高度な検索": ["自己結合", "更新操作"],
                "集約と分析": ["集約関数", "ソートとグループ化"],
                "集合演算": ["union", "except", "intersect"],
                "テーブル制約と管理": ["テーブルに対する制約", "alter"],
                "トランザクション": ["トランザクションにおける基本操作", "acid特性"]    
            }
            index_item = normal_index_item[item]
            return render_template('index_main.html',
                                    title=item,
                                    normal_index_item=index_item,
                                    current_level="top",
                                    breadcrumbs = [
                                    {"label": "トップ", "url": "/index"},
                                    {"label": item, "url": None}  # 現在の項目なのでURLはなし
                                ])  # 大項目に戻るため

        if flag == "min":
            min_index_item = {
                "データベースとは": [
                    {"name": "データベースとは", "url": "/databasebasic/whatdatabase"}
                ],
                "関係データベースとは": [
                    {"name": "関係データベースとは", "url": "/databasebasic/whatrelationaldatabase"}
                ],
                "キー": [
                    {"name": "キー", "url": "/partofdatabase/key"}
                ],
                "テーブルの定義": [
                    {"name": "テーブルの定義", "url": "/partofdatabase/definition"}
                ],
                "テーブルの作成": [
                    {"name": "テーブルの作成", "url": "/partofdatabase/create"}
                ],
                "select": [
                    {"name": "単一条件", "url": "/basic/select/single/study"},
                    {"name": "複数条件", "url": "/basic/select/multiple/study"}
                ],
                "join": [
                    {"name": "cross", "url": "/basic/join/cross_join/study"},
                    {"name": "inner", "url": "/basic/join/inner_join/study"},
                    {"name": "left", "url": "/basic/join/left_outer_join/study"},
                    {"name": "right", "url": "/basic/join/right_outer_join/study"},
                    {"name": "複数のテーブルの結合", "url": "/basic/join/multiple_table_join/study"},
                    {"name": "まとめクイズ", "url": "/basic/join/join_quiz"}
                ],
                "insert": [
                    {"name": "挿入", "url": "/basic/insert/insert/study"},
                    {"name": "select文を利用したデータの挿入", "url": "/basic/insert/insert-select/study"}
                ],
                "update": [
                    {"name": "一つのカラム一つの条件", "url": "/basic/update/single-column/study"},
                    {"name": "複数のカラムに対して複数の条件", "url": "/basic/update/multiple-columns/study"},
                    {"name": "全レコード更新、計算", "url": "/basic/update/all-records/study"},
                    {"name": "join", "url": "/basic/update/join/study"}
                ],
                "upsert": [
                    {"name": "replace構文", "url": "/basic/upsert/replace/study"},
                    {"name": "insert on duplicate key update", "url": "/basic/upsert/duplicate-key/study"}
                ],
                "delete": [
                    {"name": "単一条件", "url": "/basic/delete/single/study"},
                    {"name": "複数条件", "url": "/basic/delete/multiple/study"},
                    {"name": "全レコード削除", "url": "/basic/delete/all-records/study"},
                    {"name": "共通なタプルの削除", "url": "/basic/delete/shared-tuple/study"}
                ],
                "自己結合": [
                    {"name": "self join", "url": "/advanced/self-join/study"}
                ],
                "更新操作": [
                    {"name": "副問い合わせを用いた更新", "url": "/advanced/update/subquery/study"},
                    {"name": "副問い合わせを用いた挿入", "url": "/advanced/insert/subquery/study"},
                    {"name": "副問い合わせを用いた削除", "url": "/advanced/delete/subquery/study"}
                ],
                "集約関数": [
                    {"name": "集約関数の注意書き", "url": "/aggregation/warning_message"},
                    {"name": "count", "url": "/aggregation/count/study"},
                    {"name": "sum", "url": "/aggregation/sum/study"},
                    {"name": "avg", "url": "/aggregation/avg/study"},
                    {"name": "min", "url": "/aggregation/min/study"},
                    {"name": "max", "url": "/aggregation/max/study"}
                ],
                "ソートとグループ化": [
                    {"name": "order by", "url": "/aggregation/order-by/study"},
                    {"name": "group by", "url": "/aggregation/group-by/study"},
                    {"name": "having", "url": "/aggregation/having/study"}
                ],
                "テーブルに対する制約": [
                    {"name": "主キー", "url": "/constraints/primary-key/study"},
                    {"name": "一意性制約", "url": "/constraints/unique/study"},
                    {"name": "NOT NULL制約", "url": "/constraints/not-null/study"},
                    {"name": "外部キー制約", "url": "/constraints/foreign-key/study"},
                    {"name": "DEFAULT値", "url": "/constraints/default/study"}
                ],
                "alter": [
                    {"name": "カラムの追加", "url": "/table-management/alter/add-column/study"},
                    {"name": "カラムの削除", "url": "/table-management/alter/drop-column/study"},
                    {"name": "カラムの変更", "url": "/table-management/alter/modify-column/study"},
                    {"name": "制約の追加", "url": "/table-management/alter/add-constraint/study"},
                    {"name": "制約の削除", "url": "/table-management/alter/drop-constraint/study"},
                    {"name": "制約の変更", "url": "/table-management/alter/modify-constraint/study"}
                ],
                "トランザクションにおける基本操作": [
                    {"name": "start→commit or rollback", "url": "/transaction/basic-operations/study"}
                ],
                "acid特性": [
                    {"name": "原始性", "url": "/transaction/acid/atomicity/study"}
                ]
            }

            # ✅ 小項目 → 親カテゴリの逆引き用辞書を作成
            reverse_index = {}
            for parent, children in {
                "データベースの基礎": ["データベースとは", "関係データベースとは"],
                "データベースの要素": ["キー", "テーブルの定義", "テーブルの作成"],
                "基本操作": ["select", "join", "insert", "update", "upsert", "delete"],
                "高度な検索": ["自己結合", "更新操作"],
                "集約と分析": ["集約関数", "ソートとグループ化"],
                "集合演算": ["union", "except", "intersect"],
                "テーブル制約と管理": ["テーブルに対する制約", "alter"],
                "トランザクション": ["トランザクションにおける基本操作", "acid特性"]
            }.items():
                for child in children:
                    reverse_index[child] = parent

            index_item = min_index_item[item]
            parent_category = reverse_index.get(item, None)

            return render_template(
                'index_main.html',
                title=item,
                min_index_item=index_item,
                parent_category=parent_category,
                current_level="middle",
                breadcrumbs=[
                    {"label": "トップ", "url": "/index"},
                    {"label": parent_category, "url": f"/index/{parent_category}?flag=normal"},
                    {"label": item, "url": None}
                ]
            )


    except Exception as e:
        return render_template('error.html', title="エラー", error_message=e)

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

#insert 学習
@app.route('/basic/insert/insert/study', methods=['GET', 'POST'])
def insert_study():
    return render_template('insert_study.html')

#insert文 演習
@app.route('/basic/insert/insert/practice', methods=['GET', 'POST'])
def insert_practice():
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

#insert 実行例
@app.route('/basic/insert/insert/example', methods=['GET', 'POST'])
def insert_example():
    return render_template('insert_example.html')

# insert_select 学習
@app.route('/basic/insert/insert-select/study', methods=['GET', 'POST'])
def insert_select_study():
    return render_template('insert_select_study.html')

# insert_select 実行例
@app.route('/basic/insert/insert-select/example', methods=['GET', 'POST'])
def insert_select_example():
    return render_template('insert_select_example.html')

# insert_select 演習
@app.route('/basic/insert/insert-select/practice/<type>', methods=['GET', 'POST'])
def insert_select_practice(type):
    if type == 'select':
        html = 'insert_select_practice_select.html'
    elif type == 'free':
        html = 'insert_select_practice_free.html'
    else:
        error = 'URLが正しくありません。practice/<type>, typeの部分はselect or freeでもう一度お試しください。'
        return redirect(url_for('error_page', msg=str(error)))

    sql = ''
    message = ''
    error_message = ''

    ALLOWED_COLUMNS = {'id', 'name', 'age'}

    import re
    SAFE_SQL_PATTERN = re.compile(r"""
        ^\s*INSERT\s+INTO\s+selected_users\s*
        \(\s*selected_id\s*,\s*selected_name\s*\)\s*
        SELECT\s+[\w\s,]+\s+FROM\s+all_users\s+
        WHERE\s+.+;\s*$""", re.IGNORECASE | re.VERBOSE)

    if request.method == 'POST':
        action = request.form.get('submit_button')

        if action == 'execute':
            if type == 'select':
                columns = request.form.get('columns', '').strip()
                condition = request.form.get('condition', '').strip()
                col_list = [col.strip() for col in columns.split(",")]
                if len(col_list) != 2 or not all(c in ALLOWED_COLUMNS for c in col_list):
                    error_message = "使用できるカラムは id, name, age のみです。"
                else:
                    col1, col2 = col_list
                    sql = f"""
                        INSERT INTO selected_users (selected_id, selected_name)
                        SELECT {col1}, {col2} FROM all_users WHERE {condition}
                    """
                    try:
                        run_query(sql, commit=True)
                        message = "データの挿入に成功しました。"
                    except Exception as e:
                        error_message = f"SQL実行エラー: {e}"

            elif type == 'free':
                sql = request.form.get('sql', '').strip()

                if not SAFE_SQL_PATTERN.match(sql):
                    error_message = "許可された形式のSQL文のみ実行できます。"
                else:
                    try:
                        run_query(sql, commit=True)
                        message = "SQLを実行しました。"
                    except Exception as e:
                        error_message = f"SQL実行エラー: {e}"

        elif action == 'reset':
            try:
                run_query("TRUNCATE TABLE selected_users", commit=True)
                message = "selected_usersテーブルを初期化しました。"
            except Exception as e:
                error_message = f"初期化エラー: {e}"

    try:
        desc1, all_users = fetch_table_data('all_users')
        desc2, selected_users = fetch_table_data('selected_users')
        return render_template(html,
                               all_users=all_users,
                               selected_users=selected_users,
                               sql=sql,
                               message=message,
                               error_message=error_message)
    except Exception as e:
        return render_template(html)




#delete single 学習
@app.route('/basic/delete/single/study', methods=['GET', 'POST'])
def delete_single_study():
    return render_template('delete_single_study.html')

#delete single 実行例
@app.route('/basic/delete/single/example', methods=['GET', 'POST'])
def delete_single_example():
    return render_template('delete_single_example.html')

#delete multiple 学習
@app.route('/basic/delete/multiple/study', methods=['GET', 'POST'])
def delete_multiple_study():
    return render_template('delete_multiple_study.html')

#delete multiple 実行例
@app.route('/basic/delete/multiple/example', methods=['GET', 'POST'])
def delete_multiple_example():
    return render_template('delete_multiple_example.html')

#DELETE文 演習ページ
@app.route('/basic/delete/<type>/practice', methods=['GET', 'POST'])
def delete(type):
    table_name = "employees"
    if type == 'single':
        url = 'delete.html'
    elif type == 'multiple':
        url = 'delete_mul.html'
    else:
        print(f"ページが存在しません。/basic/delete/<type>/practiceでtypeの部分をsingleかmultipleでもう一度確かめてみてください。")
        error_message = "ページが存在しません。/basic/delete/<type>/practiceでtypeの部分をsingleかmultipleでもう一度確かめてみてください。"
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

#quiz 管理
@app.route('/quiz/<quiz_type>', methods=['GET', 'POST'])
def quiz(quiz_type):
    # データベース接続
    conn = mysql.connector.MySQLConnection(**dns)
    cursor = conn.cursor(dictionary=True)

    # 質問と選択肢をJOINで取得
    cursor.execute("""
        SELECT q.id AS question_id, q.question_text, q.explanation,
               c.id AS choice_id, c.choice_text, c.is_correct
        FROM questions AS q
        JOIN choices AS c ON q.id = c.question_id
        WHERE q.category = %s
        ORDER BY q.id, c.id
    """, (quiz_type,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # クイズが存在しない場合
    if not rows:
        return "クイズが見つかりません", 404

    # 問題を構造化（choicesを辞書で保持）
    questions = []
    current_qid = None
    q_data = {}

    for row in rows:
        if row["question_id"] != current_qid:
            if q_data:
                questions.append(q_data)
            q_data = {
                "id": row["question_id"],
                "question": row["question_text"],
                "explanation": row["explanation"],
                "choices": [],
                "answer": None
            }
            current_qid = row["question_id"]

        choice_data = {
            "id": row["choice_id"],
            "text": row["choice_text"],
            "is_correct": row["is_correct"]
        }
        q_data["choices"].append(choice_data)

        if row["is_correct"]:
            q_data["answer"] = row["choice_text"]

    if q_data:
        questions.append(q_data)


    # POST送信時の処理
    submitted = False
    score = 0
    user_answers = {}

    if request.method == 'POST':
        submitted = True
        for i, question in enumerate(questions):
            key = f"answer_{i}"
            selected = request.form.get(key)
            user_answers[key] = selected
            if selected == question["answer"]:
                score += 1

        # --- スコアをprogressに保存 ---
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを取得
        quiz_name = quiz_type.replace("_", " ")
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()


        if result:
            quiz_id = result[0]
            cursor.execute("""
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))
            conn.commit()
        
        cursor.close()
        conn.close()


    return render_template("quiz_base.html",
                           quiz_type=quiz_type,
                           questions=questions,
                           submitted=submitted,
                           user_answers=user_answers,
                           score=score,
                           total=len(questions))



@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template('error.html', error_message=error)


# ユーザー管理系
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
            tables = ['users', 'products', 'products_initialstate', 'discounts', 'customers', 'inventory', 'employees', 'sales',
                    'quiz_list', 'progress', 'all_users', 'selected_users']
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
            
            flash("ユーザー登録が完了しました", "success")
            print('ユーザー登録が完了しました')
            return redirect(url_for('login'))

    return render_template('signup.html')

#ログイン機能
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # パラメータ化されたクエリ（SQLインジェクション対策）
            select_user_query = "SELECT id, username, password, is_admin FROM users WHERE username = " + username
            users = user_db.query(select_user_query)

            if users and bcrypt.check_password_hash(users[0][2], password):
                session['user_id'] = users[0][0]
                session['username'] = users[0][1]
                session['is_admin'] = (users[0][3] == 1)

                user_db_name = f"{username}_db"
                this_users_dns['database'] = user_db_name
                return redirect(url_for('main'))
            else:
                flash("パスワードかユーザー名が違います", "danger")

        except Exception as e:
            print(f"Login Error: {e}")
            flash("ログイン中にエラーが発生しました", "danger")

    return render_template('login.html')



#ログアウト
@app.route('/logout')
def logout():
    session.clear()
    this_users_dns['database'] = None
    return redirect(url_for('login'))

from functools import wraps
# 管理者のみがアクセスできるページ権限
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("管理者のみアクセス可能です。", "danger")
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return decorated_function


#ユーザー管理ページ
@app.route('/user_management', methods=['GET', 'POST'])
@admin_required
def user_management():
    stmt = "SELECT id, username FROM users"
    users = user_db.query(stmt)
    return render_template('user_management.html', users=users)

#ユーザー削除ページ
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    try:
        # ユーザー名とDB名取得
        user_info = user_db.query(f"SELECT username FROM users WHERE id = {user_id}")
        if not user_info:
            flash("ユーザーが見つかりませんでした。", "danger")
            return redirect(url_for('user_management'))

        username = user_info[0][0]
        db_name = f"{username}_db"

        # 専用DB削除
        conn = mysql.connector.MySQLConnection(**user_dns)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
        cursor.execute(f"DELETE FROM user_databases WHERE user_id = {user_id}")
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        conn.commit()
        cursor.close()
        conn.close()

        flash("ユーザーを削除しました。", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash("ユーザーの削除に失敗しました。", "danger")

    return redirect(url_for('user_management'))

#ユーザーの進捗チェック
@app.route('/user_progress/<username>')
@admin_required
def user_progress(username):
    try:
        # 接続はユーザーDBだが、クエリで dataset. を明示する
        user_dbname = f"{username}_db"
        this_users_dns['database'] = user_dbname
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ds_ql.quiz_name, 
                IFNULL(up.score, 0) AS score,
                COUNT(ds_q.id) AS total_questions
            FROM dataset.quiz_list ds_ql
            LEFT JOIN {}.progress up ON ds_ql.id = up.quiz_id
            LEFT JOIN dataset.questions ds_q 
                ON ds_q.category COLLATE utf8mb4_general_ci = ds_ql.quiz_name COLLATE utf8mb4_general_ci
            GROUP BY ds_ql.id
        """.format(user_dbname))


        progress = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('user_progress.html', username=username, progress=progress)

    except Exception as e:
        print(f"Error: {e}")
        return render_template("error.html", error_message="進捗の取得に失敗しました。")






#-------------------------------------------------------------------------#
#
# 
# ここから荒木が作成！！！！！！！！！！！！！！！！！！
#
# 
# -------------------------------------------------------------------------#

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
@app.route('/basic/update/single-column', methods=['GET', 'POST'])
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
@app.route('/group-by', methods=['GET', 'POST'])
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
@app.route('/basic/update/join', methods=['GET', 'POST'])
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




    return render_template('join_select.html')

# 以下は各JOINページ
#CROSS JOIN 学習ページ
@app.route('/basic/join/cross_join/study', methods=['GET', 'POST'])
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
@app.route('/basic/join/cross_join/example', methods=['GET'])
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

# CROSS JOIN 演習ページ
@app.route('/basic/join/cross_join/practice', methods=['GET', 'POST'])
def cross_join_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # productsテーブルとcustomersテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # customersテーブルの内容を取得
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'cross_join_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            customers_data=[],
            products_desc=[],
            customers_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'cross_join_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        customers_data=customers_data,
        products_desc=products_desc,
        customers_desc=customers_desc
    )


# CROSS JOIN クイズページ(cross_join_quiz.html)
@app.route('/basic/join/cross_join/quiz', methods=['GET', 'POST'])
def cross_join_quiz():
    questions = [
        {
            'question': "CROSS JOINは何を行いますか？",
            'choices': [
                "2つのテーブルを条件付きで結合する",
                "2つのテーブルのすべてのレコードの組み合わせを作成する",
                "1つのテーブルに新しいレコードを追加する",
                "特定の列のデータを変更する"
            ],
            'answer': "2つのテーブルのすべてのレコードの組み合わせを作成する",
            'explanation': "CROSS JOINは、2つのテーブルのすべてのレコードを組み合わせた結果を返します。"
        },
        {
            'question': "次のCROSS JOINの結果は何レコードになりますか？\nテーブルAに3行2列、テーブルBに4行5列のデータがあります。",
            'choices': [
                "3レコード",
                "4レコード",
                "7レコード",
                "12レコード"
            ],
            'answer': "12レコード",
            'explanation': "CROSS JOINの結果は、テーブルAの行数×テーブルBの行数になります。この場合、3×4＝12レコードです。"
        },
        {
            'question': "CROSS JOINの結果が非常に多くの行になる場合、どのような問題が発生する可能性がありますか？",
            'choices': [
                "メモリの使用量が増える可能性がある",
                "SQLクエリが常に失敗する",
                "結果が予期せぬ順序で表示される",
                "SQL文が遅くなることはない"
            ],
            'answer': "メモリの使用量が増える可能性がある",
            'explanation': "CROSS JOINで生成される組み合わせの数が増えると、結果として大量のメモリを消費する可能性があります。"
        },
        {
            'question': "CROSS JOINを使用する際に注意すべきことは何ですか？",
            'choices': [
                "結合条件を指定することを忘れないこと",
                "テーブルの数が多い場合にパフォーマンスに影響が出る可能性がある",
                "WHERE句を必ず使用すること",
                "結果は常に昇順に並べられること"
            ],
            'answer': "テーブルの数が多い場合にパフォーマンスに影響が出る可能性がある",
            'explanation': "テーブルの行数が多くなるほど、CROSS JOINの結果として生成される組み合わせの数も多くなり、パフォーマンスに影響を与えることがあります。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM products CROSS JOIN customers;",
            'choices': [
                "productsとcustomersのすべてのレコードが組み合わせられる",
                "productsテーブルのデータのみ表示される",
                "customersテーブルのデータのみ表示される",
                "エラーが発生する"
            ],
            'answer': "productsとcustomersのすべてのレコードが組み合わせられる",
            'explanation': "CROSS JOINを使用すると、2つのテーブルのすべてのレコードの組み合わせが表示されます。"
        },
        {
            'question': "次のSQL文でCROSS JOINの結果をフィルタリングするには、どの句を使用しますか？\nSELECT * FROM products CROSS JOIN customers;",
            'choices': [
                "WHERE句",
                "GROUP BY句",
                "HAVING句",
                "ORDER BY句"
            ],
            'answer': "WHERE句",
            'explanation': "CROSS JOINの結果をフィルタリングするにはWHERE句を使用します。"
        },
        {
            'question': "CROSS JOINの別名として使用される言葉は？",
            'choices': [
                "自己結合",
                "内部結合",
                "完全結合",
                "デカルト積"
            ],
            'answer': "デカルト積",
            'explanation': "CROSS JOINはデカルト積（Cartesian Product）とも呼ばれます。"
        },
        {
            'question': "CROSS JOINの用途として適切なものはどれですか？",
            'choices': [
                "レポート作成のためにすべての組み合わせを生成する",
                "データの重複を削除する",
                "テーブルの結合を最適化する",
                "特定の条件に基づいてレコードを削除する"
            ],
            'answer': "レポート作成のためにすべての組み合わせを生成する",
            'explanation': "CROSS JOINは、すべての組み合わせを生成する際に役立ちます。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        # クイズの問題に対するスコア計算
        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'CROSS JOIN'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('cross_join_quiz.html', error_message=error_message)

        return render_template(
            'cross_join_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'cross_join_quiz.html',
        questions=questions,
        submitted=False
    )


#INNER JOIN 学習ページ(inner_join_study.html)
@app.route('/basic/join/inner_join/study', methods=['GET', 'POST'])
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

#INNER JOIN 演習ページ(inner_join_advance.html)
@app.route('/basic/join/inner_join/practice', methods=['GET', 'POST'])
def inner_join_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # productsテーブルとcustomersテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # customersテーブルの内容を取得
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'inner_join_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            customers_data=[],
            products_desc=[],
            customers_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']
          
            #クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証
            if query.count(';') != 1:
                raise ValueError("クエリには必ず1つだけセミコロンを含めてください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'inner_join_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        customers_data=customers_data,
        products_desc=products_desc,
        customers_desc=customers_desc
    )

# INNER JOIN 実行例ページ
@app.route('/basic/join/inner_join/example', methods=['GET'])
def inner_join_study_example():
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

        # INNER JOINのクエリを実行
        inner_join_query = """
        SELECT products.product_id, products.product_name, customers.customer_id, customers.order_date
        FROM products
        INNER JOIN customers ON products.product_id = customers.product_id;
        """
        cursor.execute(inner_join_query)
        inner_join_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('inner_join_study_example.html', error_message=error_message)
    
    # カラム情報の設定
    columns = "products.product_id, products.product_name, customers.customer_id, customers.order_date"

    return render_template('inner_join_study_example.html',  products_desc=products_desc, customers_desc=customers_desc, products_data=products_data, customers_data=customers_data,
                           inner_join_result=inner_join_result, columns=columns)

# INNER JOIN クイズページ(inner_join_quiz.html)
@app.route('/basic/join/inner_join/quiz', methods=['GET', 'POST'])
def inner_join_quiz():
    questions = [
        {
            'question': "INNER JOINは何を行いますか？",
            'choices': [
                "すべてのレコードを結合する",
                "2つのテーブルで共通するレコードを結合する",
                "片方のテーブルのすべてのレコードを取得する",
                "一方のテーブルのみを結合する"
            ],
            'answer': "2つのテーブルで共通するレコードを結合する",
            'explanation': "INNER JOINは、2つのテーブルの共通部分を基準にレコードを結合します。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM products INNER JOIN customers ON products.product_id = customers.product_id;",
            'choices': [
                "productsとcustomersのすべてのレコードが表示される",
                "productsテーブルのすべてのレコードが表示される",
                "共通のproduct_idを持つレコードのみ表示される",
                "エラーが発生する"
            ],
            'answer': "共通のproduct_idを持つレコードのみ表示される",
            'explanation': "INNER JOINは、共通するproduct_idを持つレコードのみを結合します。"
        },
        {
            'question': "INNER JOINの結果が空になるのはどのような場合ですか？",
            'choices': [
                "すべてのレコードが一致しない場合",
                "一方のテーブルにレコードがない場合",
                "一方のテーブルにNULL値が含まれている場合",
                "すべての選択肢"
            ],
            'answer': "すべてのレコードが一致しない場合",
            'explanation': "INNER JOINは共通するレコードがない場合、結果は空になります。"
        },
        {
            'question': "次のSQL文のWHERE句は、INNER JOINのどの部分に影響を与えますか？\nSELECT * FROM products INNER JOIN customers ON products.product_id = customers.product_id WHERE customers.order_date > '2023-08-01';",
            'choices': [
                "結合の条件",
                "結果セットのフィルタリング",
                "両方",
                "どちらでもない"
            ],
            'answer': "結果セットのフィルタリング",
            'explanation': "WHERE句はINNER JOINの後に適用され、結果セットをフィルタリングします。"
        },
        {
            'question': "INNER JOINと等価な別の結合方法は？",
            'choices': [
                "LEFT JOIN",
                "RIGHT JOIN",
                "CROSS JOIN",
                "JOIN (ON句付き)"
            ],
            'answer': "JOIN (ON句付き)",
            'explanation': "INNER JOINはJOINとON句を使用することで同じ結果が得られます。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM products INNER JOIN discounts ON products.product_id = discounts.product_id;",
            'choices': [
                "productsとdiscountsのすべてのレコード",
                "共通のproduct_idを持つレコードのみ",
                "productsテーブルのすべてのレコード",
                "discountsテーブルのすべてのレコード"
            ],
            'answer': "共通のproduct_idを持つレコードのみ",
            'explanation': "INNER JOINは共通するproduct_idを持つレコードを結合します。"
        },
        {
            'question': "次のSQL文は正しいですか？\nSELECT * FROM products INNER JOIN customers;",
            'choices': [
                "はい",
                "いいえ",
                "一部のデータベースでは正しい",
                "不明"
            ],
            'answer': "いいえ",
            'explanation': "INNER JOINを使用する場合は、ON句を指定する必要があります。"
        },
        {
            'question': "INNER JOINを使用する理由として最も適切なのは？",
            'choices': [
                "すべての組み合わせを生成するため",
                "共通のデータを抽出するため",
                "一方のテーブルのすべてのレコードを表示するため",
                "データを削除するため"
            ],
            'answer': "共通のデータを抽出するため",
            'explanation': "INNER JOINは、共通のデータを抽出する際に使用されます。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1
        
        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'INNER JOIN'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('inner_join_quiz.html', error_message=error_message)


        return render_template(
            'inner_join_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'inner_join_quiz.html',
        questions=questions,
        submitted=False
    )


#LEFT OUTER JOIN 学習ページ(left_outer_join_study.html)
@app.route('/basic/join/left_outer_join/study', methods=['GET', 'POST'])
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

#LEFT OUTER JOIN 演習ページ(left_outer_join_advance.html)
@app.route('/basic/join/left_outer_join/practice', methods=['GET', 'POST'])
def left_outer_join_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # productsテーブルとcustomersテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # customersテーブルの内容を取得
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'left_outer_join_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            customers_data=[],
            products_desc=[],
            customers_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証
            if query.count(';') != 1:
                raise ValueError("クエリには必ず1つだけセミコロンを含めてください。複数のクエリは実行できません。")


            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'left_outer_join_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        customers_data=customers_data,
        products_desc=products_desc,
        customers_desc=customers_desc
    )


# LEFT OUTER JOINの実行例ページ
@app.route('/basic/join/left_outer_join/example', methods=['GET'])
def left_outer_join_study_example():
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

        # LEFT OUTER JOINのクエリを実行
        left_outer_join_query = """
        SELECT products.product_id, products.product_name, customers.customer_id, customers.order_date
        FROM products
        LEFT OUTER JOIN customers ON products.product_id = customers.product_id;
        """
        cursor.execute(left_outer_join_query)
        left_outer_join_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('left_outer_join_study_example.html', error_message=error_message)
    
    # カラム情報の設定
    columns = "products.product_id, products.product_name, customers.customer_id, customers.order_date"

    return render_template('left_outer_join_study_example.html',  products_desc=products_desc, customers_desc=customers_desc, products_data=products_data, customers_data=customers_data,
                           left_outer_join_result=left_outer_join_result, columns=columns)

# LEFT OUTER JOIN クイズページ(left_outer_join_quiz.html)
@app.route('/basic/join/left_outer_join/quiz', methods=['GET', 'POST'])
def left_outer_join_quiz():
    questions = [
        {
            'question': "LEFT OUTER JOINとINNER JOINの主な違いは何ですか？",
            'choices': [
                "LEFT OUTER JOINは両方のテーブルから一致するレコードのみを返す",
                "INNER JOINは左側のテーブルのすべてのレコードを返す",
                "LEFT OUTER JOINは右側のテーブルに一致するレコードがない場合も左側のレコードを返す",
                "INNER JOINはNULLを返すことがある"
            ],
            'answer': "LEFT OUTER JOINは右側のテーブルに一致するレコードがない場合も左側のレコードを返す",
            'explanation': "INNER JOINは一致するレコードのみを返しますが、LEFT OUTER JOINは右側に一致するレコードがない場合でも、左側のテーブルのレコードを返します。"
        },
        {
            'question': "LEFT OUTER JOINの主な特徴は次のうちどれですか？",
            'choices': [
                "結合条件に一致するレコードのみを返す",
                "左側のテーブルのすべてのレコードを返し、右側の一致するレコードを返す",
                "両方のテーブルのすべてのレコードを返す",
                "一致しないレコードはすべて除外される"
            ],
            'answer': "左側のテーブルのすべてのレコードを返し、右側の一致するレコードを返す",
            'explanation': "LEFT OUTER JOINは、左側のテーブルのすべてのレコードを返し、右側のテーブルから一致するレコードを追加します。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM products LEFT OUTER JOIN discounts ON products.product_id = discounts.product_id;",
            'choices': [
                "productsとdiscountsの共通するレコードのみ",
                "productsテーブルのすべてのレコードと一致するdiscountsのレコード",
                "共通するレコードがない場合、結果は空になる",
                "エラーが発生する"
            ],
            'answer': "productsテーブルのすべてのレコードと一致するdiscountsのレコード",
            'explanation': "LEFT OUTER JOINでは、productsのすべてのレコードが表示され、一致するdiscountsのレコードが追加されます。"
        },
        {
            'question': "LEFT OUTER JOINを使用する主な理由は次のうちどれですか？",
            'choices': [
                "すべてのレコードの組み合わせを生成するため",
                "両方のテーブルから共通するデータのみを取得するため",
                "片方のテーブルのすべてのレコードを保持するため",
                "データを削除するため"
            ],
            'answer': "片方のテーブルのすべてのレコードを保持するため",
            'explanation': "LEFT OUTER JOINは、左側のテーブルのすべてのレコードを保持しつつ、右側のテーブルの一致するレコードを追加します。"
        },
        {
            'question': "LEFT OUTER JOINを使用して一致しないレコードをNULLとして返すのはどのテーブルですか？",
            'choices': [
                "左側のテーブル",
                "右側のテーブル",
                "両方のテーブル",
                "どちらでもない"
            ],
            'answer': "右側のテーブル",
            'explanation': "一致しないレコードは右側のテーブルのデータがNULLとして返されます。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT products.product_name, discounts.discount_rate FROM products LEFT OUTER JOIN discounts ON products.product_id = discounts.product_id WHERE discounts.discount_rate IS NULL;",
            'choices': [
                "すべての製品と割引率",
                "割引が適用されていない製品",
                "すべての割引が適用された製品",
                "一致する製品がない"
            ],
            'answer': "割引が適用されていない製品",
            'explanation': "WHERE句でdiscount_rateがNULLである製品をフィルタリングすることで、割引が適用されていない製品を取得します。"
        },
        {
            'question': "次のSQL文は正しいですか？\nSELECT * FROM products LEFT OUTER JOIN customers;",
            'choices': [
                "はい",
                "いいえ",
                "一部のデータベースでは正しい",
                "不明"
            ],
            'answer': "いいえ",
            'explanation': "LEFT OUTER JOINを使用する場合は、ON句を指定する必要があります。"
        },
        {
            'question': "LEFT OUTER JOINを使用して、どのような場合にNULL値が発生しますか？",
            'choices': [
                "右側のテーブルに一致するレコードがない場合",
                "左側のテーブルに一致するレコードがない場合",
                "両方のテーブルに一致するレコードがない場合",
                "NULL値は発生しない"
            ],
            'answer': "右側のテーブルに一致するレコードがない場合",
            'explanation': "LEFT OUTER JOINでは、右側のテーブルに一致するレコードがない場合、右側の列はNULLとして返されます。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1
    
    # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'LEFT OUTER JOIN'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('left_puter_join_quiz.html', error_message=error_message)


        return render_template(
            'left_outer_join_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'left_outer_join_quiz.html',
        questions=questions,
        submitted=False
    )


#RIGHT OUTER JOIN 学習ページ(right_outer_join_study.html)
@app.route('/basic/join/right_outer_join/study', methods=['GET', 'POST'])
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


#RIGHT OUTER JOIN 演習ページ(right_outer_join_advance.html)
@app.route('/basic/join/right_outer_join/practice', methods=['GET', 'POST'])
def right_outer_join_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # productsテーブルとcustomersテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # customersテーブルの内容を取得
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.execute("DESC customers")
        customers_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'right_outer_join_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            customers_data=[],
            products_desc=[],
            customers_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証
            if query.count(';') != 1:
                raise ValueError("クエリには必ず1つだけセミコロンを含めてください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'right_outer_join_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        customers_data=customers_data,
        products_desc=products_desc,
        customers_desc=customers_desc
    )


# RIGHT OUTER JOINの実行例ページ
@app.route('/basic/join/right_outer_join/example', methods=['GET'])
def right_outer_join_study_example():
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

        # RIGHT OUTER JOINのクエリを実行
        right_outer_join_query = """
        SELECT products.product_id, products.product_name, customers.customer_id, customers.order_date
        FROM products
        RIGHT OUTER JOIN customers ON products.product_id = customers.product_id;
        """
        cursor.execute(right_outer_join_query)
        right_outer_join_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('right_outer_join_study_example.html', error_message=error_message)
    
    # カラム情報の設定
    columns = "products.product_id, products.product_name, customers.customer_id, customers.order_date"

    return render_template('right_outer_join_study_example.html',  products_desc=products_desc, customers_desc=customers_desc, products_data=products_data, customers_data=customers_data,
                           right_outer_join_result=right_outer_join_result, columns=columns)

# RIGHT OUTER JOIN クイズページ(right_outer_join_quiz.html)
@app.route('/basic/join/right_outer_join/quiz', methods=['GET', 'POST'])
def right_outer_join_quiz():
    questions = [
        {
            'question': "RIGHT OUTER JOINの主な特徴は次のうちどれですか？",
            'choices': [
                "結合条件に一致するレコードのみを返す",
                "右側のテーブルのすべてのレコードを返し、左側の一致するレコードを返す",
                "両方のテーブルのすべてのレコードを返す",
                "左側のテーブルのすべてのレコードを返し、右側の一致するレコードを返す"
            ],
            'answer': "右側のテーブルのすべてのレコードを返し、左側の一致するレコードを返す",
            'explanation': "RIGHT OUTER JOINは、右側のテーブルのすべてのレコードを返し、左側の一致するレコードを追加します。"
        },
        {
            'question': "RIGHT OUTER JOINとLEFT OUTER JOINの主な違いは何ですか？",
            'choices': [
                "RIGHT OUTER JOINは左側のテーブルのすべてのレコードを返す",
                "LEFT OUTER JOINは右側のテーブルのすべてのレコードを返す",
                "RIGHT OUTER JOINは右側のテーブルに一致するレコードがない場合も左側のレコードを返す",
                "LEFT OUTER JOINは右側のテーブルに一致するレコードがない場合も右側のレコードを返す"
            ],
            'answer': "RIGHT OUTER JOINは右側のテーブルに一致するレコードがない場合も左側のレコードを返す",
            'explanation': "RIGHT OUTER JOINは右側のテーブルに一致するレコードがない場合でも、左側のテーブルのレコードをNULLとして返します。"
        },
        {
            'question': "RIGHT OUTER JOINの結果、左側のテーブルに一致しないレコードはどうなりますか？",
            'choices': [
                "NULLとして表示される",
                "右側のテーブルのレコードと結合される",
                "結果から除外される",
                "何も表示されない"
            ],
            'answer': "NULLとして表示される",
            'explanation': "RIGHT OUTER JOINでは、左側のテーブルに一致しないレコードはNULLとして表示されます。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM products RIGHT OUTER JOIN customers ON products.product_id = customers.product_id WHERE customers.customer_id IS NOT NULL;",
            'choices': [
                "購入者がいない製品とその購入者",
                "購入者の情報のみ",
                "すべての製品とその購入者",
                "NULL値のない製品のみ"
            ],
            'answer': "購入者の情報のみ",
            'explanation': "WHERE句でcustomer_idがNULLでないレコードをフィルタリングすることで、購入者の情報のみを取得します。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT * FROM customers RIGHT OUTER JOIN products ON customers.product_id = products.product_id;",
            'choices': [
                "customersとproductsの共通するレコードのみ",
                "customersテーブルのすべてのレコードと一致するproductsのレコード",
                "productsテーブルのすべてのレコードと一致するcustomersのレコード",
                "共通するレコードがない場合、結果は空になる"
            ],
            'answer': "productsテーブルのすべてのレコードと一致するcustomersのレコード",
            'explanation': "RIGHT OUTER JOINでは、右側のテーブルであるproductsのすべてのレコードが表示され、一致するcustomersのレコードが追加されます。"
        },
        {
            'question': "RIGHT OUTER JOINを使用する主な理由は次のうちどれですか？",
            'choices': [
                "すべてのレコードの組み合わせを生成するため",
                "左側のテーブルから共通するデータのみを取得するため",
                "右側のテーブルのすべてのレコードを保持するため",
                "データを削除するため"
            ],
            'answer': "右側のテーブルのすべてのレコードを保持するため",
            'explanation': "RIGHT OUTER JOINは、右側のテーブルのすべてのレコードを保持しつつ、左側の一致するレコードを追加します。"
        },
        {
            'question': "RIGHT OUTER JOINを使用して一致しないレコードをNULLとして返すのはどのテーブルですか？",
            'choices': [
                "左側のテーブル",
                "右側のテーブル",
                "両方のテーブル",
                "どちらでもない"
            ],
            'answer': "左側のテーブル",
            'explanation': "一致しないレコードは左側のテーブルのデータがNULLとして返されます。"
        },
        {
            'question': "次のSQL文の結果は？\nSELECT customers.customer_id, products.product_name FROM customers RIGHT OUTER JOIN products ON customers.product_id = products.product_id WHERE customers.customer_id IS NULL;",
            'choices': [
                "すべての購入者と商品名",
                "購入者がいない商品",
                "すべての購入者がNULL",
                "一致するレコードがない"
            ],
            'answer': "購入者がいない商品",
            'explanation': "WHERE句でcustomer_idがNULLである商品をフィルタリングすることで、購入者がいない商品を取得します。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'RIGHT OUTER JOIN'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('right_outer_join_quiz.html', error_message=error_message)


        return render_template(
            'right_outer_join_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'right_outer_join_quiz.html',
        questions=questions,
        submitted=False
    )


#複数のテーブルJOIN 学習ページ(multiple_table_join_study.html)
@app.route('/basic/join/multiple_table_join/study', methods=['GET', 'POST'])
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

#複数のテーブルJOIN 演習ページ(multiple_table_join_advance.html)
@app.route('/basic/join/multiple_table_join/practice', methods=['GET', 'POST'])
def multiple_table_join_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # テーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # customersテーブルの内容を取得
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()

        # discountsテーブルの内容を取得
        cursor.execute("SELECT * FROM discounts")
        discounts_data = cursor.fetchall()

        # inventoryテーブルの内容を取得
        cursor.execute("SELECT * FROM inventory")
        inventory_data = cursor.fetchall()

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
        return render_template(
            'multiple_table_join_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            customers_data=[],
            discounts_data=[],
            inventory_data=[],
            products_desc=[],
            customers_desc=[],
            discounts_desc=[],
            inventory_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証
            if query.count(';') != 1:
                raise ValueError("クエリには必ず1つだけセミコロンを含めてください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'multiple_table_join_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        customers_data=customers_data,
        discounts_data=discounts_data,
        inventory_data=inventory_data,
        products_desc=products_desc,
        customers_desc=customers_desc,
        discounts_desc=discounts_desc,
        inventory_desc=inventory_desc
    )



# JOINのまとめクイズページ(quiz.html)
@app.route('/basic/join/join_quiz', methods=['GET', 'POST'])
def join_quiz():
    questions = [
        {   # INNER JOINの基本的な知識問題
            'question': "INNER JOINを使用する際、結合条件に一致しない行はどうなりますか？",
            'choices': [
                "結果セットに含まれない",
                "NULLとして表示される",
                "すべての行が表示される",
                "データベースエラーが発生する"
            ],
            'answer': "結果セットに含まれない"
        },
        {   # LEFT OUTER JOINの説明
            'question': "LEFT OUTER JOINを使用する場合、左側のテーブルにあるが右側のテーブルにない行はどうなりますか？",
            'choices': [
                "結果セットに含まれない",
                "NULL値で結果セットに含まれる",
                "デフォルト値が設定される",
                "エラーが発生する"
            ],
            'answer': "NULL値で結果セットに含まれる"
        },
        {   # RIGHT OUTER JOINの動作理解
            'question': "RIGHT OUTER JOINはどのように動作しますか？",
            'choices': [
                "左側のテーブルのすべての行を返し、右側のテーブルの一致する行を返す",
                "右側のテーブルのすべての行を返し、左側のテーブルの一致する行を返す",
                "両方のテーブルのすべての行を返す",
                "一致する行のみを返す"
            ],
            'answer': "右側のテーブルのすべての行を返し、左側のテーブルの一致する行を返す"
        },
        {   # CROSS JOINの知識問題
            'question': "CROSS JOINの結果セットに含まれる行数は、どのように計算されますか？",
            'choices': [
                "両方のテーブルの行数の合計",
                "両方のテーブルの行数の積",
                "常に一定の行数",
                "条件に依存する"
            ],
            'answer': "両方のテーブルの行数の積"
        },
        {   # INNER JOINのSQLコード問題
            'question': "次のSQLクエリの結果を選んでください:\n\nSELECT customers.customer_id, products.product_name \nFROM customers \nINNER JOIN products ON customers.product_id = products.product_id;",
            'choices': [
                "すべての購入者と商品が表示される",
                "購入者とその購入した商品が表示される",
                "すべての商品が表示される",
                "エラーが発生する"
            ],
            'answer': "購入者とその購入した商品が表示される"
        },
        {   # LEFT JOINのコード問題
            'question': "次のSQLクエリの結果として、NULL値が含まれるのはどのケースですか？\n\nSELECT products.product_name, discounts.discount_rate \nFROM products \nLEFT JOIN discounts ON products.product_id = discounts.product_id;",
            'choices': [
                "すべての製品に割引がある場合",
                "一部の製品に割引がない場合",
                "製品テーブルが空の場合",
                "割引率が0の場合"
            ],
            'answer': "一部の製品に割引がない場合"
        },
        {   # RIGHT JOINのコード問題
            'question': "次のSQLクエリの結果を予測してください:\n\nSELECT inventory.product_id, products.product_name \nFROM inventory \nRIGHT JOIN products ON inventory.product_id = products.product_id;",
            'choices': [
                "すべての在庫と製品名が表示される",
                "すべての製品名が表示されるが、一部の在庫がNULLになる",
                "すべての製品と在庫が一致する",
                "エラーが発生する"
            ],
            'answer': "すべての製品名が表示されるが、一部の在庫がNULLになる"
        },
        {   # CROSS JOINのコード問題
            'question': "次のSQLクエリの結果として、何行の結果が返されますか？\n\nSELECT * FROM customers CROSS JOIN discounts;",
            'choices': [
                "顧客テーブルの行数と割引テーブルの行数の合計",
                "顧客テーブルの行数と割引テーブルの行数の積",
                "常に10行",
                "NULL値が含まれる"
            ],
            'answer': "顧客テーブルの行数と割引テーブルの行数の積"
        },
        {   # 複数テーブルをJOINする問題
            'question': "次のSQLクエリは何を実行しますか？\n\nSELECT customers.customer_id, products.product_name, discounts.discount_rate \nFROM customers \nINNER JOIN products ON customers.product_id = products.product_id \nLEFT JOIN discounts ON products.product_id = discounts.product_id;",
            'choices': [
                "顧客IDと商品名のみを表示する",
                "顧客ID、商品名、割引率を表示するが、割引がない場合はNULLになる",
                "割引がある商品のみを表示する",
                "エラーが発生する"
            ],
            'answer': "顧客ID、商品名、割引率を表示するが、割引がない場合はNULLになる"
        },
        {   # 複雑なJOINの理解
            'question': "次のSQLクエリの結果として、どの行が結果セットに含まれるか？\n\nSELECT p.product_name, i.quantity_change \nFROM products p \nLEFT JOIN inventory i ON p.product_id = i.product_id \nWHERE i.quantity_change > 0;",
            'choices': [
                "すべての製品が表示される",
                "在庫が増加した製品のみが表示される",
                "在庫が減少した製品のみが表示される",
                "在庫が変更されなかった製品のみが表示される"
            ],
            'answer': "在庫が増加した製品のみが表示される"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'JOIN SAMMARY'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('join_quiz.html', error_message=error_message)


        return render_template(
            'join_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'join_quiz.html',
        questions=questions,
        submitted=False
    )


#以下はUPDATE!
#UPDATE 学習ページ
@app.route('/update_select', methods=['GET', 'POST'])
def update_select():
    return render_template('update_select.html')

#1つのカラムに対して1つの条件でレコードをUPDATEする(update_single_study)
@app.route('/basic/update/single-column/study', methods=['GET', 'POST'])
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

# 1つのカラムに対して1つの条件でレコードをUPDATEする実行例ページ
@app.route('/basic/update/single-column/example', methods=['GET', 'POST'])
def update_single_example():
    target_product_id = 1  # 更新する商品のID
    new_price = 100000       # 設定する新しい価格
    update_result = False

    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()
        
        # 更新前のproductsテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        # テーブルの構造（カラム名）も取得
        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        # UPDATEクエリを実行
        update_query = """
        UPDATE products
        SET price = %s
        WHERE product_id = %s;
        """
        cursor.execute(update_query, (new_price, target_product_id))
        conn.commit()
        update_result = True

        # 更新後のproductsテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        updated_products_data = cursor.fetchall()

        cursor.close()
        conn.close()

        # テーブルを初期状態に戻す処理
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

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('update_single_study_example.html', error_message=error_message)
    
    return render_template('update_single_study_example.html',products_desc=products_desc, products_data=products_data,
                           updated_products_data=updated_products_data, update_result=update_result, 
                           target_product_id=target_product_id, new_price=new_price)

#複数のカラムに対して複数の条件でレコードをUPDATEする(update_multiple_study)
@app.route('/basic/update/multiple-columns/study', methods=['GET', 'POST'])
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

# 複数のカラムに対して複数の条件でレコードをUPDATEする実行例ページ
@app.route('/basic/update/multiple-columns/example', methods=['GET', 'POST'])
def update_multiple_study_example():
    target_product_id = 2      # 更新する商品のID
    target_status = 'active'   # 更新対象のステータス
    new_price = 190000           # 設定する新しい価格
    new_stock = 80             # 設定する新しい在庫数
    update_result = False

    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        # UPDATEクエリを実行
        update_query = """
        UPDATE products
        SET price = %s, stock_quantity = %s
        WHERE product_id = %s AND status = %s;
        """
        cursor.execute(update_query, (new_price, new_stock, target_product_id, target_status))
        conn.commit()
        update_result = True

        # 更新後のproductsテーブルの中身を取得
        cursor.execute("SELECT * FROM products")
        updated_products_data = cursor.fetchall()

        cursor.close()
        conn.close()

        # テーブルを初期状態に戻す処理
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

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('update_multiple_study_example.html', error_message=error_message)
    
    return render_template(
        'update_multiple_study_example.html',
        products_desc=products_desc, products_data=products_data,
        updated_products_data=updated_products_data,
        update_result=update_result,
        target_product_id=target_product_id,
        target_status=target_status,
        new_price=new_price,
        new_stock=new_stock
    )

# UPDATE文 演習ページ(update_advance.html)
@app.route('/basic/update/practice', methods=['GET', 'POST'])
def update_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # productsテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # productsテーブルの内容を取得
        cursor.execute("SELECT * FROM products")
        products_data = cursor.fetchall()

        cursor.execute("DESC products")
        products_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'update_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            products_data=[],
            products_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            query = query.strip()  # 空白や改行を除去

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # ホワイトリストによる検証（正規表現で厳密に確認）
            if not re.match(r"^UPDATE\s+products\s+SET\s+.+;$", query, re.IGNORECASE):
                raise ValueError("許可されていないSQL文です。UPDATE文であり、かつproductsテーブルへの操作のみ許可されます。")


            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            conn.commit()

            # 更新されたデータを再取得
            cursor.execute("SELECT * FROM products")
            updated_products_data = cursor.fetchall()

            cursor.close()
            conn.close()

            query_result = updated_products_data
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'update_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        products_data=products_data,
        products_desc=products_desc
    )


# UPDATE文 クイズページ(update_quiz.html)
@app.route('/basic/update/quiz', methods=['GET', 'POST'])
def update_quiz():
    questions = [
        {
            'question': "UPDATE文の基本的な役割は何ですか？",
            'choices': [
                "テーブルに新しいレコードを追加する",
                "既存のレコードを削除する",
                "既存のレコードの値を変更する",
                "テーブルの構造を変更する"
            ],
            'answer': "既存のレコードの値を変更する",
            'explanation': "UPDATE文は既存のレコードの値を変更するために使用されます。"
        },
        {
            'question': "次のUPDATE文で何が更新されますか？\nUPDATE products SET price = 90000 WHERE product_id = 1;",
            'choices': [
                "すべての商品の価格が90000に変更される",
                "product_idが1の商品の価格が90000に変更される",
                "価格が90000以上の商品が更新される",
                "変更は行われない"
            ],
            'answer': "product_idが1の商品の価格が90000に変更される",
            'explanation': "WHERE句でproduct_idが1の商品の価格のみ変更されます。"
        },
        {
            'question': "次のUPDATE文の実行結果は？\nUPDATE customers SET order_date = '2024-12-01';",
            'choices': [
                "特定のレコードが更新される",
                "すべてのレコードのorder_dateが更新される",
                "エラーが発生する",
                "NULL値が追加される"
            ],
            'answer': "すべてのレコードのorder_dateが更新される",
            'explanation': "WHERE句が指定されていない場合、すべてのレコードが更新されます。"
        },
        {
            'question': "次のUPDATE文は正しいですか？\nUPDATE discounts SET discount_rate = 0.2 WHERE product_id = 3;",
            'choices': [
                "正しい",
                "正しくない",
                "WHERE句が必要",
                "discount_rateのカラムが不足している"
            ],
            'answer': "正しくない",
            'explanation': "productsテーブルにproduct_id 3のレコードが存在しないため、変更は行われません。"
        },
        {
            'question': "複数のカラムを同時にUPDATEするにはどのように書きますか？",
            'choices': [
                "UPDATE table SET column1 = value1, column2 = value2;",
                "UPDATE table SET column1 = value1 WHERE column2 = value2;",
                "UPDATE table WHERE column1 = value1, column2 = value2;",
                "UPDATE table (column1, column2) VALUES (value1, value2);"
            ],
            'answer': "UPDATE table SET column1 = value1, column2 = value2;",
            'explanation': "複数のカラムを同時に変更するには、SET句でカラム名と値をカンマで区切って指定します。"
        },
        {
            'question': "次のUPDATE文でNULL値がどのように処理されますか？\nUPDATE products SET status = NULL WHERE product_id = 2;",
            'choices': [
                "エラーが発生する",
                "statusがNULLに設定される",
                "statusは変更されない",
                "statusが0に設定される"
            ],
            'answer': "statusがNULLに設定される",
            'explanation': "NULLは特別な値であり、statusカラムに設定することが可能です。"
        },
        # 他の問題を追加...
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'UPDATE'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('update_quiz.html', error_message=error_message)

        return render_template(
            'update_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'update_quiz.html',
        questions=questions,
        submitted=False
    )


# 全レコードUPDATE (update_all_column_study)
@app.route('/basic/update/all-records/study', methods=['GET', 'POST'])
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


#以下は集約関数!
@app.route('/aggregate_select', methods=['GET', 'POST'])
def aggregate_select():
    return render_template('aggregate_select.html')

# 集約関数の注意書きページ(aggregate_notes.html)
@app.route('/aggregation/warning_message')
def aggregate_notes():
    return render_template('aggregate_notes.html')

# COUNT 学習ページ(aggregate_count_study.html)
@app.route('/aggregation/count/study', methods=['GET', 'POST'])
def aggregate_count_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # salesテーブルの構造（カラム名）を取得
        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('aggregate_count_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            count_clauses = []
            count_columns = request.form.getlist('count_column')
            as_columns = request.form.getlist('as_column')
            where_clause = request.form.get('where_clause')

            # COUNTを使用するクエリの作成
            for col, as_col in zip(count_columns, as_columns):
                count_clauses.append(f"COUNT({col}) AS `{as_col}`")

            # WHERE句を使用するかどうかでクエリを分岐
            count_query = "SELECT " + ', '.join(count_clauses) + " FROM sales"
            if where_clause:
                count_query += f" WHERE {where_clause}"
            count_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # COUNTクエリの結果を取得
            cursor.execute(count_query)
            count_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('aggregate_count_study.html', sales_desc=sales_desc, sales_data=sales_data,
                                   count_result=count_result, count_query=count_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('aggregate_count_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('aggregate_count_study.html', sales_desc=sales_desc, sales_data=sales_data)

# COUNT 演習ページ(aggregate_count_advance.html)
@app.route('/aggregation/count/practice', methods=['GET', 'POST'])
def aggregate_count_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'aggregate_count_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'aggregate_count_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# COUNT 実行例
@app.route('/aggregation/count/example', methods=['GET', 'POST'])
def aggregate_count_example():
    return 0


# COUNT クイズページ(aggregate_count_quiz.html)
@app.route('/aggregation/count/quiz', methods=['GET', 'POST'])
def aggregate_count_quiz():
    questions = [
        {
            'question': "COUNT関数の主な目的は何ですか？",
            'choices': [
                "すべての行の合計を計算する",
                "NULL値を含むすべての行を数える",
                "指定したカラムの非NULL値の数を数える",
                "文字列データを連結する"
            ],
            'answer': "指定したカラムの非NULL値の数を数える",
            'explanation': "COUNT関数は、指定したカラムの非NULL値の数をカウントします。COUNT(*)は、NULLを含むすべての行をカウントしますが、カラム名を指定した場合は非NULL値のみが対象です。"
        },
        {
            'question': "次のクエリの結果はどうなりますか？ SELECT COUNT(*) FROM sales;",
            'choices': [
                "salesテーブルのすべての行数が返される",
                "NULL値を除いた行数が返される",
                "商品の合計数が返される",
                "エラーが発生する"
            ],
            'answer': "salesテーブルのすべての行数が返される",
            'explanation': "COUNT(*)はテーブル内のすべての行をカウントします。NULL値を含む行もカウントされます。"
        },
        {
            'question': "COUNT関数にNULL値を含むカラムを指定した場合、結果はどうなりますか？",
            'choices': [
                "NULL値も含めてすべての行をカウントする",
                "NULL値を無視して非NULL値のみをカウントする",
                "NULL値の数だけをカウントする",
                "エラーが発生する"
            ],
            'answer': "NULL値を無視して非NULL値のみをカウントする",
            'explanation': "COUNT関数は、指定したカラムにNULL値が含まれている場合、そのNULL値を無視して非NULL値の数のみをカウントします。"
        },
        {
            'question': "COUNT関数は次のどのケースで役立ちますか？",
            'choices': [
                "商品の平均価格を計算する",
                "販売された商品の数を数える",
                "最も高価な商品を見つける",
                "すべての商品の名前をリストアップする"
            ],
            'answer': "販売された商品の数を数える",
            'explanation': "COUNT関数は、特定の条件を満たす行数をカウントするのに役立ちます。たとえば、販売された商品の数をカウントする場合に使用します。"
        },
        {
            'question': "次のクエリで返される結果は？ SELECT COUNT(price) FROM sales;",
            'choices': [
                "すべての行数が返される",
                "NULL値を含まないpriceカラムの行数が返される",
                "価格の合計が返される",
                "価格の平均が返される"
            ],
            'answer': "NULL値を含まないpriceカラムの行数が返される",
            'explanation': "COUNT(price)は、priceカラムにNULLでない値がある行の数をカウントします。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'COUNT'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('aggregate_count_quiz.html', error_message=error_message)


        return render_template(
            'aggregate_count_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'aggregate_count_quiz.html',
        questions=questions,
        submitted=False
    )


# SUM 学習ページ(aggregate_sum_study.html)
@app.route('/aggregation/sum/study', methods=['GET', 'POST'])
def aggregate_sum_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # salesテーブルの構造（カラム名）を取得
        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('aggregate_sum_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            sum_clauses = []
            sum_columns = request.form.getlist('sum_column')
            as_columns = request.form.getlist('as_column')
            where_clause = request.form.get('where_clause')

            # SUMを使用するクエリの作成
            for col, as_col in zip(sum_columns, as_columns):
                sum_clauses.append(f"SUM({col}) AS `{as_col}`")

            # WHERE句を使用するかどうかでクエリを分岐
            sum_query = "SELECT " + ', '.join(sum_clauses) + " FROM sales"
            if where_clause:
                sum_query += f" WHERE {where_clause}"
            sum_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # SUMクエリの結果を取得
            cursor.execute(sum_query)
            sum_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('aggregate_sum_study.html', sales_desc=sales_desc, sales_data=sales_data,
                                   sum_result=sum_result, sum_query=sum_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('aggregate_sum_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('aggregate_sum_study.html', sales_desc=sales_desc, sales_data=sales_data)

# SUM 演習ページ(aggregate_sum_advance.html)
@app.route('/aggregation/sum/practice', methods=['GET', 'POST'])
def aggregate_sum_advance():

    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'aggregate_sum_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'aggregate_sum_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# SUM 実行例
@app.route('/aggregation/sum/example', methods=['GET', 'POST'])
def aggregate_sum_example():
    return 0

# SUM クイズページ(aggregate_sum_quiz.html)
@app.route('/aggregation/sum/quiz', methods=['GET', 'POST'])
def aggregate_sum_quiz():
    questions = [
        {
            'question': "SUM関数の主な目的は何ですか？",
            'choices': [
                "数値データの平均を計算する",
                "数値データの合計を計算する",
                "行数をカウントする",
                "最小値を見つける"
            ],
            'answer': "数値データの合計を計算する",
            'explanation': "SUM関数は、指定された数値カラムの合計値を計算するために使用されます。"
        },
        {
            'question': "次のクエリの結果はどうなりますか？ SELECT SUM(price) FROM sales;",
            'choices': [
                "salesテーブルの行数が返される",
                "priceカラムの合計値が返される",
                "価格の平均値が返される",
                "エラーが発生する"
            ],
            'answer': "priceカラムの合計値が返される",
            'explanation': "SUM(price)は、salesテーブルのpriceカラムのすべての値の合計を返します。"
        },
        {
            'question': "SUM関数は次のどのケースで役立ちますか？",
            'choices': [
                "最も高価な商品を見つける",
                "販売された商品の合計金額を計算する",
                "NULL値の数をカウントする",
                "文字列を連結する"
            ],
            'answer': "販売された商品の合計金額を計算する",
            'explanation': "SUM関数は、売上の合計や合計金額を計算する場合に便利です。"
        },
        {
            'question': "次のクエリで返される結果は？ SELECT SUM(quantity) FROM sales WHERE price > 100;",
            'choices': [
                "すべての商品の数量の合計が返される",
                "価格が100より大きい商品の数量の合計が返される",
                "価格が100以下の商品の数量の合計が返される",
                "エラーが発生する"
            ],
            'answer': "価格が100より大きい商品の数量の合計が返される",
            'explanation': "SUM(quantity)は、条件に一致する商品の数量を合計します。この場合、price > 100の条件を満たす商品の数量が対象です。"
        },
        {
            'question': "次のクエリについて正しい説明はどれですか？ SELECT SUM(price) AS total_price FROM sales;",
            'choices': [
                "価格の最大値が返される",
                "価格の合計値がtotal_priceとして返される",
                "価格の最小値が返される",
                "行数が返される"
            ],
            'answer': "価格の合計値がtotal_priceとして返される",
            'explanation': "SUM(price) AS total_priceは、合計値をtotal_priceというエイリアス名で返します。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'SUM'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('aggregate_sum_quiz.html', error_message=error_message)

        return render_template(
            'aggregate_sum_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'aggregate_sum_quiz.html',
        questions=questions,
        submitted=False
    )


# AVG 学習ページ (aggregate_avg_study.html)
@app.route('/aggregation/avg/study', methods=['GET', 'POST'])
def aggregate_avg_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # salesテーブルの構造（カラム名）を取得
        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('aggregate_avg_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            avg_clauses = []
            avg_columns = request.form.getlist('avg_column')
            as_columns = request.form.getlist('as_column')
            where_clause = request.form.get('where_clause')

            # AVGを使用するクエリの作成
            for col, as_col in zip(avg_columns, as_columns):
                avg_clauses.append(f"AVG({col}) AS `{as_col}`")

            # WHERE句を使用するかどうかでクエリを分岐
            avg_query = "SELECT " + ', '.join(avg_clauses) + " FROM sales"
            if where_clause:
                avg_query += f" WHERE {where_clause}"
            avg_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # AVGクエリの結果を取得
            cursor.execute(avg_query)
            avg_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('aggregate_avg_study.html', sales_desc=sales_desc, sales_data=sales_data,
                                   avg_result=avg_result, avg_query=avg_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('aggregate_avg_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('aggregate_avg_study.html', sales_desc=sales_desc, sales_data=sales_data)

# AVG 演習ページ(aggregate_avg_advance.html)
@app.route('/aggregation/avg/practice', methods=['GET', 'POST'])
def aggregate_avg_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'aggregate_avg_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'aggregate_avg_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# AVG 実行例
@app.route('/aggregation/avg/example', methods=['GET', 'POST'])
def aggregate_avg_example():
    return 0

# AVG クイズページ(aggregate_avg_quiz.html)
@app.route('/aggregation/avg/quiz', methods=['GET', 'POST'])
def aggregate_avg_quiz():
    questions = [
        {
            'question': "AVG関数の主な目的は何ですか？",
            'choices': [
                "数値データの最大値を計算する",
                "数値データの最小値を計算する",
                "数値データの合計を計算する",
                "数値データの平均値を計算する"
            ],
            'answer': "数値データの平均値を計算する",
            'explanation': "AVG関数は、指定された数値カラムの平均値を計算するために使用されます。"
        },
        {
            'question': "次のクエリの結果はどうなりますか？ SELECT AVG(price) FROM sales;",
            'choices': [
                "salesテーブルの行数が返される",
                "priceカラムの平均値が返される",
                "価格の合計値が返される",
                "エラーが発生する"
            ],
            'answer': "priceカラムの平均値が返される",
            'explanation': "AVG(price)は、salesテーブルのpriceカラムのすべての値の平均を返します。"
        },
        {
            'question': "次のクエリで返される値はどれですか？ SELECT AVG(quantity) FROM sales WHERE category = 'Electronics';",
            'choices': [
                "すべての商品の数量の平均",
                "Electronicsカテゴリの商品数量の平均",
                "最小の数量",
                "NULL"
            ],
            'answer': "Electronicsカテゴリの商品数量の平均",
            'explanation': "このクエリは、categoryが'Electronics'である商品のquantityカラムの平均を計算します。"
        },
        {
            'question': "AVG関数を使用する際に、次のうち無視される値はどれですか？",
            'choices': [
                "負の値",
                "NULL値",
                "ゼロ",
                "すべての値が考慮される"
            ],
            'answer': "NULL値",
            'explanation': "AVG関数はNULL値を無視して計算します。"
        },
        {
            'question': "次のクエリについて正しい説明はどれですか？ SELECT AVG(price) AS avg_price FROM sales;",
            'choices': [
                "価格の最大値が返される",
                "価格の最小値が返される",
                "価格の平均値がavg_priceとして返される",
                "行数が返される"
            ],
            'answer': "価格の平均値がavg_priceとして返される",
            'explanation': "AVG(price) AS avg_priceは、平均値をavg_priceというエイリアス名で返します。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'AVG'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('aggregate_avg_quiz.html', error_message=error_message)

        return render_template(
            'aggregate_avg_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'aggregate_avg_quiz.html',
        questions=questions,
        submitted=False
    )


# MAX 学習ページ (aggregate_max_study.html)
@app.route('/aggregation/max/study', methods=['GET', 'POST'])
def aggregate_max_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # salesテーブルの構造（カラム名）を取得
        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('aggregate_max_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            max_clauses = []
            max_columns = request.form.getlist('max_column')
            as_columns = request.form.getlist('as_column')
            where_clause = request.form.get('where_clause')

            # MAXを使用するクエリの作成
            for col, as_col in zip(max_columns, as_columns):
                max_clauses.append(f"MAX({col}) AS `{as_col}`")

            # WHERE句を使用するかどうかでクエリを分岐
            max_query = "SELECT " + ', '.join(max_clauses) + " FROM sales"
            if where_clause:
                max_query += f" WHERE {where_clause}"
            max_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # MAXクエリの結果を取得
            cursor.execute(max_query)
            max_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('aggregate_max_study.html', sales_desc=sales_desc, sales_data=sales_data,
                                   max_result=max_result, max_query=max_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('aggregate_max_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('aggregate_max_study.html', sales_desc=sales_desc, sales_data=sales_data)

# MAX 演習ページ (aggregate_max_study.html)
@app.route('/aggregation/max/practice', methods=['GET', 'POST'])
def aggregate_max_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'aggregate_max_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'aggregate_max_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# MAX 実行例
@app.route('/aggregation/max/example', methods=['GET', 'POST'])
def aggregate_max_example():
    return 0

# MAX クイズページ(aggregate_max_quiz.html)
@app.route('/aggregation/max/quiz', methods=['GET', 'POST'])
def aggregate_max_quiz():
    questions = [
        {
            'question': "MAX関数の主な目的は何ですか？",
            'choices': [
                "数値データの最小値を取得する",
                "数値データの合計を取得する",
                "数値データの平均値を取得する",
                "数値データの最大値を取得する"
            ],
            'answer': "数値データの最大値を取得する",
            'explanation': "MAX関数は、指定したカラムの中で最も大きな値を返します。"
        },
        {
            'question': "次のクエリの結果はどうなりますか？ SELECT MAX(price) FROM sales;",
            'choices': [
                "salesテーブルの行数が返される",
                "priceカラムの最大値が返される",
                "価格の合計値が返される",
                "エラーが発生する"
            ],
            'answer': "priceカラムの最大値が返される",
            'explanation': "MAX(price)は、salesテーブルのpriceカラムの中で最も高い値を返します。"
        },
        {
            'question': "次のクエリで返される値はどれですか？ SELECT MAX(quantity) FROM sales WHERE category = 'Furniture';",
            'choices': [
                "すべての商品の数量の最大値",
                "Furnitureカテゴリの商品数量の最大値",
                "最小の数量",
                "NULL"
            ],
            'answer': "Furnitureカテゴリの商品数量の最大値",
            'explanation': "このクエリは、categoryが'Furniture'である商品のquantityカラムの最大値を計算します。"
        },
        {
            'question': "次のクエリについて正しい説明はどれですか？ SELECT MAX(salary) AS highest_salary FROM employees;",
            'choices': [
                "最小の給与が返される",
                "すべての従業員の平均給与が返される",
                "最高給与がhighest_salaryという名前で返される",
                "従業員の数が返される"
            ],
            'answer': "最高給与がhighest_salaryという名前で返される",
            'explanation': "MAX(salary) AS highest_salaryは、最高給与をhighest_salaryというエイリアス名で返します。"
        },
        {
            'question': "MAX関数は、次のどのタイプのデータに使用できますか？",
            'choices': [
                "数値型データのみ",
                "文字列型データのみ",
                "数値型と文字列型の両方",
                "日付型データのみ"
            ],
            'answer': "数値型と文字列型の両方",
            'explanation': "MAX関数は、数値型データと文字列型データの両方に使用できます。文字列の場合、辞書順で最大の値が返されます。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'MAX'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('aggregate_max_quiz.html', error_message=error_message)

        return render_template(
            'aggregate_max_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'aggregate_max_quiz.html',
        questions=questions,
        submitted=False
    )

# MIN 学習ページ (aggregate_min_study.html)
@app.route('/aggregation/min/study', methods=['GET', 'POST'])
def aggregate_min_study():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # salesテーブルの構造（カラム名）を取得
        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('aggregate_min_study.html', error_message=error_message)

    # POSTリクエストの処理
    if request.method == 'POST':
        try:
            min_clauses = []
            min_columns = request.form.getlist('min_column')
            as_columns = request.form.getlist('as_column')
            where_clause = request.form.get('where_clause')

            # MINを使用するクエリの作成
            for col, as_col in zip(min_columns, as_columns):
                min_clauses.append(f"MIN({col}) AS `{as_col}`")

            # WHERE句を使用するかどうかでクエリを分岐
            min_query = "SELECT " + ', '.join(min_clauses) + " FROM sales"
            if where_clause:
                min_query += f" WHERE {where_clause}"
            min_query += ";"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            # MINクエリの結果を取得
            cursor.execute(min_query)
            min_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('aggregate_min_study.html', sales_desc=sales_desc, sales_data=sales_data,
                                   min_result=min_result, min_query=min_query)

        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('aggregate_min_study.html', error_message=error_message)

    # GETリクエスト時の処理
    return render_template('aggregate_min_study.html', sales_desc=sales_desc, sales_data=sales_data)

# MIN 演習ページ (aggregate_min_advance.html)
@app.route('/aggregation/min/practice', methods=['GET', 'POST'])
def aggregate_min_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'aggregate_min_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'aggregate_min_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# MIN 実行例
@app.route('/aggregation/min/example', methods=['GET', 'POST'])
def aggregate_min_example():
    return 0

# MIN クイズページ(aggregate_min_quiz.html)
@app.route('/aggregation/min/quiz', methods=['GET', 'POST'])
def aggregate_min_quiz():
    questions = [
        {
            'question': "MIN関数の主な目的は何ですか？",
            'choices': [
                "指定したカラムの最大値を取得する",
                "指定したカラムの合計を取得する",
                "指定したカラムの最小値を取得する",
                "指定したカラムのデータ型を変更する"
            ],
            'answer': "指定したカラムの最小値を取得する",
            'explanation': "MIN関数は、指定したカラムの中で最も小さな値を返します。"
        },
        {
            'question': "次のクエリの結果は何ですか？ SELECT MIN(price) FROM products;",
            'choices': [
                "productsテーブルのすべての価格の合計",
                "productsテーブルの最も安い価格",
                "productsテーブルの行数",
                "エラーが発生する"
            ],
            'answer': "productsテーブルの最も安い価格",
            'explanation': "MIN(price)は、productsテーブルのpriceカラムの中で最も小さい値を返します。"
        },
        {
            'question': "次のクエリで返される値はどれですか？ SELECT MIN(sale_date) FROM sales;",
            'choices': [
                "最新の日付",
                "最古の日付",
                "すべての日付の合計",
                "エラーが発生する"
            ],
            'answer': "最古の日付",
            'explanation': "MIN関数は、日付データに対しても最小値を計算でき、最も古い日付を返します。"
        },
        {
            'question': "次のクエリについて正しい説明はどれですか？ SELECT MIN(age) AS youngest FROM employees;",
            'choices': [
                "最小の年齢がyoungestという名前で返される",
                "最小の給与が返される",
                "最も古い従業員の名前が返される",
                "エラーが発生する"
            ],
            'answer': "最小の年齢がyoungestという名前で返される",
            'explanation': "MIN(age) AS youngestは、最小の年齢をyoungestというエイリアス名で返します。"
        },
        {
            'question': "MIN関数は、次のどのタイプのデータに使用できますか？",
            'choices': [
                "数値型データのみ",
                "文字列型データのみ",
                "数値型と文字列型の両方",
                "日付型データのみ"
            ],
            'answer': "数値型と文字列型の両方",
            'explanation': "MIN関数は、数値型データ、文字列型データ、日付型データに使用できます。文字列の場合、辞書順で最小の値が返されます。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'MIN'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('aggregate_min_quiz.html', error_message=error_message)

        return render_template(
            'aggregate_min_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'aggregate_min_quiz.html',
        questions=questions,
        submitted=False
    )


#以下はソートとグループ化!
@app.route('/organize_select', methods=['GET', 'POST'])
def organize_select():
    return render_template('organize_select.html')

# GROUP BY句 学習ページ(organize_groupby.html)
@app.route('/aggregation/group-by/study', methods=['GET', 'POST'])
def organize_groupby():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_groupby.html', error_message=error_message)

    if request.method == 'POST':
        try:
            select_columns = request.form.getlist('columns[]')  # カラムの取得
            aggregate_function = request.form.getlist('aggregate_function[]')  # 集約関数の取得
            aggregate_column = request.form.getlist('aggregate_column[]')  # 集約対象のカラムの取得
            as_name = request.form.getlist('as_column[]')  # エイリアスの取得
            group_column = request.form['group_column']  # GROUP BYのカラムの取得
            where_condition = request.form.get('where_condition')  # WHERE条件の取得

            # SELECT句の作成
            select_clauses = select_columns  # 追加されたカラム
            for func, col, alias in zip(aggregate_function, aggregate_column, as_name):
                select_clauses.append(f"{func}({col}) AS `{alias}`")

            # WHERE条件があれば追加
            where_clause = f" WHERE {where_condition}" if where_condition else ""
            
            # GROUP BY句のSQL文の作成
            groupby_query = f"SELECT {', '.join(select_clauses)} FROM sales{where_clause} GROUP BY {group_column};"

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(groupby_query)
            groupby_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('organize_groupby.html', sales_desc=sales_desc, sales_data=sales_data,
                                groupby_result=groupby_result, groupby_query=groupby_query)
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('organize_groupby.html', error_message=error_message)

    return render_template('organize_groupby.html', sales_desc=sales_desc, sales_data=sales_data)

# GROUP BY句 実行例のページ(organize_groupby_example.html)
@app.route('/aggregation/group-by/example', methods=['GET'])
def organize_groupby_example():
    try:
        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # GROUP BYクエリの実行
        groupby_query = """
        SELECT category, COUNT(*) AS total_items, SUM(quantity) AS total_quantity
        FROM sales
        GROUP BY category;
        """
        cursor.execute(groupby_query)
        groupby_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_groupby_example.html', error_message=error_message)

    return render_template('organize_groupby_example.html', sales_data=sales_data, groupby_result=groupby_result)

# GROUP BY句 演習のページ(organize_groupby_advance.html)
@app.route('/aggregation/group-by/practice', methods=['GET', 'POST'])
def organize_groupby_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'organize_groupby_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'organize_groupby_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )


# GROUP BY句 クイズページ(organize_groupby_quiz.html)
@app.route('/aggregation/group-by/quiz', methods=['GET', 'POST'])
def organize_groupby_quiz():
    questions = [
        {
            'question': "GROUP BY句を使用して、どのような集計を行うことができますか？",
            'choices': [
                "合計値、平均値、最大値、最小値などの集計",
                "特定の列をソートする",
                "重複した行を削除する",
                "すべての行を結合する"
            ],
            'answer': "合計値、平均値、最大値、最小値などの集計",
            'explanation': "GROUP BY句を使用すると、集計関数（SUM、AVG、MAX、MINなど）と組み合わせてデータを集計できます。"
        },
        {
            'question': "次のSQL文でGROUP BY句を使用する主な理由は何ですか？",
            'choices': [
                "レコードの順番を指定するため",
                "データを集約してグループ化するため",
                "NULL値を含むレコードを除外するため",
                "テーブルを結合するため"
            ],
            'answer': "データを集約してグループ化するため",
            'explanation': "GROUP BY句を使用すると、データを特定の列ごとにグループ化し、集計関数を適用できます。"
        },
        {
            'question': "GROUP BYを使用する際に、集約関数で使用できるものはどれですか？",
            'choices': [
                "SUM",
                "COUNT",
                "AVG",
                "すべての選択肢"
            ],
            'answer': "すべての選択肢",
            'explanation': "GROUP BYを使用すると、SUM、COUNT、AVGなどの集約関数を使ってデータを集計できます。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT category, COUNT(DISTINCT product_name) FROM sales GROUP BY category;",
            'choices': [
                "カテゴリーごとのユニークな商品の数を表示する",
                "カテゴリーごとの商品の合計数を表示する",
                "カテゴリーごとの平均価格を表示する"
            ],
            'answer': "カテゴリーごとのユニークな商品の数を表示する",
            'explanation': "DISTINCTを使用することで、カテゴリーごとに重複を排除したユニークな商品の数を表示します。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT category, AVG(price) FROM sales GROUP BY category;",
            'choices': [
                "カテゴリーごとの商品の平均価格を表示する",
                "カテゴリーごとの商品の合計数を表示する",
                "すべての商品の合計価格を表示する"
            ],
            'answer': "カテゴリーごとの商品の平均価格を表示する",
            'explanation': "AVG関数は、各カテゴリーごとの商品の平均価格を計算して表示します。"
        },
        {
            'question': "次のSQL文の結果は何ですか？\nSELECT category, MAX(price) FROM sales GROUP BY category;",
            'choices': [
                "カテゴリーごとの最小価格を表示する",
                "カテゴリーごとの平均価格を表示する",
                "カテゴリーごとの最大価格を表示する"
            ],
            'answer': "カテゴリーごとの最大価格を表示する",
            'explanation': "MAX関数を使用すると、カテゴリーごとの最大価格が表示されます。"
        },
        {
            'question': "以下のSQLクエリの結果を予測してください: SELECT category, COUNT(*) FROM sales GROUP BY category;",
            'choices': [
                "カテゴリーごとの商品の数を表示する",
                "すべての商品の合計数を表示する",
                "カテゴリーごとの平均価格を表示する"
            ],
            'answer': "カテゴリーごとの商品の数を表示する",
            'explanation': "COUNT(*)関数は、カテゴリーごとの商品の数をカウントして表示します。"
        },
        {
            'question': "GROUP BY句を正しく使用したクエリはどれですか？",
            'choices': [
                "SELECT category, AVG(price) FROM sales GROUP BY price;",
                "SELECT category, COUNT(*) FROM sales GROUP BY COUNT(*);",
                "SELECT category, MAX(price) FROM sales GROUP BY category;"
            ],
            'answer': "SELECT category, MAX(price) FROM sales GROUP BY category;",
            'explanation': "GROUP BY句を使用する際は、集計関数を適切に使用して、指定した列でデータをグループ化する必要があります。"
        },
        {
            'question': "GROUP BYを使用して集計する際に、COUNT関数で得られる値は何を表しますか？",
            'choices': [
                "グループ内のデータの合計値",
                "グループ内の行数",
                "グループ内のデータの平均値"
            ],
            'answer': "グループ内の行数",
            'explanation': "COUNT関数は、グループ内の行数をカウントして、その数を返します。"
        },
        {
            'question': "SELECT product_name, price, SUM(quantity) FROM sales GROUP BY product_name;のエラーの原因は？",
            'choices': [
                "price列がGROUP BYまたは集約関数に含まれていない",
                "SUM関数はGROUP BYと一緒に使えない",
                "salesテーブルにproduct_name列が存在しない"
            ],
            'answer': "price列がGROUP BYまたは集約関数に含まれていない",
            'explanation': "GROUP BYを使用する場合、集約されない列（ここではprice）もGROUP BY句または集約関数に含める必要があります。"
        }
    ]


    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'GROUP BY'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('organize_groupby_quiz.html', error_message=error_message)


        return render_template(
            'organize_groupby_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'organize_groupby_quiz.html',
        questions=questions,
        submitted=False
    )


# HAVING句 学習ページ(organize_having.html)
@app.route('/aggregation/having/study', methods=['GET', 'POST'])
def organize_having():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_having.html', error_message=error_message)

    if request.method == 'POST':
        try:
            select_columns = request.form.getlist('columns[]')
            aggregate_function = request.form.getlist('aggregate_function[]')
            aggregate_column = request.form.getlist('aggregate_column[]')
            as_name = request.form.getlist('as_column[]')
            group_column = request.form['group_column']
            having_condition = request.form.get('having_condition')

            select_clauses = select_columns
            for func, col, alias in zip(aggregate_function, aggregate_column, as_name):
                select_clauses.append(f"{func}({col}) AS `{alias}`")

            having_clause = f" HAVING {having_condition}" if having_condition else ""
            
            having_query = f"SELECT {', '.join(select_clauses)} FROM sales GROUP BY {group_column}{having_clause};"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(having_query)
            having_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('organize_having.html', sales_desc=sales_desc, sales_data=sales_data,
                                   having_result=having_result, having_query=having_query)
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('organize_having.html', error_message=error_message)

    return render_template('organize_having.html', sales_desc=sales_desc, sales_data=sales_data)

# HAVING句 実行例ページ(organize_having_example.html)
@app.route('/aggregation/having/example', methods=['GET'])
def organize_having_example():
    try:
        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # HAVING句を含むクエリの実行
        having_query = """
        SELECT category, COUNT(*) AS total_items, SUM(quantity) AS total_quantity
        FROM sales
        GROUP BY category
        HAVING SUM(quantity) > 50;
        """
        cursor.execute(having_query)
        having_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_having_example.html', error_message=error_message)

    return render_template('organize_having_example.html', sales_data=sales_data, having_result=having_result)

# HAVING句 演習ページ(organize_having_advance.html)
@app.route('/aggregation/having/practice', methods=['GET', 'POST'])
def organize_having_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'organize_having_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'organize_having_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# HAVING句 クイズページ(organize_having_quiz.html)
@app.route('/aggregation/having/quiz', methods=['GET', 'POST'])
def organize_having_quiz():
    questions = [
        {
            'question': "HAVING句とは何ですか？",
            'choices': [
                "GROUP BYでグループ化されたデータに対して条件を設定するための句",
                "WHERE句と同様に行単位で条件を設定するための句",
                "データベースからデータを削除するための句",
                "テーブルの作成や変更を行うための句"
            ],
            'answer': "GROUP BYでグループ化されたデータに対して条件を設定するための句",
            'explanation': "HAVING句はGROUP BY句と組み合わせて使用され、グループ化された結果に対して条件を設定するために使用されます。WHERE句とは異なり、行単位ではなくグループ単位でフィルタリングを行います。"
        },
        {
            'question': "以下のSQLクエリの結果を予測してください: SELECT category, SUM(quantity) FROM sales GROUP BY category HAVING SUM(quantity) >= 100;",
            'choices': [
                "各カテゴリーの合計数量が100以上の行を表示する",
                "各カテゴリーの合計数量が100以下の行を表示する",
                "エラーが発生する"
            ],
            'answer': "各カテゴリーの合計数量が100以上の行を表示する",
            'explanation': "HAVING句はグループ化されたデータに対して条件を設定します。このクエリは、各カテゴリーの合計数量が100以上の行のみを表示します。"
        },
        {
            'question': "HAVING句を正しく使用したクエリはどれですか？",
            'choices': [
                "SELECT category FROM sales HAVING SUM(price) > 500;",
                "SELECT category, SUM(price) FROM sales GROUP BY category HAVING SUM(price) > 500;",
                "SELECT category, SUM(price) FROM sales WHERE SUM(price) > 500;"
            ],
            'answer': "SELECT category, SUM(price) FROM sales GROUP BY category HAVING SUM(price) > 500;",
            'explanation': "HAVING句はGROUP BYでグループ化された結果に対して条件を設定するため、正しいクエリはGROUP BY句とHAVING句を併用しています。"
        },
        {
            'question': "HAVING句とWHERE句の主な違いは何ですか？",
            'choices': [
                "HAVING句はグループ化されたデータに適用される",
                "HAVING句はグループ化前のデータに適用される",
                "HAVING句では条件を設定できない"
            ],
            'answer': "HAVING句はグループ化されたデータに適用される",
            'explanation': "WHERE句は行単位でデータをフィルタリングしますが、HAVING句はGROUP BY句でグループ化されたデータに対して条件を設定します。"
        },
        {
            'question': "以下のSQLでエラーが発生する原因は？ SELECT category, SUM(quantity) AS total FROM sales GROUP BY category HAVING total > 50;",
            'choices': [
                "HAVING句で集計関数の結果を使用している",
                "カラムのエイリアスをHAVING句で使用している",
                "GROUP BY句で正しくグループ化されていない"
            ],
            'answer': "カラムのエイリアスをHAVING句で使用している",
            'explanation': "HAVING句ではエイリアスを直接使用することができません。集計関数やその結果を条件として使う必要があります。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT category, COUNT(*) FROM sales GROUP BY category HAVING COUNT(*) > 5;",
            'choices': [
                "カテゴリーごとのレコード数が5以上のカテゴリーを表示する",
                "カテゴリーごとのレコード数が5以下のカテゴリーを表示する",
                "エラーが発生する"
            ],
            'answer': "カテゴリーごとのレコード数が5以上のカテゴリーを表示する",
            'explanation': "HAVING句により、カテゴリーごとのレコード数が5以上のカテゴリーのみを表示します。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT category, SUM(price) FROM sales GROUP BY category HAVING SUM(price) < 1000;",
            'choices': [
                "カテゴリーごとの合計価格が1000未満のカテゴリーを表示する",
                "カテゴリーごとの合計価格が1000以上のカテゴリーを表示する",
                "エラーが発生する"
            ],
            'answer': "カテゴリーごとの合計価格が1000未満のカテゴリーを表示する",
            'explanation': "HAVING句はグループ化されたデータに対して条件を設定するため、合計価格が1000未満のカテゴリーを表示します。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT category, AVG(price) FROM sales GROUP BY category HAVING AVG(price) BETWEEN 200 AND 400;",
            'choices': [
                "カテゴリーごとの平均価格が200から400の範囲のカテゴリーを表示する",
                "カテゴリーごとの平均価格が400以上のカテゴリーを表示する",
                "カテゴリーごとの平均価格が200未満のカテゴリーを表示する"
            ],
            'answer': "カテゴリーごとの平均価格が200から400の範囲のカテゴリーを表示する",
            'explanation': "HAVING句で条件を設定することで、カテゴリーごとの平均価格が200から400の範囲にあるカテゴリーのみを表示します。"
        },
        {
            'question': "次のSQLクエリにおけるHAVING句の役割は何ですか？ SELECT product_name, SUM(quantity) FROM sales GROUP BY product_name HAVING SUM(quantity) > 50;",
            'choices': [
                "製品ごとの販売数量が50以上の製品を表示する",
                "製品ごとの販売数量が50以下の製品を表示する",
                "製品ごとの販売数量が50を超えたデータを削除する"
            ],
            'answer': "製品ごとの販売数量が50以上の製品を表示する",
            'explanation': "HAVING句はグループ化されたデータに条件を設定するため、販売数量が50以上の製品をフィルタリングします。"
        },
        {
            'question': "次のSQLクエリにおけるエラーの原因は何ですか？ SELECT category, COUNT(*) FROM sales GROUP BY category HAVING COUNT(*) = 0;",
            'choices': [
                "COUNT関数はHAVING句で使用できない",
                "COUNT(*)でゼロの結果は存在しない",
                "GROUP BY句の結果がゼロでない場合、HAVING句は機能しない"
            ],
            'answer': "COUNT(*)でゼロの結果は存在しない",
            'explanation': "COUNT(*)はグループ化されたデータの行数をカウントしますが、ゼロの結果が存在しないため、HAVING句で0を指定することは意味がありません。"
        }
    ]


    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'HAVING'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('organize_having_quiz.html', error_message=error_message)

        return render_template(
            'organize_having_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'organize_having_quiz.html',
        questions=questions,
        submitted=False
    )


# ORDER BY句 学習ページ(organize_orderby.html)
@app.route('/aggregation/order-by/study', methods=['GET', 'POST'])
def organize_orderby():
    try:
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_orderby.html', error_message=error_message)

    if request.method == 'POST':
        try:
            select_columns = request.form.getlist('columns[]')
            order_columns = request.form.getlist('order_columns[]')
            order_directions = request.form.getlist('order_directions[]')

            select_clauses = ", ".join(select_columns)
            order_by_clauses = ", ".join([f"{col} {dir}" for col, dir in zip(order_columns, order_directions)])

            order_query = f"SELECT {select_clauses} FROM sales ORDER BY {order_by_clauses};"

            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(order_query)
            order_result = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('organize_orderby.html', sales_desc=sales_desc, sales_data=sales_data,
                                   order_result=order_result, order_query=order_query)
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            return render_template('organize_orderby.html', error_message=error_message)

    return render_template('organize_orderby.html', sales_desc=sales_desc, sales_data=sales_data)

# ORDER BY句 実行例ページ(organize_orderby_example.html)
@app.route('/aggregation/order-by/example', methods=['GET'])
def organize_orderby_example():
    try:
        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの中身を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        # ORDER BYクエリの実行
        orderby_query = """
        SELECT product_name, category, quantity, price
        FROM sales
        ORDER BY price DESC, quantity ASC;
        """
        cursor.execute(orderby_query)
        orderby_result = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('organize_orderby_example.html', error_message=error_message)

    return render_template('organize_orderby_example.html', sales_data=sales_data, orderby_result=orderby_result)


# ORDER BY句 演習ページ(organize_orderby_advance.html)
@app.route('/aggregation/order-by/practice', methods=['GET', 'POST'])
def organize_orderby_advance():
    query = None
    query_result = None
    error_message = None

    try:
        # salesテーブルのデータを取得
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # salesテーブルの内容を取得
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()

        cursor.execute("DESC sales")
        sales_desc = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template(
            'organize_orderby_advance.html',
            query=query,
            query_result=query_result,
            error_message=error_message,
            sales_data=[],
            sales_desc=[]
        )

    if request.method == 'POST':
        try:
            # ユーザーからのクエリを取得
            query = request.form['query']

            # クエリの検証（ホワイトリストとセミコロンのチェック）
            allowed_statements = ['SELECT']
            if not query.upper().startswith(tuple(allowed_statements)):
                raise ValueError("許可されていないSQL文です。SELECT文のみ使用可能です。")

            # セミコロンの数を検証（クエリの最後に1つのみ許可）
            if query.count(';') != 1 or not query.endswith(';'):
                raise ValueError("クエリには必ず1つだけセミコロンを含め、最後に配置してください。複数のクエリは実行できません。")

            # データベースに接続してクエリを実行
            conn = mysql.connector.MySQLConnection(**this_users_dns)
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            query_result = {"columns": columns, "data": result}

            cursor.close()
            conn.close()
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"

    return render_template(
        'organize_orderby_advance.html',
        query=query,
        query_result=query_result,
        error_message=error_message,
        sales_data=sales_data,
        sales_desc=sales_desc
    )

# ORDER BY句 クイズページ(organize_orderby_quiz.html)
@app.route('/aggregation/order-by/quiz', methods=['GET', 'POST'])
def organize_orderby_quiz():
    questions = [
        {
            'question': "以下のSQLクエリの結果を予測してください: SELECT product_name, price FROM sales ORDER BY price ASC;",
            'choices': [
                "価格の高い順に商品を並べる",
                "価格の低い順に商品を並べる",
                "商品の名前順に並べる"
            ],
            'answer': "価格の低い順に商品を並べる",
            'explanation': "ORDER BY price ASCは、価格を昇順（低い順）で並べることを意味します。"
        },
        {
            'question': "以下のクエリを実行した結果、どのように並べ替えられますか？ SELECT category, sale_date FROM sales ORDER BY sale_date DESC;",
            'choices': [
                "販売日が新しい順に並べる",
                "販売日が古い順に並べる",
                "カテゴリーごとに並べる"
            ],
            'answer': "販売日が新しい順に並べる",
            'explanation': "ORDER BY sale_date DESCは、販売日を降順（新しい順）で並べることを意味します。"
        },
        {
            'question': "次のクエリの結果を予測してください: SELECT category, price FROM sales ORDER BY category ASC, price DESC;",
            'choices': [
                "カテゴリーごとに昇順、価格は各カテゴリー内で降順に並べる",
                "価格を昇順、カテゴリーを降順に並べる",
                "カテゴリーと価格の両方を昇順に並べる"
            ],
            'answer': "カテゴリーごとに昇順、価格は各カテゴリー内で降順に並べる",
            'explanation': "ORDER BY句で複数のカラムを指定する場合、最初のカラムでグループ化し、次のカラムでそのグループ内の並び替えを行います。"
        },
        {
            'question': "`ORDER BY`句で複数のカラムを指定する場合、どのような順序で並び替えが実行されますか？",
            'choices': [
                "最初のカラムを並べ替え、次に2つ目のカラムで並び替える",
                "すべてのカラムを同時に並べ替える",
                "昇順のみで並び替えが行われる",
                "並び替えはクエリの実行順序に依存する"
            ],
            'answer': "最初のカラムを並べ替え、次に2つ目のカラムで並び替える",
            'explanation': "ORDER BY句で複数のカラムを指定すると、最初のカラムで並び替えを行い、その後、同じ値を持つ行について2つ目のカラムで並び替えを行います。"
        },
        {
            'question': "次のSQLクエリを実行した場合、NULL値はどのように並べ替えられますか？ SELECT product_name, category FROM sales ORDER BY category DESC;",
            'choices': [
                "NULL値は最後に配置される",
                "NULL値は最初に配置される",
                "NULL値は並び替えに影響しない",
                "NULL値はランダムな位置に配置される"
            ],
            'answer': "NULL値は最初に配置される",
            'explanation': "ORDER BY DESCを指定した場合、NULL値は最初に配置されます。SQLでは、NULL値は「値がない」と解釈されるため、昇順では最後、降順では最初に配置されます。"
        },
        {
            'question': "次のSQLクエリを実行した場合、NULL値はどのように並べ替えられますか？ SELECT product_name, category FROM sales ORDER BY category ASC;",
            'choices': [
                "NULL値は最後に配置される",
                "NULL値は最初に配置される",
                "NULL値は並び替えに影響しない",
                "NULL値はランダムな位置に配置される"
            ],
            'answer': "NULL値は最後に配置される",
            'explanation': "ORDER BY ASCでは、NULL値は「値がない」と解釈され、昇順（ASC）で並べる際、NULLは最後に配置されます。"
        },
        {
            'question': "次のSQLクエリを実行した場合、どのように並べ替えられますか？ SELECT product_name, price FROM sales ORDER BY price DESC;",
            'choices': [
                "価格の高い順に並べる",
                "価格の低い順に並べる",
                "商品の名前順に並べる"
            ],
            'answer': "価格の高い順に並べる",
            'explanation': "ORDER BY price DESCは、価格を降順（高い順）で並べることを意味します。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT product_name, sale_date FROM sales ORDER BY sale_date ASC;",
            'choices': [
                "販売日が新しい順に並べる",
                "販売日が古い順に並べる",
                "価格が高い順に並べる"
            ],
            'answer': "販売日が古い順に並べる",
            'explanation': "ORDER BY sale_date ASCは、販売日を昇順（古い順）で並べることを意味します。"
        },
        {
            'question': "ORDER BY句で指定した複数のカラムに異なる並べ替え順序を使用した場合、どのように動作しますか？",
            'choices': [
                "最初に指定されたカラムで並べ替え、その後、2番目のカラムで並べ替えを行う",
                "すべてのカラムは昇順または降順に並べ替えられる",
                "ORDER BY句は複数のカラムで並べ替えを行わない"
            ],
            'answer': "最初に指定されたカラムで並べ替え、その後、2番目のカラムで並べ替えを行う",
            'explanation': "ORDER BY句で複数のカラムを指定する際、最初のカラムで並べ替え、その後同じ値を持つ行について、2番目のカラムで並べ替えを行います。"
        },
        {
            'question': "次のSQLクエリの結果を予測してください: SELECT product_name, price FROM sales ORDER BY price ASC LIMIT 5;",
            'choices': [
                "価格の低い順に上位5件の製品を表示する",
                "価格の高い順に上位5件の製品を表示する",
                "すべての商品を表示する"
            ],
            'answer': "価格の低い順に上位5件の製品を表示する",
            'explanation': "ORDER BY price ASCで価格を昇順に並べ、LIMIT 5でその中から上位5件を表示します。"
        }
    ]

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = 0

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(f'answer_{idx}', '')
            if user_answer == question['answer']:
                score += 1

        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor()

        # クイズIDを設定（クイズ名に基づいてIDを取得）
        quiz_name = 'ORDER BY'
        cursor.execute("SELECT id FROM quiz_list WHERE quiz_name = %s", (quiz_name,))
        result = cursor.fetchone()

        if result:
            quiz_id = result[0]  # クイズ名に基づいてIDを取得

            # 進捗状況の更新または挿入
            cursor.execute(""" 
                INSERT INTO progress (quiz_id, score)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE score = VALUES(score)
            """, (quiz_id, score))

            conn.commit()
            cursor.close()
            conn.close()
        else:
            # クイズ名に該当するIDが見つからない場合の処理
            error_message = "指定されたクイズが見つかりません"
            return render_template('organize_orderby_quiz.html', error_message=error_message)

        return render_template(
            'organize_orderby_quiz.html',
            questions=questions,
            submitted=True,
            score=score,
            total=len(questions),
            user_answers=user_answers
        )

    return render_template(
        'organize_orderby_quiz.html',
        questions=questions,
        submitted=False
    )


# クイズ進捗ページ(quiz_progress.html)
@app.route('/quiz_progress', methods=['GET'])
def quiz_progress():
    try:
        # データベース接続
        conn = mysql.connector.MySQLConnection(**this_users_dns)
        cursor = conn.cursor(dictionary=True)

        # 全クイズのリストを取得
        cursor.execute("SELECT id, quiz_name, total_questions FROM quiz_list")
        quiz_list = cursor.fetchall()

        # 各クイズの進捗状況を取得
        cursor.execute("SELECT quiz_id, score, completed_at FROM progress")
        progress_data = cursor.fetchall()

        # クイズIDをキーに辞書を作成
        progress_dict = {item['quiz_id']: item for item in progress_data} if progress_data else {}

        # クイズIDに対応するファイル名をマッピング
        quiz_files = {
            1: "basic/join/cross_join/quiz",
            2: "basic/join/inner_join/quiz",
            3: "basic/join/left_outer_join/quiz",
            4: "basic/join/right_outer_join/quiz",
            5: "basic/join/join_quiz",
            6: "basic/update/quiz",
            7: "aggregation/count/quiz",
            8: "aggregation/sum/quiz",
            9: "aggregation/avg/quiz",
            10: "aggregation/max/quiz",
            11: "aggregation/min/quiz",
            12: "aggregation/group-by/quiz",
            13: "aggregation/having/quiz",
            14: "aggregation/order-by/quiz",
            15: "quiz/insert",
            16: "quiz/insert_select",
            17: "quiz/delete_single",
            18: "quiz/delete_multiple"
        }

        # 完了したクイズの数を計算
        completed_quizzes = sum(1 for quiz in quiz_list if quiz['id'] in progress_dict)
        total_quizzes = len(quiz_list)

        # 全体の進捗率を計算
        progress_rate = 0 if total_quizzes == 0 else round((completed_quizzes / total_quizzes) * 100, 2)

        cursor.close()
        conn.close()

    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return render_template('quiz_progress.html', error_message=error_message)

    return render_template(
        'quiz_progress.html',
        progress_rate=progress_rate,
        quiz_list=quiz_list,
        progress_dict=progress_dict,
        quiz_files=quiz_files
    )



#-------------------------------------------------------------------------#
#
# ここまで！！！！！！！！！！！！！
#
#-------------------------------------------------------------------------#




#おまじない
if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=app.config['DEBUG'])


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

def calculate_progress_rate(cursor):
    conn = mysql.connector.MySQLConnection(**this_users_dns)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS total_quizzes FROM quiz_list")
    total_quizzes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS completed_quizzes FROM progress WHERE score > 0")
    completed_quizzes = cursor.fetchone()[0]

    return int((completed_quizzes / total_quizzes) * 100)

def run_query(sql, commit=False):

    conn = mysql.connector.connect(**this_users_dns)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        if commit:
            conn.commit()
        return cursor.fetchall() if cursor.with_rows else None
    finally:
        cursor.close()
        conn.close()

#カウント
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)
