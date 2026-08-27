from abc import ABC, abstractmethod
import math

import pygame

from src.utils.color import Color
from src.utils.sprite_enums import (
        SpriteState, GhostState, PacmanState, Direction
)


class Sprite(ABC):
    def __init__(self, tile_size: int) -> None:
        self.tile_size = tile_size
        self.anim_tick: int = 0
        self.last_anim_update: int = 0
        self.anim_speed: int = 0
        self.anim_count: int = 0
        self.frames: dict[
            tuple[Direction | None, SpriteState],
            list[pygame.surface.Surface]
        ] = {}
        self._build_frames()

    @abstractmethod
    def _build_frames(self) -> None:
        pass

    def update(self, current_time: int) -> None:
        if current_time - self.last_anim_update >= self.anim_speed:
            self.anim_tick = (self.anim_tick + 1) % self.anim_count
            self.last_anim_update = current_time

    def draw(
        self,
        surface: pygame.surface.Surface,
        x: int,
        y: int,
        variant: tuple[Direction | None, SpriteState]
    ) -> None:
        surface.blit(self.frames[variant][self.anim_tick], (x, y))


class PacmanSprite(Sprite):
    def __init__(self, tile_size: int) -> None:
        super().__init__(tile_size)
        self.anim_count = 4
        self.anim_speed = 75

    def _build_frames(self) -> None:
        frames = [self._build_frame(i) for i in range(3)]
        cycle = frames + [frames[1]]
        self.frames[(Direction.RIGHT, PacmanState.ALIVE)] = cycle
        self.frames[(Direction.UP, PacmanState.ALIVE)] = [
            pygame.transform.rotate(f, 90) for f in cycle
        ]
        self.frames[(Direction.LEFT, PacmanState.ALIVE)] = [
            pygame.transform.rotate(f, 180) for f in cycle
        ]
        self.frames[(Direction.DOWN, PacmanState.ALIVE)] = [
            pygame.transform.rotate(f, 270) for f in cycle
        ]


    def _build_frame(self, frame_index: int) -> pygame.surface.Surface:
        frames = [
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000001111110000000",
                "00000111111111100000",
                "00001111111111110000",
                "00001111111111110000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00001111111111110000",
                "00001111111111110000",
                "00000111111111100000",
                "00000001111110000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000001111110000000",
                "00000111111111100000",
                "00001111111111110000",
                "00001111111111000000",
                "00011111111000000000",
                "00011111100000000000",
                "00011110000000000000",
                "00011110000000000000",
                "00011111100000000000",
                "00011111111000000000",
                "00001111111111000000",
                "00001111111111110000",
                "00000111111111100000",
                "00000001111110000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000001111110000000",
                "00000111111100000000",
                "00001111111000000000",
                "00001111110000000000",
                "00011111100000000000",
                "00011111000000000000",
                "00011110000000000000",
                "00011110000000000000",
                "00011111000000000000",
                "00011111100000000000",
                "00001111110000000000",
                "00001111111000000000",
                "00000111111100000000",
                "00000001111110000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ]
        ]
        grid = frames[frame_index]
        surface = pygame.surface.Surface(
            (len(grid[0]), len(grid[0])), pygame.SRCALPHA
        )
        for y, row in enumerate(grid):
            for x, pixel in enumerate(row):
                if pixel == "1":
                    surface.set_at((x, y), Color.YELLOW)
        surface = pygame.transform.scale(
            surface, (self.tile_size, self.tile_size)
        )
        return surface

class GhostSprite(Sprite):
    def __init__(self, tile_size: int, color: tuple[int, int, int]) -> None:
        self.color = color
        super().__init__(tile_size)
        self.anim_count = 2
        self.anim_speed = 75

    def _build_frames(self) -> None:
        frames = [self._build_frame(i) for i in range(6)]
        side = frames[:2]
        up = frames[2:4]
        down = frames[4:]
        self.frames[(Direction.RIGHT, GhostState.CHASE)] = side
        self.frames[(Direction.LEFT, GhostState.CHASE)] = [
            pygame.transform.flip(f, True, False) for f in side
        ]
        self.frames[(Direction.UP, GhostState.CHASE)] = up
        self.frames[(Direction.DOWN, GhostState.CHASE)] = down
        for direction in [
            Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN
        ]:
            self.frames[(direction, GhostState.SCATTER)] = self.frames[
                (direction, GhostState.CHASE)
            ]

    def _build_frame(self, frame_index: int) -> pygame.surface.Surface:
        frames = [
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000011111111000000",
                "00000111111111100000",
                "00001112211112210000",
                "00001122221122220000",
                "00001122331122330000",
                "00011122331122331000",
                "00011112211112211000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011011111111011000",
                "00010001100110001000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000011111111000000",
                "00000111111111100000",
                "00001112211112210000",
                "00001122221122220000",
                "00001122331122330000",
                "00011122331122331000",
                "00011112211112211000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011110111101111000",
                "00001100011000110000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000033111133000000",
                "00000233211233200000",
                "00001222211222210000",
                "00001222211222210000",
                "00001122111122110000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011011111111011000",
                "00010001100110001000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000033111133000000",
                "00000233211233200000",
                "00001222211222210000",
                "00001222211222210000",
                "00001122111122110000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011110111101111000",
                "00001100011000110000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000011111111000000",
                "00000111111111100000",
                "00001111111111110000",
                "00001122111122110000",
                "00001222211222210000",
                "00011222211222211000",
                "00011233211233211000",
                "00011133111133111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011011111111011000",
                "00010001100110001000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000011111111000000",
                "00000111111111100000",
                "00001111111111110000",
                "00001122111122110000",
                "00001222211222210000",
                "00011222211222211000",
                "00011233211233211000",
                "00011133111133111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011111111111111000",
                "00011110111101111000",
                "00001100011000110000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],

        ]
        grid = frames[frame_index]
        surface = pygame.surface.Surface(
            (len(grid[0]), len(grid[0])), pygame.SRCALPHA
        )
        for y, row in enumerate(grid):
            for x, pixel in enumerate(row):
                match pixel:
                    case "1":
                        surface.set_at((x, y), self.color)
                    case "2":
                        surface.set_at((x, y), Color.WHITE)
                    case "3":
                        surface.set_at((x, y), Color.BLUE)
        surface = pygame.transform.scale(
            surface, (self.tile_size, self.tile_size)
        )
        return surface

