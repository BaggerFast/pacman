import pygame as pg
import os.path


class Text:
    def __init__(self, text, size, rect=(0, 0), color=(255, 255, 255),
                 font=os.path.join('fonts', 'font0.ttf')):
        pg.font.init()
        self.pos = rect
        self.text = text
        self.size = size
        self.color = color
        self.font = pg.font.Font(font, self.size)
        self.surface = self.font.render(self.text, False, self.color)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, False, self.color)

    def update_position(self, a=()):
        self.pos = a

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

