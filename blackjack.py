suitSymbols = {'SPADE':'♠', 'CLUB':'♣', 'DIAMOND':'♦', 'HEART':'♥'}
cardTemplate = []
deck = []

with open('card_template.txt', 'r', encoding='utf-8') as ct, open('cards.txt', 'r') as d:
    for line in ct:
        cardTemplate.append(line.replace('\n', ''))
    
    for c in d:
        c = c.replace('\n', '')
        c = c.split('|')
        deck.append([c[1], c[2]])





class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __str__(self):
        fullCard = ''
        for count, line in enumerate(cardTemplate):
            if 'F' in line:
                line = line.replace('F', self.face)
            elif 'S' in line:
                line = line.replace('S', suitSymbols[self.suit])
            
            if count == 0:
                fullCard += line
            else:
                fullCard += '\n' + line
        
        return fullCard


aceHeart = Card('HEART', 'A')
print(aceHeart)