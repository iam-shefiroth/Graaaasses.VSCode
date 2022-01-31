from os import error
from re import A
from typing import Text
from flask import *
import time

import resultData
import amazon_selection_oono
import gamesoftAI_oono
import kuutyoukadenAI_oono
import repository
None


# ロボット扱いにされてない場合、使う
testurl = "https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E7%A9%BA%E6%B0%97%E6%B8%85%E6%B5%84%E6%A9%9F%E3%80%90%E5%8A%A0%E6%B9%BF%E6%A9%9F%E8%83%BD%E4%BB%98%E3%80%91%EF%BC%88%E7%A9%BA%E6%B8%8523%E7%95%B3%E3%81%BE%E3%81%A7-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88%E7%B3%BB%EF%BC%89SHARP-%E3%80%8C%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC7000%E3%80%8D%E6%90%AD%E8%BC%89-KC-L50-W/dp/B07Z8PRD4W/ref=sr_1_1?pd_rd_r=6c787daa-4e8e-494c-aad3-b77016f532e6&pd_rd_w=WiR2i&pd_rd_wg=PHcd0&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=AR75ZKJY9ENZTPPHQG1Q&qid=1643243957&refinements=p_72%3A82417051&s=kitchen&sr=1-1&th=1"
# testurl = "https://www.amazon.co.jp/%E3%83%9E%E3%83%AA%E3%82%AA-%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF-%E6%9D%B1%E4%BA%AC2020%E3%82%AA%E3%83%AA%E3%83%B3%E3%83%94%E3%83%83%E3%82%AF-%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%82%B9-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/dp/B09MZ6YQG5/ref=sr_1_6?crid=64D3261VWMSR&keywords=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF&qid=1640050427&s=videogames&sprefix=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%A2%E3%83%B3%E3%83%89%2Cvideogames%2C399&sr=1-6"

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
    
    return check

# 商品のジャンル次第で分析するファイルを選ぶ
def analysischoise(category,allreview):
    resultReview = ""
    if(category == "ゲームソフト"):
        resultReview = gamesoftAI_oono.analysisreview(allreview)
    elif category == "空調・季節家電":
        resultReview = kuutyoukadenAI_oono.analysisreview(allreview)
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
    overview = amazon_selection_oono.get_product_overview(url)
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
    
    # サクラ判定
    # not_sakura_review = sakura_jadgement.judge(all_review)
    
    #レビューのポジネガ判定とその分析を行う
    # resultReview = analysischoise(overview["o_category"],not_sakura_review)
    resultReview = analysischoise(judge,all_review)
    resultTimer.append(time.perf_counter())

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
    
    resultTime(resultTimer)
    return selectionInfo

#テスト用受け渡し※後に消せ
if __name__ == '__main__':
    selection = reviewSelection(testurl)
    # print(selection.img)
    # print(selection.name)
    # print(selection.url)
    # for i in range(len(selection.positive)):
    #     print(selection.posititle[i])
    #     print(selection.positive[i])
    #     print(selection.negatitle[i])
    #     print(selection.negative[i])
    
    # print(selection.posiReviewRatio)
    # print(selection.negaReviewRatio)
    # print(selection.totalcount)
    # print(selection.posicount)
    # print(selection.negacount)