import codecs
import sqlite3
with codecs.open(r'Z:\UserProfile\s20192087\Desktop\Tem\Graaaasses.VSCode\review_weight1.txt', 'r', 'UTF-8') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            columns = line.split(',')
            data.append((columns[0],float(columns[1])))
        
        con = sqlite3.connect('kekka.db')
        cur=con.cursor()
        sql1 = 'CREATE TABLE IF NOT EXISTS gamesoft_weight (name TEXT, weight REAL)'
        cur.execute(sql1)
        # sql1 = 'DROP TABLE gamesoft_weight'
        # con.execute(sql1)

        sql2 = 'INSERT INTO gamesoft_weight (name, weight) VALUES (?,?)'
        cur.executemany(sql2,data)     #sql文を実行
        con.commit()
        con.close()          #データベースを閉じる