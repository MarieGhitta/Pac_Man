"""Animated sprite classes for Pac-Man, ghosts, and super-pacgums."""


from abc import ABC, abstractmethod

import pygame

from src.utils.color import Color
from src.utils.sprite_enums import (
        SpriteState, GhostState, PacmanState, Direction
)


class Sprite(ABC):
    """Abstract base class for tile-based animated sprites."""

    def __init__(self, tile_size: int) -> None:
        """Initialize the sprite animation state.

        Args:
            tile_size: Size in pixels of a single tile.
        """
        self.tile_size = tile_size
        self.anim_tick: int = 0
        self.last_anim_update: int = 0
        self.anim_speed: int = 0
        self.anim_count: int = 0
        self.anim_stop: bool = False
        self._last_variant: tuple[
            Direction | None, SpriteState | None
        ] = (None, None)
        self._one_shot_variants: set[
            tuple[Direction | None, SpriteState]
        ] = set()
        self.frames: dict[
            tuple[Direction | None, SpriteState | None],
            list[pygame.surface.Surface]
        ] = {}
        self._build_frames()

    @abstractmethod
    def _build_frames(self) -> None:
        """Build and populate the frames dictionary."""

    def update(
        self,
        current_time: int,
        variant: tuple[Direction | None, SpriteState | None]
    ) -> None:
        """Advance the animation tick for the given variant.

        Args:
            current_time: Current time in milliseconds.
            variant: (direction, state) key identifying the animation.
        """
        if variant != self._last_variant:
            self.anim_tick = 0
            self._last_variant = variant
            self.anim_stop = False
            self.last_anim_update = current_time
        if not self.frames[variant] or self.anim_stop:
            return
        if current_time - self.last_anim_update >= self.anim_speed:
            if self.anim_tick < len(self.frames[variant]) - 1:
                self.anim_tick = (
                    (self.anim_tick + 1) % len(self.frames[variant])
                )
                self.last_anim_update = current_time
            else:
                if variant in self._one_shot_variants:
                    self.anim_stop = True
                else:
                    self.anim_tick = 0
                    self.last_anim_update = current_time

    def draw(
        self,
        surface: pygame.surface.Surface,
        x: int,
        y: int,
        variant: tuple[Direction | None, SpriteState | None]
    ) -> None:
        """Blit the current animation frame onto a surface.

        Args:
            surface: Target surface.
            x: Pixel x-coordinate (top-left).
            y: Pixel y-coordinate (top-left).
            variant: (direction, state) key identifying the animation.
        """
        if not self.frames[variant]:
            return
        tick = self.anim_tick % len(self.frames[variant])
        surface.blit(self.frames[variant][tick], (x, y))


class PacmanSprite(Sprite):
    """Animated Pac-Man sprite with directional and death variants."""

    def __init__(self, tile_size: int) -> None:
        """Initialize Pac-Man frames and store the life icon.

        Args:
            tile_size: Size in pixels of a single tile.
        """
        super().__init__(tile_size)
        self.anim_count = 4
        self.anim_speed = 75
        self.life: pygame.surface.Surface = self.frames[
            (Direction.LEFT, PacmanState.ALIVE)
        ][1]

    def _build_frames(self) -> None:
        """Build all directional frames and the one-shot DYING sequence."""
        frames = [self._build_frame(i) for i in range(13)]
        cycle = frames[:3] + [frames[1]]
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
        self.frames[(None, PacmanState.DYING)] = frames[3:]
        self._one_shot_variants.add((None, PacmanState.DYING))

    def _build_frame(self, frame_index: int) -> pygame.surface.Surface:
        """Render a single Pac-Man pixel-art frame scaled to tile_size.

        Args:
            frame_index: Index into the frame grid list.

        Returns:
            Scaled SRCALPHA surface for this frame.
        """
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
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00011000000000011000",
                "00011100000000111000",
                "00011110000001111000",
                "00011111000011111000",
                "00011111100111111000",
                "00011111111111111000",
                "00001111111111110000",
                "00001111111111110000",
                "00000111111111100000",
                "00000001111110000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00001000000000010000",
                "00111100000000111100",
                "00111110000001111100",
                "00111111000011111100",
                "00111111100111111100",
                "00011111111111111000",
                "00011111111111111000",
                "00001111111111110000",
                "00000011100111000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00111100000000111100",
                "00111100000000111100",
                "00111111000011111100",
                "00011111111111111000",
                "00011111111111111000",
                "00001111111111110000",
                "00000011100111000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00111100000000111100",
                "00011111111111111000",
                "00011111111111111000",
                "00001111111111110000",
                "00000111100111100000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000001111110000000",
                "00011111111111111000",
                "00001111111111110000",
                "00000111100111100000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000001111110000000",
                "00001111100111110000",
                "00000111000011100000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000011000000000",
                "00000000111100000000",
                "00000001111110000000",
                "00000111100111100000",
                "00000011000011000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000011000000000",
                "00000000111100000000",
                "00000000111100000000",
                "00000001100110000000",
                "00000001100110000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000011000000000",
                "00000000011000000000",
                "00000000011000000000",
                "00000000011000000000",
                "00000000011000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000010000001000000",
                "00000010000001000000",
                "00000001100110000000",
                "00011000000000011000",
                "00000110000001100000",
                "00000000000000000000",
                "01111000000000011110",
                "00000000000000000000",
                "00000110000001100000",
                "00011000000000011000",
                "00000000000000000000",
                "00000001100110000000",
                "00000010000001000000",
                "00000010000001000000",
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
                if pixel == "1":
                    surface.set_at((x, y), Color.YELLOW)
        surface = pygame.transform.scale(
            surface, (self.tile_size, self.tile_size)
        )
        return surface


