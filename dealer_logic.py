import csv

with open('strategy.csv', 'r') as st:
    parsed = csv.reader(st, delimiter=',')
    logicTable = []
    for c, row in enumerate(parsed):
        newData = []
        if c == 0:
            for ele in row:
                if ele.isdigit():
                    newData.append(int(ele))
                else:
                    newData.append(str(ele))
            playerLookup = newData.copy()
        else:
            for ele in row:
                if ele.isdigit():
                    newData.append(int(ele))
                else:
                    newData.append(str(ele))
            logicTable.append(newData)

class Logic:
    def __init__(self, pCard, myHand):
        self.pCard = pCard
        self.opponentPoints = pCard.points
        self.myHand = myHand
        self.myPoints = self.myHand.points
    
    def decideMove(self):
        valLocation = playerLookup.index(self.opponentPoints)
        if self.myHand.hasAce():
            lookupType = 'soft'
        else:
            lookupType = 'hard'
        if self.myHand.chkSplit():
            lookupType = 'pair'

        for row in logicTable:
            if row[0] == lookupType and row[1] == self.myPoints:
                return row[valLocation]