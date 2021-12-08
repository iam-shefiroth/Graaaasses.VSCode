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
from pandas import Series
from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import ExtractAttributeFilter, POSKeepFilter, TokenFilter
import pandas
import re
import csv
import textwrap
 
#windows(chromedriver.exeのパスを設定)
chrome_path = r'z:\UserProfile\s20192087\Desktop\etc\chromedriver.exe'

#インポート時は実行されないように記載
if __name__ == '__main__':
     
    #　Amzon商品ページ
    review_list = []
    for i in range(8):
        csv_file = open(r'z:\UserProfile\s20192087\Desktop\etc\reviewData{0}-完.csv'.format(i), "r", encoding="ms932", errors="", newline="" )
        #リスト形式
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        a = 0
        b = 0
        for row in f:
            article = {
                "label": row[0],
                "text": row[1],
            }
            if row[0] == "ポジ" and a < 700:
                a += 1
                review_list.append(article) 
            elif row[0] == "ネガ":
                b += 1
                review_list.append(article)  
        csv_file.close()
    
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

    feature_to_weight = dict()
    for w, name in zip(classifier.coef_[0], feature_vectorizer.get_feature_names()):
        feature_to_weight[name] = w
    se = Series(feature_to_weight)
    se.sort_values(ascending=False, inplace=True)
    print("Positive or Negative")
    print("--Positiveの判定に効いた素性")
    print(se[:20])
    print("--Negativeの判定に効いた素性")
    print(se[-20:])
    print("--" * 50)

    def validate():
        # 学習
        classifier = LogisticRegression()
        transformed_X_train = feature_vectorizer.fit_transform(X_train)
        classifier.fit(transformed_X_train, y_train)
        # 評価
        vectorized = feature_vectorizer.transform(X_test)
        y_pred = classifier.predict(vectorized)
        print(classification_report(y_test, y_pred))
        # モデルのダンプ
        feature_to_weight = dict()
        for w, name in zip(classifier.coef_[0], feature_vectorizer.get_feature_names()):
            feature_to_weight[name] = w
        se = Series(feature_to_weight)
        se.sort_values(ascending=False, inplace=True)
        print("--Positiveの判定に効いた素性")
        print(se[:20])
        print("--Negativeの判定に効いた素性")
        print(se[-20:])
        print("--" * 50)
        return y_pred
    
    # 前処理
    char_filters = [
        RegexReplaceCharFilter("^[『「【].*[』」】]", ""),
        RegexReplaceCharFilter("(https?:\/\/[\w\.\-/:\#\?\=\&\;\%\~\+]*)", "")]
    # 後処理
    token_filters = [
        POSKeepFilter(['名詞', '動詞', '形容詞', '副詞']),
        ExtractAttributeFilter("base_form")]
    # Tokenizerの再初期化
    tokenizer = Tokenizer()
    # 前処理・後処理が追加されたVectorizerに変更
    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
    feature_vectorizer = CountVectorizer(binary=True, analyzer=analyzer.analyze)
    # 再評価
    result = validate()
    