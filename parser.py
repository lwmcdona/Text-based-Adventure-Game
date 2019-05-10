"""This is the file for the parser.
It defines the grammar for the language and contains parser functions that
parse input from the user into something the game can understand.
"""

# 1. Define the grammar of the language.
# the structure of a sentence is:
# sentence = verb [preposition] [article] noun
# where prepositions and articles are optional and the noun can in some cases be None

# another possible sentence structure is:
# sentence = verb [article] noun preposition [article] noun
# where the verb applies the first noun to the second

# sentences can be connected using the word "and"

preposition = {"at", "to", "on", "inside", "around", "up", "me", "with", "from"}
articles = {"the", "a", "an"}

# the following are sets of actions (verbs) that permit two nouns
# the word after the underscore indicates the valid preposition
actions_with = {"attack", "kill", "hit", "hurt"}
actions_on = {"use", "cast"}

actions_to = {"change", "switch"}

# This dictionary determines which prepositions work with which verbs.
# For example, while "look at" should work, "use at" and "pet to" should not.
verb_to_prep = {"go":{"to", "inside", "outside"},
                "look":{"at", "around"},
                "move":{"to", "inside", "outside"},
                "travel":{"to", "inside", "outside"},
                "pick":{"up"},
                "help":{"me"},
                "use":{"on"},
                "attack":{"with"},
                "kill":["with"],
                "hit":["with"],
                "hurt":["with"],
                "run":["to"],
                "escape":["to", "from"],
                "flee":["to"]}

# A list of nouns in a given room and the actions that can be applied to
# them must be provided to the parser.
# These will be passed in from the location in question
# For example:
# avail_nouns = {"out":["go"], "north":["go"], "bread":["eat", "look"],
#               "house":["look", "go"], "dog":["pet", "look"], "dragon":["attack"+"with"]}

# Note that in our "language" directions like north, south, and out are
# considered nouns because the action "go" can be applied to them.

def only_letters(line):
    """Removes punctuation, numbers, and any other non-letter characters from
    the line of input. Keep spaces constant."""
    line = list(line)

    for l in line:
        if not l.isalpha() and l != " ":
                line.remove(l)

    return "".join(line)

def flavour_text(line, verbs, verb):
    """Used to respond to some user input without calling an action.
    Adds variety in responses rather than simply responding "that is
    not a valid action" every time. Just for fun!

    Args:
        line: a list of words
        verbs: a list of given verbs
        verb: the extracted verb
        """

    if len(line) == 1:
        # print some flavour text in response to certain phrases
        if line[0] == "why":
            print("Because.")
        elif line[0] == "awe":
            print("I'm sorry, I don't make the rules.")
        elif line[0] == "thanks":
            print("You're welcome.")
        elif line[0] == "cool":
            print("I'm glad you think so.")
        elif line[0] == "sorry":
            print("That's okay. I suppose I can forgive you.")
        elif line[0] == "hi" or line[0] == "hello":
            print("Greetings.")
        else:
            return False

    elif " ".join(line) == "how are you":
        print("I am fine, thanks.")

    elif " ".join(line) == "thank you":
        print("You are welcome.")

    elif verb not in verbs:
        print("You try to {}, but you can't do that here.".format(" ".join(line)))
    else:
        return False
    return True

def print_help():
    """If the help command is called, print the following text."""

    print("""
        These commands are accepted in any location and at any time:
        HELP, HELP ME - prints this list
        INFO - for information about the game itself
        LOOK, LOOK AT ___ - to look around the area or at an object
        VIEW/LOOK (AT) INVENTORY - prints a list of the items you have
            on your person
        CHOOSE WEAPON - lets you choose or change your current weapon

        In addition to the above commands, the following commands can also
        be used in battle:

        ATTACK ENEMY: initiates combat or begins a new round of combat
            Note: you can also specify a weapon by typing "attack enemy with
                weapon", where "weapon" is the weapon you wish to use.

        VIEW ORBS: Lets you view a list of the orbs you have summoned up to the
            current point.

        CAST ORBNAME: Lets you cast a specific orb on your chosen weapon.

        FLEE: Allowing you to flee from battle. A direction (east, west, north,
            or south) can also be specified.

        If you have purchased healing potions (cup, jug, bottle) from the shop:
        USE POTIONNAME: For example, "use bottle". Lets you use a potion to heal
            yourself.
        USE POTIONNAME ON ENEMY: For example, "use bottle on dragon". Lets you
            heal the enemy, if you decide for some reason that you want to do
            that.
        """)

def print_information():
    """Prints information about the game."""

    print("""
        *** WELCOME TO OUR TEXT BASED ADVENTURE GAME ***
        This is a simple text based adventure game with a
        reasonably intelligent parser.

        Creators: Logan McDonald and Veronica Salm

        Type "help" or "help me" to view a list of basic commands.
    """)


