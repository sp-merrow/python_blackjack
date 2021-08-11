class improperDeck(Exception):
    def __str__(self):
        return 'Deck not properly initialized.'

class forcedCardNotFound(Exception):
    def __str__(self):
        return 'forceDraw method in class Deck could not find requested cards.'

class endRoundError(Exception):
    def __init__(self, user, win):
        self.user = user
        self.win = win

    def __str__(self):
        return f'endRound method for {self.user} in class Hand was invoked with an invalid win status.\nWin status given: {self.win}'

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
    def __init__(self, errorType, extra):
        self.errorType = errorType
        self.extra = extra

    def __str__(self):
        if self.errorType == 1:
            return 'Error in finishGame method in class Game, all game states exhausted.'
        if self.errorType == 2:
            return f'Error in addResult function in finishGame method, win status of "{self.extra}" is invalid.'

class winStatusError(Exception):
    def __init__(self, winList):
        self.winList = winList
    
    def __str__(self):
        wins = ''
        for i in self.winList:
            wins += '\n' + i
        return f'Error in endgameStr method in class Game, winStatus received: {wins}'