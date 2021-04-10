from random import randint
import pygame
from time import sleep

pond_height = 50
pond_width = 100
stone_coord = []
weed_coord = []
fish_coord = []
pond = []
coords =  [{"dx": -1, "dy": -1},{"dx": 0, "dy": -1},{"dx": 1, "dy": -1},{"dx": -1, "dy": 0},{"dx": 1, "dy": 0},{"dx": -1, "dy": 1},{"dx": 0, "dy": 1},{"dx": 1, "dy": 1}]
def get_random(maxNumber):
    return randint(0, maxNumber)




class place():
    color = (173,216,230)
    def __init__(self, x, y):
        self.color = place.color
        self.x = x
        self.y = y
    def draw(self):
        new_rect = pygame.Rect(self.x,self.y,10,10)
        pygame.draw.rect(ekraani_pind,self.color, new_rect)

class stone(place):
    color = (0,0,0)
    def __init__(self,x, y):
        super().__init__(x, y)
        self.color = stone.color

class weed(place):
    color = (30, 130, 76)
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = weed.color
        self.time_to_live = randint(1,3)
        self.age = 0
        self.spare_number = randint(1,3)
    def make_older(self):
        if(self.age == self.spare_number):
           self.spare()
        elif(self.age == self.time_to_live):
            self.die()
        elif(self.time_to_live > self.age):
            self.age += 1
    def die(self):
        for row in range(1,pond_height):
            for elem in range(1,pond_width):
                if(id(self) == id(pond[row][elem])):
                    pond[row][elem] = place(pond[row][elem].x, pond[row][elem].y)
    def spare(self):
        x = int(self.x / 10)
        y = int(self.y / 10)
        random_number = get_random(len(coords) - 1)
        x += coords[random_number]["dx"]
        y += coords[random_number]["dy"]
        if x < 99 and y < 50 and x > 0 and y > 0:
            if isinstance(pond[y][x], place) and not(isinstance(pond[y][x], stone) and not(isinstance(pond[y][x], fish))):
                pond[y][x] = self.__class__(x * 10,y * 10)
            
class fish(weed):
    color = (77, 5, 232, 1)
    def __init__(self, x, y):
        super(weed, self).__init__(x,y)
        self.color = fish.color
        self.time_to_live = 20
        self.age = 0
        self.spare_number = 10
        self.energia = 500
    def eat(self):
        x = self.think()[0]
        y = self.think()[1]
        if self.energia == 0:
            self.die()
        elif isinstance(pond[y][x], weed):
                self.energia += 1
                self.die()
                pond[y][x] = self.__class__(x * 10,y * 10)
        else:
            pond[y][x] = self.__class__(x * 10,y * 10)
            self.energia -= 1

    def think(self):
        for direction in range(len(coords)):
            x = int(self.x / 10)
            y = int(self.y / 10)
            x += coords[direction]["dx"]
            y += coords[direction]["dy"]
            if x < 99 and y < 50 and x > 0 and y > 0:
                if isinstance(pond[y][x], weed):
                    return x, y
        x = int(self.x / 10)
        y = int(self.y / 10)
        x += coords[get_random(len(coords) - 1)]["dx"]
        y += coords[get_random(len(coords) - 1)]["dy"]
        if x < 99 and y < 50 and x > 0 and y > 0:
            return x, y
        else:
            return -1, -1

    

    

    
            

def coord_maker(arr):
    random_x = randint(1,pond_width - 1)
    random_y = randint(1,pond_height - 1)
    if(not((random_x, random_y) in arr)):
        arr.append((random_x, random_y))
    else:
        while((random_x, random_y) in arr):
            random_x = randint(1,pond_width - 1)
            random_y = randint(1,pond_height - 1)
    return random_x, random_y

def stone_creater():
    for number_of_stones in range(50):
        random_x, random_y = coord_maker(stone_coord)
        pond[random_y][random_x] = stone(pond[random_y][random_x].x, pond[random_y][random_x].y)
def weed_creator():
    for number_of_stones in range(50):
        random_x, random_y = coord_maker(weed_coord)
        pond[random_y][random_x] = weed(pond[random_y][random_x].x, pond[random_y][random_x].y)
def fish_creator():
    for number_of_fishes in range(100):
        random_x, random_y = coord_maker(fish_coord)
        pond[random_y][random_x] = fish(pond[random_y][random_x].x, pond[random_y][random_x].y)


def pond_creator():    
    for row in range(pond_height + 1):
        pond.append([])
        for elem in range(pond_width + 1):
            if(row == 0 or row == 50):
                pond[row].append(stone(elem*10,row*10))
            elif(elem == 0 or elem == 100):
                pond[row].append(stone(elem*10,row*10))
            else:
                pond[row].append(place(elem*10,row*10))
def render():
    for row in range(51):
        for elem in range(101):
            pond[row][elem].draw()
            if type(pond[row][elem]) == weed or type(pond[row][elem]) == fish:
                pond[row][elem].make_older()
            if type(pond[row][elem]) == fish:
                pond[row][elem].eat()

    pygame.display.flip()

pond_creator()
stone_creater()
weed_creator()
fish_creator()
pygame.init()
ekraani_pind = pygame.display.set_mode( (pond_width * 10 + 10, pond_height * 10 + 10) )
pygame.display.set_caption("Pond")
ekraani_pind.fill( (0,255,0) )

while True:
    render()
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
pygame.quit()

