from player import Player
import tiles

# Implements wrapper actions for all possible actions in the form of classes.
# The parent class is Action(), and all other actions are based off of this
# basic class.

# Every action in the game, with the exception of help and info (which are
# dealt with directly in the parser) has its own class in actions.py

# These actions have an associated method in player.py, and it is this method
# that is used to actually implement the action in the game.

# Instances of the action classes are created in tiles.py with the appropriate
# parameters filled in.

# Note: if an action is changed, it must also be changed in player.py
# and in tiles.py in any rooms that call that action.

class Action():
    """The basic or parent class for all actions.
    All actions have:
        method: an associated method in player.py
        noun: the object or thing to which the action is applied
        verbs: a list of the acceptable verbs to call this action
        kwargs: the keyword arguments needed to call the method in player.py"""
    def __init__(self, method, verbs, noun, **kwargs):
        self.method = method
        self.noun = noun # the noun to apply the action to
        self.verbs = verbs
        self.kwargs = kwargs

    def __str__(self):
        """Allow printing of the verb and noun pairs, for convenience.
        Printing is in the form 'verb, noun'. For example: 'move, west'"""
        for n in self.verbs:
            return "{}, {}".format(n, self.noun)

    def add_actions(self):
        """Used to add an action to the dictionary of moves that is passed
        to the parser. The dictionary requires both a noun and a list of
        verbs."""
        return self.noun, self.verbs

class MoveNorth(Action):
    """Allows the player to move to an adjacent tile to the north."""
    def __init__(self):
        super().__init__(method=Player.move_north,
                        verbs=["move", "go", "travel"],
                        noun="north")


class MoveSouth(Action):
    """Allows the player to move to an adjacent tile to the south."""
    def __init__(self):
        super().__init__(method=Player.move_south,
                        verbs=["move", "go", "travel"],
                        noun="south")


class MoveEast(Action):
    """Allows the player to move to an adjacent tile to the east."""
    def __init__(self):
        super().__init__(method=Player.move_east,
                        verbs=["move", "go", "travel"],
                        noun="east")


class MoveWest(Action):
    """Allows the player to move to an adjacent tile to the west."""
    def __init__(self):
        super().__init__(method=Player.move_west,
                        verbs=["move", "go", "travel"],
                        noun="west")


class ViewInventory(Action):
    """Prints the player's inventory."""
    def __init__(self):
        super().__init__(method=Player.print_inventory,
                        verbs=["view", "look"],
                        noun="inventory")

class ViewOrbs(Action):
    """Prints the player's orb list in battle."""
    def __init__(self):
        super().__init__(method=Player.print_orbs,
                        verbs=["view", "look"],
                        noun="orbs")

class PickUp(Action):
    """Used to pick up an item.

    Attributes (in addition to those of the parent class):
        item: the item to be taken, which is the instance of a class in items.py
        tile: the room in which the item exists (which must be modified when the
            item is taken)
        """
    def __init__(self, item, tile):
        super().__init__(method=Player.add_loot,
                        verbs=["pick", "take", "grab"],
                        noun=item.name,
                        item=item,
                        tile=tile)


class Attack(Action):
    """Used to initiate each round of combat.

    Attributes:
        enemy: the enemy to be attacked
        tile: the room in which the enemy exists
        weapon: The weapon to use when attacking the enemy.
                The weapon can be set to None if no weapon is specified."""
    def __init__(self, enemy, tile, weapon):
        super().__init__(method=Player.attack,
                        noun=enemy.name,
                        verbs=["attack", "hit", "kill", "hurt","battle","beat"],
                        enemy=enemy,
                        tile=tile,
                        weapon=weapon)

class Cast(Action):
    """Used to cast an orb in battle. Orbs can only be cast on the player.
    Attributes:
        orb: the orb to be cast"""
    def __init__(self, orb):
        super().__init__(method=Player.cast_orb,
                        verbs=["cast", "put"],
                        noun=orb.name,
                        orb=orb)

class ChangeWeapon(Action):
    """Allows the player to change the weapon that they currently have equipped.
    The new weapon replaces any old ones.

    Attributes:
        weapon: the weapon to be equipped."""
    def __init__(self):
        super().__init__(method=Player.choose_weapon,
                        verbs=["change", "choose", "switch"],
                         noun="weapon")

class Look(Action):
    """Enables the player to look at objects in the room or around the room
    in general.

    Attributes:
        tile: the room to look around in"""
    def __init__(self, tile, noun):
        super().__init__(tile=tile,
                        method=Player.look,
                        verbs=["look"],
                        noun=noun,
                        item=noun)

class Shop(Action):
    """Allows the player to begin shopping in the store.

    Attributes:
        tile: any tile in which a shop exists, in this case TownShop"""
    def __init__(self, tile):
        super().__init__(method=Player.shop,
                        verbs=["shop"],
                        noun=None,
                        tile=tile)

class UsePotion(Action):
    """Enables the player to use a potion.

    Attributes:
        tile: the current room
        enemy: an enemy being fought"""
    def __init__(self, potion, tile, enemy):
        super().__init__(method=Player.use_potion,
                        verbs=["use"],
                        noun=potion.name,
                        potion=potion,
                        tile=tile,
                        enemy=enemy)

class Flee(Action):
    """Enables the player to flee to an adjacent tile during a battle. The
    player cannot flee beyond an enemy, but can retreat back the way they came.

    Attributes:
        direction: an optional direction in which to flee
        enemy: the enemy to flee from"""
    def __init__(self, noun, enemy, direction):
        super().__init__(method=Player.flee,
                        verbs=["flee", "run", "escape"],
                        noun=noun,
                        enemy=enemy,
                        direction=direction)
