# adapted from http://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python/

import items, enemies, actions, world, NPCs
import player

class MapTile:
    """An abstract base class to base all other
    tiles on. We will never actually call MapTile
    directly."""
    def __init__(self, x, y, visited = False, look_at = {}):
        self.x = x
        self.y = y
        self.visited = visited
        self.look_at = look_at

    def intro_text(self):
        """The introductory text to display whenever the
        player enters a tile."""
        raise NotImplementedError()

    def update(self, moves, avail_actions, action):
        """Adds an action to the moves dictionary and avail_actions list.

        For moves: checks if a noun exists in the moves dictionary and updates
        the moves dictionary accordingly. If the noun is already a key, extend
        its value to include the new_verbs. If not, add the noun:new_verbs to
        the dictionary.

        Args:
            moves: the dictionary of noun:[verbs]
            avail_actions: the list of actions from actions.py

        Returns: moves and avail_actions"""
        avail_actions.append(action)
        noun, new_verbs = action.add_actions()

        if noun in moves:
            # Needed because otherwise any actions attached to an item are
            # replaced by the new verbs. We want to add the new verbs along
            # with the other verbs
            moves[noun] = moves[noun] + new_verbs
        else:
            moves[noun] = new_verbs

        return moves, avail_actions

    def generic_moves(self, player):
        """Returns the standard moves that are available in every room.
        These include: -movement options
                       -choosing weapons
                       -viewing inventory
                       -using potions
                       -looking around at objects in room
        Args:
            player: an instance of the player class

        Returns:
            moves: dictionary mapping nouns to the verbs that can be applied to them.
            avail_actions: a list of actions from actions.py
            descriptors: dictionary mapping nouns to their respective descriptors
                        allow adjectives in commands
        """
        moves = dict() # the verbs associated with each noun
        descriptors = dict() # the adjectives associated with each noun
        avail_actions = [] # the availble actions from actions.py

        # determine the possible moves to other tiles (ie, move west)
        if world.tile_exists(self.x + 1, self.y):
            moves, avail_actions = self.update(moves, avail_actions, actions.MoveEast())

        if world.tile_exists(self.x - 1, self.y):
            moves, avail_actions = self.update(moves, avail_actions, actions.MoveWest())

        if world.tile_exists(self.x, self.y - 1):
            moves, avail_actions = self.update(moves, avail_actions, actions.MoveNorth())

        if world.tile_exists(self.x, self.y + 1):
            moves, avail_actions = self.update(moves, avail_actions, actions.MoveSouth())

        # look at inventory
        moves, avail_actions = self.update(moves, avail_actions, actions.ViewInventory())

        for potion in player.available_potions():
            moves, avail_actions = self.update(moves, avail_actions, actions.UsePotion(potion=potion, tile=self, enemy=None))

        # choose or change weapon
        moves, avail_actions = self.update(moves, avail_actions, actions.ChangeWeapon())

        moves, avail_actions = self.update(moves, avail_actions, actions.Look(noun=None, tile=self))

        for item in self.look_at:
            moves, avail_actions = self.update(moves, avail_actions, actions.Look(noun=item, tile=self))
            descriptors[item] = self.look_at[item]

        return moves, avail_actions, descriptors

    def available_actions(self, player):
        """Returns all of the available actions in a room.
        See generic_moves for parameter descriptions."""

        moves, avail_actions, descriptors = self.generic_moves(player)

        return moves, avail_actions, descriptors

    def look(self, noun=None):
        """The look command. Allows the player to look around in general (if no
        item is specified) or to look at a specific item."""
        raise NotImplementedError

