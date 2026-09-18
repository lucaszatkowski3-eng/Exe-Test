import pygame
import random
import sys

# -----------------------------
# Einstellungen
# -----------------------------
WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SIZE = 45
PLAYER_SPEED = 6

ENEMY_SIZE = 40
ENEMY_SPEED_MIN = 3
ENEMY_SPEED_MAX = 7

# -----------------------------
# Pygame starten
# -----------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge - Überlebe so lange du kannst!")

clock = pygame.time.Clock()

# Schriftarten
font_big = pygame.font.Font(None, 70)
font = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 28)

# -----------------------------
# Farben
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 25)
BLUE = (50, 150, 255)
RED = (230, 60, 60)
GREEN = (60, 220, 120)
GRAY = (100, 100, 110)

# -----------------------------
# Spieler
# -----------------------------
player = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,
    HEIGHT - 80,
    PLAYER_SIZE,
    PLAYER_SIZE
)

# -----------------------------
# Gegner
# -----------------------------
enemies = []

spawn_timer = 0
spawn_delay = 700

# -----------------------------
# Spielvariablen
# -----------------------------
score = 0
game_over = False
start_screen = True

start_time = 0


def reset_game():
    global enemies
    global score
    global game_over
    global spawn_timer
    global spawn_delay
    global start_time

    player.x = WIDTH // 2 - PLAYER_SIZE // 2
    player.y = HEIGHT - 80

    enemies = []

    score = 0
    game_over = False
    spawn_timer = 0
    spawn_delay = 700

    start_time = pygame.time.get_ticks()


def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_SIZE)

    enemy = pygame.Rect(
        x,
        -ENEMY_SIZE,
        ENEMY_SIZE,
        ENEMY_SIZE
    )

    speed = random.randint(
        ENEMY_SPEED_MIN,
        ENEMY_SPEED_MAX
    )

    enemies.append({
        "rect": enemy,
        "speed": speed
    })


def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


# -----------------------------
# Spiel zurücksetzen
# -----------------------------
reset_game()

# -----------------------------
# Hauptschleife
# -----------------------------
running = True

while running:

    dt = clock.tick(FPS)

    # -------------------------
    # Events
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Start
            if start_screen:
                if event.key == pygame.K_SPACE:
                    start_screen = False
                    reset_game()

            # Game Over
            elif game_over:
                if event.key == pygame.K_r:
                    reset_game()

                if event.key == pygame.K_ESCAPE:
                    running = False

    # -------------------------
    # Startbildschirm
    # -------------------------
    if start_screen:

        screen.fill(BLACK)

        draw_text(
            "DODGE",
            font_big,
            BLUE,
            WIDTH // 2,
            180
        )

        draw_text(
            "Überlebe so lange wie möglich!",
            font,
            WHITE,
            WIDTH // 2,
            250
        )

        draw_text(
            "WASD oder Pfeiltasten zum Bewegen",
            font_small,
            GRAY,
            WIDTH // 2,
            320
        )

        draw_text(
            "Drücke LEERTASTE zum Starten",
            font,
            GREEN,
            WIDTH // 2,
            400
        )

        pygame.display.flip()
        continue

    # -------------------------
    # Game Over Bildschirm
    # -------------------------
    if game_over:

        screen.fill(BLACK)

        draw_text(
            "GAME OVER",
            font_big,
            RED,
            WIDTH // 2,
            180
        )

        draw_text(
            f"Punkte: {score}",
            font,
            WHITE,
            WIDTH // 2,
            270
        )

        draw_text(
            "R = Neustart",
            font,
            GREEN,
            WIDTH // 2,
            350
        )

        draw_text(
            "ESC = Beenden",
            font_small,
            GRAY,
            WIDTH // 2,
            410
        )

        pygame.display.flip()
        continue

    # -------------------------
    # Tastatur
    # -------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= PLAYER_SPEED

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += PLAYER_SPEED

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= PLAYER_SPEED

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += PLAYER_SPEED

    # Spieler im Bildschirm halten
    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    if player.top < 0:
        player.top = 0

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    # -------------------------
    # Gegner erzeugen
    # -------------------------
    spawn_timer += dt

    if spawn_timer >= spawn_delay:
        create_enemy()
        spawn_timer = 0

    # -------------------------
    # Gegner bewegen
    # -------------------------
    for enemy in enemies:
        enemy["rect"].y += enemy["speed"]

    # Gegner entfernen
    enemies = [
        enemy
        for enemy in enemies
        if enemy["rect"].top < HEIGHT
    ]

    # -------------------------
    # Kollision
    # -------------------------
    for enemy in enemies:

        if player.colliderect(enemy["rect"]):
            game_over = True

    # -------------------------
    # Punkte
    # -------------------------
    score = (pygame.time.get_ticks() - start_time) // 100

    # Schwierigkeit erhöhen
    if score > 0 and score % 100 == 0:
        spawn_delay = max(250, 700 - score // 2)

    # -------------------------
    # Zeichnen
    # -------------------------
    screen.fill(BLACK)

    # Spieler
    pygame.draw.rect(
        screen,
        BLUE,
        player,
        border_radius=10
    )

    # Kleines Highlight auf dem Spieler
    pygame.draw.circle(
        screen,
        WHITE,
        (player.centerx, player.centery),
        6
    )

    # Gegner
    for enemy in enemies:

        pygame.draw.rect(
            screen,
            RED,
            enemy["rect"],
            border_radius=8
        )

    # Punkte
    draw_text(
        f"Punkte: {score}",
        font_small,
        WHITE,
        20,
        20,
        center=False
    )

    pygame.display.flip()


# -----------------------------
# Beenden
# -----------------------------
pygame.quit()
sys.exit()
