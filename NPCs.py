import random
from parser import parse
import items

# contains the NPC (non player character) classes used in the game
# the only class in use in the current version of the game is the ShopKeeper,
# but several other commented-out NPCs have been left in underneath as they
# could still be useful in a future version of the game.

# Note: the ShopKeeper's store is also located within the Shopkeeper class

class NPC():
    def __init__(self, name):
        self.name = name

    def flavour_text():
        raise NotImplementedError()

class ShopKeeper(NPC):
    def __init__(self, stock=[], bought_items=set(),
                store_items= [items.Cup(), items.Bottle(), items.Jug(), items.Case(), items.Pack()]):
        super().__init__(name="Shopkeeper")
        self.stock = stock
        self.bought_items = bought_items
        self.store_items = store_items

    def print_stock(self, player):
        print("""
        *****    IN STOCK   *****""")
        if len(self.stock) > 0:
            for i in self.stock:
                print(i)
        else:
            print("     Sorry, we're all out of stock!")

        print()

        gold_value = player.available_gold().value
        print("Your gold: {}".format(gold_value))
        print("What would you like to do?")
        print("TYPE: buy [item], sell [item], or leave store")

    def shop(self, player, tile):

        # print random intro text for the shopkeeper
        intro_text = ["Hello! Welcome to the shop!",
                    "Come in, we're open!",
                    "What would you like to buy?",
                    "You look like a fine young adventurer! Need some supplies for your journey?"]
        r = random.randint(0, len(intro_text) - 1)
        print("Shopkeeper: {}".format(intro_text[r]))

        leftover_input = None
        valid_adj = []

        while True:
            self.stock = []

            # add items to the stock only if they have not been bought by the player
            for i in self.store_items:
                if i not in self.bought_items:
                    self.stock.append(i)

            # print the stock for the player
            self.print_stock(player)

            # get moves from the TownShop tile
            moves, avail_actions, descriptors = tile.available_actions(player)

            cannot_sell = {"gold"} # a list of things that cannot be sold


            if len(player.available_weapons()) == 1:
                # if the player only has one weapon, they should
                # not be able to sell it
                cannot_sell.add(player.available_weapons()[0].name)

            if len(player.available_bags()) == 1:
                # players should not be able to sell their only orb container
                cannot_sell.add(player.available_bags()[0].name)

            for item in self.stock:
                # add the things the player can buy to moves
                if item.name in moves:
                    moves[item.name] = moves[item.name] + ["buy"]
                else:
                    moves[item.name] = ["buy"]
            for item in player.inventory:
                # add all items in the player's inventory into moves
                # items that cannot be sold are dealt with later
                if item.name in moves:
                    moves[item.name] = moves[item.name] + ["sell"]
                else:
                    moves[item.name] = ["sell"]

            # allow the player to leave the shop
            moves["store"] = ["leave"]
            moves["shop"] = ["leave"]
            moves[None] = ["leave", "stop"]

            # prevent the player from leaving the shop in other ways
            # they must stop shopping first
            for direction in ["east", "west", "north", "south"]:
                if direction in moves:
                    moves.pop(direction)

            if leftover_input == None:
                # need new input - feed a new line of input to the parser
                act, leftover_input = parse(input(), moves, valid_adj)

            else:
                # use leftover input as the new input for the parser
                act, leftover_input = parse(leftover_input, moves, valid_adj)

            if act != 0: # act = 0 if the parser returned invalid input
                if act[0] == "buy":
                    for i in self.stock: # cycle through the items in the store
                        if i.name == act[1]:
                            # the player must have enough gold to make the purchase
                            if player.available_gold().value >= i.value:
                                # confirm the purchase
                                ans = input("Buy the {} for {} gold? (yes/no): ".format(i.name,i.value))

                                if ans == "yes":
                                    print("You buy the {} from the shopkeeper!".format(i.name))

                                    # add the item to the player's inventory
                                    player.inventory.append(i)
                                    # add the item to bought items
                                    self.bought_items.add(i)

                                    # update the player's gold
                                    player.available_gold().value = player.available_gold().value - i.value

                                elif ans == "no":
                                    print("Transaction cancelled.")

                                else:
                                    print("I don't understand. Transaction cancelled.")

                            else:
                                print("You don't have enough gold for that!")

                elif act[0] == "sell":
                    #print(act[1])
                    for i in player.inventory:
                        if i.name == act[1]:
                            if i.name in cannot_sell:
                                print("You cannot sell your only {}!".format(i.name))

                            else:
                                ans = input("Sell the {} for {} gold? (yes/no): ".format(i.name,i.value//2))
                                if ans == "yes":
                                    print("You sell your {} to the shopkeeper!".format(i.name))
                                    player.inventory.remove(i)

                                    # update the player's gold
                                    player.available_gold().value = player.available_gold().value + i.value//2

                                    self.store_items.append(i)

                                elif ans == "no":
                                    print("Transaction cancelled.")

                                else:
                                    print("I don't understand. Transaction cancelled.")

                elif act[0] == "leave" or act[0] == "stop":
                    print("Shopkeeper: Come again! The door is to your east.")
                    break

                else:
                    for action in avail_actions:

                        if act[0] in action.verbs and act[1] == action.noun:
                            # implement the action in the player class
                            player.do_action(action, **action.kwargs)

                input("Type any key to continue shopping.")

# unused NPCs due to lack of time
# class TownsPerson(NPC):
#     def __init__(self, gender = None, pronoun = None):
#         super().__init__(name =  None)
#         r = random.randint(0,2)
#         if r == 0:
#             self.gender = "male"
#             self.pronoun = "He" # if in the middle of a sentence, can use tolower()
#             self.name = "Man"
#         else:
#             self.gender = "female"
#             self.pronoun = "She"
#             self.name = "Woman"
#
#
#     def flavour_text(self):
#         return "{} doesn't want to talk.".format(self.pronoun)
#
# class Riddler(NPC):
#     def __init__(self):
#         super().__init__(name="Riddler")
#
#     def riddle(self):
#         print("You shall not pass until you answer my riddle.")
#         print("The riddle is this:")
#         print("What walks on four legs in the morning, two legs in the afternoon, and three in the evening?")
#         while True:
#             ans = input("Type your answer: ")
#             if ans == "I give up":
#                 return False
#             if ans == "human":
#                 return True
#
#     def flavour_text(self):
#         if self.riddle() == True:
#             return """You beat me!"""
#         elif self.riddle() == False:
#             return """Ha ha! Wrong answer!"""
