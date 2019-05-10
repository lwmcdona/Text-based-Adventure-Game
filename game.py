import world
from player import Player
from parser import parse
import actions

# This file contains the main game loop and is the main loction from where the
# parser is called.
# (Note that there is also a parser loop in the shop located in the Shopkeeper
# NPC class in NPCs.py)

# sets used for composite actions
need_weapon = {"attack", "kill", "hit", "hurt"} # eg, "hit enemy with weapon"
need_two_objects = {"use"} # eg "use potion on self"
need_enemy = {"use"}

# to be printed when the game is complete (either because the player is
# victorious or because the player has died)
victory_text = """
        You are victorious! Thanks for playing!"""
defeat_text = """
        You lose... better luck next time!"""


def play():
    world.load_tiles()
    player = Player() # create an instance of the Player class

    #These lines load the starting room and display its intro text
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())

    leftover_input = None # initially None as the parser has not yet been called

    while player.is_alive() and not player.victory:
        implemented_action = True
        room = world.tile_exists(player.location_x, player.location_y)

        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:

            # the available_actions method returns three things:
            # moves: a dictionary of noun:[valid verbs]
            # available_actions: a list of instances of available action classes
            # valid_adj: a dictionary of noun:[valid adectives]
            moves, available_actions, valid_adj = room.available_actions(player)

            if leftover_input == None:
                # need new input - feed a new line of input to the parser
                act, leftover_input = parse(input(), moves, valid_adj)
                # the parser returns any leftover input (split by the keyword
                # "and") or returns None

            else:
                # use leftover input as the new input for the parser
                act, leftover_input = parse(leftover_input, moves, valid_adj)

            if act != 0: # the parser returns 0 if the input was invalid
                implemented_action = False # used for extra error handling
                for action in available_actions:
                    # if the input was valid, act = (verb, nouns)
                    # where nouns can be None, a single noun, or a list of two nouns
                    # eg, ("attack", ["dragon", "sword"])
                    verb = act[0]
                    noun = act[1]
                    noun2 = None # the second object is initially set to None

                    if noun is not None:
                        if len(list(noun)) == 2:
                            noun = act[1][0]
                            noun2 = act[1][1]

                    if verb in action.verbs and noun == action.noun:
                        # if the parsed action matches an available action
                        implemented_action = True
                        if noun2 != None:
                            if verb in need_weapon:
                                # for example, you attack something with a weapon
                                # so a weapon is needed
                                action.kwargs["weapon"] = noun2

                            elif verb in need_enemy:
                                action.kwargs["enemy"] = noun2

                        # implement the action in the player class
                        player.do_action(action, **action.kwargs)
                        break

            if implemented_action == False:
                # just in case an invalid action somehow passes the parser
                # it will be caught here
                if noun != None:
                    print("You can't {} {}!".format(verb, noun))
                else:
                    print("You can't do that.")

    # once the loop breaks, the game has ended. Print the appropriate text:
    if player.victory:
        print(victory_text)

    else:
        print(defeat_text)

if __name__ == "__main__":
    play()
