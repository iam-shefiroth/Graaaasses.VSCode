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
from janome.tokenfilter import ExtractAttributeFilter, POSKeepFilter, TokenFilter,LowerCaseFilter,CompoundNounFilter
import pandas
from janome.tokenizer import Tokenizer
from os import P_DETACH, error
import codecs
import numpy as np
import io
import re
import neologdn
import sqlite3
np.seterr(divide='ignore') 
 
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
    
    con = sqlite3.connect('kekka.db')
    cur=con.cursor()
    for data in cur.execute("select * from kuutyoukaden_weight"):
        dic[data[0]] = float(data[1])

    return dic

class NumericReplaceFilter(TokenFilter):
        def apply(self, tokens):
            tmp = ""
            for i,token in enumerate(tokens):
                parts = token.part_of_speech.split(',')
                if parts[0] == '助動詞' and token.base_form == 'ない' and (tmp.part_of_speech.split(',')[0] == '動詞' or tmp.part_of_speech.split(',')[0] == '形容詞'):
                    tmp2 = token
                    token = tmp
                    token.base_form = tmp.surface + tmp2.base_form
                    token.surface = tmp.surface + tmp2.base_form
                    token.reading = tmp.reading + tmp2.reading
                    token.phonetic = tmp.phonetic + tmp2.phonetic
                    tmp = token
                else:
                    if tmp == "":
                        tmp = token
                    else:
                        if tmp.part_of_speech.split(',')[0] != '助動詞':
                            yield tmp
                        tmp = token

def analysisreview(amazonreview):
    choise = {}
    # CorpusElementのリスト
    naive_corpus = []
    
    # 前処理
    char_filters = [
        RegexReplaceCharFilter("(https?:\/\/[\w\.\-/:\#\?\=\&\;\%\~\+]*)", ""),
        RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ''),
        RegexReplaceCharFilter('おもしろい', '面白い'),
        RegexReplaceCharFilter('おもしろくない', '面白くない'),
        RegexReplaceCharFilter('たのしい', '楽しい')]
    # 後処理
    token_filters = [
        POSKeepFilter(['名詞', '動詞', '形容詞', '副詞', '助動詞']),
        LowerCaseFilter(),
        NumericReplaceFilter(),
        # CompoundNounFilter(),
        ExtractAttributeFilter("base_form")]
        
    naive_tokenizer = Tokenizer()

    # 一つのレビュー本文とトークンをリストに入れる
    for text2 in amazonreview:
        normalized_text = neologdn.normalize(text2["text"])
        tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)
        text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
        tokens = naive_tokenizer.tokenize(text_removed_symbol)
        element = CorpusElement(text_removed_symbol, tokens,title = text2["title"])
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

    choise["posicnt"] = p
    choise["negacnt"] = n

    p_per = p/len(amazonreview)
    n_per = n/len(amazonreview)

    choise["totalposiper"] = p_per
    choise["totalnegaper"] = n_per

    bestlist = []
    worstlist = []
    
    # 最も高い3件を表示
    for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores), reverse=True)[:3]:
        best = {"title":io.StringIO(element.title).readline(),
                "posiper":sum(element.pn_scores),
                "text":io.StringIO(element.text2).readline()}
        bestlist.append(best)
    choise["positive"] = bestlist
    

    # 平均値が最も低い3件を表示
    for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores))[:3]:
        worst = {"title":io.StringIO(element.title).readline(),
                "posiper":sum(element.pn_scores),
                "text":io.StringIO(element.text2).readline()}
        worstlist.append(worst)
    
    choise["negative"] = worstlist
        
    return choise