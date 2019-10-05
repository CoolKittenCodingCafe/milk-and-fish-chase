import pygame, sys
import random

pygame.init()

SCREEN_TITLE = 'The milk and fish chase game'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE_COLOR = (255, 255, 255)

clock = pygame.time.Clock()

font = pygame.font.SysFont('Open Sans', 120)

rand = random.randint

# initialize the mixer
pygame.mixer.init()

class Game:

    """
    Class that holds all information for a game.
    """
    
    TICK_RATE = 60
 
    def __init__(self,image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image,(width, height))
    
    def run_game_loop(self, level):
        game_over = False
        won = False
        direction = 0

        hero = PlayerCharacter('cat.png', 375, 700, 100, 100)

        enemy0 = NonPlayerCharacter('vaccumcleaner.png', 750, 450, 100, 100)
        enemy0.SPEED *= level

        enemy1 = NonPlayerCharacter('vaccumcleaner.png', 750, 210, 100, 100)
        enemy1.SPEED *= level

        treats = Item('milkfish.png', (random.randrange(0, 700)), (random.randrange(0, 340)), 130, 130)
         
        # load the music into the mixer
        # please type the title of the mp3 file that you added to the game folder instead of the word music
        pygame.mixer.music.load('music.mp3')

         # play the music. Passing -1 repeats the music infinitely
        pygame.mixer.music.play(-1)

   
        # Main game loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = 2
                    elif event.key == pygame.K_LEFT:
                        direction = 3
                    elif event.key == pygame.K_RIGHT:
                        direction = 4
                    
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                        direction = 0
                print(event)
 
            # Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))

            # Move and draw the treats
            # Draw the treats
            treats.trick_move(direction)
            treats.draw(self.game_screen)    

            # Update the player position
            hero.move(direction)
            # Draw the player at the new position
            hero.draw(self.game_screen)
 
            # Move and draw the enemy character
            enemy0.guard_move(self.width)
            enemy0.draw(self.game_screen)

            # Spawn another enemy
            if level > 2:
                enemy1.guard_move(self.width)
                enemy1.draw(self.game_screen)

            # End game if collision between player and enemy0 ca marche
            if hero.collision_detection(enemy0):
                game_over = True
                won = False
                text = font.render('Phooey!', True, WHITE_COLOR)
                print('collision with enemy0')
                self.game_screen.blit(text, (270, 230))
                pygame.display.update()
                clock.tick(1)
                break

            # End game if collision between player and enemy1 
            if hero.collision_detection(enemy1):
                game_over = True
                won = False
                text = font.render('Ouch!', True, WHITE_COLOR)
                print('collision with enemy1')
                self.game_screen.blit(text, (270, 230))
                pygame.display.update()
                clock.tick(1)
                break
                
            # Win game if collision between player and treats
            elif hero.collision_detection(treats):
                game_over = False
                won = True
                text = font.render('Yum-yum!', True, WHITE_COLOR)
                print('collision with treasure')
                self.game_screen.blit(text, (210, 230))
                pygame.display.update()
                clock.tick(1)
                break
 
            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        # Restart game loop if we won
        # If we won we are going to run this function all over again
        if won:
            self.run_game_loop(level + 0.4)
        else:
            return
 
class GameObject:
    """
    The GameObject Class  holds the information for generic game object
    """
 
    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y
 
        self.width = width
        self.height = height
 
    # Draw the object by blitting it onto the background
    def draw(self, background):
            background.blit(self.image, (self.x_pos, self.y_pos))
            
# The PlayerCharacter Class subclasses the GameObject class
class PlayerCharacter(GameObject):
    
    # How many tiles the character moves per second
    SPEED = 10
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
 
    # Move function will move character according to direction
    def move(self, direction):
        if direction == 1 :
            self.y_pos -= self.SPEED
        elif direction == 2:
            self.y_pos += self.SPEED
        elif direction == 3:
            self.x_pos -= self.SPEED
        elif direction == 4:
            self.x_pos += self.SPEED
        
        # Make sure the character never goes off the screen
        if self.y_pos > 600 :
            self.y_pos = 600
            
        if self.y_pos < 0:
            self.y_pos = 0

        if self.x_pos > 700:
            self.x_pos = 700

        if self.x_pos < 0:
            self.x_pos = 0

    # Detect collision.
    def collision_detection(self, other_object):
        if (self.x_pos < (other_object.x_pos + other_object.width)
            and (self.x_pos + self.width) > other_object.x_pos
            and self.y_pos < (other_object.y_pos + other_object.height)
            and (self.y_pos + self.height) > other_object.y_pos):
            return True

#The NonPlayerCharacter Class subclasses the GameObject class
class NonPlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 10
 
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
 
    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def guard_move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >=  max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

# The Item Class subclasses the GameObject class
class Item(GameObject):
    SPEED = 13
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
   
   # Move function will move the item according to direction
    def trick_move(self, direction):
        if direction == 1 :
            self.x_pos -= self.SPEED
        elif direction == 2:
            self.x_pos += self.SPEED
        elif direction == 3:
            self.y_pos -= self.SPEED
        elif direction == 4:
            self.y_pos += self.SPEED
        
        # Make sure the item never goes off the screen
        if self.y_pos > 600 :
            self.y_pos = 600
            
        if self.y_pos < 0:
            self.y_pos = 0

        if self.x_pos > 700:
            self.x_pos = 700

        if self.x_pos < 0:
            self.x_pos = 0
    
new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
# We run the game loop for the very first time. We pass in a 1 as the speed of the enemies
# that will be increased with the levels
new_game.run_game_loop(1)
  
# Quit pygame and the program
pygame.quit()
sys.exit()
quit()
