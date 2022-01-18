import resultData
import csv
import pandas as pd
import os
import glob

testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%AB%E3%83%BC%E3%83%888-%E3%83%87%E3%83%A9%E3%83%83%E3%82%AF%E3%82%B9-Switch/dp/B01N12G06K/ref=bmx_dp_gm4br0pn_3/356-0976207-0608456?pd_rd_w=Ok09I&pf_rd_p=4d553c85-e63f-434a-bc92-4126a56917a6&pf_rd_r=HMKJPX6FR6M08J7D8FTG&pd_rd_r=cd57e681-f8ab-4aca-9c5b-ed215a762779&pd_rd_wg=NsjBR&pd_rd_i=B01N12G06K&psc=1"
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

# csvファイルを作る
def createdb():
    return None

# 入力されたurlと格納されているdb(csv)内のurlを比較する
def selectdb(url):
    
    # ディレクトリ変更（要変更）
    os.chdir(r'z:/UserProfile/s20193085/Desktop/data/db')
    df = pd.DataFrame(columns = [])
    
    # csvファイルを読み込む
    for onefile in glob.glob("*amazonreview*"):
        with open(r'z:/UserProfile/s20193085/Desktop/data/db/' + onefile,'r', encoding='utf-8', errors='ignore',newline="") as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                print(row)
            f.close
    
    return None

# スクレイピングで取得した情報をdb(csv)に書き込む
def insertdb(resultData):
    with open(r'z:/UserProfile/s20193085/Desktop/data/db/amazonreview_{0}.csv'.format(1),'w',encoding="utf-8", errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow()
        f.close()
        return None

# 既存のAmazonreview情報の更新を行う
def updatedb(resultData):
    return None

# Amazonreview情報を削除する
def deletedb():
    return None
# テスト用
if __name__ == '__main__':
    selectdb(testurl)