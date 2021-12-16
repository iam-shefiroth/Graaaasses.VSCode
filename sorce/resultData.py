from flask import *


class ResultData():
    url:str                     #url（リンク）
    name:str                    #商品名
    img:str                     #画像
    positive = []               #ポジティブレビュー(配列)
    negative = []               #ネガティブレビュー（配列）
    posiReviewRatio:float
    negaReviewRatio:float
    
    def overviewInsert(self,insert_url,insert_name,insert_img):
        self.url = insert_url
        self.name = insert_name
        self.img = insert_img
    
    def positiveInsert(self,word):
        self.positive.append(word)
    
    def negativeInsert(self,word):
        self.negative.append(word)
        
    def reviewRatio(self, posi, nega):
        sums = posi + nega
        self.posiReviewRatio = round((posi / sums) * 100, 1)
        self.negaReviewRatio = 100 - self.posiReviewRatio