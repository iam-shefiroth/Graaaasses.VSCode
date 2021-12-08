import requests
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#上のやつはAnacondaのプロンプトからインストールして

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
}

# ASIN取得
def get_asin_from_amazon(url):
    
    asin = ""
    
    try:
        text = get_page_from_amazon(url)
        soup = BeautifulSoup(text, features='lxml')
        
        div_base = soup.find(class_="column col2")
        asin = div_base.find(class_="value").text
    except:
        print(text)
        traceback.print_exc()        
    
    return asin

# ASIN取得2
def get_asin_from_amazon_2(url):
    
    asin = ""
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    
    # ブラウザーを起動
    #佐藤君の場所のパスを入力kして
    driver = webdriver.Chrome(r"z:\UserProfile\s20193085\Desktop\data\etc\chromedriver", options=options) 
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

# Amazonページ取得
def get_page_from_amazon(url):
    
    text = ""
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    
    # ブラウザーを起動
    driver = webdriver.Chrome(r"z:\UserProfile\s20193085\Desktop\data\etc\chromedriver", options=options)
    driver.get(url)
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
    
    text = driver.page_source
    
    # ブラウザ停止
    driver.quit()
    
    return text

# サクラ度分析の値取得
def get_detail_value(elem):
    
    value = elem.find_element_by_tag_name("div").text
    value = value.replace("%", "", 1)
    value = value.strip()
    
    return value

# サクラチェッカーをスクレイピング
def get_sakurachecker(asin):
    
    url = "https://sakura-checker.jp/search/" + asin + "/"
    
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    
    # ブラウザーを起動
    driver = webdriver.Chrome(r"z:\UserProfile\s20193085\Desktop\data\etc\chromedriver", options=options)
    driver.get(url)
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
    
    # 独自の評価
    rating = ""
    try:
        elem_base = driver.find_element_by_class_name("mainBlock")
        elem_rating = elem_base.find_element_by_class_name('item-rating')
        rating = elem_rating.text
        rating = rating.replace("/5", "", 1)
    except:
        traceback.print_exc()     
    
    # サクラ度
    try:
        elem_sakura_num = driver.find_element_by_class_name("sakura-num")
        sakura_num = elem_sakura_num.text
        sakura_num = sakura_num.replace("%", "", 1)
    except:
        traceback.print_exc()   
    
    # サクラ度の詳細分析
    try:
        elem_base = driver.find_element_by_class_name("mainBlock")
        elem_circle = elem_base.find_elements_by_class_name('circlecustom')
    
        price_product = get_detail_value(elem_circle[0])
        shop_area = get_detail_value(elem_circle[1])
        shop_review = get_detail_value(elem_circle[2])
        review_distribution = get_detail_value(elem_circle[3])
        review_date = get_detail_value(elem_circle[4])
        review_reviewer = get_detail_value(elem_circle[5])
    except:
        traceback.print_exc()    
    
    # ブラウザ停止
    driver.quit()
    
    print("独自評価：" + rating)
    print("サクラ度：" + sakura_num)
    print("価格・製品：" + price_product)
    print("ショップ情報・地域：" + shop_area)
    print("ショップレビュー：" + shop_review)
    print("レビュー分布：" + review_distribution)
    print("レビュー日付：" + review_date)
    print("レビュー&amp;レビュアー：" + review_reviewer)
    
if __name__ == '__main__':
    url = input()
    
    # 実際にアクセスしてASIN取得
    asin = get_asin_from_amazon_2(url)

    # サクラチェッカーをスクレイピング
    get_sakurachecker(asin)