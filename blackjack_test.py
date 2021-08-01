from blackjack import *
import unittest

player = Player()

class testBlackjack(unittest.TestCase):
    def test_makeCopy(self):
        self.assertNotEqual(player.hand.__str__(), player.hand.makeCopy()) 