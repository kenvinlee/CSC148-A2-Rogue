from hero import *
from room import *
from screen import *

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
CENTRE = 4


class Game:
    '''The controller class that keeps track of the current room
    the hero is in, the screen it should display to, etc. '''

    def __init__(self, mapname, hero):
        '''(Game, str, Hero) -> NoneType
        Create a new Game given the name of an initial room
        to load and a Hero object. mapname excludes extension.'''

        self.current_room = self.load(mapname)
        self.hero = hero
        self.room_list = []
        # start hero in position 4 (center)
        # corresponding to Room.locations[4]

        self.current_room.add_hero(self.hero, CENTRE)

    def game_over(self):
        '''(Game) -> NoneType
        Return True iff hero's hit points are 0 or less.'''

        return self.hero.hp <= 0

    def load(self, mapname):
        '''(Game, str) -> Room
        Append .map to mapname and open corresponding file.
        Create a new Room with appropriately placed walls.
        Precondition: file is a valid map format file.'''

        if mapname == "None":
            return
        mapfile = open(mapname + ".map", "r")
        walls = []
        row = 0

        assert mapfile.readline() == "MAPSTART\n"
        currline = mapfile.readline()
        while currline != "MAPFINISH\n":
            for col in range(len(currline)):
                if currline[col] == 'X':
                    walls.append((row, col))
            currline = mapfile.readline()
            row += 1

        #create Room
        room = Room(self, walls)

        #begin populating with items
        assert mapfile.readline() == "ITEMS\n"
        currline = mapfile.readline()

        #Agghhhhh
        while currline != "MONSTERS\n":
            #item parsing code
            item_stats = []
            item_stats = currline.split(',')
            item = Item(item_stats[0], int(item_stats[1]), int(item_stats[2]),\
                        int(item_stats[3]))
            room.add(item, int(item_stats[4]), int(item_stats[5]))
            currline = mapfile.readline()
        currline = mapfile.readline()

        while currline != "ENDFILE":
            # ADD MONSTER PARSING CODE HERE
            mons_stats = []
            mons_stats = currline.split(',')
            mons = Monster(mons_stats[0], int(mons_stats[1]), \
                           int(mons_stats[2]))
            room.add(mons, int(mons_stats[3]), int(mons_stats[4]))
            currline = mapfile.readline()
        mapfile.close()

        # PROCESS .links FILES HERE
        link_file = open(mapname + ".links", "r")
        links = []
        rooms = []
        north_door = Door(NORTH)
        south_door = Door(SOUTH)
        east_door = Door(EAST)
        west_door = Door(WEST)
        currline = link_file.readline()

        while currline != '':
            currline = currline.rstrip('\n')
            links.append(currline)
            currline = link_file.readline()

        for i in range(len(links)):
            if links[i] != "None" and links[i] != "Done":
                linked_room = self.load(links[i])
                room.dir_links[i] = linked_room
                linked_room.dir_links[self.switch_dir(i)] = room
                if i == NORTH:
                    room.add(north_door, 0, 10)
                elif i == SOUTH:
                    room.add(south_door, 10, 10)
                elif i == EAST:
                    room.add(east_door, 5, 20)
                elif i == WEST:
                    room.add(west_door, 5, 0)

            elif links[i] == "Done":
                if i == NORTH:
                    room.add(north_door, 0, 10)
                elif i == SOUTH:
                    room.add(south_door, 10, 10)
                elif i == EAST:
                    room.add(east_door, 5, 20)
                elif i == WEST:
                    room.add(west_door, 5, 0)
            elif links[i] == "None":
                    room.dir_links[i] = None
            else:
                return None

        return room

    def move_hero(self, x, y):
        '''(Game, int, int)
        Send a move command from the GameScreen to the current room
        to move the hero x tiles to the right and y tiles down.'''

        self.current_room.move_hero(x, y)

    def switch_dir(self, i):
        '''(Game, int) -> int
        Reverses direction'''

        if i == NORTH:
            return SOUTH
        elif i == SOUTH:
            return NORTH
        elif i == EAST:
            return WEST
        elif i == WEST:
            return EAST
        else:
            return 1
