import urllib.robotparser

# robots.txtの読み取り
robots_txt_url = 'https://www.amazon.co.jp/robots.txt'
rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_txt_url)
rp.read()

# robots.txtの情報から調査したいURL、User-Agentでクロール可能かを調べる
user_agent = '*'
url = 'https://qiita.com/api/*'
result = rp.can_fetch(user_agent, url)
print(result)