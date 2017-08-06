from game import *


class GameScreen:
    '''Display the current state of a game in a text-based format.
    This class is fully implemented and needs no
    additional work from students.'''

    def initialize_game(self):
        '''(GameScreen) -> NoneType
        Initialize new game with new user-selected hero class
        and starting room files.'''

        hero = None
        while hero is None:
            c = input("Select hero type:\n(R)ogue (M)age (B)arbarian\n")
            c = c.lower()
            if c == 'r':
                hero = Rogue()
            elif c == 'm':
                hero = Mage()
            elif c == 'b':
                hero = Barbarian()

        self.game = Game("rooms/startroom", hero)

    def play(self):
        '''(Game) -> NoneType
        The main game loop.'''

        exit = False
        while not exit:
            print(self)
            if self.game.game_over():
                break
            c = input("Next: ")
            if c in ['q', 'x']:
                print("Thanks for playing!")
                exit = True
            elif c == 'w':  # UP
                self.game.move_hero(-1, 0)
            elif c == 's':  # DOWN
                self.game.move_hero(1, 0)
            elif c == 'a':  # LEFT
                self.game.move_hero(0, -1)
            elif c == 'd':  # RIGHT
                self.game.move_hero(0, 1)
            elif c == 'r':
                ## RESTART GAME
                self.initialize_game()
            else:
                pass

    def __str__(self):
        '''(GameScreen) -> NoneType
        Return a string representing the current room.
        Include the game's Hero string represetation and a
        status message from the last action taken.'''

        room = self.game.current_room
        s = ""

        if self.game.game_over():
            #render a GAME OVER screen with text mostly centered
            #in the space of the room in which the character died.

            #top row
            s += "X" * (2 + room.cols) + "\n"
            #empty rows above GAME OVER
            for i in list(range(floor((room.rows - 2) / 2))):
                s += "X" + " " * room.cols + "X\n"
            # GAME OVER rows
            s += ("X" + " " * floor((room.cols - 4) / 2) +
                "GAME" + " " * ceil((room.cols - 4) / 2) + "X\n")
            s += ("X" + " " * floor((room.cols - 4) / 2) +
                "OVER" + " " * ceil((room.cols - 4) / 2) + "X\n")
            #empty rows below GAME OVER
            for i in list(range(ceil((room.rows - 2) / 2))):
                s += "X" + " " * room.cols + "X\n"
            #bottom row
            s += "X" * (2 + room.cols) + "\n"
        else:
            for i in range(room.rows):
                for j in room.grid[i]:
                    if j is not None:
                        if j.visible:
                            s += j.symbol()
                        else:
                            #This is the symbol for 'not yet explored' : ?
                            s += "?"
                s += "\n"
        #hero representation
        s += str(self.game.hero)
        #last status message
        s += room.status
        return s

if __name__ == '__main__':
    gs = GameScreen()
    gs.initialize_game()
    gs.play()
