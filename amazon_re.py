import json
from os import error
from janome.tokenizer import Tokenizer
import glob
import codecs
import numpy as np
import io
import csv
import re
np.seterr(divide='ignore') 

# livedoorトピックニュースの文章リスト


# livedoorトピックニュースのファイル名一覧を取得する
paths = r'z:\UserProfile\s20192004\Desktop\data\etc\reviewData4y.csv'
texts = []
text = []
i = 0
with open(paths) as f:
    original_text = csv.reader(f)


    for row in original_text:
        text.append(row)
        texts.append(text[i][1])
        i= i + 1
            

print(i)

class CorpusElement:
    def __init__(self, text='', tokens=[], pn_scores=[]):
        self.text2 = text2 # テキスト本文
        self.tokens = tokens # 構文木解析されたトークンのリスト
        self.pn_scores = pn_scores # 感情極性値(後述)


# CorpusElementのリスト
naive_corpus = []

naive_tokenizer = Tokenizer()

for text2 in texts:
    tokens = naive_tokenizer.tokenize(text2)
    element = CorpusElement(text2, tokens)
    naive_corpus.append(element)





# pn_ja.dicファイルから、単語をキー、極性値を値とする辞書を得る
def load_pn_dict():
    dic = {}
    
    with codecs.open(r'C:\data2\amazon\review_weightP.txt', 'r', 'UTF-8') as f:
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

# トークンリストから極性値リストを得る
def get_pn_scores(tokens, pn_dic):
    scores = []
    
    for surface in [t.surface for t in tokens if t.part_of_speech.split(',')[0] in ['動詞','名詞', '形容詞', '副詞']]:
        if surface in pn_dic:
            scores.append(pn_dic[surface])
        
    return scores


# 感情極性対応表のロード
pn_dic = load_pn_dict()
print(pn_dic['良い'])
# 0.999995

# 各文章の極性値リストを得る
for element in naive_corpus:
    element.pn_scores = get_pn_scores(element.tokens, pn_dic)



# 最も高い5件を表示
for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores), reverse=True)[:5]:
    print('Average: {:.3f}'.format(sum(element.pn_scores)))
    print('Positib: {}'.format(io.StringIO(element.text2).readline()))
# Error
    
print("-------------------------------------------------------------------------------------")
  

# 平均値が最も低い5件を表示
for element in sorted(naive_corpus, key=lambda e: sum(e.pn_scores))[:5]:
    print('Average: {:.3f}'.format(sum(element.pn_scores)))
    print('Negatib: {}'.format(io.StringIO(element.text2).readline()))