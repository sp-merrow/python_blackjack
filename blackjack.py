from random import randint
from dealer_logic import Logic
from os import name, system

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
betAmounts = {'1':1.00, '2':2.50, '3':5.00, '4':25.00, '5':50.00, '6':100.00, '7':500.00}

with open('card_template.txt', 'r', encoding='utf-8') as ct:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    
clear = lambda: system('cls' if name == 'nt' else 'cls')

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
            print('*** DECK NOT PROPERLY INITIALIZED ***')

deck = Deck()

class Hand(list):
    def __init__(self, isDealer, splitCard, bet):
        self.points = 0
        self.isDealer = isDealer
        self.bet = bet
        self.hasDoubled = False
        if not splitCard:
            self.newHand()
        else:
            self.append(splitCard)

    def newHand(self):
        for i in range(2):
            self.append(deck.getRandom())
        if self.isDealer: #if this is the dealer's hand, show only one card face up
            self[1].isFlipped = True
        for card in self:
            self.points += card.points

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
        currentPts = self.points
        aceList = [i for i in self.copy() if i.face == 'A']
        aceList = iter(aceList)
        while currentPts > 21:
            try:
                next(aceList).points = 1
            except StopIteration:
                break
        if currentPts > 21:
            return True
        return False

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
        self.hand = Hand(True, None, self.originalBet)
        self.pCard = pCard
        self.isSplit = False
        self.splitAce = False
        Dealer.cash -= self.originalBet

    def split(self): #splits hand
        if self.hand[0] == 'A' and self.hand[1] == 'A':
            self.splitAce = True
        self.spHand = Hand(False, self.hand.pop(), self.originalBet)
        self.isSplit = True
        Dealer.cash -= self.originalBet
    
    def parseMove(self, move, currentHand): #used by play method, takes move from dealer_logic and performs it
        if move == 'S':
            pass
        elif move == 'H':
            currentHand.hit()
        elif move == 'D':
            currentHand.doubleDown()
        else:
            self.split()

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
            return self.hand.hasDoubled and self.spHand.hasDoubled
        return self.hand.hasDoubled

    def play(self):
        returnStr = []
        if not self.anyDouble() and not self.splitAce:
            mainLogic = Logic(self.pCard, self.hand)
            move = mainLogic.decideMove()
            returnStr.append(move)
            if self.isSplit:
                logicTwo = Logic(self.pCard, self.spHand)
                moveTwo = logicTwo.decideMove()
                self.parseMove(moveTwo, self.spHand)
                returnStr.append(moveTwo)
            self.parseMove(move, self.hand)
        else:
            returnStr.append('S')
        return returnStr


class Player:
    cash = 500
    def __init__(self):
        self.makeBet()
        self.hand = Hand(False, None, self.originalBet)
        self.isSplit = False
        self.splitAce = False
    
    def __str__(self):
        return f'Your current cash is ${Player.cash:.2f}'
    
    def totalBust(self):
        if self.isSplit:
            if self.spHand.chkBreak() and self.hand.chkBreak():
                return True
        if self.hand.chkBreak():
            return True
        return False

    def split(self):
        if self.hand[0] == 'A' and self.hand[1] == 'A':
            self.splitAce = True
        self.spHand = Hand(False, self.hand.pop(), self.originalBet)
        self.isSplit = True
        Player.cash -= self.originalBet
        print(self.spHand)
    
    def anyDouble(self): #returns boolean representing if player has doubled down on any hand
        if self.isSplit:
            return self.hand.hasDoubled and self.spHand.hasDoubled
        return self.hand.hasDoubled
    
    def makeBet(self):
        clear()
        if Player.cash <= 0:
            print('*** MAKEBET INVOKED WITH INVALID PLAYER CASH ***')
        print(self)
        betAmt = takeInput(('1', '2', '3', '4', '5', '6', '7'), '\n1. $1.00\n2. $2.50\n3. $5.00\n4. $25.00\n5. $50.00\n6. $100.00\n7. $500.00\n\nEnter bet choice: ')
        while betAmounts[betAmt] > Player.cash:
            betAmt = takeInput(('1', '2', '3', '4', '5', '6', '7'), "\n1. $1.00\n2. $2.50\n3. $5.00\n4. $25.00\n5. $50.00\n6. $100.00\n7. $500.00\n\nCan't afford bet! Enter lower amount: ")
        for k, v in betAmounts.items():
            if betAmt == k:
                self.originalBet = v
        Player.cash -= self.originalBet

    def play(self):
        returnStr = []
        if not self.anyDouble() and not self.splitAce:
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
                    option = takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice: ')
                    if option == '1':
                        self.hand.hit()
                        returnStr.append('H')
                    else:
                        returnStr.append('S')
            if self.isSplit and not self.spHand.chkBreak():
                if self.spHand.chkDouble():
                    option = takeInput(('1', '2', '3'), '\n*** FOR HAND 2 ***\n\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice: ')
                    if option == '1':
                        self.spHand.hit()
                        returnStr.append('H')
                    elif option == '2':
                        returnStr.append('S')
                    else:
                        self.spHand.doubleDown()
                        returnStr.append('D')
                else:
                    option = takeInput(('1', '2'), '\n*** FOR HAND 2 ***\n\n1. Hit\n2. Stand\n\nEnter choice: ')
                    if option == '1':
                        self.spHand.hit()
                        returnStr.append('H')
                    else:
                        returnStr.append('S')
        else:
            returnStr.append('S')
        return returnStr
            
        


