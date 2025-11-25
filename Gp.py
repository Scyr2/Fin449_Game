import pygame
import pgzrun
import math

from pgzero.actor import Actor

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
btn_number_6 = Actor("btn_number_6")
btn_number_7 = Actor("btn_number_7")
btn_number_8 = Actor("btn_number_8")
btn_number_9 = Actor("btn_number_9")
btn_number_10 = Actor("btn_number_10")
btn_number_11 = Actor("btn_number_11")

#Need to add some sort of plunder system for turns here too later.

# In-Game Actors
player_ship = Actor("player_ship")
weapon_parrot = Actor("weapon_parrot")
weapon_cannon = Actor("weapon_cannon")
weapon_blunderbuss = Actor("weapon_blunderbuss")
cannon_bullet = Actor("weapon_cannon_bullet")

# Settings for the Cannon Game
angle_deg = 0 # Cannon actual angle (degrees)
deg_to_show = 25 # Cannon base angle (degrees)
line_length = 150 # Length of the aiming line
power = 0
cannon_bullets = [] # We need a list to track the active shots
cannon_shoot = True # This tracks the state of the Spacebar when shooting


# Creating the arc line for the Cannon's aim
def draw_arc_from_cannon():
    g = 9.81 # Gravity
    t = 0 # Time step, which is also the accurancy of the line
    v = power # Velocity
    deg_to_show_rad = math.radians(deg_to_show)

    start_x = weapon_cannon.x - line_length / 3.1 * math.cos(deg_to_show_rad)
    start_y = weapon_cannon.y - line_length / 3.1 * math.sin(deg_to_show_rad)

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


# Cannon Game
def cannon_game():
    weapon_cannon.draw()

    if (cannon_shoot and not cannon_bullets):
        draw_arc_from_cannon()

    weapon_cannon.angle = -angle_deg

    # Displaying the angle and power variables to the player
    screen.draw.text(
        f"{deg_to_show}°\nPower: {power}",
        (weapon_cannon.x - 120, weapon_cannon.y + 10),
        fontname = "arial",
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
        fontname = "arial",
        fontsize = 18,
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
    btn_parrot.pos = (500, 175)
    btn_cannon.pos = (500, 325)
    btn_blunderbuss.pos = (500, 450)
    btn_easy.pos = (300, 175)
    btn_medium.pos = (300, 325)
    btn_hard.pos = (300, 450)
    btn_back.pos = (20, 20)
    btn_number_6.pos = (50, 100)
    btn_number_7.pos = (50, 250)
    btn_number_8.pos = (50, 400)
    btn_number_9.pos = (150, 100)
    btn_number_10.pos = (150, 250)
    btn_number_11.pos = (150, 400)
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
    draw_background_cover(images.selections_background)
    selections_menu()
    btn_parrot.draw()
    btn_cannon.draw()
    btn_blunderbuss.draw()
    btn_easy.draw()
    btn_medium.draw()
    btn_hard.draw()
    btn_back.draw()
    btn_number_6.draw()
    btn_number_7.draw()
    btn_number_8.draw()
    btn_number_9.draw()
    btn_number_10.draw()
    btn_number_11.draw()

# Game screen
def draw_game():
    draw_background_cover(images.game_background)
    game_menu()
    player_ship.draw()
    btn_back.draw()

    if selected_weapon == "parrot":
        weapon_parrot.draw()
    if selected_weapon == "cannon":
        cannon_game()        
    if selected_weapon == "blunderbuss":
        weapon_blunderbuss.draw()

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
    global current_screen, settings_open, volume, muted, selected_weapon

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

    if current_screen == "Game" and btn_back.collidepoint(pos):
        current_screen = "Selections"
            
# Game Loop

# Parrot Movement
def update():
    if current_screen == 'Game' and selected_weapon == 'parrot':
        # Move left
        if keyboard.left:
            weapon_parrot.x -= 7

        # Move right
        if keyboard.right:
            weapon_parrot.x += 7

        # Keep the parrot on screen
        if weapon_parrot.left < 0:
            weapon_parrot.left = 0
        if weapon_parrot.right > WIDTH:
            weapon_parrot.right = WIDTH

    if (current_screen == "Game" and selected_weapon == "cannon"):
        global angle_deg, deg_to_show, power, cannon_shoot

        # Angle Controls
        if (keyboard.left):
            angle_deg -= 1
            deg_to_show -= 1
    
        if (keyboard.right):
            angle_deg += 1
            deg_to_show += 1
    
        angle_deg = max(-25, min(65, angle_deg)) # Making sure that -25 <= angle actual degree <= 65
        deg_to_show = max(0, min(90, deg_to_show)) # Making sure that 0 <= base angle degree <= 90

        # Power Controls
        if (keyboard.up):
            power += 1

        if (keyboard.down):
            power -= 1

        power = max(0, min(100, power)) # Limiting power 0 <= Power <= 100

        # Shooting Controls - Spacebar to shoot
        g = 9.81
        t = 0.17 # Time per frame in seconds
        v = power
        deg_to_show_rad = math.radians(deg_to_show)

        if (keyboard.space and cannon_shoot):
            deg_to_show_rad = math.radians(deg_to_show)
        
            start_x = weapon_cannon.x - line_length / 2.2 * math.cos(deg_to_show_rad)
            start_y = weapon_cannon.y - line_length / 2.2 * math.sin(deg_to_show_rad)

            end_x = -v * math.cos(deg_to_show_rad)
            end_y = -v * math.sin(deg_to_show_rad)

            bullet_dic = {
                "Actor": cannon_bullet,
                "x": start_x,
                "y": start_y,
                "Ending x": end_x,
                "Ending y": end_y
            }
            bullet_dic["Actor"].pos = (start_x, start_y)
            cannon_bullets.append(bullet_dic)

            cannon_shoot = False # Waiting for the Spacebar to be released before making another shot, otherwise it will be like a machine gun.

        # Reseting cannon_shoot after Spacebar is released.
        if (not keyboard.space):
            cannon_shoot = True

        for i in cannon_bullets:
            i["x"] += i["Ending x"] * t
            i["Ending y"] += g * t # Gravity
            i["y"] += i["Ending y"] * t
            i["Actor"].pos = (i["x"], i["y"])


#Music start on title screen
music.play("title_screen")
music.set_volume(volume)

pgzrun.go()