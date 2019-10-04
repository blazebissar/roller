"""
Contains utilities for the main program like file I/O and the random dice
rolling
"""

import random

def readFromFile(filepath="./character.txt"):
    """
    This function will read in all the characteistics defined in the given
    file, defaulting to ./character.txt, and return the key/values in a dict.
    All keys and values are strings to maintain consistency between stats and
    names and the like.
    """

    with open(filepath, "r") as fd:
        # Assumes format is one key:value per line
        res = dict(i.rstrip().split(":") for i in fd.readlines())

    return res

def writeToFile(data, filepath="./character.txt"):
    """
    This function dumps the provided dictionart, data, to the specified file,
    defaulting to character.txt. It will dump in alphabetical order based on
    key names.
    """

    with open(filepath, "w") as fd:
        # Write lines in format key:value
        fd.writelines((k + ":" + v + "\n" for k, v in sorted(data.items())))

def skillCheck(modifier, die=20):
    """
    Creates a random number and modifies it accordingly, expects an integer
    input for modifier. Will return the modified roll and the natural roll.
    """
    natural_roll = random.randrange(1, die + 1)

    return max(0, natural_roll + modifier), natural_roll

def damageRoll(quantity, die, modifier, multiplier=1):
    """
    Rolls damage of the specified amount (multiplier * (quantity d die) plus
    modifier) and returns the result. This means that multiplier values are
    only including the dice rolled, not the modifier (useful for, say, critical
    hits)
    """

    damage = sum((random.randrange(1, die + 1) for i in range(quantity)))

    return (damage * multiplier) + modifier
