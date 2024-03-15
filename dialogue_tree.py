import time
import keyboard
import sys
import textwrap

class DialogueNode:
    def __init__(self, text, moral_change=0, condition=None, is_exit=False):
        self.text = text
        self.moral_change = moral_change  
        self.condition = condition
        self.responses = []
        self.is_exit = is_exit

    def add_response(self, response):
        self.responses.append(response)

    def is_accessible(self, game_state):
        return self.condition.is_met(game_state) if self.condition else True
    
    def construct_dialogue_tree_act_one(cls):
        # Initial approach by Dr. Elara
        root = cls("Dr. Elara approaches you with a sense of urgency in her eyes. 'You are the one known as the Scavenger, aren't you? I have a proposition that might interest someone of your... unique skills.'")

        # Protagonist's response options with moral alignment changes
        curious_response = cls("What kind of proposition?", moral_change=5)
        dismissive_response = cls("I'm not interested in propositions from strangers.", moral_change=-5, is_exit=True)
        cautious_response = cls("I'm listening, but I make no promises.", moral_change=0)
        sarcastic_response = cls("Does it pay well, or is it another 'world-saving' gig?", moral_change=-2)

        # Dr. Elara's follow-up based on protagonist's curiosity
        elara_explanation_curious = cls("Dr. Elara's eyes gleam with excitement and fear. 'It's about the Genesis Matrix, a device said to possess the power to either save our world or doom it. And I believe you might be the key to finding it.'")

        # Responses to Elara's explanation with moral alignment changes
        accept_mission_curious = cls("The Genesis Matrix? Sounds like a myth, but if it can save even a single person I am in!", moral_change=10)
        need_more_info_curious = cls("This Genesis Matrix... tell me more.", moral_change=5)
        decline_mission_curious = cls("I'm out. Unless you make it worth my while, I am not chasing some myth for free.", moral_change=-5)

        # More info on the Genesis Matrix with moral alignment changes
        matrix_details_curious = cls("Dr. Elara leans in closer, lowering her voice. 'The Genesis Matrix is no myth. It's the apex of pre-fall technology, capable of altering reality itself. But in the wrong hands... it could be catastrophic.'")

        # Final response options
        idealistic_acceptance = cls("If this Matrix can truly change things for the better, I'm in. Let's do this for the world, not for riches.", moral_change=10)
        reluctant_acceptance_money = cls("Alright, but you better make good on that payment. I'm doing this for the chips, not for some grand cause.", moral_change=-5)

        # Dr. Elara's concluding remarks and next steps for idealistic acceptance
        conclusion_idealistic = cls(textwrap.fill("Dr. Elara beams with a mix of relief and excitement. 'You have no idea how much this means. The first step is to gather any intel on the Matrix's last known location. Meet me at my lab tomorrow morning; we have much to prepare.'"), is_exit=True)

        # Dr. Elara's concluding remarks and next steps for reluctant acceptance
        conclusion_money = cls(textwrap.fill("Dr. Elara nods solemnly, understanding your stance. 'Fair enough; your skills warrant compensation. As agreed, 500 chips now, and more upon completion. Tomorrow, we start planning our first move. My lab, first light.'"), is_exit=True)

        # Linking nodes together
        root.add_response(curious_response)
        root.add_response(dismissive_response)
        root.add_response(cautious_response)
        root.add_response(sarcastic_response)

        curious_response.add_response(elara_explanation_curious)
        elara_explanation_curious.add_response(accept_mission_curious)
        elara_explanation_curious.add_response(need_more_info_curious)
        elara_explanation_curious.add_response(decline_mission_curious)

        need_more_info_curious.add_response(matrix_details_curious)
        
        # Here is where you add the concluding remarks nodes
        accept_mission_curious.add_response(conclusion_idealistic)
        reluctant_acceptance_money.add_response(conclusion_money)
        
        # Add final responses to the 'matrix_details_curious' node
        matrix_details_curious.add_response(idealistic_acceptance)
        matrix_details_curious.add_response(reluctant_acceptance_money)

        return root


