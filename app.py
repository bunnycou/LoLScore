from flask import Flask, render_template, redirect
from markupsafe import escape
from api import getWLKD

app = Flask(__name__)

@app.route("/<region>/<user>/<tag>") # legacy/ranked shorthand
def rankedWL(region, user, tag):
    print(f"Returning ranked WL for {user}#{tag}")
    win, loss, kills, deaths = getWLKD(region.lower(), user.lower(), tag.lower(), "ranked")
    return render_template("score.html", win=win, loss=loss)

@app.route("/<region>/<user>/<tag>/kd") # legacy/ranked shorthand
def rankedWLWLKD(region, user, tag):
    print(f"Returning ranked WLKD for {user}#{tag}")
    win, loss, kills, deaths = getWLKD(region.lower(), user.lower(), tag.lower(), "ranked")
    return render_template("scorekd.html", win=win, loss=loss, kills=kills, deaths=deaths)

@app.route("/<region>/<user>/<tag>/<gameType>") # for aram and norms (supports ranked)
def otherWL(region, user, tag, gameType):
    print(f"Returning {gameType} WL for {user}#{tag}")
    win, loss, kills, deaths = getWLKD(region.lower(), user.lower(), tag.lower(), gameType.lower())
    return render_template("scorekd.html", win=win, loss=loss, kills=kills, deaths=deaths)

@app.route("/<region>/<user>/<tag>/<gameType>/kd") # for aram and norms (supports ranked)
def otherWLKD(region, user, tag, gameType):
    print(f"Returning {gameType} WLKD for {user}#{tag}")
    win, loss, kills, deaths = getWLKD(region.lower(), user.lower(), tag.lower(), gameType.lower())
    return render_template("scorekd.html", win=win, loss=loss, kills=kills, deaths=deaths)

@app.route("/")
def home():
    return render_template("index.html")