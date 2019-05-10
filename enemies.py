# adapted from http://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python/

class Enemy:
    """The base enemy class.
    Attributes:
        -name: a string denoting the name of the enemy.
        -hp: enemy's hitpoints. The enemy dies when these fall to 0.
        -damagemax: maximum damage the enemy can do.
        -damagemin: minimum damage the enemy can do.
        -capacity: amount of orbs the enemy can hold at one time.
        -gold_dropped: amount of gold the enemy drops when killed
        -intelligence: affects which orbs the enemy will choose to cast
        -orb: current type of the enemy, initialized to None
        -orb_list: list of orbs the enemy holds, initialized to empty
    """
    def __init__(self, name, hp, damagemax, damagemin, capacity, gold_dropped,
                    intelligence, orb=None, orb_list=[]):
        self.name = name
        self.hp = hp
        self.damagemax = damagemax
        self.damagemin = damagemin
        self.capacity = capacity
        self.orb = orb
        self.orb_list = orb_list
        self.gold_dropped = gold_dropped
        self.intelligence = intelligence

    def is_alive(self):
        """Returns whether or not the enemy is alive."""
        return self.hp > 0

    def enemy_hp(self, name):
        """Allows to determine the original hp for an enemy. Used to respawn an
           enemy and also in healing an enemy."""
        hp = {"goblin":30, "salamander":12, "dragon":100}
        if name in hp:
            return hp[name]

"""The following are enemy subclasses."""
class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="dragon",
                         hp=100,
                         damagemax=25,
                         damagemin=5,
                         capacity=5,
                         intelligence = 7,
                         gold_dropped = 1000)

class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="goblin",
                         hp=30,
                         damagemax=7,
                         damagemin=3,
                         capacity=1,
                         intelligence = 4,
                         gold_dropped = 10)

class Salamander(Enemy):
    def __init__(self):
        super().__init__(name="salamander",
                         hp=9,
                         damagemax=2,
                         damagemin=1,
                         capacity=1,
                         intelligence = 2,
                         gold_dropped = 5)


"""These two enemy classes are not in use in our version of the game, but could
easily be added in without modification."""
class Spider(Enemy):
    def __init__(self):
        super().__init__(name="spider",
                        hp=10,
                        damagemax=5,
                        damagemin=1,
                        capacity=1,
                        intelligence=3,
                        gold_dropped=12)

class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="ogre",
                        hp=50,
                        damagemax=15,
                        damagemin=10,
                        capacity=2,
                        intelligence=2,
                        gold_dropped=20)
