from flask import *
from PIL import Image
from dataclasses import dataclass

from sorce.resultData import resultData

#テスト用（後に消します）
testname = "マリオカート"
#↓要パス変更
testimg = Image.open("z:\UserProfile\s20193085\Desktop\data\etc\mariokart8dx_test.jpg")
testurl = "https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%9E%E3%83%AA%E3%82%AA%E3%8[…]ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
testposi1 = "このゲームは素晴らしいです。"
testposi2 = "操作性も良くて神ゲー"
testposi3 = "子供がよく遊んでます。"
testnega1 = "ワルイージしかいないマリオカートだったので売りました。"
testnega2 = "打開しないと勝てないしアイテム運ゲーで明暗を分けるクソゲーなので捨てました。"
testnega3 = "Сука, Блядь, бля, блять, черепашки, недорезанные!!!!"

def reviewSelection(url):
    
    selectionInfo = resultData.overviewInsert(testurl,testname,testimg)
    selectionInfo += resultData.overviewInsert(testposi1)
    return selectionInfo