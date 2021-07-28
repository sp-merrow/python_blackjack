from random import randint
from dealer_logic import Logic

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
betAmounts = {'1':1.00, '2':2.50, '3':5.00, '4':25.00, '5':50.00, '6':100.00, '7':500.00}

with open('card_template.txt', 'r', encoding='utf-8') as ct:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    



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
            print('*** ERROR! DECK NOT PROPERLY INITIALIZED! ***')

deck = Deck()

class Hand(list):
    def __init__(self, isDealer, splitCard):
        self.points = 0
        self.isDealer = isDealer
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

    def hasAce(self):
        aceList = [i for i in self if i.face == 'A']
        if aceList:
            return True
        else:
            return False

    def chkBreak(self):
        handCopy = self.copy()
        currentPts = self.points
        aceList = [i for i in handCopy if i.face == 'A']
        aceList = iter(aceList)
        while currentPts > 21:
            try:
                next(aceList).points = 1
            except StopIteration:
                break
        if currentPts > 21:
            return True
        else:
            return False

    def chkDouble(self):
        if self.points in range(9, 12):
            return True
        else:
            return False

    def chkSplit(self):
        faces = [i.face for i in self]
        if faces[0] == faces[1]:
            return True
        else:
            return False

    def chkBlackjack(self):
        if self.points == 21:
            return True
        else:
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
        self.hand = Hand(True, None)
        self.pCard = pCard
        self.isSplit = False
        self.currentBet = betAmounts[str(randint(1, 6))]

    def split(self):
        self.spHand = Hand(False, self.hand[1])
        self.isSplit = True
    
    def parseMove(self, move, currentHand):
        if move == 'S':
            pass
        elif move == 'H':
            currentHand.hit()
        elif move == 'D':
            self.currentBet *= 2
        else:
            self.split()
        
    def play(self):
        mainLogic = Logic(self.pCard, self.hand)
        move = mainLogic.decideMove()
        if self.isSplit:
            logicTwo = Logic(self.pCard, self.spHand)
            moveTwo = logicTwo.decideMove()
            self.parseMove(moveTwo, self.spHand)
        self.parseMove(move, self.hand)


            

class Player:
    cash = 500
    def __init__(self):
        self.hand = Hand(False, None)
        self.currentBet = 0
        self.isSplit = False

    def split(self):
        self.spHand = Hand(False, self.hand[1])
        self.isSplit = True
    
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
                self.currentBet = v

    def play(self):
        if self.hand.chkSplit() and self.hand.chkDouble():
            option = self.takeInput(('1', '2', '3', '4'), '\n1. Hit\n2. Stand\n3. Split\n4. Double Down\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
            elif option == '2':
                pass
            elif option == '3':
                self.split()
            else:
                self.currentBet *= 2
        elif self.hand.chkSplit():
            option = self.takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Split\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
            elif option == '2':
                pass
            else:
                self.split()
        elif self.hand.chkDouble():
            option = self.takeInput(('1', '2', '3'), '\n1. Hit\n2. Stand\n3. Double Down\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
            elif option == '2':
                pass
            else:
                self.currentBet *= 2
        else:
            option = self.takeInput(('1', '2'), '\n1. Hit\n2. Stand\n\nEnter choice: ')
            if option == '1':
                self.hand.hit()
            else:
                pass




class Game:
    def __init__(self):
        deck.shuffle()
        self.player = Player()
        self.dealer = Dealer(self.player.hand[0])
    
    def __str__(self):
        return "*** Dealer's Hand ***\n" + self.dealer.hand.__str__() + '\n\n*** Your Hand ***\n' + self.player.hand.__str__()




        
g = Game()
print(g)
print(g.dealer.currentBet)
g.dealer.play()
print(g)
print(g.dealer.currentBet)