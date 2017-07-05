from flask import Flask, render_template, url_for
from string import Template
import statsparser as sp

app = Flask(__name__)

graph_template = Template("""

<h1>
    ${dsname}
</h1>

<img src="/static/${dsname}_epoch_vs_usr.png" alt="failed"/>

""")

@app.route('/')
def home():
    dsnLst = sp.parse_stats()
    return render_template("home.html", dsnLst = dsnLst)

@app.route('/<dsname>')
def graph(dsname):
    return(graph_template.substitute(dsname=dsname))

if __name__ == "__main__":
    app.run(debug=True,use_reloader=True)
