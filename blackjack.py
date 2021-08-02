from random import randint
from dealer_logic import Logic
from os import name, system

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
betAmounts = {'1':1.00, '2':2.50, '3':5.00, '4':25.00, '5':50.00, '6':100.00, '7':500.00}

with open('card_template.txt', 'r', encoding='utf-8') as ct:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    
clear = lambda: system('cls' if name == 'nt' else 'clear')

def takeInput(valids, text): #input validation function
    while True:
        choice = input(f'{text}')
        if choice not in valids:
            print('\nInvalid option. Please try again.')
        else:
            break
    return choice

class Card:
    def __init__(self, suit, face, isFlipped):
        self.suit = suit
        self.face = face
        self.isFlipped = isFlipped
        if self.face in ('J', 'Q', 'K'):
            self.points = 10
        elif self.face == 'A':
            self.points = 11
        else:
            self.points = int(self.face)

    def __str__(self):
        if self.isFlipped:
            return self.flippedCard()
        fullCard = ''
        for count, line in enumerate(cardTemplate):
            if 'F' in line:
                if len(self.face) > 1:
                    line = line.replace('F ', self.face)
                    line = line.replace(' F', self.face)
                else:
                    line = line.replace('F', self.face) 
            elif 'S' in line:
                line = line.replace('S', suitSymbols[self.suit])
            
            if count == 0:
                fullCard += line
            else:
                fullCard += '\n' + line
        return fullCard
    
    def flippedCard(self):
        fullCard = ''
        for count, line in enumerate(cardTemplate):
            line = line.replace('F', '▒')
            line = line.replace('S', '▒')
            line = line.replace(' ', '▒')
            if count == 0:
                fullCard += line
            else:
                fullCard += '\n' + line
        return fullCard

class improperDeck(Exception):
    def __str__(self):
        return 'Deck not properly initialized.'

class ForcedCardNotFound(Exception):
    def __str__(self):
        return 'forceDraw method in class Deck could not find requested cards.'

class Deck(list):
    def shuffle(self):
        with open('cards.txt', 'r') as d:
            for c in d:
                c = c.replace('\n', '')
                c = c.split('|')
                self.append(Card(c[1], c[2], False))
    
    def getRandom(self):
        try:
            return self.pop(randint(0, (len(self)-1)))
        except:
            raise improperDeck
    
    def forceDraw(self, forcedFace):
        for c, card in enumerate(self):
            if card.face == forcedFace:
                return self.pop(c)
        raise ForcedCardNotFound
    
    def getSplit(self):
        while True:
            split = []
            for i in range(2):
                randIndex = randint(0, len(self)-1)
                split.append([randIndex, self[randIndex]])
            if split[0][1].face == split[1][1].face:
                return [i[1] for i in split]
    
    def getDouble(self):
        while True:
            double = []
            for i in range(2):
                randIndex = randint(0, len(self)-1)
                double.append([randIndex, self[randIndex]])
            if double[0][1].points + double[1][1].points in range(9, 12):
                return [i[1] for i in double]


deck = Deck()

