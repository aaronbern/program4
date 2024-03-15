import os
import time
from characters import Hero, Ally, Villain, Monster
from combat import CombatSystem
import dialogue_tree
from game_interface import GameInterface, clear_screen
from game_state import GameState
from loot_tree import LootTree, populate_loot_tree

def main():
    
    name = input("Enter your hero's name: ")
    user_hero = Hero(name, 100)
    game_state = GameState(user_hero)
    game_interface = GameInterface(user_hero, game_state)
    loot_tree = LootTree()
    populate_loot_tree(loot_tree)
    clear_screen()
    print("---To Skip Dialogue Typing Hit 'Space'---")
    dialogue_tree.opening_message(user_hero)
    print("\n")
    game_interface.main_loop()


main()