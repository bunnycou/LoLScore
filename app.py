from flask import Flask, render_template
from markupsafe import escape
import RiotApi

app = Flask(__name__)

@app.route("/<region>/<user>/<tag>")
def na_user(region,user, tag):
    #return f"<p>{RiotApiNA.matches(RiotApiNA.getpuuid(user, tag))[0]}</p>"
    #return f"<p>{RiotApiNA.getWL(user,tag)}</p>"
    win, loss = RiotApi.getWL(region,user,tag)
    return render_template("score.html", win=win, loss=loss)