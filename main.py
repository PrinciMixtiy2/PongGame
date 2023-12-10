import pygame
from pygame.locals import *

import random
import time

pygame.init()

# ------------------------ Constantes ------------------------
WIDTH, HEIGHT = 1200, 600
SIZE = (WIDTH, HEIGHT)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 100
PLAYER_SPEED = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FONT = pygame.font.SysFont("Bebas Neue", 30)
FONT2 = pygame.font.SysFont("Bebas Neue", 100)

clock = pygame.time.Clock()
# ------------------------------------------------------------

# ------------------ Configuration de display ---------------------
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Pong Game By Princi Mixtiy')
# -----------------------------------------------------------------

# -------------------------------------------Definition des figures -------------------------------------------
player1 = pygame.Rect((10, 10, PLAYER_WIDTH, PLAYER_HEIGHT))
player2 = pygame.Rect((WIDTH - 20, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT))
separator = pygame.draw.line(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 2)
ball = pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), 20)
# -------------------------------------------------------------------------------------------------------------

# --------- Variables liees aux figures ---------------
p1_score = 0
p2_score = 0
p1_speed = [0, PLAYER_SPEED]
p2_speed = [0, -PLAYER_SPEED]
p1_lose = False
p2_lose = False
ball_speed = [random.choice([3, -3]), random.choice([1, -1])]
# -----------------------------------------------------

# ----------- Variables liees au temps ----------------
start_time = time.time()
speed_time_increment = 10000
increment_count = 0
# -----------------------------------------------------


def draw():
    # ----------------------------------------- Fonds -----------------------------------------
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 2)
    pygame.draw.rect(screen, (155, 0, 0), (2, 2, WIDTH / 2 - 2, HEIGHT - 4))
    pygame.draw.rect(screen, (0, 0, 155), (WIDTH / 2, 2, WIDTH / 2 - 2, HEIGHT - 4))
    pygame.draw.rect(screen, WHITE, separator)
    # --------------------------------------- Textes ------------------------------------------
    screen.blit(p1_text, (40, 20))
    screen.blit(p2_text, (WIDTH - 40 - p2_text.get_width(), 20))
    screen.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, 20))
    # -------------------------------------- Objets en mouvement ------------------------------
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    # -----------------------------------------------------------------------------------------
    pygame.display.update()


running = True
while running:
    increment_count += clock.tick(60)

    if increment_count > speed_time_increment and (ball.colliderect(player1) or ball.colliderect(player2)):
        """\
        Incrementer de 0.5 la vitesse de la balle
        sur l'axe x apres 10s et que la ball touche un joueur.
        """
        if ball_speed[0] < 0:
            ball_speed[0] -= 0.5
        else:
            ball_speed[0] += 0.5
        increment_count = 0

    # Temps passe en seconde depuis le lancement du jeu
    elapsed_time = time.time() - start_time
    time_text = FONT.render(f"Time: {int(elapsed_time)}s", 1, WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # ------------------ commande des joueurs ---------------------------
            if event.key == K_w and player1.top > 10:
                p1_speed[1] = -PLAYER_SPEED
            elif event.key == K_s and player1.bottom < HEIGHT - 10:
                p1_speed[1] = PLAYER_SPEED
            if event.key == K_UP and player2.top > 10:
                p2_speed[1] = -PLAYER_SPEED
            elif event.key == K_DOWN and player2.bottom < HEIGHT - 10:
                p2_speed[1] = PLAYER_SPEED
            # -------------------------------------------------------------------

    screen.fill(BLACK)

    p1_text = FONT.render(f'Player 1 : {p1_score}', 1, WHITE)
    p2_text = FONT.render(f'Player 2 : {p2_score}', 1, WHITE)

    # ---------------------- Mouvement des joueurs --------------------------
    player1 = player1.move(p1_speed)
    if player1.top <= 10 or player1.bottom >= HEIGHT - 10:
        p1_speed[1] = 0

    player2 = player2.move(p2_speed)
    if player2.top <= 10 or player2.bottom >= HEIGHT - 10:
        p2_speed[1] = 0
    # -----------------------------------------------------------------------

    # -----------------------------------------------Mouvements de la balle -------------------------------------------
    ball = ball.move(ball_speed)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        # -- Rebondissement haut | bas --
        ball_speed[1] = -ball_speed[1]

    if (ball.left <= player1.right and ball.colliderect(player1)) or (ball.right >= player2.left and
                                                                      ball.colliderect(player2)):
        # --------------------------------- Rebondissement sur les joueurs --------------------------------------------
        ball_speed[0] = -ball_speed[0]
        # -------------------------------- Augmentation de la vetesse verticale de la balle ---------------------------
        if (ball.colliderect(player1) and p1_speed[1] < 0 and ball_speed[1] < 0) or (ball.colliderect(player2) and 0 >
                                                                                     p2_speed[1] and ball_speed[1] < 0):
            ball_speed[1] = ball_speed[1] - 0.5
        if (ball.colliderect(player1) and p1_speed[1] > 0 and ball_speed[1] > 0) or (ball.colliderect(player2) and 0 <
                                                                                     p2_speed[1] and ball_speed[1] > 0):
            ball_speed[1] = ball_speed[1] + 0.5
        # -------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -- Conditions de defaites --
    if ball.right < 0:
        p1_lose = True
    if ball.left > WIDTH:
        p2_lose = True
    # ----------------------------

    # ------------------------------------- Dessin -------------------------------------------------------
    draw()
    if p1_lose:
        p2_score += 1
        w2 = FONT2.render("PLAYER 2 WIN", 1, YELLOW)
        screen.blit(w2, (WIDTH / 2 - w2.get_width() / 2, HEIGHT / 2 - w2.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(4000)
    if p2_lose:
        p1_score += 1
        w1 = FONT2.render("PLAYER 1 WIN", 1, YELLOW)
        screen.blit(w1, (WIDTH / 2 - w1.get_width() / 2, HEIGHT / 2 - w1.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(4000)
    if p1_lose or p2_lose:
        # ---------------------- Reinitialisation des formes ----------------------------------------
        player1 = pygame.Rect((10, 10, PLAYER_WIDTH, PLAYER_HEIGHT))
        player2 = pygame.Rect((WIDTH - 20, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT))
        ball = pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), 20)
        # ---------------------- Reinitialisation des vitesses --------------------------------------
        ball_speed = [random.choice([3, -3]), random.choice([1, -1])]
        p1_speed = [0, PLAYER_SPEED]
        p2_speed = [0, -PLAYER_SPEED]
        # ------------- Remise a zero du compteur de temps pour l'incrementation de vitesse ---------
        increment_count = 0
        # ------------------------ Remise a zero des status (Winer | Loser) -------------------------
        p1_lose = False
        p2_lose = False
    # ---------------------------------------------------------------------------------------------------

    if p2_score >= 5 or p1_score >= 5:
        break

pygame.quit()
