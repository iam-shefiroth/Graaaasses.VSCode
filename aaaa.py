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
        gazou  = amazon_bs.select('.a-fixed-left-grid-col')
        
        for j in range(len(gazou)):
            article = {
            "gazou": gazou[j].attrs['src'] 
            }
            review_list.append(article)                      #　レビュー情報をreview_listに格納
        
        return gazou
 
#インポート時は実行されないように記載
if __name__ == '__main__':
     
    url = 'https://www.amazon.co.jp/TCL-%E3%82%B9%E3%83%9E%E3%83%BC%E3%83%88%E3%83%86%E3%83%AC%E3%83%93-32S516E-%E5%A4%96%E4%BB%98%E3%81%91HDD%E3%81%A7%E8%A3%8F%E7%95%AA%E7%B5%84%E9%8C%B2%E7%94%BB%E5%AF%BE%E5%BF%9C-2021%E5%B9%B4%E3%83%A2%E3%83%87%E3%83%AB/dp/B09HQK5PRD/ref=sr_1_1_sspa?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2Y7ZGOOKYNRBP&dchild=1&keywords=%E3%83%86%E3%83%AC%E3%83%93&qid=1635483159&sprefix=%E3%83%86%E3%83%AC%E3%83%93%2Caps%2C227&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMzRKQkw5RUZLWjVQJmVuY3J5cHRlZElkPUEwMzMyMzM1MzVDR0ZMVEZIV1RFTiZlbmNyeXB0ZWRBZElkPUEzMTBUMkFSMjU5WDE0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1'

    review_list = []
    review_url = url.replace('dp', 'product-reviews')
    review_list = get_all_reviews(review_url)

    print(review_list)

            