class Hand(list):
    def __init__(self, isDealer, splitCard, bet, isCopy, debugHand):
        self.points = 0
        self.isDealer = isDealer
        self.bet = bet
        self.hasDoubled = False
        if not isCopy and not debugHand:
            if not splitCard:
                self.newHand()
            else:
                self.append(splitCard)
        elif debugHand and not isCopy:
            for i in debugHand:
                self.append(deck.forceDraw(i.face))
        else:
            pass

    def newHand(self):
        for i in range(2):
            self.append(deck.getRandom())
        if self.isDealer: #if this is the dealer's hand, show only one card face up
            self[1].isFlipped = True
        for card in self:
            self.points += card.points
    
    def makeCopy(self):
        handCopy = Hand(self.isDealer, None, self.bet, True, None)
        for c in self:
            handCopy.append(c)
        return handCopy

    def endRound(self, won):
        if self.isDealer:
            if won == 'W':
                Dealer.cash += self.bet * 2
            if won == 'B':
                Dealer.cash += self.bet + self.bet * 1.5
            if won == 'D':
                Dealer.cash += self.bet
        else:
            if won == 'W':
                Player.cash += self.bet * 2
            if won == 'B':
                Player.cash += self.bet + self.bet * 1.5
            if won == 'D':
                Player.cash += self.bet
    
    def doubleDown(self):
        if not self.hasDoubled:
            self.hasDoubled = True
            if self.isDealer:
                Dealer.cash -= self.bet    
            else:
                Player.cash -= self.bet
            self.bet *= 2
            self.hit()

    def hasAce(self):
        aceList = [i for i in self if i.face == 'A']
        if aceList:
            return True
        return False

    def chkBreak(self):
        testList = self.makeCopy()
        testList.points = self.points
        aceList = []
        for count, i in enumerate(testList):
            if i.face == 'A':
                aceList.append([count, i])
        if self.hasAce():
            aceList = iter(aceList)
            while testList.points > 21:
                try:
                    currentAce = next(aceList)
                    testList.points -= 10
                except StopIteration:
                    break
        if testList.points > 21:
            return True
        return False
    
    def changeAce(self):
        aceList = []
        for count, i in enumerate(self):
            if i.face == 'A':
                aceList.append([count, i])
        aceList = iter(aceList)
        while self.points > 21:
            try:
                currentAce = next(aceList)
                self.points -= 10
            except StopIteration:
                break

    def chkDouble(self):
        if self.points in range(9, 12) and len(self) == 2 and not self.hasDoubled:
            return True
        return False

    def chkSplit(self):
        if len(self) == 2:
            faces = [i.face for i in self]
            if faces[0] == faces[1]:
                return True
        return False

    def chkBlackjack(self):
        if self.points == 21 and len(self) == 2:
            return True
        if self.points == 21 and len(self) != 2:
            print('*** CHKBLACKJACK METHOD IMPROPERLY INVOKED ***')
        return False

    def hit(self):
        newCard = deck.getRandom()
        if self.isDealer:
            newCard.isFlipped = True
        self.points += newCard.points
        self.append(newCard)
    
    def __str__(self):
        tempAdd = []
        fullHand = ''
        for count, card in enumerate(self):
            for lineCount, line in enumerate(card.__str__().split('\n')):
                if count == 0:
                    tempAdd.append(line + '\n')
                else:
                    editLine = tempAdd[lineCount]
                    editLine = editLine.replace('\n', ' ' + line + '\n')
                    tempAdd[lineCount] = editLine
                    
        for i in tempAdd:
            fullHand += ''.join(i)
        
        return fullHand


