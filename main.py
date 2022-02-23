import pygame
from pygame.locals import *
import time

SIZE = 40

class Snake:
        def __init__(self, surface, length):
            self.parent_screen = surface
            self.length = length
            self.block = pygame.image.load("resources/block.jpg").convert()
            self.x = [SIZE]*length
            self.y = [SIZE]*length
            self.direction = 'down'

        def draw(self):
            self.parent_screen.fill((110, 110, 5))

            for i in range(self.length):
                self.parent_screen.blit(self.block, (self.x[i], self.y[i]))   

            pygame.display.flip() 

        def move_left(self):
           self.direction = 'left'

        def move_right(self):
            self.direction = 'right'

        def move_up(self):
            self.direction = 'up'

        def move_down(self):
            self.direction = 'down' 

        def walk(self):
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            if self.direction == 'left':
                self.x[0] -= SIZE
            if self.direction == 'right':
                self.x[0] += SIZE
            if self.direction == 'up':
                self.y[0] -= SIZE
            if self.direction == 'down':
                self.y[0] += SIZE            
            
            self.draw()                   
                
    
class Game:
        def __init__(self):
            pygame.init()
            self.surface = pygame.display.set_mode((800,600))
            self.surface.fill((110, 110, 5))  
            self.snake = Snake(self.surface, 2)  
            self.snake.draw()

        def run(self):
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                         #Movement keys
                        if event.key == K_UP:
                            self.snake.move_up()
                             
                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                             
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                            
                               
                    elif event.type == QUIT:
                        running = False

                self.snake.walk()
                time.sleep(0.3)        
                           
if __name__ == "__main__":
    game = Game()
    game.run()    