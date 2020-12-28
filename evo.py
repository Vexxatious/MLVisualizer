import flappy_bird as fb
import random
import nn_layer as nn
import sys
from numpy import array
import numpy as np
import math


class Network:
    def __init__(self):
        self.bird = fb.Bird(100, 300)
        self.layer1 = nn.Layer(3, 3)
        self.layer2 = nn.Layer(3, 5)
        self.layer3 = nn.Layer(5, 1)
        self.layers = [self.layer1, self.layer2, self.layer3]
        self.weights = [layer.weights for layer in self.layers]

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs


class EVO:
    def __init__(self,dataset, parameters):
        self.nets = []
        self.generation = 0
        self.generationSize = parameters[0]
        for i in range(self.generationSize):
            self.nets.append(Network())
            fb.birds.append(self.nets[i].bird)
        self.mutationRate = parameters[1]
        self.average_fitness = 0
        self.best_fitness = 0
        self.run()

    def breed(self, weights1, weights2):
        child = Network()
        weights = []

        for w1, w2 in zip(weights1, weights2):
            w = []
            for column1, column2 in zip(w1, w2):
                column = []
                for theta1, theta2 in zip(column1, column2):
                    choosen = random.choice((theta1, theta2))
                column.append(choosen)
                w.append(column)
            weights.append(array(w))
        child.weights = weights
        return child

    def mutate(self, net):
        for layer in net.layers:
            for x in range(len(layer.weights)):
                for y in range(len(layer.weights[x])):
                    if random.uniform(0, 1) < self.mutationRate:
                        change = random.uniform(-0.5, 0.5)
                        layer.weights[x][y] += change

            for b in range(len(layer.biases)):
                if random.uniform(0, 1) < self.mutationRate:
                    change = random.uniform(-0.5, 0.5)
                    layer.biases[b] += change

    def evolve(self):
        self.nets.sort(key=lambda x: x.bird.score, reverse=True)
        winners = self.nets[:int(self.generationSize / 3)]
        self.average_fitness = sum(net.bird.score for net in self.nets) / len(self.nets)
        print(f"Average fitness: {self.average_fitness}")
        if self.nets[0].bird.score > self.best_fitness:
            self.best_fitness = self.nets[0].bird.score
        print([net.bird.score for net in self.nets])
        for net in winners:
            net.bird.gameOver = False
            net.bird.score = 0

        for i in range(int(self.generationSize / 3), self.generationSize):
            if i == int(self.generationSize / 3):
                bird = self.breed(winners[0].weights, winners[1].weights)
            else:
                bird = self.breed(random.choice(winners).weights, random.choice(winners).weights)

            self.mutate(bird)
        self.nets[i] = bird

        fb.pipeSpawner.reset()
        fb.birds = []
        for net in self.nets:
            fb.birds.append(net.bird)

        self.generation += 1
        print(f"Generation: {self.generation}, GenerationSize: {len(self.nets)}")

    def run(self):
        fb.start()
        while 1:
            fb.clock.tick(fb.FPS)
            for event in fb.pygame.event.get():
                if event.type == fb.pygame.QUIT:
                    sys.exit()
            genOver = True
            for net in self.nets:
                genOver = genOver and net.bird.gameOver
            if not genOver:
                for net in self.nets:
                    if not net.bird.gameOver:

                        if net.forward(fb.getData(net.bird)) > 0.5:
                            net.bird.jump()
            else:
                self.evolve()

            fb.update()
            fb.draw(self.generation, self.average_fitness, self.best_fitness)