def is_valid_prep(v, p):
    """Checks if a preposition is valid with a given verb.
    Args:
        v: a verb
        p: an action

    Returns: p if p is valid, else returns 0."""
    if v not in verb_to_prep:
        return 0
    elif p not in verb_to_prep[v]:
        return 0
    else:
        return p

def is_valid_adj(adj, noun, valid_adj):
    """Checks to see if the given adjective can be applied to a given
    noun.
    Args:
        adj, noun: an adjective and a noun
        valid_adj: a dictionary of nouns and the adjectives that can be applied
            to them.
    Returns: True if the adjective is valid, else returns False"""

    if adj in valid_adj[noun]:
        return True
    else:
        return False

def composite_action(verb, nouns, prep):
    """Checks to see if a composite action (one that requires more than one noun)
    is valid.

    There are two types of composite actions:
    1. use noun on noun
    2. attack noun with noun

    The parser will already have checked if the nouns are valid with the given
    verbs. This function checks that there are at least two nouns and that the
    preposition is correct.

    args:
        verb: the verb in question
        nouns: the list of nouns
        prep: the stored preposition

    returns:
        True if the composite action is valid, else False"""

    if nouns == None:
        print("You need a target for your '{}' action!".format(verb))
        return False

    if prep == None:
        return True

    if type(nouns) == str: # not enough nouns! Need a second noun to apply the first noun to
        # this catches cases like "use dragon" or "attack sword"
        print("What do you want to {} {} {}?".format(verb, nouns, prep))
        return False

    if nouns[0] == nouns[1]:
        # example: "use dragon on dragon" should not be valid_adj
        print("You cannot {} {} {} {}!".format(verb, nouns[0], prep, nouns[1]))
        return False
    else:
        return True

