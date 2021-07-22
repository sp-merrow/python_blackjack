from random import randint

suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
cardsInPlay = []

with open('card_template.txt', 'r', encoding='utf-8') as ct:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    



class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
    
    def __str__(self):
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

class Deck(list):
    def shuffle(self):
        with open('cards.txt', 'r') as d:
            for c in d:
                c = c.replace('\n', '')
                c = c.split('|')
                self.append(Card(c[1], c[2]))
    
    def getRandom(self):
        return self.pop(randint(0, len(self)-1))

deck = Deck()


class Hand(list):
    def __init__(self):
        for i in range(2):
            self.append(deck.getRandom())

    def hit(self):
        self.append(deck.getRandom())
    
    def __str__(self):
        tempAdd = []
        fullHand = ''
        for card in self:
            tempAdd.append(card.__str__()) #add a list within tempAdd to append str onto
        

        for c, item in enumerate(tempAdd):
            if c < len(tempAdd):
                tempAdd[c] = tempAdd[c].replace('\n', '') + tempAdd[c+1]



        for i in tempAdd:
            fullHand += ''.join(i)
            
        
        return fullHand
        


while True:
    deck.shuffle()
    currentHand = Hand()
    dealerHand = Hand()

    print('DEALER')
    print(dealerHand)
    
    print('\nUSER')
    print(currentHand)
    
    break
