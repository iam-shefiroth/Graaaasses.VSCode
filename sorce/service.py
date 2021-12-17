from flask import *
import cv2
import matplotlib.pyplot as plt
import time

import resultData
import amazon_selection

#テスト用データ※後に消せ
testname = "マリオカート"
#↓要パス変更
testimg = cv2.imread("z:/UserProfile/s20193085/Desktop/data/etc/mariokart8dx_test.jpg")
testimg = cv2.cvtColor(testimg, cv2.COLOR_BGR2RGB)
# ロボット扱いにされた場合、使う
# testurl = "z:/UserProfile/s20193085/Desktop/data/check/Amazon.co.jp_ スーパーマリオ 3Dワールド + フューリーワールド_オンラインコード版 _ ゲーム.html"
# ロボット扱いにされてない場合、使う
testurl = "https://www.amazon.co.jp/%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4%E3%83%8A%E3%83%A0%E3%82%B3%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%86%E3%82%A4%E3%83%B3%E3%83%A1%E3%83%B3%E3%83%88-%E3%80%90PS4%E3%80%91%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%AA%E3%83%83%E3%83%88%E3%82%B7%E3%83%BC%E3%82%BA%E3%83%B3%E3%80%90%E6%97%A9%E6%9C%9F%E8%B3%BC%E5%85%A5%E7%89%B9%E5%85%B8%E3%80%91%E8%A1%A3%E8%A3%85DLC%E3%80%8E%E6%9A%81%E3%81%AE%E3%82%86%E3%81%8B%E3%81%9F%E3%80%8F%E3%81%8C%E5%85%A5%E6%89%8B%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E3%82%B3%E3%83%BC%E3%83%89-%E5%B0%81%E5%85%A5/dp/B08W5S54P1/ref=sr_1_7?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&keywords=%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC&qid=1639620405&sr=8-7"
testposi1 = "このゲームは素晴らしいです。"
testposi2 = "操作性も良くて神ゲー"
testposi3 = "子供がよく遊んでます。"
testnega1 = "ワルイージしかいないマリオカートだったので売りました。"
testnega2 = "打開しないと勝てないしアイテム運ゲーで明暗を分けるクソゲーなので捨てました。"
testnega3 = "Сука, Блядь, бля, блять, черепашки, недорезанные!!!!"
testposiper = 0.35
testnegaper = 0.7

# 処理時間を出力する（検証用）※後に消せ
def resultTime(resultTimer):
    print("Amazon商品取得時間：{}".format(resultTimer[1] - resultTimer[0]))
    print("全レビュー取得時間：{}".format(resultTimer[2] - resultTimer[1]))
    print("総合時間：{}".format(resultTimer[2] - resultTimer[0]))
    

#入力されたURLから結果処理に必要な情報を取得する
def reviewSelection(url):
    resultTimer = []
    resultTimer.append(time.perf_counter())
    #商品の情報を取得する。
    overview = amazon_selection.get_product_overview(url)
    print(overview)
    resultTimer.append(time.perf_counter())
    
    # スクレイピングブロックされてないか確認
    if(overview[1] == None):
        return None
    
    #レビューのスクレイピングを取得する
    all_review = amazon_selection.get_all_reviews(overview[4])
    print(all_review)
    resultTimer.append(time.perf_counter())
    #レビューのポジネガ判定
    
    #取得結果を配列に挿入する
    selectionInfo = resultData.ResultData()
    #処理結果を処理結果クラスに挿入する（試験用テストを使用中、消してね）
    selectionInfo.overviewInsert(overview[0],overview[1],overview[2])
    selectionInfo.positiveInsert(testposi1)
    selectionInfo.positiveInsert(testposi2)
    selectionInfo.positiveInsert(testposi3)
    selectionInfo.negativeInsert(testnega1)
    selectionInfo.negativeInsert(testnega2)
    selectionInfo.negativeInsert(testnega3)
    selectionInfo.reviewRatio(testposiper,testnegaper)
    
    resultTime(resultTimer)
    return selectionInfo

#テスト用受け渡し※後に消せ
if __name__ == '__main__':
    selection = reviewSelection(testurl)
    print(selection.img)
    print(selection.name)
    print(selection.url)
    for i in range(len(selection.positive)):
        print(selection.positive[i])
        print(selection.negative[i]) 
    print(selection.posiReviewRatio)
    print(selection.negaReviewRatio)