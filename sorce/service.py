from os import error
from re import A
from typing import Text
from flask import *
import matplotlib.pyplot as plt
import time

import resultData
import amazon_selection
import amazonAIt
import repository


# ロボット扱いにされてない場合、使う
testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC-%E3%83%9E%E3%83%AA%E3%82%AA%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3-Switch/dp/B07DPDDP5V/ref=pd_sbs_3/356-0976207-0608456?pd_rd_w=VK50K&pf_rd_p=133595aa-365a-4ded-92cd-226dcfd5ea4f&pf_rd_r=TWF2FTF3DDCBJSTB9RFC&pd_rd_r=4d37ec4a-17d3-4ffd-88ba-bd5668667080&pd_rd_wg=lAQH4&pd_rd_i=B07DPDDP5V&psc=1"
# testurl = "https://www.amazon.co.jp/%E3%83%9E%E3%83%AA%E3%82%AA-%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF-%E6%9D%B1%E4%BA%AC2020%E3%82%AA%E3%83%AA%E3%83%B3%E3%83%94%E3%83%83%E3%82%AF-%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%82%B9-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/dp/B09MZ6YQG5/ref=sr_1_6?crid=64D3261VWMSR&keywords=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF&qid=1640050427&s=videogames&sprefix=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%2Cvideogames%2C399&sr=1-6"

# 商品のジャンル判定
def categorycheck(category):
    check = ''
    if category == "ゲームソフト":
        check = 'OK'
    else:
        check = 'NO'
    return check

# 商品のジャンル次第で分析するファイルを選ぶ
def analysischoise(category,allreview):
    resultReview = ""
    if(category == "ゲームソフト"):
        resultReview = amazonAIt.analysisreview(allreview)
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
    
    # 処理速度を計る（後に消します）
    resultTimer = []
    resultTimer.append(time.perf_counter())
    
    #商品の情報を取得する。
    overview = amazon_selection.get_product_overview(url)
    resultTimer.append(time.perf_counter())
    
    # スクレイピング成功したかどうか確認
    if(overview["o_title"] == "!Not Scraping!"):
        selection = resultData.ResultData(err = overview["o_category"])
        return selection
    
    # 現在対応してるカテゴリーかどうか確認する
    judge = categorycheck(overview["o_category"])
    if judge == "NO":
        selection = resultData.ResultData(err = "この商品のジャンルは現在対応しておりません")
        return selection
    
    #レビューのスクレイピングを取得する
    all_review = amazon_selection.get_all_reviews(overview["review"])
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
    
    #レビューのポジネガ判定とその分析を行う
    resultReview = analysischoise(overview["o_category"],all_review)
    resultTimer.append(time.perf_counter())

    # 処理結果を処理結果クラスに挿入する
    # 商品概要の取得結果をデータクラスに挿入する
    selectionInfo = resultData.ResultData(url,overview["o_title"],overview["o_image"],totalreview,resultReview["posicnt"],
                                        resultReview["negacnt"])
    
    # レビューをデータクラスに挿入する
    insertreviews(selectionInfo,resultReview["positive"],resultReview["negative"])
    
    # ポジネガ判定の比率をデータクラスに挿入する
    selectionInfo.reviewRatio(resultReview["totalposiper"],resultReview["totalnegaper"])
    
    # Amazonreview情報をcsvに書き込む
    repository.insertdb(selectionInfo)
    
    resultTime(resultTimer)
    return selectionInfo

#テスト用受け渡し※後に消せ
if __name__ == '__main__':
    selection = reviewSelection(testurl)
    print(selection.img)
    print(selection.name)
    print(selection.url)
    for i in range(len(selection.positive)):
        print(selection.posititle[i])
        print(selection.positive[i])
        print(selection.negatitle[i])
        print(selection.negative[i])
    
    print(selection.posiReviewRatio)
    print(selection.negaReviewRatio)
    print(selection.totalcount)
    print(selection.posicount)
    print(selection.negacount)