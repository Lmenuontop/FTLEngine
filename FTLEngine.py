"""
MOST USELESS ENGINE EVER... I'LL MAKE A GAME WITH IT
"""
import pygame
import sys
import random
from pygame.locals import *
# Initialize Pygame
pygame.init()
#Initialize mixer
#mixer.init()

# Define global variables
WHITE = (255, 255, 255)
DISPLAY = None
player_x = None
player_y = None
velocity = 0
class Engine:
    def create_display(self, width, height, title):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    #def begin_frame(self):
       #self.DISPLAY.fill((30, 30, 30))

    def update(self):
        pygame.display.flip()
        clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def load_asset(self, asset_name, directory):
        return pygame.image.load(f"{directory}/{asset_name}")
    def add_default_movement(self, asset_to_move_x_pos, asset_to_move_y_pos, speed):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            asset_to_move_y_pos -= speed
        if keys[K_DOWN]:
            asset_to_move_y_pos += speed
        if keys[K_LEFT]:
            asset_to_move_x_pos -= speed
        if keys[K_RIGHT]:
            asset_to_move_x_pos += speed
        return asset_to_move_x_pos, asset_to_move_y_pos
    def add_custom_movement(self, asset_to_move_x_pos, asset_to_move_y_pos, key_up, key_down, key_left, key_right,speed):
        keys = pygame.key.get_pressed()
        if keys[key_up]:
            asset_to_move_y_pos -= speed
        if keys[key_down]:
            asset_to_move_y_pos += speed
        if keys[key_left]:
            asset_to_move_x_pos -= speed
        if keys[key_right]:
            asset_to_move_x_pos += speed
        return asset_to_move_x_pos, asset_to_move_y_pos
    
    def add_x_axis_movement(self, target_x, speed):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            target_x -= speed
        if keys[K_RIGHT]:
            target_x += speed
        return target_x
    def add_y_axis_movement(self, target_y, speed):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            target_y -= speed
        if keys[K_DOWN]:
            target_y += speed
        return target_y
    
    def draw_sprite(self, asset_name_draw, x_draw, y_draw):
        self.DISPLAY.blit(asset_name_draw, (x_draw, y_draw))

    def border_collision(self, asset_to_move_x_pos, asset_to_move_y_pos, width, height, sprite_width, sprite_height):
        # Prevent the sprite from going out of bounds on all sides
        if asset_to_move_x_pos < 0:
            asset_to_move_x_pos = 0
        elif asset_to_move_x_pos > width - sprite_width:
            asset_to_move_x_pos = width - sprite_width

        if asset_to_move_y_pos < 0:
            asset_to_move_y_pos = 0
        elif asset_to_move_y_pos > height - sprite_height:
            asset_to_move_y_pos = height - sprite_height
        return asset_to_move_x_pos, asset_to_move_y_pos
    def sprite_collision(self, player_x, player_y, enemy_x, enemy_y):
        if player_x < enemy_x + 50 and player_x + 50 > enemy_x and player_y < enemy_y + 50 and player_y + 50 > enemy_y:
            #Make this stop the sprites instead of teleportin the player
            previous_x, previous_y = player_x - 1, player_y - 1
            player_x = previous_x
            player_y = previous_y
            if player_x < previous_x:
                player_x = player_x + 1
            elif player_x > previous_x:
                player_x = player_x - 1
            if player_y < previous_y:
                player_y = player_y + 1
            elif player_y > previous_y:
                player_y = player_y - 1
            return True, player_x, player_y
        else:
            return False, player_x, player_y
    #Use for debugging. examples below
    def devmode(self, TF):
        if TF == True:
            print("(Ab)Using devmode")
        else:
            print("Not using dev mode")
    def random_number(self, lower_range, upper_range):
        randnum = random.randint(lower_range, upper_range)
        return randnum
    def enemy_ai_movement(self, enemy_x, enemy_y, player_x, player_y, speed):
        """
        Moves the enemy towards the player.
        :param enemy_x: Enemy's current x position.
        :param enemy_y: Enemy's current y position.
        :param player_x: Player's current x position.
        :param player_y: Player's current y position.
        :param speed: Speed of the enemy.
        :return: Updated enemy_x, enemy_y positions.
        """
        if enemy_x < player_x:
            enemy_x += speed
        elif enemy_x > player_x:
            enemy_x -= speed

        if enemy_y < player_y:
            enemy_y += speed
        elif enemy_y > player_y:
            enemy_y -= speed

        return enemy_x, enemy_y
    def debug_log(self, message, dvv):
        #dvv stands for dev value(checks value of dev_mode)
        if dvv == True:
            print(message)
        else:
            print("you need dev mode to see this debug message") 
    def background(self, red, green, blue):
        self.DISPLAY.fill((red, green, blue))
    #Actually useful collision
    def rect_collide(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )
    def play_audio(self, file, volume):
        mixer.music.load(file)
        mixer.music.set_volume(volume)
        mixer.music.play()
    
    def drawTriangle(self,x,y,z):
        pygame.draw.line(DISPLAY, x, y)
        pygame.draw.line(DISPLAY, y, z)
        pygame.draw.line(DISPLAY, z, x)

    #def play_music(file):
        #make this play music when called
###    
# # collision is cooked
# create_display(1080, 920)
# set_display_title("test for my set of functions")
# # Load the player sprite multiple sprite test
# player_sprite = load_asset("enemy.png", "Assets")
# enemy_sprite = load_asset("player.png", "Assets")
# # Assume the sprite is 50px by 50px (you should adjust this based on your actual sprite size)
# sprite_width, sprite_height = player_sprite.get_width(), player_sprite.get_height()
# key = pygame.key.get_pressed()
# # Ingitial position of the sprite
# player_x, player_y = 250, 250
# enemy_x, enemy_y = 250 + 50, 250 + 50
# # Get the display size for collision checking
# display_width, display_height = 1080, 920
# #game loop stuff
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running= False
#             print("process exited")
#     #enable devmode
#     devmode(True)
#     # Update the sprite's position based on keyboard input
#     player_x, player_y = add_default_movement(player_x, player_y)
#     # Check for border collision
#     player_x, player_y = check_border_collision(player_x, player_y, display_width, display_height, sprite_width, sprite_height)
#     # Check for sprite collision
#     collision_detected, player_x, player_y = sprite_collision(player_x, player_y, enemy_x, enemy_y)
#     ##COMMENTING THIS LINE MAKE SOME STUPID THING HAPPEN???
#     DISPLAY.fill((255, 255, 255))  # White background
#     # Draw the player and enemy sprites
#
#     draw_sprite(player_sprite, player_x, player_y)
#     draw_sprite(enemy_sprite, enemy_x, enemy_y)
#     # Update the display
#     pygame.display.update()
#     if key[K_KP1] and devmode(True):
#         player_x = player_x + 10
#         player_y = player_y + 10
#     random_number(1, 100)
#     enemy_ai_movement(enemy_x, enemy_y, player_x, player_y, 1)
#     draw_sprite(player_sprite, player_x, player_y)
#
#Quit pygame n stuff
#pygame.quit()
#end of test
#sys.exit()
###

