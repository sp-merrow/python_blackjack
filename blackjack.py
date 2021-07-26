from random import randint

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []

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
        return self.pop(randint(0, (len(self)-1)))

deck = Deck()


class Hand(list):
    def __init__(self, isDealer):
        self.points = 0
        self.isDealer = isDealer
        for i in range(2):
            self.append(deck.getRandom())
        if self.isDealer: #if this is the dealer's hand, show only one card face up
            self[1].isFlipped = True
        for card in self:
            self.points += card.points


    def chkAce(self):
        aceList = [i for i in self if i.face == 'A']
        aceList = iter(aceList)
        while self.points > 21:
            try:
                next(aceList).points = 1
            except StopIteration:
                break


    def chkBreak(self):
        self.chkAce()
        if self.points > 21:
            return True
        else:
            return False



    def hit(self):
        newCard = deck.getRandom()
        self.points += newCard.points
        self.append(newCard)
        self.chkAce()
    
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
    def __init__(self, dumb):
        self.hand = Hand(True)
        self.dumb = dumb
    
    def considerAce(self):
        aceList = [i for i in self if i.face == 'A']
        if aceList:


    
    def play(self, pHand):
        if self.dumb == True:
            if self.hand.points <= 17:
                self.hand.hit()
        else:
            faceUpCard = pHand[0]
            if faceUpCard.face == 'A' or faceUpCard.points in range(7, 11):
                if self.points < 17:
                    self.hand.hit()
            elif faceUpCard.points in range(4, 7):
                if self.points < 12:
                    self.hand.hit()
            else:
                if self.points < 13:
                    self.hand.hit()
        


class Game:
    def __init__(self):
        deck.shuffle()
        self.dealer = Dealer()
        self.playerHand = Hand(False)
    
    def __str__(self):
        return "*** Dealer's Hand ***\n" + self.dealerHand.__str__() + '\n\n*** Your Hand ***\n' + self.playerHand.__str__()


        

g = Game()
print(g)