import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
FONT_COLOR = (255, 255, 255)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()    

    def move(self):
        # Randomly move apple
        self.x = random.randint(0, 19) * SIZE
        self.y = random.randint(0, 14) * SIZE 

class Snake:
        def __init__(self, parent_screen, length):
            self.parent_screen = parent_screen
            self.length = length
            self.block = pygame.image.load("resources/block.jpg").convert()
            
            # Declare the length of the snake
            self.x = [SIZE]*length
            self.y = [SIZE]*length

            # Determine initial snake movement
            self.direction = 'down'

        def increase_length(self):
            # Increase length of the snake
            self.length += 1
            self.x.append(-1)
            self.y.append(-1)

        def draw(self):
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

            # Set text on the window bars
            pygame.display.set_caption("Belajar Programming yuk Din :D")

            # Sound
            pygame.mixer.init()
            # self.play_bgm()
            self.snake_slow = 0.3
            self.surface = pygame.display.set_mode((800,600))
            self.snake = Snake(self.surface, 2)  
            self.snake.draw()
            self.apple = Apple(self.surface)
            self.apple.draw()

        def is_collision(self, x1, y1, x2, y2):
            # Detecting collisions
            if x1 >= x2 and x1 < x2 + SIZE:
                if y1 >= y2 and y1 < y2 + SIZE:
                    return True
            return False
        
        def play_sound(self, sound):
            # Create function for playing sound effect
            sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
            pygame.mixer.Sound.play(sound)

        def play_bgm(self):
            # Playing bgm
            pygame.mixer.music.load('resources/bg_music_1.mp3')
            pygame.mixer.music.play(-1, 0)

        def render_background(self):
            bg = pygame.image.load("resources/background.jpg")
            self.surface.blit(bg, (0, 0))
                    
        def play(self):
             self.render_background()
             self.snake.walk()
             self.apple.draw()    
             self.display_score()
             pygame.display.flip()

             # Check if collision occur with apple
             for i in range(self.snake.length):
                 if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                     # self.play_sound("ding")     
                     self.snake_slow -= 0.01          
                     self.snake.increase_length()
                     self.apple.move()
                 
             # Check if snake is colliding with itself
             for i in range(3, self.snake.length):
                 if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                     #self.play_sound("crash")
                     raise "Game over"      

             # Check if snake is colliding with boundaries
             if self.is_collision(0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
                 raise "Crashed the boundaries"
                     
        
        def show_game_over(self):
            self.render_background()
            font = pygame.font.SysFont('arial', 15)
            line1 = font.render(f"Game Over! Your score is {self.snake.length - 2}", True, FONT_COLOR)
            self.surface.blit(line1, (150, 300))
            line2 = font.render(f"To play again press Enter. To quit press Escape.", True, FONT_COLOR)
            self.surface.blit(line2, (150, 330))
            pygame.display.flip()
            pygame.mixer.music.pause()

        def reset(self):
            # Resetting the game
            self.snake = Snake(self.surface, 2)
            self.apple = Apple(self.surface)
            self.snake_slow = 0.3
            
        def display_score(self):
            font = pygame.font.SysFont('arial', 15)
            score = font.render(f"Score: {self.snake.length - 2}", True, FONT_COLOR)
            self.surface.blit(score, (730, 10))

        def run(self):
            running = True
            pause = False

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        # Quit key is ESC
                        if event.key == K_ESCAPE:
                            running = False

                        # Restart key is Enter
                        if event.key == K_RETURN:
                            pause = False
                            pygame.mixer.music.unpause()

                        if not pause:
                            # Movement keys is movement arrow
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

                try:
                    if not pause:
                        self.play()

                except Exception as e:
                    self.show_game_over()    
                    pause = True
                    self.reset()

                time.sleep(self.snake_slow)        
                           
if __name__ == "__main__":
    game = Game()
    game.run()    