"""
A module that allows a genius bird to play a famous mobile game (Don't Touch The Spikes)

Author
----------
Adam Skudlarek

Classes
----------
Game:
    Maintains the game loop for the running of the game

"""
import sys
import os
import pygame

class Bird(pygame.sprite.Sprite):
    """
    A class to represent the bird/main player.

    Attributes
    ----------
    image : pygame image
        image of the bird sprite
    rect : pygame rect
        rect information (x, y) for sprite
    bird_height : int
        contains the image height of the bird for resizing
    bird_width : int
        contains the image width of the bird for resizing
    x_speed : int
        the horizontal speed of the bird
    velocity : int
        the velocity of the bird to calculate force
    mass : int
        the mass of the bird to calculate force
    isjump : int
        is the bird currently jumping; 1 = True, 0 = False
    alive : bool
        determines whether or not the bird is alive still

    Methods
    -------
    get_height():
        Returns the height of the sprite image.
    get_width():
        Returns the width of the sprite image.
    collid(pygame:sprite_group)
        Returns whether or not bird has collided with sprite in sprite_group.
    flip():
        Flips the birds direction.
    jump():
        Sets isjump to True and moves sprite for jump.
    died():
        Sets the bird to be dead.
    reset():
        Resets the bird to restart game.
    update():
        Updates the birds position.
    """
    # Bird Image Size
    bird_height = 65
    bird_width = 100

    # Bird mechanics
    x_speed = 10
    velocity = 8
    mass = 2

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load image sprite
        self.image = pygame.image.load('images/bird.png').convert()

        # Resize the image
        self.image = pygame.transform.scale(self.image, (self.bird_width, self.bird_height))

        # Set transparency color
        self.image.set_colorkey(Game.BLACK)

        # Set rect of the image
        self.rect = self.image.get_rect()

        # Bird is not currently jumping
        self.isjump = 0

        # Set the bird to be alive
        self.alive = True

    def get_height(self):
        '''
        Gets the height of the sprites image.

                Returns:
                        a (int): The height of the sprite's image
        '''
        return self.image.get_height()

    def get_width(self):
        '''
        Gets the width of the sprites image.

                Returns:
                        a (int): The width of the sprite's image
        '''
        return self.image.get_width()

    def flip(self):
        '''
        Flips the birds direction.
        '''
        self.image = pygame.transform.flip(self.image, True, False)
        if self.x_speed > 0:
            self.x_speed = -10
        else:
            self.x_speed = 10

    def collide(self, sprite_group):
        '''
        Checks if the bird has collided with another sprite in sprite group.

                Returns:
                        a (bool): Whether or not the bird collided
        '''
        return pygame.sprite.spritecollide(self, sprite_group, False)

    def jump(self):
        '''
        Sets the bird to be currently jumping for the update function.
        '''
        self.isjump = 1

    def died(self):
        '''
        Sets the bird to be dead.
        '''
        self.alive = False

    def reset(self, display_width, display_height):
        '''
        Resets the birds state to restart the game.
        '''
        # Set bird to be alive
        self.alive = True

        # Position bird in the center of the screen
        self.rect.x = (display_width - self.get_width()) / 2
        self.rect.y = (display_height / 2) - self.get_height()

        # Reset the velocity and jump
        self.isjump = 0
        self.velocity = 8

    def update(self):
        '''
        Updates the position of the bird.
        '''
        if self.alive:
            # Update horizontal movement
            self.rect.x += self.x_speed

            # Update gravity and falling based on force
            force = self.mass * self.velocity
            self.rect.y = self.rect.y - force
            self.velocity -= 1

            # Reset upon jumping
            if self.isjump:
                self.velocity = 8
                self.isjump = 0

class Spike(pygame.sprite.Sprite):
    """
    A class to represent the static bottom and top spikes as sprites.

    Attributes
    ----------
    image : pygame image
        image of the sprite
    rect : pygame rect
        rect information (x, y) for sprite

    Methods
    -------
    get_height():
        Returns the height of the sprite image.
    flip():
        Flips the sprite image horizontally.
    """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load image sprite
        self.image = pygame.image.load('images/spikes.png').convert()

        # Set transparency color
        self.image.set_colorkey(Game.WHITE)

        # Set rect of the image
        self.rect = self.image.get_rect()

    def get_height(self):
        '''
        Gets the height of the sprites image.

                Returns:
                        a (int): The height of the sprite's image
        '''
        return self.image.get_height()

    def flip(self):
        '''
        Flips the sprite image horizontally.
        '''
        self.image = pygame.transform.flip(self.image, False, True)

class Wall(pygame.sprite.Sprite):
    """
    A class to represent the walls confining the player as sprites.

    Attributes
    ----------
    image : pygame image
        image of the sprite
    rect : pygame rect
        rect information (x, y) for sprite

    Methods
    -------
    get_width():
        Returns the width of the sprite image.
    """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load image sprite
        self.image = pygame.image.load('images/wall.png').convert()

        # Set transparency color
        self.image.set_colorkey(Game.WHITE)

        # Set rect of the image
        self.rect = self.image.get_rect()

    def get_width(self):
        '''
        Gets the width of the sprites image.

                Returns:
                        a (int): The width of the sprite's image
        '''
        return self.image.get_width()

