import numpy as np
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.inventory = []
        self.dialogue_tree = None
        self.max_health = 100

    def set_dialogue_tree(self, dialogue_root):
        self.dialogue_tree = dialogue_root

    def get_dialogue(self, game_state):
        return self.dialogue_tree

    def display(self):
        print(f"Name: {self.name}, Health: {self.health}")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} took {amount} damage. Health is now {self.health}.")
        if self.health <= 0:
            print(f"{self.name} has been defeated.")

class Hero(Character):
    def __init__(self, name, health, moral_alignment=50, chips = 0):
        super().__init__(name, health)
        self.stats = np.array([100, 75, 50])
        self.moral_alignment = moral_alignment
        self.chips = chips
        self.equipped_weapon = "None"

    def update_alignment(self, decision):
        self.moral_alignment += decision
        print(f"{self.name}'s alignment is now {self.moral_alignment}.")

    def attack(self, target):
        print(f"{self.name} attacks {target.name}!")

class Ally(Character):
    def __init__(self, name, health, influence=50):
        super().__init__(name, health)
        self.influence = influence

class Villain(Character):
    def __init__(self, name, health, evil_plan="World Domination"):
        super().__init__(name, health)
        self.evil_plan = evil_plan

    def __repr__(self):
        return f"{self.name}, the Villain, seeks to {self.evil_plan} and has {self.health} health remaining."
    
    def confront(self, target):
        print(f"{self.name} confronts {target.name} with the plan of {self.evil_plan}.")

class Monster(Character):
    def __init__(self, name, health, monster_type="Goblin"):
        super().__init__(name, health)
        self.monster_type = monster_type

    def attack(self, target):
        print(f"The {self.monster_type} {self.name} attacks {target.name}!")


