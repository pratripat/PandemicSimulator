import pygame
from Person import *
from button import *

width = 800
height = 700
size = (width, height)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pandemic')

global population, isolatedPopulation
population = []
isolatedPopulation = []
FPS = 60

#Area where the population lives
public_area_width = 500
public_area_height = 500

#Area where the isolated people should live
isolation_area_width = 200
isolation_area_height = 200

isolation_x = 0
isolation_y = height - isolation_area_height

def generateNewPopulation(n):
    global population, isolatedPopulation, showingContact

    population = []
    isolatedPopulation = []
    for i in range(n):
        population.append(Person(width=public_area_width, height=public_area_height, population=population, fps=FPS, showContact=showingContact))

    #Getting random person to catch the virus
    r_person = random.choice(population)
    r_person.catch_virus()

#Craeting function to reduce typing same things again for the button
def clickButton(button, clicked, variable):
    if button.isClicked(clicked):
        button.shiftColor()
        return not variable

    return None

def drawBoundaries(surface):
    #Drawing borders where the people will live
    pygame.draw.line(surface, WHITE, (public_area_width, 0), (public_area_width, public_area_height))
    pygame.draw.line(surface, WHITE, (0, public_area_height), (public_area_width, public_area_height))

    #Drawing borders where the isolated people will live
    pygame.draw.rect(surface, WHITE, (isolation_x, isolation_y, isolation_area_width, isolation_area_height), 1)

def update_contact(person):
    global showingContact

    if showingContact:
        person.showContact = True
    else:
        person.showContact = False

def update(surface):
    global population, isolatedPopulation, showingContact
    running = True
    clock = pygame.time.Clock()
    populationCount = 50
    font = pygame.font.SysFont('comicsans', 40)

    #Currently such variables are false
    startSocialDistancing = False
    startIsolation = False
    showingContact = False

    #Creating the button to allow for user interaction
    sdButton = Button(width - 150, 50, 150, 50, text='Social Distancing', color=GREEN if startSocialDistancing else RED, hoverColor=GREEN if not startSocialDistancing else RED, rectMode=True, fontSize=25)
    isoButton = Button(width - 150, 150, 150, 50, text='Isolation', color=GREEN if startIsolation else RED, hoverColor=GREEN if not startIsolation else RED, rectMode=True, fontSize=25)
    newPopulationButton = Button(width - 150, 250, 150, 50, text='New population', color=RED, hoverColor=GREEN, rectMode=True, fontSize=25)
    contactButton = Button(width - 150, 350, 150, 50, text='Show contact', color=RED, hoverColor=GREEN, rectMode=True, fontSize=25)

    #Generating people according to the amount of populationCount variable
    generateNewPopulation(populationCount)

    def display_text():
        offset = 20
        x = isolation_x+isolation_area_width+offset
        y = isolation_y+offset
        label = font.render('Total number of people: ' + str(populationCount), 1, WHITE)
        label2 = font.render('Symptomatic affected people: ' + str(symptomaticPeople), 1, WHITE)
        label3 = font.render('Unsymptomatic affected people: ' + str(unsymptomaticPeople), 1, WHITE)

        surface.blit(label, (x, y))
        y += label.get_height() * 2
        surface.blit(label2, (x, y))
        y += label2.get_height() * 2
        surface.blit(label3, (x, y))

    while running:
        symptomaticPeople = 0
        unsymptomaticPeople = 0
        clock.tick(FPS)

        surface.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            clicked = event.type == pygame.MOUSEBUTTONDOWN

            #Checking for the response from the function, whether the response is a boolean or not
            response = clickButton(sdButton, clicked, startSocialDistancing)
            if response != None:
                startSocialDistancing = response

            response = clickButton(isoButton, clicked, startIsolation)
            if response != None:
                startIsolation = response

            response = clickButton(contactButton, clicked, showingContact)
            if response != None:
                showingContact = response

            response = clickButton(newPopulationButton, clicked, False)
            if response == True:
                population = []
                isolatedPopulation = []

                generateNewPopulation(populationCount)

                newPopulationButton.shiftColor()

        #Showing and running other functionalities for the people
        for person in population[:]:
            #Resetting peoples' showcontact variable to either show contact or not
            update_contact(person)

            person.move(population)
            person.edges()
            person.spread()
            person.reduceHealth()

            #Calling social distancing to avoid catching the virus only if the variable is true
            if startSocialDistancing:
                person.socialDistancing()

            person.show(surface)

            #Checking if the person is no more alive
            if person.is_dead():
                population.remove(person)
            elif person.havingVirus and person.havingSymptoms:
                symptomaticPeople += 1

                if startIsolation:
                    person.S_X = isolation_x
                    person.S_Y = isolation_y
                    person.S_WIDTH = isolation_area_width + isolation_x
                    person.S_HEIGHT = isolation_area_height + isolation_y

                    #Giving false as x, y so it sets it to random position
                    person.set_pos(False, False, person.S_WIDTH, person.S_HEIGHT)

                    isolatedPopulation.append(person)
                    population.remove(person)
            elif person.havingVirus:
                unsymptomaticPeople += 1

        #Showing all the people who are isolated
        for person in isolatedPopulation[:]:
            #Resetting peoples' showcontact variable to either show contact or not
            symptomaticPeople += 1
            update_contact(person)

            person.move(isolatedPopulation)
            person.edges()
            person.spread()
            person.reduceHealth()

            person.show(surface)

            #Checking if the person is no more alive
            if person.is_dead():
                isolatedPopulation.remove(person)

        drawBoundaries(surface)

        #Checking if the mouse is hovering over the buttons
        sdButton.hover()
        isoButton.hover()
        newPopulationButton.hover()
        contactButton.hover()

        #Showing the buttons
        sdButton.show(surface)
        isoButton.show(surface)
        newPopulationButton.show(surface)
        contactButton.show(surface)

        display_text()

        pygame.display.update()

update(screen)
