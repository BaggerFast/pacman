from pygame import Rect
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.misc import is_esc_pressed
from pacman.objects import Btn, ButtonController, Text
from pacman.objects.buttons import BTN_GREEN_COLORS, BTN_RED_COLORS
from pacman.sound import SoundController
from pacman.storage import SettingsStorage

from .base import BaseScene, SceneManager


class SettingsScene(BaseScene):
    class SettingButton(Btn):
        def __init__(self, name, i, var):
            flag_var = getattr(SettingsStorage(), var)
            super().__init__(
                rect=Rect(0, 0, 180, 35),
                text=name + (" ON" if flag_var else " OFF"),
                text_size=FontCfg.BUTTON_TEXT_SIZE,
                colors=BTN_GREEN_COLORS if flag_var else BTN_RED_COLORS,
            )
            self.move_center(Cfg.RESOLUTION.h_width, 75 + i * 40)
            self.name = name
            self.var = var

        def click(self):
            flag_var = not getattr(SettingsStorage(), self.var)
            setattr(SettingsStorage(), self.var, flag_var)
            event_append(EvenType.UPDATE_SOUND)
            if flag_var:
                self.text = self.name + " ON"
                self.colors = BTN_GREEN_COLORS
            else:
                self.text = self.name + " OFF"
                self.colors = BTN_RED_COLORS
            SoundController().CLICK.play()

    __volume_position = 150
    __difficulty_pos = 210
    __dificulties = {0: "easy", 1: "medium", 2: "hard"}

    def _create_objects(self) -> None:
        self.difficult_button = Btn(
            rect=Rect(0, 0, 120, 35),
            function=self.click_difficult,
            text_size=FontCfg.BUTTON_TEXT_SIZE,
            text=self.__dificulties[SettingsStorage().difficulty],
        ).move_center(Cfg.RESOLUTION.h_width, self.__difficulty_pos)
        self.create_buttons()
        self.volume_value = Text(f"{SettingsStorage().volume}%", 20).move_center(
            Cfg.RESOLUTION.h_width,
            self.__volume_position + 30,
        )
        self.objects += [
            Text("SETTINGS", 30, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30),
            Text("VOLUME", 20).move_center(Cfg.RESOLUTION.h_width, self.__volume_position),
            self.volume_value,
        ]

    def click_sound(self, step):
        SettingsStorage().set_volume(SettingsStorage().volume + step)
        self.volume_value.text = f"{SettingsStorage().volume}%"

    def click_difficult(self) -> None:
        SettingsStorage().difficulty = (SettingsStorage().difficulty + 1) % len(self.__dificulties)
        self.difficult_button.text = self.__dificulties[SettingsStorage().difficulty]

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "mute"),
            ("FUN", "fun"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(names[i][0], i, names[i][1]))

        self.buttons += [
            Btn(
                rect=Rect(0, 0, 40, 35),
                text="-",
                function=lambda: self.click_sound(-5),
            ).move_center(Cfg.RESOLUTION.h_width - 60, self.__volume_position + 30),
            Btn(
                rect=Rect(0, 0, 40, 35),
                text="+",
                function=lambda: self.click_sound(5),
            ).move_center(Cfg.RESOLUTION.h_width + 65, self.__volume_position + 30),
            self.difficult_button,
            Btn(
                rect=Rect(0, 0, 180, 40),
                text="BACK",
                function=SceneManager().pop,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.h_width, 250),
        ]
        self.objects.append(ButtonController(self.buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()