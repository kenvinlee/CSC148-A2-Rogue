from tile import *
from math import floor, ceil
from game import *

ROWS = 11
COLS = 21


class Room:
    '''A class representing one of several interconnected
    Rooms that constitute the game.'''

    def __init__(self, game, walls):
        '''(Room, Game, list) -> NoneType
        Create a new Room that belongs to game game.
        Add walls at all coordinates specified as tuples (x, y) in walls.'''

        self.game = game
        self.rows = ROWS
        self.cols = COLS

        #stores the linked rooms
        self.dir_links = [None, None, None, None]

        #populate the entire grid with empty tiles first
        self.grid = [[Tile() for q in list(range(self.cols))]
            for z in list(range(self.rows))]

        #add walls as specified by the map file
        for i, j in walls:
            self.grid[i][j] = Wall()

        self.status = ""

        #specify where hero should appear if he is coming from
        #each direction: 0 - north, 1 - south, 2 - east, 3 - west
        # 4 - center

        self.locations = [(self.rows - 2, ceil(self.cols // 2)),
                        (1, ceil(self.cols // 2)),
                        (ceil(self.rows // 2), 1),
                        (ceil(self.rows // 2), self.cols - 2),
                        (ceil(self.rows // 2), ceil(self.cols // 2))]

    def update_visibility(self):
        '''(Room) -> NoneType
        Update what the hero has uncovered given his new position.'''
        self.reveal_tile(self.hero.radius, self.hero_x, self.hero_y)

    def add_hero(self, hero, where):
        '''(Room, Hero, int) -> NoneType
        Add hero hero to the room, placing him
        as specified in self.locations[where].'''

        self.hero_x, self.hero_y = self.locations[where]
        self.hero = hero
        self.grid[self.hero_x][self.hero_y] = self.hero
        self.update_visibility()

    def add(self, obj, x, y):
        '''(Room, Tile, int, int) -> NoneType
        Add Tile object obj to the room at (x, y).'''

        self.grid[x][y] = obj

    def in_grid(self, x, y):
        '''(Room, int, int) -> bool
        Return True iff coordinates (x,y) fall within the room's grid.'''

        return x >= 0 and x < self.rows and y >= 0 and y < self.cols

    def move_hero(self, x, y):
        '''(Room, int, int) -> NoneType
        Move hero to new location +x and +y from current location.
        If the new location is impenetrable, do not update hero location.'''

        newx = self.hero_x + x
        newy = self.hero_y + y
        if not self.in_grid(newx, newy) or type(self.grid[newx][newy]) == Wall:
            return

        # DOOR CODE GOES HERE
        if type(self.grid[newx][newy]) == Door:
            for i in range(4):
                if self.grid[newx][newy].direction == i:
                    self.game.current_room = self.dir_links[i]
                    self.game.current_room.add_hero(self.game.hero, i)
        else:
            self.resolve(newx, newy)
        self.update_visibility()

    def resolve(self, x, y):
        '''(Room, int, int) -> NoneType
        Resolve an encounter between a penetrable Tile and a hero.
        '''

        #Replace space hero left with a new blank Tile
        self.grid[self.hero_x][self.hero_y] = Tile(True)

        # ITEM AND MONSTER CODE GOES HERE
        if type(self.grid[x][y]) == Item:
            self.hero.take(self.grid[x][y])
            self.status = "Picked up " + self.grid[x][y].name
        elif type(self.grid[x][y]) == Monster:
            self.status = self.hero.fight(self.grid[x][y]) + \
                self.grid[x][y].name
        else:
            self.status = ""

        #update hero location
        self.hero_x = x
        self.hero_y = y
        self.grid[x][y] = self.hero

    def reveal_tile(self, radius, x, y):
        '''(int, int, int) -> None
        Recursively reveals tiles around hero with given radius'''
        if (radius == 0 and self.in_grid(x, y)):
            self.grid[x][y].visible = True
        else:
            if self.in_grid(x, y):
                self.reveal_tile(radius - 1, x + 1, y)
                self.reveal_tile(radius - 1, x - 1, y)
                self.reveal_tile(radius - 1, x, y + 1)
                self.reveal_tile(radius - 1, x, y - 1)
                self.reveal_tile(radius - 1, x + 1, y + 1)
                self.reveal_tile(radius - 1, x + 1, y - 1)
                self.reveal_tile(radius - 1, x - 1, y + 1)
                self.reveal_tile(radius - 1, x - 1, y - 1)
                
        #how to check radius...
        #should really just be a double for loop - would be more efficient than all the recursive calls
        #start at hero's coordinates, +- radius to x coordinates.
        #for every x coordinate, you +- radius to y coordinate.
