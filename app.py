from flask import Flask, render_template
from markupsafe import escape
import RiotApiNA

app = Flask(__name__)

@app.route("/na/<user>/<tag>")
def na_user(user, tag):
    #return f"<p>{RiotApiNA.matches(RiotApiNA.getpuuid(user, tag))[0]}</p>"
    #return f"<p>{RiotApiNA.getWL(user,tag)}</p>"
    win, loss = RiotApiNA.getWL(user,tag)
    return render_template("score.html", win=win, loss=loss)