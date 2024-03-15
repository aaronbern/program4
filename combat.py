import random

class CombatSystem:
    def __init__(self, hero, enemies):
        self.hero = hero
        self.enemies = enemies  # List of enemies (Villains/Monsters) the hero will fight against

    def roll_hit(self, chance):
        # Simplified hit chance calculation
        return random.randint(1, 100) <= chance

    def perform_attack(self, attacker, defender, attack_type):
        if attack_type == "quick":
            chance = 80  # 80% chance to hit
            damage_range = (5, 10) if attacker.equipped_weapon == "None" else (attacker.equipped_weapon.min_damage, attacker.equipped_weapon.max_damage)
        elif attack_type == "heavy":
            chance = 50  # 50% chance to hit
            damage_range = (10, 20) if attacker.equipped_weapon == "None" else (attacker.equipped_weapon.min_damage * 1.5, attacker.equipped_weapon.max_damage * 1.5)

        if self.roll_hit(chance):
            damage = random.randint(*damage_range)
            print(f"{attacker.name}'s {attack_type} attack hits {defender.name} for {damage} damage!")
            defender.take_damage(damage)
        else:
            print(f"{attacker.name}'s {attack_type} attack missed!")

    def combat_round(self):
        # Player's turn
        print(f"Your Health: {self.hero.health}, Enemy Health: {self.enemies[0].health}")
        print("Choose your action:")
        print("1. Quick Attack")
        print("2. Heavy Attack")

        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            self.perform_attack(self.hero, self.enemies[0], "quick")
        elif choice == "2":
            self.perform_attack(self.hero, self.enemies[0], "heavy")
        else:
            print("Invalid choice. Please select 1 or 2.")

        # Enemy's turn (assuming a single enemy for simplicity)
        if self.enemies[0].health > 0:
            self.perform_attack(self.enemies[0], self.hero, "quick")  # Enemy uses quick attacks

        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]  # Remove defeated enemies

    def start_combat(self):
        print("Combat starts!")
        while self.enemies and self.hero.health > 0:
            self.combat_round()
            print()  # Add a newline for readability

        if not self.enemies:
            print("You've defeated the enemy!")
        else:
            print("You've been defeated...")
