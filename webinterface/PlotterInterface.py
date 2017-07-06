from flask import Flask, render_template, url_for
import statsparser as sp

app = Flask(__name__)
summaries = sp.get_dsnames("/home/jguiang/ProjectMetis/webinterface/static/summaryinfo.json")

@app.route('/')
def home():
    return render_template("home.html", summaries = summaries)

@app.route('/graphs/<string:dsname>/')
def graph(dsname):
    return render_template("graphs.html", dsname = dsname, summaries = summaries)

if __name__ == "__main__":
    app.run()
