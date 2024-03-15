import game_interface
import time
import loot_tree
from characters import Character, Hero, Ally, Villain, Monster
from dialogue_tree import DialogueNode
import dialogue_tree

#Comments are proposed implementation

class GameState:
    def __init__(self, hero: Hero):
        self.stage = 1
        self.num_combats = 0
        self.hero = hero
        self.allies = []
        self.villain_met = None
        self.matrix_location_known = False
        self.elara_decision_made = False
        self.stage_two_special = False
        self.stage_four_special = False
        self.endings = {
            'hopeful': False,
            'dark': False,
            'compromise': False
        }

    def look_around(self):
        if(self.stage == 1):
            print("\n")

    def stage_one(self):
        self.num_combats = 1
        print("Act 1: The Quest Begins")
        # Introduction to the setting and characters
        self.hero.set_dialogue_tree(DialogueNode.con)
        # Hero meets Dr. Elara and learns about the Genesis Matrix.
        # Player is given initial choices that start to shape moral alignment.
        # Set initial objectives for the Hero to complete.

    def stage_two(self):
        self.num_combats = 1
        print("Act 2: Gathering Allies")
        # Hero starts to meet potential allies.
        self.allies.append(Ally("Jax", 100))  # Example of adding an ally
        self.allies.append(Ally("Nova", 100))  # Another ally
        # Each ally can also have their own dialogue trees and inventory.
        # Define challenges and interactions with tech pirates.

    def stage_three(self):
        self.num_combats = 1
        print("Act 3: Encounters with the Villains")
        # Hero's encounters with Cyrus and the Tech Raiders begin.
        self.villain_met = (Villain("Cyrus", 150, evil_plan="use the Genesis Matrix to gain ultimate control over all technology, establishing a totalitarian regime where only those aligned with his vision of 'tech supremacy' will thrive."))
        # Introduce recurring confrontations and decisions that affect the storyline.
        # Choices here can heavily influence moral alignment.

    def stage_four(self):
        self.num_combats = 1
        print("Act 4: Trials of the Wasteland")
        # Describe the arduous journey through Neo-Eden and the Silent Zones.
        self.villain_met.evil_plan = "harness the power of the Genesis Matrix to plunge the world into chaos, allowing him to seize control over all nations and establish himself as the undisputed ruler of the entire planet."
        # Trials faced here test the player's combat skills and decision-making.

    def stage_five(self):
        self.num_combats = 1
        print("Act 5: The Revelation")
        # Hero discovers the Genesis Matrix and Dr. Elara's true intentions.
        # The player is faced with critical choices that lead to different endings.
        # Update self.endings based on the choices made.

    def special_check(self):
        if(self.stage == 4 or self.stage == 2):
            return True
        else:
            return False
        
    def special_choice(self):
        if(self.stage == 2):
            if(self.stage_two_special == True):
                print("\nYou have already checked the ancient archives\n")
            else:
                s = "\nYou delve into the ancient archives, uncovering a secret weapon of the past\n"
                dialogue_tree.delay_print(s)
                wep = loot_tree.Weapon("Genesis Sword", 30)
                loot_tree.loot_pickup(wep)
                self.hero.inventory += wep
    
    def advance_stage(self):
        self.stage += 1
        getattr(self, f'stage_{self.stage}')()  # Dynamically move to the next stage method
        self.heal_hero_and_allies()  # Heal hero and allies after completing the stage

        if self.stage == 5:
            print("You've reached a significant milestone in your journey, but many challenges still lie ahead.")
        elif self.stage > 5:
            print("Your adventure continues as you venture into uncharted territory.")
    
    def heal_hero_and_allies(self):
        # Healing process
        for ally in self.allies:
            ally.health = self.hero.max_health  # Reset ally's health to full
        self.hero.health = self.hero.max_health  # Reset hero's health to full

        # Display immersive healing messages
        print("As you and your allies conclude this stage of your journey, you take a moment to rest and recuperate.")
        time.sleep(2)
        print("Gentle warmth suffuses your bodies, soothing your wounds and rejuvenating your spirits.")
        time.sleep(2)
        print("Your injuries fade away, replaced by renewed strength and vitality.")
        time.sleep(2)
        print("With fresh determination, you prepare to face the challenges that lie ahead.")
        time.sleep(2)