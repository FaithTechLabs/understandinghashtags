from flask import Flask, request
from flask import render_template
from twitter_search import TwitterSearch
app = Flask(__name__)

tw_search = TwitterSearch()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    data = None
    if request.method == "POST":
        print(request.form)
        data = tw_search.run_search(request.form.get("search", ""), count=5, geo="43.423681,-80.465330,100mi")
    elif request.method == "GET":
        data = tw_search.run_search("", count=5, geo="43.423681,-80.465330,100mi")
    return render_template("index.html", data=data)
