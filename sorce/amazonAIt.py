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
from os import P_DETACH, error
import codecs
import numpy as np
import io
np.seterr(divide='ignore') 
#windows(chromedriver.exeのパスを設定)
chrome_path = r"z:/UserProfile/s20193085/Desktop/data/etc/chromedriver.exe"
 
#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'

class CorpusElement:
    def __init__(self, text2='', tokens=[], pn_scores=[],title = ''):
        self.text2 = text2 # テキスト本文
        self.tokens = tokens # 構文木解析されたトークンのリスト
        self.pn_scores = pn_scores # 感情極性値(後述)
        self.title = title  #レビューのタイトル
 


# トークンリストから極性値リストを得る
def get_pn_scores(tokens, pn_dic):
    scores = []
    
    for surface in [t.surface for t in tokens if t.part_of_speech.split(',')[0] in ['動詞','名詞', '形容詞', '副詞']]:
        if surface in pn_dic:
            scores.append(pn_dic[surface])
        
    return scores

# pn_ja.dicファイルから、単語をキー、極性値を値とする辞書を得る
def load_pn_dict():
    dic = {}
    
    with codecs.open(r'Z:/UserProfile/s20193085/Desktop/AIService/Graaaasses/Graaaasses/review_weightP.txt', 'r', 'UTF-8') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            # 各行は"良い:よい:形容詞:0.999995"
             # 先頭2行は不要なメタ情報のため、削除
            
            columns = line.split(',')
            
            s = columns[1].replace(" \r\n","")
            dic[columns[0]] = float(s)
            i = i + 1
            
    return dic

def analysisreview(amazonreview):
    ga = []
    
    # CorpusElementのリスト
    naive_corpus = []

    naive_tokenizer = Tokenizer()

    # 一つのレビュー本文とトークンをリストに入れる
    for text2 in amazonreview:
        tokens = naive_tokenizer.tokenize(text2["text"])
        element = CorpusElement(text2["text"], tokens,title = text2["title"])
        naive_corpus.append(element)

    # 感情極性対応表のロード
    pn_dic = load_pn_dict()

    # 各文章の極性値リストを得る
    p = 0
    n = 0
    for element in naive_corpus:
        element.pn_scores = get_pn_scores(element.tokens, pn_dic)
        ans = sum(element.pn_scores)

        if ans > 0:
            p += 1
        else:
            n += 1

    p_per = p/len(amazonreview)
    n_per = n/len(amazonreview)

    print("ポジ%",p_per)
    print("ネガ%",n_per)

    print("ベスト3")
    # 最も高い3件を表示
    for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores), reverse=True)[:3]:
        print('title: {}'.format(io.StringIO(element.title).readline()))
        print('ポジティブ度: {:.3f}'.format(sum(element.pn_scores)))
        print('Posi: {}'.format(io.StringIO(element.text2).readline()))
        print("--" * 50)
    # Error
    
    print("ワースト3")
    # 平均値が最も低い3件を表示
    for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores))[:3]:
        print('title: {}'.format(io.StringIO(element.title).readline()))
        print('ネガティブ度: {:.3f}'.format(sum(element.pn_scores)))
        print('Nega: {}'.format(io.StringIO(element.text2).readline()))
        print("--" * 50)
    
    
    return ga