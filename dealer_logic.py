import csv

with open('strategy.csv', 'r') as st:
    parsed = csv.reader(st, delimiter=',')
    logicTable = []
    for c, row in enumerate(parsed):
        newData = []
        if c == 0:
            for ele in row:
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
    def __init__(self, pCard, myHand, isSP):
        self.pCard = pCard
        if pCard.face in {'J', 'K', 'Q'}:
            self.opponentFace = '10'
        else:
            self.opponentFace = pCard.face
        self.myHand = myHand
        self.myPoints = self.myHand.points
        self.isSP = isSP
    
    def decideMove(self):
        valLocation = playerLookup.index(self.opponentFace)
        if self.myHand.hasAce():
            lookupType = 'soft'
        else:
            lookupType = 'hard'
        if self.myHand.chkSplit() and not self.isSP:
            lookupType = 'pair'

        for row in logicTable:
            if row[0] == lookupType and row[1] == self.myPoints:
                return row[valLocation]