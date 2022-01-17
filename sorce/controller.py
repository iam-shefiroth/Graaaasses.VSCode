from flask import *

import reviewData
import resultData
import time
#import service

app = Flask(__name__)

@app.route('/')
def search_top():
    return render_template("top.html")

@app.route("/search", methods=["POST"])
def search_result_db():
    url = request.form.get('searchUrl')
    
    if not(checkUrl(url)):
        return render_template("top.html", errorMessage="AmazonのURLではないです。")
    
    if(False): # DBをチェックし該当するURLあり
        result = null # DBからデータを引っ張ってくる
        return render_template("result.html", result = result) # 結果画面へ
    else :
        return render_template("midium.html", url = url) # 確認画面へ
        

@app.route("/search_advance", methods=["POST"])
def search_result():
    
    judge = request.form.get('judge')
    url = request.form.get('searchUrl')
    
    if(judge == "YES"): # 選択画面にて「はい」が選択された場合
        print("YESです")# 消していいです
        
        #result = service.reviewSelection(url)
    
        # 上手く情報を取得できたか確認
        #if(result.error != ''):
            #return render_template("top.html", errorMessage=result.error)
        # result = sampleResult()
        #print("{}".format(result.posiReviewRatio))
        return render_template("result.html", result = sampleResult()) # 結果画面へ
    else: # 選択画面にて「いいえ」が選択された場合
        print("NOです") # 消していいです
        return render_template("top.html") # トップ画面へ
    

def checkUrl(url):
    return url.startswith('https://www.amazon.co.jp/')

def sampleResult():
        result = resultData.ResultData()
        result.url = "https://www.amazon.co.jp/%E3%83%AA%E3%83%A5%E3%82%A6%E3%82%B8%E5%BC%8F%E8%87%B3%E9%AB%98%E3%81%AE%E3%83%AC%E3%82%B7%E3%83%94-%E4%BA%BA%E7%94%9F%E3%81%A7%E3%81%84%E3%81%A1%E3%81%B0%E3%82%93%E7%BE%8E%E5%91%B3%E3%81%97%E3%81%84-%E5%9F%BA%E6%9C%AC%E3%81%AE%E6%96%99%E7%90%86100-%E3%83%AA%E3%83%A5%E3%82%A6%E3%82%B8/dp/4909044345/ref=cm_cr_arp_d_product_top?ie=UTF8"
        result.name = "リュウジ式至高のレシピ 人生でいちばん美味しい! 基本の料理100"
        result.img = "https://images-na.ssl-images-amazon.com/images/I/51MXlJyFGiL._SX393_BO1,204,203,200_.jpg"
        posi_rev1 = reviewData.ReviewData("楽しすぎる", "邪道！！こんなの知らない！！ええっ！？美味い！！リュウジさんの味、とても口に合う。動画は見るのが面倒だった私だけど、目から鱗のコツが多くて動画も載ってるのありがたい。ただしまず酒を作るクセがついた。しばらく楽しめそう。さぁ今日のお昼ご飯を選ぼう。わくわく。")
        text = "料理を作っても、失敗したときはやたらと指摘されるのに上手くいっても褒められない。 そんなサイクルにモチベーションと自信を奪われていました"
        text += "でもこの本のレシピ達を見たら説明がわかりやすいし美味しそうだし、難しい工程も聞いたこともない調味料も登場しない。 読んでいくうちに久しぶりに色々な料理を作ってみたくなってしまいました。 もし誰も褒めてくれなくても美味しくできたら自分で食べてにこにこできればいいかなと思い直すことにします！"
        posi_rev2 = reviewData.ReviewData("自信がない人でもご飯を作りたくなる本",  text)
        text = "前は好きだった料理がだんだん重荷になり、外食が一番じゃん？て思うようになっていた頃、リュウジさんのレシピと料理に対する思いを見かけて、救われた気持ちになりました。 簡単で美味しくて、そして誰かのために料理作ってえらい！と言ってくれるリュウジさんのレシピは素晴らしいです。 "
        text += " 至高のレシピは他のリュウジさんレシピの中では手間がかかりますが、わかりやすく書いてくれてるし、動画もあるので見ながらやれば大丈夫！ 味見をして、え、こんな味になったんだ！うま！て毎回なります。 作って損はないレシピばかり！おすすめです＾＾ ついでに後書きで思いがけず泣いてしまいました（笑）"
        posi_rev3 = reviewData.ReviewData("楽しく料理！！", text)
        result.positive = [posi_rev1, posi_rev2, posi_rev3]
        text = "一つの料理につき、料理の完成図で１ページ＋画像入りのレシピで１ページにまとめているが、レシピが3〜4手順しか載っておらず、おまけにB5サイズ本なので情報量が少なく、料理初心者はこの本だけでは作れないと思う。だとすると動画を見た方が手順の説明が丁寧で更に面白くてよいのだが、そうすると本にした意味がない。"
        text += " 一方で、ある程度料理ができる人は、このレシピの情報量でも料理を作れるが、レシピ自体にはさほど新規性はないので、これくらいの料理はすでに習得してるので読む必要性が低い。 動画の補足本にしたいなら、とことん画像は少なくして、動画で伝えきれない細かいレシピやコツをふんだんに書いてほしい。"
        text += " 逆に、本の補足を動画で行いたいのであれば、どの部分を動画で見てほしいのか（火の入れ方、切り方、混ぜ方など）を本に書いてほしい。初心者だと、全部わからなくて、全手順を動画で見るハメになり、本の意味がなくなる。 以上から、本にする意味はなかった気がする。"
        text += "あと、レシピの説明が普通すぎて、リュウジさん色が全然出てないので、動画からリュウジさんのファンになった人には面白くないと思う。マスコットキャラの一言がもっとあればよかったのに。 また、QRコードは章末にまとめるメリットはゼロ。各レシピのページに貼り付けてほしかった。もっと言えばレシピの中で、動画で見てほしい部分について、画像の横にQRコードを読み取ればその動画の該当部分に飛ぶ仕組みにしてほしかった。"
        nega_rev1 = reviewData.ReviewData("本にする意味はなかった気がする", text)
        nega_rev2 = reviewData.ReviewData("リュウジさんの想いがつまった一冊", "Youtubeでもいつもお世話になっています。社会人になって一人暮らしをはじめて、リュウジさんのレシピにどれだけ助けられたか。ただのレシピ本ってだけじゃなくて、リュウジさんの想いに触れて心もほっこりする、そんな一冊です。")
        nega_rev3 = reviewData.ReviewData("レシピは最高", "レシピは何度も作っているものも多く、この本で解禁のレシピも至高を謳っているからにはまず間違いなく美味しい(味濃いめな傾向はあるけど)ので安心して予約購入しました。手元に届いて惜しいと思ったのは、巻末に材料別インデックスが付いてなかったことくらいです。徹頭徹尾リュウジ節がきいててページをめくっているだけでも楽しいです。いつか全レシピ制覇したいと思います！")
        result.negative = [nega_rev1, nega_rev2, nega_rev3]
        result.reviewRatio(1096, 847)

        return result
# 
if __name__ == '__main__':
    app.run(port=80, debug="true")