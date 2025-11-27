import pygame
import pgzrun
import math
import random

from pgzero.actor import Actor
from pygame.gfxdraw import rectangle

# Base sizes
base_width = 800
base_height = 600
WIDTH = base_width
HEIGHT = base_height

current_screen = "Menu"
settings_open = False
volume = 0.5
muted = False
selected_weapon = None
selected_level = None

# Button Actors
btn_play = Actor("btn_play")
btn_settings = Actor("btn_settings")
btn_vol_up = Actor("btn_volume_up")
btn_vol_down = Actor("btn_volume_down")
btn_vol_mute = Actor("btn_volume_mute")
btn_instructions = Actor("btn_instructions")
btn_back = Actor("btn_back")

# Selection Screen Actors
btn_parrot = Actor("btn_parrot")
btn_cannon = Actor("btn_cannon")
btn_blunderbuss = Actor("btn_blunderbuss")
btn_easy = Actor("btn_easy")
btn_medium = Actor("btn_medium")
btn_hard = Actor("btn_hard")
plunders_box_img = Actor("plunders_box")
plunders_box = Rect(200, 310, 150, 40)
easy_box = Rect(425, 132, 150, 86)
medium_box = Rect(425, 282, 150, 86)
hard_box = Rect(425, 432, 150, 86)

#Need to add some sort of plunder system for turns here too later.

# In-Game Actors
player_ship = Actor("player_ship")
weapon_parrot = Actor("weapon_parrot")
weapon_cannon = Actor("weapon_cannon")
weapon_blunderbuss = Actor("weapon_blunderbuss")
cannon_bullet = Actor("weapon_cannon_bullet")
parrot_bullet = Actor("weapon_parrot_bullet")
blunderbuss_bullet = Actor("weapon_blunderbuss_bullet")


#Settings for the Parrot Game
parrot_bullets = [] #Active shots for parrot
parrot_shoot = True # This tracks the state of the Spacebar when shooting


# Settings for the Cannon Game
angle_deg = 0 # Cannon actual angle (degrees)
deg_to_show = 25 # Cannon base angle (degrees)
line_length = 150 # Length of the aiming line
power = 0
cannon_bullets = [] # We need a list to track the active shots
cannon_shoot = True # This tracks the state of the Spacebar when shooting

# Settings for the Blunderbuss Game
blunderbuss_angle_deg = 0
blunderbuss_bullets = []
blunderbuss_shoot = True
blunderbuss_offset_x = -73
blunderbuss_offset_y = -6



pirate_r_list = []
player_r_list = []
landing_x = 0
player_r_guess = 0 # The player's IRR guess
shot_message = ""
booty = random.randint(1, 100) # The CFs for the NPV
blood = 0 # This is the initial cost for a project, for example

plunder_text = ""
plunder_box_active = False
plunders = 1

easy_box_active = False
medium_box_active = False
hard_box_active = False

game_over = False
current_turn = "Player"
rounds_left = plunders
pirate_r_guess = None
midpoint = [0, 1.0]
player_message_timer = 0.0
pending_pirate_turn = False
pirate_message_timer = 0.0 # How long to keep the Pirate's message
pirate_has_acted = False # An indicator of whether the Pirate made his turn
pending_player_turn = False
player_turn_message_timer = 0.0
last_player_message = ""



for i in range(5):
    pirate_r_list.append(round(random.uniform(0.2, 0.8), 2)) # Drawing 5 random locations (r values) for the pirate

pirate_current_r = round(random.choice(pirate_r_list), 2) # Selecting a location for the pirate at random

for i in range(5):
    player_r_list.append(round(random.uniform(0.2, 0.8), 2)) # Drawing 5 random locations (r values) for the pirate

player_current_r = random.choice(pirate_r_list) # Selecting a location for the pirate at random


def npv_zero(my_r, opponent_r, time_to_maturity):
    global blood
    npv = 0 

    if my_r == 0:
        npv = booty * time_to_maturity # When the discount rate is 0, money in the future is the same as money today
    else:
        blood = int(booty / opponent_r * (1 - (1 + opponent_r)**(-time_to_maturity)) - npv)

        npv = booty / my_r * (1 - (1 + my_r)**(-time_to_maturity)) - blood # Since it's an annuity
        npv = round(npv, 2)

    return npv

