from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# 1. Initialize 3D Engine Window
app = Ursina()

# 3D Sky & Castle Grounds Ground
Sky()
ground = Entity(model='plane', scale=(200, 1, 200), color=color.rgb(34, 139, 34), collider='box')

# Hogwarts Main Castle Keep
castle = Entity(model='cube', scale=(55, 38, 55), position=(0, 19, 75), color=color.gray, collider='box')
tower_left = Entity(model='cylinder', scale=(9, 36, 9), position=(-25, 18, 45), color=color.dark_gray, collider='box')
tower_right = Entity(model='cylinder', scale=(9, 36, 9), position=(25, 18, 45), color=color.dark_gray, collider='box')

# 🧪 Potion Station: 3D Cauldron & Bubbling Liquid
cauldron = Entity(model='cylinder', scale=(3, 2.5, 3), position=(10, 1.25, 15), color=color.black, collider='box')
cauldron_liquid = Entity(model='cylinder', scale=(2.6, 0.2, 2.6), position=(10, 2.4, 15), color=color.green)

# Foragable Potion Ingredients on Ground
horklump = Entity(model='sphere', scale=1.4, position=(-20, 1, 10), color=color.green, collider='box')
dittany = Entity(model='sphere', scale=1.4, position=(25, 1, 10), color=color.magenta, collider='box')

# Interactive Quest Entities
sorting_hat = Entity(model='cone', scale=(2, 3, 2), position=(0, 1.5, 25), color=color.rgb(120, 70, 20), collider='box')
dummy = Entity(model='cube', scale=(2.5, 6, 2.5), position=(-15, 3, 15), color=color.brown, collider='box')

# 3D Player Controller
player = FirstPersonController(y=2, speed=8)

# Broomstick Entity
broom = Entity(
    parent=camera, model='cylinder', scale=(0.15, 2.0, 0.15), 
    position=(0.3, -0.4, 0.8), rotation=(75, 0, 0), 
    color=color.rgb(110, 60, 20), enabled=False
)
Entity(parent=broom, model='cone', scale=(2.5, 0.6, 2.5), position=(0, -0.8, 0), rotation=(180, 0, 0), color=color.yellow)

# Inventory & Potion Variables
has_horklump = False
has_dittany = False
potions_brewed = 0
potion_active = False

house_name = "Unsorted"
current_spell = "Incendio (Red Fireball)"
is_flying = False
quest_step = 1

lumos_light = PointLight(parent=camera, position=(0,0,1), enabled=False, color=color.white)
protego_shield = Entity(parent=camera, model='sphere', scale=(3,3,3), color=color.rgba(0, 191, 255, 100), enabled=False)

# UI Elements (Quest & Inventory HUD)
quest_title = Text(text="📜 CURRENT QUEST:", position=(-0.85, 0.45), scale=1.1, color=color.gold)
quest_desc = Text(text="Quest 1: Approach the Sorting Hat (Press E)", position=(-0.85, 0.40), scale=0.9, color=color.white)

inv_text = Text(text="🎒 Ingredients: None | Potions: 0", position=(-0.85, 0.34), scale=0.95, color=color.lime)
hud_text = Text(text="Spell: Incendio | House: Unsorted", position=(-0.85, -0.42), scale=1.0, color=color.yellow)
controls_text = Text(text="WASD=Move | E=Interact/Collect/Brew | P=Drink Potion | B=Broom | Keys 1-4=Spells", position=(-0.85, -0.47), scale=0.75, color=color.white)

# Game Update Loop
def update():
    global is_flying
    if is_flying:
        if held_keys['space']:
            player.y += 16 * time.dt
        if held_keys['left shift']:
            player.y -= 16 * time.dt

# Player Inputs & Brewing Mechanics
def input(key):
    global current_spell, house_name, is_flying, quest_step
    global has_horklump, has_dittany, potions_brewed, potion_active

    # Press E to Interact (Sorting, Collect Ingredients, Brew Potions)
    if key == 'e':
        # Quest 1: Sorting Hat
        if quest_step == 1 and distance(player.position, sorting_hat.position) < 8:
            house_name = "Gryffindor"
            quest_step = 2
            quest_desc.text = "Quest 2: Forage ingredients & Brew Wiggenweld Potion at the Cauldron!"
            quest_desc.color = color.lime

        # Collect Horklump Juice
        if horklump.enabled and distance(player.position, horklump.position) < 5:
            horklump.enabled = False
            has_horklump = True
            inv_text.text = f"🎒 Ingredients: {'Horklump ' if has_horklump else ''}{'Dittany' if has_dittany else ''} | Potions: {potions_brewed}"

        # Collect Dittany Leaf
        if dittany.enabled and distance(player.position, dittany.position) < 5:
            dittany.enabled = False
            has_dittany = True
            inv_text.text = f"🎒 Ingredients: {'Horklump ' if has_horklump else ''}{'Dittany' if has_dittany else ''} | Potions: {potions_brewed}"

        # Brew Potion at Cauldron
        if distance(player.position, cauldron.position) < 6:
            if has_horklump and has_dittany:
                has_horklump = False
                has_dittany = False
                potions_brewed += 1
                cauldron_liquid.color = color.cyan
                inv_text.text = f"🎒 Ingredients: None | Potions: {potions_brewed} (Wiggenweld)"
                if quest_step == 2:
                    quest_step = 3
                    quest_desc.text = "Quest 3: Press P to drink potion, then Press B to mount Broom!"
                    quest_desc.color = color.yellow
            else:
                quest_desc.text = "Collect both Green & Purple plants before brewing!"

    # Press P to Drink Potion (Speed Boost!)
    elif key == 'p':
        if potions_brewed > 0:
            potions_brewed -= 1
            player.speed = 16
            inv_text.text = f"🧪 Potion Active! Super Speed Boost! | Potions left: {potions_brewed}"
            cauldron_liquid.color = color.green

    # Toggle Broomstick Flying (B key)
    elif key == 'b':
        if quest_step >= 3:
            is_flying = not is_flying
            broom.enabled = is_flying
            player.gravity = 0 if is_flying else 1
            player.speed = 22 if is_flying else 8

    # Switch Spells (Keys 1, 2, 3, 4)
    elif key == '1':
        current_spell = "Incendio (Red Fireball)"
        lumos_light.enabled = False
        protego_shield.enabled = False
        hud_text.text = f"Spell: {current_spell} | House: {house_name}"
    elif key == '2':
        current_spell = "Levioso (Yellow Levitation)"
        lumos_light.enabled = False
        protego_shield.enabled = False
        hud_text.text = f"Spell: {current_spell} | House: {house_name}"
    elif key == '3':
        current_spell = "Lumos (Wand Light)"
        lumos_light.enabled = not lumos_light.enabled
        protego_shield.enabled = False
        hud_text.text = f"Spell: Lumos | House: {house_name}"
    elif key == '4':
        current_spell = "Protego (Shield Bubble)"
        protego_shield.enabled = not protego_shield.enabled
        lumos_light.enabled = False
        hud_text.text = f"Spell: Protego Shield | House: {house_name}"

    # Cast Wand Spells (Click or F key)
    elif key == 'left mouse down' or key == 'f':
        spell_color = color.red if "Incendio" in current_spell else color.yellow
        spell = Entity(model='sphere', color=spell_color, scale=0.8, position=player.position + camera.forward * 2 + Vec3(0,1,0))
        spell.animate_position(spell.position + camera.forward * 35, duration=0.7)
        destroy(spell, delay=0.7)

# Run 3D Hogwarts Game
app.run()
