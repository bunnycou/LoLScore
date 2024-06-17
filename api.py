from requests import get
from time import time
from math import floor

KEY = open("key.txt").readline()

def api_account(user, tag):
    return f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user}/{tag}?api_key={KEY}" #region does not matter for account

def api_matches(region, puuid, gameType, queue):
    curTime = floor(time())
    return f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={curTime-86400}&endTime={curTime}&type={gameType}&queue={queue}&api_key={KEY}"

def api_match(region, id):
    return f"https://{region}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={KEY}"

def matches(region, puuid, gameType, queue):
    req = get(api_matches(region, puuid, gameType, queue))
    if (req.ok):
        matchlist = req.json()
        if len(matchlist) == 0: return [] # no matches
        for i in range(len(matchlist)):
            matchlist[i] = match(region, matchlist[i])
            if matchlist[i] == "err":
                return "err"

        curTime = time()*1000
        if ((curTime - (10800*1000)) > matchlist[0]["info"]["gameCreation"]): # if most recent match is not within 3 hours
            return []
        else:
            startOfSession = len(matchlist)-1
            for i in range(len(matchlist)-1):
                if ((matchlist[i]["info"]["gameCreation"] - 10800*1000) > matchlist[i+1]["info"]["gameCreation"]): # gap greater than 3 hours between matches
                    startOfSession = i
                    break

            return matchlist[:startOfSession+1]
    else:
        print("matches - " + str(req.status_code))
        return "err"

def match(region, id):
    req = get(api_match(region, id))
    if (req.ok):
        return req.json()
    else:
        print("match - " + str(req.status_code))
        return "err"

def getpuuid(user, tag):
    req = get(api_account(user, tag))
    if (req.ok):
        return req.json()["puuid"]
    else:
        print("puuid - " + str(req.status_code))
        return "err"
    
def getWLKD(region, user, tag, gameType):
    win = 0
    loss = 0
    kills = 0
    deaths = 0

    region = region.lower()

    if region in ["na", "br", "lan", "las", "americas"]:
        region = "americas"
    elif region in ["eune", "euw", "tr", "ru", "eu", "europe"]:
        region = "europe"
    elif region in ["kr", "jp", "asia"]:
        region = "asia"
    elif region in ["sea", "oceania", "oce", "ph2", "sg2", "th2", "tw2", "vn2"]:
        region = "sea"
    else: region = "americas" # default to americas

    queue = 420 # default ranked, 400 for norm, 450 for aram

    if gameType in ["ranked", "rank"]: # catch for ranked just in case
        gameType = "ranked"
        queue = "420"
    elif gameType in ["flex"]:
        gameType = "ranked"
        queue = "440"
    elif gameType in ["aram"]: # catch for aram alternate names
        gameType = "normal"
        queue = "450"
    elif gameType in ["normal", "normals", "norm", "norms", "draft"]:
        gameType = "normal"
        queue = "400"

    puuid = getpuuid(user, tag)

    if puuid == "err":
        return 0,0,0,0

    userMatches = matches(region, puuid, gameType, queue)

    if userMatches == "err":
        return 0,0,0,0

    if len(userMatches) == 0:
        return 0,0,0,0
    else:
        for minfo in userMatches:
            # print(minfo)
            if minfo["info"]["gameDuration"] < 660: # game is less than 11 mintues (remake)
                continue
            for participant in minfo["info"]["participants"]:
                if participant["puuid"] == puuid:
                    kills += participant["kills"]
                    deaths += participant["deaths"]
                    if participant["win"]:
                        win += 1
                    else:
                        loss += 1
                    break
        return win, loss, kills, deaths