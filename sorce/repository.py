from distutils.log import error
import sqlite3
import resultData
import re

testurl = "https://www.amazon.co.jp/%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4%E3%83%8A%E3%83%A0%E3%82%B3%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%86%E3%82%A4%E3%83%B3%E3%83%A1%E3%83%B3%E3%83%88-%E3%80%90PS4%E3%80%91%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%AA%E3%83%83%E3%83%88%E3%82%B7%E3%83%BC%E3%82%BA%E3%83%B3%E3%80%90%E6%97%A9%E6%9C%9F%E8%B3%BC%E5%85%A5%E7%89%B9%E5%85%B8%E3%80%91%E8%A1%A3%E8%A3%85DLC%E3%80%8E%E6%9A%81%E3%81%AE%E3%82%86%E3%81%8B%E3%81%9F%E3%80%8F%E3%81%8C%E5%85%A5%E6%89%8B%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E3%82%B3%E3%83%BC%E3%83%89-%E5%B0%81%E5%85%A5/dp/B08W5S54P1/ref=sr_1_7?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&keywords=%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC&qid=1639620405&sr=8-7"
testtitle = ""
testimg = ""
testposititle = ["1","2","3"]
testpositive = ["よし","うん","おけ"]
testnegatitle = ["-1","-2","-3"]
testnegative = ["くそ","だめ","cyka"]
testtotalcnt = 100
testposicnt = 65
testnegacnt = 35
testposiratio = round((testposicnt / testtotalcnt) * 100,1)
testnegaratio = round(100 - testposiratio,1)


# 入力されたurlと格納されているdb内のurlを比較する
def selectdb(url):
    db = sqlite3.connect("kekka.db")
    temurl = ''
    
    url_a = re.search('[^0-9A-Z]([0-9A-Z]{10})([^0-9A-Z]|$)', url).group().replace("/","")
    print(url_a)
    sql = 'SELECT asin_code FROM kekka WHERE asin_code = ?'
    cur = db.execute(sql,(url_a,))
    data = cur.fetchall()
    print(data)
    print(1)
    # sql実行結果の件数が0件ではないか確認
    if len(data) != 0:
        temurl = ''.join(data[0])
        print(temurl)
        print(2)
    db.close()
    
    # 入力されたurlとsql検索結果のurlが一致したかどうか確認
    if (url_a == temurl):
        db = sqlite3.connect("kekka.db")
        # 入力されたurlの全情報をsqlから取得する
        sql = 'SELECT * FROM kekka WHERE asin_code = ?'
        cur = db.execute(sql,(temurl,))
        kekka = cur.fetchall()
        work = kekka[0]
        
        # 総合レビュー数
        totalreview = work[15] + work[16]
        
        # ポジティブ率、ネガティブ率を産出する
        posiper = work[15] / totalreview
        negaper = work[16] / totalreview
        
        # 処理結果を処理結果クラスに挿入する
        # 商品概要の取得結果をデータクラスに挿入する
        selectionInfo = resultData.ResultData(work[0],work[1],work[2],totalreview,work[15],work[16])
    
        # レビューをデータクラスに挿入する
        selectionInfo.insertpositive(work[3],work[4])
        selectionInfo.insertpositive(work[5],work[6])
        selectionInfo.insertpositive(work[7],work[8])
        selectionInfo.insertnegative(work[9],work[10])
        selectionInfo.insertnegative(work[11],work[12])
        selectionInfo.insertnegative(work[13],work[14])
    
        # ポジネガ判定の比率をデータクラスに挿入する
        selectionInfo.reviewRatio(posiper,negaper)
    else:
        selectionInfo = resultData.ResultData(err="Not Data")

    return selectionInfo

# スクレイピングで取得した情報をdbに書き込む
def insertdb(resultData):
    db = sqlite3.connect("kekka.db",              #ファイル名
        isolation_level=None)
    
    sql1 = 'CREATE TABLE IF NOT EXISTS kekka (asin_code TEXT primary key,product_name TEXT, img TEXT,positaitle1 TEXT,positive1 TEXT,positaitle2 TEXT,positive2 TEXT,positaitle3 TEXT,positive3 TEXT,negataitle1 TEXT,negative1 TEXT,negataitle2 TEXT,negative2 TEXT,negataitle3 TEXT,negative3 TEXT,posicount INTEGER,negacount INTEGER)'
    db.execute(sql1)
    
    url_a = re.search('[^0-9A-Z]([0-9A-Z]{10})([^0-9A-Z]|$)', resultData.url).group().replace("/","")
    sql2 = 'INSERT INTO kekka(asin_code,product_name, img,positaitle1,positive1,positaitle2,positive2,positaitle3,positive3,negataitle1,negative1,negataitle2,negative2,negataitle3,negative3,posicount,negacount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    data = (url_a,resultData.name,resultData.img,resultData.posititle[0],resultData.positive[0],resultData.posititle[1],resultData.positive[1],resultData.posititle[2],resultData.positive[2],resultData.negatitle[0],resultData.negative[0],resultData.negatitle[1],resultData.negative[1],resultData.negatitle[2],resultData.negative[2],resultData.posicount,resultData.negacount)
    db.commit()
    db.execute(sql2,data)     #sql文を実行
    db.close()          #データベースを閉じる
    

# 既存のAmazonreview情報の更新を行う
def updatedb(resultData):
    return None

# Amazonreview情報を削除する
def deletedb():
    return None


# テスト用
if __name__ == '__main__':
    # a = selectdb(testurl)
    a = selectdb("https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E5%A4%A7%E4%B9%B1%E9%97%98%E3%82%B9%E3%83%9E%E3%83%83%E3%82%B7%E3%83%A5%E3%83%96%E3%83%A9%E3%82%B6%E3%83%BC%E3%82%BA-SPECIAL-Switch/dp/B07FDW61HX/ref=pd_bxgy_img_2/356-0976207-0608456?pd_rd_w=RzMyH&pf_rd_p=d8f6e0ab-48ef-4eca-99d5-60d97e927468&pf_rd_r=EVWKK7SF9DXYHNMP5H96&pd_rd_r=1de399b8-420a-438e-ab11-d7f56725aa35&pd_rd_wg=ruZTT&pd_rd_i=B07FDW61HX&psc=1")
    