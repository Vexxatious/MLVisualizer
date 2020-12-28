import pygame
import numpy as np
import random
import math
import sys

gravity = 5
FPS = 60
size = width, height = 800, 600
birds = []

def start():
    global font,clock,background,bird_sprites,pipe_sprite,pipe_reverse_sprite,screen
    pygame.font.init()
    font = pygame.font.SysFont('arial', 20)
    pygame.init()

    clock = pygame.time.Clock()

    background = pygame.image.load("assets/background-day.jpg")
    bird_sprites = [pygame.image.load("assets/bird0.png"), pygame.image.load("assets/bird1.png"),
                    pygame.image.load("assets/bird2.png")]
    pipe_sprite = pygame.image.load("assets/pipe.png")
    pipe_reverse_sprite = pygame.image.load("assets/pipe-reverse.png")
    screen = pygame.display.set_mode(size)



class Pipe:
    def __init__(self, x, gapLocation):
        self.x = x
        self.gapLocation = gapLocation
        self.color = (0, 255, 0)
        self.gapSize = 100
        self.rectTop = pygame.Rect(x, 0, 52, self.gapLocation)
        self.rectBottom = pygame.Rect(x, self.gapLocation + self.gapSize, 52, height - self.gapLocation - self.gapSize)

    def update(self):
        self.x -= 2
        self.rectTop = pygame.Rect(self.x, 0, 52, self.gapLocation)
        self.rectBottom = pygame.Rect(self.x, self.gapLocation + self.gapSize, 52,
                                      height - self.gapLocation - self.gapSize)

    def draw(self):
        screen.blit(pipe_reverse_sprite, (self.x, self.gapLocation - 500))
        screen.blit(pipe_sprite, (self.x, self.gapLocation + self.gapSize))


class PipeSpawner:
    def __init__(self):
        self.pipes = [Pipe(600, random.randint(200, 400)), Pipe(1000, random.randint(200, 400))]
        self.clock = pygame.time.get_ticks()

    def reset(self):
        self.pipes = [Pipe(600, random.randint(200, 400)), Pipe(1000, random.randint(200, 400))]
        self.clock = pygame.time.get_ticks()

    def update(self):
        currentTime = pygame.time.get_ticks()
        timePassed = currentTime - self.clock
        if timePassed > 2000:
            self.pipes.append(Pipe(self.pipes[-1].x + 400, random.randint(200, 400)))
            self.clock = currentTime
        for pipe in self.pipes:
            if pipe.x + 180 < birds[0].x:
                self.pipes.remove(pipe)
            pipe.update()

    def draw(self):
        for pipe in self.pipes:
            pipe.draw()

pipeSpawner = PipeSpawner()

class Bird:
    def __init__(self, x, y):
        global gravity
        self.gameOver = False
        self.score = 0
        self.x = x
        self.y = y
        self.speed = gravity
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rect = pygame.Rect(x, y, 32, 32)
        self.animation_count = 0
        self.animation_index = 0

    def draw(self):
        if not self.gameOver:
            screen.blit(bird_sprites[self.animation_index], (self.x, self.y))

    def update(self):
        if not self.gameOver:
            if self.score > 2000:
                self.gameOver = True
            self.score += 1
            if self.y + 32 > height or self.y < 0:
                self.gameOver = True
            self.y += self.speed
            for pipe in pipeSpawner.pipes:
                if self.rect.colliderect(pipe.rectTop) or self.rect.colliderect(pipe.rectBottom):
                    self.gameOver = True
            if self.speed < gravity:
                self.speed += 1
            self.rect = pygame.Rect(self.x, self.y, 32, 32)
            if self.animation_count > 0:
                self.animation_count += 1
                self.animation_count = self.animation_count % 11
                self.animation_index = math.ceil(self.animation_count / 5)

    def jump(self):
        self.speed = -10
        if self.animation_count == 0:
            self.animation_count += 1



def getData(bird):
    data = np.zeros(3)
    data[0] = bird.y - pipeSpawner.pipes[0].gapLocation
    data[1] = pipeSpawner.pipes[0].gapLocation + pipeSpawner.pipes[0].gapSize - bird.y
    data[2] = bird.y
    return data


def update():
    for bird in birds:
        bird.update()
    pipeSpawner.update()


def draw(gen, average_fit, best_fit):
    screen.blit(background, (0, 0))
    for bird in birds:
        bird.draw()
    pipeSpawner.draw()
    bird.draw()
    gen_text = font.render(f"Generation: {gen}", True, (255, 255, 255))
    average_fit_text = font.render(f"Average fitness of last generation: {average_fit}", True, (255, 255, 255))
    best_fit_text = font.render(f"Best fitness: {best_fit}", True, (255, 255, 255))

    screen.blit(gen_text, (0, 0))
    screen.blit(average_fit_text, (0, 25))
    screen.blit(best_fit_text, (0, 50))
    pygame.display.update()