class Game:
    def __init__(self):
        deck.shuffle()
        self.player = Player()
        self.dealer = Dealer(self.player.hand[0])
        self.winStatus = None
    
    def __str__(self):
        if not self.dealer.isSplit and not self.player.isSplit:
            return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your Hand ***\n' + self.player.hand.__str__()
        if self.player.isSplit and not self.dealer.isSplit:
            if not self.player.spHand.chkBreak():
                return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** Your 2nd Hand ***\n' + self.player.spHand.__str__()
            return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** 2nd Hand Is Bust ***'
        if self.dealer.isSplit and not self.player.isSplit:
            return "*** Dealer's 1st Hand ***\n" + self.dealer.hand.__str__() + "\n*** Dealer's 2nd Hand ***\n" + self.dealer.spHand.__str__() + '\n\n*** Your Hand ***\n' + self.player.hand.__str__()
        if self.player.isSplit and self.dealer.isSplit:
            if not self.player.spHand.chkBreak():
                return "*** Dealer's 1st Hand ***\n" + self.dealer.hand.__str__() + "\n*** Dealer's 2nd Hand ***\n" + self.dealer.spHand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** Your 2nd Hand ***\n' + self.player.spHand.__str__()
            return "*** Dealer's 1st Hand ***\n" + self.dealer.hand.__str__() + "\n*** Dealer's 2nd Hand ***\n" + self.dealer.spHand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** 2nd Hand Is Bust ***'

    def eitherBlackjack(self): #made individual method for blackjack case so it can be checked at game start
        if self.player.hand.chkBlackjack():
            return self.__str__() + '\n\n*** YOU HAVE BLACKJACK! YOU WIN! ***'
        elif self.dealer.hand.chkBlackjack():
            return self.__str__() + '\n\n*** DEALER HAS BLACKJACK! DEALER WINS! ***'
        else:
            return ''

    def play(self):
        pHandBust, pSplitHandBust = False, False
        while True:
            clear()
            print(self)
            self.lastPlayerMove = self.player.play()
            if self.player.isSplit:
                if self.player.spHand.chkBreak() and not pSplitHandBust:
                    print('\n*** BUST! ***')
                    pSplitHandBust = True
            if self.player.hand.chkBreak() and not pHandBust:
                print('\n*** BUST! ***')
                pHandBust = True
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
            if self.player.isSplit:
                if not self.player.spHand.chkBreak():
                    playerResults[self.player.spHand.points] = self.player.spHand
            if not self.player.hand.chkBreak():
                playerResults[self.player.hand.points] = self.player.hand
            if self.dealer.isSplit:
                if not self.dealer.spHand.chkBreak():
                    dealerResults[self.dealer.spHand.points] = self.dealer.spHand
            if not self.dealer.hand.chkBreak():
                dealerResults[self.dealer.hand.points] = self.dealer.hand
            
            bestP = max(playerResults.keys())
            bestD = max(dealerResults.keys())
            pKeys = list(playerResults.keys())
            dKeys = list(dealerResults.keys())

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
            


print('\n*** Blackjack ***')

while True:
    if Player.cash == 0:
        clear()
        option = takeInput({'1', '2'}, "You're out of money! Options:\n1. Start over with default cash\n2. Exit\n")
        if option == '1':
            Player.cash, Dealer.cash = 500, 500
        else:
            pass #boilerplate code, will call end of program function once implemented
    elif Dealer.cash == 0:
        clear()
        print('Dealer is out of cash! Player wins!')
        option = takeInput({'1', '2'}, "Options:\n1. Start over with default cash\n2. Exit\n")
        if option == '1':
            Player.cash, Dealer.cash = 500, 500
        else:
            pass #boilerplate code, see above in Player.cash if statement
    else:
        currentGame = Game()
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
