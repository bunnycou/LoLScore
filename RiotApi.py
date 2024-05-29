from requests import get
from time import time
from math import floor

KEY = open("key.txt").readline()

def api_account(user, tag):
    return f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user}/{tag}?api_key={KEY}" #region does not matter for account

def api_matches(region, puuid):
    curTime = floor(time())
    return f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={curTime-86400}&endTime={curTime}&type=ranked&api_key={KEY}"

def api_match(region, id):
    return f"https://{region}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={KEY}"

def matches(region, puuid):
    req = get(api_matches(region, puuid))
    if (req.ok):
        matchlist = req.json()
        for i in range(len(matchlist)):
            matchlist[i] = match(region, matchlist[i])

        curTime = time()*1000
        if ((curTime - (7200*1000)) > matchlist[0]["info"]["gameCreation"]):
            return []
        else:
            startOfSession = len(matchlist)-1
            for i in range(len(matchlist)-1):
                print(matchlist[i]["info"]["gameCreation"], matchlist[i+1]["info"]["gameCreation"])
                if ((matchlist[i]["info"]["gameCreation"] - 7200*1000) > matchlist[i+1]["info"]["gameCreation"]):
                    startOfSession = i
                    break

            return matchlist[:startOfSession+1]
    else:
        return "err"

def match(region, id):
    req = get(api_match(region, id))
    if (req.ok):
        return req.json()
    else:
        return "err"

def getpuuid(user, tag):
    req = get(api_account(user, tag))
    if (req.ok):
        return req.json()["puuid"]
    else:
        return "err"
    
def getWL(region, user, tag):
    win = 0
    loss = 0

    region = region.lower()

    if region in ["na", "br", "lan", "las", "americas"]:
        region = "americas"
    elif region in ["eune", "euw", "tr", "ru", "eu", "europe"]:
        region = "europe"
    elif region in ["kr", "jp", "asia"]:
        region = "asia"
    elif region in ["oce", "ph2", "sg2", "th2", "tw2", "vn2", "sea"]:
        region = "sea"
    else: region = "americas" # default to americas

    puuid = getpuuid(user, tag)
    userMatches = matches(region, puuid)

    if matches == "err":
        return 0,0

    if len(userMatches) == 0:
        return 0,0
    else:
        for minfo in userMatches:
            for participant in minfo["info"]["participants"]:
                if participant["puuid"] == puuid:
                    if participant["win"]:
                        win += 1
                    else:
                        loss += 1
                    break
        return win, loss