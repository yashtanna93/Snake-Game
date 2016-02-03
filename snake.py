import pygame
from pygame.locals import *
import random

size = width, height = 640, 480
block_size = 20
score=0

class Food:
    def __init__(self, screen, snake):
        self.snake = snake
        self.screen = screen
        self.image = self.image = pygame.Surface((20, 20));
        self.image.fill((255,0,0));
        self.spawn()
        
    def spawn(self):
        collision = True
    
        while collision:
            random_x = random.randrange(0, width, block_size)
            random_y = random.randrange(0, height, block_size)
            
            collision = False
            
            for each in snake.parts:
                if each.position.x == random_x and each.position.y == random_y:
                    collision = True
                    break
        
        self.position = self.image.get_rect().move(random_x, random_y)
        
        self.blit()
        
    def blit(self):
        self.screen.blit(self.image, self.position)

class Part:
    def __init__(self, x=0, y=0, direction=20):
        self.direction = direction
        self.image = pygame.Surface((20, 20));
        self.image.fill((0, 255, 0));
        self.position = self.image.get_rect().move(x, y)
        self.speed = block_size
        
    def change_direction(self, direction):
        if self.direction + direction == 0:
            return
            
        self.direction = direction
        
    def move(self):
        if self.position.x >= width - block_size and self.direction == 20:
            return False
            
        if self.position.y >= height - block_size and self.direction == -10:
            return False
            
        if self.position.x <= 0 and self.direction == -20:
            return False
            
        if self.position.y <= 0 and self.direction == 10:
            return False
        
        if self.direction == 10:
            self.position = self.position.move(0, -self.speed)
        elif self.direction == -10:
            self.position = self.position.move(0, self.speed)
        elif self.direction == 20:
            self.position = self.position.move(self.speed, 0)
        elif self.direction == -20:
            self.position = self.position.move(-self.speed, 0)
          
        return True

class Snake:
    def __init__(self, screen, x=0, y=0):
        self.screen = screen
        self.head = Part(x, y)
        self.direction = 20
        self.length = 0
        self.parts = []
        self.parts.append(self.head)
        self.extend_flag = False
        
    def change_direction(self, direction):
        self.direction = direction
        
    def move(self, food):
        new_direction = self.direction
        old_direction = None
        new_part = None
    
        if self.extend_flag:
            last_part = self.parts[-1]
            new_part = Part(last_part.position.x, last_part.position.y, last_part.direction)
    
        for each in self.parts:
            old_direction = each.direction
            each.change_direction(new_direction)
            
            if not each.move():
                return False
                
            new_direction = old_direction
            
        if self.extend_flag:
            self.extend(new_part)
        
        for each in self.parts[1:]:
            if each.position.x == self.head.position.x and each.position.y == self.head.position.y:
                return False
                
        if food.position.x == self.head.position.x and food.position.y == self.head.position.y:
            food.spawn()
            self.extend_flag = True
        
        return True
            
    def extend(self, part):
        self.parts.append(part)
        self.length += 1
        self.extend_flag = False
        
    def blit(self):
        for each in self.parts:
            f=pygame.font.SysFont('Arial', 29);
            t=f.render('Score : '+str(self.length), True, (255,255,255));
            screen.blit(t, (10, 10))
            self.screen.blit(each.image, each.position)

            
black = 0, 0, 0

pygame.init()
pygame.display.set_caption('CG project by Yash Tanna')
screen = pygame.display.set_mode(size)

game = True

while True:
    snake = Snake(screen)
    food = Food(screen, snake)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            
            if event.type == KEYDOWN:
                if (event.key == K_RIGHT):
                    snake.change_direction(20)
                elif (event.key == K_LEFT):
                    snake.change_direction(-20)
                elif (event.key == K_UP):
                    snake.change_direction(10)
                elif (event.key == K_DOWN):
                    snake.change_direction(-10)
                elif (event.key == K_c):
                    snake.extend_flag = True
                    
        if not snake.move(food):
            game = False
            break
            
        screen.fill(black)
        snake.blit()
        food.blit()
        pygame.display.update()
        pygame.time.delay(100)

    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()

            if event.type == KEYDOWN:
                if (event.key == K_RETURN):
                    game = True
                elif (event.key == K_ESCAPE) :
                    quit()
        f=pygame.font.SysFont('Arial', 29);
        bg=(' GAME OVER :');
        bg1=('PRESS ENTER TO PLAY AGAIN')
        t=f.render('Your score was: '+str(snake.length), True, (255,255,255));
        background = f.render(bg, True, (255, 255, 255));
        background1= f.render(bg1, True, (255,255,255));
        screen.blit(background, (220, 190))
        screen.blit(background1, (100, 220))
        screen.blit(t, (180, 270))
        pygame.display.flip()
        pygame.time.delay(100)
