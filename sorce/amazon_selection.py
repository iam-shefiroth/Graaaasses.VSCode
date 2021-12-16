from time import sleep
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap

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
    # ASIN取得2
def get_asin_from_amazon_2(url):
     
    asin = ""
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
     
    # ブラウザーを起動
    driver = webdriver.Chrome("z:/UserProfile/s20193085/Desktop/data/etc/chromedriver.exe", options=options)
    driver.get(url)
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
     
    elem_base = driver.find_element_by_id('ASIN')
    if elem_base:
        asin = elem_base.get_attribute("value")
    else:
        print("NG")
         
    # ブラウザ停止
    driver.quit()
     
    return asin

#商品の情報をリストにする
def get_product_overview(url):
    overview_list = []
    print("now_reading_page")
    text = get_amazon_page_info(url)
    # print(text)
    amazon_bs = bs4.BeautifulSoup(text,features='lxml')
    
    #amazonの商品情報を取得
    
    # ↓商品名
    title = amazon_bs.select_one('.product-title-word-break')
    title = title.text.replace("\n", "").replace("\u3000", "").strip()
    # 商品の画像
    image = amazon_bs.select('#main-image-container > ul > li.image.item.itemNo0.maintain-height.selected > span > span > div > img')
    image = image[0].attrs['src']
    # 商品の全レビューURL
    all_review_page = amazon_bs.select_one('#reviews-medley-footer > div.a-row.a-spacing-medium a')
    all_review_page ='https://www.amazon.co.jp/'  + all_review_page.attrs['href']
    # 商品のカテゴリー
    category = amazon_bs.select_one('#wayfinding-breadcrumbs_feature_div > ul > li:nth-of-type(5) > span > a')
    category = category.text.replace("\n", "").replace("\u3000", "").strip()
    
    overview_list.append(url)
    overview_list.append(title)
    overview_list.append(image)
    overview_list.append(category)
    overview_list.append(all_review_page)
    
    return overview_list

# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = bs4.BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
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
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする

            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
    return review_list

