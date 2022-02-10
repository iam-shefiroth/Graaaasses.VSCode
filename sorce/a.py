import codecs
import psycopg2

def insert_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql, (231,'A'))
        
    con.commit()

if __name__ == '__main__':
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5432" +
                           " dbname=" + "test_database" +
                           " user=" + "workuser" +
                           " password=" + "taka1114")

    sql =  """insert into test_table(id, name) values(%s, %s)"""

    # データ登録
    insert_execute(con, sql)

    con.close()