class Dealer:
    cash = 500
    def __init__(self, pCard):
        self.originalBet = betAmounts[str(randint(1, 6))]
        self.hand = Hand(True, None, self.originalBet, False, None)
        self.pCard = pCard
        self.isSplit = False
        self.splitAce = False
        Dealer.cash -= self.originalBet
    
    def __str__(self):
        if not self.isSplit:
            return self.hand.__str__()
        else:
            tempAdd = []
            fullHand = ''
            for handCount, h in enumerate([self.hand, self.spHand]):
                for count, card in enumerate(h):
                    for lineCount, line in enumerate(card.__str__().split('\n')):
                        if count == 0:
                            tempAdd.append(line + '\n')
                        elif handCount > 0:
                            editLine = tempAdd[lineCount]
                            editLine = editLine.replace('\n', '\t' + line + '\n')
                        else:
                            editLine = tempAdd[lineCount]
                            editLine = editLine.replace('\n', ' ' + line + '\n')
                            tempAdd[lineCount] = editLine
                        
            for i in tempAdd:
                fullHand += ''.join(i)
            
            return fullHand

    def split(self): #splits hand
        if self.hand.chkSplit() and not self.isSplit:
            if self.hand[0] == 'A' and self.hand[1] == 'A':
                self.splitAce = True
            self.spHand = Hand(False, self.hand.pop(), self.originalBet, False, None)
            self.isSplit = True
            Dealer.cash -= self.originalBet
        elif not self.hand.chkSplit() and not self.isSplit:
            print('*** DEALER PERFORMED ILLEGAL SPLIT, NOT ALLOWED BY CHKSPLIT ***')
        elif self.hand.chkSplit() and self.isSplit:
            print('*** DEALER PERFORMED ILLEGAL SPLIT, ALREADY SPLIT ***')
        else:
            print('*** DEALER PERFORMED ILLEGAL SPLIT, ALREADY SPLIT AND NOT ALLOWED BY CHKSPLIT ***')

    
    def parseMove(self, move, currentHand): #used by play method, takes move from dealer_logic and performs it
        if move == 'S':
            pass
        elif move == 'H':
            currentHand.hit()
        elif move == 'D':
            currentHand.doubleDown()
        elif move == 'SP':
            self.split()
        else:
            print(f'*** PARSEMOVE RECEIVED INVALID MOVE ***\nMove that was received: {move}')

    def totalBust(self): #returns true if all dealer's hands have busted, else false
        if self.isSplit:
            if self.spHand.chkBreak() and self.hand.chkBreak():
                return True
        if self.hand.chkBreak():
            return True
        return False
    
    def showCards(self): #flips all dealer's cards face up to display at end of round
        if self.isSplit:
            for c in self.spHand:
                c.isFlipped = False
        for c in self.hand:
            c.isFlipped = False
    
    def anyDouble(self):
        if self.isSplit:
            return self.hand.hasDoubled or self.spHand.hasDoubled
        return self.hand.hasDoubled

    def play(self):
        returnStr = []
        if not self.anyDouble() and not self.splitAce:
            if self.hand.hasAce() and self.hand.chkBreak(): #if hand is bust and has an ace, make all aces equal to 1 until bust is resolved
                self.hand.changeAce()
                if self.hand.chkBreak(): #if bust not resolved, stand and return
                    returnStr.append('S')
                    return returnStr
            mainLogic = Logic(self.pCard, self.hand, self.isSplit)
            move = mainLogic.decideMove()
            returnStr.append(move)
            if self.isSplit:
                if self.spHand.hasAce() and self.spHand.chkBreak(): #see above comments
                    self.spHand.changeAce()
                    if self.spHand.chkBreak():
                        returnStr.append('S')
                        return returnStr
                logicTwo = Logic(self.pCard, self.spHand, self.isSplit)
                moveTwo = logicTwo.decideMove()
                self.parseMove(moveTwo, self.spHand)
                returnStr.append(moveTwo)
            self.parseMove(move, self.hand)
        else:
            returnStr.append('S')
        return returnStr


