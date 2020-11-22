import sys

import pygame

from objects.button import ButtonController, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color
from scenes.levels import LevelsScene


class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()

    def create_title(self) -> None:
        title = Text(self.game, 'Pacman', 40, color=Color.WHITE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.start_game, 'PLAY',
                   center=(self.game.width // 2, 100)),

            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.start_records, 'RECORDS',
                   center=(self.game.width // 2, 163)),

            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   sys.exit, 'EXIT',
                   center=(self.game.width // 2, 226))
        ]
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def start_game(self) -> None:
        self.game.set_scene(self.game.SCENE_GAME)

    def start_records(self) -> None:
        self.game.set_scene(self.game.SCENE_RECORDS)
