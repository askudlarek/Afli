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
    WHITE : Tuple int
        contains the RGB color for white
    BLACK : Tuple int
        contains the RGB color for black
    BACKGROUND : Tuple int
        contains the RGB color for the background

    Methods
    -------
    play():
        Starts the game, contains the main game loop.
    draw():
        Draws the main components for the game.
    create_spikes():
        Creates the top and bottom spikes.
    """
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (200, 200, 200)

    # Screen Information
    display_width = 1080
    display_height = 720

    # Font style
    font_size = 36

    # Sprite Groups
    all_sprites_list = pygame.sprite.Group()

    def __init__(self):
        # Init pygame
        pygame.init()

        # Set window title
        pygame.display.set_caption('Afli')

        # Create window
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])

        # Set font
        self.font = pygame.font.SysFont("courier", self.font_size)

        # Create game components
        self.score = Score(self.display_width, self.display_height, self.font)
        self.create_spikes()

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw()

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
