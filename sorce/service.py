from flask import *
import cv2
import matplotlib.pyplot as plt

import resultData
import amazon_selection

#テスト用データ（後に消します）
testname = "マリオカート"
#↓要パス変更
testimg = cv2.imread("z:/UserProfile/s20193085/Desktop/data/etc/mariokart8dx_test.jpg")
testimg = cv2.cvtColor(testimg, cv2.COLOR_BGR2RGB)
testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%8[…]ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
testposi1 = "このゲームは素晴らしいです。"
testposi2 = "操作性も良くて神ゲー"
testposi3 = "子供がよく遊んでます。"
testnega1 = "ワルイージしかいないマリオカートだったので売りました。"
testnega2 = "打開しないと勝てないしアイテム運ゲーで明暗を分けるクソゲーなので捨てました。"
testnega3 = "Сука, Блядь, бля, блять, черепашки, недорезанные!!!!"
testposiper = 67
testnegaper = 33

#入力されたURLから結果処理に必要な情報を取得する
def reviewSelection(url):
    
    #商品の情報を取得する。
    
    #レビューのスクレイピングを取得する
    
    #レビューのポジネガ判定
    
    #取得結果を配列に挿入する
    selectionInfo = resultData.ResultData()
    #処理結果を処理結果クラスに挿入する（試験用テストを使用中、消してね）
    selectionInfo.overviewInsert(testurl,testname,testimg,testposiper,testnegaper)
    selectionInfo.positiveInsert(testposi1)
    selectionInfo.positiveInsert(testposi2)
    selectionInfo.positiveInsert(testposi3)
    selectionInfo.negativeInsert(testnega1)
    selectionInfo.negativeInsert(testnega2)
    selectionInfo.negativeInsert(testnega3)
    
    return selectionInfo

#テスト用受け渡し※後に消せ
if __name__ == '__main__':
    selection = reviewSelection(testurl)
    plt.imshow(selection.img)
    plt.show()
    print(selection.name)