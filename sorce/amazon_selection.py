from time import sleep
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd 
# import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager
import re


#windows(chromedriver.exeのパスを設定)※要変更
# chrome_path = r'z:\UserProfile\s20193085\Desktop\data\etc\chromedriver.exe'
# chrome_path = "z:\\UserProfile\s20192060\Desktop\AI開発\chromedriver.exe"
#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'

# スクレイピングブロック判定
blockJudge = "申し訳ありませんが、お客様がロボットでないことを確認させていただく必要があります。最良のかたちでアクセスしていただくために、お使いのブラウザがクッキーを受け入れていることをご確認ください。"
 
#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    # スクレイピングブロック対策として、関係ないサイト且つ容量が少ないサイトを開く
    driver.get("https://www.amazon.co.jp/gp/help/customer/display.html?nodeId=201909000")
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す

#商品の情報をリストにする
def get_product_overview(url):
    print("now_reading_page")
    text = get_amazon_page_info(url)
    amazon_bs = bs4.BeautifulSoup(text,features='lxml')
    
    #スクレイピングブロックチェック
    title = amazon_bs.select_one('.a-last')
    if(title != None):
        title = title.text.replace("\n", "").replace("\u3000", "").strip()
        if(title == blockJudge):
            overview_list = {"o_title":"!Not Scraping!","o_category":"スクレイピングブロックされています、時間が経ってから再度ご利用ください"}
            return overview_list
    
    # 商品名
    title = amazon_bs.select_one('.product-title-word-break')
    
    # Amazon商品概要サイトではないURLかどうか確認する
    if(title == None):
        overview_list = {"o_title":"!Not Scraping!","o_category":"Amazon商品概要サイトのURLでないか、URL内容に誤りがあります"}
        return overview_list
    title = title.text.replace("\n", "").replace("\u3000", "").strip()
    
    # 商品の画像
    image = amazon_bs.select('#main-image-container > ul > li.image.item.itemNo0.maintain-height.selected > span > span > div > img')
    image = image[0].attrs['src']
    
    
    # 商品のカテゴリー
    category = []
    category.append(amazon_bs.select_one('#wayfinding-breadcrumbs_feature_div > ul > li:nth-of-type(7) > span > a'))
    category.append(amazon_bs.select_one('#wayfinding-breadcrumbs_feature_div > ul > li:nth-of-type(5) > span > a'))
    category.append(amazon_bs.select_one('#wayfinding-breadcrumbs_feature_div > ul > li:nth-of-type(3) > span > a'))
    category.append(amazon_bs.select_one('#wayfinding-breadcrumbs_feature_div > ul > li:nth-of-type(1) > span > a'))
    
    
    # パンくずリストを取得できたかどうか確認
    for i in range(len(category)):
        if category[i] != None:
            category[i]= category[i].text.replace("\n", "").replace("\u3000", "").strip()
        else:
            category[i] = ''
    

    # 商品の全レビューURL
    all_review_page = amazon_bs.select_one('#reviews-medley-footer > div.a-row.a-spacing-medium a')
    
    # AmazonレビューページURLが存在するかどうか確認
    if(all_review_page == None):
        overview_list = {"o_title":"!Not Scraping!","o_category":"この商品のレビュー数は0件です"}
    else:
        all_review_page ='https://www.amazon.co.jp/'  + all_review_page.attrs['href']
        
        # Amazon商品の取得情報を配列に挿入
        overview_list = {"o_title":title,"o_image":image,"o_category":category,"review":all_review_page}
    
    
    
    return overview_list

# Amazonの発売日もしくは取り扱い開始日を取得
def getOriginDate(url):
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(3)
    try:
        tableElem = driver.find_element_by_id('productDetails_detailBullets_sections1')
        html = tableElem.get_attribute('outerHTML')
        #print(type(html))
        dfs = pd.read_html(html)
        df = dfs[0].values.tolist()
        dates = []
        for data in df:
            if data[0] in 'Amazon.co.jp での取り扱い開始日' or '発売日' in data[0]:
                date =  datetime.datetime.strptime(data[1], '%Y/%m/%d')
                dates.append(date)
        date = decideDates(dates)
        return date
    except:
        pass
        try:
            ulElem = driver.find_element_by_id('detailBullets_feature_div')
            liElem = ulElem.find_elements_by_class_name('a-list-item')
            dates = []
            for li in liElem:
                if '発売日' in li.text or '取り扱い開始日' in li.text:
                    date = datetime.datetime.strptime(re.findall('20.+', li.text)[0], '%Y/%m/%d')
                    dates.append(date)
            date = decideDates(dates)
            return date
        except:
            pass
            print("取得失敗")
            return None
                
def decideDates(dates):
    if len(dates) > 1:
        return heapq.nlargest(1, dates)[0]
    else:
        return dates[0]

# 全ページ分をリストにする
def get_all_reviews(url):
    
    review_list = []                        #　初期化
    origin_date = getOriginDate(url)
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        
        url = url.replace('dp', 'product-reviews')
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = bs4.BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        
        # スクレイピングブロックチェック
        title = amazon_bs.select_one('.a-last')
        if(title != None):
            title = title.text.replace("\n", "").replace("\u3000", "").strip()
            if(title == blockJudge):
                review_list = []
                article = {"title":"!Not Scraping!","text":"スクレイピングブロックされています、時間が経ってから再度ご利用ください。"}
                review_list.append(article)
                return review_list
        
        review_title = amazon_bs.select('a.review-title')   #ページ内の全レビュータイトルを取得
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')    # ページ内の全評価数を取得
        spandate  = amazon_bs.select('span.review-date') # ページ内の全レビュー日を取得
        
        if stars != []:
            for j in range(len(stars)):
                # origin_dateから日数を取得したかどうか確認
                if origin_date is None:
                    dateResult = "未定義"
                else:
                    reviewDate = re.findall('2.*?日', spandate[j].text)
                    reviewDate = datetime.datetime.strptime(reviewDate[0], '%Y年%m月%d日')
                    dateResult = (reviewDate - origin_date).days
                star = re.findall('[0-5].[0-5]', stars[j].text)[0]
                starFloat = float(star)
                article = {
                "title":review_title[j].text.replace("\n", "").replace("\u3000", ""),
                "text": reviews[j].text.replace("\n", "").replace("\u3000", ""),
                "dateResult": dateResult,
                "star": star,
                }
                review_list.append(article)                      #　レビュー情報をreview_listに格納
            
            next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        else:
            break
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする

            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
    return review_list