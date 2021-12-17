from flask import *
from dataclasses import dataclass

@dataclass
class ResultData():
    url:str                     #url（リンク）
    name:str                    #商品名
    img:str                     #画像
    posititle = []              #ポジティブレビュータイトル（配列）
    negatitle = []              #ネガティブレビュータイトル（配列）
    positive = []               #ポジティブレビュー(配列)
    negative = []               #ネガティブレビュー（配列）
    posiReviewRatio:float       #ポジティブ確率（Float）
    negaReviewRatio:float       #ネガティブ確率（Float）
    totalcount:int              #総レビュー数
    posicount:int               #ポジティブレビュー数
    negacount:int               #ネガティブレビュー数
    
    def __init__(self,insert_url,insert_name,insert_img,totalcnt = 0,posicnt = 0,negacnt = 0,positive=[],negative=[],posititle=[],negatitle=[]):
        self.url = insert_url
        self.name = insert_name
        self.img = insert_img
        self.totalcount = totalcnt
        self.posicount = posicnt
        self.negacount = negacnt
        self.positive = positive
        self.negatitle = negative
        self.posititle = posititle
        self.negatitle = negatitle
        
    def reviewRatio(self, posi, nega):
        sums = posi + nega
        self.posiReviewRatio = round((posi / sums) * 100, 1)
        self.negaReviewRatio = 100 - self.posiReviewRatio