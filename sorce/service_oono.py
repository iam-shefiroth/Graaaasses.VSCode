from os import error
from re import A
from typing import Text
from flask import *
import time

import resultData
import amazon_selection_oono
import amazonAIt_oono


# ロボット扱いにされた場合、使う
# testurl = "z:/UserProfile/s20193085/Desktop/data/check/Amazon.co.jp_ スーパーマリオ 3Dワールド + フューリーワールド_オンラインコード版 _ ゲーム.html"
# ロボット扱いにされてない場合、使う
testurl = "https://www.amazon.co.jp/%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4%E3%83%8A%E3%83%A0%E3%82%B3%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%86%E3%82%A4%E3%83%B3%E3%83%A1%E3%83%B3%E3%83%88-%E3%80%90PS4%E3%80%91%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%AA%E3%83%83%E3%83%88%E3%82%B7%E3%83%BC%E3%82%BA%E3%83%B3%E3%80%90%E6%97%A9%E6%9C%9F%E8%B3%BC%E5%85%A5%E7%89%B9%E5%85%B8%E3%80%91%E8%A1%A3%E8%A3%85DLC%E3%80%8E%E6%9A%81%E3%81%AE%E3%82%86%E3%81%8B%E3%81%9F%E3%80%8F%E3%81%8C%E5%85%A5%E6%89%8B%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E3%82%B3%E3%83%BC%E3%83%89-%E5%B0%81%E5%85%A5/dp/B08W5S54P1/ref=sr_1_7?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&keywords=%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC&qid=1639620405&sr=8-7"
# testurl = "https://www.amazon.co.jp/%E3%83%9E%E3%83%AA%E3%82%AA-%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF-%E6%9D%B1%E4%BA%AC2020%E3%82%AA%E3%83%AA%E3%83%B3%E3%83%94%E3%83%83%E3%82%AF-%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%82%B9-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/dp/B09MZ6YQG5/ref=sr_1_6?crid=64D3261VWMSR&keywords=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF&qid=1640050427&s=videogames&sprefix=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%2Cvideogames%2C399&sr=1-6"

# 商品のジャンル次第で分析するファイルを選ぶ
def analysischoise(category,allreview):
    resultReview = ""
    if(category == "ゲームソフト"):
        resultReview = amazonAIt_oono.analysisreview(allreview) 
    
    else:
        resultReview = None
        
    return resultReview

# 格納されてるレビュー結果をデータクラスに入れる
def insertreviews(info,positive,negative):
    for i in range(3):
        positive_one = positive[i]
        negative_one = negative[i]
        
        info.insertpositive(positive_one["title"],positive_one["text"])
        info.insertnegative(negative_one["title"],negative_one["text"])

# 処理時間を出力する（検証用）※後に消せ
def resultTime(resultTimer):
    print("Amazon商品取得時間：{}".format(resultTimer[1] - resultTimer[0]))
    print("全レビュー取得時間：{}".format(resultTimer[2] - resultTimer[1]))
    print("Amazonレビュー分析時間：{}".format(resultTimer[3] - resultTimer[2]))
    print("総合時間：{}".format(resultTimer[3] - resultTimer[0]))
    

#入力されたURLから結果処理に必要な情報を取得する
def reviewSelection(url):
    selectionInfo = []
    
    # 処理速度を計る
    resultTimer = []
    resultTimer.append(time.perf_counter())
    
    #商品の情報を取得する。
    overview = amazon_selection_oono.get_product_overview(url)
    resultTimer.append(time.perf_counter())
    
    # スクレイピング成功したかどうか確認
    if(overview["o_title"] == "!Not Scraping!"):
        selection = resultData.ResultData(err = overview["o_category"])
        return selection
    
    #レビューのスクレイピングを取得する
    all_review = amazon_selection_oono.get_all_reviews(overview["review"])
    # all_review = amazon_selection.get_all_reviews("all_review = amazon_selection.get_all_reviews")
    
    resultTimer.append(time.perf_counter())
    
    # 全レビュー取得中にロボット確認ページへ飛ばされてないか確認
    one_review = all_review[0]
    if(one_review["title"] == "!Not Scraping!"):
        selection = resultData.ResultData(err = one_review["text"])
        return selection
    
    
    # 総レビュー数
    totalreview = len(all_review)
    
    # レビュー数が少ないかどうか確認
    if(totalreview < 10):
        selection = resultData.ResultData(err = "レビュー数が少ないため分析出来ません")
        return selection
    
    # サクラレビューチェック
    
    #レビューのポジネガ判定とその分析を行う
    resultReview = analysischoise(overview["o_category"],all_review)
    resultTimer.append(time.perf_counter())
    
    # うまく処理されてないか確認
    if(resultReview == None):
        selection = resultData.ResultData(err = "この商品のジャンルは現在対応しておりません")
        return selection

    # 処理結果を処理結果クラスに挿入する
    # 商品概要の取得結果をデータクラスに挿入する
    selectionInfo = resultData.ResultData(url,overview["o_title"],overview["o_image"],totalreview,resultReview["posicnt"],
                                        resultReview["negacnt"])
    
    # レビューをデータクラスに挿入する
    insertreviews(selectionInfo,resultReview["positive"],resultReview["negative"])
    
    # ポジネガ判定の比率をデータクラスに挿入する
    selectionInfo.reviewRatio(resultReview["totalposiper"],resultReview["totalnegaper"])
    
    resultTime(resultTimer)
    return selectionInfo

#テスト用受け渡し※後に消せ
if __name__ == '__main__':
    selection = reviewSelection(testurl)
    print(selection.img)
    print(selection.name)
    print(selection.url)
    for i in range(len(selection.positive)):
        print("ポジティブ度{0}位".format(i+1),selection.posititle[i])
        print(selection.positive[i])
        print("**"*50)
        print("ネガティブ度{0}位".format(i+1),selection.negatitle[i])
        print(selection.negative[i])
        print("**"*50)
    
    print(selection.posiReviewRatio)
    print(selection.negaReviewRatio)
    print(selection.totalcount)
    print(selection.posicount)
    print(selection.negacount)