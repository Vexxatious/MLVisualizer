import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pygame
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog
import cv2

screen = None
size = 0
width = 0
height = 0
font = None
nn = None

def init_screen():
    global screen , size ,width, height, font
    pygame.font.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)

    font = pygame.font.SysFont('arial', 32)
class NN:
    def __init__(self, dataset, parameters, model = ""):
        global nn
        nn = self
        print(model)
        init_screen()
        self.user_image = None
        self.acc = 0
        self.prediction = -1
        self.training = True
        self.mnist = tf.keras.datasets.mnist
        (self.x_train, self.y_train), (self.x_test, self.y_test) = self.mnist.load_data()
        self.x_train = tf.keras.utils.normalize(self.x_train, axis=1)
        self.x_test = tf.keras.utils.normalize(self.x_test, axis=1)
        if model == "":
            self.parameters = parameters
            self.parameters[0].append(10)
            self.model = tf.keras.models.Sequential()
            self.model.add(tf.keras.layers.Flatten())
            for i in range(len(self.parameters[0])):
                self.model.add(tf.keras.layers.Dense(self.parameters[0][i], activation=eval("tf.nn." + self.parameters[1])))
            self.model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
            self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            self.train()
        else:
            self.model = tf.keras.models.load_model(model)
            self.training = False
            _, self.acc = self.model.evaluate(self.x_test, self.y_test)
            with open("Saved Model/layers.txt" , "r") as f:
                self.parameters = [[int(i) for i in f.read().split(',')[:-1]]]
    def draw(self, epoch):
        screen.fill((0, 0, 0))
        for i in range(len(self.parameters[0])):
            r = height / (4 * min(self.parameters[0][i], 10))
            x = width / len(self.parameters[0])
            for j in range(min(self.parameters[0][i], 10)):
                pygame.draw.circle(screen, (255, 255, 255), (x + i * x - 2 * r, r + j * r * 4), r)
                if i < len(self.parameters[0]) - 1:
                    for w in range(min(10, len(np.asarray(self.model.layers[2 + i].weights[0][j])))):
                        pygame.draw.line(screen,
                                         (255, 0, 0) if np.sign(self.model.layers[i + 1].weights[0][j][w]) == -1 else (
                                         0, 0, 255), (x + i * x - 2 * r, r + j * r * 4),
                                         (x + (i + 1) * x - 2 * r, r + w * r * 4),
                                         width=min(
                                             max(abs(int(np.asarray(self.model.layers[i + 1].weights[0][j])[w] * 50)),
                                                 1), 4))

        note_text_1 = font.render("(Only showing 10 neurons from", False, (255, 255, 255))
        note_text_2 = font.render("each layer for simplicity)", False, (255, 255, 255))
        screen.blit(note_text_1, (0, 780))
        screen.blit(note_text_2, (0, 820))
        if self.user_image:
            screen.blit(self.user_image, (10, 500))
            custom_image_text = font.render("Your image", False, (255, 255, 255))
            prediction_text = font.render("Models prediction", False, (255, 255, 255))
            predicted_text = font.render(f"{self.prediction}", False, (255, 0, 0))
            screen.blit(predicted_text, (250, 550))
            screen.blit(custom_image_text, (10, 450))
            screen.blit(prediction_text, (200, 450))
        if self.training:
            training_text = font.render(f"Training, current epoch: {epoch + 1}/{self.parameters[2]}", False, (255, 0, 0))
            screen.blit(training_text, (0, 0))
        else:
            training_text = font.render("Training completed !", False, (255, 0, 0))
            accuracy_text = font.render(f"Accuracy = %{self.acc*100: .2f}",False,(25,255,255))
            screen.blit(training_text, (0, 0))
            screen.blit(accuracy_text, (0,400))
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(20, 150, 200, 70))
            save_model_text = font.render("Save model", False, (200, 200, 200))
            screen.blit(save_model_text, (30, 160))
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(20, 250, 300, 70))
            save_model_text = font.render("Test Custom Image", False, (255, 255, 255))
            screen.blit(save_model_text, (30, 260))

        pygame.display.update()

    def train(self):
        for i in range(self.parameters[2]):
            self.model.fit(self.x_train, self.y_train, epochs=1)
            self.draw(i)
        _, self.acc = self.model.evaluate(self.x_test,self.y_test)
        self.training = False


def start():

    while 1:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not nn.training:
                if 20 < mouse[0] < 220 and 150 < mouse[1] < 220:
                    nn.model.save("Saved Model")
                    ctypes.windll.user32.MessageBoxW(0, "Model saved successfully!", "Model Saved", 0)
                    with open("Saved Model/layers.txt", "w") as f:
                        for s in nn.parameters[0]:
                            f.write(str(s)+",")
                elif 20 < mouse[0] < 270 and 250 < mouse[1] < 320:
                    root = tk.Tk()
                    root.withdraw()
                    file = filedialog.askopenfilename()
                    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                    img = np.array([img])
                    img = img / 255.0
                    nn.prediction = np.argmax(nn.model.predict(img))
                    nn.user_image = pygame.image.load(file)
                    nn.user_image = pygame.transform.scale(nn.user_image, (100, 100))

        nn.draw(-1)