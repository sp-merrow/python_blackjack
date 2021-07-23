from random import randint

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
cardsInPlay = []

with open('card_template.txt', 'r', encoding='utf-8') as ct:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    



class Card:
    def __init__(self, suit, face, isFlipped):
        self.suit = suit
        self.face = face
        self.isFlipped = isFlipped
    
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
        self.isDealer = isDealer
        for i in range(2):
            self.append(deck.getRandom())
        if self.isDealer:
            for card in self:
                card.isFlipped = True
        else:
            self[1].isFlipped = True

    def hit(self):
        self.append(deck.getRandom())
    
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
        

class Game:
    def __init__(self):
        deck.shuffle()
        self.dealerHand = Hand(True)
        self.playerHand = Hand(False)
        

g = Game()
print(g.dealerHand)