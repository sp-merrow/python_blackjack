import csv

with open('strategy.csv', 'r') as st:
    parsed = csv.reader(st, delimiter=',')
    logicTable = []
    for c, row in enumerate(parsed):
        newData = []
        if c == 0:
            for ele in row:
                newData.append(str(ele).strip())
            playerLookup = newData.copy()
        else:
            for ele in row:
                if ele.isdigit():
                    newData.append(int(ele))
                else:
                    newData.append(str(ele).strip())
            logicTable.append(newData)

class LogicTableLookupFailed(Exception):
    def __str__(self):
        return 'decideMove method could not find field'

class Logic:
    def __init__(self, pCard, myHand, isSP):
        self.pCard = pCard
        if pCard.face in {'J', 'K', 'Q'}:
            self.opponentFace = '10'
        else:
            self.opponentFace = str(pCard.face)
        self.myHand = myHand
        self.myPoints = self.myHand.points
        self.isSP = isSP
    
    def decideMove(self):
        valLocation = playerLookup.index(self.opponentFace)
        if self.myHand.chkSplit() and not self.isSP:
            lookupType = 'pair'
        elif self.myHand.hasAce():
            lookupType = 'soft'
        else:
            lookupType = 'hard'

        move = "If you're reading this, move is unassigned."
        for row in logicTable:
            if row[0] == lookupType and row[1] == self.myPoints:
                move = row[valLocation]
        
        if move not in {'S', 'H', 'D', 'SP'}:
            print(f'Move received: {move}')
            raise LogicTableLookupFailed
        else:
            return move