"""
A module that allows a genius bird to play a famous mobile game (Don't Touch The Spikes)

Author
----------
Adam Skudlarek

Classes
----------
Game:
    Maintains the game loop for the running of the game
Score:
    Maintains the score of the game.
Wall:
    The walls for the bird to bounce off of.
WallSpike:
    The spikes on the side walls for the player to dodge.
Spike:
    The top and bottom static spikes.
Bird:
    The bird or main player of the game.

"""
import sys
import os
import random
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
    isjump : int
        is the bird currently jumping; 1 = True, 0 = False
    alive : bool
        determines whether or not the bird is alive still
    MASS : int
        the mass of the bird to calculate force
    VEL : int
        the default velocity of the bird

    Methods
    -------
    get_height():
        Returns the height of the sprite image.
    get_width():
        Returns the width of the sprite image.
    collide(pygame:sprite_group)
        Returns whether or not bird has collided with sprite in sprite_group.
    flip():
        Flips the birds direction.
    jump():
        Sets isjump to True and moves sprite for jump.
    died():
        Sets the bird to be dead.
    reset(display_width:int, display_height:int):
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

    # Static bird mechanics
    VEL = 8
    MASS = 2

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

                Parameters:
                        sprite_group (pygame:sprit_group): The group to check against the object
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

                Parameters:
                        display_width (int): The width of the game screen
                        display_height (int): The height of the game screen
        '''
        # Set bird to be alive
        self.alive = True

        # Position bird in the center of the screen
        self.rect.x = (display_width - self.get_width()) / 2
        self.rect.y = (display_height / 2) - self.get_height()

        # Reset direction
        if self.x_speed < 0:
            self.flip()

        # Reset the velocity and jump
        self.isjump = 0
        self.velocity = self.VEL

    def update(self):
        '''
        Updates the position of the bird.
        '''
        if self.alive:
            # Update horizontal movement
            self.rect.x += self.x_speed

            # Update gravity and falling based on force
            force = self.MASS * self.velocity
            self.rect.y = self.rect.y - force
            self.velocity -= 1

            # Reset upon jumping
            if self.isjump:
                self.velocity = self.VEL
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

class WallSpike(pygame.sprite.Sprite):
    """
    A class to represent the spikes on the side walls.

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
    get_height():
        Returns the height of the sprite image.
    flip():
        Flips the spikes vertically.
    set_spike(x_pos:int, y_pos:int):
        Sets the sprite at the given x and y coordinates.
    reset():
        Resets the spike back to its default state.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load image sprite
        self.image = pygame.image.load('images/wall_spike.png').convert()

        # Set transparency color
        self.image.set_colorkey(Game.WHITE)

        # Start with image flipped for left side
        self.flip()

        # Set rect of the image
        self.rect = self.image.get_rect()

    def get_width(self):
        '''
        Gets the width of the sprites image.

                Returns:
                        a (int): The width of the sprite's image
        '''
        return self.image.get_width()

    def get_height(self):
        '''
        Gets the height of the sprites image.

                Returns:
                        a (int): The height of the sprite's image
        '''
        return self.image.get_height()

    def flip(self):
        '''
        Flips the sprite image vertically.
        '''
        self.image = pygame.transform.flip(self.image, True, False)

    def set_spike(self, x_pos, y_pos):
        '''
        Sets the spike to the given x and y positions.

                Parameters:
                        x_pos (int): The x position for the sprite to be set at
                        y_pos (int): The y position for the sprite to be set at
        '''
        self.rect.x = x_pos
        self.rect.y = y_pos

    def reset(self):
        '''
        Resets the spikes to reset the game.
        '''
        self.__init__()

class Wall(pygame.sprite.Sprite):
    """
    A class to represent the walls confining the player as sprites.

    Attributes
    ----------
    image : pygame image
        image of the sprite
    rect : pygame rect
        rect information (x, y) for sprite
    wall_height : int
        default height of the wall
    wall_width : int
        default width of the wall

    Methods
    -------
    get_width():
        Returns the width of the sprite image.
    """
    # Default wall height and width
    wall_height = 1920
    wall_width = 33

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
                        screen (pygame:surface): A screen to have the score drawn to
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
    top_wall_spike : Wall_Spike
        the top side of the wall spikes.
    bottom_wall_spike : Wall_Spike
        the bottom side of the wall spikes.
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
    collision_detection():
        Checks whether the bird has collided with any other sprite and acts accordingly.
    reset():
        Resets the entire game back to default state to restart game.
    spike_change():
        Randomize wall spikes and the opening for the player to go through.
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
        Creates top, bottom and side spikes.
        '''
        # Create top and bottom spikes
        self.bottom_spike = Spike()
        self.top_spike = Spike()

        # Create side spikes
        self.top_wall_spike = WallSpike()
        self.bottom_wall_spike = WallSpike()

        # Position bottom spike
        self.bottom_spike.rect.x = 0
        self.bottom_spike.rect.y = self.display_height - self.bottom_spike.get_height()

        # Position top spike
        self.top_spike.rect.x = 0
        self.top_spike.rect.y = 0

        # Flip top spikes
        self.top_spike.flip()

        # Add spikes to the all sprite group
        self.all_sprites_list.add(self.top_spike)
        self.all_sprites_list.add(self.bottom_spike)
        self.all_sprites_list.add(self.top_wall_spike)
        self.all_sprites_list.add(self.bottom_wall_spike)

        # Add to the spikes group
        self.spikes.add(self.top_spike)
        self.spikes.add(self.bottom_spike)
        self.spikes.add(self.top_wall_spike)
        self.spikes.add(self.bottom_wall_spike)

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
                self.reset()
            self.collision_detection()
            self.update()
            self.draw()

    def reset(self):
        '''
        Resets the entire game back to default state to restart game.
        '''
        self.bottom_wall_spike.reset()
        self.top_wall_spike.reset()
        self.bird.reset(self.display_width, self.display_height)
        self.score.reset()

    def spike_change(self):
        '''
        Randomize wall spikes and the opening for the player to go through.
        '''
        # Set the minimum size of the gap to be twice the size of the bird
        gap_min = self.bird.get_height() * 2

        # Set the gap to decrease when score increases
        gap = (self.display_height / 2) - (self.score.score * 10)

        # Check that gap isn't below minimum
        if gap < gap_min:
            gap = gap_min

        # Set the constraints for the random y coordinate
        a_range_constraint = self.top_spike.get_height() * 2
        b_range_constraint = (self.display_height - gap) - a_range_constraint

        # Randomize the y coordinate given the constraints
        random_y = random.randint(a_range_constraint, b_range_constraint)

        # Get the new y coordinates for both the top and bottom wall spikes
        top_y = (0 - self.top_wall_spike.get_height()) + random_y
        bottom_y = random_y + gap

        # Get the x coordinate for spikes on right side
        x_pos = self.display_width - self.top_wall_spike.get_width()

        # Determine which side of the spikes need to be on
        if self.bird.x_speed < 0:
            self.top_wall_spike.set_spike(x_pos, top_y)
            self.bottom_wall_spike.set_spike(x_pos, bottom_y)
        else:
            self.top_wall_spike.set_spike(0, top_y)
            self.bottom_wall_spike.set_spike(0, bottom_y)

        # Flip the image of the spikes if this isn't the first bounce
        if self.score.score > 0:
            self.top_wall_spike.flip()
            self.bottom_wall_spike.flip()

    def collision_detection(self):
        '''
        Checks whether the bird has collided with any other sprite and acts accordingly
        '''
        if self.bird.collide(self.walls):
            self.spike_change()
            self.score.increment()
            self.bird.flip()
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
