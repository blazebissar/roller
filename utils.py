'''
Utilities for tracking and performing checks with character attributes
'''

import random

class Character:
    '''
    Class that contains the traits of a character or creature and can
    perform rolls with those values
    '''

    def __init__(self, values=None):
        '''
        Initializes a Character from a dictionary
        '''
        if values is not None:
            self.traits = values.copy()
        else:
            self.traits = dict()

    @classmethod
    def from_file(cls, filepath='./character.txt'):
        '''
        Constructs a Character with the values read in from the specified file
        '''

        with open(filepath, 'r') as f:
            # Assumes format is one key:value per line
            res = dict(i.rstrip().split(':') for i in f.readlines())

        return Character(res)

    def to_file(self, filepath='./character.txt'):
        '''
        Will write the Character object's attributes to the specified file
        for persistent use
        '''

        with open(filepath, 'w') as f:
            # Write lines in format key:value
            f.writelines((k + ':' + v + '\n' for k, v in sorted(self.traits.items())))

    def __repr__(self):
        '''
        Prints out the key value pairs constituting the class
        '''

        return '{0}({1})'.format(self.__class__.__name__, repr(self.traits))

    def __str__(self):
        '''
        Prints out the key value pairs constituting the class in alphabetical
        key order and prepending the name and class of the character if
        present
        '''
        NAME_KEY = 'name'
        CLASS_KEY = 'class'
        res = ''

        if NAME_KEY in self.traits:
            res += '{0}: {1}\n'.format(NAME_KEY.capitalize(), self.traits[NAME_KEY])
        if CLASS_KEY in self.traits:
            res += '{0}: {1}\n'.format(CLASS_KEY.capitalize(), self.traits[CLASS_KEY])

        for k, v in sorted(self.traits.items()):
            if (k not in [NAME_KEY, CLASS_KEY]):
                res += '{0}: {1}\n'.format(k.capitalize(), v)

        return res


def skill_check(modifier, die=20):
    '''
    Creates a random number and modifies it accordingly, expects an integer
    input for modifier. Will return the modified roll and the natural roll.
    '''
    natural_roll = random.randrange(1, die + 1)

    return max(0, natural_roll + modifier), natural_roll

def damage_roll(quantity, die, modifier, multiplier=1):
    '''
    Rolls damage of the specified amount (multiplier * (quantity d die) plus
    modifier) and returns the result. This means that multiplier values are
    only including the dice rolled, not the modifier (useful for, say, critical
    hits)
    '''

    damage = sum((random.randrange(1, die + 1) for i in range(quantity)))

    return (damage * multiplier) + modifier
