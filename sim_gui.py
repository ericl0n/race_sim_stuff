import pygame
import sys
from adapter import *
from calibrate_bit import *
import threading
from com_port_selector import *

port = ""
baudrate = 0 

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Handbrake Calibration")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Simulated pressure value (replace with actual handbrake input)
pressure_value = 0
max_pressure = 100

# Font for displaying text
font = pygame.font.Font(None, 36)

# Button settings

button_width, button_height = 120, 45
button_padding = 20

calibrate_button_x = screen_width - button_width - button_padding
calibrate_button_y = screen_height - button_height - button_padding
calibrate_button_rect = pygame.Rect(calibrate_button_x, calibrate_button_y, button_width, button_height)

# Port selection button position
port_button_x = calibrate_button_x - button_width - button_padding - 100
port_button_y = calibrate_button_y
port_button_rect = pygame.Rect(port_button_x, port_button_y, (button_width + 20), button_height)

def display_pressure(screen, pressure):
    screen.fill(WHITE)
    
    # Border for the pressure bar
    border_rect = pygame.Rect(screen_width // 2 - 30, 50, 60, screen_height - 150)
    pygame.draw.rect(screen, BLACK, border_rect, 2)
    
    # Calculate bar height based on pressure, ensuring it stays within the border
    bar_height = int((pressure / max_pressure) * (border_rect.height - 4))
    
    # Draw the pressure bar
    pygame.draw.rect(screen, BLUE, (border_rect.left + 2, border_rect.bottom - bar_height - 2, border_rect.width - 4, bar_height))
    
    # Display the pressure label and value
    label_text = font.render(f"Pressure: {pressure}%", True, BLACK)
    screen.blit(label_text, (screen_width // 2 - 50, border_rect.bottom + 10))
    
    # Draw the calibrate button
    pygame.draw.rect(screen, GRAY, calibrate_button_rect)
    calibrate_button_text = font.render("Calibrate", True, BLACK)
    calibrate_text_rect = calibrate_button_text.get_rect(center=calibrate_button_rect.center)
    screen.blit(calibrate_button_text, calibrate_text_rect)
    
    # Draw the port selection button
    pygame.draw.rect(screen, GRAY, port_button_rect)
    port_button_text = font.render("Port Select", True, BLACK)
    port_text_rect = port_button_text.get_rect(center=port_button_rect.center)
    screen.blit(port_button_text, port_text_rect)
    
    
    pygame.display.flip()

def display_notused(screen):
    screen.fill(BLACK)
    
    pygame.display.flip()


def get_com_vals_s():
    global port
    global baudrate
    val = read_record("com_settings.csv")
    port = val[0][0]
    baudrate = int(val[0][1])

def run_sim_gui():

    if file_exists("com_settings.csv"):
        pass
    else:
        thead2 = threading.Thread(target=run_com_select_window, name="thead2")
        thead2.start()
        while True:
            if thead2.is_alive():
                time.sleep(1)
            else:
                break


    if file_exists("max_min.csv"):
        pass
    else:
        thead1 = threading.Thread(target=import_bit, name="thead1")
        thead1.start()
        while True:
            if thead1.is_alive():
                time.sleep(1)
            else:
                break
                        
                        
    # Main loop
    running = True
    setup_vals()
    get_com_vals_s()
    gamepad = gamepad_setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if calibrate_button_rect.collidepoint(event.pos):
                    thead1 = threading.Thread(target=import_bit, name="thead1")
                    thead1.start()
                    while True:
                        if thead1.is_alive():
                            display_notused(screen)
                            time.sleep(1)
                        else:
                            break
                    setup_vals()
                    print("Calibrate button pressed")
                elif port_button_rect.collidepoint(event.pos):
                    thead2 = threading.Thread(target=run_com_select_window, name="thead2")
                    thead2.start()
                    while True:
                        if thead2.is_alive():
                            display_notused(screen)
                            time.sleep(1)
                        else:
                            break
                    get_com_vals()
                    get_com_vals_s()
                    print("port selected")    
        
        # Simulate reading handbrake pressure (replace with actual reading logic)
        pressure_value = value_to_other_application(port,baudrate)
        handbrake_value_for_gamepad = pressure_value / 100
        
        output_to_ver_controlr(gamepad,handbrake_value_for_gamepad)
        
        display_pressure(screen, pressure_value)
        
        # Control the frame rate
        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()