class Player:
    cash = 500
    def __init__(self, debug):
        self.makeBet()
        self.hand = Hand(False, None, self.originalBet, False, debug)
        self.isSplit = False
        self.splitAce = False
    
    def __str__(self):
        if not self.isSplit:
            return self.hand.__str__()
        else:
            tempAdd = []
            fullHand = ''
            for handCount, h in enumerate([self.hand, self.spHand]):
                if h.chkBreak():
                    if tempAdd:
                        for count, line in enumerate(tempAdd):
                            if count == 3:
                                tempAdd[3].replace('\n', f'\t** BUST **')
                            else:
                                editLine = line
                                editLine = editLine[:-12] + '\n'
                                tempAdd[count] = editLine
                    else:
                        for i in range(9):
                            if i == 3:
                                tempAdd.append('** BUST **\n')
                            else:
                                tempAdd.append('           \n')
                else:
                    for count, card in enumerate(h):
                        cardLines = card.__str__().split('\n')
                        for lineCount, line in enumerate(cardLines):
                            if count == 0 and handCount == 0:
                                tempAdd.append(line + '\n')
                            else:
                                editLine = tempAdd[lineCount]
                                if count == len(h)-1:
                                    editLine = editLine.replace('\n', '\t\t' + line + '\n')
                                else:
                                    editLine = editLine.replace('\n', ' ' + line + '\n')
                                tempAdd[lineCount] = editLine
                        
            for i in tempAdd:
                fullHand += ''.join(i)
            
            return fullHand
    
    def totalBust(self):
        if self.isSplit:
            if self.spHand.chkBreak() and self.hand.chkBreak():
                return True
        if self.hand.chkBreak():
            return True
        return False

    def split(self):
        if self.hand.chkSplit() and not self.isSplit:
            if self.hand[0] == 'A' and self.hand[1] == 'A':
                self.splitAce = True
            self.spHand = Hand(False, self.hand.pop(), self.originalBet, False, None)
            self.isSplit = True
            Player.cash -= self.originalBet
        else:
            print('*** PLAYER PERFORMED ILLEGAL SPLIT ***')
    
    def anyDouble(self): #returns boolean representing if player has doubled down on any hand
        if self.isSplit:
            return self.hand.hasDoubled or self.spHand.hasDoubled
        return self.hand.hasDoubled
    
    def makeBet(self):
        clear()
        if Player.cash <= 0:
            print('*** MAKEBET INVOKED WITH INVALID PLAYER CASH ***')
        print(f'Your current cash is ${Player.cash:.2f}')
        betAmt = takeInput(('1', '2', '3', '4', '5', '6', '7'), '\n1. $1.00\n2. $2.50\n3. $5.00\n4. $25.00\n5. $50.00\n6. $100.00\n7. $500.00\n\nEnter bet choice: ')
        while betAmounts[betAmt] > Player.cash:
            betAmt = takeInput(('1', '2', '3', '4', '5', '6', '7'), "\n1. $1.00\n2. $2.50\n3. $5.00\n4. $25.00\n5. $50.00\n6. $100.00\n7. $500.00\n\nCan't afford bet! Enter lower amount: ")
        for k, v in betAmounts.items():
            if betAmt == k:
                self.originalBet = v
        Player.cash -= self.originalBet

    def play(self):
        returnStr = []
        if not self.anyDouble() and not self.splitAce: #need fix play method in class Player to improve split UI
            if not self.hand.chkBreak():
                if self.hand.chkSplit() and self.hand.chkDouble() and not self.isSplit:
                    option = takeInput(('1', '2', '3', '4'), '\n1. Hit\n2. Stand\n3. Split\n4. Double Down\n\nEnter choice: ')
                    if option == '1':
                        self.hand.hit()
                        returnStr.append('H')
                    elif option == '2':
                        returnStr.append('S')
                    elif option == '3':
                        self.split()
                        returnStr.append('SP')
                    else:
                        self.hand.doubleDown()
                        returnStr.append('D')
                elif self.hand.chkSplit() and not self.isSplit:
                    option = takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Split\n\nEnter choice: ')
                    if option == '1':
                        self.hand.hit()
                        returnStr.append('H')
                    elif option == '2':
                        returnStr.append('S')
                    else:
                        self.split()
                        returnStr.append('SP')
                elif self.hand.chkDouble():
                    if self.isSplit:
                        option = takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice for hand #1: ')
                    else:
                        option = takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice: ')
                    if option == '1':
                        self.hand.hit()
                        returnStr.append('H')
                    elif option == '2':
                        returnStr.append('S')
                    else:
                        self.hand.doubleDown()
                        returnStr.append('D')
                else:
                    if self.isSplit:
                        option = takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice for hand #1: ')
                    else:
                        option = takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice: ')
                    if option == '1':
                        self.hand.hit()
                        returnStr.append('H')
                    else:
                        returnStr.append('S')
            if self.isSplit and not self.spHand.chkBreak():
                if self.spHand.chkDouble():
                    option = takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice for hand #2: ')
                    if option == '1':
                        self.spHand.hit()
                        returnStr.append('H')
                    elif option == '2':
                        returnStr.append('S')
                    else:
                        self.spHand.doubleDown()
                        returnStr.append('D')
                else:
                    option = takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice for hand #2: ')
                    if option == '1':
                        self.spHand.hit()
                        returnStr.append('H')
                    else:
                        returnStr.append('S')
        else:
            returnStr.append('S')
        return returnStr
            
        


