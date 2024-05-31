from flask import Flask, render_template
from markupsafe import escape
from api import getWLKD

app = Flask(__name__)

@app.route("/<region>/<user>/<tag>")
def userWL(region, user, tag):
    #return f"<p>{RiotApiNA.matches(RiotApiNA.getpuuid(user, tag))[0]}</p>"
    #return f"<p>{RiotApiNA.getWL(user,tag)}</p>"
    win, loss, kills, deaths = getWLKD(region, user, tag)
    return render_template("score.html", win=win, loss=loss)

@app.route("/<region>/<user>/<tag>/kd")
def userWLKD(region, user, tag):
    win, loss, kills, deaths = getWLKD(region, user, tag)
    #return f"<p>{win}W {loss}L {kills}K {deaths}D</p>"
    return render_template("scorekd.html", win=win, loss=loss, kills=kills, deaths=deaths)