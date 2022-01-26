from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from pandas import Series
from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import ExtractAttributeFilter, POSKeepFilter, TokenFilter,LowerCaseFilter,CompoundNounFilter
import pandas
import csv
import re
import neologdn
#windows(chromedriver.exeのパスを設定)
# chrome_path = r'z:\UserProfile\s20192087\Desktop\etc\chromedriver.exe'

#インポート時は実行されないように記載
if __name__ == '__main__':
     
    #　Amzon商品ページ
    review_list = []
    for i in range(16):
        csv_file = open(r'z:\UserProfile\s20192087\Desktop\etc\reviewData{0}.csv'.format(i), "r", encoding="ms932", errors="", newline="" )
        #リスト形式
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        a = 0
        b = 0
        for row in f:
            if row[0] == "5つ星のうち5.0":
                row[0] = "ポジ"
                normalized_text = neologdn.normalize(row[1])
                # tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', normalized_text)
                # text_replaced_number = re.sub(r'\d+', '0', tmp)
                tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)
                text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
                if len(text_removed_symbol) > 80:
                    article = {
                        "label": row[0],
                        "text": text_removed_symbol,
                    }
                    a += 1
                    review_list.append(article) 
            elif row[0] == "5つ星のうち4.0":
                row[0] = "ポジ"
                normalized_text = neologdn.normalize(row[1])
                # tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', normalized_text)
                # text_replaced_number = re.sub(r'\d+', '0', tmp)
                tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)
                text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
                if len(text_removed_symbol) > 80:
                    article = {
                        "label": row[0],
                        "text": text_removed_symbol,
                    }
                    a += 1
                    review_list.append(article) 
            elif row[0] == "5つ星のうち2.0":
                row[0] = "ネガ"
                normalized_text = neologdn.normalize(row[1])
                # tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', normalized_text)
                # text_replaced_number = re.sub(r'\d+', '0', tmp)
                tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)
                text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
                if len(text_removed_symbol) > 1:
                    article = {
                        "label": row[0],
                        "text": text_removed_symbol,
                    }
                    b += 1
                    review_list.append(article) 
            elif row[0] == "5つ星のうち1.0":
                row[0] = "ネガ"
                normalized_text = neologdn.normalize(row[1])
                # tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', normalized_text)
                # text_replaced_number = re.sub(r'\d+', '0', tmp)
                tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)
                text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
                if len(text_removed_symbol) > 1:
                    article = {
                        "label": row[0],
                        "text": text_removed_symbol,
                    }
                    b += 1
                    review_list.append(article) 

        csv_file.close()
    
    dataset = pandas.DataFrame(review_list)
    filtered_by_label = dataset.query("label == 'ポジ' | label == 'ネガ'")
    group_by_label = filtered_by_label.groupby("label")
    labels_size = group_by_label.size()
    print(labels_size)
    
    
    label_vectorizer = LabelEncoder()
    #数合わせ
    n = labels_size.min()
    dataset = group_by_label.apply(lambda x: x.sample(n, random_state=0))
    transformed_label = label_vectorizer.fit_transform(dataset.get("label"))
    dataset["label"] = transformed_label
    # 入力と出力に分割
    x, y = dataset.get("text"), dataset.get("label")
    # 学習とテストデータに9:1で分割
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=0)
    # それぞれの数があっているか確認
    print([len(c) for c in [X_train, X_test, y_train, y_test]])

    # tokenizer = Tokenizer(wakati=True)
    # feature_vectorizer = CountVectorizer(binary=True, analyzer=tokenizer.tokenize)
    # # 学習
    # classifier = LogisticRegression()
    # transformed_X_train = feature_vectorizer.fit_transform(X_train)
    # classifier.fit(transformed_X_train, y_train)

    # vectorized = feature_vectorizer.transform(X_test)
    # y_pred = classifier.predict(vectorized)
    # print(classification_report(y_test, y_pred,target_names=label_vectorizer.classes_))

    # feature_to_weight = dict()
    # for w, name in zip(classifier.coef_[0], feature_vectorizer.get_feature_names()):
    #     feature_to_weight[name] = w
    # se = Series(feature_to_weight)
    # se.sort_values(ascending=False, inplace=True)
    # print("Positive or Negative")
    # print("--Positiveの判定に効いた素性")
    # print(se[:20])
    # print("--Negativeの判定に効いた素性")
    # print(se[-20:])
    # print("--" * 50)

    class NumericReplaceFilter(TokenFilter):
        def apply(self, tokens):
            tmp = ""
            for i,token in enumerate(tokens):
                parts = token.part_of_speech.split(',')
                if parts[0] == '助動詞' and token.base_form == 'ない' and (tmp.part_of_speech.split(',')[0] == '動詞' or tmp.part_of_speech.split(',')[0] == '形容詞'):
                    tmp2 = token
                    token = tmp
                    token.base_form = tmp.surface + tmp2.base_form
                    token.surface = tmp.surface + tmp2.base_form
                    token.reading = tmp.reading + tmp2.reading
                    token.phonetic = tmp.phonetic + tmp2.phonetic
                    tmp = token
                else:
                    if tmp == "":
                        tmp = token
                    else:
                        if tmp.part_of_speech.split(',')[0] != '助動詞':
                            yield tmp
                        tmp = token
                    

    def validate():
        # 学習
        classifier = LogisticRegression()
        transformed_X_train = feature_vectorizer.fit_transform(X_train)
        classifier.fit(transformed_X_train, y_train)
        # 評価
        vectorized = feature_vectorizer.transform(X_test)
        y_pred = classifier.predict(vectorized)
        print(classification_report(y_test, y_pred))
        # モデルのダンプ
        feature_to_weight = dict()
        for w, name in zip(classifier.coef_[0], feature_vectorizer.get_feature_names()):
            feature_to_weight[name] = w
        se = Series(feature_to_weight)
        se.sort_values(ascending=False, inplace=True)
        print("--Positiveの判定に効いた素性")
        print(se[:50])
        print("--Negativeの判定に効いた素性")
        print(se[-50:])
        print("--" * 50)
        with open(r'z:\UserProfile\s20192087\Desktop\etc\review_weight.csv','w', encoding='CP932', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            # 全データを表示
            for k,v in se.items():
                csvlist=[]
                #データ作成
                csvlist.append(k)
                csvlist.append(v)
                writer.writerow(csvlist)
            # ファイルクローズ
            f.close()

        return y_pred
    
    # 前処理
    char_filters = [
        RegexReplaceCharFilter("(https?:\/\/[\w\.\-/:\#\?\=\&\;\%\~\+]*)", ""),
        RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ''),
        RegexReplaceCharFilter('おもしろい', '面白い'),
        RegexReplaceCharFilter('おもしろくない', '面白くない'),
        RegexReplaceCharFilter('たのしい', '楽しい')]
    # 後処理
    token_filters = [
        POSKeepFilter(['名詞', '動詞', '形容詞', '副詞', '助動詞']),
        LowerCaseFilter(),
        NumericReplaceFilter(),
        # CompoundNounFilter(),
        ExtractAttributeFilter("base_form")]
    # Tokenizerの再初期化
    tokenizer = Tokenizer()
    # 前処理・後処理が追加されたVectorizerに変更
    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
    feature_vectorizer = CountVectorizer(binary=True, analyzer=analyzer.analyze)
    # 再評価
    result = validate()
    #　検証用のDataFrameを作成
    validate_df = pandas.concat([X_test, y_test], axis=1)
    validate_df["y_pred"] = result
    # 予測とラベルが異なるものを抽出
    false_positive = validate_df.query("y_pred == 1 & label == 0")
    print(false_positive)
    print("--" * 50)
    false_negative = validate_df.query("y_pred == 0 & label == 1")
    print(false_negative)