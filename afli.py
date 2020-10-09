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

    Methods
    -------
    get_height():
        Returns the height of the sprite image.
    get_width():
        Returns the width of the sprite image.
    jump():
        Sets isjump to True and moves sprite for jump
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

    def jump(self):
        '''
        Sets the bird to be currently jumping for the update function.
        '''
        self.isjump = 1

    def update(self):
        '''
        Updates the position of the bird.
        '''
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
    create_spikes():
        Creates the top and bottom spikes.
    add_bird():
        Adds the bird to the spite group and to the center of the screen.
    """
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (200, 200, 200)

    # Screen Information
    display_width = 1080
    display_height = 720
    FPS = 60

    # Font style
    font_size = 36

    # Sprite Groups
    all_sprites_list = pygame.sprite.Group()

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

        # Add spikes to the sprite group
        self.all_sprites_list.add(top_spike)
        self.all_sprites_list.add(bottom_spike)

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
            self.update()
            self.draw()

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