class GhostSprite(Sprite):
    """Animated ghost sprite with per-type color and state variants."""

    def __init__(self, tile_size: int, color: tuple[int, int, int]) -> None:
        """Initialize ghost frames for the given color.

        Args:
            tile_size: Size in pixels of a single tile.
            color: RGB body color for this ghost type.
        """
        self.color = color
        super().__init__(tile_size)
        self.anim_count = 2
        self.anim_speed = 150

    def _build_frames(self) -> None:
        """Build all directional frames."""
        frames = [self._build_frame(i) for i in range(8)]
        side = frames[:2]
        up = frames[2:4]
        down = frames[4:6]
        frightened = frames[6:]
        alt_frames = [
            self._build_frame(i, respawn=True, flicker=True) for i in range(8)
        ]
        alt_side = alt_frames[:2]
        alt_up = alt_frames[2:4]
        alt_down = alt_frames[4:6]
        alt_frightened = alt_frames[6:]

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
            self.frames[direction, GhostState.FRIGHTENED] = frightened

        self.frames[(Direction.RIGHT, GhostState.RESPAWN)] = alt_side
        self.frames[(Direction.LEFT, GhostState.RESPAWN)] = [
            pygame.transform.flip(f, True, False) for f in alt_side
        ]
        self.frames[(Direction.UP, GhostState.RESPAWN)] = alt_up
        self.frames[(Direction.DOWN, GhostState.RESPAWN)] = alt_down

        for direction in [
            Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN
        ]:
            self.frames[direction, GhostState.FLICKER] = alt_frightened

    def _build_frame(
        self, frame_index: int, respawn: bool = False, flicker: bool = False
    ) -> pygame.surface.Surface:
        """Render a single ghost pixel-art frame scaled to tile_size.

        Args:
            frame_index: Index into the frame grid list.
            respawn: If True, omit the body color (eyes-only mode).
            flicker: If True, use FLICKER color palette.

        Returns:
            Scaled SRCALPHA surface for this frame.
        """
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
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000444400000000",
                "00000044444444000000",
                "00000444444444400000",
                "00004444444444440000",
                "00004444444444440000",
                "00004445544554440000",
                "00044445544554444000",
                "00044444444444444000",
                "00044444444444444000",
                "00044554455445544000",
                "00045445544554454000",
                "00044444444444444000",
                "00044044444444044000",
                "00040004400440004000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
            ],
            [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000444400000000",
                "00000044444444000000",
                "00000444444444400000",
                "00004444444444440000",
                "00004444444444440000",
                "00004445544554440000",
                "00044445544554444000",
                "00044444444444444000",
                "00044444444444444000",
                "00044554455445544000",
                "00045445544554454000",
                "00044444444444444000",
                "00044440444404444000",
                "00004400044000440000",
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
                        if not respawn:
                            surface.set_at((x, y), self.color)
                    case "2":
                        surface.set_at((x, y), Color.WHITE)
                    case "3":
                        surface.set_at((x, y), Color.BLUE)
                    case "4":
                        if not flicker:
                            surface.set_at((x, y), Color.BLUE)
                        else:
                            surface.set_at((x, y), Color.WHITE)
                    case "5":
                        if not flicker:
                            surface.set_at((x, y), Color.LIGHTPINK)
                        else:
                            surface.set_at((x, y), Color.RED)
        surface = pygame.transform.scale(
            surface, (self.tile_size, self.tile_size)
        )
        return surface


class SuperPacgumSprite(Sprite):
    """Static super-pacgum sprite (blinking handled by the renderer)."""

    def __init__(self, tile_size: int) -> None:
        """Initialize the super-pacgum frame.

        Args:
            tile_size: Size in pixels of a single tile.
        """
        super().__init__(tile_size)

    def _build_frames(self) -> None:
        """Build the single super-pacgum frame."""
        frame = [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000111100000000",
                "00000001111110000000",
                "00000011111111000000",
                "00000011111111000000",
                "00000011111111000000",
                "00000011111111000000",
                "00000001111110000000",
                "00000000111100000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
        ]
        surface = pygame.surface.Surface(
            (len(frame[0]), len(frame[0])), pygame.SRCALPHA
        )
        for y, row in enumerate(frame):
            for x, pixel in enumerate(row):
                if pixel == "1":
                    surface.set_at((x, y), Color.LIGHTPINK)
        surface = pygame.transform.scale(
            surface, (self.tile_size, self.tile_size)
        )
        self.frames[(None, None)] = [surface]
