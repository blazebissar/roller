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

def perform_attack(args, character):
    '''
    Parses the commands ands executes the attack. Assumes a strength-based
    attack unless specified otherwise.
    '''
    # Variables to test for commands and their shorthands, also track modifications
    advantage_types = ['advantage', 'adv']
    disadvantage_types = ['disadvantage', 'dis']
    base_skill = 'strength'
    advantage_status = ''

    print(args)

    # When only specifying advantage/disadvantage or a non-strength stat to use
    if len(args) == 1:
        if args[0] in advantage_types + disadvantage_types:
            advantage_status = args[0]
        elif args[0] in character.traits:
            base_skill = args[0]
        else:
            print('Error: expected advantage/disadvantage or base skill')
            return
    # When using both advantage/disadvantage and a non-strength stat
    # because we allow for either order in the command
    elif len(args) == 2:
        all_words = advantage_types + disadvantage_types + list(character.traits.keys())
        if args[0] not in all_words or args[1] not in all_words:
            print('Error: expected advantage/disadvantage or base skill')
            return
        if args[0] in advantage_types + disadvantage_types:
            advantage_status = args[0]
            base_skill = args[1]
        else:
            advantage_status = args[1]
            base_skill = args[0]
    elif len(args) != 0:
        print('Error: expecting zero, one, or two modifiers for attacks')
        return

    # Perform the attack
    modifier = get_modifier(int(character.traits[base_skill]))
    modifier += int(character.traits['proficiency'])

    res, nat_res = utils.skill_check(modifier)

    # Roll again for advantage or disadvantage
    if advantage_status in advantage_types:
        re_res, re_nat_res = utils.skill_check(modifier)
        res, nat_res = max(res, re_res), max(nat_res, re_nat_res)
    elif advantage_status in disadvantage_types:
        re_res, re_nat_res = utils.skill_check(modifier)
        res, nat_res = min(res, re_res), min(nat_res, re_nat_res)

    print('Attack rolled a %d with a natural %d' % (res, nat_res))


def handle_skill(args, character):
    '''
    Determines what kind of skill check is required and loads the appropriate
    character information to deal with it. Prints the information directly
    rather than returning.
    '''

    # Variables to test for commands and their shorthands
    advantage_types = ['advantage', 'adv']
    disadvantage_types = ['disadvantage', 'dis']
    check_types = ['save', 'check']

    # A properly formatted command will have the skill and either 'check' or
    # 'save' followed by an optional advantage/disadvantage
    skill = variant = advantage_status = ''
    reroll = False

    if len(args) == 2:
        skill, variant = args
    elif len(args) == 3:
        skill, variant, advantage_status = args
        reroll = True

        if advantage_status not in advantage_types + disadvantage_types:
            print('Error: third argument must be one of:', advantage_types + disadvantage_types)
            return
    else:
        print('Error: expecting two or three arguments')
        return

    if variant not in check_types:
        print('Error: second argument must be one of:', check_types)
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

        if advantage_status in advantage_types:
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
            player_char = utils.Character.from_file(character)
            perform_attack(args[1::], player_char)
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
