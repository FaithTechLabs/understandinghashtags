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
    search_form = None
    search = "#metoo"
    counts = {}
    #search = ""
    if request.method == "POST":
        geo = request.form.get("location", "")
        within = request.form.get("within", "")
        search += " " + request.form.get("search", "")
        search_form = request.form

        if not geo and not within:
            geo = "43.423681,-80.465330,"
            within = "25mi"
        data = tw_search.run_search(search, count=100, geo=geo + within + "mi")
        colours = tw_search.colours(search, count=100, geo=geo + within + "mi")
    elif request.method == "GET":
        data = tw_search.run_search(search, count=6, geo="43.423681,-80.465330,25mi")
        colours = tw_search.colours(search, count=100, geo="43.423681,-80.465330,25mi")

    counts["waterloo"] = tw_search.count(search, count=100, geo="43.423681,-80.465330,25mi")
    counts["new_york"] = tw_search.count(search, count=100, geo="40.712250,-74.001853,25mi")
    counts["vancouver"] = tw_search.count(search, count=100, geo="49.275308,-123.109660,25mi")

    #emojis = tw_search.get_emojis()
    return render_template("index.html", data=data, search_form=search_form, counts=counts, colours=colours)
