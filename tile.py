class Tile:
    '''Anything that takes up one square tile on the map.
    The default tile is empty space.'''

    def __init__(self, vis=False):
        '''(Tile, bool, bool) -> NoneType
        Construct a new tile. If penetrate is True,
        the tile can be stepped on by the Hero.
        self.visible is set to True once the Hero
        has uncovered that tile.'''

        self.visible = vis

    def symbol(self):
        '''(Tile) -> str
        Return the map representation symbol for Tile.'''

        return " "


class Wall(Tile):
    '''A subclass of Tile that represents an impassable wall.'''

    def __init__(self):
        '''(Wall) -> NoneType
        Construct an impenetrable Tile'''

        Tile.__init__(self)

    def symbol(self):
        '''(Wall) -> str
        Return the map representation symbol for Wall: X.'''

        #return "\u2588"
        return "X"


class Item(Tile):
    def __init__(self, name, hp, strength, rad):
        '''(Item, str, int, int, int) -> None
        Construct an item that can be picked up'''

        Tile.__init__(self)
        self.name = name
        self.hp = hp
        self.strength = strength
        self.rad = rad

    def symbol(self):
        '''(Item) -> str
        Return map representation for Item: I'''
        return "I"


class Monster(Tile):
    def __init__(self, name, hp, strength):
        '''(Monster, str, int, int, int) -> None
        Construct an evil monster that fights you'''

        Tile.__init__(self)
        self.name = name
        self.hp = hp
        self.strength = strength

    def symbol(self):
        '''(Monster) -> str
        Return map representation for Monster: M.'''
        return "M"


class Door(Tile):
    '''A subclass of Tile that represents an impassable wall.'''

    def __init__(self, d):
        '''(Door) -> NoneType
        Construct a Door to another room'''
        self.direction = d
        Tile.__init__(self)

    def symbol(self):
        '''(Door) -> str
        Return the map representation symbol for Door: /.'''

        return "/"