def parse(line, avail_nouns, valid_adj):
    """Parses a line of input from the user into something the game can understand.

    Args:
        line: a single line of user-generated input
        avail_nouns: a dictionary of nouns in a given room and the actions that can be applied to them.
            These will be passed in from the location in question. For example, we might have:
            avail_nouns = {"bread":["eat", "look"], "house":["go", "look"], "dog":["pet", "look"]}
        valid_adj: Like avail_nouns, a dictionary of the nouns in the room and any adjectives that can
            be applied to them. For example:
            valid_adj = {"bread":["brown"], "house":["small", "white"], "dog":["fierce", ]}

    Returns:
        0, None: if the input is invalid
        or
        (verb, noun), leftover_input: A tuple of the verb and the noun to apply it to, along with any
        leftover input (which will be fed back into the parser once it has been determined that the first
        action is valid)
    """
    # create a set of valid adjectives based on the given room
    adjectives = set()
    for n in valid_adj:
        for a in valid_adj[n]:
            adjectives.add(a)
    # create a set of valid verbs based on the given room
    verbs = set()
    for n in avail_nouns:
        for v in avail_nouns[n]:
            verbs.add(v)

    # these commands can be used in any location
    verbs.add("help")
    verbs.add("info")

    # format the line by removing all numbers and punctuation
    # and converting it to a list, splitting by whitespace
    line = only_letters(line)
    line = line.strip().lower().split()

    # all sentence parts start as None
    prep = None # preposition
    article = None
    noun = None
    adj = []
    objects = dict() # a dictionary of actions and the nouns they are applied to

    leftover_input = None

    if len(line) == 0: # if the command is empty
        return 0, None

    # the first word in the sentence is considered to be a verb
    verb = line[0]
    objects[verb] = None


    for i in range(1, len(line)): #process the rest of input
        if line[i] in preposition: # if the word is a preposition
            if prep == None: # if there is not already a preposition stored
                prep = is_valid_prep(verb, line[i])

                if prep == 0:
                    print("You can't {} {}!".format(verb, line[i]))
                    return 0, leftover_input

            else:
                print("It's not possible to {}!".format(" ".join(line)))
                return 0, leftover_input

        elif line[i] in avail_nouns:
            if objects[verb] == None:
                noun = line[i] # set the noun for the action.
                # For example, map objects[attack] to dragon

                if verb not in avail_nouns[noun]:
                    # if the verb is invalid, give the player some help
                    # tell them what they can do with the given noun
                    if len(avail_nouns[noun]) < 3:
                        print("You can't {}! You can only {} {}.".format(" ".join(line), " or ".join(avail_nouns[noun]), noun))
                    else:
                        print("You can't {}! You can only {} or {} {}.".format(" ".join(line),
                                ", ".join(avail_nouns[noun][0:-1]),
                                avail_nouns[noun][-1],
                                noun))
                    return 0, leftover_input

                for a in adj: # cycle through stored adjectives
                    if not is_valid_adj(a, noun, valid_adj): # if any are not valid
                        print("The {} is not {}!".format(" ".join(adj), noun))
                        return 0, leftover_input
                # reset in case there is another noun with new adjectives
                # (ie, use blue orb on red sword))
                # adj = []
                objects[verb] = noun

            elif verb in actions_on or verb in actions_with:
                # actions_on and actions_with are two global lists
                if len(objects[verb].split()) == 1:
                    # there can only be one object attached to the verb!
                    new_noun = line[i]

                    if verb not in avail_nouns[noun]:
                        print("That action doesn't work with that object.")
                        return 0, leftover_input

                    for a in adj:
                        if not is_valid_adj(a, line[i], valid_adj): # if all the adjectives are valid, continue
                            # if any are invalid, return 0
                            print("There is no {} {}!".format(" ".join(adj), line[i]))
                            return 0, leftover_input

                    adj = [] # reset adjectives
                    objects[verb] = [noun, new_noun]
                    noun = new_noun
            else:
                print("Your sentence doesn't make sense.")
                return 0, leftover_input

        elif line[i] == "and": # this is the start of a new action
            # this lets us parse more complicated sentences
            # and create a queue of actions
            leftover_input = " ".join(line[i+1:])
            break

        elif line[i] in verb:
            # if the word is a valid verb, set verb
            if verb == None:
                verb = line[i]
                objects[verb] = None

            else:
                print("Your sentence doesn't make sense.")

        elif line[i] in articles:
            # check if the article is in the accepted list of articles
            # note that a phrase like "an dog" or "a cliffs" is valid!
            # a check for this would involve determining whether the
            # noun is plural or singular and whether it begins with a
            # vowel, but we did not have time to do this.
            if article == None:
                article = line[i]

            else:
                print("I don't understand '{} {}'".format(article, line[i]))
                return 0, leftover_input

        elif line[i] in adjectives:
            adj.append(line[i])
        else:
            if verb == "look":
                print("I don't see anything like that.")
                return 0, leftover_input

            if flavour_text(line, verbs, verb) == True:
                return 0, leftover_input

            if line[0] not in verbs:
                print("That is not a valid action.")
                return 0, leftover_input

            if verb == "go" or verb == "move" or verb == "travel":
                # if the noun is not in valid nouns, give the user some help
                directions = {"north", "south", "east", "west"}

                if line[i] in directions:
                    # if the user tries to go a direction where there is no tile
                    print("There is nothing to the {}.".format(line[i]))

                else:
                    print("You can't go to the {}. Try going north, south, east, or west instead.".format(line[i]))

                return 0, leftover_input

            else:
                print("You can't do that.")
                return 0, leftover_input

    if verb in actions_with or verb in actions_on:
        # if the verb is "use" or some variant of "attack"
        # check if it is a valid composite action (action with more
        # than one noun)
        if composite_action(verb, objects[verb], prep) == False:
            return 0, leftover_input

    if flavour_text(line, verbs, verb) == True:
        return 0, leftover_input

    # set of verbs that can exist by themselves
    noun_can_be_none = {"look", "leave", "stop", "flee", "run", "escape", "shop"}

    # check if the action is complete
    # some actions, like "look" can have no noun attached, but others need
    # to specify a noun
    if objects[verb] == None: # if there is no extracted noun
        if verb == "go" or verb == "move" or verb == "travel":
            # if the verb specifies movement, prompt the user to choose a direction
            direction = input(("Where do you want to {}? Please choose a direction: ".format(verb))).split()
            if len(direction) == 1 and direction[0] in avail_nouns:
                objects[verb] = direction[0]
            else:
                print("You can't go '{}'.".format(" ".join(direction)))
                return 0, leftover_input

        elif verb == "help":
            print_help() # print the help text
            return 0, leftover_input

        elif verb == "info":
            print_information() # print the game information
            return 0, leftover_input

        elif verb not in noun_can_be_none:
            if verb in verbs: # if the verb is valid for something else in the room
                print("I don't understand. You need to specify something to {}.".format(verb))

            else: # if the verb is unrecognized, it could be anything
                print("That is not a valid action.")

            return 0, leftover_input

    return (verb, objects[verb]), leftover_input

if __name__ == "__main__":
    while True:
        avail_nouns = {"dragon":["use", "attack"], "orb":["use"], "sword":["attack"]}
        valid_adj = {"dragon":["purple"], "orb":["blue", "green"]}
        action = parse(input(), avail_nouns, valid_adj)
        if action != 0:
            print(action)
