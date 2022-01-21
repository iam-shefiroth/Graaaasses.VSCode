# import sqlite3

# # TEST.dbを作成する
# # すでに存在していれば、それにアスセスする。
# dbname = 'TEST.db'
# conn = sqlite3.connect(dbname)

# # データベースへのコネクションを閉じる。(必須)
# conn.close()
import sqlite3

dbname = 'TEST.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING)')

# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()