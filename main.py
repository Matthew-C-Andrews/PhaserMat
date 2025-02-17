import pygame
import psycopg2
import socket
import time

# -----------------------
# Configuration Settings
# -----------------------
DB_NAME = "photon"
DB_USER = "student"
DB_PASSWORD = "student" 
DB_HOST = "localhost"

UDP_PORT = 7500              # UDP broadcast port
DEFAULT_UDP_IP = "127.0.0.1"    # Default UDP target IP

# -----------------------
# Pygame Initialization & Constants
# -----------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Phaser Project")
FONT = pygame.font.Font(None, 28)
CLOCK = pygame.time.Clock()

# Colors
BG_COLOR = pygame.Color('black')
TEXT_COLOR = pygame.Color('white')
INFO_COLOR = pygame.Color('yellow')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BUTTON_COLOR = pygame.Color('gray')

# -----------------------
# Load Splash Image
# -----------------------
try:
    splash_image = pygame.image.load("logo.jpg")
    splash_image = pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print("Error loading splash image:", e)
    splash_image = None

# -----------------------
# Helper Classes for Input & Buttons
# -----------------------
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, TEXT_COLOR)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, TEXT_COLOR)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BUTTON_COLOR
        self.text = text
        self.txt_surface = FONT.render(text, True, TEXT_COLOR)
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

# -----------------------
# Database & UDP Helper Functions
# -----------------------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

def send_udp_message(target_ip, message, port=UDP_PORT):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if target_ip == "255.255.255.255":
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.sendto(str(message).encode(), (target_ip, port))
        client_socket.close()
        print(f"Sent message '{message}' to {target_ip}:{port}")
    except Exception as e:
        print("UDP send error:", e)

def update_player_codename(player_id, new_codename):
    conn = get_db_connection()
    if conn is None:
        return False
    cur = conn.cursor()
    try:
        cur.execute("UPDATE players SET codename = %s WHERE id = %s", (new_codename, player_id))
        conn.commit()
        print(f"Player {player_id} codename updated to {new_codename}")
        return True
    except Exception as e:
        print("DB update error:", e)
        return False
    finally:
        cur.close()
        conn.close()

# -----------------------
# Global Variables & State Management
# -----------------------
# States: "splash", "check", "add_new", "found", "equipment"
state = "splash"
splash_start_time = pygame.time.get_ticks()

player_id = ""
player_codename = ""
info_text = "Enter Player ID and press 'Check'"

# Create input boxes
player_id_box = InputBox(50, 60, 200, 32)
new_codename_box = InputBox(50, 110, 200, 32)
update_codename_box = InputBox(50, 110, 200, 32)
equipment_box = InputBox(50, 110, 200, 32)
udp_ip_box = InputBox(50, 170, 200, 32, text=DEFAULT_UDP_IP)

# Button callbacks
def check_player():
    global state, player_codename, player_id, info_text
    pid = player_id_box.text.strip()
    if not pid.isdigit():
        info_text = "Player ID must be an integer."
        return
    player_id = pid
    conn = get_db_connection()
    if conn is None:
        info_text = "DB connection error."
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
        result = cur.fetchone()
        if result:
            player_codename = result[0]
            info_text = f"Player found: Codename - {player_codename}. Update codename or proceed."
            state = "found"
        else:
            info_text = "Player not found. Enter new codename and press 'Add Player'."
            state = "add_new"
    except Exception as e:
        info_text = f"DB error: {e}"
    finally:
        cur.close()
        conn.close()

def add_new_player():
    global state, player_codename, info_text
    new_name = new_codename_box.text.strip()
    if new_name == "":
        info_text = "Codename cannot be empty."
        return
    conn = get_db_connection()
    if conn is None:
        info_text = "DB connection error."
        return
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO players (id, codename) VALUES (%s, %s)", (player_id, new_name))
        conn.commit()
        player_codename = new_name
        equipment_box.text = ""
        equipment_box.txt_surface = FONT.render("", True, TEXT_COLOR)
        info_text = f"Player added: Codename - {player_codename}. Proceed to enter Equipment ID."
        state = "equipment"
    except Exception as e:
        info_text = f"DB insert error: {e}"
    finally:
        cur.close()
        conn.close()

def update_codename():
    global state, player_codename, info_text
    new_name = update_codename_box.text.strip()
    if new_name == "":
        info_text = "New codename cannot be empty."
        return
    if update_player_codename(player_id, new_name):
        player_codename = new_name
        update_codename_box.text = ""
        update_codename_box.txt_surface = FONT.render("", True, TEXT_COLOR)
        equipment_box.text = ""
        equipment_box.txt_surface = FONT.render("", True, TEXT_COLOR)
        info_text = f"Codename updated to {player_codename}. Proceed to enter Equipment ID."
        state = "equipment"
    else:
        info_text = "Failed to update codename."

