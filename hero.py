from tile import *


class Hero(Tile):
    '''A class representing the hero venturing into the dungeon.
    Heroes have the following attributes: a name, a list of items,
    hit points, strength, gold, and a viewing radius. Heroes
    inherit the visible boolean from Tile.'''

    def __init__(self, name, bonuses=(0, 0, 0)):
        '''(Hero, str, list) -> NoneType
        Create a new hero with name name,
        an empty list of items and bonuses to
        hp, strength, gold and radius as specified
        in bonuses'''

        self.name = name
        self.items = []
        self.hp = 10 + bonuses[0]
        self.strength = 3 + bonuses[1]
        self.radius = 1 + bonuses[2]
        Tile.__init__(self, True)

    def symbol(self):
        '''(Hero) -> str
        Return the map representation symbol of Hero: O.'''

        #return "\u263b"
        return "O"

    def __str__(self):
        '''(Item) -> str
        Return the Hero's name.'''

        return "{}\nHP:{:2d} STR:{:2d} RAD:{:2d}\n".format(
                    self.name, self.hp, self.strength, self.radius)

    def take(self, item):
        '''ADD SIGNATURE HERE
        Add item to hero's items
        and update their stats as a result.'''

        # IMPLEMENT TAKE METHOD HERE
        self.hp += item.hp
        self.strength += item.strength
        self.radius += item.rad
        self.items.append(item.name)

    def fight(self, baddie):
        '''ADD SIGNATURE HERE -> str
        Fight baddie and return the outcome of the
        battle in string format.'''

        # Baddie strikes first
        # Until one opponent is dead
            # attacker deals damage equal to their strength
            # attacker and defender alternate
        while(baddie.hp > 0 and self.hp > 0):
            self.hp -= baddie.strength
            baddie.hp -= self.strength
        if self.hp < 0:
            return "Killed by "
        else:
            return "Defeated "


class Mage(Hero):
    '''A mage class that has better sight than all heroes, but with
    weaker strength and constitution'''

    def __init__(self):
        Hero.__init__(self, "Mage", bonuses=(-2, -1, 2))


class Rogue(Hero):
    '''A rogue class that has better sight than all heroes, but with
        weaker constitution'''

    def __init__(self):
        Hero.__init__(self, "Rogue", bonuses=(0, -1, 1))


class Barbarian(Hero):
    '''A Barbarian class that has greater constitution than all heroes'''

    def __init__(self):
        Hero.__init__(self, "Barbarian", bonuses=(2, 0, 0))
