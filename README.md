Game is now in a playable state, still working on interface as well as ironing out remaining bugs.

Current WIPS:
-Ironing out bugs in finishGame method in class Game, sometimes displays wrong win status
(hopefully fixed this by changing finishGame method from dict based to list based)
-Fixing bug in play method in class Dealer, sometimes passes a 0 as hand point value to dealer_logic.py
-Fixing minor graphical glitch when player has split and 2nd hand goes bust

The program probably won't full on crash at this stage, but no guarantees.

Game may behave strangely, such as not registering a bust, etc.

To anyone kind enough to sit down and play this for a bit:
If you experience any strange game behaviors or crashes, please post an issue on the github repo so I can find and fix the bug.

Thanks for checking out my code!