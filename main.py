import pygame
import sys
import pickle 
from random import randint

pygame.init()

WIDTH = 336
HEIGHT = 540

SCALE = 1.2

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# backround music
pygame.mixer.music.load("sounds/backround_music.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play()

# point sound
point_sound = pygame.mixer.Sound("sounds/point.mp3")
point_sound.set_volume(0.1)

# die sound
die_sound = pygame.mixer.Sound("sounds/die.mp3")
die_sound.set_volume(0.1)

# flap sound
flap_sound = pygame.mixer.Sound("sounds/flap.mp3")
flap_sound.set_volume(0.1)


class Game():
    def __init__(self):
        self.state = "play"
        self.score = 0
        try: 
            file = open("record.pickle", "rb")
            self.record = pickle.load(file)
            file.close()
        except:
            file = open("record.pickle", "wb")
            pickle.dump(0, file)
            file.close()
            self.record = 0
        self.score_font = pygame.font.Font("Flappy-Bird.ttf", 55)
        self.score_text = self.score_font.render("0", True, "white")
        self.score_pos = (WIDTH - 316, 20)

        self.record_font = pygame.font.Font("Flappy-Bird.ttf", 55)
        self.record_text = self.record_font.render("0", True, "white")
        self.record_pos = (WIDTH - 40 - (self.record_text.get_width() // 2), 20)

        self.restart_font = pygame.font.Font("Flappy-Bird.ttf", 45)
        self.restart_text = self.restart_font.render("Press SPACE to restart", True, "white")
        self.restart_pos = (WIDTH // 2 - (self.restart_text.get_width() // 2), HEIGHT // 2 - (self.restart_text.get_height() // 2))

    def draw_score(self):
        window.blit(self.score_text, self.score_pos) 
        window.blit(self.record_text, self.record_pos) 

    def draw_restart(self):
        window.blit(self.restart_text, self.restart_pos)

    def update_score(self):
        self.score_text = self.score_font.render(str(self.score) ,True, "white")
        self.score_pos = (WIDTH - 316, 20)
        self.record_text = self.record_font.render(str(self.record) ,True, "white")
        self.record_pos = (WIDTH - 40 - (self.record_text.get_width() // 2), 20)

    def restart(self):
        self.state = "play"
        self.score = 0
        self.update_score()
        pipes.gate = randint(150, HEIGHT - 150)
        pipes.rect_top.bottomleft = (WIDTH, pipes.gate - 65)
        pipes.rect_bot.topleft = (WIDTH, pipes.gate + 65)
        bird.rect.center = (WIDTH//3, HEIGHT//2)
        bird.fall = False
        
class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gate = randint(150, HEIGHT - 150)
        self.image_top = pygame.image.load("images/top-pipe.png")
        self.image_top = pygame.transform.scale_by(self.image_top, SCALE)
        self.rect_top = self.image_top.get_rect()
        self.rect_top.bottomleft = (WIDTH, self.gate - 65)
    
        self.image_bot = pygame.image.load("images/bot-pipe.png")
        self.rect_bot = self.image_bot.get_rect()
        self.rect_bot.topleft = (WIDTH, self.gate + 65)
        self.image_bot = pygame.transform.scale_by(self.image_bot, SCALE)

    def draw(self):
        window.blit(self.image_top, self.rect_top)
        window.blit(self.image_bot, self.rect_bot)

    def update(self):
        self.rect_top.x -= 3
        self.rect_bot.x -= 3
        if self.rect_top.right <= 0:
            self.gate = randint(150, HEIGHT - 150)
            self.rect_top.bottomleft = (WIDTH, self.gate - 65)
            self.rect_bot.topleft = (WIDTH, self.gate + 65)
            game.score += 1
            if game.score > game.record:
                game.record = game.score
                file = open("record.pickle", "wb")
                pickle.dump(game.record, file)
                file.close()
            point_sound.play()
            game.update_score(   )

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_speed = -2
        self.speed = self.base_speed
        self.image = pygame.image.load("images/bird.png")
        self.rect = self.image.get_rect(center = (WIDTH//3, HEIGHT//2))
        self.fall = False

    def draw(self):
        window.blit(self.image, self.rect)

    def update(self, events):
        self.rect.y -= self.speed
        self.speed -= 1
        if self.rect.bottom >=  HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
        if game.state == "play":
            if self.rect.y < 0:
                self.rect.y = 0
            if self.speed < self.base_speed:
                self.speed = self.base_speed
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE or e.type == pygame.MOUSEBUTTONDOWN:
                    self.speed = 10
                    flap_sound.play()
            if self.rect.collideobjectsall([pipes.rect_bot, pipes.rect_top]) or self.rect.bottom >= HEIGHT - 30:
                game.state = "lose"
                self.speed = -6
                die_sound.play()

class Background():
    def __init__(self):
        self.image = pygame.image.load("images/background.png")
        self.x1 = 0
        self.x2 = WIDTH


    def draw(self):
        window.blit(self.image, (self.x1, 0)) 
        window.blit(self.image, (self.x2, 0))

    def update(self):
        self.x1 = self.x1 - 1
        if self.x1 <= -WIDTH:
            self.x1 = WIDTH
        self.x2 = self.x2 - 1
        if self.x2 <= -WIDTH:
            self.x2 = WIDTH

class Ground():
    def __init__(self):
        self.image = pygame.image.load("images/ground.png")
        self.x1 = 0
        self.x2 = WIDTH
        self.y = HEIGHT - 30


    def draw(self):
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))

    def update(self):
        self.x1 = self.x1 - 1
        if self.x1 <= -WIDTH:
            self.x1 = WIDTH
        self.x2 = self.x2 - 1
        if self.x2 <= -WIDTH:
            self.x2 = WIDTH

bg = Background()
bird = Bird()
pipes = Pipes()
ground = Ground()
game = Game()

# The game
while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and game.state == "lose":
                game.restart()
        if e.type == pygame.MOUSEBUTTONDOWN and game.state == "lose":
            game.restart()

    if game.state == "play":
        # update
        pipes.update()
        bg.update()
        ground.update()
    bird.update(events)
    # draw
    bg.draw()
    pipes.draw()
    bird.draw()
    ground.draw()
    game.draw_score()
    if game.state == "lose":
        game.draw_restart()
    pygame.display.flip()
    clock.tick(60)
