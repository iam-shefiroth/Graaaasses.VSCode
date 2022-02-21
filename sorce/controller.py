from flask import *

import service
import repository

app = Flask(__name__)

@app.route('/')
def search_top():
    return render_template("top.html")

@app.route("/search", methods=["POST"])
def search_result_db():
    
    # top.htmlから情報を取得
    url = request.form.get('searchUrl')
    
    # ↓AmazonのURlかどうか確認
    if not(checkUrl(url)):
        return render_template("top.html", errorMessage="AmazonのURLではないです。")
    
    # DB内にあるかURLを使って検索
    result = repository.selectdb(url)
    
    if(result.error == "Not Data"): # DBをチェックし該当するURLがあるか確認
        return render_template("midium.html", url = url) # 確認画面へ
    else :
        return render_template("result.html", result = result) # 結果画面へ

@app.route("/search_advance", methods=["POST"])
def search_result():
    
    # midium.htmlから情報を取得
    judge = request.form.get('judge')
    url = request.form.get('searchUrl')
    
    if(judge == "YES"): # 選択画面にて「はい」が選択された場合
        
        # スクレイピングを利用しAmazonreview情報を取得する
        result = service.reviewSelection(url)
    
        # 上手く情報を取得できたか確認
        if(result.error != ''):
            return render_template("top.html", errorMessage=result.error)
        else:
            return render_template("result.html", result = result) # 結果画面へ
    else: # 選択画面にて「いいえ」が選択された場合
        return render_template("top.html") # トップ画面へ
    

def checkUrl(url):
    return url.startswith('https://www.amazon.co.jp/')

if __name__ == '__main__':
    app.run(port=80, debug="true")