class Game:
    def __init__(self, debug):
        deck.shuffle()
        if debug:
            self.player = Player(debug)
        else:
            self.player = Player(None)
        self.dealer = Dealer(self.player.hand[0])
        self.winStatus = None
    
    def __str__(self):
        if not self.dealer.isSplit and not self.player.isSplit:
            return "   *** Dealer's Hand ***\n" + self.dealer.__str__() + '\n\n   *** Your Hand ***\n' + self.player.__str__()
        if self.player.isSplit and not self.dealer.isSplit:
            return "   *** Dealer's Hand ***\n" + self.dealer.__str__() + '\n\n   *** Your Hands ***\n'+ self.player.__str__()
        if self.dealer.isSplit and not self.player.isSplit:
            return "   *** Dealer's Hands ***\n" + self.dealer.__str__() + '\n\n   *** Your Hand ***\n' + self.player.__str__()
        if self.player.isSplit and self.dealer.isSplit:
            return "   *** Dealer's Hands ***\n" + self.dealer.__str__() + '\n\n   *** Your Hands ***\n' + self.player.__str__()

    def eitherBlackjack(self): #made individual method for blackjack case so it can be checked at game start
        if self.player.hand.chkBlackjack():
            self.dealer.showCards()
            return self.__str__() + '\n\n*** YOU HAVE BLACKJACK! YOU WIN! ***'
        elif self.dealer.hand.chkBlackjack():
            self.dealer.showCards()
            return self.__str__() + '\n\n*** DEALER HAS BLACKJACK! DEALER WINS! ***'
        else:
            return ''

    def play(self):
        while True:
            clear()
            print(self)
            self.lastPlayerMove = self.player.play()
            self.lastDealerMove = self.dealer.play()
            if (self.lastDealerMove != ['S'] and self.lastDealerMove != ['S', 'S']) and (self.lastPlayerMove == ['S'] or self.lastPlayerMove == ['S', 'S'])\
            and not self.player.totalBust():
                while self.lastDealerMove != ['S'] and self.lastDealerMove != ['S', 'S'] and not self.dealer.totalBust():
                    self.lastDealerMove = self.dealer.play()
            if ( (self.lastPlayerMove == ['S'] or self.lastPlayerMove == ['S', 'S']) and\
                (self.lastDealerMove == ['S'] or self.lastDealerMove == ['S', 'S']) ) or\
                (self.player.totalBust() or self.dealer.totalBust()):
                break

    def finishGame(self):
        self.dealer.showCards()
        playerResults = {}
        dealerResults = {}
        if 'YOU' in self.eitherBlackjack():
            self.player.hand.endRound('B')
        elif 'DEALER' in self.eitherBlackjack():
            self.dealer.hand.endRound('B')
        elif not self.player.totalBust() and not self.dealer.totalBust():
            if self.player.isSplit and not self.player.spHand.chkBreak():
                playerResults[self.player.spHand.points] = self.player.spHand
            if not self.player.hand.chkBreak():
                playerResults[self.player.hand.points] = self.player.hand
            if self.dealer.isSplit and not self.dealer.spHand.chkBreak():
                dealerResults[self.dealer.spHand.points] = self.dealer.spHand
            if not self.dealer.hand.chkBreak():
                dealerResults[self.dealer.hand.points] = self.dealer.hand
            
            pKeys = list(playerResults.keys())
            dKeys = list(dealerResults.keys())
            bestP = max(pKeys)
            bestD = max(dKeys)

            def pointChk(): #used 3 inner functions because these snippets of code were used more than once
                if bestP > bestD:
                    playerResults[bestP].endRound('W')
                    self.winStatus = 'pw'
                elif bestP == bestD:
                    playerResults[bestP].endRound('D')
                    dealerResults[bestD].endRound('D')
                    self.winStatus = 'draw'
                else:
                    dealerResults[bestD].endRound('W')
                    self.winStatus = 'dw'
                
            def samePlayerPointChk(): #see pointChk comment
                if bestP > bestD:
                    self.player.hand.endRound('W')
                    self.player.spHand.endRound('w')
                    self.winStatus = 'pw'
                elif bestP == bestD:
                    self.player.hand.endRound('D')
                    self.player.spHand.endRound('D')
                    dealerResults[bestD].endRound('D')
                    self.winStatus = 'draw'
                else:
                    dealerResults[bestD].endRound('W')
                    self.winStatus = 'dw'

            def sameDealerPointChk(): #see pointChk comment
                if bestD > bestP:
                    self.dealer.hand.endRound('W')
                    self.dealer.spHand.endRound('W')
                    self.winStatus = 'dw'
                elif bestD == bestP:
                    self.dealer.hand.endRound('D')
                    self.dealer.spHand.endRound('D')
                    playerResults[bestP].endRound('D')
                    self.winStatus = 'draw'
                else:
                    playerResults[bestP].endRound('W')
                    self.winStatus = 'pw'

            if len(playerResults) == 1 and len(dealerResults) == 1:
                pointChk()
            elif len(playerResults) > len(dealerResults):
                if pKeys[0] != pKeys[1]:
                    pointChk()
                else:
                    samePlayerPointChk()
            elif len(playerResults) < len(dealerResults):
                if dKeys[0] != dKeys[1]:
                    pointChk()
                else:
                    sameDealerPointChk()
            else:
                if (pKeys[0] != pKeys[1]) and (dKeys[0] != dKeys[1]):
                    pointChk()
                elif (pKeys[0] == pKeys[1]) and (dKeys[0] != dKeys[1]):
                    samePlayerPointChk()
                elif (pKeys[0] != pKeys[1]) and (dKeys[0] == dKeys[1]):
                    sameDealerPointChk()
                else:
                    if bestP > bestD:
                        self.player.hand.endRound('W')
                        self.player.spHand.endRound('W')
                        self.winStatus = 'pw'
                    elif bestP < bestD:
                        self.dealer.hand.endRound('W')
                        self.dealer.spHand.endRound('W')
                        self.winStatus = 'dw'
                    else:
                        self.dealer.hand.endRound('D')
                        self.dealer.spHand.endRound('D')
                        self.player.hand.endRound('D')
                        self.player.spHand.endRound('D')
                        self.winStatus = 'draw'
        elif self.player.totalBust() and not self.dealer.totalBust():
            self.winStatus = 'dw'
            if self.dealer.isSplit:
                if not self.dealer.spHand.chkBreak():
                    self.dealer.spHand.endRound('W')
            if not self.dealer.hand.chkBreak():
                self.dealer.hand.endRound('W')
        elif self.dealer.totalBust() and not self.player.totalBust():
            self.winStatus = 'pw'
            if self.player.isSplit:
                if not self.player.spHand.chkBreak():
                    self.player.spHand.endRound('W')
            if not self.player.hand.chkBreak():
                self.player.hand.endRound('W')
        elif self.player.totalBust() and self.dealer.totalBust():
            self.winStatus = 'n'
        else:
            print('*** ERROR IN FINISHGAME METHOD, ALL GAME STATES EXHAUSTED ***')
    
    def endgameStr(self):
        if self.winStatus == 'pw':
            return '*** PLAYER WINS ***'
        if self.winStatus == 'dw':
            return '*** DEALER WINS ***'
        if self.winStatus == 'draw':
            return '*** DRAW ***'
        if self.winStatus == 'n':
            return '*** ALL BUSTED ***'
        print('*** ERROR IN ENDGAMESTR METHOD, INCORRECT WINSTATUS ***')
            

