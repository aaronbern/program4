import random

class LootItem:
    def __init__(self, name):
        self.name = name

class Weapon(LootItem):
    def __init__(self, name, damage):
        super().__init__(name)
        self.damage = damage
    def __repr__(self):
        return f"Weapon Name: {self.name}, Damage: {self.damage}"

class Food(LootItem):
    def __init__(self, name, healing_amount):
        super().__init__(name)
        self.healing_amount = healing_amount
    def __repr__(self):
        return f"Food Name: {self.name}, Healing: {self.healing_amount}"
        

class ItemNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class CategoryNode:
    def __init__(self, category):
        self.category = category
        self.items_head = None  # Head of the LLL for items in this category
        self.left = None
        self.right = None

    def add_item(self, item):
        new_node = ItemNode(item)
        if not self.items_head:
            self.items_head = new_node
        else:
            # Add new item nodes to the head for simplicity and to ensure the first one gets dropped
            new_node.next = self.items_head
            self.items_head = new_node

class LootTree:
    def __init__(self):
        self.root = None
        

    def _insert_recursive(self, current_node, category, item):
        if current_node is None:
            new_node = CategoryNode(category)
            new_node.add_item(item)
            return new_node

        if category < current_node.category:
            current_node.left = self._insert_recursive(current_node.left, category, item)
        elif category > current_node.category:
            current_node.right = self._insert_recursive(current_node.right, category, item)
        else:
            current_node.add_item(item)

        return current_node

    def insert_item(self, category, item):
        if not self.root:
            self.root = CategoryNode(category)
            self.root.add_item(item)
        else:
            self._insert_recursive(self.root, category, item)

    def _search_recursive(self, current_node, category):
        if current_node is None:
            return None

        if category < current_node.category:
            return self._search_recursive(current_node.left, category)
        elif category > current_node.category:
            return self._search_recursive(current_node.right, category)
        else:
            return current_node

    def drop_loot(self):
        # 25% chance for a weapon, otherwise food or drink
        categories = ['Weapon', 'Food', 'Drink']
        weights = [0.25, 0.375, 0.375]
        chosen_category = random.choices(categories, weights)[0]
        
        category_node = self._search_recursive(self.root, chosen_category)
        if category_node and category_node.items_head:
            loot = category_node.items_head.item
            # Remove the dropped item from the LLL
            category_node.items_head = category_node.items_head.next
            return loot
        return None

def populate_loot_tree(loot_tree):
    # Weapons
    weapons = [
        Weapon("Laser Sword", 25),
        Weapon("Plasma Rifle", 30),
        Weapon("Photon Dagger", 15),
        Weapon("Electro Mace", 20),
        Weapon("Quantum Bow", 28),
        Weapon("Nano Blade", 32),
        Weapon("Pulse Cannon", 35),
        Weapon("Arc Lance", 22),
        Weapon("Gravity Hammer", 40),
        Weapon("Sonic Whip", 18),
    ]

    # Food
    food_items = [
        Food("Energy Bar", 10),
        Food("Health Drink", 15),
        Food("Protein Pack", 20),
        Food("Regen Fruit", 25),
        Food("Vitality Nuts", 12),
        Food("Medicinal Herbs", 18),
        Food("Stamina Jerky", 16),
        Food("Nutrient Paste", 22),
        Food("Revival Seeds", 30),
        Food("Healing Mushrooms", 14),
    ]

    # Drinks
    drink_items = [
        Food("Hydration Fluid", 8),
        Food("Electrolyte Brew", 12),
        Food("Invigorating Tea", 16),
        Food("Rejuvenation Elixir", 24),
        Food("Adrenaline Shot", 20),
        Food("Mystic Tonic", 28),
        Food("Energy Soda", 10),
        Food("Stamina Draft", 14),
        Food("Focus Water", 18),
        Food("Clarity Cocktail", 22),
    ]

    # Inserting items into the LootTree
    for weapon in weapons:
        loot_tree.insert_item('Weapon', weapon)

    for food in food_items:
        loot_tree.insert_item('Food', food)

    for drink in drink_items:
        loot_tree.insert_item('Drink', drink)

def loot_pickup(item):
    print(f"You have picked up {item}")