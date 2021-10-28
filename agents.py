import pygame
import random
import math

# initialise screen details + colours
WIDTH      = 1000
HEIGHT     = 1000
FPS        = 30
SPEED      = 5
PIXEL_SIZE = 5

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
BLUE  = (0,   0,   255)
GREEN = (0,   255, 0)


# initialise agent (each dot on the screen)
class Agent():
    def __init__(self, ID):
        self.ID = ID
        self.speed = 5
        self.x = 0
        self.y = 0
        self.angle = 0 # in radians
        self.rect = pygame.Rect(
            self.x, self.y, PIXEL_SIZE, PIXEL_SIZE
        )

    def __str__(self):
        return "Agent(ID=%d)" % self.ID

    def set_position(self, x, y):
        self.rect.center = (x, y)

    def set_angle(self, angle):
        self.angle = angle
        self.dx = math.cos(self.angle)*self.speed 
        self.dy = math.sin(self.angle)*self.speed 

    def update(self):
        # move the partile in dx dy direction
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)

        # make sure the particle does not go off screen
        if self.rect.left < 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top < 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class AgentManager:
    def __init__(self):
        self.agents = []

    def __len__(self):
            return len(self.agents)

    def populate(self, n_agents):
        for i in range(n_agents):
            self.agents.append(Agent(len(self)))

    # assign a random location and direction to the created sprites
    def randomize(self):
        for agent in self.agents:
            # this will a random degree and convert it to radians
            agent.set_angle((random.random() * 360)*(math.pi/180))
            agent.set_position(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT))

    def update(self):
        for agent in self.agents:
            agent.update()

    def draw(self, screen):
        for agent in self.agents:
            agent.draw(screen)

    def __iter__(self):
        return iter(self.agents)

if __name__ == "__main__":
    agent_manager = AgentManager()
    agent_manager.populate(100)
    agent_manager.randomize()

    # initialise pygame and make a window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SPRITES")
    clock = pygame.time.Clock()


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        agent_manager.update()

        screen.fill(BLACK)         # clear screen
        agent_manager.draw(screen) # render agents
        pygame.display.flip()      # refresh screen
        clock.tick(FPS)            # wait untill next frame

    pygame.quit()
