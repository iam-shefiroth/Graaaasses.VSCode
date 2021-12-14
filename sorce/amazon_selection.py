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
    # ASIN取得2
def get_asin_from_amazon_2(url):
     
    asin = ""
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
     
    # ブラウザーを起動
    driver = webdriver.Chrome("z:\UserProfile\s20193085\Desktop\data\etc\chromedriver.exe", options=options)
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
    text = get_asin_from_amazon_2(url)
    print(text)
    amazon_bs = bs4.BeautifulSoup(text,features='lxml')
    
    #amazonの商品情報を取得
    title = amazon_bs.select_one('.product-title-word-break')
    #image = amazon_bs.select_one('li.imageThumbnail span.a-button-next img')
    all_review_page = amazon_bs.select_one('a.a-link-emphasis href')
    category = amazon_bs.select_one('span.a-link-item a')
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
        amazon_bs = bs4.BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        review_title = amazon_bs.select('a.review-title')
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')
        
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


    #テスト用実行(amazonレビューget用)※後に消せ
if __name__ == '__main__':
    # print("goto overview")
    # testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%AB%E3%83%BC%E3%83%888-%E3%83%87%E3%83%A9%E3%83%83%E3%82%AF%E3%82%B9-Switch/dp/B01N12G06K?ref_=Oct_d_obs_d_637394&pd_rd_w=tdtgg&pf_rd_p=03b65386-84ce-4d82-8c83-dd9d2863fe54&pf_rd_r=7324W03N2CXES5GZP2V0&pd_rd_r=2c99141f-47e1-4744-8965-105b19ea3a38&pd_rd_wg=0FBhj&pd_rd_i=B01N12G06Khttps://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%AB%E3%83%BC%E3%83%888-%E3%83%87%E3%83%A9%E3%83%83%E3%82%AF%E3%82%B9-Switch/dp/B01N12G06K?ref_=Oct_d_obs_d_637394&pd_rd_w=tdtgg&pf_rd_p=03b65386-84ce-4d82-8c83-dd9d2863fe54&pf_rd_r=7324W03N2CXES5GZP2V0&pd_rd_r=2c99141f-47e1-4744-8965-105b19ea3a38&pd_rd_wg=0FBhj&pd_rd_i=B01N12G06K"
    # overview_list = get_product_overview(testurl)
    # print(overview_list)
    
    print("goto allreview")
    testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%BA-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/product-reviews/B097C67NF2/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    overview_list = get_all_reviews(testurl)
    print(overview_list)
    