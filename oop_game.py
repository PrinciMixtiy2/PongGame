import pygame
import random
import time
from pygame.locals import *

WIDTH, HEIGHT = 1300, 700
SIZE = (WIDTH, HEIGHT)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 100
PLAYER_SPEED = 3

WHITE = (255, 255, 255)
YELLOW = (200, 200, 0)

clock = pygame.time.Clock()


class Player:
    def __init__(self, left: bool):
        if left:
            self.figure = pygame.Rect((10, 10, PLAYER_WIDTH, PLAYER_HEIGHT))
            self.speed = [0, PLAYER_SPEED]
        else:
            self.figure = pygame.Rect((WIDTH - 20, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT))
            self.speed = [0, -PLAYER_SPEED]
        self.score = 0
        self.win = False

    def move(self):
        self.figure = self.figure.move(self.speed)
        if self.figure.top <= 10 or self.figure.bottom >= HEIGHT - 10:
            self.speed[1] = 0


class PongGame:
    def __init__(self):
        pygame.init()
        self.left_player = Player(left=True)
        self.right_player = Player(left=False)
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Pong Game By Princi Mixtiy')
        self.separator = pygame.draw.line(self.screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 2)
        self.ball = pygame.draw.circle(self.screen, WHITE, (WIDTH / 2, HEIGHT / 2), 15)
        self.ball_speed = [random.choice([3, -3]), random.choice([1, -1])]
        self.start_time = 0
        self.speed_increment_delai = 10000
        self.increment_count = 0
        self.elapsed_time = 0
        self.running = False
        self.FONT = pygame.font.SysFont("Bebas Neue", 30)
        self.FONT2 = pygame.font.SysFont("Bebas Neue", 100)

    def reset(self):
        self.ball = pygame.draw.circle(self.screen, WHITE, (WIDTH / 2, HEIGHT / 2), 15)
        self.ball_speed = [random.choice([3, -3]), random.choice([1, -1])]
        self.increment_count = 0

    def draw(self):
        # ----------------------------------------- Fonds -----------------------------------------
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 2)
        pygame.draw.rect(self.screen, (155, 0, 0), (2, 2, WIDTH / 2 - 2, HEIGHT - 4))
        pygame.draw.rect(self.screen, (0, 0, 155), (WIDTH / 2, 2, WIDTH / 2 - 2, HEIGHT - 4))
        pygame.draw.rect(self.screen, WHITE, self.separator)
        # --------------------------------------- Textes ------------------------------------------
        p1_text = self.FONT.render(f'Player 1 : {self.left_player.score}', 1, WHITE)
        p2_text = self.FONT.render(f'Player 2 : {self.right_player.score}', 1, WHITE)
        time_text = self.FONT.render(f"Time: {int(self.elapsed_time)}s", 1, WHITE)
        self.screen.blit(p1_text, (40, 20))
        self.screen.blit(p2_text, (WIDTH - 40 - p2_text.get_width(), 20))
        self.screen.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, 20))
        # -------------------------------------- Objets en mouvement ------------------------------
        pygame.draw.rect(self.screen, WHITE, self.left_player.figure)
        pygame.draw.rect(self.screen, WHITE, self.right_player.figure)
        pygame.draw.ellipse(self.screen, "yellow", self.ball)
        # -----------------------------------------------------------------------------------------
        pygame.display.update()

    def listen_players_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break
            elif event.type == KEYDOWN:
                # ------------------ commande des joueurs ---------------------------
                if event.key == K_w and self.left_player.figure.top > 10:
                    self.left_player.speed[1] = -PLAYER_SPEED
                elif event.key == K_s and self.left_player.figure.bottom < HEIGHT - 10:
                    self.left_player.speed[1] = PLAYER_SPEED
                if event.key == K_UP and self.right_player.figure.top > 10:
                    self.right_player.speed[1] = -PLAYER_SPEED
                elif event.key == K_DOWN and self.right_player.figure.bottom < HEIGHT - 10:
                    self.right_player.speed[1] = PLAYER_SPEED

    def move_players(self):
        self.left_player.move()
        self.right_player.move()

    def move_ball(self):
        self.ball = self.ball.move(self.ball_speed)
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            # -- Rebondissement haut | bas --
            self.ball_speed[1] = -self.ball_speed[1]

        if ((self.ball.left <= self.left_player.figure.right and self.ball.colliderect(self.left_player.figure)) or
                (self.ball.right >= self.right_player.figure.left and self.ball.colliderect(self.right_player.figure))):
            # --------------------------------- Rebondissement sur les joueurs -----------------------------------------
            self.ball_speed[0] = -self.ball_speed[0]
            # -------------------------------- Augmentation de la vetesse verticale de la balle ------------------------
            if ((self.ball.colliderect(self.left_player.figure) and self.left_player.speed[1] < 0 and self.ball_speed[1] < 0)
                    or (self.ball.colliderect(self.right_player.figure) and 0 > self.right_player.speed[1] and self.ball_speed[1] < 0)):
                self.ball_speed[1] -= 0.5
            if ((self.ball.colliderect(self.left_player.figure) and self.left_player.speed[1] > 0 and self.ball_speed[1] > 0)
                    or (self.ball.colliderect(self.right_player.figure) and 0 < self.right_player.speed[1] and self.ball_speed[1] > 0)):
                self.ball_speed[1] += 0.5
            # -------------------------------- Augmentation de la vetesse horizontale de la balle ----------------------
            if (self.increment_count > self.speed_increment_delai and
                    (self.ball.colliderect(self.left_player.figure) or self.ball.colliderect(self.right_player.figure))):
                if self.ball_speed[0] < 0:
                    self.ball_speed[0] -= 0.5
                else:
                    self.ball_speed[0] += 0.5
                self.increment_count = 0

    def check_for_winner(self):
        if self.ball.right < 0:
            self.right_player.score += 1
            w2 = self.FONT2.render("PLAYER 2 WIN", 1, YELLOW)
            self.screen.blit(w2, (WIDTH / 2 - w2.get_width() / 2, HEIGHT / 2 - w2.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
        if self.ball.left > WIDTH:
            self.left_player.score += 1
            w1 = self.FONT2.render("PLAYER 1 WIN", 1, YELLOW)
            self.screen.blit(w1, (WIDTH / 2 - w1.get_width() / 2, HEIGHT / 2 - w1.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
        if self.ball.right < 0 or self.ball.left > WIDTH:
            self.reset()
            if self.left_player.score >= 5 or self.right_player.score >= 5:
                self.running = False

    def run(self):
        self.running = True
        self.start_time = time.time()
        while self.running:
            self.increment_count += clock.tick(60)
            self.elapsed_time = time.time() - self.start_time

            self.listen_players_input()
            self.move_players()
            self.move_ball()
            self.draw()
            self.check_for_winner()

        pygame.quit()


if __name__ == '__main__':
    game = PongGame()
    game.run()
