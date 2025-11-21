import pygame
import pgzrun

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

# Selection Screen Actors
btn_parrot = Actor("btn_parrot")
btn_cannon = Actor("btn_cannon")
btn_blunderbuss = Actor("btn_blunderbuss")
btn_easy = Actor("btn_easy")
btn_medium = Actor("btn_medium")
btn_hard = Actor("btn_hard")
#Need to add some sort of plunder system for turns here too later.

#In-Game Actors
player_ship = Actor("player_ship")
weapon_parrot = Actor("weapon_parrot")
weapon_cannon = Actor("weapon_cannon")
weapon_blunderbuss = Actor("weapon_blunderbuss")

# Resize helper
def resize_actor(actor, width, height):
    scaled = pygame.transform.smoothscale(actor._surf, (width, height))
    actor._surf = scaled
    actor.width = width
    actor.height = height



# Layout buttons
def layout_menu():
    win_w, win_h = screen.surface.get_size()
    btn_play.pos = (400,300)
    btn_instructions.pos = (win_w - 100, win_h -500)
    btn_settings.pos = (win_w - 100, win_h -350)

    btn_vol_up.pos = (int(win_w * 0.75), int(win_h * 0.45))
    btn_vol_down.pos = (btn_vol_up.x, btn_vol_up.y + 70)
    btn_vol_mute.pos = (btn_vol_up.x, btn_vol_up.y + 140)

#Selection Screen buttons
def selections_menu():
    btn_parrot.pos = (700,75)
    btn_cannon.pos = (700,175)
    btn_blunderbuss.pos = (700,275)
    btn_easy.pos = (700,375)
    btn_medium.pos = (700,475)
    btn_hard.pos = (700,550)

#In Game Buttons and Actors
def game_menu():
    player_ship.pos = (700,400)


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

    screen.draw.filled_rect(panel_rect, (0, 0, 0))
    screen.draw.rect(panel_rect, "white")

    screen.draw.text(
        "Settings",
        midtop=(panel_rect.centerx, panel_rect.top + 10),
        color="white",
        fontsize=32,
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



# Game screen
def draw_game():
    draw_background_cover(images.game_background)
    game_menu()
    player_ship.draw()
    if selected_weapon == "parrot":
        weapon_parrot.draw()
    if selected_weapon == "cannon":
        weapon_cannon.draw()
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

        elif btn_instructions.collidepoint(pos):
            print("Instructions")

        elif btn_settings.collidepoint(pos):
            settings_open = not settings_open

        if settings_open:

            if btn_vol_up.collidepoint(pos):
                volume = min(1.0, volume + 0.1)
                print("Volume up:", round(volume, 2))

            elif btn_vol_down.collidepoint(pos):
                volume = max(0.0, volume - 0.1)
                print("Volume down:", round(volume, 2))

            elif btn_vol_mute.collidepoint(pos):
                muted = not muted
                print("Muted:", muted)


#Selections click handling
    if current_screen == "Selections":

        if btn_parrot.collidepoint(pos):
            selected_weapon = "parrot"
            current_screen = "Game"
            weapon_parrot.pos = (450, 100)
        elif btn_cannon.collidepoint(pos):
            selected_weapon = "cannon"
            current_screen = "Game"
            weapon_cannon.pos = (650, 520)
        elif btn_blunderbuss.collidepoint(pos):
            selected_weapon = "blunderbuss"
            current_screen = "Game"
            weapon_blunderbuss.pos = (650, 520)
#Game Loop

#Parrot Movement
def update():
    if current_screen == 'Game' and selected_weapon == 'parrot':
        #Move left
        if keyboard.left:
            weapon_parrot.x -= 7

        #Move right
        if keyboard.right:
            weapon_parrot.x += 7

        #Keep the parrot on screen
        if weapon_parrot.left < 0:
            weapon_parrot.left = 0
        if weapon_parrot.right > WIDTH:
            weapon_parrot.right = WIDTH


pgzrun.go()