class StartingLocation(MapTile):
    """ The default starting location for the game. All other map tile locations
        are in reference to this room."""
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        # set the items in the room that are available to look at
        # along with any descriptors
        self.look_at = {"crevice":[None], "cliffs":["high"], "clearing":[None], "hole":[None]}
        if self.visited == False:
            self.visited = True
            return """
            You find yourself in the middle of a clearing, with high cliffs on
            all sides.
            """
        else:
            return """
            You are now back in the same clearing in which you started.
            Nothing has changed.
            """

    def Look(self, item=None):
        if item == "cliffs":
            print("""
            The cliffs stretch up as high as you can see in all directions.
            They are far too steep to climb.""")

        elif item == "crevice":
            print("""
            A hole in the cliffs that looks just big enough for you to
            squeeze through.""")
        elif item == "clearing":
            print("""
            It's quite pretty. You consider having a picnic, but decide it would
            be better to forge onwards. Besides, you don't have any food.""")
        elif item == "hole":
            print(
            """
            It's a crevice to the west of the cliffs."""
            )
        elif item == None:
            print("""
            You see a small crevice to the west that looks like it
            might lead somewhere.""")

class ThresholdRoom(MapTile):
    """ Room to be placed just before the final boss."""
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self):
        self.look_at = {"room":["empty"]}
        return """
            The final boss room lies ahead. Proceed with caution."""

    def Look(self, item=None):
        if item == "room":
            print("""
            A completely empty room.""")
        elif item == None:
            print("""
            There is nothing here. Please move on.""")

class Road(MapTile):
    """ Room connector class. Can be used to connect two rooms together,
        but not necessary"""
    def __init__(self, x, y):
        super().__init__(x, y)

    def directions_to_travel(self):
        """Returns a list of the possible directions the player can travel
        along the road."""
        moves = [] # a list of directions, eg, east

        if world.tile_exists(self.x + 1, self.y):
            direction, verbs = actions.MoveEast().add_actions()
            moves.append(direction)
        if world.tile_exists(self.x - 1, self.y):
            direction, verbs = actions.MoveWest().add_actions()
            moves.append(direction)
        if world.tile_exists(self.x, self.y - 1):
            direction, verbs = actions.MoveNorth().add_actions()
            moves.append(direction)
        if world.tile_exists(self.x, self.y + 1):
            direction, verbs = actions.MoveSouth().add_actions()
            moves.append(direction)
        return moves

    def intro_text(self):
        """Prints the available directions to travel along the road."""
        self.look_at = {"road":["dusty"]}
        directions = self.directions_to_travel() # gets possible directions
        # prints possible directions
        if len(directions) == 1:
            directions = directions[0]
        elif len(directions) == 2:
            directions = directions[0] + " and " + directions[1]
        elif len(directions) > 2:
            directions = ", ".join(directions[0:-1]) + ", and " + directions[-1]
        return """
                You travel along the dusty road.
                It stretches off to the {}.""".format(directions)

    def Look(self, item=None):
        if item == None or item == "road":
            print("""
            Just another stretch of road.""")

class LootRoom(MapTile):
    """ Base class for rooms containing items:
        Attributes:
            -picked_up(bool): whether or not an item has been picked_up
            -item: an instance of an item class, the actual item
    """

    def __init__(self, x, y, item, picked_up=False):
        self.picked_up = picked_up
        self.item = item
        super().__init__(x, y)

    def available_actions(self, player):
        """Returns all of the available actions in this room."""
        moves, avail_actions, descriptors = self.generic_moves(player)

        if self.picked_up == False:
            if self.item.name == "pouch":
                moves.pop("west")

            moves, avail_actions = self.update(moves, avail_actions, actions.PickUp(item=self.item, tile=self))

        return moves, avail_actions, descriptors

    def picked_up_text(self):
        raise NotImplementedError

class PlayersHouse(LootRoom):
    """ Room containing the suit of armour. """
    def __init__(self, x, y):
        super().__init__(x, y, items.SuitofArmour())

    def intro_text(self):
        if self.picked_up == False:
            self.look_at = {"armour":["suit of"], "house":[None], "rug":["nice", "little"]}
            return """
            You enter a small house. It looks cosy.

            You notice some armour lying on the ground.
            """
        else:
            self.look_at = {"house":[None], "rug":["nice", "little"]}
            return """
            You are back in the small house.
            There is nothing left to take.
            """
    def Look(self, item=None):
        if item == "armour":
            print("""
            It's a very shiny suit of armour. Looks to be about your size!""")

        elif item == "house":
            print("""
            The house is pretty sparse, but still manages to look cozy. You see
            a nice little rug on the floor.""")

        elif item == "rug":
            print("""
            A rug made of cleverly-woven rags. You take a peek underneath, but
            sadly nothing was hidden there.""")

        elif item == None:
            print("""
            The house looks cosy. You feel oddly as if you have been here
            before. You take a short rest and contemplate your existence.""")

    def picked_up_text(self):
        return """
            The armour fits you perfectly, so you decide to take it with you.
        """

