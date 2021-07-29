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
            self.bet *= 2
            self.hasDoubled = True
            if self.isDealer:
                Dealer.cash -= self.bet    
            else:
                Player.cash -= self.bet


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
        if self.points in range(9, 12):
            return True
        return False

    def chkSplit(self):
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
        Dealer.cash -= self.originalBet

    def split(self):
        self.spHand = Hand(False, self.hand[1], self.originalBet)
        self.isSplit = True
        Dealer.cash -= self.originalBet
    
    def parseMove(self, move, currentHand):
        if move == 'S':
            pass
        elif move == 'H':
            currentHand.hit()
        elif move == 'D':
            currentHand.doubleDown()
        else:
            self.split()
    
    def totalBust(self):
        if self.isSplit:
            if self.spHand.chkBreak() and self.hand.chkBreak():
                return True
        if self.hand.chkBreak():
            return True
        return False
        
    def play(self):
        while True:
            returnStr = []
            mainLogic = Logic(self.pCard, self.hand)
            move = mainLogic.decideMove()
            returnStr.append(move)
            if self.isSplit:
                logicTwo = Logic(self.pCard, self.spHand)
                moveTwo = logicTwo.decideMove()
                self.parseMove(moveTwo, self.spHand)
                returnStr.append(moveTwo)
            self.parseMove(move, self.hand)
            if returnStr == ['S'] or ['S', 'S'] or self.totalBust():
                break
        return returnStr


class Player:
    cash = 500
    def __init__(self):
        self.makeBet()
        self.hand = Hand(False, None, self.originalBet)
        self.isSplit = False
    
    def __str__(self):
        return f'Your current cash is ${Player.cash}'
    
    def totalBust(self):
        if self.isSplit:
            if self.spHand.chkBreak() and self.hand.chkBreak():
                return True
        if self.hand.chkBreak():
            return True
        return False

    def split(self):
        self.spHand = Hand(False, self.hand[1], self.originalBet)
        self.isSplit = True
        Player.cash -= self.originalBet
    
    def takeInput(self, valids, text):
        while True:
            choice = input(f'{text}')
            if choice not in valids:
                print('\nInvalid option. Please try again.')
            else:
                break
        return choice
    
    def makeBet(self):
        betAmt = self.takeInput(('1', '2', '3', '4', '5', '6', '7'), '\n*** MAKE BET ***\n\n1. $1.00\n2. $2.50\n3. $5.00\n4. $25.00\n5. $50.00\n6. $100.00\n7. $500.00\n\nEnter choice: ')
        for k, v in betAmounts.items():
            if betAmt == k:
                self.originalBet = v
        Player.cash -= self.originalBet

    def play(self):
        returnStr = []
        if self.hand.chkSplit() and self.hand.chkDouble() and not self.isSplit and not self.hand.hasDoubled:
            option = self.takeInput(('1', '2', '3', '4'), '\n1. Hit\n2. Stand\n3. Split\n4. Double Down\n\nEnter choice: ')
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
            option = self.takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Split\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
                returnStr.append('H')
            elif option == '2':
                returnStr.append('S')
            else:
                self.split()
                returnStr.append('SP')
        elif self.hand.chkDouble() and not self.hand.hasDoubled:
            option = self.takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
                returnStr.append('H')
            elif option == '2':
                returnStr.append('S')
            else:
                self.hand.doubleDown()
                returnStr.append('D')
        else:
            option = self.takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
                returnStr.append('H')
            else:
                returnStr.append('S')
        if self.isSplit:
            if self.spHand.chkDouble() and not self.spHand.hasDoubled:
                option = self.takeInput(('1', '2', '3'), '\n*** FOR HAND 2 ***\n\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice: ')
                if option == '1':
                    self.spHand.hit()
                    returnStr.append('H')
                elif option == '2':
                    returnStr.append('S')
                else:
                    self.spHand.doubleDown()
                    returnStr.append('D')
            else:
                option = self.takeInput(('1', '2'), '\n*** FOR HAND 2 ***\n\n1. Hit\n2. Stand\n\nEnter choice: ')
                if option == '1':
                    self.spHand.hit()
                    returnStr.append('H')
                else:
                    returnStr.append('S')
        return returnStr
            
        


class Game:
    def __init__(self):
        deck.shuffle()
        self.player = Player()
        self.dealer = Dealer(self.player.hand[0])
    
    def __str__(self):
        if not self.dealer.isSplit and not self.player.isSplit:
            return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your Hand ***\n' + self.player.hand.__str__()
        if self.player.isSplit and not self.dealer.isSplit:
            return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** Your 2nd Hand ***\n' + self.player.spHand.__str__()
        if self.dealer.isSplit and not self.player.isSplit:
            return "*** Dealer's 1st Hand ***\n" + self.dealer.hand.__str__() + "\n*** Dealer's 2nd Hand ***\n" + self.dealer.spHand.__str__() + '\n\n*** Your Hand ***\n' + self.player.hand.__str__()
        if self.player.isSplit and self.dealer.isSplit:
            return "*** Dealer's 1st Hand ***\n" + self.dealer.hand.__str__() + "\n*** Dealer's 2nd Hand ***\n" + self.dealer.spHand.__str__() + '\n\n*** Your 1st Hand ***\n' + self.player.hand.__str__() + '\n*** Your 2nd Hand ***\n' + self.player.spHand.__str__()
    
    def eitherBlackjack(self):
        if self.player.hand.chkBlackjack():
            return '*** YOU HAVE BLACKJACK! YOU WIN! ***'
        elif self.dealer.hand.chkBlackjack():
            return '*** DEALER HAS BLACKJACK! DEALER WINS! ***'
        else:
            return ''
    
    def play(self):
        self.lastDealerMove = self.dealer.play()
        while True:
            print(self)
            self.lastPlayerMove = self.player.play()
            if self.lastPlayerMove == ['S'] or self.lastPlayerMove == ['S', 'S'] or self.player.totalBust():
                break
        
    def finishGame(self):
        playerResults = []
        dealerResults = []
        if 'YOU' in self.eitherBlackjack():
            self.player.hand.endRound('B')
        if 'DEALER' in self.eitherBlackjack():
            self.dealer.hand.endRound('B')
        else:
            if self.player.isSplit:
                if not self.player.spHand.chkBreak():
                    playerResults.append(self.player.spHand)
            if not self.player.hand.chkBreak():
                playerResults.append(self.player.hand)
            if self.dealer.isSplit:
                if not self.dealer.spHand.chkBreak():
                    dealerResults.append(self.dealer.spHand)
            if not self.dealer.hand.chkBreak():
                dealerResults.append(self.dealer.hand)
            bestP = max(playerResults.points)
            bestD = max(dealerResults.points)
            if bestP > bestD:
                bestP.endRound('W')
            else:
                bestD.endRound('W')
                        

                
        
        



print('\n*** Blackjack ***')

while True:
    currentGame = Game()
    print(currentGame.player)

    if currentGame.eitherBlackjack():
        print(currentGame.eitherBlackjack())
        currentGame.finishGame()
    else:
        currentGame.play()
        currentGame.finishGame()
    
    cont = Player.takeInput(('y', 'n'), 'Play again? (y/n) ')
    if cont == 'n':
        break
