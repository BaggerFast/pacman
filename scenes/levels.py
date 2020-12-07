from copy import copy

import pygame as pg

from misc import Font
from objects import ButtonController, Text, ImageObject
from objects.button import Button
from scenes import base


class Scene(base.Scene):
    class LvlButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self):
            self.game.maps.cur_id = self.value[0]
            self.game.records.update_records()
            self.game.scenes.set(self.game.scenes.MENU, reset=True)

        def select(self) -> None:
            self.game.scenes.current.is_current = True
            self.game.scenes.current.preview.image = self.value[1].image

            super().select()

        def deselect(self) -> None:
            if not self.game.scenes.current.is_current:
                self.game.scenes.current.preview.image = self.game.maps.images[self.game.maps.cur_id].image

            super().deselect()

    __buttons_on_scene = 4

    def process_event(self, event: pg.event.Event) -> None:
        self.is_current = False
        super().process_event(event)

    def create_static_objects(self):
        self.is_current = False
        self.__scroll = self.game.maps.cur_id
        self.__scroll = min(self.__scroll, self.game.maps.count - self.__buttons_on_scene)
        self.__scroll = max(self.__scroll, 0)
        self.__create_title()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def create_buttons(self) -> None:
        buttons = []
        counter = 0
        for i in range(self.__scroll, self.__scroll + self.__buttons_on_scene):
            buttons.append(
                self.LvlButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 100, 40),
                    value=(i, self.game.maps.images[i]),
                    text='LEVEL' + str(i + 1),
                    center=(self.game.width // 2 - 55, (85 + 40 * counter)),
                    text_size=Font.BUTTON_TEXT_SIZE-4,
                    active=i in self.game.unlocked_levels)
            )
            counter += 1
        buttons.append(self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=(self.game.scenes.MENU, False),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE))

        for index in range(len(buttons)):
            if str(self.game.maps.cur_id + 1) == buttons[index].text[-1:] \
                or str(self.game.maps.cur_id + 1) == buttons[index].text[-2:]:
                buttons[index].text = '-' + buttons[index].text + '-'

        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def unlocked(self) -> int:
        return len(self.game.unlocked_levels)

    def create_objects(self) -> None:
        self.objects = []
        self.preview = copy(self.game.maps.images[self.game.maps.cur_id])
        self.objects.append(self.preview)
        self.create_buttons()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)
        elif event.type == pg.MOUSEWHEEL:
            self.__scroll -= event.y
            self.__scroll = min(self.__scroll, self.game.maps.count - self.__buttons_on_scene)
            self.__scroll = max(self.__scroll, 0)
            self.create_objects()
