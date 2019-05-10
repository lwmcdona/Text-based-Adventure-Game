# adapted from http://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python/
from enum import Enum

class Item():
    """The base class to be used for all items.
    Items have a name, description, and value."""
    def __init__ (self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        """For convenience, allows printing of the attributes of the items."""
        return "{}\n=====\n{}\nValue: {}\n".format(
        self.name, self.description, self.value)

class Gold(Item):
    """Gold, to be used as currency. The value of various items can be directly
    converted to an amount of gold."""
    def __init__ (self, amt):
        self.amt = amt
        super().__init__(name="gold",
                         description="A sack of round gold coins.",
                         value=self.amt)

##################################################################################################################
# The potion types used in the game.
class Potion(Item):
    """The potion base class. Allows for a healing method."""
    def __init__(self, name, description, value, healing):
        self.healing = healing
        super().__init__(name, description, value)

    def potion_types():
        """Returns a list of all potion_types"""
        return [Cup(), Bottle(), Jug()]

class Cup(Potion):
    def __init__(self):
        super().__init__(name="cup",
                         description="A cup of healing potion. Heals 10 hp.",
                         value=20,
                         healing=10)

class Bottle(Potion):
    def __init__(self):
        super().__init__(name="bottle",
                         description="A bottle of healing potion. Heals 20 hp.",
                         value=35,
                         healing=20)

class Jug(Potion):
    def __init__(self):
        super().__init__(name="jug",
                         description="A jug of healing potion. Heals 40 hp.",
                         value=60,
                         healing=40)

##################################################################################################################
# The orb types used in the game.
class OrbContainer(Item):
    """Containers for holding orbs, which can be of various sizes (capacities)."""
    def __init__(self, name, description, value, capacity, orb_list=[]):
        self.capacity = capacity  # the number of orbs that can be stored
        self.orb_list = orb_list  # a list of the orbs currently in the bag
        super().__init__(name, description, value)

class Pouch(OrbContainer):
    def __init__(self):
        super().__init__(name="pouch",
                         description="A small pouch. Should be enough to hold two orbs in battle.",
                         value=0,
                         capacity=2)

class Case(OrbContainer):
    def __init__(self):
        super().__init__(name="case",
                         description="""A distinguished case, somewhat larger than a pouch. Should be enough
to hold three orbs in battle.""",
                         value=30,
                         capacity=3)

class Pack(OrbContainer):
    def __init__(self):
        super().__init__(name="pack",
                         description="""A large pack. Should be enough to hold four orbs in battle.""",
                         value=50,
                         capacity=4)

class Orb(Item):
    """Orbs are mystical items that can be cast on a weapon by the player to
    change its damage type. Each type of orb has strengths and weaknesses
    against other orb types.

    Enemies are also capable of casting orbs on themselves."""
    def __init__(self, name, description, value, damagemultiplier):
        self.damagemultiplier = damagemultiplier
        super().__init__(name, description, value)

    def num_to_orb(num):
        """A dictionary mapping each orb type to a number. Used to randomly
        generate orbs."""
        num_to_orb = {  1:Firorb(),
                        2:Watorb(),
                        3:Natorb(),
                        4:Silvorb() }
        return num_to_orb[num]

    def orb_types():
        """Returns a list of all orb types."""
        return [Firorb(), Natorb(), Silvorb(), Watorb()]

    def best_combs(orb_name):
        combo = {"watorb": ["natorb", "watorb", "silvorb", "firorb"],
                 "natorb": ["firorb", "natorb", "silvorb", "watorb"],
                 "firorb": ["watorb", "firorb", "silvorb", "natorb"],
                 "silvorb": ["silvorb"]}
        return combo[orb_name]

    def worst_combs(orb_name):
        combo = {"watorb": ["firorb", "watorb", "silvorb", "natorb"],
                 "natorb": ["watorb", "natorb", "silvorb", "firorb"],
                 "firorb": ["natorb", "firorb", "silvorb", "watorb"],
                 "silvorb": ["silvorb"]}
        return combo[orb_name]

class Firorb(Orb):
    def __init__(self):
        super().__init__(name="firorb",
                        description="""A flaming ball of pure fire.
Careful, it's hot!""",
                        value=0,
                        damagemultiplier={"firorb" : 1,
                                           "watorb" : 0.5,
                                           "natorb" : 2,
                                           "silvorb": 0.75})

class Watorb(Orb):
    def __init__(self):
        super().__init__(name="watorb",
                        description="""A confined sphere of luminescent water.
Try not to spill!""",
                        value=0,
                        damagemultiplier={"firorb" : 2,
                                           "watorb" : 1,
                                           "natorb" : 0.5,
                                           "silvorb": 0.75})

class Natorb(Orb):
    def __init__(self):
        super().__init__(name="natorb",
                        description="""An irregular mass of nature.
What is nature exactly? Nobody knows.""",
                        value=0,
                        damagemultiplier={"firorb" : 0.5,
                                           "watorb" : 2,
                                           "natorb" : 1,
                                           "silvorb": 0.75})

class Silvorb(Orb):
    def __init__(self):
        super().__init__(name="silvorb",
                        description="""A perfect sphere of silver.""",
                        value=0,
                        damagemultiplier={"firorb" : 0.9,
                                           "watorb" : 0.9,
                                           "natorb" : 0.9,
                                           "silvorb": 1.1})
##################################################################################################################
class Weapon(Item):
    """Base weapon class
    Attributes:
        damagemax(int): maximum base damage a weapon can do
        damagmin(int): minimum base damage a weapon can do
        orb: the orb on the weapon, represents its 'type' """
    def __init__(self, name, description, value, damagemax, damagemin, orb=None):
        self.damagemax = damagemax
        self.damagemin = damagemin
        self.orb = orb
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage range: {}-{}".format(self.name,
                self.description, self.value, self.damagemin, self.damagemax)

    def damagerange(self):
        return self.damagemax, self.damagemin

class Rock(Weapon):
    def __init__(self):
        super().__init__(name="rock", # needs to be lower case to be able to read from input
                         description=
                         """A fist-sized rock, suitable for bludgeoning.""",
                         value=0,
                         damagemax=5,
                         damagemin=2)

class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="rock", # needs to be lower case to be able to read from input
                         description=
                         """A pointy dagger. Should be able to do some damage, at least.""",
                         value=0,
                         damagemax=8,
                         damagemin=5)

class Sword(Weapon):
    def __init__(self):
        super().__init__(name="sword",
                         description="""A reliable sword encrusted with several
large red gems. Looks valuable. And deadly.""",
                         value=100,
                         damagemax=15,
                         damagemin=13)

class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="dagger",
                         description="""A small dagger with some rust. It looks
like it may break at any minute. Somewhat more dangerous than a rock.""",
                         value=10,
                         damagemax=9,
                         damagemin=2)
##################################################################################################################
# Note: There was not enough time to implement effects of armour
class Armour(Item):
    """Base armour class. Doesn't actually affect damage in this version of the game."""
    def __init__(self, name, description, value, defense):
        self.defense = defense
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDefense: {}".format(self.name,
                                    self.description, self.value, self.defense)

class SuitofArmour(Armour):
    def __init__(self):
        super().__init__(name="armour",
                         description="It fits you perfectly.",
                         value=50,
                         defense=5)
