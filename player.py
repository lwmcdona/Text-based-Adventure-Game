import items, world
import random

# Contains the player class.
# Methods within the player class are used to execute all actions in the game.

class Player():
    def __init__(self):
        """Player class to represent the player as they travel through the game.
        Attributes:
            -inventory: list containing items from the items.py class
            -hp: player's hitpoints; the game is over if they go to 0
            -location_x: map horizontal location
            -location_y: map vertical location
            -victory: boolean that indicates if the player has won the game
            -weapon: equipped weapon
            -bestbag: equipped orb container
            -prev_tile: where the player came from
            -max_hp: the player's max possible
        """
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
        self.weapon = None
        self.bestbag = None
        self.prev_tile = None
        self.max_hp = 100

    def available_weapons(self):
        """Returns a list of weapons in the player's inventory"""
        return [item for item in self.inventory if isinstance(item, items.Weapon)]

    def available_bags(self):
        """Returns a list of bags (used to store orbs in battle) in the player's
           inventory"""
        return [item for item in self.inventory if isinstance(item, items.OrbContainer)]

    def available_potions(self):
        """Returns a list of potions in the player's inventory"""
        return [item for item in self.inventory if isinstance(item, items.Potion)]

    def available_gold(self):
        """Returns the gold item in the inventory. There should only be one."""
        gold_list = [item for item in self.inventory if isinstance(item, items.Gold)]
        if len(gold_list) == 1:
            return gold_list[0]

    def is_alive(self):
        """Returns true if the player is alive and false if not. If false,
        the game ends."""
        return self.hp > 0

    def print_inventory(self):
        """Prints all items in the player's inventory"""
        for item in self.inventory:
            print(item, '\n')

    def print_orbs(self):
        """Prints all of the player's current orbs"""
        print()
        if self.bestbag == None or len(self.bestbag.orb_list) == 0:
            print("""You currently have no orbs. They will be summoned when
            attacking.""")

        else:
            print("Your orbs:")
            for item in self.bestbag.orb_list:
                print(item.name)

            if not self.weapon.orb == None:
                print("Your current weapon orb is {}".format(self.weapon.orb.name))

            print()

    def move(self, dx, dy):
        """Moves the player to the appropriate map tile.
        Args:
            dx: integer change in room longitude
            dy: integer change in room latitude
        """
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        """Moves the player north and sets the prev_tile to south"""
        self.move(dx=0, dy=-1)
        self.prev_tile = "south"

    def move_south(self):
        """Moves the player south and sets the prev_tile to north"""
        self.move(dx=0, dy=1)
        self.prev_tile = "north"

    def move_east(self):
        """Moves the player east and sets the prev_tile to west"""
        self.move(dx=1, dy=0)
        self.prev_tile = "west"

    def move_west(self):
        """Moves the player west and sets the prev_tile to east"""
        self.move(dx=-1, dy=0)
        self.prev_tile = "east"

    def add_loot(self, tile, item):
        """Adds the loot from a tile (required to be a LootRoom) to the player's
           inventory
        Args:
            -tile: an instance of LootRoom containing the item
            -item: an instance of Item class to add to the player's inventory"""
        self.inventory.append(item)
        tile.picked_up = True
        print(tile.picked_up_text())

    def choose_weapon(self):
        """Allows the player to choose a weapon to wield from their available
           weapons"""
        weapons = self.available_weapons()
        print("Available weapons:")

        for i in weapons:
            print(i.name)

        weapon_str = input("Weapon: ").lower()
        chosen_weapon = None

        while chosen_weapon == None:
            for weapon in weapons:
                if weapon.name == weapon_str:
                    chosen_weapon = weapon

            if chosen_weapon == None:
                weapon_str = input("You don't have a {}. Choose a weapon: ".format(weapon_str)).lower()

        print("""
            Your weapon is now a {}
            """.format(chosen_weapon.name))

        self.weapon = chosen_weapon

    def choose_best_bag(self):
        """Chooses the bag from the player's inventory with the largest capacity"""
        bags = self.available_bags()

        if self.bestbag == None:
            max_cap = 0

        else:
            max_cap = self.bestbag.capacity

        for item in bags: # find the bag with the highest capacity in inventory
            if item.capacity > max_cap:
                max_cap = item.capacity
                item.orb_list = []
                self.bestbag = item

    def enemy_orb_summon(self, enemy):
        """Fills the enemies orb bag to its capacity.
        Args:
            enemy: an instance of the Enemy class native to a particular room
        """
        # make sure the enemy list is empty to start a battle
        if enemy.orb == None:
            enemy.orb_list = []

        print(enemy.orb_list)

        if not enemy.capacity == len(enemy.orb_list):
            print("{} summons {} orb(s):".format(enemy.name, enemy.capacity - len(enemy.orb_list)))

            for i in range(enemy.capacity - len(enemy.orb_list)):
                num = random.randint(1,4)
                orb = items.Orb.num_to_orb(num)
                enemy.orb_list.append(orb)
                print(orb.name)

            print()

    def orb_summon(self):
        """Fills the player's orb bag to its capacity"""
        if not self.bestbag.capacity == len(self.bestbag.orb_list):
            print("You summon {} orb(s) from your surroundings:".format(self.bestbag.capacity - len(self.bestbag.orb_list)))

            for i in range(self.bestbag.capacity - len(self.bestbag.orb_list)):
                num = random.randint(1,4)
                orb = items.Orb.num_to_orb(num)
                self.bestbag.orb_list.append(orb)
                print(orb.name)

            print()

    def use_potion(self, potion, tile, enemy):
        """Heals the player. Can also be used to heal an enemy.
        Args:
            -potion: an instance of the Potion class; used to heal
            -tile: an instance of the MapTile class; the current location
            -enemy (str): the enemy name passed in from the parser
        """
        if enemy == None:
            if self.hp > 100-potion.healing: # if the potion would heal beyond full health
                print("You use potion. You are healed for {} HP! You are now at full health.".format(100-self.hp))
                self.hp = 100

            else: # if the potion heals below full health
                self.hp += potion.healing
                print("You use potion. You are healed for {} HP! You now have {} HP.".format(potion.healing,self.hp))

            self.inventory.remove(potion) # remove the potion from the inventory

        else:
            if tile.enemy.name == enemy: # the enemy in the room must match the enemy name
                enemy = tile.enemy
                max_enemy_hp = enemy.enemy_hp(enemy.name)

                if enemy.hp > max_enemy_hp - potion.healing: # if enemy is healed beyond full health
                    print("For some reason, you use potion on {}. It is healed for {} HP and is now at max health!".format(enemy.name,
                    round(max_enemy_hp-enemy.hp),max_enemy_hp))

                    enemy.hp = max_enemy_hp

                else: # if enemy would be healed below full health
                    enemy.hp += potion.healing
                    print("For some reason, you use potion on {}. It is healed for {} HP, and now has {} HP.".format(enemy.name,

                    potion.healing, round(enemy.hp)))

                self.inventory.remove(potion)

            else:
                print("There doesn't appear to be a {} to use that on.".format(enemy))

    def initial_orb_cast(self):
        """The player must initially be prompted to cast an orb on their weapon."""
        orb_str = input("Cast which orb on {}?: ".format(self.weapon.name)).lower()
        chosen_orb = None
        while chosen_orb == None:
            for orb in self.bestbag.orb_list:
                if orb_str == orb.name:
                    chosen_orb = orb
                    self.bestbag.orb_list.remove(orb) # pop the orb off the list
                    break

            if chosen_orb == None:
                orb_str = input("You don't have a {}. Choose an orb: ".format(orb_str)).lower()

        self.weapon.orb = chosen_orb

        print("You cast {} on {}\n".format(self.weapon.orb.name, self.weapon.name))

    def cast_orb(self, orb):
        """Cast an orb on the player's equipped weapon. If no weapon is specified,
        chooses a weapon first.
        Args:
            -orb: an instance of the Orb class; the orb to be cast
        """
        if self.bestbag == None:
            print("You currently have no orbs. They will be summoned in battle.")

        else:
            if self.weapon == None:
                print("Choose weapon to cast on.")
                self.choose_weapon()

            list_len = len(self.bestbag.orb_list)

            for item in self.bestbag.orb_list:
                if item.name == orb.name:
                    self.weapon.orb = item
                    self.bestbag.orb_list.remove(item)
                    print("You cast {} on {}.".format(item.name, self.weapon.name))
                    break

            if list_len == len(self.bestbag.orb_list):
                print("You don't have a {}.".format(orb.name))

    def enemy_cast(self, enemy):
        """Casts an orb from the enemy orb list onto the enemy. The cast is
        semi-intelligent with three scenarios based on a randomly generated
        number: 1: if number is less than the enemy's intelligence attribute,
                   it will choose the orb to do the most damage. This causes
                   enemies with higher intelligence to be harder to beat.
                2: if the number is 10, the player has gotten lucky, and the
                   enemy will choose an orb so the player does the most damage
                3: if the number is elsewhere, the enemy will choose an orb
                   based on a random number.
        Args:
            -enemy: an instance of the Enemy class; the enemy in the current
                    location
        """
        num = random.randint(1,10)
        found = False

        if num < enemy.intelligence: #pick the best option
            print("Enemy is smart!")

            best_list = items.Orb.best_combs(self.weapon.orb.name) # list of best combos

            for name in best_list:
                for orb in enemy.orb_list:
                    if name == orb.name:
                        enemy.orb = orb
                        enemy.orb_list.remove(orb)
                        found = True
                        break

                if found == True:
                    break

            if found == False: # in the case of silvorbs being used
                num = random.randint(0,enemy.capacity-1)
                enemy.orb = enemy.orb_list.pop(num)

        elif num == 10: # pick worst option
            print("You got lucky!")
            worst_list = items.Orb.worst_combs(self.weapon.orb.name)

            if len(worst_list) == 1: # if the worst_list is just silvorb
                # find a random orb in the inventory that is not silvorb
                orb_list = items.Orb.worst_combs('firorb')
                orb_list.remove('silvorb') #get a list with silvorb not included

                count = 0
                while count < 3: # 3 times, one for each orb other than silvorb
                    rand_orb_name = random.choice(orb_list)
                    orb_list.remove(rand_orb_name)

                    for orb in enemy.orb_list:
                        if orb.name == rand_orb_name:
                            enemy.orb = orb
                            enemy.orb_list.remove(orb)
                            found = True
                            break

                    if found == True:
                        break
                    count += 1

                if found == False: #nothing found, inventory is all silvorbs
                    enemy.orb = enemy.orb_list[0]
                    enemy.orb_list.pop(0)
                    print(enemy.orb_list)

            else:
                for name in worst_list: # elemental weapon orb, so pick the worst one
                    for orb in enemy.orb_list:
                        if name == orb.name:
                            enemy.orb = orb
                            enemy.orb_list.remove(orb)
                            found = True
                            break

                    if found == True:
                        break

        else: # pick random orb
            print("Enemy chose randomly!")
            num = random.randint(0,enemy.capacity-1)
            enemy.orb = enemy.orb_list.pop(num)
        print("{} chose {}!\n".format(enemy.name, enemy.orb.name))

    def player_damage(self, enemy):
        """Calculates player damage and subtracts from enemy hp
        Args:
            -enemy: an instance of the Enemy class; the enemy in the current
                    location
        """
        max_dmg, min_dmg = self.weapon.damagerange()
        base_damage = random.randint(min_dmg, max_dmg)
        multiplier = self.weapon.orb.damagemultiplier[enemy.orb.name]

        # this is printed to give the player some idea of how orbs
        # affect other orbs
        if multiplier > 1:
            print("{} is strong against {}!".format(self.weapon.orb.name, enemy.orb.name))
        elif multiplier < 1:
            print("{} is weak against {}!".format(self.weapon.orb.name, enemy.orb.name))
        else:
            print("You use {} against {}!".format(self.weapon.name, enemy.name))

        damage = round(base_damage * multiplier,1)
        enemy.hp = round(enemy.hp - damage,1)

        print("You did {} damage.".format(damage))

    def enemy_damage(self, enemy):
        """Calculates enemy damage and subtracts from player hp
        Args:
            -enemy: an instance of the Enemy class; the enemy in the current
                    location
        """
        enemy_base_damage = random.randint(enemy.damagemin, enemy.damagemax)

        # multiplier is based on the orb the enemy has currently cast
        multiplier = enemy.orb.damagemultiplier[self.weapon.orb.name]
        enemy_damage = round(enemy_base_damage * multiplier,1)

        self.hp = round(self.hp - enemy_damage,1)

        return enemy_damage

    def attack(self, enemy, tile, weapon=None):
        """Attack action.
        Args:
            -enemy: an instance of the Enemy class; the enemy in the current
                    location
            -tile: an instance of the MapTile class; the current location
            -weapon (str): a weapon name. Becomes the player's equipped weapon
                if it matches the name of any of the players weapons.
        """
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.choose_best_bag()

        if weapon is not None: # if a weapon is provided, assign to the equipped weapon
            for w in self.available_weapons():
                if w.name == weapon:
                    self.weapon = w

        if self.weapon == None: # otherwise, prompt the user to choose weapon if this is their first battle
            self.choose_weapon()

        # summon orbs
        self.enemy_orb_summon(enemy)
        self.orb_summon()

        # cast an orb on the equipped weapon if this is the first battle round
        if self.weapon.orb == None:
            self.initial_orb_cast()

        # enemy orb cast
        if enemy.orb == None: # pick a random orb from inventory
            num = random.randint(0,enemy.capacity-1)
            enemy.orb = enemy.orb_list.pop(num)
            print("{} chose {}!\n".format(enemy.name, enemy.orb.name))

        else: #if the enemy already has an orb, he may cast or attack
            num = random.randint(0,1)
            print()
            if num == 1: # 50% chance that enemy will cast an orb
                self.enemy_cast(enemy)

        # execute player damage on enemy
        self.player_damage(enemy)

        if not enemy.is_alive(): # battle is over, enemy is dead
            print("You killed {}!".format(enemy.name))

            # reset orb parameters
            enemy.orb = None
            enemy.orb_list = []
            if not self.weapon == None:
                self.weapon.orb = None

            if not self.bestbag == None:
                self.bestbag.orb_list = []

            # update gold
            if enemy.gold_dropped is not None:
                print("You find {} gold on the {}'s corpse!".format(enemy.gold_dropped, enemy.name))
                gold = self.available_gold()
                gold.value = gold.value + enemy.gold_dropped

            #victory is achieved if the dragon has been killed
            tile.victory = True
            if enemy.name == "dragon":
                self.victory = True
        else: # enemy is alive
            print("{} HP is {}.".format(enemy.name, enemy.hp))
            enemy_damage = self.enemy_damage(enemy)

            print("{} does {} damage.".format(enemy.name, enemy_damage))
            if self.hp > 0: #enemy and player are still alive, continue battle by summoning new orbs
                print("You have {} HP remaining.\n".format(self.hp))
                self.enemy_orb_summon(enemy)
                self.orb_summon()
            else: #player has died
                print("You have 0 HP. Your quest is over...")
                self.victory = False

    def look(self, tile, item):
        """Calls the Look method in the given tile. This prints flavour text
        about the given item that is specific to that room."""
        tile.Look(item)

    def flee(self, enemy, direction):
        """From a EnemyRoom, moves the player back in the direction from which
        they entered.
        Args:
            -enemy: an instance of the Enemy class; the enemy in the current
                    location
            -direction (str): the direction in which to move the player
        """
        enemy.orb = None
        enemy.orb_list = []
        if self.weapon:
            self.weapon.orb = None
        if self.bestbag: # orbs are transient, so empty the bag before fleeing
            self.bestbag.orb_list = []

        if direction == "north":
            self.move_north()
        if direction == "south":
            self.move_south()
        if direction == "west":
            self.move_west()
        if direction == "east":
            self.move_east()

    def shop(self, tile):
        """Runs the shop method in the ShopKeeper class"""
        tile.NPC.shop(self, tile)

    def do_action(self, action, **kwargs):
        """Execute a given action."""
        # get the attributes of the given action
        action_method = getattr(self, action.method.__name__)
        if action_method:
            # Call it using **kwargs to be able
            # to use variable lengths of arguments.
            # This method allows us to call all possible functions from
            # the same location without knowing in advance which one we
            # are calling.
            action_method(**kwargs)
