import pygame, sys, random, json, os

# INITIAL SETUP
pygame.init()
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tempo Takedown")
CLOCK = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 48)
SMALL_FONT = pygame.font.SysFont("arial", 22)
HEADER_FONT = pygame.font.SysFont("arial", 36, bold=True)

# CONSTANTS
# Single player lanes - centered
LANE_X_P1_SOLO = [450, 550, 650, 750]  # Centered for solo play
# Multiplayer lanes - closer together to make room for side stats
LANE_X_P1 = [250, 325, 400, 475]  # Left side for P1 (moved right)
LANE_X_P2 = [725, 800, 875, 950]  # Right side for P2 (moved left)
HIT_ZONE_Y = HEIGHT - 100  # Moved up to accommodate triangles
NOTE_SPEED_EASY = 3
NOTE_SPEED_MEDIUM = 4.5
NOTE_SPEED_HARD = 6
SPAWN_RATE_EASY = 1000  # ms
SPAWN_RATE_MEDIUM = 800
SPAWN_RATE_HARD = 600
GAME_DURATION = 90000  # 90 seconds in ms
USER_FILE = "users.json"

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
CYAN = (0, 255, 255)

# Long note settings
LONG_NOTE_MIN_LENGTH = 200  # pixels
LONG_NOTE_MAX_LENGTH = 400  # pixels
LONG_NOTE_CHANCE_EASY = 0.15  # 15% chance on easy
LONG_NOTE_CHANCE_MEDIUM = 0.25  # 25% chance on medium
LONG_NOTE_CHANCE_HARD = 0.30  # 30% chance on hard

# GLOBAL STATE
current_user = None
score_p1 = 0
combo_p1 = 0
max_combo_p1 = 0
health_p1 = 5
notes_p1 = []
perfect_p1 = 0
good_p1 = 0
miss_p1 = 0
hit_feedback_p1 = {"text": "", "timer": 0, "color": WHITE}
score_p2 = 0
combo_p2 = 0
max_combo_p2 = 0
health_p2 = 5
notes_p2 = []
perfect_p2 = 0
good_p2 = 0
miss_p2 = 0
hit_feedback_p2 = {"text": "", "timer": 0, "color": WHITE}
paused = False
KEYS_P1 = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
KEYS_P2 = [pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON]

# Combo multiplier thresholds
def get_combo_multiplier(combo):
    if combo >= 50:
        return 2.5
    elif combo >= 30:
        return 2.0
    elif combo >= 20:
        return 1.5
    elif combo >= 10:
        return 1.2
    else:
        return 1.0

# USER DATA
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# UTILITY
def draw_center(text, font, color, y, x_offset=0):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2 + x_offset, y))
    SCREEN.blit(surf, rect)

def draw_left(text, font, color, x, y):
    surf = font.render(text, True, color)
    SCREEN.blit(surf, (x, y))

