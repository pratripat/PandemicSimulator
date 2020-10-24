import pygame

class Button:
    def __init__(self, x, y, width, height, rectMode=False, color=(255, 255, 255), hoverColor=(255, 255, 0), text='', fontStyle='comicsans', fontSize=20, fontColor=(255, 255, 255)):
        self.defineDimesions(x, y, width, height, rectMode)
        self.defineText(color, hoverColor, text, fontStyle, fontSize, fontColor)
        self.clicked = False

    def defineDimesions(self, x, y, width, height, rectMode):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if rectMode:
            self.x -= self.width//2
            self.y -= self.height//2

    def defineText(self, color, hoverColor, text, fontStyle, fontSize, fontColor):
        self.color = color
        self.prevColor = self.color
        self.hoverColor = hoverColor
        self.text = text
        self.fontStyle = fontStyle
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.SysFont(self.fontStyle, self.fontSize)

    def showText(self, surface):
        label = self.font.render(self.text, 1, self.fontColor)

        cx = (self.x + self.width//2) - label.get_width()//2
        cy = (self.y + self.height//2) - label.get_height()//2

        surface.blit(label, (cx, cy))

    def show(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        self.showText(surface)

    def hover(self):
        pos = pygame.mouse.get_pos()
        x, y = pos

        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            self.color = self.hoverColor
            return True

        self.color = self.prevColor
        return False

    def isClicked(self, clicked):
        return self.hover() and clicked

    def shiftColor(self):
        hoverColor = self.hoverColor

        self.hoverColor = self.prevColor
        self.prevColor = hoverColor
