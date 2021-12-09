from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
 
#windows(chromedriver.exeのパスを設定)
chrome_path = r'z:\UserProfile\s20192087\Desktop\etc\chromedriver.exe'
 
#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'
 
#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=chrome_path,options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す
 
# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')
        
        for j in range(len(stars)):
            article = {
            "text": reviews[j].text.replace("\n", "").replace("\u3000", ""),
            "label": stars[j].text,
            }
            review_list.append(article)                      #　レビュー情報をreview_listに格納

             
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする

            sleep(1)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list
 
#インポート時は実行されないように記載
if __name__ == '__main__':
     
    urls = []
    # スイッチ
    urls.append('https://www.amazon.co.jp/Monster-Hunter-Rise-Deluxe-%E8%BC%B8%E5%85%A5%E7%89%88/product-reviews/B08JJ3VC8Z/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')

    for k, url in enumerate(urls, start=1):
        review_list = []
        review_url = url.replace('dp', 'product-reviews')
        review_list = get_all_reviews(review_url)
        a = 0
        b = 0
        for review in review_list:
            if review["label"] == "5つ星のうち5.0":
                review["label"] = "ポジ"
                a += 1
            elif review["label"] == "5つ星のうち4.0":
                review["label"] = "ポジ"
                a += 1
            elif review["label"] == "5つ星のうち3.0":
                review["label"] = "ネガ"
                b += 1
            elif review["label"] == "5つ星のうち2.0":
                review["label"] = "ネガ"
                b += 1
            elif review["label"] == "5つ星のうち1.0":
                review["label"] = "ネガ"
                b += 1
            
        #CSVにレビュー情報の書き出し
        with open(r'z:\UserProfile\s20192087\Desktop\etc\reviewData{0}.csv'.format(k),'w', encoding='CP932', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            # 全データを表示
            for review in review_list:
                csvlist=[]
                #データ作成
                csvlist.append(review["label"])
                csvlist.append(review["text"])
                # 出力    
                writer.writerow(csvlist)
            # ファイルクローズ
            print("csv",k)
            f.close()