def debug():
    while True:
        deck.shuffle()
        clear()
        choice = input('\n\nDebug Menu\n\n1. Specify dealt hand\n2. Deal condition permitting split\n3. Deal condition permitting double down\n4. Exit and play normal game\n')
        if choice == '1':
            hand = input('Enter hand: ')
            hand = hand.split(',')
        elif choice == '2':
            hand = deck.getSplit()
        elif choice == '3':
            hand = deck.getDouble()
        else:
            break
        currentGame = Game(hand)
        if currentGame.eitherBlackjack():
            print(currentGame.eitherBlackjack())
            currentGame.finishGame()
        else:
            currentGame.play()
            currentGame.finishGame()
            clear()
            print(currentGame)
            print(currentGame.endgameStr())




enterDebug = input('Welcome! Press Enter to start.\n')
if enterDebug == 'debug':
    debug()

while True:
    if Player.cash == 0:
        clear()
        option = takeInput({'1', '2'}, "You're out of money! Options:\n1. Start over with default cash\n2. Exit\n")
        if option == '1':
            Player.cash, Dealer.cash = 500, 500
        else:
            break
    elif Dealer.cash == 0:
        clear()
        print('Dealer is out of cash! Player wins!')
        option = takeInput({'1', '2'}, "Options:\n1. Start over with default cash\n2. Exit\n")
        if option == '1':
            Player.cash, Dealer.cash = 500, 500
        else:
            break
    else:
        currentGame = Game(None)
        if currentGame.eitherBlackjack():
            print(currentGame.eitherBlackjack())
            currentGame.finishGame()
        else:
            currentGame.play()
            currentGame.finishGame()
            clear()
            print(currentGame)
            print(currentGame.endgameStr())
    cont = takeInput(('y', 'n'), '\nPlay again? (y/n)\n')
    if cont == 'n':
        break
