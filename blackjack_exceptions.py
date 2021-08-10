class improperDeck(Exception):
    def __str__(self):
        return 'Deck not properly initialized.'

class forcedCardNotFound(Exception):
    def __str__(self):
        return 'forceDraw method in class Deck could not find requested cards.'

class chkBlackjackError(Exception):
    def __str__(self):
        return 'chkBlackjack method in class Hand improperly invoked.'

class illegalSplit(Exception):
    def __init__(self, errorType):
        self.errorType = errorType
    
    def __str__(self):
        base = 'Dealer performed illegal split, '
        if self.errorType == 'c':
            return base + 'not allowed by chkSplit method.'
        if self.errorType == 'a':
            return base + 'already split.'
        if self.errorType == 'b':
            return base + 'already split and not allowed by chkSplit method.'
        if self.errorType == 'p':
            return 'Player performed illegal split.'

class parseMoveError(Exception):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return f'parseMove method in class Dealer received invalid move.\nMove received: {self.move}'

class makeBetError(Exception):
    def __str__(self):
        return 'makeBet method in class Player invoked with invalid player cash.'

class finishGameError(Exception):
    def __str__(self):
        return 'Error in finishGame method in class Game, all game states exhausted.'

class winStatusError(Exception):
    def __init__(self, winList):
        self.winList = winList
    
    def __str__(self):
        wins = ''
        for i in self.winList:
            wins += '\n' + i
        return f'Error in endgameStr method in class Game, winStatus received: {wins}'