def blunderbuss_barrel_tip():
    rad = math.radians(blunderbuss_angle_deg)

    lx = blunderbuss_offset_x
    ly = blunderbuss_offset_y

    rx = lx * math.cos(rad) - ly * math.sin(rad)
    ry = lx * math.sin(rad) + ly * math.cos(rad)

    start_x = weapon_blunderbuss.x + rx
    start_y = weapon_blunderbuss.y + ry

    return start_x, start_y

# Creating the arc line for the Cannon's aim
def draw_cannon_arc():
    g = 9.81 # Gravity
    t = 0 # Time step, which is also the accuracy of the line
    v = power # Velocity
    deg_to_show_rad = math.radians(deg_to_show)

    start_x = weapon_cannon.x - line_length / 2.2 * math.cos(deg_to_show_rad)
    start_y = weapon_cannon.y - line_length / 2.2 * math.sin(deg_to_show_rad)

    positions = []

    while True:
        x = v * math.cos(deg_to_show_rad) * t # # Using the physics equation y(t) = v * cos(θ) * t to find the x value of the point
        y = v * math.sin(deg_to_show_rad) * t - 0.5 * g * t**2 # Using the physics equation y(t) = v * sin(θ) * t -0.5 * g * t^2 to find the y value of the point

        screen_x = start_x - x # This will give us the distance from the current point to the next on x-axis
        screen_y = start_y - y # This will give us the distance from the current point to the next on y-axis

        if (screen_x < 0 or screen_y > HEIGHT):
            break

        positions.append((screen_x, screen_y))
        t += 0.2 # Time step, which is also the accurancy of the line

    for i in range(len(positions) - 1):
        screen.draw.line(positions[i], positions[i + 1], "yellow")


# Drawing the arc for the Blunderbuss
def draw_blunderbuss_arc():
    g = 9.81 # Gravity
    t = 0 # Time step, which is also the accuracy of the line
    v = power # Velocity
    blunderbuss_angle_deg_rad = math.radians(blunderbuss_angle_deg)

    #start_x = weapon_blunderbuss.x - line_length / 1.9 * math.cos(deg_to_show_rad)
    #start_y = weapon_blunderbuss.y - line_length / 9 * math.sin(deg_to_show_rad)

    start_x, start_y = blunderbuss_barrel_tip()

    positions = []

    while True:
        x = v * math.cos(blunderbuss_angle_deg_rad) * t # # Using the physics equation y(t) = v * cos(θ) * t to find the x value of the point
        y = v * math.sin(blunderbuss_angle_deg_rad) * t - 0.5 * g * t**2 # Using the physics equation y(t) = v * sin(θ) * t -0.5 * g * t^2 to find the y value of the point

        screen_x = start_x - x # This will give us the distance from the current point to the next on x-axis
        screen_y = start_y - y # This will give us the distance from the current point to the next on y-axis

        if (screen_x < 0 or screen_y > HEIGHT):
            break

        positions.append((screen_x, screen_y))
        t += 0.2 # Time step, which is also the accurancy of the line

    for i in range(len(positions) - 1):
        screen.draw.line(positions[i], positions[i + 1], "yellow")


