import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class HighscoreScreen(Screen):
    def __init__(
        self,
        surface: pygame.surface.Surface,
        scores: list[dict[str, str | int]]
    ) -> None:
        super().__init__(surface)
        self.scores = scores

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_screen = "title"

    def update(self, current_time: int) -> None:
        pass

    def draw(self) -> None:
        self.surface.fill(Color.BLACK)

        title = self.font.render("HIGHSCORES", True, Color.WHITE)
        title_rect = title.get_rect(
            center=(self.width // 2, self.height // 4)
        )
        self.surface.blit(title, title_rect)

        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.scores) * line_height
        row_start_y = self.height // 2 - total_height // 4

        col_rank_x = self.width * (6/20)
        col_name_x = self.width * (7/20)
        col_score_x = self.width * (14/20)

        colors = [
            Color.RED,
            Color.ORANGE,
            Color.YELLOW,
            Color.LIME,
            Color.GREEN,
            Color.TEAL,
            Color.CYAN,
            Color.BLUE,
            Color.PURPLE,
            Color.MAGENTA
        ]

        for i, el in enumerate(self.scores):
            rank = self.font.render(str(i + 1), True, colors[i])
            rank_rect = rank.get_rect(
                midright=(col_rank_x, row_start_y + i * line_height)
            )
            self.surface.blit(rank, rank_rect)
            name = self.font.render(str(el["username"]), True, colors[i])
            name_rect = name.get_rect(
                midleft=(col_name_x, row_start_y + i * line_height)
            )
            self.surface.blit(name, name_rect)
            score = self.font.render(str(el["score"]), True, colors[i])
            score_rect = score.get_rect(
                midright=(col_score_x, row_start_y + i * line_height)
            )
            self.surface.blit(score, score_rect)
