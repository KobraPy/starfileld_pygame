import random
import pygame
from math import sqrt

# create a screen of size say 800 * 600.
screen_width, screen_height = 800, 600
pygame.init()
pygame.display.set_caption('Starfield Simulation')
screen = pygame.display.set_mode((800, 600))

center_x = screen_width // 2
center_y = screen_height // 2
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
stars = pygame.sprite.Group()
clock = pygame.time.Clock()
ticks = clock.tick(60)

class Star(pygame.sprite.Sprite):
    def __init__(self, w=1, h=1, x=0, y=0, color="GREY", vector = None):
        super().__init__()

        #Magniude - calculating the size of the vector between the point (0,0) and (x,y) 
        delta_x = x - center_x
        delta_y = y - center_y
        magnitude = sqrt(delta_x**2 + delta_y**2)
        if magnitude > 0:  # Avoid division by zero
            vector = (delta_x/magnitude, delta_y/magnitude)
        else:
            vector = (0, 0)  # Default if spawned exactly at center

        self._width = w
        self._height = h
        self.color = color  # Store color
        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self._x_subpixel = float(x)
        self._y_subpixel = float(y)
        self.vector = vector
        print(vector)
        
    # Creating a property and setter to be able to change the POSITION inside the instances
    @property
    def x_subpixel(self):
        return self._x_subpixel
    @x_subpixel.setter
    def x_subpixel(self, new_x):
        self._x_subpixel = new_x
        self.rect.x = int(round(new_x))

    @property
    def y_subpixel(self):
        return self._y_subpixel
    @y_subpixel.setter
    def y_subpixel(self, new_y):
        self._y_subpixel = new_y
        self.rect.y = int(round(new_y))

    # Creating a property and setter to be able to change the SIZE inside the instances
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, new_width):
        self._width = new_width
        self._resize()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height
        self._resize()

        '''This method is needed beacause to resise the Surface we need to have access to values tha will
        be only avaliable after the process of repositioning them. So it gets the coordinaates of the 
        Surface and recreate it in the new position with new size. And the method "tranform" has bugs...'''
    def _resize(self):
        """Resizes the sprite and keeps its position."""
        old_topleft = self.rect.topleft  # Save current position
        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self.color)  # Reapply color
        self.rect = self.image.get_rect()
        self.rect.topleft = old_topleft  # Restore position

    def move(self):

        self.x_subpixel += self.vector[0] * ( mouse[0] / 300)
        self.y_subpixel += self.vector[1] * (mouse[0] / 300)


done = False
while not done: 

    mouse =  pygame.mouse.get_pos()

    if random.random() < 0.05:
        star = Star(x=random.randrange(0, screen_width), y=random.randrange(0, screen_height))
        stars.add(star)
    for star in stars:

        star.move()
        if star.width < 10:
            star.width += 0.1
            star.height += 0.1

    # as soon as they collide with the wall, they disappear.
    for star in stars:
        if star.x_subpixel <= 0 or star.x_subpixel >= screen_width:
            stars.remove(star)
        elif star.y_subpixel <= 0 or star.y_subpixel >= screen_height:
            stars.remove(star)

    # do regular pygame stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    stars.draw(screen)  # Group.draw uses each .image and .rect to draw
    pygame.display.flip()
pygame.quit()