def proceed_without_update():
    global state, info_text
    info_text = f"Proceeding with codename: {player_codename}. Enter Equipment ID."
    state = "equipment"

def submit_equipment():
    global state, info_text
    equipment = equipment_box.text.strip()
    if not equipment.isdigit():
        info_text = "Equipment ID must be an integer."
        return
    udp_ip = udp_ip_box.text.strip()
    send_udp_message(udp_ip, equipment)
    info_text = f"Equipment ID {equipment} broadcasted to {udp_ip}:{UDP_PORT}."
    state = "check"
    player_id_box.text = ""
    player_id_box.txt_surface = FONT.render("", True, TEXT_COLOR)
    new_codename_box.text = ""
    new_codename_box.txt_surface = FONT.render("", True, TEXT_COLOR)
    update_codename_box.text = ""
    update_codename_box.txt_surface = FONT.render("", True, TEXT_COLOR)
    equipment_box.text = ""
    equipment_box.txt_surface = FONT.render("", True, TEXT_COLOR)

# Create button instances
check_button = Button(300, 60, 100, 32, "Check", check_player)
add_button = Button(300, 110, 100, 32, "Add Player", add_new_player)
update_button = Button(300, 110, 100, 32, "Update", update_codename)
proceed_button = Button(300, 150, 100, 32, "Proceed", proceed_without_update)
submit_button = Button(300, 170, 100, 32, "Submit", submit_equipment)

# -----------------------
# Main Event Loop
# -----------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Process events only if not in splash state.
        if state != "splash":
            player_id_box.handle_event(event)
            new_codename_box.handle_event(event)
            update_codename_box.handle_event(event)
            equipment_box.handle_event(event)
            udp_ip_box.handle_event(event)
            if state == "check":
                check_button.handle_event(event)
            elif state == "add_new":
                add_button.handle_event(event)
            elif state == "found":
                update_button.handle_event(event)
                proceed_button.handle_event(event)
            elif state == "equipment":
                submit_button.handle_event(event)

    if state != "splash":
        player_id_box.update()
        new_codename_box.update()
        update_codename_box.update()
        equipment_box.update()
        udp_ip_box.update()

    screen.fill(BG_COLOR)

    if state == "splash":
        if splash_image:
            screen.blit(splash_image, (0, 0))
        if pygame.time.get_ticks() - splash_start_time > 3000:
            state = "check"
    elif state == "check":
        label = FONT.render("Enter Player ID:", True, TEXT_COLOR)
        screen.blit(label, (50, 20))
        player_id_box.draw(screen)
        check_button.draw(screen)
    elif state == "add_new":
        label1 = FONT.render("Player ID: " + player_id_box.text, True, TEXT_COLOR)
        screen.blit(label1, (50, 20))
        label2 = FONT.render("Enter new Codename:", True, TEXT_COLOR)
        screen.blit(label2, (50, 80))
        new_codename_box.draw(screen)
        add_button.draw(screen)
    elif state == "found":
        label1 = FONT.render("Player ID: " + player_id_box.text, True, TEXT_COLOR)
        screen.blit(label1, (50, 20))
        label2 = FONT.render("Current Codename: " + player_codename, True, TEXT_COLOR)
        screen.blit(label2, (50, 50))
        label3 = FONT.render("Update Codename (optional):", True, TEXT_COLOR)
        screen.blit(label3, (50, 80))
        update_codename_box.draw(screen)
        update_button.draw(screen)
        proceed_button.draw(screen)
    elif state == "equipment":
        label1 = FONT.render(f"Player ID: {player_id_box.text}  Codename: {player_codename}", True, TEXT_COLOR)
        screen.blit(label1, (50, 20))
        label2 = FONT.render("Enter Equipment ID:", True, TEXT_COLOR)
        screen.blit(label2, (50, 60))
        equipment_box.rect.topleft = (50, 90)
        equipment_box.draw(screen)
        label3 = FONT.render("UDP Target IP:", True, TEXT_COLOR)
        screen.blit(label3, (50, 140))
        udp_ip_box.rect.topleft = (50, 170)
        udp_ip_box.draw(screen)
        submit_button.rect.topleft = (300, 170)
        submit_button.draw(screen)
    if state != "splash":
        info_surface = FONT.render(info_text, True, INFO_COLOR)
        screen.blit(info_surface, (50, 260))

    pygame.display.flip()
    CLOCK.tick(30)

pygame.quit()
