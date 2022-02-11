import codecs
import psycopg2
import sqlite3

# def insert_execute(con, sql):
#     with con.cursor() as cur:
#         cur.execute(sql, (231,'A'))
        
#     con.commit()

# if __name__ == '__main__':
#     con = psycopg2.connect("host=" + "localhost" +
#                            " port=" + "5432" +
#                            " dbname=" + "test_database" +
#                            " user=" + "workuser" +
#                            " password=" + "taka1114")

#     sql =  """insert into test_table(id, name) values(%s, %s)"""

#     # データ登録
#     insert_execute(con, sql)

#     con.close()

with codecs.open(r'Z:\UserProfile\s20192087\Desktop\Tem\Graaaasses.VSCode\review_weight3.txt', 'r', 'UTF-8') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            columns = line.split(',')
            data.append((columns[0],float(columns[1])))
        
        con = sqlite3.connect('kekka.db')
        cur=con.cursor()
        sql1 = 'CREATE TABLE IF NOT EXISTS chair_weight (name TEXT, weight REAL)'
        cur.execute(sql1)
        # sql1 = 'DROP TABLE chair_weight'
        # con.execute(sql1)

        sql2 = 'INSERT INTO chair_weight (name, weight) VALUES (?,?)'
        cur.executemany(sql2,data)     #sql文を実行
        con.commit()
        con.close()          #データベースを閉じる
