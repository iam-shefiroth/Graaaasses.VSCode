from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap

#windows(chromedriver.exeのパスを設定)
chrome_path = r'z:\UserProfile\s20193085\Desktop\data\etc\chromedriver.exe'

#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'

#テスト用url※後に消せ
testurl:str

 
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

#商品の情報をリストにする
def get_product_overview(url):
    overview_list = []
    print("now_reading_page")
    text = get_amazon_page_info(url)
    amazon_bs = BeautifulSoup(text,features='lxml')
    
    #amazonの商品情報を取得
    title = amazon_bs.select_one('span.product-title-word-break')
    #image = amazon_bs.select_one('li.imageThumbnail span.a-button-next img')
    all_review_page = amazon_bs.select('div.a-spacing-medium a')
    category = amazon_bs.select('ul.a-horizontal span.a-link-item')
    # overview_list.append(title)
    # overview_list.append(image)
    # overview_list.append(category)
    # overview_list.append(all_review_page)
    print(title)
    #print(image)
    print(all_review_page)
    print(category)
    return overview_list

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

            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list


    #テスト用実行(amazonレビューget用)※後に消せ
if __name__ == '__main__':
    go = input("please insert to go method overview = 1,amazon all review = other")
    if(go == 1):
        print("goto overview")
        testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%BA-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/dp/B097C67NF2/ref=pd_sbs_1/355-8689788-2301132?pd_rd_w=A3Cnt&pf_rd_p=4e34a507-1281-42ae-953a-93a761caa89c&pf_rd_r=MY3KWA5QSEE4X9N2YYZ5&pd_rd_r=8db547d5-80e1-46a6-a91f-046d92e06a57&pd_rd_wg=c4JXe&pd_rd_i=B097C67NF2&psc=1"
        overview_list = get_product_overview(testurl)
        print(overview_list)
    else:
        print("goto allreview")
        testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%BA-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/product-reviews/B097C67NF2/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        overview_list = get_all_reviews(testurl)
        print(overview_list)
    