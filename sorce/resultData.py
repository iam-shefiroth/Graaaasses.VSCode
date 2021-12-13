from flask import *


class ResultData():
    url:str                     #url（リンク）
    name:str                    #商品名
    img:str                     #画像
    positive = []               #ポジティブレビュー(配列)
    negative = []               #ネガティブレビュー（配列）
    posiper:int
    negaper:int
    
    def overviewInsert(self,insert_url,insert_name,insert_img,posiper,negaper):
        self.url = insert_url
        self.name = insert_name
        self.img = insert_img
        self.posiper = posiper
        self.negaper = negaper
    
    def positiveInsert(self,word):
        self.positive.append(word)
    
    def negativeInsert(self,word):
        self.negative.append(word)