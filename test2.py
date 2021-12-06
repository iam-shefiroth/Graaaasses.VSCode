from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import pandas
import re
 
#windows(chromedriver.exeのパスを設定)
chrome_path = r'C:\data\etc\chromedriver'
 
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
def get_all_reviews(url, review_list):
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')
        


        for j in range(len(reviews)):
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
     
    #　Amzon商品ページ
    urls = []
    urls.append('https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9D%E3%82%B1%E3%83%83%E3%83%88%E3%83%A2%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%BC-%E3%83%96%E3%83%AA%E3%83%AA%E3%82%A2%E3%83%B3%E3%83%88%E3%83%80%E3%82%A4%E3%83%A4%E3%83%A2%E3%83%B3%E3%83%89-Switch/product-reviews/B09CL1NLVP/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
    urls.append('https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%BA-Switch/product-reviews/B097BL85Y7/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
    review_list = []
    for url in urls:
        review_url = url.replace('dp', 'product-reviews')
        review_list = get_all_reviews(review_url, review_list)
    
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
    df = pandas.DataFrame(review_list)
    filtered_by_label = df.query("label == 'ポジ' | label == 'ネガ'")
    group_by_label = filtered_by_label.groupby("label")
    labels_size = group_by_label.size()
    print(labels_size)
    
    label_vectorizer = LabelEncoder()
    transformed_label = label_vectorizer.fit_transform(df.get("label"))
    df["label"] = transformed_label
    # 入力と出力に分割
    x, y = df.get("text"), df.get("label")
    # 学習とテストデータに9:1で分割
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, stratify=y, random_state=0)
    # それぞれの数があっているか確認
    print([len(c) for c in [X_train, X_test, y_train, y_test]])

    tokenizer = Tokenizer(wakati=True)
    feature_vectorizer = CountVectorizer(binary=True, analyzer=tokenizer.tokenize)
    # 学習
    classifier = LogisticRegression()
    transformed_X_train = feature_vectorizer.fit_transform(X_train)
    classifier.fit(transformed_X_train, y_train)

    vectorized = feature_vectorizer.transform(X_test)
    y_pred = classifier.predict(vectorized)
    print(classification_report(y_test, y_pred,target_names=label_vectorizer.classes_))