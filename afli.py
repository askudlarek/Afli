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

class Game:
    """
    A class to represent the game Don't Touch The Spikes and allow an AI to play that game.

    Attributes
    ----------
    screen : pygame
        the screen for the game
    BACKGROUND : RGB int
        contains the RGB color for the background
    display_width : int
        width of the screen
    display_height : int
        height of the screen

    Methods
    -------
    play():
        Starts the game, contains the main game loop.
    draw():
        Draws the main components for the game.
    """
    BACKGROUND = (200, 200, 200)
    display_width = 1080
    display_height = 720

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])

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
        pygame.display.update()

if __name__ == "__main__":
    Game().play()
