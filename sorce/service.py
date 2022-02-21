from os import error
from re import A
from typing import Text
from flask import *
import matplotlib.pyplot as plt
import time

import resultData
import amazon_selection
import gamesoftAI
import kuutyoukadenAI
import chairAI
import repository
import sakura_jadgement


# 商品のジャンル判定
def categorycheck(category):
    check = 'NO'
    for category_one in category:
        if category_one == "ゲームソフト":
            check = 'ゲームソフト'
            break
        elif category_one == '空調・季節家電':
            check = '空調・季節家電'
            break
        elif category_one == 'チェア':
            check = 'チェア'
            break
    
    return check

# 商品のジャンル次第で分析するファイルを選ぶ
def analysischoise(category,allreview):
    resultReview = ""
    if(category == "ゲームソフト"):
        resultReview = gamesoftAI.analysisreview(allreview)
    elif category == "空調・季節家電":
        resultReview = kuutyoukadenAI.analysisreview(allreview)
    elif category == "チェア":
        resultReview = chairAI.analysisreview(allreview)
    return resultReview

# 格納されてるレビュー結果をデータクラスに入れる
def insertreviews(info,positive,negative):
    for i in range(3):
        positive_one = positive[i]
        negative_one = negative[i]
        
        info.insertpositive(positive_one["title"],positive_one["text"])
        info.insertnegative(negative_one["title"],negative_one["text"])

#入力されたURLから結果処理に必要な情報を取得する
def reviewSelection(url):
    selectionInfo = []
    
    #商品の情報を取得する。
    overview = amazon_selection.get_product_overview(url)
    
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
    
    # サクラ判定
    all_review = sakura_jadgement.judge(all_review)
    
    #レビューのポジネガ判定とその分析を行う
    # resultReview = analysischoise(overview["o_category"],not_sakura_review)
    resultReview = analysischoise(judge,all_review)
    
    # 処理結果を処理結果クラスに挿入する
    # 商品概要の取得結果をデータクラスに挿入する
    selectionInfo = resultData.ResultData(url,overview["o_title"],overview["o_image"],totalreview,resultReview["posicnt"],
                                        resultReview["negacnt"])
    
    # レビューをデータクラスに挿入する
    insertreviews(selectionInfo,resultReview["positive"],resultReview["negative"])
    
    # ポジネガ判定の比率をデータクラスに挿入する
    selectionInfo.reviewRatio(resultReview["totalposiper"],resultReview["totalnegaper"])
    
    # Amazonreview情報をDBに書き込む
    repository.insertdb(selectionInfo)
    
    return selectionInfo