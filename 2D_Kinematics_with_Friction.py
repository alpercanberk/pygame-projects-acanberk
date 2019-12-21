import pygame
import random
import math

# Initialize the game engine
pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

WIDTH = 500
HEIGHT = 500
# Set the height and width of the screen
SIZE = [WIDTH, HEIGHT]

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Ball Animation")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
# Create an empty array
ball_list = pygame.sprite.Group()


def sign(n):
    if n > 0:
        return -1
    else:
        return 1

def random_color():
    return (random.randrange(0, 244), random.randrange(0, 244), random.randrange(0, 244))

class Ball(pygame.sprite.Sprite):

    def __init__(self, size, x, y, velocity, theta, elasticity, forces, friction_coefficient):

        super().__init__()

        self.size = size
        self.friction_coefficient = friction_coefficient
        self.elasticity = elasticity

        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = HEIGHT - y

        self.v_x = velocity * math.cos(theta)
        self.v_y = -1 * velocity * math.sin(theta)

        self.a_x = 0
        self.a_y = 0

        self.forces = forces

        # Draw the ellipse
        pygame.draw.ellipse(self.image, (random.randrange(0, 244), random.randrange(0, 244), random.randrange(0, 244)),[0, 0, self.size, self.size])

    def apply_force(self, force):
        self.a_x += force[0]
        self.a_y += -1 * force[1]

    def update(self):

        for force in self.forces:
            self.apply_force(force)

        #bogus friction (messes things up when v is too high or too low)
        friction_x = (self.v_x ** 2)*sign(self.v_x)*self.friction_coefficient
        friction_y = (self.v_y ** 2)*sign(self.v_y)*self.friction_coefficient*-1

        #friction_y is multiplied by -1 because y increases as the ball goes down

        self.apply_force([friction_x, friction_y])

        self.v_x += self.a_x
        self.v_y += self.a_y

        self.rect.x += self.v_x
        self.rect.y += self.v_y

        self.a_x = 0
        self.a_y = 0

        self.collision()



    def collision(self):
        if self.rect.x > WIDTH-self.size or self.rect.x < self.size:
            # Reset it just above the top
            self.v_x = -1 * self.v_x * self.elasticity

            if(self.rect.x < self.size):
                self.rect.x = self.size

            if(self.rect.y > WIDTH-self.size):
                self.rect.y = WIDTH-self.size


        if self.rect.y < 0 or self.rect.y > HEIGHT - self.size:

            if(self.rect.y < 0):
                self.rect.y = 0

            if(self.rect.y > HEIGHT - self.size):
                self.rect.y = HEIGHT - self.size

            self.v_y = -1 * self.v_y * self.elasticity


# Loop 50 times and add a ball flake in a random x,y position

clock = pygame.time.Clock()


all_sprite_list = pygame.sprite.Group()

all_sprite_list.add(Ball(x=50,
            y=50,
            size=10,
            velocity=50,
            theta=math.pi/2.5,
            forces=[[0, -0.9]],
            elasticity=.9,
            friction_coefficient=0.01
            ))

# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():   # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True   # Flag that we are done so we exit this loop

    all_sprite_list.draw(screen)
    all_sprite_list.update()

    pygame.display.flip()
    clock.tick(100)


pygame.quit()
