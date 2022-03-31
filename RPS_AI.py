import random

turns = 30

changeRate = 0.2
decay = 6

beats = {"R": "S", "P": "R", "S": "P"}

alowed = ["R", "P", "S"]

MarcovW = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}
MarcovL = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}
MarcovD = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}

data = ["R", "P"]
wins = [0]
lastX = "S"
lastY = "S"
lastWin = 0

def chainUpdate(x, lastY):
    global MarcovW
    global MarcovL
    global MarcovD
    global data
    global decay
    global wins

    lastX = data[-decay + 1:]
    lastWins = wins[-decay + 1:]
    idxMarc = 0

    if 1 in lastWins:
        MarcovW = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}
    if -1 in lastWins:
        MarcovL = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}
    if 0 in lastWins:
        MarcovD = {"B": {"B": 1/3, "L": 1/3, "P": 1/3}, "L": {"B": 1/3, "L": 1/3, "P": 1/3}, "P": {"B": 1/3, "L": 1/3, "P": 1/3}}

    for i in range(len(lastX) - 1):

        if lastWins[i] == 1:
            idxMarc = MarcovW
        elif lastWins[i] == -1:
            idxMarc = MarcovL
        else:
            idxMarc = MarcovD

        if lastX[i] == lastX[i + 1]:
            if lastX[i - 1] == lastX[i]:
                MarcovU = {"P": {"B": idxMarc["P"]["B"]-changeRate/2, "L": idxMarc["P"]["L"]-changeRate/2, "P": idxMarc["P"]["P"]+changeRate}}
            elif lastX[i] == beats[lastX[i - 1]]:
                MarcovU = {"L": {"B": idxMarc["L"]["B"]-changeRate/2, "L": idxMarc["L"]["L"]-changeRate/2, "P": idxMarc["L"]["P"]+changeRate}}
            else:
                MarcovU = {"B": {"B": idxMarc["B"]["B"]-changeRate/2, "L": idxMarc["B"]["L"]-changeRate/2, "P": idxMarc["B"]["P"]+changeRate}}
        elif lastX[i + 1] == beats[lastX[i]]:
            if lastX[i - 1] == lastX[i]:
                MarcovU = {"p": {"B": idxMarc["P"]["B"]-changeRate/2, "L": idxMarc["P"]["L"]+changeRate, "P": idxMarc["P"]["P"]-changeRate/2}}
            elif lastX[i] == beats[lastX[i - 1]]:
                MarcovU = {"L": {"B": idxMarc["L"]["B"]-changeRate/2, "L": idxMarc["L"]["L"]+changeRate, "P": idxMarc["L"]["P"]-changeRate/2}}
            else:
                MarcovU = {"B": {"B": idxMarc["B"]["B"]-changeRate/2, "L": idxMarc["B"]["L"]+changeRate, "P": idxMarc["B"]["P"]-changeRate/2}}
        else:
            if lastX[i - 1] == lastX[i]:
                MarcovU = {"P": {"B": idxMarc["P"]["B"]+changeRate, "L": idxMarc["P"]["L"]-changeRate/2, "P": idxMarc["P"]["P"]-changeRate/2}}
            elif lastX[i] == beats[lastX[i - 1]]:
                MarcovU = {"L": {"B": idxMarc["L"]["B"]+changeRate, "L": idxMarc["L"]["L"]-changeRate/2, "P": idxMarc["L"]["P"]-changeRate/2}}
            else:
                MarcovU = {"B": {"B": idxMarc["B"]["B"]+changeRate, "L": idxMarc["B"]["L"]-changeRate/2, "P": idxMarc["B"]["P"]-changeRate/2}}
        
        if lastWins[i] == 1:
            MarcovW.update(MarcovU)
        elif lastWins[i] == -1:
            MarcovL.update(MarcovU)
        else:
            MarcovD.update(MarcovU)

def rpsAi(lastWins, lastX):
    global MarcovW
    global MarcovL
    global MarcovD
    
    if lastX[1] == lastX[0]:
        strat = "P"
    elif lastX[1] == beats[lastX[0]]:
        strat = "L"
    else:
        strat = "B"

    newStrat = "P"
    
    if lastWins[0] == 1:
        if MarcovW[strat]["L"] > MarcovW[strat]["P"]:
            newStrat = "L"
        elif MarcovW[strat]["B"] > MarcovW[strat]["P"]:
            newStrat = "B"
    elif lastWins[0] == -1:
        if MarcovL[strat]["L"] > MarcovL[strat]["P"]:
            newStrat = "L"
        elif MarcovL[strat]["B"] > MarcovL[strat]["P"]:
            newStrat = "B"
    else:
        if MarcovD[strat]["L"] > MarcovD[strat]["P"]:
            newStrat = "L"
        elif MarcovD[strat]["B"] > MarcovD[strat]["P"]:
            newStrat = "B"

    if random.random() < 0.7:
        if newStrat == "P":
            output = beats[beats[lastX[1]]]
        elif newStrat == "L":
            output = lastX[1]
        else:
            output = beats[lastX[1]]
    else:
        if newStrat == "P":
            output = lastX[1]
        elif newStrat == "L":
            output = beats[lastX[1]]
        else:
            output = beats[beats[lastX[1]]]

    return output

def getInput():
    global alowed
    i = input("RPS: ").upper()
    while not alowed.__contains__(i):
        i = input("RPS: ").upper()
        if alowed.__contains__(i):
            break
    return i

for turn in range(turns):
    win = 0
    
    x = getInput()
    #x = "P"

    y = rpsAi(wins[-1:], data[-2:])

    if beats[x] == y:
        win = 1
    elif beats[y] == x:
        win = -1
    wins.append(win)
    chainUpdate(x, lastY)
    data.append(x)
    lastY = y
    print(x + " - " + y)
    print(win)
if wins.count(-1) > wins.count(1):
    print("AI Wins")
    print(wins.count(-1)/(len(wins) - wins.count(0)))
else:
    print("You Win")
    print(1-(wins.count(-1)/(len(wins) - wins.count(0))))
