from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
 
#windows(chromedriver.exeのパスを設定)
chrome_path = r'z:\UserProfile\s20192087\Desktop\etc\chromedriver.exe'
 
#mac
#chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'
 
#　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与
    #　chromedriverのパスとパラメータを設定
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=chrome_path,options=options)
    driver.get(url)                         #　chromeブラウザでurlを開く
    driver.implicitly_wait(10)              #　指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source               #　ページ情報を取得
    
    driver.quit()                           #　chromeブラウザを閉じる
    
    return text                             #　取得したページ情報を返す
 
# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        stars  = amazon_bs.select('a.a-link-normal span.a-icon-alt')
        
        for j in range(len(stars)):
            article = {
            "text": reviews[j].text.replace("\n", "").replace("\u3000", ""),
            "label": stars[j].text,
            }
            review_list.append(article)                      #　レビュー情報をreview_listに格納

             
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする

            sleep(3)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list
 
#インポート時は実行されないように記載
if __name__ == '__main__':
     
    urls = []
    # スイッチ
    #スマブラ マリオカートDX pokemon剣盾 スプラ
    #ペルソナ sekiro BF 仁王2
    # あつもり ドラクエ ゼルダ 桃鉄

    # 空気清浄機
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E7%A9%BA%E6%B0%97%E6%B8%85%E6%B5%84%E6%A9%9F%E3%80%90%E5%8A%A0%E6%B9%BF%E6%A9%9F%E8%83%BD%E4%BB%98%E3%80%91%EF%BC%88%E7%A9%BA%E6%B8%8523%E7%95%B3%E3%81%BE%E3%81%A7-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88%E7%B3%BB%EF%BC%89SHARP-%E3%80%8C%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC7000%E3%80%8D%E6%90%AD%E8%BC%89-KC-L50-W/dp/B07Z8PRD4W/ref=lp_4083011_1_1?th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E7%A9%BA%E6%B0%97%E6%B8%85%E6%B5%84%E6%A9%9F%E3%80%90%E5%8A%A0%E6%B9%BF%E6%A9%9F%E8%83%BD%E4%BB%98%E3%80%91%EF%BC%88%E7%A9%BA%E6%B8%8531%E7%95%B3%E3%81%BE%E3%81%A7-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88%E7%B3%BB%EF%BC%89SHARP-%E3%80%8C%E9%AB%98%E6%BF%83%E5%BA%A6%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC25000%E3%80%8D%E6%90%AD%E8%BC%89-KI-LS70-W/dp/B07Z8PNXYH/ref=lp_4083011_1_2?th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E5%8A%A0%E6%B9%BF%E7%A9%BA%E6%B0%97%E6%B8%85%E6%B5%84%E6%A9%9F-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC%E6%90%AD%E8%BC%89-KC-F70-W-FZ-Y80MF/dp/B01M2Y6RSE/ref=lp_4083011_1_3')
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC-%E3%83%8A%E3%82%A4%E3%83%88%E3%83%A9%E3%82%A4%E3%83%88%E4%BB%98-2021%E5%B9%B4%E3%83%A2%E3%83%87%E3%83%AB-FU-NC01-W/dp/B08QVLMKF1/ref=lp_4083011_1_5?th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E9%99%A4%E5%8A%A0%E6%B9%BF%E7%A9%BA%E6%B0%97%E6%B8%85%E6%B5%84%E6%A9%9F-SHARP-%E3%80%8C%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC25000%E3%80%8D%E6%90%AD%E8%BC%89-KI-LD50-W/dp/B0876MZ6RY/ref=lp_4083011_1_7')
    
    # 電気毛布
    # urls.append('https://www.amazon.co.jp/%E5%B0%8F%E6%B3%89-%E3%82%B3%E3%82%A4%E3%82%BA%E3%83%9F-KDS-4092-%E9%9B%BB%E6%B0%97%E6%95%B7%E6%AF%9B%E5%B8%83/dp/B081GLKDQ1/ref=sr_1_1?pd_rd_r=fc3d690d-0c0e-4485-8327-a943c9480e66&pd_rd_w=HD6n2&pd_rd_wg=icwwg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0TE5SJWVM9QA0WHKPJ5S&qid=1642986634&refinements=p_72%3A82417051&s=kitchen&sr=1-1')
    # urls.append('https://www.amazon.co.jp/%E5%B1%B1%E5%96%84-%E6%B4%97%E3%81%88%E3%82%8B%E3%81%A9%E3%81%93%E3%81%A7%E3%82%82%E3%82%AB%E3%83%BC%E3%83%9A%E3%83%83%E3%83%88-180%C3%9780cm-%E3%83%95%E3%83%A9%E3%83%B3%E3%83%8D%E3%83%AB%E4%BB%95%E4%B8%8A%E3%81%92-YWC-182F/dp/B01LX90CJ2/ref=sr_1_4?pd_rd_r=fc3d690d-0c0e-4485-8327-a943c9480e66&pd_rd_w=HD6n2&pd_rd_wg=icwwg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0TE5SJWVM9QA0WHKPJ5S&qid=1642986801&refinements=p_72%3A82417051&s=kitchen&sr=1-4')
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-IRIS-OHYAMA-HW-HC-C-%E3%83%92%E3%83%BC%E3%83%88%E3%82%AF%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3/dp/B08XBGHFGJ/ref=sr_1_3?pd_rd_r=fc3d690d-0c0e-4485-8327-a943c9480e66&pd_rd_w=HD6n2&pd_rd_wg=icwwg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0TE5SJWVM9QA0WHKPJ5S&qid=1642986801&refinements=p_72%3A82417051&s=kitchen&sr=1-3&th=1')
    # urls.append('https://www.amazon.co.jp/Sugiyama-%E3%80%90%E6%B0%B4%E6%B4%97%E3%81%84OK%E3%80%91-%E6%95%B7%E3%81%8D%E6%AF%9B%E5%B8%83-140%C3%9780cm-NA-023S/dp/B005HMMBYE/ref=sr_1_8?pd_rd_r=fc3d690d-0c0e-4485-8327-a943c9480e66&pd_rd_w=HD6n2&pd_rd_wg=icwwg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0TE5SJWVM9QA0WHKPJ5S&qid=1642986801&refinements=p_72%3A82417051&s=kitchen&sr=1-8')
    # urls.append('https://www.amazon.co.jp/%E6%A4%99%E5%B1%B1%E7%B4%A1%E7%B9%94-NA-013K-Sugiyama-%E9%9B%BB%E6%B0%97%E6%8E%9B%E6%95%B7%E5%85%BC%E7%94%A8%E6%AF%9B%E5%B8%83/dp/B005HMMC0M/ref=sr_1_19?pd_rd_r=fc3d690d-0c0e-4485-8327-a943c9480e66&pd_rd_w=HD6n2&pd_rd_wg=icwwg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0TE5SJWVM9QA0WHKPJ5S&qid=1642986801&refinements=p_72%3A82417051&s=kitchen&sr=1-19')
    
    #電気暖房
    # urls.append('https://www.amazon.co.jp/%E3%83%87%E3%83%AD%E3%83%B3%E3%82%AE-DeLonghi-%E3%83%B4%E3%82%A7%E3%83%AB%E3%83%86%E3%82%A3%E3%82%AB%E3%83%AB%E3%83%89-%E3%82%AB%E3%83%A2%E3%83%9F%E3%83%BC%E3%83%AB%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88-RHJ21F0812-WH/dp/B09BTRQNZ9/ref=sr_1_1?pd_rd_r=ba064f90-8e63-4a92-9607-0fb25d8eb0d4&pd_rd_w=Wfl6R&pd_rd_wg=8yXuj&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0K2ZMHPJ3YXSNH2350R4&qid=1642991183&refinements=p_72%3A82417051&s=kitchen&sr=1-1&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%BB%E3%83%A9%E3%83%9F%E3%83%83%E3%82%AF%E3%83%95%E3%82%A1%E3%83%B3%E3%83%92%E3%83%BC%E3%82%BF%E3%83%BC-%E4%BA%BA%E6%84%9F%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E4%BB%98%E3%81%8D-%E6%8A%BC%E3%81%97%E3%83%9C%E3%82%BF%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%97-PDH-1200TD1-W/dp/B07HQT9C2J/ref=sr_1_2?pd_rd_r=ba064f90-8e63-4a92-9607-0fb25d8eb0d4&pd_rd_w=Wfl6R&pd_rd_wg=8yXuj&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0K2ZMHPJ3YXSNH2350R4&qid=1642991183&refinements=p_72%3A82417051&s=kitchen&sr=1-2&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E4%BA%BA%E6%84%9F%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E4%BB%98%E3%81%8D-%E3%82%BB%E3%83%A9%E3%83%9F%E3%83%83%E3%82%AF%E3%83%95%E3%82%A1%E3%83%B3%E3%83%92%E3%83%BC%E3%82%BF%E3%83%BC-%E3%83%9E%E3%82%A4%E3%82%B3%E3%83%B3%E5%BC%8F-JCH-126T-W/dp/B07WP92J16/ref=sr_1_3?pd_rd_r=ba064f90-8e63-4a92-9607-0fb25d8eb0d4&pd_rd_w=Wfl6R&pd_rd_wg=8yXuj&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0K2ZMHPJ3YXSNH2350R4&qid=1642991183&refinements=p_72%3A82417051&s=kitchen&sr=1-3')
    # urls.append('https://www.amazon.co.jp/%E5%B1%B1%E5%96%84-%E9%9B%BB%E6%B0%97%E3%82%B9%E3%83%88%E3%83%BC%E3%83%96-%E8%BB%A2%E5%80%92OFF%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81-DS-D086-%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC%E4%BF%9D%E8%A8%BC1%E5%B9%B4/dp/B07X1JMFND/ref=sr_1_8?pd_rd_r=ba064f90-8e63-4a92-9607-0fb25d8eb0d4&pd_rd_w=Wfl6R&pd_rd_wg=8yXuj&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0K2ZMHPJ3YXSNH2350R4&qid=1642991183&refinements=p_72%3A82417051&s=kitchen&sr=1-8')
    # urls.append('https://www.amazon.co.jp/%E5%B1%B1%E5%96%84-%E9%81%A0%E8%B5%A4%E5%A4%96%E7%B7%9A%E3%82%AB%E3%83%BC%E3%83%9C%E3%83%B3%E3%83%92%E3%83%BC%E3%82%BF%E3%83%BC-2%E6%AE%B5%E9%9A%8E%E5%88%87%E6%9B%BF-%E8%87%AA%E5%8B%95%E9%A6%96%E6%8C%AF%E3%82%8A%E6%A9%9F%E8%83%BD%E4%BB%98-DC-S097/dp/B01M4FMS8I/ref=sr_1_6?pd_rd_r=ba064f90-8e63-4a92-9607-0fb25d8eb0d4&pd_rd_w=Wfl6R&pd_rd_wg=8yXuj&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=0K2ZMHPJ3YXSNH2350R4&qid=1642991183&refinements=p_72%3A82417051&s=kitchen&sr=1-6&th=1')
    
    # 加湿器
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E5%8A%A0%E6%B9%BF%E5%99%A8-%E8%B6%85%E9%9F%B3%E6%B3%A2-UTK-230-W-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88/dp/B08H5MJRCB/ref=sr_1_1?pd_rd_r=551d25dc-f787-4e22-ab71-9c268608d323&pd_rd_w=MDPT5&pd_rd_wg=1PNMe&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=XSFBWFGJE769ETPE2X04&qid=1643070744&refinements=p_72%3A82417051&s=kitchen&sr=1-1')
    # urls.append('https://www.amazon.co.jp/Yokizu-%E6%9C%9D%E3%81%BE%E3%81%A7%E9%80%A3%E7%B6%9A%E7%A8%BC%E5%83%8D-LED%E3%83%A9%E3%82%A4%E3%83%88-%E7%A9%BA%E7%84%9A%E3%81%8D%E9%98%B2%E6%AD%A2-360%C2%B0%E3%83%9F%E3%82%B9%E3%83%88%E8%AA%BF%E6%95%B4%E5%8F%AF%E8%83%BD/dp/B07WJF7J12?ref_=Oct_d_obs_d_4082991&pd_rd_w=VtIrf&pf_rd_p=03b65386-84ce-4d82-8c83-dd9d2863fe54&pf_rd_r=XSFBWFGJE769ETPE2X04&pd_rd_r=551d25dc-f787-4e22-ab71-9c268608d323&pd_rd_wg=1PNMe&pd_rd_i=B07WJF7J12')
    # urls.append('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC-KC-F70-W-%E4%BD%BF%E3%81%84%E6%8D%A8%E3%81%A6%E3%83%97%E3%83%AC%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC-FZ-PF80K1/dp/B076RKZD59/ref=sr_1_6?pd_rd_r=551d25dc-f787-4e22-ab71-9c268608d323&pd_rd_w=MDPT5&pd_rd_wg=1PNMe&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=XSFBWFGJE769ETPE2X04&qid=1643070744&refinements=p_72%3A82417051&s=kitchen&sr=1-6')
    # urls.append('https://www.amazon.co.jp/KMJ-%E3%82%AA%E3%83%95%E3%82%A3%E3%82%B9-%E3%83%8A%E3%82%A4%E3%83%88%E3%83%A9%E3%82%A4%E3%83%88-%E6%AC%A1%E4%BA%9C%E5%A1%A9%E7%B4%A0%E9%85%B8%E6%B0%B4-%E5%A4%A7%E5%AE%B9%E9%87%8F360ml/dp/B08N6G596X/ref=sr_1_15?pd_rd_r=551d25dc-f787-4e22-ab71-9c268608d323&pd_rd_w=MDPT5&pd_rd_wg=1PNMe&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=XSFBWFGJE769ETPE2X04&qid=1643070744&refinements=p_72%3A82417051&s=kitchen&sr=1-15&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%80%90%E4%BB%A4%E5%92%8C%E6%9C%80%E6%96%B0%E3%83%A2%E3%83%87%E3%83%AB%E3%80%91-Levoit-%E3%82%B9%E3%83%9E%E3%83%BC%E3%83%88%E3%81%8A%E3%82%84%E3%81%99%E3%81%BF%E3%83%A2%E3%83%BC%E3%83%89-%E5%99%B4%E9%9C%A7%E9%87%8F4%E6%AE%B5%E9%9A%8E%E8%AA%BF%E7%AF%80%E5%8F%AF%E8%83%BD-100/dp/B086PTWHVB/ref=sr_1_20?pd_rd_r=551d25dc-f787-4e22-ab71-9c268608d323&pd_rd_w=MDPT5&pd_rd_wg=1PNMe&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=XSFBWFGJE769ETPE2X04&qid=1643070744&refinements=p_72%3A82417051&s=kitchen&sr=1-20&th=1')
    
    # かいろ
    # urls.append('https://www.amazon.co.jp/%E5%85%85%E9%9B%BB%E3%83%8F%E3%83%B3%E3%83%89%E3%82%A6%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%BC-14%E6%99%82%E9%96%93%E9%80%A3%E7%B6%9A%E7%99%BA%E7%86%B1-9000mAh%E5%AE%B9%E9%87%8F-3%E9%9A%8E%E6%AE%B5%E6%B8%A9%E5%BA%A6%E8%AA%BF%E7%AF%80-USB%E8%BB%BD%E9%87%8F%E3%83%A2%E3%83%90%E3%82%A4%E3%83%AB%E3%83%90%E3%83%83%E3%83%86%E3%83%AA%E3%83%BC/dp/B08HRZJDPZ/ref=sr_1_3?pd_rd_r=c10ed2c6-6cab-4cbf-9935-825b397d7d5a&pd_rd_w=8WZ34&pd_rd_wg=QAOwl&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=ENPS2BM21TNDBY3W6638&qid=1643073746&refinements=p_72%3A82417051&s=kitchen&sr=1-3&th=1')
    # urls.append('https://www.amazon.co.jp/ZIPPO-%E3%82%B8%E3%83%83%E3%83%9D%E3%83%BC-%E3%83%8F%E3%83%B3%E3%83%89%E3%82%A6%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%BC/product-reviews/B01MZIRU3A/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
    # urls.append('https://www.amazon.co.jp/%E5%BA%83%E9%9B%BB-%E3%82%BD%E3%83%95%E3%83%88%E3%81%82%E3%82%93%E3%81%8B-%E3%83%94%E3%83%B3%E3%82%AF%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF-VWF157-PC/dp/B07HQHXT7K/ref=sr_1_5?pd_rd_r=c10ed2c6-6cab-4cbf-9935-825b397d7d5a&pd_rd_w=8WZ34&pd_rd_wg=QAOwl&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=ENPS2BM21TNDBY3W6638&qid=1643073746&refinements=p_72%3A82417051&s=kitchen&sr=1-5&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%83%91%E3%83%8A%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF-%E9%9B%BB%E6%B0%97%E3%81%82%E3%82%93%E3%81%8B-%E3%82%BD%E3%83%95%E3%83%88-%E6%A0%BC%E5%AD%90%E6%9F%84-DW-78P-H/dp/B00N1EWIRU/ref=sr_1_8?pd_rd_r=c10ed2c6-6cab-4cbf-9935-825b397d7d5a&pd_rd_w=8WZ34&pd_rd_wg=QAOwl&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=ENPS2BM21TNDBY3W6638&qid=1643073929&refinements=p_72%3A82417051&s=kitchen&sr=1-8')
    # urls.append('https://www.amazon.co.jp/%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B8%E3%83%A7%E3%82%A4-%E9%9B%BB%E6%B0%97%E3%81%82%E3%82%93%E3%81%8B-%E6%B8%A9%E5%BA%A6%E8%AA%BF%E7%AF%80%E3%81%A4%E3%81%8D-22cm%C3%9724-5cm-AY601/dp/B07FXJDH4L/ref=sr_1_10?pd_rd_r=c10ed2c6-6cab-4cbf-9935-825b397d7d5a&pd_rd_w=8WZ34&pd_rd_wg=QAOwl&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=ENPS2BM21TNDBY3W6638&qid=1643073929&refinements=p_72%3A82417051&s=kitchen&sr=1-10')
    
    # サーキュレーター
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%B5%E3%83%BC%E3%82%AD%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%83%BC-%E4%B8%8A%E4%B8%8B%E5%B7%A6%E5%8F%B3%E9%A6%96%E6%8C%AF%E3%82%8A-2019%E5%B9%B4%E3%83%A2%E3%83%87%E3%83%AB-PCF-SDC15T/dp/B07QP882VF?ref_=Oct_d_otopr_d_14157321&pd_rd_w=da37O&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=P3QMP7NMB2BD7YSXJ6AH&pd_rd_r=798fefc2-b4fa-4e69-b785-15ffcff78a1f&pd_rd_wg=ZYILg&pd_rd_i=B07QP882VF&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%80%90Amazon-co-jp-%E5%B1%B1%E5%96%84-%E3%82%B5%E3%83%BC%E3%82%AD%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%83%BC-AYC-18-%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC%E4%BF%9D%E8%A8%BC1%E5%B9%B4/dp/B08WWW154L/ref=sr_1_8?pd_rd_r=798fefc2-b4fa-4e69-b785-15ffcff78a1f&pd_rd_w=da37O&pd_rd_wg=ZYILg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=P3QMP7NMB2BD7YSXJ6AH&qid=1643072846&refinements=p_72%3A82417051&s=kitchen&sr=1-8&th=1')
    # urls.append('https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%B5%E3%83%BC%E3%82%AD%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%83%BC-%E3%83%9E%E3%83%83%E3%83%88%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3-%E3%83%91%E3%83%AF%E3%83%95%E3%83%AB%E9%80%81%E9%A2%A8-PCF-MKM15-H/dp/B08Z3C8HQC/ref=sr_1_9?pd_rd_r=798fefc2-b4fa-4e69-b785-15ffcff78a1f&pd_rd_w=da37O&pd_rd_wg=ZYILg&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=P3QMP7NMB2BD7YSXJ6AH&qid=1643072846&refinements=p_72%3A82417051&s=kitchen&sr=1-9')
    
    # ヘッドホン
    urls.append('https://www.amazon.co.jp/%E3%82%BD%E3%83%8B%E3%83%BC-SONY-MDR7506-%E3%82%B9%E3%83%86%E3%83%AC%E3%82%AA%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-MDR-7506/dp/B000AJIF4E/ref=sr_1_17?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643247563&refinements=p_72%3A82399051&s=electronics&sr=1-17')
    # urls.append('https://www.amazon.co.jp/%E3%83%9E%E3%83%BC%E3%82%B7%E3%83%A3%E3%83%AB-Marshall-%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-MAJOR-BLUETOOTH/dp/B07CDZD8B7/ref=sr_1_27?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643247776&refinements=p_72%3A82399051&s=electronics&sr=1-27')
    # urls.append('https://www.amazon.co.jp/%E3%83%8E%E3%82%A4%E3%82%BA%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AA%E3%83%B3%E3%82%B0-Bluetooth-%E8%87%AA%E5%8B%95%E3%83%9A%E3%82%A2%E3%83%AA%E3%83%B3%E3%82%B0-ANC%E3%83%8E%E3%82%A4%E3%82%BA%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AB-Srhythm/dp/B083S6Q8VK/ref=sr_1_29?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643247776&refinements=p_72%3A82399051&s=electronics&sr=1-29&th=1')
    
    # 次のやつ
    # urls.append('https://www.amazon.co.jp/Soundcore-Q30%EF%BC%88Bluetooth5-0-%E3%82%AA%E3%83%BC%E3%83%90%E3%83%BC%E3%82%A4%E3%83%A4%E3%83%BC%E5%9E%8B%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3%EF%BC%89%E3%80%90%E3%82%A2%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%83%8E%E3%82%A4%E3%82%BA%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AA%E3%83%B3%E3%82%B0-NFC%E3%83%BBBluetooth%E5%AF%BE%E5%BF%9C-%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3%E3%80%91%E3%83%96%E3%83%A9%E3%83%83%E3%82%AF/dp/B08HYX5NS9/ref=sr_1_1?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-1')
    # urls.append('https://www.amazon.co.jp/%E3%82%BD%E3%83%8B%E3%83%BC-%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%83%8E%E3%82%A4%E3%82%BA%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AA%E3%83%B3%E3%82%B0%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-WH-1000XM4-Bluetooth-%E6%9C%80%E5%A4%A730%E6%99%82%E9%96%93%E9%80%A3%E7%B6%9A%E5%86%8D%E7%94%9F/dp/B08F2866Q3/ref=sr_1_2?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-2')
    # urls.append('https://www.amazon.co.jp/%E3%80%90Amazon-co-jp-%E9%99%90%E5%AE%9A%E3%80%91%E3%82%BC%E3%83%B3%E3%83%8F%E3%82%A4%E3%82%B6%E3%83%BC-%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-SE%E3%80%90%E5%9B%BD%E5%86%85%E6%AD%A3%E8%A6%8F%E5%93%81%E3%80%91-508697/dp/B07Q7S7247/ref=sr_1_7?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-7')
    # urls.append('https://www.amazon.co.jp/Soundcore-Q10%EF%BC%88Bluetooth-%E3%82%AA%E3%83%BC%E3%83%90%E3%83%BC%E3%82%A4%E3%83%A4%E3%83%BC%E5%9E%8B%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3%EF%BC%89%E3%80%90%E3%83%8F%E3%82%A4%E3%83%AC%E3%82%BE%E5%AF%BE%E5%BF%9C-%E6%9C%80%E5%A4%A760%E6%99%82%E9%96%93%E9%9F%B3%E6%A5%BD%E5%86%8D%E7%94%9F-USB-C%E5%85%85%E9%9B%BB/dp/B07WYYJNKX/ref=sr_1_6?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-6')
    # urls.append('https://www.amazon.co.jp/OneOdio-Bluetooth-%E3%83%A2%E3%83%8B%E3%82%BF%E3%83%BC%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-FuSion-A7/dp/B07RY1ZSJ6/ref=sr_1_10?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-10')
    # urls.append('https://www.amazon.co.jp/Bluetooth-%E3%82%AA%E3%83%BC%E3%83%90%E3%83%BC%E3%82%A4%E3%83%A4%E3%83%BC%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-%E3%83%96%E3%83%AB%E3%83%BC%E3%83%88%E3%82%A5%E3%83%BC%E3%82%B9-%E3%83%8E%E3%82%A4%E3%82%BA%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AA%E3%83%B3%E3%82%B0-%E3%82%B3%E3%83%BC%E3%83%89%E3%83%AC%E3%82%B9%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3/dp/B09DFYJVQ3/ref=sr_1_20?pd_rd_r=4c84a560-c861-4fe6-870f-130616032645&pd_rd_w=01HXr&pd_rd_wg=oXvch&pf_rd_p=ba2a089a-90bd-4698-833b-549e0f2fbdf4&pf_rd_r=39Z355X5X3XGJ8PW72JB&qid=1643248128&refinements=p_72%3A82399051&s=electronics&sr=1-20')
    for k, url in enumerate(urls, start=12):
        review_list = []
        review_url = url.replace('dp', 'product-reviews')
        review_list = get_all_reviews(review_url)
        a = 0
        b = 0
            
        #CSVにレビュー情報の書き出し
        with open(r'z:\UserProfile\s20192087\Desktop\etc\iyahon{0}.csv'.format(k),'w', encoding='CP932', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            # 全データを表示
            for review in review_list:
                csvlist=[]
                #データ作成
                csvlist.append(review["label"])
                csvlist.append(review["text"])
                # 出力    
                writer.writerow(csvlist)
            # ファイルクローズ
            print("csv",k)
            f.close()