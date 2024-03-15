import pytest

from game_interface import GameInterface
from game_state import GameState
from combat import CombatSystem
from loot_tree import lootBST
from dialogue_tree import DialogueBST

@pytest.fixture
def game_interface():
    return GameInterface()

@pytest.fixture
def game_state():
    return GameState()

@pytest.fixture
def combat():
    return CombatSystem()

@pytest.fixture
def inventory_tree():
    return lootBST()

@pytest.fixture
def dialogue_tree():
    return DialogueBST

# Main Menu Tests
def test_main_menu_loads_options(game_interface):
    expected_options = ["Start New Game", "Settings", "Lore"]
    assert set(game_interface.main_menu_options()).issuperset(expected_options)

def test_start_new_game_option(game_interface):
    game_interface.select_option("Start New Game")
    assert game_interface.is_new_game_session()

# Narrative and Choices Tests
def test_narrative_progression(game_state):
    game_state.make_choice("Explore the ruins")
    assert "ruins" in game_state.current_location_description()

def test_choice_impact_on_game_state(game_state):
    initial_state = game_state.get_state_attribute("reputation")
    game_state.make_choice("Help the stranger")
    assert game_state.get_state_attribute("reputation") > initial_state

# Combat Feedback Tests
def test_combat_initiation(combat_system):
    combat_system.start_combat("Mutant Rat")
    assert combat_system.enemy_type() == "Mutant Rat"

def test_combat_action_feedback(combat_system):
    combat_system.perform_action("Attack")
    assert "damage" in combat_system.last_action_feedback()

# Inventory Display and Management Tests
def test_inventory_listing(inventory_system):
    inventory_system.add_item("Plasma Rifle")
    assert "Plasma Rifle" in inventory_system.list_items()

def test_item_use_effect(inventory_system, game_state):
    inventory_system.add_item("Healing Potion")
    initial_health = game_state.player_health()
    inventory_system.use_item("Healing Potion")
    assert game_state.player_health() > initial_health

# Exploration and Decision-Making Tests
def test_exploration_choice_leads_to_new_area(game_state):
    game_state.choose_exploration_option("Enter the abandoned lab")
    assert game_state.current_location() == "Abandoned Lab"

def test_decision_impact_on_npc_relationship(game_state):
    initial_relation = game_state.get_npc_relationship("Dr. Elara")
    game_state.make_decision("Support Dr. Elara's research")
    assert game_state.get_npc_relationship("Dr. Elara") > initial_relation

# Simplified Combat System Tests
def test_combat_victory_updates_game_state(game_state, combat_system):
    combat_system.start_combat("Rogue Drone")
    combat_system.win_encounter()
    assert game_state.has_combat_victory_flag()

def test_combat_loss_behavior(game_state, combat_system):
    combat_system.start_combat("Desert Marauder")
    combat_system.lose_encounter()
    assert game_state.is_player_incapacitated()

# Moral Alignment System Tests
def test_alignment_change_after_decision(game_state):
    initial_alignment = game_state.get_moral_alignment()
    game_state.make_significant_choice("Sacrifice the village")
    assert game_state.get_moral_alignment() != initial_alignment

def test_alignment_influences_npc_interactions(game_state):
    game_state.set_moral_alignment("Altruist")
    npc_reaction = game_state.interact_with_npc("Village Leader")
    assert "thankful" in npc_reaction

# Game Conclusion Tests
def test_game_ending_reflects_alignment(game_state):
    game_state.set_moral_alignment("Egoist")
    ending = game_state.conclude_game()
    assert "Egoist" in ending

def test_replayability_with_different_choices(game_state):
    game_state.conclude_game()
    game_state.start_new_game()
    game_state.make_choice("Reject the quest")
    assert game_state.has_different_outcome()

# Test Dialogue Initialization
def test_dialogue_initialization(dialogue_system):
    """Ensure the dialogue system initializes with a root node."""
    assert dialogue_system.root is not None
    assert dialogue_system.root.text.startswith("Welcome")

# Test Dialogue Progression
def test_dialogue_progression(dialogue_system, game_state):
    """Test that selecting a dialogue option progresses the dialogue correctly."""
    initial_option = dialogue_system.get_current_options()
    dialogue_system.select_option(1)  # Assuming this method advances the dialogue based on the option chosen
    new_option = dialogue_system.get_current_options()
    
    assert new_option != initial_option
    assert len(new_option) > 0  # Ensures new options are presented after a choice

# Test Dialogue Impact on Game State
def test_dialogue_impact_on_game_state(dialogue_system, game_state):
    """Verify that dialogue choices correctly impact the game state, such as altering moral alignment."""
    initial_alignment = game_state.get_moral_alignment()
    dialogue_system.select_option(1)  # Assuming this option is aligned with a moral choice
    
    new_alignment = game_state.get_moral_alignment()
    assert new_alignment != initial_alignment

# Test Multiple Dialogue Paths
def test_multiple_dialogue_paths(dialogue_system, game_state):
    """Ensure that different dialogue paths lead to appropriate narrative branches."""
    dialogue_system.select_option(1)
    first_path_result = game_state.current_narrative()

    dialogue_system.reset()  # Assuming a reset method to start dialogue from the root
    dialogue_system.select_option(2)  # Choose a different initial option
    second_path_result = game_state.current_narrative()

    assert first_path_result != second_path_result

# Test Dialogue Loops
def test_dialogue_loops_back(dialogue_system):
    """Test that the dialogue can loop back to a previous point if designed to do so."""
    root_text = dialogue_system.root.text
    dialogue_system.select_option(1)  # Choose an option that loops back
    assert dialogue_system.get_current_dialogue().text == root_text  # Check if dialogue loops back to root

# Test Dialogue End
def test_dialogue_end(dialogue_system):
    """Verify that the dialogue ends appropriately when no further options are available."""
    while dialogue_system.get_current_options():
        dialogue_system.select_option(0)  # Continuously select the first option
    
    assert dialogue_system.get_current_options() == []  # No more options should be available, indicating the end of the dialogue
