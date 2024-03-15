import os
import combat
import dialogue_tree
import characters
import game_state
class GameInterface:
    def __init__(self, character: characters.Hero, game_state: game_state.GameState):
        self.init_screen = 'main_menu'
        self.screen = {
            'main_menu' : self.main_menu,
            'combat' : self.combat,
            'dialogue' : self.dialogue,
            'game' : self.game,
            'inventory' : self.inventory
        }
        self.hero = character
        self.state = game_state
        self.looked_around = False

    def main_loop(self):
        while True:
            self.screen[self.init_screen]()
    def main_menu(self):
        print("1. Start New Game")
        print("2. View Lore(Spoilers)")
        print("3. Exit")
        choice = input("Enter your choice: ")
        self.handle_main_menu(choice)
    def handle_main_menu(self, input_choice):
        try:
            choice = int(input_choice)  # Convert input to integer
            if choice == 1:
                self.init_screen = 'game'
            elif choice == 2:
                self.display_lore()
            elif choice == 3:
                exit()
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid choice. Try again.")

    def display_lore(self):
        clear_screen()
        story_overview = dialogue_tree.lore_string(self.hero)
        dialogue_tree.delay_print(story_overview)

    def combat(self):
        self.init_screen = 'combat'
        clear_screen()

    def game(self):
        clear_screen()
        combatcompleted: bool = self.state.num_combats
        dialogue_tree.stage_desc(self.state.stage, combatcompleted)
        print()
        print("1. Look around")
        print("2. Talk to Allies")
        print("3. Continue on toward goal")
        print("4. Check Inventory")
        print("Current Health: ", self.hero.health)
        print()
        
        choice = input("Enter your choice: ")
        self.handle_game(choice)

    def handle_game(self, choice):
        if choice == '1':
            self.looked_around = True
            self.state.look_around()
        elif choice == '3':
            self.continue_journey()
        elif choice == '4':
            # Handle inventory logic here
            pass
        else:
            print("Invalid choice. Please select a valid option.")

    def continue_journey(self):
        # Check for combat encounters based on game state
        if self.state.num_combats > 0:
            if self.state.stage == 1:
                enemy = characters.Monster("Goblin", 50, "Goblin")  # Example enemy for stage 1
                combat.CombatSystem(self.hero, enemy)
                combat.CombatSystem.start_combat()
            elif self.state.stage == 2:
                enemy = characters.Monster("Orc Warrior", 75, "Orc")  # Different enemy for stage 2
            elif self.state.stage == 3:
                enemy = characters.Villain("Cyrus", 100, "Tech Dominance")  # Villain encounter in stage 3
            if self.state.stage == 4:
                enemies = [
                characters.Monster("Desert Automaton", 90, "Automaton"),  
                characters.Monster("Sand Serpent", 80, "Serpent")  # Another enemy for a more varied encounter
                ]
            elif self.state.stage == 5:
                enemies = [
                    characters.Villain("Cyrus", 200, "World Domination"),  # The main antagonist for an epic showdown
                ]
            self.combat_interface([enemy])  # Initiate combat with the selected enemy
            self.state.num_combats -= 1  # Decrement the number of combats remaining in this stage

            if self.state.num_combats == 0 and self.state.stage < 5:
                self.hero.health = 100 #heal
                self.state.advance_stage()  # Advance to the next stage if all combats are completed
        else:
            print("You continue your journey without any encounters.")

    def combat_interface(self, enemies):
        clear_screen()
        print("Combat Encounter!")
        
        combat_system = combat.CombatSystem(self.hero, enemies)
        combat_system.start_combat()
        
        # After combat, determine what screen to return to
        self.init_screen = 'game'  # Return to the game screen after combat
    def inventory(self):
        self.init_screen = 'inventory'
    def dialogue(self):
        self.init_screen = 'dialogue'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')