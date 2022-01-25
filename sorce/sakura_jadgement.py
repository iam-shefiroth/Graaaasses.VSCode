import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
import csv

# サクラレビューか判定する
# 使用時はAnacondaのプロンプトにて「install transformers==4.10.2 fugashi==1.1.0 ipadic==1.0.0 pytorch-lightning==1.2.7」を入力してください
# また、slackにアップしたモデルをダウンロードし、sorceフォルダ内に配置してください
def judge(all_review):
    
    # 日本語の事前学習モデル
    modelName = 'cl-tohoku/bert-base-japanese-whole-word-masking'
    # AI判定のモデルをロード
    bert_sc = BertForSequenceClassification.from_pretrained(
        r'sorce\AI_model\model_transformers'
    )
    
    # エンコード用のリストを作成
    sakura = []
    for review in all_review:
        sakura.append(str(review['dateResult']) + "," + str(review['star']) + "," + review['text']) # "日数差,評価,本文"の形式
    tokenizer = BertJapaneseTokenizer.from_pretrained(modelName) # トークナイザのロード
    # エンコード実行
    encoding = tokenizer(
        sakura,
        max_length=512,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    # 推論
    with torch.no_grad():
        output = bert_sc(**encoding)
    # 推論の結果取得
    scores = output.logits
    # 各本文の判定結果を取得、リスト化
    labels_predicted = scores.argmax(-1).tolist()
    
    # 判定結果と照らし合わせサクラレビューを排除
    result_all_review = []
    for i in range(len(sakura)):
        if labels_predicted[i] <= 0: # サクラレビューの判定が下されていない場合、戻り値の配列に格納する
            result_all_review.append(all_review[i])
    return result_all_review