class Score:
    """
    A class to represent the current score of the game.

    Attributes
    ----------
    score : int
        current score of the game
    font : pygame
        font of the text to display
    x_pos : int
        x position of the score display
    y_pos : int
        y position of the score display

    Methods
    -------
    increment():
        Increments the score by 1.
    reset():
        Resets the score back to 0.
    draw(pygame:screen):
        Draws the text for the score to the given screen.
    """
    score = 0

    def __init__(self, x, y, font):
        self.font = font
        self.x_pos = int(x / 2)
        self.y_pos = int(y / 4)

    def increment(self):
        '''
        Increments the score by 1.
        '''
        self.score += 1

    def reset(self):
        '''
        Resets the score back to 0.
        '''
        self.score = 0

    def draw(self, screen):
        '''
        Draws the score onto the given screen.

                Parameters:
                        a (pygame:surface): A screen to have the score drawn to
        '''
        text = self.font.render(str(self.score), True, Game.WHITE)
        screen.blit(text, (self.x_pos, self.y_pos))

class Game:
    """
    A class to represent the game Don't Touch The Spikes and allow an AI to play that game.

    Attributes
    ----------
    screen : pygame
        the screen for the game
    font : pygame
        font used for text in the window
    score : Score
        holds the score for the current game
    display_width : int
        width of the screen
    display_height : int
        height of the screen
    font_size : int
        contains the size of the score font
    all_sprites_list : pygame sprite group
        contains all the sprites in the game
    bird : Bird
        the main player of the game
    clock : Pygame
        to help limit framerate and keep game time consistent
    left_side_wall : Wall
        the left side wall for the bird to bounce off of
    right_side_wall : Wall
        the right side wall for the bird to bounce off of
    walls : Pygame sprite group
        a list of wall sprites for collision detection
    spikes : Pygame sprite group
        a list of spike sprites for collision detection
    WHITE : Tuple int
        contains the RGB color for white
    BLACK : Tuple int
        contains the RGB color for black
    BACKGROUND : Tuple int
        contains the RGB color for the background
    FPS : int
        sets the framerate for pygame to limit framerate

    Methods
    -------
    play():
        Starts the game, contains the main game loop.
    draw():
        Draws the main components for the game.
    update():
        Updates the main game components including position and collision detection.
    create_walls():
        Creates the side walls.
    create_spikes():
        Creates the top and bottom spikes.
    add_bird():
        Adds the bird to the spite group and to the center of the screen.
    """
    # Start the window in the center of the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (200, 200, 200)

    # Screen Information
    display_width = 1080
    display_height = 900
    FPS = 60

    # Font style
    font_size = 36

    # Sprite Groups
    all_sprites_list = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    spikes = pygame.sprite.Group()

    def __init__(self):
        # Init pygame
        pygame.init()

        # Set window title
        pygame.display.set_caption('Afli')

        # Create window and clock
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.clock = pygame.time.Clock()

        # Set font
        self.font = pygame.font.SysFont("courier", self.font_size)

        # Create game components
        self.score = Score(self.display_width, self.display_height, self.font)
        self.create_spikes()
        self.create_walls()
        self.add_bird()

    def add_bird(self):
        '''
        Creates the bird/main player as an attribute of the Game class.
        '''
        # Create the bird
        self.bird = Bird()

        # Position bird in the center of the screen
        self.bird.rect.x = (self.display_width - self.bird.get_width()) / 2
        self.bird.rect.y = (self.display_height / 2) - self.bird.get_height()

        # Add the player to the sprite group
        self.all_sprites_list.add(self.bird)

    def create_walls(self):
        '''
        Creates the two side walls.
        '''
        # Create the walls
        self.left_side_wall = Wall()
        self.right_side_wall = Wall()

        # Position right wall
        self.left_side_wall.rect.x = self.display_width - self.left_side_wall.get_width()
        self.left_side_wall.rect.y = 0

        # Position left wall
        self.right_side_wall.rect.x = 0
        self.right_side_wall.rect.y = 0

        # Add walls to the all sprites group
        self.all_sprites_list.add(self.right_side_wall)
        self.all_sprites_list.add(self.left_side_wall)

        # Add walls to the walls sprite group
        self.walls.add(self.right_side_wall)
        self.walls.add(self.left_side_wall)

    def create_spikes(self):
        '''
        Creates top and bottom spikes.
        '''
        # Create Spikes
        bottom_spike = Spike()
        top_spike = Spike()

        # Position bottom spike
        bottom_spike.rect.x = 0
        bottom_spike.rect.y = self.display_height - bottom_spike.get_height()

        # Position top spike
        top_spike.rect.x = 0
        top_spike.rect.y = 0

        # Flip top spikes
        top_spike.flip()

        # Add spikes to the all sprite group
        self.all_sprites_list.add(top_spike)
        self.all_sprites_list.add(bottom_spike)

        # Add to the spikes group
        self.spikes.add(top_spike)
        self.spikes.add(bottom_spike)

    def play(self):
        '''
        Starts the game, contains the main game loop.
        '''
        while True:
            keys = pygame.key.get_pressed()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_UP]:
                self.bird.jump()
            if keys[pygame.K_SPACE]:
                self.bird.reset(self.display_width, self. display_height)
                self.score.reset()
            self.collision_detection()
            self.update()
            self.draw()

    def collision_detection(self):
        '''
        Checks whether the bird has collided with any other sprite and acts accordingly
        '''
        if self.bird.collide(self.walls):
            self.bird.flip()
            self.score.increment()
        elif self.bird.collide(self.spikes):
            self.bird.alive = False

    def update(self):
        '''
        Updates the main components in the game.
        '''
        self.all_sprites_list.update()

    def draw(self):
        '''
        Draws the main components for the game.
        '''
        # Fill the screen with background color
        self.screen.fill(Game.BACKGROUND)

        # Draw the score
        self.score.draw(self.screen)

        # Draw sprites
        self.all_sprites_list.draw(self.screen)

        # Update display
        pygame.display.update()

if __name__ == "__main__":
    Game().play()