class PouchRoom(LootRoom):
    """Defines the room containing the pouch.
       Placement: Must be placed to the left (west) of StartingLocation with
                  only outgoing rooms being the StartingLocation to the right
                  (east) and the SalamanderRoom to left (west).
    """

    def __init__(self, x, y):
        super().__init__(x, y, items.Pouch())

    def intro_text(self):
        if self.picked_up == False:
            self.look_at = {"pouch":["small"], "dirt":["disturbed"], "clearing":["empty"]}
            return """
                You enter an empty clearing. There doesn't seem to be anything
                here, but there doesn't seem to be anywhere else to go."""

        else:
            self.look_at = {"dirt":["disturbed"]}

            return """
                You once again enter the clearing where you found the pouch.
                Nothing has changed."""

    def picked_up_text(self):
        self.picked_up = True
        return """
            You pick up the pouch and dust it off. This will be useful in
            battle. You hear a strange noise in the distance and a path reveals
            itself to the west.
            """

    def Look(self, item=None):
        if item == "dirt":
            print("""
            You brush aside the dirt and find a small pouch on the ground.
            """)

        elif item == "pouch":
            if self.picked_up == False:
                print("""
            {}""".format(self.item.description))
            else:
                print("""
            You already took the pouch.""")

        elif item == None or item == "clearing":
            if self.picked_up == False:
                print("""
            There seems to be some disturbed dirt near the edge of the clearing.
                """)
            else:
                print("""
            There is a door to the west.
                """)

class FindSwordRoom(LootRoom):
    """ Defines the room containing the sword. Swords may also be bought from
    shop."""
    def __init__(self, x, y):
        super().__init__(x, y, items.Sword())

    def intro_text(self):
        if self.picked_up == False:
            self.look_at = {"chest":["large"], "sword":["ruby-encrusted"]}
        else:
            self.look_at = {"chest":["large"]}

        return """
            You approach a huge castle. The drawbridge is down,
            proceed and enter. After wandering through several
            passages and walking past a few nondescript rooms,
            you enter a room with a large chest in the center.

            You can go south to leave the castle, or continue
            to the north.
            """

    def picked_up_text(self):
        return """
            You take the sword with you. It might come in handy.
        """

    def Look(self, item=None):
        if item == "chest":
            if self.picked_up == False:
                print("""
            You open the chest in the center of the room and find a
            ruby-encrusted sword.""")

            else:
                print("""
            You see an empty chest that used to hold a sword.""")

        elif item == "sword":
            if self.picked_up == False:
                print("""
            Looks valuable. And deadly.""")

            else:
                print("""
            You already took the sword.""")

        elif item == None:
            print("""
            There is nothing else in the room.""")

