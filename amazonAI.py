from time import sleep
from numpy.lib.function_base import piecewise
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import ExtractAttributeFilter, POSKeepFilter, TokenFilter
import pandas
from janome.tokenizer import Tokenizer
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

            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list

def get_gazou(url):
    i = 1
    print(i,'page_search')
    i += 1
    text = get_amazon_page_info(url)
    amazon_bs = BeautifulSoup(text, features='lxml')
    gazous  = amazon_bs.select('.a-fixed-left-grid-col img')
    gazou = gazous[0].attrs['src']
    
    return gazou


#インポート時は実行されないように記載
if __name__ == '__main__':
     
    url = 'https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%8A%E3%83%93%E3%81%A4%E3%81%8D-%E3%81%A4%E3%81%8F%E3%81%A3%E3%81%A6%E3%82%8F%E3%81%8B%E3%82%8B-%E3%81%AF%E3%81%98%E3%82%81%E3%81%A6%E3%82%B2%E3%83%BC%E3%83%A0%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0-Switch/dp/B093WDM64Q/ref=sr_1_39?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=1VBWM2M8Q16SE&keywords=%E3%82%B2%E3%83%BC%E3%83%A0%E3%82%BD%E3%83%95%E3%83%88+switch&qid=1639453269&sprefix=ge-mu%2Caps%2C351&sr=8-39'

    review_list = []
    review_url = url.replace('dp', 'product-reviews')
    review_list = get_all_reviews(review_url)
    gazou = get_gazou(review_url)

    model = pickle.load(open('amazon_review.pkl', 'rb'))

    # 前処理
    char_filters = [
        RegexReplaceCharFilter("(https?:\/\/[\w\.\-/:\#\?\=\&\;\%\~\+]*)", "")]
    # 後処理
    token_filters = [
        POSKeepFilter(['名詞', '動詞', '形容詞', '副詞']),
        ExtractAttributeFilter("base_form")]
    # Tokenizerの初期化
    tokenizer = Tokenizer()
    # 前処理・後処理が追加されたVectorizerに変更
    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
    feature_vectorizer = CountVectorizer(binary=True, analyzer=analyzer.analyze)
    df = pandas.DataFrame(review_list)
    vectorized = feature_vectorizer.transform(df.get("text"))
    pre = model.predict(vectorized)
    print(pre)
