import pygame, random

#Setting some colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#Setting the functionalities of the virus and how it will affect a person
virus = {
    'spreadingRadius': 50,
    'catchingSpeed': 50,
    'noSymptomPercentage': 40,
    'maxSurvivalTime': 500
}

class Person:
    def __init__(self, width, height, population, fps, x=False, y=False, sx=0, sy=0, showContact=False):
        #Setting up own things
        self.acc = pygame.math.Vector2()
        self.speed = 2
        self.r = 5
        self.health = 100
        self.immunity = random.randrange(50, 100)
        self.maxspeed = 5
        self.havingVirus = False
        self.havingSymptoms = False
        self.distancing = random.uniform(0, 10/fps)
        self.showContact = showContact

        #Setting up global things
        self.S_X = sx
        self.S_Y = sy
        self.S_WIDTH = width
        self.S_HEIGHT = height
        self.W_FPS = fps
        self.W_PEOPLE_IN_RADIUS = []

        #Calling functions in order to know own pos, vel and things like that
        self.set_pos(x, y, width, height)
        self.set_vel()
        self.set_color()
        self.calculatePeopleInRadius(population)

    def set_pos(self, x, y, width, height):
        #Checking if particular position exists or else setting random position
        if not (x and y):
            x = random.randrange(0, width)
            y = random.randrange(0, height)

        self.pos = pygame.math.Vector2(x, y)

    def set_vel(self):
        #Selecting random velocity
        rand_x = random.randrange(-self.speed, self.speed+1)
        rand_y = random.randrange(-self.speed, self.speed+1)

        self.vel = pygame.math.Vector2(rand_x, rand_y)

        self.limit_speed()

    def limit_speed(self):
        #Limiting the velocity so the person does not go very fast

        #X velocity limiting
        if self.vel.x > self.maxspeed:
            self.vel.x = self.maxspeed
        elif self.vel.x < -self.maxspeed:
            self.vel.x = -self.maxspeed

        #Y velocity limiting
        if self.vel.y > self.maxspeed:
            self.vel.y = self.maxspeed
        elif self.vel.y < -self.maxspeed:
            self.vel.y = -self.maxspeed

    def set_color(self):
        #Changing color according to health state
        self.color = WHITE

        if self.havingVirus and self.havingSymptoms:
            self.color = RED

        if self.havingVirus and not self.havingSymptoms:
            self.color = YELLOW

    def calculatePeopleInRadius(self, population):
        #Checking all the people who are in the virus spreading radius
        self.W_PEOPLE_IN_RADIUS = []

        for person in population:
            if person != self:
                d = self.pos.distance_to(person.pos)

                if d < virus['spreadingRadius']:
                    self.W_PEOPLE_IN_RADIUS.append(person)

    def catch_virus(self):
        self.havingVirus = True

        #Getting a random chance to have no symptoms
        r = random.uniform(0,1)
        self.havingSymptoms = r > (virus['noSymptomPercentage']/100)

    def spread(self):
        speed = virus['catchingSpeed']

        if self.havingVirus:
            for other in self.W_PEOPLE_IN_RADIUS:
                if not other.havingVirus:
                    if other.immunity < speed:
                        #If the person's immunity is not strong, that person will catch the virus
                        other.catch_virus()
                    else:
                        other.reduceImmunity()

    def socialDistancing(self):
        for other in self.W_PEOPLE_IN_RADIUS:
            distancingAcc = self.pos - other.pos
            magnitude = distancingAcc.magnitude()
            if magnitude != 0:
                distancingAcc /= magnitude

            #Vector pointing awat from people in the radius
            self.acc += distancingAcc

    def reduceImmunity(self):
        #If self is in radius of a person affected by the virus,
        #self's immunity reduces showing the virus is growing stronger in oneself
        self.immunity -= random.randrange(5)

        if self.immunity < 0:
            self.immunity = 10

    def reduceHealth(self):
        #Reducing health self is having virus
        if self.havingVirus:
            self.health -= self.W_FPS / virus['maxSurvivalTime']

    def is_dead(self):
        return self.health <= 0

    def show(self, surface):
        self.set_color()

        #Drawing self
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.r)

        if self.showContact:
            #Drawing radius of virus spreading
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), virus['spreadingRadius'], 1)

            #Drawing line from self to people in the radius of virus spreading
            #This is somewhat contact with others
            for other in self.W_PEOPLE_IN_RADIUS:
                pygame.draw.line(surface, BLUE, (int(self.pos.x), int(self.pos.y)), (int(other.pos.x), int(other.pos.y)))

    def move(self, population):
        self.pos += self.vel
        self.set_vel()
        self.vel += self.acc
        self.acc *= 0

        self.calculatePeopleInRadius(population)

    def edges(self):
        #Within the screen width
        if self.pos.x + self.r > self.S_WIDTH:
            self.vel.x *= -1
            self.pos.x = self.S_WIDTH - self.r
        elif self.pos.x - self.r < self.S_X:
            self.vel.x *= -1
            self.pos.x = self.S_X + self.r

        #Within the screen height
        if self.pos.y + self.r > self.S_HEIGHT:
            self.vel.y *= -1
            self.pos.y = self.S_HEIGHT - self.r
        elif self.pos.y - self.r < self.S_Y:
            self.vel.y *= -1
            self.pos.y = self.S_Y + self.r
