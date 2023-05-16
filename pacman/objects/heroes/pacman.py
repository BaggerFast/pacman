import pygame as pg

from pacman.data_core.interfaces import IEventful
from pacman.misc.cell_util import CellUtil
from pacman.objects.heroes.character_base import Character


class Pacman(Character, IEventful):
    action = {pg.K_w: "up", pg.K_a: "left", pg.K_s: "down", pg.K_d: "right"}

    def __init__(self, game, loader) -> None:
        self.game = game
        self.__walk_anim = game.skins.current.walk
        self.__dead_anim = game.skins.current.dead
        super().__init__(self.__walk_anim, loader, f"pacman/{game.skins.current.name}/aura")
        self.is_dead = False
        self.__feature_rotate = "none"
        self.__ai_timer = 0
        self.animator.stop()

    @property
    def dead_anim(self):
        return self.__dead_anim

    def event_handler(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in self.action.keys() and not self.is_dead:
            self.go()
            self.__feature_rotate = self.action[event.key]

    def update(self) -> None:
        self.animator.update()
        if not self.is_dead:
            if CellUtil.in_cell_center(self.rect):
                if self.can_rotate_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                    self.animator.set_cur_image(0)
                c = self.direction[self.__feature_rotate][2]
                if self.can_rotate_to(c):
                    self.set_direction(self.__feature_rotate)
            super().update()

    def death(self) -> None:
        self.__ai_timer = pg.time.get_ticks()
        self.animator = self.__dead_anim
        self.game.sounds.siren.pause()
        self.game.sounds.pellet.stop()
        self.game.sounds.pacman.play()
        self.animator.start()
        self.is_dead = True

    def death_is_finished(self) -> bool:
        return pg.time.get_ticks() - self.__ai_timer >= 2500 and self.animator.is_finished and self.is_dead
