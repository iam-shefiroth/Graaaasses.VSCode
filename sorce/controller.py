from flask import *

app = Flask(__name__)

@app.route('/')
def search_top():
    return render_template("top.html")

@app.route("/search", methods=["POST"])
def search_result():
    url = request.form.get('searchUrl')
    return render_template("result.html", word = url)

# 
if __name__ == '__main__':
    app.run(port=80)