def opening_message(hero):
    open_string = f"""Venture into a world hanging by a razor's edge, oscillating between rebirth and imminent doom. You are {hero.name}, a sage of technology salvaged from the debris of a forgotten era. You are known as the Scavenger to those also in the shadows of Haven City, a final refuge where humanity's last stand merges ancient relics with the raw instincts of survival. Yet beneath this survivalist veneer, a deeper urge stirs, propelled by tales of something transformative—something capable of rewriting our world's fate, for better or worse.

The "Genesis Matrix," shrouded in allure and peril, whispers your name. Rumors swirl of its power to resurrect our world or plunge it into deeper darkness, healing the scars of neglect or exploiting them. Poised at the juncture of safety and the great unknown, you face a critical choice: Will you step beyond the safety of Haven City, into the realms where light and shadow dance, in quest of a glimmer of hope? But at what cost?

Your skills, your cunning, and the choices you make will either forge a beacon of salvation or a harbinger of despair. The path you tread is fraught with moral quandaries, each decision tipping the scales towards salvation or ruin. Will you rise as the architect of a brighter future, or will the allure of power tempt you into darkness? The journey is fraught, and the choices you make will echo through the ages. Welcome to your crucible. Welcome to an odyssey where every choice could be your last."""
    delay_print(open_string)
    
def delay_print(s, width=80):
    wrapped_text = textwrap.fill(s, width=width)  # Wrap the text to the specified width.
    for i, c in enumerate(wrapped_text):
        if keyboard.is_pressed('space'):  # Check if the space bar is pressed
            sys.stdout.write(wrapped_text[i:])  # Print the rest of the string instantly
            sys.stdout.flush()
            break  # Exit the loop
        else:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.04)  # Delay between each character

def show_dialogue(node, game_state):
    print("\n" + node.text)
    accessible_responses = [response for response in node.responses if response.is_accessible(game_state)]
    
    for idx, response in enumerate(accessible_responses, 1):
        print(f"{idx}. {response.text}")

    if accessible_responses:
        choice = input("Choose an option: ")
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(accessible_responses):
                chosen_node = accessible_responses[choice]
                if chosen_node.is_exit:
                    print("Exiting dialogue.")
                    return
                else:
                    show_dialogue(chosen_node, game_state)
            else:
                print("Invalid choice. Please try again.")
                show_dialogue(node, game_state)
        except ValueError:
            print("Invalid input. Please enter a number.")
            show_dialogue(node, game_state)
    else:
        print("The dialogue ends here.")

def lore_string(hero):
    return f"""
        Story Overview
        --------------
        The game follows the journey of a character named {hero.name}, a skilled tech scavenger with a murky past. {hero.name}'s adventure begins in the relatively safe confides of Haven City, a community that has successfully managed to combine old-world tech with newfound methods of survival. Despite its safety, {hero.name} feels the pull of the unknown, driven by rumors of an ancient device capable of restoring the world to its former glory, known as the "Genesis Matrix."

        Act 1: The Quest Begins
        ------------------------
        {hero.name}'s journey starts when they encounter an old scientist named Dr. Elara, who has dedicated her life to finding the Genesis Matrix. She believes {hero.name} possesses the unique skills necessary to retrieve it. Skeptical yet intrigued, {hero.name} agrees to embark on this quest, driven by the promise of untold riches and perhaps a chance to make a real difference.

        Act 2: Gathering Allies
        ------------------------
        Understanding the dangers ahead, {hero.name} knows they'll need assistance. The first ally they encounter is Jax, a former security android reprogrammed to protect {hero.name}. Next, they meet Nova, a rogue bio-engineer with a talent for manipulating the organic hazards of the wasteland to her advantage. Together, they face various challenges, from navigating treacherous landscapes to dealing with marauding bands of tech pirates.

        Act 3: Encounters with the Villains
        ------------------------------------
        As their quest progresses, {hero.name} and their companions cross paths with the enigmatic leader of the Tech Raiders, Cyrus, who seeks the Genesis Matrix for his own tyrannical purposes. Cyrus becomes a recurring thorn in their side, confronting them at various points and challenging their resolve.

        Act 4: Trials of the Wasteland
        -------------------------------
        The journey takes {hero.name} and their allies through a series of trials, each designed to test their resolve, skills, and the strength of their bonds. These include braving the AI-controlled city of Neo-Eden, a place where technology has evolved beyond human control, and the Silent Zones, areas where all forms of electronic signals are mysteriously dampened, rendering most tech useless.

        Act 5: The Revelation
        ----------------------
        Upon finally locating the Genesis Matrix within the ruins of the old world's most advanced tech lab, {hero.name} faces a moral dilemma. Dr. Elara reveals her true intentions: to reset the world and erase the mistakes of the past, which would include eradicating what remains of human civilization to start anew. {hero.name} must choose between activating the Genesis Matrix, joining Dr. Elara's vision, or finding a new path that could lead to a different kind of rebirth for humanity.

        Conclusion
        ----------
        The game's conclusion is shaped by the player's choices, particularly {hero.name}'s final decision regarding the Genesis Matrix. The endings vary from a hopeful rebirth of civilization with {hero.name} leading the new world, to a return to the dark ages with the destruction of the remaining tech, or even a compromise that sees humanity slowly rebuild with a newfound respect for the power and dangers of their technology.  
        """

