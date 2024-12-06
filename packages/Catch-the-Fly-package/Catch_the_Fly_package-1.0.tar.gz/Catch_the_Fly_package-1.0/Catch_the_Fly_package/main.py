import pygame
import random
from pygame import mixer
import tkinter as tk
import os
import math
from importlib.resources import files

# classes
class Fly(pygame.sprite.Sprite):
    def __init__(self,x,y, speed, img):
        super().__init__()
        #print(x,y)
        self.image = img
        self.rect = self.image.get_rect()
        if x == None:
            self.rect.x = random.randint(0, width - self.rect.width)
        else:
            self.rect.x = x
        if y == None:
            self.rect.y = random.randint(0, height - self.rect.height)
        else:
            self.rect.y = y
        self.speed = [speed, speed]
        self.destination_x = random.randint(0, width - self.rect.width)
        self.destination_y = random.randint(0, height - self.rect.height)

    def move(self):
        if self.rect.x < self.destination_x and abs(self.rect.x - self.destination_x) > self.speed[0]:
            self.rect.x += self.speed[0]
        elif self.rect.x > self.destination_x and abs(self.rect.x - self.destination_x) > self.speed[0]:
            self.rect.x -= self.speed[0]
        if self.rect.y < self.destination_y and abs(self.rect.y - self.destination_y) > self.speed[1]:
            self.rect.y += self.speed[1]
        elif self.rect.y > self.destination_y and abs(self.rect.y - self.destination_y) > self.speed[1]:
            self.rect.y -= self.speed[1]
        # if the fly is close to the destination, then changing the destination
        if abs(self.rect.x - self.destination_x) < self.speed[0] and abs(self.rect.y - self.destination_y) < self.speed[1]:
            self.change_direction()

    def change_direction(self):
        global speed, width
        self.destination_x = random.randint(0, width - self.rect.width)
        self.destination_y = random.randint(0, height - self.rect.height)
        self.speed = [speed + random.randint(speed//10, speed//6), speed + random.randint(speed//10, speed//6)]

# functions

def load_i(image):
    image_path = files("Catch_the_Fly_package.assets").joinpath(image)
    return pygame.image.load(str(image_path))

def load_s(sound):
    sound_path = files("Catch_the_Fly_package.assets").joinpath(sound)
    return str(sound_path)

def load_b(background): 
    background_path = files("Catch_the_Fly_package.backgrounds").joinpath(background)
    return pygame.image.load(str(background_path))

def load_backgrounds():
    backgrounds = [pygame.transform.scale(load_b('bedroom.jpg'), (width, height)), pygame.transform.scale(load_b("notebook.jpg"), (width, height) ), pygame.transform.scale(load_b("kitchen.jpg"), (width, height))]
    return backgrounds

# function for applying the settings
def apply_settings(e1, e2, e3, e4, e5):
    global speed, time, background, music, sounds
    if type(e1.get()) == int:
        speed = e1.get()
    if type(e2.get()) == int:
        time = e2.get()
    background = backgrounds[e3.get()]
    music = e4.get()
    sounds = e5.get()

# settigns window function
def settings():
    root = tk.Tk()
    root.title("Settings")
    root.geometry("300x300")
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text="Settings")
    label.grid(row=0, column=0, columnspan=2)
    label = tk.Label(frame, text="Speed of the flies")
    label.grid(row=1, column=0)
    e1 = tk.IntVar()
    e1.set(speed)
    entry = tk.Entry(frame, textvariable=e1)
    entry.grid(row=1, column=1)
    label = tk.Label(frame, text="Time for the round")
    label.grid(row=2, column=0)
    e2 = tk.IntVar()
    e2.set(time)
    entry = tk.Entry(frame, textvariable=e2)
    entry.grid(row=2, column=1)
    label = tk.Label(frame, text="Background")
    label.grid(row=3, column=0)
    e3 = tk.StringVar()
    e3.set(backgrounds.index(background))
    option_menu = tk.OptionMenu(frame, e3, *range(len(backgrounds)))
    option_menu.grid(row=3, column=1)
    label = tk.Label(frame, text="Music")
    label.grid(row=4, column=0)
    e4 = tk.BooleanVar()
    e4.set(music)
    checkbutton = tk.Checkbutton(frame, variable=e4)
    checkbutton.grid(row=4, column=1)
    label = tk.Label(frame, text="Sounds")
    label.grid(row=5, column=0)
    e5 = tk.BooleanVar()
    e5.set(sounds)
    checkbutton = tk.Checkbutton(frame, variable=e5)
    checkbutton.grid(row=5, column=1)
    button = tk.Button(frame, text="Apply", command=lambda: apply_settings(e1, e2, e3, e4, e5))
    button.grid(row=6, column=0, columnspan=2)

    root.mainloop()

# game over screen function
def game_over_screen():
    global running, num_of_clicks, number_of_flies
    game_over = True
    while game_over:
        screen.fill((0, 0, 0))
        # drawing the points
        text = font.render(f'Game Over! Points: {points}', True, (255, 255, 255))
        screen.blit(text, (width/2 - text.get_width() // 2, height/2 - text.get_height() // 2))
        # drawing the number of clicks
        text = font.render(f'Number of clicks: {num_of_clicks}', True, (255, 255, 255))
        screen.blit(text, (width/2 - text.get_width() // 2, height/2 - text.get_height() // 2 + text.get_height()))
        # drawing the number of flies
        text = font.render(f'Number of flies: {number_of_flies}', True, (255, 255, 255))
        screen.blit(text, (width/2 - text.get_width() // 2, height/2 - text.get_height() // 2 + 2 * text.get_height()))
        # drawing the time
        text = font.render(f'Time: {int(time)}', True, (255, 255, 255))
        screen.blit(text, (width/2 - text.get_width() // 2, height/2 - text.get_height() // 2 + 3 * text.get_height()))
        # drawing the hit to miss ratio
        if num_of_clicks == 0:
            hit_to_miss_ratio = 0
        else:
            hit_to_miss_ratio = math.floor(points / num_of_clicks * 100)
        text = font.render(f'Hit ratio: {hit_to_miss_ratio}%', True, (255, 255, 255))
        screen.blit(text, (width/2 - text.get_width() // 2, height/2 - text.get_height() // 2 + 4 * text.get_height()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        clock.tick(frame_rate)
        pygame.display.update()

# reset game function
def reset_game():
    global points, flies, number_of_flies, background, backgrounds, time_till_end, music
    points = 0
    for fly in flies:
        flies.remove(fly)
    resize_screen()
    fly = Fly(None, None, speed, fly_img)
    flies.add(fly)
    number_of_flies = 1
    background = random.choice(backgrounds)
    time_till_end = time * frame_rate
    if music:
        mixer.music.load(load_s('background_music.mp3'))
        mixer.music.play(-1)

# resize screen function:
def resize_screen():
    global width, height, base_size, settings_img, speed, fly_img, font, screen, backgrounds
    width, height = screen.get_size()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    base_size = width // 18
    backgrounds = load_backgrounds()
    settings_img = pygame.transform.scale(load_i('settings.png'), (base_size, base_size))
    speed = base_size // 12
    fly_img = pygame.transform.scale(load_i('fly.png'), (base_size, base_size))
    font = pygame.font.Font('freesansbold.ttf', base_size // 2)

# Initializing Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Catch the Fly!")
icon = load_i('fly.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
base_size = width // 18
#print(base_size)
backgrounds = load_backgrounds()
background = random.choice(backgrounds)
settings_img = pygame.transform.scale(load_i('settings.png'), (base_size, base_size))
frame_rate = 90
speed = base_size // 12
fly_img = pygame.transform.scale(load_i('fly.png'), (base_size, base_size))
fly = Fly(None, None, speed, fly_img)
flies = pygame.sprite.Group()
flies.add(fly)
number_of_flies = 1
font = pygame.font.Font('freesansbold.ttf', base_size // 2)
slap_sound = mixer.Sound(load_s('slap.mp3'))
sounds = True
music = True

# main loop
running = True
points = 0
time = 60
time_till_end = time * frame_rate
num_of_clicks = 0
if music:
    mixer.music.load(load_s('background_music.mp3'))
    mixer.music.play(-1)
while running:

    # background
    screen.blit(background, (0, 0))

    # event handling 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                num_of_clicks += 1
                # checking if player clicked on the settings button
                if event.pos[0] > width - settings_img.get_width() and event.pos[1] < settings_img.get_height():
                    settings()
                # checking if player clicked on a fly
                for fly in flies:
                    if fly.rect.collidepoint(event.pos):
                        points += 1
                        if sounds:
                            slap_sound.play()
                        fly.change_direction()
                        # if the points are multiples of 10, then deleting the old fly and adding two new flies
                        if points % 10 == 0:
                            x, y = fly.rect.x, fly.rect.y
                            flies.remove(fly)
                            number_of_flies += 1
                            if number_of_flies < 10: # ten flies is the max
                                for i in range(2):
                                    fly = Fly(x,y,speed, fly_img)
                                    flies.add(fly)

    # moving the flies
    for fly in flies:
        fly.move()
        if random.randint(0, 100) == 0: # maybe will be changed later
            fly.change_direction()

    # drawing the flies
    flies.draw(screen)

    # drawing the points
    text = font.render(f'Points: {points}', True, (255, 0, 0))
    screen.blit(text, (width/2 - text.get_width() // 2, 10))

    # drawing the time
    text = font.render(f'Time: {int(time_till_end/frame_rate)}', True, (255, 0, 0))
    screen.blit(text, (width/2 - text.get_width() // 2, 10 + text.get_height()))

    # drawing the settings button in the top right corner
    screen.blit(settings_img, (width - settings_img.get_width(), 0))

    # moving the flies that are not on the screen back, it shouldnt happen, but just in case
    for fly in flies:
        if fly.rect.x > width or fly.rect.x < 0 or fly.rect.y > height or fly.rect.y < 0:
            fly.change_direction()

    # checking if the game is over
    if time_till_end <= 0:
        game_over_screen()
    else:
        time_till_end -= 1

    clock.tick(frame_rate)
    pygame.display.update()