#!/usr/bin/env python3
'''
The main module for the roller application. Command parsing resides here.
'''

import sys
import utils

def get_modifier(value):
    '''
    Function that returns the modifier for a skill of a given amount
    '''
    return (value - 10) // 2

def handle_skill(args, character):
    '''
    Determines what kind of skill check is required and loads the appropriate
    character information to deal with it. Prints the information directly
    rather than returning.
    '''

    # A properly formatted command will have the skill and either 'check' or
    # 'save' followed by an optional advantage/disadvantage
    skill = variant = advantage_status = ''
    reroll = False

    if len(args) == 2:
        skill, variant = args
    elif len(args) == 3:
        skill, variant, advantage_status = args
        reroll = True

        if advantage_status not in ['advantage', 'disadvantage']:
            print('Error: expecting third argument to be "advantage" or "disadvantage"')
            return
    else:
        print('Error: expecting two or three arguments')
        return

    if variant not in ['save', 'check']:
        print('Error: expecting second argument to be "check" or "save"')
        return

    # Check for proficiency
    modifier = get_modifier(int(character.traits[skill]))
    if (variant == 'save' and skill in character.traits['save_proficiencies']) \
            or (variant == 'check' and skill in character.traits['check_proficiencies']):
        modifier += int(character.traits['proficiency'])

    res, nat_res = utils.skill_check(modifier)

    # Roll again for advantage or disadvantage
    if reroll:
        re_res, re_nat_res = utils.skill_check(modifier)

        if advantage_status == 'advantage':
            res, nat_res = max(res, re_res), max(nat_res, re_nat_res)
        else:
            res, nat_res = min(res, re_res), min(nat_res, re_nat_res)

    print('%s check rolled a %d with a natural %d' % (skill, res, nat_res))

def process_args(args, character='character.txt'):
    '''
    Function that processes arguments, allowing for a more free-form input
    like ./roller con save
    The character argument is implemented for recursive calls from helper
    functions after determining that there is a different character file
    specified.
    '''

    # Key words for skills
    skills = [
        'strength', 'str',
        'dexterity', 'dex',
        'constitution', 'con',
        'intelligence', 'int',
        'wisdom', 'wis',
        'charisma', 'cha',
        'athletics', 'ath',
        'acrobatics', 'acro',
        'slight of hand', 'slightofhand', 'slight',
        'stealth',
        'arcana',
        'history', 'hist',
        'investigation', 'invest',
        'nature', 'nat',
        'religion', 'rel',
        'animal handling', 'animalhandling', 'anim',
        'insight', 'ins',
        'medicine', 'med',
        'perception', 'per',
        'survival', 'sur',
        'deception', 'dec',
        'intimidation', 'intim',
        'performance', 'perform', 'perf',
        'persuasion', 'persuade', 'pers'
        ]
    # Key words for top level commands
    commands = [
        'attack',
        'damage',
        'autogen',
        'gen'
        ]

    first = args[0]

    # Determine if this is a skill check of some sort
    if first in skills:
        player_char = utils.Character.from_file(character)
        handle_skill(args, player_char)
    # Otherwise it is a command
    elif first in commands:
        if first == 'attack':
            print('Pending implementation')
        elif first == 'damage':
            print('Pending implementation')
        elif first == 'gen':
            print('Pending implementation')
        elif first == 'autogen':
            print('Pending implementation')
        else:
            pass
    else:
        print("Error: command %s is invalid" % first)

def main():
    '''
    Main input loop before calling handler functions
    '''

    process_args(sys.argv[1::], 'character.txt')


if __name__ == '__main__':
    main()