def stage_desc(stage, combatcompleted):
    if(stage == 1 and combatcompleted == False):
        s = """Under the flickering glow of a makeshift lantern, you navigate the labyrinthine streets of Haven City, your mind consumed by whispered tales of the Genesis Matrix. Each alley holds the promise of discovery, each relic a clue to a world beyond our own. The air is thick with the scent of damp concrete and rust, a tangible reminder of the city's decay. Faint echoes of distant footsteps and the occasional creak of metal reverberate through the narrow passages, shrouded in the veil of morning mist. Ahead, amidst the shadows of a forgotten alley, you find Dr. Elara's sanctuary. The flickering light dances upon weathered stone walls, casting eerie shadows that seem to beckon you closer."""
        delay_print(s)
    elif(stage == 1 and combatcompleted == True):
        s = """The encounter with Dr. Elara has left a mark on your consciousness, like a puzzle piece falling into place amidst the chaos of your thoughts. As you step back into the waking world of Haven City, the streets seem to whisper secrets of their own. The morning sun casts long shadows that stretch across the cobblestones, a stark contrast to the dim recesses of the alley where you et the enigmatic scientist. Your steps feel lighter now, buoyed by a newfound sense of purpose. The weight of Dr. Elara's words lingers in the air, mingling with the scent of morning dew and distant industry. With each footfall, you are drawn closer to the mysteries that lie ahead, you path illuminated by the promise of the Genesis Matrix."""
        delay_print(s)
    elif(stage == 2 and combatcompleted == False):
        s = """Amidst the wreckage of a once-thriving metropolis, you stand at the precipice of uncertainty, your gaze fixed upon the looming shadows of Haven City's outskirts. The air is heavy with the scent of rust and decay, a haunting reminder of humanity's struggle against time and oblivion. The ruins echo with the whispers of forgotten dreams, each shattered building a testament to the fragility of existence. In the distance, the silhouette of a lone figure emerges from the rubble—a rogue bio-engineer known only as Nova. Her presence brings a glimmer of hope to the desolation, a promise of redemption amidst the ruins. With determination etched into her every movement, she beckons you forth, her eyes ablaze with the fire of purpose. Together, you chart a course through the wasteland, your footsteps echoing against the backdrop of crumbling infrastructure. The journey is fraught with danger, yet with Nova at your side, you are emboldened to face whatever trials await. As the sun sets on the horizon, casting long shadows across the desolate landscape, you know that your alliance will be tested like never before."""
        delay_print(s)
    elif(stage == 2 and combatcompleted ==True):
        s = """After countless trials and tribulations, you emerge from the depths of the wasteland, your spirits battered but unbroken. The journey has tested your limits and forged bonds that transcend mere camaraderie. With each step, the weight of your shared experiences hangs heavy upon you both, a burden borne of sacrifice and resilience. As you return to Haven City, the streets are alive with newfound purpose, the once-dormant city pulsating with the energy of renewed hope. The air crackles with anticipation, a tangible sense of change permeating the atmosphere. In the distance, the spires of the city rise like monuments to your triumph, a testament to the resilience of the human spirit. Yet amidst the celebrations, a shadow lingers—a reminder of the challenges that still lie ahead. The enigmatic leader of the Tech Raiders, Cyrus, looms on the horizon, his presence a harbinger of impending conflict. With your allies by your side and the promise of a brighter future within reach, you steel myself for the battles yet to come, knowing that the fate of humanity hangs in the balance."""
        delay_print(s)
    