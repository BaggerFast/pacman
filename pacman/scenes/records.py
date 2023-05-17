from pygame import Rect
from pygame.event import Event

from pacman.data_core import Colors, Config
from pacman.data_core.game_objects import GameObjects
from pacman.misc import Font
from pacman.misc.animator.sprite_sheet import sprite_slice
from pacman.misc.serializers import LevelStorage
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, ImageObject, Text, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class RecordsScene(BaseScene):
    def _create_objects(self) -> None:
        super()._create_objects()
        self.__indicator = Text(f"level {LevelStorage().current + 1}", 12, font=Font.DEFAULT).move_center(
            Config.RESOLUTION.half_width, 55
        )
        self.objects += [
            self.__indicator,
            Text("RECORDS", 32, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
        ]
        self.__error_text = Text("NO RECORDS", 24, color=Colors.RED).move_center(Config.RESOLUTION.half_width, 100)
        self.__create_text_labels()
        self.__create_medals()
        self.create_buttons()

    def create_buttons(self) -> None:
        back_button = Button(
            game=self.game,
            rect=Rect(0, 0, 180, 40),
            text="MENU",
            function=SceneManager().pop,
            text_size=Font.BUTTON_TEXT_SIZE,
        ).move_center(Config.RESOLUTION.half_width, 250)
        self.objects.append(ButtonController([back_button]))

    def __create_text_labels(self) -> None:
        self.medals_text = []
        text_colors = [Colors.GOLD, Colors.SILVER, Colors.BRONZE, Colors.WHITE, Colors.WHITE]
        current_highscores = LevelStorage().current_highscores()
        for i, score in enumerate(current_highscores):
            self.medals_text.append(Text(f"{score}", 25, Rect(60, 60 + 35 * i, 0, 0), text_colors[i]))

    def __create_medals(self) -> None:
        self.__medals = GameObjects()
        medals_sprite = sprite_slice("medals", (16, 16))
        for i, medal in enumerate(medals_sprite):
            self.__medals.append(ImageObject(medal, (16, 60 + 35 * i)).scale(30, 30))

    def draw(self) -> None:
        super().draw()
        current_highscores = LevelStorage().current_highscores()
        if not sum(current_highscores):
            self.__error_text.draw(self._screen)
            return self._screen
        for i in range(len(current_highscores)):
            self.__medals[i].draw(self._screen)
            self.medals_text[i].draw(self._screen)
        return self._screen

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
