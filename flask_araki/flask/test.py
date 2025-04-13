data = [('id', 'int(11)', 'NO', 'PRI', None, ''), ('name', 'char(32)', 'YES', '', None, '')]

# HTMLテーブルを作成
table_headers = [column[0] for column in data]
table_data = [(column[1],) for column in data]
print(table_headers)
print(table_data)