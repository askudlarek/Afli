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
    WHITE : Tuple int
        contains the RGB color for white
    BACKGROUND : Tuple int
        contains the RGB color for the background

    Methods
    -------
    play():
        Starts the game, contains the main game loop.
    draw():
        Draws the main components for the game.
    """
    WHITE = (255, 255, 255)
    BACKGROUND = (200, 200, 200)
    display_width = 1080
    display_height = 720
    font_size = 36

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.font = pygame.font.SysFont("courier", self.font_size)
        self.score = Score(self.display_width, self.display_height, self.font)

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
        self.screen.fill(Game.BACKGROUND)
        self.score.draw(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    Game().play()
