from time import sleep
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
from concurrent.futures import ThreadPoolExecutor

#windows(chromedriver.exeのパスを設定)※要変更
chrome_path = r'z:\UserProfile\s20193085\Desktop\data\etc\chromedriver.exe'

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

# Amazonレビュー全ページのURLを取得する
def get_allPage(url):
    allPage = []
    i = 1
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = bs4.BeautifulSoup(text, features='lxml',from_encoding="utf-8")    #　HTML情報を解析する
        allPage.append(amazon_bs)
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする
            
            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
        return allPage

# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    review_all_page = get_allPage(url)           #Amazonレビューページの初期化
    
    with ThreadPoolExecutor(len(get_allPage)) as executor:
        # 全レビューをタイトル・本文・星それぞれ
        work1,work2,work3 = list(executor.map())
        
        amazon_bs = bs4.BeautifulSoup(text, features='lxml',from_encoding="utf-8")    #　HTML情報を解析する
        review_title = amazon_bs.select('a.review-title')
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')
        # print(text)
        
        for j in range(len(stars)):
            article = {
            "title":review_title[j].text.replace("\n", "").replace("\u3000", ""),
            "text": reviews[j].text.replace("\n", "").replace("\u3000", ""),
            "label": stars[j].text,
            }
            review_list.append(article)                      #　レビュー情報をreview_listに格納
    return review_list

if __name__ == "__main__":
    test = [{"1":"死ね加須","2":"Cyka","3":"クズ"},{"1":"最高","2":"楽しい","3":"Good"}]
    
    for tes in test:
        sa = tes["1"]
        df = tes["3"]
        print(sa)
        print(df)