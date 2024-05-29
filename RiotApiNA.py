from requests import get
from time import time
from math import floor

KEY = open("key.txt").readline()

def api_account(user, tag):
    return f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user}/{tag}?api_key={KEY}"

def api_matches(puuid):
    curTime = floor(time())
    return f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={curTime-86400}&endTime={curTime}&type=ranked&api_key={KEY}"

def api_match(id):
    return f"https://americas.api.riotgames.com/lol/match/v5/matches/{id}?api_key={KEY}"

def matches(puuid):
    req = get(api_matches(puuid))
    if (req.ok):
        matchlist = req.json()
        for i in range(len(matchlist)):
            matchlist[i] = match(matchlist[i])

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

def match(id):
    req = get(api_match(id))
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
    
def getWL(user, tag):
    win = 0
    loss = 0

    puuid = getpuuid(user, tag)
    userMatches = matches(puuid)

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