"""
A module that allows a genius bird to play a famous mobile game (Don't Touch The Spikes)

Author
----------
Adam Skudlarek

Classes
----------
Game:
    Maintains the game loop for the running of the game
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
from neuralnetwork import NeuralNetwork

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
    brain: NeuralNetwork
        uses inputs to make the decision of to jump or not
    score: int
        the current score of the bird for the brain
    fitness: int
        the fitness of the bird for reproduction
    MASS : int
        the mass of the bird to calculate force
    VEL : int
        the default velocity of the bird

    Methods
    -------
    remove_from_groups():
        Removes the object from all pygame groups it is in.
    get_height():
        Returns the height of the sprite image.
    get_width():
        Returns the width of the sprite image.
    collide(pygame:sprite_group)
        Returns whether or not bird has collided with sprite in sprite_group.
    think(inputs:list)
        Decides if the bird shall jump or not jump based on the given inputs.
    flip():
        Flips the birds direction.
    jump():
        Sets isjump to True and moves sprite for jump.
    died():
        Sets the bird to be dead.
    reset(display_width:int, display_height:int):
        Resets the bird to restart game.
    get_x_pos():
        Returns the birds current x position.
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

    def __init__(self, brain=NeuralNetwork(5, 8, 2)):
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

        # Position bird in the center of the screen
        self.rect.x = int((Game.display_width - self.get_width()) / 2)
        self.rect.y = int((Game.display_height / 2) - self.get_height())

        # Bird is not currently jumping
        self.isjump = 0

        # Set the bird to be alive
        self.alive = True

        # Set the bird brain
        self.brain = brain

        # Set the birds own score and fitness
        self.score = 0
        self.fitness = 0
    
    def remove_from_groups(self):
        '''
        Removes this bird from all pygame groups it is in.
        '''
        self.kill()

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

    def think(self, inputs):
        '''
        Makes the decision to jump or not to jump based on the given inputs.

                Parameters:
                        inputs (list:int): The inputs for the neural network
        '''
        action = self.brain.predict(inputs)
        if action[0] > action[1]:
            self.jump()

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

        # Reset score and fitness
        self.score = 0
    
    def get_x_pos(self):
        '''
        Returns the x position of this bird.

                Returns:
                        rect.x (int): The x position of this bird
        '''
        if self.x_speed > 0:
            return self.rect.x + self.get_width()
        else:
            return self.rect.x

    def update(self):
        '''
        Updates the position of the bird.
        '''
        if self.alive:
            # Update horizontal movement
            self.rect.x += self.x_speed

            # Increase the score
            self.score += 1

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

class Game:
    """
    A class to represent the game Don't Touch The Spikes and allow an AI to play that game.

    Attributes
    ----------
    screen : pygame
        the screen for the game
    font : pygame
        font used for text in the window
    score : int
        holds the score for the current game
    display_width : int
        width of the screen
    display_height : int
        height of the screen
    font_size : int
        contains the size of the score font
    all_sprites_list : pygame sprite group
        contains all the sprites in the game
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
    population: list Bird
        list of birds in the population
    generation: Generation
        the number of generations
    POPULATION_SIZE: int
        the total size of the population
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
    all_birds_dead():
        Checks if every bird in the population is dead.
    next_generation():
        Prepares the next generation of birds.
    generate_new_population():
        Generates a new population based off of the pool selection
    pool_selection():
        Returns a clone of a bird based on their fitness for the next generation.
    normalize_fitness():
        Normalizes the score of every bird into a fitness score for pool selection.
    first_alive_bird():
        Returns the first bird that is still alive in the population.
    calculate_action():
        Determine what each bird in the population should do.
    distance_to_wall(bird:Bird):
        Calculate the distance from the given bird to the wall.
    distance_to_top_spike(bird:Bird):
        Calculate the distance from the given bird to the top spike.
    distance_to_bottom_spike(bird:Bird):
        Calculate the distance from the given bird to the bottom spike.
    distance_to_top_wall_spike(bird:Bird):
        Calculate the distance from the given bird to the top wall spike.
    distance_to_bottom_wall_spike(bird:Bird):
        Calculate the distance from the given bird to the bottom wall spike.
    birds_going_same_direction():
        Checks if all alive birds in the population are going the same direction.
    """
    # Start the window in the center of the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (200, 200, 200)

    # Population Size
    POPULATION_SIZE = 200

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

        # Create population
        self.population = []

        # Create window and clock
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.clock = pygame.time.Clock()

        # Set font
        self.font = pygame.font.SysFont("courier", self.font_size)

        # Populate the population
        self.add_bird()

        # Create game components
        self.score = 0
        self.create_spikes()
        self.create_walls()
        self.generation = 0

    def add_bird(self):
        '''
        Creates the bird/main player as an attribute of the Game class.
        '''
        while len(self.population) < Game.POPULATION_SIZE:
            # Create the bird
            bird = Bird()

            self.population.append(bird)

            # Add the bird to the sprite group
            self.all_sprites_list.add(bird)

    def create_walls(self):
        '''
        Creates the two side walls.
        '''
        # Create the walls
        self.left_side_wall = Wall()
        self.right_side_wall = Wall()

        # Position right wall
        self.right_side_wall.rect.x = self.display_width - self.right_side_wall.get_width()
        self.right_side_wall.rect.y = 0

        # Position left wall
        self.left_side_wall.rect.x = 0
        self.left_side_wall.rect.y = 0

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
        self.top_left_wall_spike = WallSpike()
        self.bottom_left_wall_spike = WallSpike()
        self.top_right_wall_spike = WallSpike()
        self.bottom_right_wall_spike = WallSpike()

        self.top_left_wall_spike.set_spike(0, 0)
        self.bottom_left_wall_spike.set_spike(0, 0)
        self.top_right_wall_spike.flip()
        self.bottom_right_wall_spike.flip()

        self.spike_change()

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
        self.all_sprites_list.add(self.top_left_wall_spike)
        self.all_sprites_list.add(self.top_right_wall_spike)
        self.all_sprites_list.add(self.bottom_left_wall_spike)
        self.all_sprites_list.add(self.bottom_right_wall_spike)

        # Add to the spikes group
        self.spikes.add(self.top_spike)
        self.spikes.add(self.bottom_spike)
        self.spikes.add(self.top_left_wall_spike)
        self.spikes.add(self.top_right_wall_spike)
        self.spikes.add(self.bottom_left_wall_spike)
        self.spikes.add(self.bottom_right_wall_spike)

    def play(self):
        '''
        Starts the game, contains the main game loop.
        '''
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.collision_detection()
            if self.all_birds_dead():
                self.next_generation()
            self.update()
            self.draw()

    def reset(self):
        '''
        Resets the entire game back to default state to restart game.
        '''
        for bird in self.population:
            bird.reset(self.display_width, self.display_height)
        self.score = 0
        self.spike_change()

    def spike_change(self):
        '''
        Randomize wall spikes and the opening for the player to go through.
        '''
        # Set the minimum size of the gap to be twice the size of the bird
        gap_min = self.population[0].get_height() * 2.5

        # Set the gap to decrease when score increases
        gap = (self.display_height / 2) - (self.score * 10)

        # Check that gap isn't below minimum
        if gap < gap_min:
            gap = gap_min

        # Set the constraints for the random y coordinate
        a_range_constraint = int(self.top_spike.get_height() * 2)
        b_range_constraint = int((self.display_height - gap) - a_range_constraint)

        # Randomize the y coordinate given the constraints
        random_y = random.randint(a_range_constraint, b_range_constraint)

        # Get the new y coordinates for both the top and bottom wall spikes
        top_y = (0 - self.top_left_wall_spike.get_height()) + random_y
        bottom_y = random_y + gap

        # Get the x coordinate for spikes on right side
        x_pos = self.display_width - self.top_left_wall_spike.get_width()

        # Width of the spikes to hide the spikes after bounces
        spike_width = self.top_left_wall_spike.get_width() * -1

        if not self.all_birds_dead():
            if self.first_alive_bird().x_speed > 0:
                # Set position of spikes birds are going towards
                self.top_right_wall_spike.set_spike(x_pos, top_y)
                self.bottom_right_wall_spike.set_spike(x_pos, bottom_y)
                # Set the position of the spikes birds are leaving from
                self.top_left_wall_spike.set_spike(spike_width, top_y)
                self.bottom_left_wall_spike.set_spike(spike_width, bottom_y)
            else:
                # Set position of spikes birds are going towards
                self.top_left_wall_spike.set_spike(0, top_y)
                self.bottom_left_wall_spike.set_spike(0, bottom_y)
                # Set the position of the spikes birds are leaving from
                self.top_right_wall_spike.set_spike(x_pos + self.top_right_wall_spike.get_width(), top_y)
                self.bottom_right_wall_spike.set_spike(x_pos + self.bottom_right_wall_spike.get_width(), bottom_y)


    def all_birds_dead(self):
        '''
        Checks if all birds are dead.

                Returns:
                        a (bool): Whether or not the bird is dead
        '''
        for bird in self.population:
            if bird.alive:
                return False
        return True

    def next_generation(self):
        '''
        Prepares the next generation of birds.
        '''
        self.normalize_fitness()
        self.reset()
        self.generate_new_population()
        self.generation += 1

    def generate_new_population(self):
        '''
        Generates a new population based off of the best bird according to the pool selection.
        '''
        # Create a new population
        new_pop = []
        # For every bird in the previous population select ones for new pop
        for bird in self.population:
            new_bird = self.pool_selection()
            new_pop.append(new_bird)

        # Remove all of the previous birds from their groups
        for bird in self.population:
            bird.remove_from_groups()

        # Add the new population of birds to their respective groups
        for bird in new_pop:
            self.all_sprites_list.add(bird)

        self.population = new_pop

    def pool_selection(self):
        '''
        Selects birds based off of fitness.

                Returns:
                        bird (Bird): Bird with a new brain
        '''
        # Pick a random number between 0 and 1
        random_num = random.random()
        index = 0
        # Continue to subtract from that number based on the normalized fitness of birds
        while random_num > 0:
            random_num -= self.population[index].fitness
            index += 1
        index -= 1

        # When the bird has a fitness that exceeds the random number return a clone
        new_brain = self.population[index].brain.copy()
        new_brain.mutate()
        return Bird(new_brain)

    def normalize_fitness(self):
        '''
        Normalizes the fitness data for pool selection.
        '''
        # Expand the birds score to increase standard deviation
        for bird in self.population:
            bird.score = pow(bird.score, 2)
        total_sum = 0

        # Take the total sum of the birds scores and normalize the data as fitness
        for bird in self.population:
            total_sum += bird.score
        for bird in self.population:
            bird.fitness = bird.score / total_sum
    
    def first_alive_bird(self):
        '''
        Retrieves the first bird that is alive.

                Returns:
                        bird (Bird): Bird that is alive still in the population
        '''
        for bird in self.population:
            if bird.alive:
                return bird
        return self.population[0]

    def calculate_action(self):
        '''
        Determine what each bird in the population should do.
        '''
        for bird in self.population:
            inputs = []
            inputs.append(self.distance_to_wall(bird))
            inputs.append(self.distance_to_top_spike(bird))
            inputs.append(self.distance_to_bottom_spike(bird))
            inputs.append(self.distance_to_top_wall_spike(bird))
            inputs.append(self.distance_to_bottom_wall_spike(bird))
            bird.think(inputs)

    def distance_to_wall(self, bird):
        '''
        Returns the distance from the given bird to the wall.

                Parameters:
                        bird (Bird): Bird to calculate how far from wall
                Returns:
                        x (int): The distance from the wall the bird is
        '''
        if bird.x_speed > 0:
            return self.right_side_wall.rect.x - bird.get_x_pos()
        else:
            distance = self.left_side_wall.rect.x + self.left_side_wall.get_width()
            return bird.get_x_pos() - distance
    
    def distance_to_top_spike(self, bird):
        '''
        Returns the distance from the given bird to the top spike.

                Parameters:
                        bird (Bird): Bird to calculate how far from top spike
                Returns:
                        x (int): The distance from the top spike the bird is
        '''
        return bird.rect.y - self.top_spike.get_height()

    def distance_to_bottom_spike(self, bird):
        '''
        Returns the distance from the given bird to the bottom spike.

                Parameters:
                        bird (Bird): Bird to calculate how far from bottom spike
                Returns:
                        x (int): The distance from the bottom spike the bird is
        '''
        bird_y = bird.rect.y + bird.get_height()
        return self.bottom_spike.rect.y - bird_y
    
    def distance_to_top_wall_spike(self, bird):
        '''
        Returns the distance from the given bird to the top wall spike.

                Parameters:
                        bird (Bird): Bird to calculate how far from top wall spike
                Returns:
                        x (int): The distance from the top wall spike the bird is
        '''
        if bird.x_speed > 0:
            y_of_spike = self.top_right_wall_spike.rect.y + self.top_right_wall_spike.get_height()
            return bird.rect.y - y_of_spike
        else:
            y_of_spike = self.top_left_wall_spike.rect.y + self.top_left_wall_spike.get_height()
            return bird.rect.y - y_of_spike
    
    def distance_to_bottom_wall_spike(self, bird):
        '''
        Returns the distance from the given bird to the bottom wall spike.

                Parameters:
                        bird (Bird): Bird to calculate how far from bottom wall spike
                Returns:
                        x (int): The distance from the bottom wall spike the bird is
        '''
        if bird.x_speed > 0:
            bird_y = bird.rect.y + bird.get_height()
            return self.bottom_right_wall_spike.rect.y - bird_y
        else:
            bird_y = bird.rect.y + bird.get_height()
            return self.bottom_left_wall_spike.rect.y - bird_y
    
    def birds_going_same_direction(self):
        '''
        Checks if all alive birds in the population are going the same direction.

                Returns:
                        a (bool): If the birds are going in the same direction
        '''
        speed = self.first_alive_bird().x_speed
        for bird in self.population:
            if bird.alive and bird.x_speed != speed:
                return False
        return True

    def collision_detection(self):
        '''
        Checks whether the bird has collided with any other sprite and acts accordingly
        '''
        for bird in self.population:
            if bird.collide(self.walls):
                bird.flip()
                if self.birds_going_same_direction():
                    self.spike_change()
                    self.score += 1
            elif bird.collide(self.spikes):
                bird.alive = False

    def update(self):
        '''
        Updates the main components in the game.
        '''
        self.calculate_action()
        self.all_sprites_list.update()

    def draw(self):
        '''
        Draws the main components for the game.
        '''
        # Fill the screen with background color
        self.screen.fill(Game.BACKGROUND)

        # Draw the score
        score_text = self.font.render(str(self.score), True, Game.WHITE)
        self.screen.blit(score_text, (self.display_width / 2, self.display_height / 4))

        # Draw generation
        gen_text = self.font.render("Generation: " + str(self.generation), True, Game.BLACK)
        self.screen.blit(gen_text, (Game.display_width / 15, Game.display_height / 15))

        # Draw sprites
        self.all_sprites_list.draw(self.screen)

        # Update display
        pygame.display.update()

if __name__ == "__main__":
    Game().play()
