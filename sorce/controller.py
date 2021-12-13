from flask import *

app = Flask(__name__)

@app.route('/')
def search_top():
    return render_template("top.html")

@app.route("/search", methods=["POST"])
def search_result():
    url = request.form.get('searchUrl')
    
    if not(checkUrl(url)):
        return render_template("top.html", errorMessage="だめ")
    
    return render_template("result.html", word = url)

def checkUrl(url):
    return url.startswith('https://www.amazon.co.jp/')

# 
if __name__ == '__main__':
    app.run(port=80, debug="true")