def draw_right(text, font, color, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(topright=(x, y))
    SCREEN.blit(surf, rect)

def draw_at_x(text, font, color, cx, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(centerx=cx, top=y)
    SCREEN.blit(surf, rect)

def draw_triangle_hit_zone(x, y, size=30, color=GRAY):
    """Draw an upward-pointing triangle for the hit zone"""
    points = [
        (x, y - size),  # Top point
        (x - size, y + size),  # Bottom left
        (x + size, y + size)   # Bottom right
    ]
    pygame.draw.polygon(SCREEN, color, points)
    pygame.draw.polygon(SCREEN, WHITE, points, 2)  # White outline

def reset_game():
    global score_p1, combo_p1, max_combo_p1, health_p1, notes_p1, perfect_p1, good_p1, miss_p1, hit_feedback_p1
    global score_p2, combo_p2, max_combo_p2, health_p2, notes_p2, perfect_p2, good_p2, miss_p2, hit_feedback_p2
    score_p1 = combo_p1 = max_combo_p1 = 0
    score_p2 = combo_p2 = max_combo_p2 = 0
    health_p1 = health_p2 = 5
    notes_p1.clear()
    notes_p2.clear()
    perfect_p1 = good_p1 = miss_p1 = 0
    perfect_p2 = good_p2 = miss_p2 = 0
    hit_feedback_p1 = {"text": "", "timer": 0, "color": WHITE}
    hit_feedback_p2 = {"text": "", "timer": 0, "color": WHITE}

def draw_text_box(text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < rect.width - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_offset = 0
    for line in lines:
        text_surface = font.render(line, True, color)
        SCREEN.blit(text_surface, (rect.x + 10, rect.y + 10 + y_offset))
        y_offset += font.get_height() + 5

# LOGIN / SIGNUP
def login_screen():
    global current_user
    username = password = ""
    active = "user"
    error = ""

    while True:
        SCREEN.fill(BLACK)
        draw_center("LOGIN / SIGN UP", BIG_FONT, WHITE, 120)
        draw_center(f"Username: {username}", FONT, ORANGE if active=="user" else WHITE, 220)
        draw_center(f"Password: {'*'*len(password)}", FONT, ORANGE if active=="pass" else WHITE, 260)
        draw_center(error, SMALL_FONT, RED, 310)
        draw_center("TAB switch | ENTER confirm", SMALL_FONT, GRAY, 350)
        draw_center("Exit", FONT, WHITE, 450)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_TAB:
                    active="pass" if active=="user" else "user"
                elif e.key==pygame.K_BACKSPACE:
                    if active=="user": username=username[:-1]
                    else: password=password[:-1]
                elif e.key==pygame.K_RETURN:
                    users = load_users()
                    if not username or not password:
                        error="Fill all fields"
                    elif len(password) < 8:
                        error="Password must be at least 8 characters"
                    elif not any(c.isdigit() for c in password):
                        error="Password must contain at least one number"
                    elif not any(c.isalpha() for c in password):
                        error="Password must contain at least one letter"
                    elif username in users:
                        if users[username]["password"]==password:
                            # Migration: add completed_game field if it doesn't exist
                            if "completed_game" not in users[username]:
                                users[username]["completed_game"] = False
                                save_users(users)
                            current_user=username
                            return
                        else:
                            error="Wrong password"
                    else:
                        users[username]={"password":password,"best_easy":0,"best_medium":0,"best_hard":0,"unlocked_medium":False,"unlocked_hard":False,"completed_game":False}
                        save_users(users)
                        current_user=username
                        return
                else:
                    if active=="user": username+=e.unicode
                    else: password+=e.unicode
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                 mx, my = e.pos
                 if 430 < my < 470:
                    exit_screen()

# MAIN MENU
def main_menu():
    while True:
        SCREEN.fill(BLACK)
        draw_center("TEMPO TAKEDOWN", BIG_FONT, WHITE, 100)
        draw_center(f"User: {current_user}", SMALL_FONT, WHITE, 150)

        # Get the current mouse position each frame for hover detection
        mx, my = pygame.mouse.get_pos()
        options=["Play","How to Play","Settings","Leaderboard","Sign Out","Exit"]
        for i,o in enumerate(options):
            # If the mouse is hovering over a button, draw it in orange, otherwise white
            button_y = 230+i*45
            if 210+i*45 < my < 250+i*45:
                draw_center(o, FONT, ORANGE, button_y)
            else:
                draw_center(o, FONT, WHITE, button_y)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i, o in enumerate(options):
                    # Check if the click y position falls within each button's boundary
                    if 210+i*45 < my < 250+i*45:
                        if o=="Play": game_mode_menu()
                        elif o=="How to Play": how_to_play()
                        elif o=="Settings": keybind_menu()
                        elif o=="Leaderboard": leaderboard()
                        # Sign out returns the player to the login screen
                        elif o=="Sign Out":
                             login_screen()
                        elif o=="Exit": exit_screen()

# HOW TO PLAY
def how_to_play():
    while True:
        SCREEN.fill(BLACK)
        draw_center("HOW TO PLAY", BIG_FONT, WHITE, 60)
        #Stored all instructions in a list
        instructions = [
            "Hit notes when they reach the green line at the bottom",
            "",
            "REGULAR NOTES (Yellow circles):",
            "Press the key when the note reaches the line",
            "",
            "LONG NOTES (Purple rectangles):",
            "Hold the key down until the entire note passes",
            "",
            "SCORING:",
            "Splendid hit (very close): 200 points",
            "Wow hit (close enough): 100 points",
            "Close hit (just made it) : 50 points",
            "Long notes: bonus points while holding",
            "",
            "Keep your combo high for max score!",
            "Lose health by missing notes or bad timing",
            "Game ends when health reaches 0 or time runs out"
        ]
        #Y resets so all the lines arnt drawn on top of eachother
        y = 130
        for line in instructions:
            if line == "":
                y += 15
            elif line.isupper() or line.endswith(":"):
                # Draw section headings in orange to make them stand out
                draw_center(line, SMALL_FONT, ORANGE, y)
                y += 25
            else:
                # Draw regular instruction text in white
                draw_center(line, SMALL_FONT, WHITE, y)
                y += 25
        
        draw_center("ESC to return", SMALL_FONT, GRAY, HEIGHT - 40)
        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# STORY INTRODUCTION
def story_intro(multiplayer):
    while True:
        SCREEN.fill(BLACK)
        draw_center("ANCIENT EGYPT - THE PYRAMID", BIG_FONT, ORANGE, 80)
        
        if multiplayer:
            story = [
                "You and your companion are brave travelers",
                "exploring the ancient pyramids of Egypt.",
                "",
                "Deep within the tomb lies a legendary artifact,",
                "said to grant immense power to those worthy.",
                "",
                "But the path is guarded by ancient protectors.",
                "You must prove your worth through rhythm and skill.",
                "",
                "Work together to overcome the challenges ahead!",
            ]
        else:
            story = [
                "You are a lone traveler exploring the",
                "ancient pyramids of Egypt.",
                "",
                "Deep within the tomb lies a legendary artifact,",
                "said to grant immense power to those worthy.",
                "",
                "But the path is guarded by ancient protectors.",
                "You must prove your worth through rhythm and skill.",
                "",
                "Can you reach the artifact and escape alive?",
            ]
        
        y = 180
        for line in story:
            if line == "":
                y += 15
            else:
                draw_center(line, SMALL_FONT, WHITE, y)
                y += 30
        
        draw_center("Press ENTER to continue", SMALL_FONT, GRAY, HEIGHT - 50)
        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# LEVEL STORY SCREEN
def level_story(level, multiplayer):
    while True:
        SCREEN.fill(BLACK)
        
        if level == "easy":
            draw_center("THE OUTER CHAMBER", BIG_FONT, ORANGE, 80)
            if multiplayer:
                story = [
                    "You and your companion enter the pyramid.",
                    "A guard blocks your path to the next chamber.",
                    "",
                    "GUARD: 'Halt! Prove your worth or be turned away!'",
                    "",
                    "Beat this challenge together to earn the Bronze Key.",
                    "Score Threshold: 6,700 points"
                ]
            else:
                story = [
                    "You enter the pyramid's outer chamber.",
                    "A guard stands before the next passage.",
                    "",
                    "GUARD: 'Halt! Prove your worth or be turned away!'",
                    "",
                    "Beat this challenge to earn the Bronze Key.",
                    "Score Threshold: 6,700 points"
                ]
        elif level == "medium":
            draw_center("THE INNER SANCTUM", BIG_FONT, ORANGE, 80)
            if multiplayer:
                story = [
                    "You've proven yourselves worthy.",
                    "The guard steps aside, revealing a deeper chamber.",
                    "",
                    "A stronger guardian awaits within.",
                    "",
                    "GUARDIAN: 'Few make it this far. Show me your skill!'",
                    "",
                    "Beat this challenge together to earn the Silver Key.",
                    "Score Threshold: 10,000 points"
                ]
            else:
                story = [
                    "You've proven yourself worthy.",
                    "The guard steps aside, revealing a deeper chamber.",
                    "",
                    "A stronger guardian awaits within.",
                    "",
                    "GUARDIAN: 'Few make it this far. Show me your skill!'",
                    "",
                    "Beat this challenge to earn the Silver Key.",
                    "Score Threshold: 10,000 points"
                ]
        else:  # hard
            draw_center("THE PHARAOH'S TOMB", BIG_FONT, ORANGE, 80)
            if multiplayer:
                story = [
                    "You reach the deepest chamber of the pyramid.",
                    "There, on a golden throne, sits Cleopatra herself!",
                    "",
                    "CLEOPATRA: 'Impressive. But I am the final test.",
                    "Defeat me in this ultimate challenge, and the",
                    "artifact is yours. Fail, and you'll join the mummies!'",
                    "",
                    "This is it - the final challenge!",
                    "Score Threshold: 15,000 points"
                ]
            else:
                story = [
                    "You reach the deepest chamber of the pyramid.",
                    "There, on a golden throne, sits Cleopatra herself!",
                    "",
                    "CLEOPATRA: 'Impressive. But I am the final test.",
                    "Defeat me in this ultimate challenge, and the",
                    "artifact is yours. Fail, and you'll join the mummies!'",
                    "",
                    "This is it - the final challenge!",
                    "Score Threshold: 15,000 points"
                ]
        
        y = 180
        for line in story:
            if line == '':
                y += 15  # standardised from 10 to match story_intro()
            else:
                draw_center(line, SMALL_FONT, WHITE, y)
                y += 30

 
        draw_center('Press ENTER to begin', SMALL_FONT, GREEN, HEIGHT - 50)
        pygame.display.flip()
        CLOCK.tick(FPS)
 
        for e in pygame.event.get():
            # K_RETURN targets the main keyboard Enter key
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()



# GAME MODE MENU
def game_mode_menu():
    while True:
        SCREEN.fill(BLACK)
        draw_center("SELECT GAME MODE", BIG_FONT, WHITE, 100)

        mx, my = pygame.mouse.get_pos()
        options = ["Single Player", "Multiplayer", "Back"]

        for i, o in enumerate(options):
            button_y = 250 + i * 50
            if 230 + i * 50 < my < 270 + i * 50:
                draw_center(o, FONT, ORANGE, button_y)
            else:
                draw_center(o, FONT, WHITE, button_y)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i, o in enumerate(options):
                    if 230 + i * 50 < my < 270 + i * 50:
                        if o == "Single Player":
                            story_intro(False)
                            level_menu(False)
                        elif o == "Multiplayer":
                            story_intro(True)
                            level_menu(True)
                        elif o == "Back":
                            return
# LEVEL MENU
def level_menu(multiplayer):
    users = load_users()  # Load saved user data
    user_data = users.get(current_user, {})  # Get current user's progress
    unlocked_medium = user_data.get("unlocked_medium", False)
    unlocked_hard = user_data.get("unlocked_hard", False)

    while True:
        SCREEN.fill(BLACK)
        draw_center("SELECT CHALLENGE", BIG_FONT, WHITE, 100)

        levels = ["Easy", "Medium", "Hard"]
        level_names = ["Bronze Key Challenge", "Silver Key Challenge", "Golden Artifact Challenge"]
        mx, my = pygame.mouse.get_pos()  # Get current mouse position

        # Draw level options
        for i, level in enumerate(levels):
            y = 230 + i * 70
            color = WHITE
            icon = ""
            if level == "Medium" and not unlocked_medium:  # Locked Medium
                color = GRAY
                icon = " (Locked)"
            elif level == "Hard" and not unlocked_hard:  # Locked Hard
                color = GRAY
                icon = " (Locked)"
            else:
                if 210 + i * 70 < my < 280 + i * 70:  # Hover effect
                    color = ORANGE
            draw_center(f"{level_names[i]}{icon}", FONT, color, y)
            draw_center(f"({level})", SMALL_FONT, color, y + 25)

        # Notes at bottom
        note = "Complete challenges to unlock the next area."
        draw_center(note, SMALL_FONT, GRAY, HEIGHT - 100)
        draw_center("ESC to back", SMALL_FONT, GRAY, HEIGHT - 50)

        pygame.display.flip()
        CLOCK.tick(FPS)

        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:  # Back to previous menu
                return
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # Left-click
                mx, my = e.pos
                for i, level in enumerate(levels):
                    if 210 + i * 70 < my < 280 + i * 70:  # Clicked within level bounds
                        # Easy level (always unlocked)
                        if level == "Easy":
                            while True:  # Retry loop
                                level_story("easy", multiplayer)  # Show story cutscene/dialogue
                                result = game_loop(multiplayer, "easy")  # Play the level
                                if result == "menu":
                                    break  # Back to level select
                                elif result == "continue":
                                    break  # Level passed
                                # If result == "retry", loop continues automatically
                            # Reload progress after finishing
                            users = load_users()
                            user_data = users.get(current_user, {})
                            unlocked_medium = user_data.get("unlocked_medium", False)
                            unlocked_hard = user_data.get("unlocked_hard", False)

                        # Medium level (check if unlocked)
                        elif level == "Medium" and unlocked_medium:
                            while True:
                                level_story("medium", multiplayer)
                                result = game_loop(multiplayer, "medium")
                                if result in ["menu", "continue"]:
                                    break
                            users = load_users()
                            user_data = users.get(current_user, {})
                            unlocked_medium = user_data.get("unlocked_medium", False)
                            unlocked_hard = user_data.get("unlocked_hard", False)

                        # Hard level (check if unlocked)
                        elif level == "Hard" and unlocked_hard:
                            while True:
                                level_story("hard", multiplayer)
                                result = game_loop(multiplayer, "hard")
                                if result in ["menu", "continue"]:
                                    break
                            users = load_users()
                            user_data = users.get(current_user, {})
                            unlocked_medium = user_data.get("unlocked_medium", False)
                            unlocked_hard = user_data.get("unlocked_hard", False)

# KEY BINDINGS
def keybind_menu():
    global KEYS_P1, KEYS_P2
    rebinding = None
    keybind_error = ""

    COL_P1_X = WIDTH // 4
    COL_P2_X = (WIDTH * 3) // 4
    START_Y = 220
    ROW_HEIGHT = 50

    while True:
        SCREEN.fill(BLACK)
        draw_center("Settings", BIG_FONT, WHITE, 80)

        # P1 column (left)
        draw_at_x("Player 1", HEADER_FONT, ORANGE, COL_P1_X, 160)
        for i, k in enumerate(KEYS_P1):
            color = ORANGE if rebinding == ("P1", i) else WHITE
            draw_at_x(f"Lane {i+1}: {pygame.key.name(k)}", FONT, color, COL_P1_X, START_Y + i * ROW_HEIGHT)

        # P2 column (right)
        draw_at_x("Player 2", HEADER_FONT, ORANGE, COL_P2_X, 160)
        for i, k in enumerate(KEYS_P2):
            color = ORANGE if rebinding == ("P2", i) else WHITE
            draw_at_x(f"Lane {i+1}: {pygame.key.name(k)}", FONT, color, COL_P2_X, START_Y + i * ROW_HEIGHT)

        if keybind_error:
            draw_center(keybind_error, SMALL_FONT, RED, HEIGHT - 110)
        if rebinding:
            draw_center("Press a key to rebind...", SMALL_FONT, YELLOW, HEIGHT - 80)
        draw_center("Click line to rebind | ESC back", SMALL_FONT, GRAY, HEIGHT - 50)
        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if rebinding:
                        rebinding = None
                    else:
                        return
                elif rebinding:
                    p, i = rebinding
                    all_keys = KEYS_P1 + KEYS_P2
                    if e.key in all_keys:
                        keybind_error = f"'{pygame.key.name(e.key)}' is already in use!"
                    else:
                        if p == "P1":
                            KEYS_P1[i] = e.key
                        else:
                            KEYS_P2[i] = e.key
                        keybind_error = ""
                        rebinding = None
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                keybind_error = ""
                for i in range(4):
                    y_top = START_Y + i * ROW_HEIGHT - 15
                    y_bot = START_Y + i * ROW_HEIGHT + 25
                    if y_top < my < y_bot and mx < WIDTH // 2:
                        rebinding = ("P1", i)
                    if y_top < my < y_bot and mx >= WIDTH // 2:
                        rebinding = ("P2", i)
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# LEADERBOARD
def leaderboard():
    selected_level = "easy"
    
    while True:
        SCREEN.fill(BLACK)
        draw_center("LEADERBOARD", BIG_FONT, WHITE, 80)
        
        # Draw level selection buttons
        levels = ["easy", "medium", "hard"]
        mx, my = pygame.mouse.get_pos() 
        for i, level in enumerate(levels):
            color = ORANGE if level == selected_level else WHITE
            draw_center(level.capitalize(), FONT, color, 150 + i * 50)
        
        # Get users and rank them by selected level
        users = load_users()
        level_key = f"best_{selected_level}"
        ranked = sorted(users.items(), key=lambda x: x[1].get(level_key, 0), reverse=True)
        
        # Filter out users with 0 score
        ranked = [(u, d) for u, d in ranked if d.get(level_key, 0) > 0]
        
        # Display top 10
        if ranked:
            for i, (u, d) in enumerate(ranked[:10]):
                score = d.get(level_key, 0)
                draw_center(f"{i+1}. {u} - {score}", SMALL_FONT, WHITE, 320 + i * 30)
        else:
            draw_center("N/A", FONT, GRAY, 400)
        
        draw_center("Click difficulty to switch | ESC to return", SMALL_FONT, GRAY, HEIGHT - 40)
        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: 
                return
            if e.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i, level in enumerate(levels):
                    if 130 + i * 50 < my < 170 + i * 50:
                        selected_level = level

# PAUSE MENU
def pause_menu():
    global paused
    while paused:
        draw_center("PAUSED", BIG_FONT, WHITE, 200)

        mx, my = pygame.mouse.get_pos()
        options = ["Resume", "Return to Menu"]

        for i, o in enumerate(options):
            if 280 + i * 50 < my < 320 + i * 50:
                draw_center(o, FONT, ORANGE, 300 + i * 50)
            else:
                draw_center(o, FONT, WHITE, 300 + i * 50)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i, o in enumerate(options):
                    if 280 + i * 50 < my < 320 + i * 50:
                        if o == "Resume":
                            paused = False
                        elif o == "Return to Menu":
                            paused = False
                            return True
    return False

# CONGRATULATIONS SCREEN (shown once after beating hard for the first time)
def congratulations_screen():
    while True:
        SCREEN.fill(WHITE)
        
        # Draw congratulations message
        draw_center("Congratulations!", BIG_FONT, BLACK, 100)
        
        # Story text
        story_lines = [
            "You have conquered all challenges and retrieved the ancient artifact!",
            "The secrets of the pharaohs are now yours to protect.",
            "You are a true master of rhythm and timing.",
            "",
            "Thank you for playing Tempo Takedown!"
        ]
        
        y_pos = 180
        for line in story_lines:
            draw_center(line, SMALL_FONT, BLACK, y_pos)
            y_pos += 35
        
        # Draw buttons
        draw_center("Retry", FONT, BLACK, HEIGHT - 120)
        draw_center("Return to menu", FONT, BLACK, HEIGHT - 70)
        
        pygame.display.flip()
        CLOCK.tick(FPS)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return  # Return to results screen
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if HEIGHT - 140 < my < HEIGHT - 100:  # Retry button
                    return  # Will continue to results screen which handles retry
                if HEIGHT - 90 < my < HEIGHT - 50:  # Return to menu button
                    return

# RESULTS SCREEN
def results_screen(multiplayer, level, won):
    global score_p1, max_combo_p1, perfect_p1, good_p1, miss_p1
    global score_p2, max_combo_p2, perfect_p2, good_p2, miss_p2

    # Determine score threshold for the level
    thresholds = {"easy": 6700, "medium": 10000, "hard":15000 }
    threshold = thresholds[level]
    
    # Check if threshold was met
    if multiplayer:
        total_score = score_p1 + score_p2
        threshold_met = total_score >= threshold
    else:
        threshold_met = score_p1 >= threshold
    
    # Determine if players passed (won AND met threshold)
    passed = won and threshold_met

    # Update user stats
    users = load_users()
    if current_user in users:
        level_key = f"best_{level}"
        if score_p1 > users[current_user].get(level_key, 0):
            users[current_user][level_key] = score_p1
        
        # Unlock next level only if passed
        if passed:
            if level == "easy":
                users[current_user]["unlocked_medium"] = True
            elif level == "medium":
                users[current_user]["unlocked_hard"] = True
            elif level == "hard":
                # Check if this is the first time completing hard mode
                if not users[current_user].get("completed_game", False):
                    users[current_user]["completed_game"] = True
                    save_users(users)
                    # Show congratulations screen
                    congratulations_screen()
        
        save_users(users)

    # Story outcome
    while True:
        SCREEN.fill(BLACK)
        
        # Show story outcome first
        if passed:
            if level == "easy":
                draw_center("VICTORY!", BIG_FONT, GREEN, 60)
                draw_center("The guard nods in respect and hands you the Bronze Key.", SMALL_FONT, WHITE, 110)
                draw_center("'You have proven yourself worthy. Proceed.'", SMALL_FONT, ORANGE, 140)
            elif level == "medium":
                draw_center("VICTORY!", BIG_FONT, GREEN, 60)
                draw_center("The guardian bows and presents you with the Silver Key.", SMALL_FONT, WHITE, 110)
                draw_center("'Impressive. The path to Cleopatra awaits you.'", SMALL_FONT, ORANGE, 140)
            else:  # hard
                draw_center("THE ARTIFACT IS YOURS!", BIG_FONT, GREEN, 60)
                draw_center("Cleopatra smiles and begins to fade into mist...", SMALL_FONT, WHITE, 110)
                draw_center("'You are truly worthy. Take the artifact and go.'", SMALL_FONT, ORANGE, 140)
                draw_center("You've completed the ultimate challenge!", SMALL_FONT, YELLOW, 170)
        else:
            draw_center("CAPTURED!", BIG_FONT, RED, 60)
            if not threshold_met:
                if multiplayer:
                    draw_center(f"Combined Score: {score_p1 + score_p2} / {threshold} needed", SMALL_FONT, WHITE, 110)
                else:
                    draw_center(f"Score: {score_p1} / {threshold} needed", SMALL_FONT, WHITE, 110)
                draw_center("You didn't meet the challenge threshold!", SMALL_FONT, RED, 140)
            else:
                draw_center("You ran out of health!", SMALL_FONT, RED, 110)
            
            draw_center("The guards capture you and throw you in the dungeon.", SMALL_FONT, WHITE, 180)
            draw_center("Try again to escape!", SMALL_FONT, ORANGE, 210)

        # Stats section
        y_start = 260
        draw_center("--- STATS ---", SMALL_FONT, GRAY, y_start)
        
        # P1 Stats
        draw_left("Player 1", SMALL_FONT, WHITE, 100, y_start + 40)
        draw_left(f"Score: {score_p1}", SMALL_FONT, WHITE, 100, y_start + 70)
        draw_left(f"Max Combo: {max_combo_p1}", SMALL_FONT, WHITE, 100, y_start + 95)
        draw_left(f"Splendid: {perfect_p1}", SMALL_FONT, WHITE, 100, y_start + 120)
        draw_left(f"Wow: {good_p1}", SMALL_FONT, WHITE, 100, y_start + 145)
        draw_left(f"Miss: {miss_p1}", SMALL_FONT, WHITE, 100, y_start + 170)

        if multiplayer:
            # P2 Stats
            draw_right("Player 2", SMALL_FONT, WHITE, WIDTH - 100, y_start + 40)
            draw_right(f"Score: {score_p2}", SMALL_FONT, WHITE, WIDTH - 100, y_start + 70)
            draw_right(f"Max Combo: {max_combo_p2}", SMALL_FONT, WHITE, WIDTH - 100, y_start + 95)
            draw_right(f"Splendid: {perfect_p2}", SMALL_FONT, WHITE, WIDTH - 100, y_start + 120)
            draw_right(f"Wow: {good_p2}", SMALL_FONT, WHITE, WIDTH - 100, y_start + 145)
            draw_right(f"Miss: {miss_p2}", SMALL_FONT, WHITE, WIDTH - 100, y_start + 170)
            
            draw_center(f"Combined Score: {score_p1 + score_p2}", FONT, YELLOW if passed else RED, y_start + 210)

        # Draw buttons at the bottom
        if passed:
            draw_center("Press ENTER to continue", SMALL_FONT, GRAY, HEIGHT - 40)
        else:
            draw_center("Retry", FONT, WHITE, HEIGHT - 80)
            draw_center("Return to Menu", FONT, WHITE, HEIGHT - 40)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if passed:
                    return "continue"
                # If failed, treat ENTER as retry
                return "retry"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if not passed:  # Only show retry/menu buttons on fail
                    mx, my = e.pos
                    if HEIGHT - 100 < my < HEIGHT - 60:  # Retry button
                        return "retry"
                    if HEIGHT - 60 < my < HEIGHT - 20:  # Return to Menu button
                        return "menu"
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# GAMEPLAY
def spawn_note(notes, lanes, level):
    # Try to find an available lane (one without a recent note)
    available_lanes = []
    for i in range(4):
        lane_x = lanes[i]
        # Check if there's already a note in this lane that's too close
        has_recent_note = any(n["x"] == lane_x and n["y"] < 200 and not n.get("hit", False) for n in notes)
        if not has_recent_note:
            available_lanes.append(i)
    
    # If no lanes available, just pick a random one (fallback)
    if not available_lanes:
        lane = random.randint(0, 3)
    else:
        lane = random.choice(available_lanes)
    
    # Difficulty-based long note chance
    long_chance = {
        "easy": LONG_NOTE_CHANCE_EASY,
        "medium": LONG_NOTE_CHANCE_MEDIUM,
        "hard": LONG_NOTE_CHANCE_HARD
    }[level]
    
    # On easy, prevent spawning long notes if one already exists
    is_long = random.random() < long_chance
    if level == "easy" and is_long:
        # Check if there's already a long note active
        has_long_note = any(n.get("long", False) and not n.get("hit", False) for n in notes)
        if has_long_note:
            is_long = False  # Spawn a regular note instead
    
    if is_long:
        length = random.randint(LONG_NOTE_MIN_LENGTH, LONG_NOTE_MAX_LENGTH)
        notes.append({
            "x": lanes[lane],
            "y": -40,
            "hit": False,
            "long": True,
            "length": length,
            "holding": False,
            "hold_progress": 0
        })
    else:
        notes.append({
            "x": lanes[lane],
            "y": -40,
            "hit": False,
            "long": False
        })

def handle_hit(key, keys, notes, lanes, key_held):
    global score_p1, combo_p1, max_combo_p1, perfect_p1, good_p1, health_p1, hit_feedback_p1
    global score_p2, combo_p2, max_combo_p2, perfect_p2, good_p2, health_p2, hit_feedback_p2
    
    if key not in keys: 
        return False
    
    lane = keys.index(key)
    is_p1 = (keys == KEYS_P1)
    
    # Check if there's a note in this lane to hit
    note_found = False
    for n in notes:
        if not n["hit"] and n["x"] == lanes[lane]:
            note_found = True
            # Long note handling
            if n.get("long", False):
                dist = abs(n["y"] - HIT_ZONE_Y)
                if dist < 40 and key_held:  # Start holding
                    n["holding"] = True
                    if is_p1:
                        hit_feedback_p1 = {"text": "Hold!", "timer": 30, "color": CYAN}
                    else:
                        hit_feedback_p2 = {"text": "Hold!", "timer": 30, "color": CYAN}
                    return True
            else:
                # Regular note handling with combo multiplier
                dist = abs(n["y"] - HIT_ZONE_Y)
                if dist < 10:  # Splendid
                    n["hit"] = True
                    if is_p1:
                        multiplier = get_combo_multiplier(combo_p1)
                        points = int(200 * multiplier)
                        score_p1 += points
                        combo_p1 += 1
                        max_combo_p1 = max(max_combo_p1, combo_p1)
                        perfect_p1 += 1
                        hit_feedback_p1 = {"text": f"Splendid! +{points}", "timer": 30, "color": GREEN}
                    else:
                        multiplier = get_combo_multiplier(combo_p2)
                        points = int(200 * multiplier)
                        score_p2 += points
                        combo_p2 += 1
                        max_combo_p2 = max(max_combo_p2, combo_p2)
                        perfect_p2 += 1
                        hit_feedback_p2 = {"text": f"Splendid! +{points}", "timer": 30, "color": GREEN}
                    return True
                elif dist < 30:  # Wow
                    n["hit"] = True
                    if is_p1:
                        multiplier = get_combo_multiplier(combo_p1)
                        points = int(100 * multiplier)
                        score_p1 += points
                        combo_p1 += 1
                        max_combo_p1 = max(max_combo_p1, combo_p1)
                        good_p1 += 1
                        hit_feedback_p1 = {"text": f"Wow! +{points}", "timer": 30, "color": YELLOW}
                    else:
                        multiplier = get_combo_multiplier(combo_p2)
                        points = int(100 * multiplier)
                        score_p2 += points
                        combo_p2 += 1
                        max_combo_p2 = max(max_combo_p2, combo_p2)
                        good_p2 += 1
                        hit_feedback_p2 = {"text": f"Wow! +{points}", "timer": 30, "color": YELLOW}
                    return True
                elif dist < 40:  # Close
                    n["hit"] = True
                    if is_p1:
                        multiplier = get_combo_multiplier(combo_p1)
                        points = int(50 * multiplier)
                        score_p1 += points
                        combo_p1 += 1
                        max_combo_p1 = max(max_combo_p1, combo_p1)
                        good_p1 += 1
                        hit_feedback_p1 = {"text": f"Close! +{points}", "timer": 30, "color": ORANGE}
                    else:
                        multiplier = get_combo_multiplier(combo_p2)
                        points = int(50 * multiplier)
                        score_p2 += points
                        combo_p2 += 1
                        max_combo_p2 = max(max_combo_p2, combo_p2)
                        good_p2 += 1
                        hit_feedback_p2 = {"text": f"Close! +{points}", "timer": 30, "color": ORANGE}
                    return True
    
    # Only penalize if there was a note to hit but they missed the timing
    # Don't penalize if no notes exist yet (game just started)
    if note_found:
        # Missed (wrong timing)
        if is_p1:
            combo_p1 = 0
            health_p1 = max(0, health_p1 - 1)  # Prevent negative health
            hit_feedback_p1 = {"text": "Miss :(", "timer": 30, "color": RED}
        else:
            combo_p2 = 0
            health_p2 = max(0, health_p2 - 1)  # Prevent negative health
            hit_feedback_p2 = {"text": "Miss :(", "timer": 30, "color": RED}
    return False

def update_long_notes(notes, keys_held, lanes, is_p1):
    global score_p1, combo_p1, max_combo_p1, perfect_p1, health_p1, hit_feedback_p1
    global score_p2, combo_p2, max_combo_p2, perfect_p2, health_p2, hit_feedback_p2
    
    for n in notes:
        if n.get("long", False) and n.get("holding", False):
            # Find which key should be held
            lane_index = lanes.index(n["x"])
            if is_p1:
                expected_key = KEYS_P1[lane_index]
            else:
                expected_key = KEYS_P2[lane_index]
            
            # Check if the key is still being held
            if keys_held[expected_key]:
                n["hold_progress"] += 1
                # Award points for holding (with combo multiplier)
                if n["hold_progress"] % 3 == 0:  # Every 3 frames
                    if is_p1:
                        multiplier = get_combo_multiplier(combo_p1)
                        score_p1 += int(10 * multiplier)
                    else:
                        multiplier = get_combo_multiplier(combo_p2)
                        score_p2 += int(10 * multiplier)
            else:
                # Released too early
                n["holding"] = False
                if is_p1:
                    combo_p1 = 0
                    hit_feedback_p1 = {"text": "Released early!", "timer": 30, "color": ORANGE}
                else:
                    combo_p2 = 0
                    hit_feedback_p2 = {"text": "Released early!", "timer": 30, "color": ORANGE}

def game_loop(multiplayer, level):
    global paused, score_p1, combo_p1, max_combo_p1, health_p1, notes_p1, perfect_p1, good_p1, miss_p1
    global score_p2, combo_p2, max_combo_p2, health_p2, notes_p2, perfect_p2, good_p2, miss_p2

    reset_game()
    spawn_timer = 0
    game_timer = 0
    note_speed = {"easy": NOTE_SPEED_EASY, "medium": NOTE_SPEED_MEDIUM, "hard": NOTE_SPEED_HARD}[level]
    spawn_rate = {"easy": SPAWN_RATE_EASY, "medium": SPAWN_RATE_MEDIUM, "hard": SPAWN_RATE_HARD}[level]
    
    # Use centered lanes for solo, split lanes for multiplayer
    lanes_p1 = LANE_X_P1_SOLO if not multiplayer else LANE_X_P1
    lanes_p2 = LANE_X_P2 if multiplayer else []
    
    p1_alive = True
    p2_alive = True if multiplayer else False
    
    # Track which keys are currently held
    keys_held = {key: False for key in KEYS_P1 + KEYS_P2}

    while True:
        if paused:
            if pause_menu():
                return "menu"  # Return to menu

        dt = CLOCK.tick(FPS)
        spawn_timer += dt
        game_timer += dt

        # EVENT HANDLING
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_p:
                    paused = True
                else:
                    if e.key in keys_held:
                        keys_held[e.key] = True
                    if p1_alive:
                        handle_hit(e.key, KEYS_P1, notes_p1, lanes_p1, True)
                    if multiplayer and p2_alive:
                        handle_hit(e.key, KEYS_P2, notes_p2, lanes_p2, True)
            if e.type == pygame.KEYUP:
                if e.key in keys_held:
                    keys_held[e.key] = False

        # Update long notes based on held keys
        if p1_alive:
            update_long_notes(notes_p1, keys_held, lanes_p1, True)
        if multiplayer and p2_alive:
            update_long_notes(notes_p2, keys_held, lanes_p2, False)

        # SPAWN NOTES
        if spawn_timer > spawn_rate:
            if p1_alive:
                spawn_note(notes_p1, lanes_p1, level)
            if multiplayer and p2_alive:
                spawn_note(notes_p2, lanes_p2, level)
            spawn_timer = 0

        # UPDATE NOTES
        for n in notes_p1 + notes_p2:
            n["y"] += note_speed

        # CHECK FOR MISSES
        if p1_alive:
            for n in notes_p1[:]:
                if n.get("long", False):
                    # Long note - check if it's passed the hit zone
                    if n["y"] - n.get("length", 0) > HIT_ZONE_Y + 40:
                        if n.get("holding", False):
                            # Successfully held the whole note
                            n["hit"] = True
                            bonus = n["hold_progress"] * 5
                            score_p1 += bonus
                            combo_p1 += 1
                            max_combo_p1 = max(max_combo_p1, combo_p1)
                            perfect_p1 += 1
                            notes_p1.remove(n)
                        elif not n["hit"]:
                            # Missed the long note
                            notes_p1.remove(n)
                            miss_p1 += 1
                            combo_p1 = 0
                            health_p1 -= 1
                            if health_p1 <= 0:
                                p1_alive = False
                else:
                    # Regular note
                    if n["y"] > HIT_ZONE_Y + 40 and not n["hit"]:
                        notes_p1.remove(n)
                        miss_p1 += 1
                        combo_p1 = 0
                        health_p1 -= 1
                        if health_p1 <= 0:
                            p1_alive = False
        
        if multiplayer and p2_alive:
            for n in notes_p2[:]:
                if n.get("long", False):
                    # Long note
                    if n["y"] - n.get("length", 0) > HIT_ZONE_Y + 40:
                        if n.get("holding", False):
                            n["hit"] = True
                            bonus = n["hold_progress"] * 5
                            score_p2 += bonus
                            combo_p2 += 1
                            max_combo_p2 = max(max_combo_p2, combo_p2)
                            perfect_p2 += 1
                            notes_p2.remove(n)
                        elif not n["hit"]:
                            notes_p2.remove(n)
                            miss_p2 += 1
                            combo_p2 = 0
                            health_p2 -= 1
                            if health_p2 <= 0:
                                p2_alive = False
                else:
                    # Regular note
                    if n["y"] > HIT_ZONE_Y + 40 and not n["hit"]:
                        notes_p2.remove(n)
                        miss_p2 += 1
                        combo_p2 = 0
                        health_p2 -= 1
                        if health_p2 <= 0:
                            p2_alive = False

        # CHECK GAME OVER
        thresholds = {"easy": 6700, "medium": 10000, "hard": 15000}    
        
        if not multiplayer:
            # Single player: game ends when P1 dies or time runs out
            if not p1_alive or game_timer >= GAME_DURATION:
                # Win if time ran out OR if threshold was met (even with 0 health)
                won = game_timer >= GAME_DURATION or score_p1 >= thresholds[level]
                result = results_screen(multiplayer, level, won)
                return result
        else:
            # Multiplayer: game ends when BOTH players die or time runs out
            if (not p1_alive and not p2_alive) or game_timer >= GAME_DURATION:
                # Win if time ran out OR if threshold was met (even with 0 health)
                total_score = score_p1 + score_p2
                won = game_timer >= GAME_DURATION or total_score >= thresholds[level]
                result = results_screen(multiplayer, level, won)
                return result

        # RENDERING
        SCREEN.fill(BLACK)

        if not multiplayer:
            # ===== SINGLE PLAYER UI =====
            
            # Draw lanes
            for x in lanes_p1:
                pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HIT_ZONE_Y + 30), 2)
            
            # Draw horizontal hit zone line
            pygame.draw.line(SCREEN, WHITE, (lanes_p1[0] - 50, HIT_ZONE_Y), 
                           (lanes_p1[-1] + 50, HIT_ZONE_Y), 3)
            
            # Draw notes FIRST (so UI appears on top)
            for n in notes_p1:
                if n.get("long", False):
                    color = CYAN if n.get("holding", False) else PURPLE
                    rect_y = int(n["y"] - n["length"])
                    pygame.draw.rect(SCREEN, color, (n["x"] - 15, rect_y, 30, n["length"]))
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
                else:
                    color = YELLOW if not n["hit"] else GREEN
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
            
            # Draw triangular hit zones with key bindings
            for i, x in enumerate(lanes_p1):
                draw_triangle_hit_zone(x, HIT_ZONE_Y + 30, 25, GRAY)
                # Draw key name INSIDE/ON the triangle
                key_text = pygame.key.name(KEYS_P1[i]).upper()
                key_surf = SMALL_FONT.render(key_text, True, WHITE)
                key_rect = key_surf.get_rect(center=(x, HIT_ZONE_Y + 25))
                SCREEN.blit(key_surf, key_rect)
            
            # NOW draw UI elements (so they appear on top of notes)
            
            # Draw Back/Pause button (top left)
            pygame.draw.rect(SCREEN, GRAY, (45, 40, 130, 60), border_radius=10)
            draw_left("Pause", SMALL_FONT, WHITE, 50, 50)
            
            # Draw Total Score (top center)
            total_score = score_p1
            score_box_width = 320
            score_box_x = (WIDTH - score_box_width) // 2
            pygame.draw.rect(SCREEN, GRAY, (score_box_x, 30, score_box_width, 70), border_radius=15)
            draw_center(f"Score: {total_score}", FONT, WHITE, 65)
            
            # Draw side stats boxes (right side)
            stat_boxes = [
                (f"Combo: {combo_p1}", 130),
                (f"Health: {health_p1}", 210),
                (f"Time: {(GAME_DURATION - game_timer) // 1000}s", 290)
            ]
            
            for text, y_pos in stat_boxes:
                pygame.draw.rect(SCREEN, GRAY, (WIDTH - 185, y_pos, 145, 50), border_radius=10)
                draw_right(text, SMALL_FONT, WHITE, WIDTH - 50, y_pos + 15)
            
            # Story/Image placeholder (left side)
            story_rect = pygame.Rect(45, 220, 330, 300)
            pygame.draw.rect(SCREEN, GRAY, story_rect, border_radius=10)
            story_text = "All eyes are on you traveler... we believe in you!"
            draw_text_box(story_text, FONT, BLACK, story_rect)
            
            # Draw hit feedback
            if hit_feedback_p1["timer"] > 0:
                draw_center(hit_feedback_p1["text"], FONT, hit_feedback_p1["color"], HIT_ZONE_Y - 80)
                hit_feedback_p1["timer"] -= 1
                
        else:
            # ===== MULTIPLAYER UI =====
            
            # Draw lanes for P1
            for x in lanes_p1:
                pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HIT_ZONE_Y + 30), 2)
            
            # Draw horizontal hit zone line for P1
            pygame.draw.line(SCREEN, WHITE, (lanes_p1[0] - 50, HIT_ZONE_Y), 
                           (lanes_p1[-1] + 50, HIT_ZONE_Y), 3)
            
            # Draw lanes for P2
            for x in lanes_p2:
                pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HIT_ZONE_Y + 30), 2)
            
            # Draw horizontal hit zone line for P2
            pygame.draw.line(SCREEN, WHITE, (lanes_p2[0] - 50, HIT_ZONE_Y), 
                           (lanes_p2[-1] + 50, HIT_ZONE_Y), 3)
            
            # Draw notes FIRST (so UI appears on top)
            # Draw notes for P1
            for n in notes_p1:
                if n.get("long", False):
                    color = CYAN if n.get("holding", False) else PURPLE
                    rect_y = int(n["y"] - n["length"])
                    pygame.draw.rect(SCREEN, color, (n["x"] - 15, rect_y, 30, n["length"]))
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
                else:
                    color = YELLOW if not n["hit"] else GREEN
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
            
            # Draw notes for P2
            for n in notes_p2:
                if n.get("long", False):
                    color = CYAN if n.get("holding", False) else PURPLE
                    rect_y = int(n["y"] - n["length"])
                    pygame.draw.rect(SCREEN, color, (n["x"] - 15, rect_y, 30, n["length"]))
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
                else:
                    color = YELLOW if not n["hit"] else GREEN
                    pygame.draw.circle(SCREEN, color, (n["x"], int(n["y"])), 20)
            
            # Draw triangular hit zones with key bindings INSIDE triangles
            # P1 triangles
            for i, x in enumerate(lanes_p1):
                draw_triangle_hit_zone(x, HIT_ZONE_Y + 30, 25, GRAY)
                key_text = pygame.key.name(KEYS_P1[i]).upper()
                key_surf = SMALL_FONT.render(key_text, True, WHITE)
                key_rect = key_surf.get_rect(center=(x, HIT_ZONE_Y + 25))
                SCREEN.blit(key_surf, key_rect)
            
            # P2 triangles
            for i, x in enumerate(lanes_p2):
                draw_triangle_hit_zone(x, HIT_ZONE_Y + 30, 25, GRAY)
                key_text = pygame.key.name(KEYS_P2[i]).upper()
                key_surf = SMALL_FONT.render(key_text, True, WHITE)
                key_rect = key_surf.get_rect(center=(x, HIT_ZONE_Y + 25))
                SCREEN.blit(key_surf, key_rect)
            
            # NOW draw UI elements (so they appear on top of notes)
            
            # Draw Back button (top left - NO BOX, just white text)
            draw_left("Back", FONT, WHITE, 50, 50)
            
            # Draw Player 1 Score (top left)
            pygame.draw.rect(SCREEN, GRAY, (200, 50, 240, 60), border_radius=15)
            draw_center(f"P1 Score: {score_p1}", FONT, WHITE, 80, -280)
            
            # Draw Player 2 Score (top right - properly centered)
            p2_score_box_x = WIDTH - 440
            pygame.draw.rect(SCREEN, GRAY, (p2_score_box_x, 50, 240, 60), border_radius=15)
            p2_score_surf = FONT.render(f"P2 Score: {score_p2}", True, WHITE)
            p2_score_rect = p2_score_surf.get_rect(center=(p2_score_box_x + 120, 80))
            SCREEN.blit(p2_score_surf, p2_score_rect)
            
            # Draw P1 stats (left side - with more space)
            draw_left(f"Combo: {combo_p1}", SMALL_FONT, WHITE, 50, 140)
            draw_left(f"Health: {health_p1}", SMALL_FONT, WHITE, 50, 170)
            
            # Draw P2 stats (right side - with more space)
            draw_right(f"Combo: {combo_p2}", SMALL_FONT, WHITE, WIDTH - 50, 140)
            draw_right(f"Health: {health_p2}", SMALL_FONT, WHITE, WIDTH - 50, 170)
            
            # Draw Time in the center (white text)
            draw_center(f"Time: {(GAME_DURATION - game_timer) // 1000}s", FONT, WHITE, 200)
            
            # Draw hit feedback
            if p1_alive and hit_feedback_p1["timer"] > 0:
                draw_center(hit_feedback_p1["text"], FONT, hit_feedback_p1["color"], HIT_ZONE_Y - 80, -250)
                hit_feedback_p1["timer"] -= 1
            
            if p2_alive and hit_feedback_p2["timer"] > 0:
                draw_center(hit_feedback_p2["text"], FONT, hit_feedback_p2["color"], HIT_ZONE_Y - 80, 250)
                hit_feedback_p2["timer"] -= 1

        pygame.display.flip()

# EXIT CONFIRMATION
def exit_screen():
    while True:
        # Clear screen each frame
        SCREEN.fill(BLACK)

        # Display confirmation message and both options
        draw_center("Are you sure you want to exit?", BIG_FONT, WHITE, 250)
        draw_center("Yes", FONT, RED, 350)
        draw_center("Return", FONT, GREEN, 400)

        pygame.display.flip()
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                # Yes closes the game entirely
                if 330 < my < 370:
                    pygame.quit()
                    sys.exit()
                # Return goes back to the main menu
                if 380 < my < 420:
                    return
                    
#MAIN ENTRY POINT
if __name__ == "__main__":
    while True:
        login_screen()
        main_menu()

#yippie!!
