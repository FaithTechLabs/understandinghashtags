from flask import Flask, request
from flask import render_template
from twitter_search import TwitterSearch
from collections import Counter
import re

app = Flask(__name__)

tw_search = TwitterSearch()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    data = None
    words = {}
    if request.method == "POST":
        geo = request.form.get("location", "")
        within = request.form.get("within", "")
        search = request.form.get("search", "")
        search_form = request.form

        if not geo and not within:
            geo = "43.423681,-80.465330,"
            within = "25mi"
        print(geo + within)
        data = tw_search.run_search(search, count=50, geo=geo + within + "mi")
        for tweet in data:
            print(Counter(w.lower() for w in re.findall(r"\w+", tweet.text)))
    elif request.method == "GET":
        data = tw_search.run_search("", count=5, geo="43.423681,-80.465330,25mi")
    return render_template("index.html", data=data, search_form=search_form)