class EnemyRoom(MapTile):
    """The basic enemy room class."""
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        self.victory = False
        super().__init__(x, y)

    def available_actions(self, player):
        """Returns all of the available actions in a room containing an enemy"""
        moves, avail_actions, descriptors = self.generic_moves(player)
        movements = ["west", "east", "north", "south"]

        if self.enemy.is_alive():
            for direction in movements:
                if direction in moves:
                    moves.pop(direction)

            moves, avail_actions = self.update(moves, avail_actions,
                actions.Flee(noun=player.prev_tile, enemy=self.enemy, direction=player.prev_tile))

            moves, avail_actions = self.update(moves, avail_actions,
                actions.Flee(noun=None, enemy=self.enemy, direction=player.prev_tile))

            moves, avail_actions = self.update(moves, avail_actions,
                actions.Flee(noun=self.enemy.name, enemy=self.enemy, direction=player.prev_tile))

            moves, avail_actions = self.update(moves, avail_actions, actions.ViewOrbs())

            for potion in player.available_potions():
                moves, avail_actions = self.update(moves, avail_actions, actions.UsePotion(potion=potion, tile=self, enemy=self.enemy))

            for orb in items.Orb.orb_types():
                moves, avail_actions = self.update(moves, avail_actions, actions.Cast(orb=orb))

            moves, avail_actions = self.update(moves, avail_actions,
                        actions.Attack(enemy=self.enemy, tile=self, weapon=None))

            a = actions.Attack(enemy=self.enemy, tile=self, weapon=None)
            noun, verbs = a.add_actions()

            weapons = player.available_weapons()
            for weapon in weapons:
                moves[weapon.name] = verbs

        return moves, avail_actions, descriptors

class SalamanderRoom(EnemyRoom):
    """ Defines the battle tutorial room.
        Placement: Must be placed to the left (west) of the PouchRoom.
    """
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Salamander())

    def intro_text(self):
        self.look_at = {"salamander":["small"]}
        if not self.enemy.is_alive():
            print("""
            The salamander has returned.""")
            enemy_hp = self.enemy.enemy_hp(self.enemy.name)
            self.enemy.hp = enemy_hp

        return """
            BATTLE TUTORIAL:
            Welcome to your first battle! In every battle, orbs are summoned
            and must be cast on weapons to do damage to enemies. Orbs are only
            summoned when you attack an enemy. To do this, type
            "attack 'enemy'".
            This will prompt you to choose a weapon from your available_weapons
            and then you will summon orbs. Choose an orb to cast on that weapon.
            This will determine your damage as well as your defense type. Your
            enemy will also choose an orb to cast on itself, also determining
            its types.
            Once orbs are summoned, you can type "view orbs" to see what orbs
            you have as well as your current weapon orb. You will not be able
            to view the enemies orbs except for when they are summoned, so try
            to remember them. After looking at orbs, you can cast specific orbs
            on your weapon using "cast 'orb_name'", or, if you are satisfied
            with the current orb matchup, simply type "attack 'enemy'" again.

            Orbs: -firorb: strong against natorb, but weak against watorb
                  -watorb: strong against firorb, but weak against natorb
                  -natorb: strong against watorb, but weak against firorb
                  -silvorb: defensive orb that's strong against itself

            Note: you may flee a battle at any time, but this will reset all
            orbs in battle, including the ones on your weapon and the enemy.

            Why don't you try it out on that small salamander?
            Type "attack salamander"!
            """

    def Look(self, item=None):
        if item == "salamander":
            if self.enemy.is_alive():
                print("""
            A small salamander!""")
            else:
                print("""
            The salamander has left this world... You are somewhat sad.""")
        elif item == None:
            if self.enemy.is_alive():
                print("""
            There is nothing else in the room. Defeat the salamander to continue.""")
            else:
                print("""
            You have defeated the salamander. He will respawn if you return.""")

class DragonRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Dragon())

    def intro_text(self):
        self.look_at = {"dragon":["menacing"]}
        if self.enemy.is_alive():
            return """
            You enter the final room of the castle. It seems quiet, yet the hair
            on the back of your neck stands up. You know you are not alone.
            Suddenly, you hear movement from above. You are blown off your
            feet by an enormous gust of wind as a menacing dragon unfurls its
            wings, causing the door to slam shut. You get to your feet...
            """
        else:
            return """
            The dragon has been vanquished.
            """

    def Look(self, item=None):
        if item == "dragon":
            print("""
            A menacing dragon!""")
        elif item == None:
            print("""
            There is nothing else in the room. The door has slammed shut and
            there's no way out!""")

class GoblinRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Goblin())

    def intro_text(self):
        if not self.enemy.is_alive():
            enemy_hp = self.enemy.enemy_hp(self.enemy.name)
            self.enemy.hp = enemy_hp

        if self.enemy.is_alive():
            self.look_at = {"goblin":["devious", "devious-looking"], "dagger":[None]}
            return """
            A devious-looking goblin sits in the middle of the room polishing
            his dagger. He sees you and starts to attack!
            """
        else:
            self.look_at = {}
            return """
            You see the remnants of the dead goblin you killed.
            """
    def Look(self, item=None):
        if item == "goblin":
            print("""
            The goblin is attacking you! You should probably do something about
            that.""")
        elif item == "dagger":
            print("""
            It's sharp and pointy.""")
        elif item == None:
            print("""
            You don't see anything in the room to help you.""")

class TownSquare(MapTile):
    def __init__(self, x, y, looked_at_shop=False):
        super().__init__(x, y)
        self.looked_at_shop = looked_at_shop

    def intro_text(self):
        if self.looked_at_shop == True:
            self.look_at = {"shop":["small"], "road":["narrow"],
                    "door":[None],"sign":["open"], "items":["travelling"],
                    "window":[None], "house":[None]}

        self.look_at = {"shop":["small"], "road":["narrow"], "house":[None]}
        return """
        You arrive at a nearby town.
        To the west you can see a small shop.
        A narrow road stretches off to the north, and you see a house
        to the south."""

    def Look(self, item=None):
        if item == "shop":
            self.looked_at_shop = True
            self.look_at = {"shop":["small"], "road":["narrow"],
                    "door":[None],"sign":["open"], "items":["travelling"],
                    "window":[None], "house":[None]}
            print("""
        The shop looks like it has seen better days, but it still seems
        operational! You can see several items on display in the window
        and an open sign on the door.""")

        if item == "road":
            print("""
        The road leads off to the north.""")

        if item == "door":
            print("""
        A sturdy wooden door. It is unlocked and looks welcoming.""")

        if item == "sign":
            print("""
        The sign says
            'OPEN: Please, please, please come in!'
        Tacked below that are the words
            'Welcome, potential customers!'
        And finally, at the bottom of the sign, you can see the last line
        written desperately in black marker:
            'Really, anyone's welcome, just like, come in!'""")

        if item == "items":
            print("""
        You don't see anything particularly impressive, just some basic
        travelling items. Perhaps there are better things inside?""")

        if item == "window":
            print("""
        A plain glass window.""")

        if item == "house":
            print("""
        You're too far away to see much of the house from here.""")

        if item == None:
            print("""
        The town is small, but still boasts a single shop! You see a few houses
        nearby, but none look particularly welcoming. The houses are modest and
        none are particularly fancy.""")

class NPCRoom(MapTile):
    def __init__(self, x, y, NPC):
        super().__init__(x, y)
        self.NPC = NPC

    def available_actions(self, player):
        """Returns all of the available actions in this room."""
        moves, avail_actions, descriptors = self.generic_moves(player)
        return moves, avail_actions, descriptors

class TownShop(NPCRoom):
    def __init__(self, x, y):
        super().__init__(x, y, NPC=NPCs.ShopKeeper())

    def intro_text(self):
        self.look_at = {"shopkeeper":[None], "counter":[None]}
        return """
        You arrive at the town's single shop. It's not very impressive.
        There is a shopkeeper standing at the counter. He perks up when
        you walk in.

        ***TYPE "SHOP" TO START SHOPPING***
        """

    def available_actions(self, player):
        """Returns all of the available actions in this room."""
        moves, avail_actions, descriptors = self.generic_moves(player)


        moves, avail_actions = self.update(moves, avail_actions, actions.Shop(self))
        return moves, avail_actions, descriptors

    def Look(self, item=None):
        if item == "shopkeeper":
            print("""
            A balding, kind-looking man. Seems a bit desperate for business.""")
        elif item == "counter":
            print("""
            Just an ordinary counter.""")
        elif item == None:
            print("""
            The shop is no more impressive from the inside, but it might have
            something that could come in handy.""")

class Building(NPCRoom):
    def __init__(self, x, y):
        super().__init__(x, y, NPC=NPCs.TownsPerson())

    def intro_text(self):
        return """
        You enter one of several buildings in the town. There is someone
        inside.
        """
