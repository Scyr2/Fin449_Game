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

# Button Actors
btn_play = Actor("btn_play")
btn_info = Actor("btn_info")
btn_settings = Actor("btn_settings")
btn_vol_up = Actor("btn_volume_up")
btn_vol_down = Actor("btn_volume_down")
btn_vol_mute = Actor("btn_volume_mute")

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
    btn_info.pos = (win_w - 100, win_h -500)
    btn_settings.pos = (win_w - 100, win_h -450)

    btn_vol_up.pos = (int(win_w * 0.75), int(win_h * 0.45))
    btn_vol_down.pos = (btn_vol_up.x, btn_vol_up.y + 70)
    btn_vol_mute.pos = (btn_vol_up.x, btn_vol_up.y + 140)

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

# Menu draw
def draw_menu():
    draw_background_cover(images.welcome_background)

    layout_menu()
    btn_play.draw()
    btn_info.draw()
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

# Game screen
def draw_game():
    draw_background_cover(images.game_background)

# Main draw
def draw():
    if current_screen == "Menu":
        draw_menu()
    elif current_screen == "Game":
        draw_game()

# Click handling
def on_mouse_down(pos):
    global current_screen, settings_open, volume, muted

    if current_screen == "Menu":

        if btn_play.collidepoint(pos):
            current_screen = "Game"

        elif btn_info.collidepoint(pos):
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

pgzrun.go()