# Cannon Game
def cannon_game():
    weapon_cannon.draw()

    if cannon_shoot and not cannon_bullets:
        draw_cannon_arc()

    weapon_cannon.angle = -angle_deg

    # Displaying the angle and power variables to the player
    screen.draw.text(
        f"{deg_to_show}°\nPower: {power}",
        (weapon_cannon.x - 120, weapon_cannon.y + 10),
        fontname = "pixel_reg",
        fontsize = 18,
        color = "white"
    )

    # Draw cannon bullets
    for i in cannon_bullets:
        i["Actor"].draw()

    # Telling the player how to shoot
    screen.draw.text(
        "Press SPACE to shoot",
        (WIDTH // 2 - 100, HEIGHT -40),
        fontname = "pixel_reg",
        fontsize = 25,
        color = "white"
    )

    if shot_message:
        screen.draw.text(
            shot_message,
            (60, 60),
            fontname = "pixel_reg",
            fontsize = 22,
            color = "white"
        )

    screen.draw.text(
        f"Turn: {current_turn.upper()} | Rounds left: {rounds_left}",
        (60, 20),
        fontname = "pixel_reg",
        fontsize = 26,
        color = "white"
    )


def blunderbuss_game():
    weapon_blunderbuss.draw()

    if blunderbuss_shoot and not blunderbuss_bullets:
        draw_blunderbuss_arc()

    weapon_blunderbuss.angle = -blunderbuss_angle_deg

    # Displaying the angle and power variables to the player
    screen.draw.text(
        f"{blunderbuss_angle_deg}°\nPower: {power}",
        (weapon_blunderbuss.x - 120, weapon_blunderbuss.y + 10),
        fontname = "pixel_reg",
        fontsize = 18,
        color = "white"
    )

    # Draw Blunderbuss bullets
    for i in blunderbuss_bullets:
        i["Actor"].draw()

    # Telling the player how to shoot
    screen.draw.text(
        "Press SPACE to shoot",
        (WIDTH // 2 - 100, HEIGHT -40),
        fontname = "pixel_reg",
        fontsize = 25,
        color = "white"
    )

    if shot_message:
        screen.draw.text(
            shot_message,
            (60, 60),
            fontname = "pixel_reg",
            fontsize = 22,
            color = "white"
        )

    screen.draw.text(
        f"Turn: {current_turn.upper()} | Rounds left: {rounds_left}",
        (60, 20),
        fontname = "pixel_reg",
        fontsize = 26,
        color = "white"
    )


# Layout buttons
def layout_menu():
    win_w, win_h = screen.surface.get_size()
    btn_play.pos = (300, 500)
    btn_instructions.pos = (500, 500)
    btn_settings.pos = (win_w - 50, win_h - 50)

    btn_vol_up.pos = (int(win_w * 0.75), int(win_h * 0.45))
    btn_vol_down.pos = (btn_vol_up.x, btn_vol_up.y + 70)
    btn_vol_mute.pos = (btn_vol_up.x, btn_vol_up.y + 140)

# Selection Screen buttons
def selections_menu():
    btn_parrot.pos = (700, 175)
    btn_cannon.pos = (700, 325)
    btn_blunderbuss.pos = (700, 475)
    btn_easy.pos = (500, 175)
    btn_medium.pos = (500, 325)
    btn_hard.pos = (500, 475)
    btn_back.pos = (20, 20)
    plunders_box_img.pos = (200, 300)
# In Game Buttons and Actors
def game_menu():
    player_ship.pos = (700, 400)
    btn_back.pos = (20, 20)


# Draw background image to cover screen
def draw_background_cover(image):
    win_w, win_h = screen.surface.get_size()
    img_w, img_h = image.get_size()

    scale = max(win_w / img_w, win_h / img_h)

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    scaled = pygame.transform.smoothscale(image, (new_w, new_h))
    x = (win_w - new_w) // 2
    y = (win_h - new_h) // 2

    screen.blit(scaled, (x, y))

# Main Menu draw
def draw_menu():
    draw_background_cover(images.welcome_background)
    layout_menu()
    btn_play.draw()
    btn_instructions.draw()
    btn_settings.draw()

    # Title

    if settings_open:
        win_w, win_h = screen.surface.get_size()
        draw_settings_panel(win_w, win_h)

# Settings panel
def draw_settings_panel(win_w, win_h):
    panel_rect = pygame.Rect(
        int(win_w * 0.65),
        int(win_h * 0.30),
        int(win_w * 0.28),
        int(win_h * 0.50),
    )

    screen.draw.filled_rect(panel_rect, (255, 255, 255))
    screen.draw.rect(panel_rect, "black")

    screen.draw.text(
        "Settings",
        midtop=(panel_rect.centerx, panel_rect.top + 10),
        fontname = "pixel_reg",
        fontsize = 30,
        color = "black"
    )

    btn_vol_up.draw()
    btn_vol_down.draw()
    btn_vol_mute.draw()

# Weapon selection and difficulty selection screen
def draw_selections():
    selections_menu()
    draw_background_cover(images.selections_background)
    pirate_rect = Rect(
        plunders_box_img.left+150,
        plunders_box_img.top+230,
        plunders_box_img.width/15,
        plunders_box_img.height/5
    )
    screen.draw.filled_rect(pirate_rect, "white")
    btn_parrot.draw()
    btn_cannon.draw()
    btn_blunderbuss.draw()
    btn_easy.draw()
    btn_medium.draw()
    btn_hard.draw()
    btn_back.draw()
    plunders_box_img.draw()

    border_color = "orange" if plunder_box_active else "black"

    screen.draw.filled_rect(plunders_box, "white") # Drawing the Plunders text box
    screen.draw.rect(plunders_box, border_color) # Drawing the border of the Plunders text box

    easy_level_color = "white" if easy_box_active else "black"
    screen.draw.rect(easy_box, easy_level_color)

    medium_level_color = "white" if medium_box_active else "black"
    screen.draw.rect(medium_box, medium_level_color)

    hard_level_color = "white" if hard_box_active else "black"
    screen.draw.rect(hard_box, hard_level_color)

    screen.draw.text(
        plunder_text,
        (plunders_box.x + 5, plunders_box.y + 5),
        fontsize = 32,
        color = "black",
        fontname = "pixel_reg",
    )

# Game screen
def draw_game():
    draw_background_cover(images.game_background)
    game_menu()
    player_ship.draw()
    btn_back.draw()

    if selected_weapon == "parrot":
        weapon_parrot.draw()

        # Telling the player how to shoot
        screen.draw.text(
            "Press SPACE to shoot",
            (WIDTH // 2 - 100, HEIGHT -40),
            fontname = "pixel_reg",
            fontsize = 25,
            color = "white"
        )

    # New code start for parrot - Myles
        # Game info to display
        screen.draw.text(
            f"Turn:{current_turn.upper()} | Rounds left: {rounds_left}",
            (60,20),
            fontname = "pixel_reg",
            fontsize = 26,
            color = "white"
        )

        # Display results of shot for parrot
        if shot_message:
            screen.draw.text(
            shot_message,
            (60,60),
            fontname = "pixel_reg",
            fontsize = 22,
            color = "white"
        )

        for i in parrot_bullets:
            i["Actor"].draw()
            
    if selected_weapon == "cannon":
        cannon_game()        
    if selected_weapon == "blunderbuss":
        blunderbuss_game()

# Main draw
def draw():
    if current_screen == "Menu":
        draw_menu()
    if current_screen == "Selections":
        draw_selections()
    elif current_screen == "Game":
        draw_game()

# Click handling
def on_mouse_down(pos):
    global current_screen, settings_open, volume, muted, selected_weapon, selected_level
    global plunder_box_active, easy_box_active, medium_box_active, hard_box_active

    if current_screen == "Menu":

        if btn_play.collidepoint(pos):
            current_screen = "Selections"
        # Optional: Uncomment line below if you want music to stop when leaving menu
        # music.stop()

        elif btn_instructions.collidepoint(pos):
            print("Instructions")

        elif btn_settings.collidepoint(pos):
            settings_open = not settings_open

        if settings_open:

            if btn_vol_up.collidepoint(pos):
                volume = min(1.0, volume + 0.1)
                if not muted: # Only updates when not muted
                    music.set_volume(volume)
                print("Volume up:", round(volume, 2))

            elif btn_vol_down.collidepoint(pos):
                volume = max(0.0, volume - 0.1)
                if not muted:
                    music.set_volume(volume)
                print("Volume down:", round(volume, 2))

            elif btn_vol_mute.collidepoint(pos):
                muted = not muted
                if music:
                    music.set_volume(0)
                else:
                    music.set_volume(volume)
                print("Muted:", muted)


# Selections click handling
    if current_screen == "Selections":
    
        # This is for the Plunders text box
        if plunders_box.collidepoint(pos):
            plunder_box_active = True
        else:
            plunder_box_active = False

        # Highlighting the level buttons
        if easy_box.collidepoint(pos):
            easy_box_active = True
            medium_box_active = False
            hard_box_active = False

        if medium_box.collidepoint(pos):
            medium_box_active = True
            easy_box_active = False
            hard_box_active = False

        if hard_box.collidepoint(pos):
            hard_box_active = True
            medium_box_active = False
            easy_box_active = False
        
        if (btn_back.collidepoint(pos)):
            current_screen = "Menu"
        
        if btn_parrot.collidepoint(pos):
            selected_weapon = "parrot"
            current_screen = "Game"
            weapon_parrot.pos = (450, 100)

        elif btn_cannon.collidepoint(pos):
            selected_weapon = "cannon"
            current_screen = "Game"
            weapon_cannon.pos = (650, 540)

        elif btn_blunderbuss.collidepoint(pos):
            selected_weapon = "blunderbuss"
            current_screen = "Game"
            weapon_blunderbuss.pos = (650, 520)

        if btn_easy.collidepoint(pos):
            selected_level = "Easy"
        elif btn_medium.collidepoint(pos):
            selected_level = "Medium"
        elif btn_hard.collidepoint(pos):
            selected_level = "Hard"

    if current_screen == "Game" and btn_back.collidepoint(pos):
        current_screen = "Selections"
            
# Game Loop

# Parrot Movement
def update():
    global rounds_left, current_turn, game_over, pirate_r_guess
    global angle_deg, deg_to_show, power, parrot_shoot, cannon_shoot, blunderbuss_shoot, blunderbuss_angle_deg
    global landing_x, player_r_guess, shot_message, last_player_message
    global pirate_has_acted, pirate_message_timer
    global player_message_timer, pending_pirate_turn, pending_player_turn, player_turn_message_timer

    g = 9.81
    t = 0.17 # Time per frames in seconds

    if pending_pirate_turn and not game_over:
        player_message_timer -= t

        if player_message_timer <= 0:
            pending_pirate_turn = False
            current_turn = "Pirate"
            pirate_has_acted = False
            pirate_message_timer = 0.0

    if pending_player_turn and not game_over:
        player_turn_message_timer -= t

        if player_turn_message_timer <= 0:
            pending_player_turn = False
            current_turn = "Player"
            shot_message = "ARR, It's Your Turn Captain!\n" + last_player_message[24:]

    # Pirate game loop using logic from cannon
    if current_screen == 'Game' and selected_weapon == 'parrot':

        if not game_over and current_turn == "Pirate":
            # If the Pirate did not play yet
            if not pirate_has_acted:
                pirate_r_guess = round(random.uniform(0.2, 0.8), 2)

                # Took bisection logic from cannon
                if selected_level == "Easy":
                    pirate_r_guess = round((midpoint[0] + midpoint[1]) / 2, 2)
                    if npv_zero(pirate_r_guess, player_current_r, plunders) > 0:
                        midpoint[0] = pirate_r_guess
                    else:
                        midpoint[1] = pirate_r_guess

                # Check if Pirate Won
                if abs(pirate_r_guess - player_current_r) < 0.01:
                    shot_message = (f"The Pirate Hit You! You Lost!\nPirate guessed r = {pirate_r_guess}")
                    game_over = True
                else:
                    rounds_left -= 1
                    if rounds_left <= 0:
                        shot_message = (f"Pirate guessed r = {pirate_r_guess}\nOut of Plunders! Draw!")
                        game_over = True
                    else:
                        shot_message = (
                            "The Pirate Missed Us!\n"
                            f"Pirate's r guess: {pirate_r_guess}\n"
                            f"Pirate's NPV: {npv_zero(pirate_r_guess, player_current_r, plunders)}"
                        )

                pirate_message_timer = 15.0
                pirate_has_acted = True

            else:
                pirate_message_timer -= t
                if pirate_message_timer <= 0 and not game_over:
                    pirate_has_acted = False
                    pending_player_turn = True
                    player_turn_message_timer = 10.0
                    current_turn = "Between"

       # How the parrote moves
        if current_turn == "Player" and game_over == False:  # Only move if it's player turn
            if keyboard.left:
                weapon_parrot.x -= 7
            if keyboard.right:
                weapon_parrot.x += 7

            # Keep the parrot on screen
            if weapon_parrot.left < 0:
                weapon_parrot.left = 0
            if weapon_parrot.right > WIDTH:
                weapon_parrot.right = WIDTH

            if keyboard.space and parrot_shoot and len(parrot_bullets) == 0:
                start_x = weapon_parrot.x
                start_y = weapon_parrot.y + 50 # The 50 will start the drop below the parrot
                parrot_dic = {
                    "Actor": Actor("weapon_parrot_bullet"),
                    "x": start_x,
                    "y": start_y,
                    "vy": 0 # We start with a velocity of 0
                }
                parrot_bullets.append(parrot_dic)
                parrot_shoot = False # Stops parrot from multiple shots

                # Reseting parrot_shoot
    if not keyboard.space:
        parrot_shoot = True

    for i in parrot_bullets:
        i["vy"] += g * t # gravity is added to the vertical speed, increases with time
        i["y"] += i["vy"] * t # Updates the vert position to move with time
        i["Actor"].pos = (i["x"], i["y"]) # Draws our bomb at the new cooridinates

        # Hit marker check on ground
        if i["y"] >= HEIGHT:
            landing_x = i["x"]

            # Took this math from cannon
            player_r_guess = max(0, min(1, landing_x / WIDTH))
            player_r_guess = round(player_r_guess, 2)

            if abs(player_r_guess - pirate_current_r) < 0.01:
                shot_message = "ARR You Won!"
                game_over = True
            else:
                last_player_message = (
                    "You Missed Him, Captain!"
                    f"\nPirate's Current r value: {pirate_current_r}"
                    f"\nYour NPV: {npv_zero(player_r_guess, pirate_current_r, plunders)}"
                    f"\nPlayer's r guess: {player_r_guess}"
                    f"\nPlunders: {plunders}"
                )
                shot_message = last_player_message
                current_turn = "Resolving"
                player_message_timer = 30.0
                pending_pirate_turn = True

            parrot_bullets.remove(i)  # Remove bullet after it hits ground
    # End of parrot gameloop

    # The Cannon Game
    if current_screen == "Game" and selected_weapon == "cannon":
        if not game_over and current_turn == "Pirate":
            pirate_r_guess = round(random.uniform(0.2, 0.8), 2)

            # If the Pirate did not play yet    
            if not pirate_has_acted:

                # Setting the Easy Level Game with the Bisection Method
                if selected_level == "Easy":
                    pirate_r_guess = round((midpoint[0] + midpoint[1]) / 2, 2)

                    if npv_zero(pirate_r_guess, player_current_r, plunders) > 0:
                        midpoint[0] = pirate_r_guess
                    else:
                        midpoint[1] = pirate_r_guess
                #elif selected_level == "Medium":

                if abs(pirate_r_guess - player_current_r) < 0.01:
                    shot_message = (
                        "The Pirate Hit You! You Lost!"
                        f"\nPirate guessed r = {pirate_r_guess}"
                    )
                    game_over = True
                else:
                    rounds_left -= 1

                    if rounds_left <= 0:
                        shot_message = (
                            f"Pirate guessed r = {pirate_r_guess}"
                            "\nOut of Plunders! Draw / You Survived!"
                        )
                        game_over = True
                    else:
                        shot_message = (
                            "Phew... The Pirate Missed Us, Captain!"
                            f"\nPirate's r guess: {pirate_r_guess}"
                            f"\nPirate's NPV: {npv_zero(pirate_r_guess, player_current_r, plunders)}"
                            f"\nBlood (Cost): {blood}"
                            f"\nBooty (Return): {booty}"
                            f"\nYour Current r value: {player_current_r}"
                            f"\nPlunders: {plunders}"
                            f"\nRounds left: {rounds_left}"
                        )

                pirate_message_timer = 15.0
                pirate_has_acted = True

            else:
                pirate_message_timer -= t

                if pirate_message_timer <= 0 and not game_over:
                    pirate_has_acted = False
                    pending_player_turn = True
                    player_turn_message_timer = 10.0
                    current_turn = "Between" # Freezing shooting


        if not game_over and current_turn == "Player":

            # Angle Controls
            if keyboard.left:
                angle_deg -= 1
                deg_to_show -= 1
        
            if keyboard.right:
                angle_deg += 1
                deg_to_show += 1
        
            angle_deg = max(-25, min(65, angle_deg)) # Making sure that -25 <= angle actual degree <= 65
            deg_to_show = max(0, min(90, deg_to_show)) # Making sure that 0 <= base angle degree <= 90

            # Power Controls
            if keyboard.up:
                power += 1

            if keyboard.down:
                power -= 1

            power = max(0, min(100, power)) # Limiting power 0 <= Power <= 100

            
            v = power
            deg_to_show_rad = math.radians(deg_to_show)

            if keyboard.space and cannon_shoot and len(cannon_bullets) == 0 and not game_over and current_turn == "Player":
            
                start_x = weapon_cannon.x - line_length / 2.2 * math.cos(deg_to_show_rad) # x starting value for the weapon_cannon_buller the image
                start_y = weapon_cannon.y - line_length / 2.2 * math.sin(deg_to_show_rad)

                end_x = -v * math.cos(deg_to_show_rad)
                end_y = -v * math.sin(deg_to_show_rad)

                bullet_dic_cannon = {
                    "Actor": cannon_bullet,
                    "x": start_x,
                    "y": start_y,
                    "Ending x": end_x,
                    "Ending y": end_y
                }
                bullet_dic_cannon["Actor"].pos = (start_x, start_y)
                cannon_bullets.append(bullet_dic_cannon)

                cannon_shoot = False # Waiting for the Spacebar to be released before making another shot, otherwise it will be like a machine gun.

            # Reseting cannon_shoot after Spacebar is released.
            if not keyboard.space:
                cannon_shoot = True

            for i in cannon_bullets:
                i["x"] += i["Ending x"] * t
                i["Ending y"] += g * t # Gravity
                i["y"] += i["Ending y"] * t
                i["Actor"].pos = (i["x"], i["y"])

                if i["y"] >= HEIGHT or i["x"] <= 0:
                    landing_x = i["x"] # We're saving the x value when x lands

                    player_r_guess = max(0, min(1, landing_x / WIDTH)) # The r guess the player made can only be between 0 and 1 and is calculated by getting its proportion to the entire screen.
                    player_r_guess = round(player_r_guess, 2)

                    if abs(player_r_guess - pirate_current_r) < 0.01:
                        shot_message = "ARR You Won!"
                        game_over = True
                    else:
                        last_player_message = (
                            "You Missed Him, Captain!"
                            f"\nPirate's Current r value: {pirate_current_r}"
                            f"\nYour NPV: {npv_zero(player_r_guess, pirate_current_r, plunders)}"
                            f"\nBlood (Cost): {blood}"
                            f"\nBooty (Return): {booty}"
                            f"\nPlayer's r guess: {player_r_guess}"
                            f"\nPlunders: {plunders}"
                            )
                        shot_message = last_player_message
                        current_turn = "Resolving" # We're doing this so that the player wouldn't be able to shoot after he made a shot
                        player_message_timer = 30.0
                        pending_pirate_turn = True

                    cannon_bullets.remove(i)

    # The Blunderbuss Game
    if current_screen == "Game" and selected_weapon == "blunderbuss":
        if not game_over and current_turn == "Pirate":
            pirate_r_guess = round(random.uniform(0.2, 0.8), 2)

            # If the Pirate did not play yet    
            if not pirate_has_acted:

                # Setting the Easy Level Game with the Bisection Method
                if selected_level == "Easy":
                    pirate_r_guess = round((midpoint[0] + midpoint[1]) / 2, 2)

                    if npv_zero(pirate_r_guess, player_current_r, plunders) > 0:
                        midpoint[0] = pirate_r_guess
                    else:
                        midpoint[1] = pirate_r_guess
                #elif selected_level == "Medium":

                if abs(pirate_r_guess - player_current_r) < 0.01:
                    shot_message = (
                        "The Pirate Hit You! You Lost!"
                        f"\nPirate guessed r = {pirate_r_guess}"
                    )
                    game_over = True
                else:
                    rounds_left -= 1

                    if rounds_left <= 0:
                        shot_message = (
                            f"Pirate guessed r = {pirate_r_guess}"
                            "\nOut of Plunders! Draw / You Survived!"
                        )
                        game_over = True
                    else:
                        shot_message = (
                            "Phew... The Pirate Missed Us, Captain!"
                            f"\nPirate's r guess: {pirate_r_guess}"
                            f"\nPirate's NPV: {npv_zero(pirate_r_guess, player_current_r, plunders)}"
                            f"\nBlood (Cost): {blood}"
                            f"\nBooty (Return): {booty}"
                            f"\nYour Current r value: {player_current_r}"
                            f"\nPlunders: {plunders}"
                            f"\nRounds left: {rounds_left}"
                        )

                pirate_message_timer = 15.0
                pirate_has_acted = True

            else:
                pirate_message_timer -= t

                if pirate_message_timer <= 0 and not game_over:
                    pirate_has_acted = False
                    pending_player_turn = True
                    player_turn_message_timer = 10.0
                    current_turn = "Between" # Freezing shooting


        if not game_over and current_turn == "Player":

            # Angle Controls
            if keyboard.left:
                blunderbuss_angle_deg -= 1
        
            if keyboard.right:
                blunderbuss_angle_deg += 1
        
            blunderbuss_angle_deg = max(0, min(90, blunderbuss_angle_deg)) # Making sure that 0 <= base angle degree <= 90

            # Power Controls
            if keyboard.up:
                power += 1

            if keyboard.down:
                power -= 1

            power = max(0, min(100, power)) # Limiting power 0 <= Power <= 100

            
            v = power
            blunderbuss_angle_deg_rad = math.radians(blunderbuss_angle_deg)

            if keyboard.space and blunderbuss_shoot and len(blunderbuss_bullets) == 0 and not game_over and current_turn == "Player":
            
                #start_x = weapon_blunderbuss.x - line_length / 2.5 * math.cos(deg_to_show_rad) # x starting value for the weapon_blunderbuss_buller the image
                #start_y = weapon_blunderbuss.y - line_length / 3 * math.sin(deg_to_show_rad)

                start_x, start_y = blunderbuss_barrel_tip()

                end_x = -v * math.cos(blunderbuss_angle_deg_rad)
                end_y = -v * math.sin(blunderbuss_angle_deg_rad)

                bullet_dic_blunderbuss = {
                    "Actor": blunderbuss_bullet,
                    "x": start_x,
                    "y": start_y,
                    "Ending x": end_x,
                    "Ending y": end_y
                }
                bullet_dic_blunderbuss["Actor"].pos = (start_x, start_y)
                blunderbuss_bullets.append(bullet_dic_blunderbuss)

                blunderbuss_shoot = False # Waiting for the Spacebar to be released before making another shot, otherwise it will be like a machine gun.

            # Reseting blunderbuss_shoot after Spacebar is released.
            if not keyboard.space:
                blunderbuss_shoot = True

            for i in blunderbuss_bullets:
                i["x"] += i["Ending x"] * t
                i["Ending y"] += g * t # Gravity
                i["y"] += i["Ending y"] * t
                i["Actor"].pos = (i["x"], i["y"])

                if i["y"] >= HEIGHT or i["x"] <= 0:
                    landing_x = i["x"] # We're saving the x value when x lands

                    player_r_guess = max(0, min(1, landing_x / WIDTH)) # The r guess the player made can only be between 0 and 1 and is calculated by getting its proportion to the entire screen.
                    player_r_guess = round(player_r_guess, 2)

                    if abs(player_r_guess - pirate_current_r) < 0.01:
                        shot_message = "ARR You Won!"
                        game_over = True
                    else:
                        last_player_message = (
                            "You Missed Him, Captain!"
                            f"\nPirate's Current r value: {pirate_current_r}"
                            f"\nYour NPV: {npv_zero(player_r_guess, pirate_current_r, plunders)}"
                            f"\nBlood (Cost): {blood}"
                            f"\nBooty (Return): {booty}"
                            f"\nPlayer's r guess: {player_r_guess}"
                            f"\nPlunders: {plunders}"
                            )
                        shot_message = last_player_message
                        current_turn = "Resolving" # We're doing this so that the player wouldn't be able to shoot after he made a shot
                        player_message_timer = 30.0
                        pending_pirate_turn = True

                    blunderbuss_bullets.remove(i)  


# This function is for handling the PLunders text box
def on_key_down(key):
    global plunder_text, plunder_box_active, plunders
    global rounds_left, current_turn, game_over, pirate_r_guess, pirate_current_r, player_current_r


    if not plunder_box_active:
        return
    

    # If the user wants to erased the values he typed
    if key == keys.BACKSPACE:
        plunder_text = plunder_text[:-1]
        return

    # Handling the plunder's text box
    if key == keys.RETURN: # If the player presses ENTER

        if plunder_text.isdigit() and int(plunder_text) > 0:
            plunders = int(plunder_text)
        else:
            plunders = 1 # Defaulting to pluders of 1 if an empty box was entered
        
        plunder_text = "" # Clear box after enter
        plunder_box_active = False
        midpoint[0], midpoint[1] = 0, 1.0
        pirate_current_r = round(random.choice(pirate_r_list), 2)
        player_current_r = random.choice(pirate_r_list)

        # Reset game state that depends on plunders
        current_turn = "Player"
        game_over = False
        pirate_r_guess = None
        rounds_left = plunders

        return
    
    # Defining the digits in a dictionary
    digit_map = {
        keys.K_0: "0", keys.K_1: "1", keys.K_2: "2", keys.K_3: "3", keys.K_4: "4",
        keys.K_5: "5", keys.K_6: "6", keys.K_7: "7", keys.K_8: "8", keys.K_9: "9",
        keys.KP0: "0", keys.KP1: "1", keys.KP2: "2", keys.KP3: "3", keys.KP4: "4",
        keys.KP5: "5", keys.KP6: "6", keys.KP7: "7", keys.KP8: "8", keys.KP9: "9",
    }

    # If the keyboard key that the user is pressing is in the dictionary then we add it to plunder_text
    if key in digit_map:
        plunder_text += digit_map[key]

        # Here we're limiting the figure number
        if len(plunder_text) > 3:
            plunder_text = plunder_text[:3]




#Parrot ends above here.


#Music start on title screen
music.play("title_screen")
music.set_volume(volume)

pgzrun.go()