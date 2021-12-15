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
testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%81%82%E3%81%A4%E3%81%BE%E3%82%8C-%E3%81%A9%E3%81%86%E3%81%B6%E3%81%A4%E3%81%AE%E6%A3%AE-%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%89%E7%89%88/dp/B084H8S45Q/ref=pd_rhf_cr_s_pd_crcd_1/355-8689788-2301132?pd_rd_w=TRTBY&pf_rd_p=6bd17f5e-1bac-4f3b-97c7-064c882625e5&pf_rd_r=HKQ6JVHAWKK4JGD61V3V&pd_rd_r=8eb328d6-fa31-44bc-b334-9e840202ee68&pd_rd_wg=vDQ72&pd_rd_i=B084H8S45Q&psc=1"
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
    overview = amazon_selection.get_product_overview(url)
    print(overview)
    #レビューのスクレイピングを取得する
    all_review = amazon_selection.get_all_reviews(overview[4])
    #レビューのポジネガ判定
    
    #取得結果を配列に挿入する
    selectionInfo = resultData.ResultData()
    #処理結果を処理結果クラスに挿入する（試験用テストを使用中、消してね）
    selectionInfo.overviewInsert(overview[0],overview[1],overview[2],testposiper,testnegaper)
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
    for i in selection:
        print(i)