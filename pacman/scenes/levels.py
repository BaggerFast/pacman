import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg, Colors, KbKeys
from pacman.misc import is_esc_pressed
from pacman.objects import ImgObj, Text
from pacman.objects.buttons import Btn, ButtonController
from pacman.storage import LevelStorage

from ..data_core.config import FontCfg
from .base_scene import BaseScene
from .scene_manager import SceneManager


class LevelsScene(BaseScene):
    def create_buttons(self) -> None:
        buttons = [
            Btn(
                text="",
                rect=self.preview.rect,
                function=SceneManager().pop,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            )
        ]
        self.__button_controller = ButtonController(buttons)
        self.objects.append(self.__button_controller)

    @property
    def current_level(self) -> int:
        return LevelStorage().current

    def _create_objects(self) -> None:
        super()._create_objects()
        self.preview: ImgObj = (
            self.game.maps.images[LevelStorage().current]
            .smoothscale(224 * 0.6, 248 * 0.6)
            .move_center(Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height)
        )
        self.objects.append(self.preview)
        self.objects.append(Text("SELECT LEVEL", 25, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30))

        self.text = Text(f"Level: {self.current_level + 1}/{LevelStorage().level_count}", 20).move_center(
            Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height
        )
        self.text2 = Text(f"L", 40, color=Colors.DARK_GRAY).move_center(
            Cfg.RESOLUTION.WIDTH // 6 - 10, Cfg.RESOLUTION.h_height
        )
        self.text3 = Text(f"R", 40, color=Colors.DARK_GRAY).move_center(
            Cfg.RESOLUTION.WIDTH - (Cfg.RESOLUTION.WIDTH // 6 - 16), Cfg.RESOLUTION.h_height
        )
        if self.current_level == 0:
            self.text2.color = Colors.BLACK
        if self.current_level == LevelStorage().level_count - 1:
            self.text3.color = Colors.BLACK
            self.text = Text(f"Level: {self.current_level + 1}", 20).move_center(
                Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height
            )
        elif self.current_level + 1 >= len(LevelStorage().unlocked):
            self.text3.color = Colors.BLACK

        self.objects.append(self.text)
        self.objects.append(self.text2)
        self.objects.append(self.text3)
        self.create_buttons()

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
        if event.type == pg.KEYDOWN:
            if event.key in KbKeys.RIGHT and self.current_level != LevelStorage().level_count - 1:
                if not (self.current_level + 1 >= len(LevelStorage().unlocked)):
                    LevelStorage().set_next_level()
            elif event.key in KbKeys.LEFT and self.current_level != 0:
                LevelStorage().set_prev_level()
            self.preview: ImgObj = self.game.maps.images[self.current_level]
            self.preview.smoothscale(224 * 0.6, 248 * 0.6)
            self.preview.move_center(Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height)

            self.objects.append(self.preview)

            self.text3.color = Colors.DARK_GRAY
            self.text2.color = Colors.DARK_GRAY
            if self.current_level == 0:
                self.text2.color = Colors.BLACK
            if self.current_level == LevelStorage().level_count - 1:
                self.text3.color = Colors.BLACK
                self.text = Text(f"Level: {self.current_level + 1}", 20).move_center(
                    Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height
                )
            elif self.current_level + 1 >= len(LevelStorage().unlocked):
                self.text3.color = Colors.BLACK
            self.text = Text(f"Level: {self.current_level + 1}/{LevelStorage().level_count}", 20).move_center(
                Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height
            )
            self.objects.append(self.text)
